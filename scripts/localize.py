#!/usr/bin/env python3
"""Self-host third-party images used in README.md (run by the 'Localize images' Action).
  localize : download external <img src="https://..."> into assets/ext/ and rewrite README
  refresh  : re-download everything in assets/ext/sources.json (failures keep the old file)
"""
import hashlib, json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXT = ROOT / "assets" / "ext"
SRC = EXT / "sources.json"
README = ROOT / "README.md"
UA = {"User-Agent": "Mozilla/5.0 (profile-readme-localizer)"}
KEEP = ("raw.githubusercontent.com", "github.com/dipanshubatra")
DROP = ("komarev.com",)


def fetch(url, tries=3):
    for i in range(tries):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read()
            if b"<svg" in data[:600]:
                return data
        except Exception:
            pass
        time.sleep(2)
    return None


def slug(url):
    name = re.sub(r"https?://(www\.)?", "", url.split("?")[0]).strip("/")
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name)[:40].strip("-")
    return f"{name}-{hashlib.md5(url.encode()).hexdigest()[:6]}.svg"


def load():
    return json.loads(SRC.read_text()) if SRC.exists() else {}


def localize():
    EXT.mkdir(parents=True, exist_ok=True)
    text = README.read_text(encoding="utf-8")
    for tag in re.findall(r'<img[^>]*src="https?://[^"]*"[^>]*/?>', text):
        if any(d in tag for d in DROP):
            text = text.replace(tag, "")
    sources, failed = load(), []
    for url in dict.fromkeys(re.findall(r'<img[^>]*src="(https?://[^"]+)"', text)):
        if any(k in url for k in KEEP):
            continue
        clean = url.replace("&amp;", "&")
        fname = slug(clean)
        data = fetch(clean)
        if data is None:
            failed.append(clean)
            print("FAIL", clean[:90], flush=True)
            continue
        (EXT / fname).write_bytes(data)
        sources[f"assets/ext/{fname}"] = clean
        text = text.replace(f'src="{url}"', f'src="assets/ext/{fname}"')
        print("ok  ", fname, flush=True)
    README.write_text(text, encoding="utf-8")
    SRC.write_text(json.dumps(sources, indent=2, sort_keys=True))
    print(f"\n{len(failed)} failed")


def refresh():
    for path, url in load().items():
        data = fetch(url, tries=2)
        if data:
            (ROOT / path).write_bytes(data)
            print("refreshed", path, flush=True)
        else:
            print("kept old ", path, flush=True)


mode = sys.argv[1] if len(sys.argv) > 1 else "localize"
{"localize": localize, "refresh": refresh}[mode]()
