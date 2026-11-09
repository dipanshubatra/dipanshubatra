#!/usr/bin/env python3
"""Extra section headings in the marker style (reuses gen_about_notes.heading).
Run from repo root: python3 scripts/gen_headings.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_cover_notes as c
import gen_about_notes as a

HEADS = {"hd-journey.svg": ("06", "journey", c.LIME, c.PINK, "// the story so far")}
if __name__ == "__main__":
    for name, args in HEADS.items():
        (c.D / name).write_text(a.heading(*args), encoding="utf-8"); print("wrote", name)
