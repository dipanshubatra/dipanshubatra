#!/usr/bin/env python3
"""Generates assets/ui/oss-note-1..3.svg (section 07 Open Source) in the same notebook style as Journey.
Run from repo root: python3 scripts/gen_oss_notes.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_journey as g

OSS = [  # tag, title, caption, sticker big, sticker label, accent, done
    ("KRAMU81/MEDTRACK_APPLICATION", "medtrack",              "94 commits. the big one.",                               "94",  "COMMITS",  "#ffe14d", True),
    ("NICODE2707/MAILGENIE",         "mailgenie",             "24 commits. my share, shipped.",                         "24",  "COMMITS",  "#ff7eb6", True),
    ("JAVA / SPRING ECOSYSTEM",      "the rest of the repos", "16+ open-source projects and still going.",              "16+", "PROJECTS", "#6c8cff", True),
]
for i in range(len(OSS)):
    (g.D / f"oss-note-{i+1}.svg").write_text(g.build(i, OSS), encoding="utf-8")
    print("wrote", f"oss-note-{i+1}.svg")
