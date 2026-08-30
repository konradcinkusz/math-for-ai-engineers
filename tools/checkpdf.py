#!/usr/bin/env python3
"""Check the finished PDFs for layout defects no log can see.

Every other gate in this repository reads the source or the log. This one reads
the artefact, because the two defects it exists for produce neither an error,
nor a warning, nor an overfull box. They are mirror images of each other, and
they sit at the two ends of a frame.

    1. STRANDED OPENER. A frame's rule and its margin badge are the last things
       on a page, and the frame's body is overleaf.

       The badge is the book's navigation device -- a reader thumbing for frame
       37 runs a finger down the edge of the block -- and a badge that names a
       frame not on the page defeats the one thing it is for.

    2. ORPHANED CUE. The other end of the same frame: the question, its
       \\dotline and everything else are on one page, and the next-frame cue is
       alone on the next one, under nothing. The reader turns over expecting
       the answer and is met by a running head, two italic words and white
       paper.

       This is not cosmetic. The cue is the instruction the whole method rests
       on -- cover the page, answer, then turn -- and a cue with no question
       above it instructs nothing. Measured on the tree that added this check:
       three such pages, one of them in F3, and every gate in the repository
       was green.

       The mechanism is worth writing down, because it is not the reservation
       above. \\dotline ends `\\par\\vspace{2pt}`, and glue after a paragraph is a
       legal breakpoint; \\nextframe's own leading \\nopagebreak is contributed
       after that glue and so arrives too late to forbid it. The fix is
       therefore editorial -- shorten the frame so the tail fits -- and NOT a
       penalty bolted onto \\dotline, which was tried, measured and reverted.

Neither can be prevented by a constant. `\\begin{fr}` reserves room before it
draws the rule, and that reservation IS NOT MONOTONIC: measured over F1,
reserving six baselineskips stranded a frame that five did not, because a
larger reservation turns pages earlier and reshuffles every later break. So the
constant is tuned against this check, and this check is what makes the tuning
honest.

Usage:
    tools/checkpdf.py main-en.pdf main-pl.pdf main-en-a4.pdf main-pl-a4.pdf

Needs pdftotext (poppler). Exits non-zero on either defect in any PDF.
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

# How far below the running head's own baseline the body starts. A fraction of
# the page height is the wrong instrument for this one: on A4 the first body
# line sits at 77.4 pt on an 841.9 pt page, which is INSIDE the top tenth, so
# HEAD_FRACTION would discard the very line this check is looking for. The head
# is found by its own position instead -- see head_baseline.
HEAD_GAP = 5.0

LANG_DIR = Path(__file__).resolve().parent.parent / "lang"


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


def cue_strings() -> set[str]:
    """The next-frame cue, in every language the book is set in.

    Read from lang/*.tex rather than written here, because a check that
    hard-codes the string it looks for stops looking the day somebody rewords
    the cue -- silently, and in exactly the direction that makes the ledger
    lie. If no cue can be found the caller is told, rather than being handed a
    green result from a check that ran on an empty set.
    """
    cues = set()
    for path in sorted(LANG_DIR.glob("*.tex")):
        for m in re.finditer(r"\\newcommand\*?\{?\\lblNextFrame\}?\{([^}]*)\}",
                             path.read_text(encoding="utf8")):
            cues.add(" ".join(m.group(1).split()))
    return cues


def head_baseline(pages) -> float:
    """The y of the running head, as the document's own mode.

    Every page but a chapter opener carries one, so the topmost word's yMin is
    the head's on the large majority of pages and the mode is unambiguous.
    """
    tops = Counter()
    for _, _, body in pages:
        ys = [w[1] for w in words(body)]
        if ys:
            tops[round(min(ys))] += 1
    return float(tops.most_common(1)[0][0])


def check(path: Path, cues: set[str]) -> tuple[list[tuple[int, list[str]]],
                                              list[tuple[int, str]]]:
    """Both defects, from one parse of the artefact.

    Returns (stranded openers, orphaned cues) as lists of (page, detail).
    """
    xml = subprocess.run(["pdftotext", "-bbox", str(path), "-"],
                         capture_output=True, text=True, check=True).stdout
    pages = RE_PAGE.findall(xml)
    lo, hi = text_block(pages)
    head = head_baseline(pages)
    stranded: list[tuple[int, list[str]]] = []
    orphans: list[tuple[int, str]] = []
    for pno, (_, ph, body) in enumerate(pages, start=1):
        ph = float(ph)
        ws = list(words(body))
        if not ws:
            continue

        # --- 2. the orphaned cue -------------------------------------------
        # Everything below the running head, in reading order. If that is the
        # cue and nothing else, the page carries an instruction with nothing to
        # instruct: the question it belongs to is on the page before.
        # A run of dots is \dotline, not content: a page carrying the row of
        # dots and the cue is the same defect one breakpoint earlier, and it
        # would otherwise read as a page with something on it.
        below_head = [w for w in ws
                      if w[1] > head + HEAD_GAP and set(w[4]) != {"."}]
        if below_head:
            line = " ".join(w[4] for w in
                            sorted(below_head, key=lambda w: (round(w[1]), w[0])))
            if line in cues:
                orphans.append((pno, line))

        # --- 1. the stranded opener ----------------------------------------
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
    return stranded, orphans


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cues = cue_strings()
    if not cues:
        print("== checkpdf == NO CUE STRING FOUND in lang/*.tex")
        print("      \\lblNextFrame is how this tool recognises the cue. Without")
        print("      it the orphaned-cue check would pass on everything, so it")
        print("      fails here instead of running on an empty set.")
        return 1
    ok = True
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"== {path} == MISSING")
            ok = False
            continue
        stranded, orphans = check(path, cues)
        if stranded:
            ok = False
            print(f"== {path.name} == {len(stranded)} STRANDED FRAME OPENER(S)")
            for pno, badges in stranded:
                print(f"      PDF page {pno}: frame {', '.join(badges)} "
                      f"opens at the foot of the page and its body is overleaf")
            print("      Re-sweep the reservation in \\begin{fr} (preamble.tex)")
            print("      against this check. A LARGER number is not a safer one.")
        if orphans:
            ok = False
            print(f"== {path.name} == {len(orphans)} ORPHANED NEXT-FRAME CUE(S)")
            for pno, line in orphans:
                print(f"      PDF page {pno}: [{line}] is the only thing on the "
                      f"page; its question is overleaf")
            print("      Shorten the frame so its question, dots and cue fit on one")
            print("      page. Do NOT bolt a penalty onto \\dotline: that was tried,")
            print("      measured and reverted, and it moves every later break.")
        if not stranded and not orphans:
            print(f"== {path.name} == no stranded frame openers, no orphaned cues")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
