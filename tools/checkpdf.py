#!/usr/bin/env python3
"""Check the finished PDFs for layout defects no log can see.

Every other gate in this repository reads the source or the log. This one reads
the artefact, because the defect it exists for produces neither an error, nor a
warning, nor an overfull box:

    a frame's rule and its margin badge are the last things on a page, and the
    frame's body is overleaf.

The badge is the book's navigation device -- a reader thumbing for frame 37 runs
a finger down the edge of the block -- and a badge that names a frame not on the
page defeats the one thing it is for.

It cannot be prevented by a constant. `\\begin{fr}` reserves room before it draws
the rule, and that reservation IS NOT MONOTONIC: measured over F1, reserving six
baselineskips stranded a frame that five did not, because a larger reservation
turns pages earlier and reshuffles every later break. So the constant is tuned
against this check, and this check is what makes the tuning honest.

Usage:
    tools/checkpdf.py main-en.pdf main-pl.pdf main-en-a4.pdf main-pl-a4.pdf

Needs pdftotext (poppler). Exits non-zero if any PDF strands a frame opener.
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

RE_PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
RE_WORD = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')

# How far outside the text block a word must sit to count as a margin badge,
# and how far below the top of the page, so the page number in the outer head
# is not mistaken for one. The head sits in the top tenth in both formats.
MARGIN_SLACK = 2.0
HEAD_FRACTION = 0.10


def words(page_body: str):
    for a, b, c, d, t in RE_WORD.findall(page_body):
        yield float(a), float(b), float(c), float(d), t


def text_block(pages) -> tuple[float, float]:
    """The left and right edges of the text block, as the document's own modes.

    Derived from the artefact rather than from the geometry options, so the
    check keeps working when the geometry changes -- which it did once already,
    when the A4 format was added.
    """
    left, right = Counter(), Counter()
    for _, _, body in pages:
        for x0, _, x1, _, _ in words(body):
            left[round(x0)] += 1
            right[round(x1)] += 1
    return float(left.most_common(1)[0][0]), float(right.most_common(1)[0][0])


def check(path: Path) -> list[tuple[int, list[str]]]:
    xml = subprocess.run(["pdftotext", "-bbox", str(path), "-"],
                         capture_output=True, text=True, check=True).stdout
    pages = RE_PAGE.findall(xml)
    lo, hi = text_block(pages)
    stranded = []
    for pno, (_, ph, body) in enumerate(pages, start=1):
        ph = float(ph)
        ws = list(words(body))
        if not ws:
            continue
        candidates = [w for w in ws
                      if w[4].strip().isdigit()
                      and (w[2] < lo - MARGIN_SLACK or w[0] > hi + MARGIN_SLACK)
                      and w[1] > ph * HEAD_FRACTION]
        # A frame badge stands ALONE beside its rule: nothing in the text block
        # shares its line. Without this, every table-of-contents entry and every
        # index entry is a badge, because both end in a number at the right
        # edge -- with their title on the same line, which is the tell.
        badges = [w for w in candidates
                  if not any(lo - MARGIN_SLACK <= v[0] <= hi + MARGIN_SLACK
                             and v[1] < w[3] and v[3] > w[1]
                             for v in ws)]
        if not badges:
            continue
        lowest = max(w[3] for w in badges)
        body_below = [w for w in ws
                      if w[1] > lowest + 1
                      and lo - MARGIN_SLACK <= w[0] <= hi + MARGIN_SLACK]
        if not body_below:
            stranded.append((pno, [w[4].strip() for w in badges]))
    return stranded


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ok = True
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"== {path} == MISSING")
            ok = False
            continue
        stranded = check(path)
        if stranded:
            ok = False
            print(f"== {path.name} == {len(stranded)} STRANDED FRAME OPENER(S)")
            for pno, badges in stranded:
                print(f"      PDF page {pno}: frame {', '.join(badges)} "
                      f"opens at the foot of the page and its body is overleaf")
            print("      Re-sweep the reservation in \\begin{fr} (preamble.tex)")
            print("      against this check. A LARGER number is not a safer one.")
        else:
            print(f"== {path.name} == no stranded frame openers")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
