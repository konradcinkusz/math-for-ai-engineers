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

    3. STRANDED SECTION HEADING. A numbered section heading is the last thing
       on a page and the section itself begins overleaf.

       Same mechanism as 1, one element earlier: `\\begin{fr}` measures the room
       left and turns the page when a frame will not fit, and by then the
       \\section before it has already been set. The heading stays behind.

       This was PERVASIVE and unnoticed. When the check was written it found
       10, 14, 9 and 9 headings left behind in the four builds, in every
       program from F1 to F4 -- and every other gate was green, because a
       heading at the foot of a page produces no error, no warning and no
       overfull box. \\section now carries the same room test \\begin{fr} has,
       sized for the heading as well; this check is what keeps it honest.

    4. ORPHAN TAIL. A body page whose ink stops in its top quarter: the reader
       turns over for the answer and is met by two lines and white paper.

       Defect 2 is its extreme case, where the tail is the cue alone. The cue
       test cannot see this one, because the page carries a line or two above
       the cue and is therefore not "the cue and nothing else".

       Three classes of page are excluded, and each exclusion is about there
       being nothing to pull back rather than about being inconvenient:

         * a blank verso;
         * a part page and a chapter opener, which carry no running head and
           are laid out by their own rules;
         * THE LAST PAGE OF A CHAPTER OR APPENDIX, because a short one is the
           chapter ending and not a frame breaking badly. The reader's next
           turn lands on an opener, which is a signposted transition and not
           two orphaned lines; and the last page of the index or of a
           generated manifest is short by construction, so a check that named
           it could never come clean. Detected as: the next page that carries
           any ink at all has no running head, or there is no next page.

None of the four can be prevented by a constant. `\\begin{fr}` reserves room
before it draws the rule, and that reservation IS NOT MONOTONIC: measured over
F1, reserving six baselineskips stranded a frame that five did not, because a
larger reservation turns pages earlier and reshuffles every later break. The
same is true of the section reservation defect 3 answers to. So the constants
are tuned against this check, and this check is what makes the tuning honest.

Usage:
    tools/checkpdf.py main-en.pdf main-pl.pdf main-en-a4.pdf main-pl-a4.pdf

Needs pdftotext (poppler). 1 and 3 are structural and always fatal. 2 is
fatal unless --cues=warn is passed. 4 is reported in full and never fatal --
see the note above main() for why, and read the count rather than the exit
code.
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

# A numbered section heading opens with its number: F4.7 in a program, B.2 in
# an appendix. \section* -- the Quiz, Can you?, the manifests, the front matter
# -- has no number and is deliberately not matched: none of those is followed
# by a frame, and the Quiz carries a room test of its own.
RE_SECNO = re.compile(r"^[A-Z]?\d*\.\d+$")

# How high up the text block a body page's ink may stop before the page reads
# as a tail rather than as a page. MEASURED, not chosen: see the sweep in the
# note above main().
FILL_FLOOR = 0.25

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


def text_blocks(pages, head: float) -> dict[int, tuple[float, float]]:
    """The left and right edges of the text block, PER PAGE PARITY.

    Derived from the artefact rather than from the geometry options, so the
    check keeps working when the geometry changes -- which it did once already,
    when the A4 format was added.

    Per parity because THE MARGINS ARE MIRRORED. A verso's block starts at 51 pt
    in the trade format and a recto's at 62 pt, so a single mode over the whole
    document describes one of the two and is 11 pt wrong about the other. That
    was survivable for the badge test, which only asks whether a word is well
    outside the block, and it is not survivable for a test that asks where the
    ink on a page stops.

    Head words are excluded, because the outer page number sits at the block's
    own left edge on a verso and would otherwise vote in its own favour.
    """
    per: dict[int, tuple[Counter, Counter]] = {0: (Counter(), Counter()),
                                               1: (Counter(), Counter())}
    for pno, (_, _, body) in enumerate(pages, start=1):
        left, right = per[pno % 2]
        for x0, y0, x1, _, _ in words(body):
            if y0 <= head + HEAD_GAP:
                continue
            left[round(x0)] += 1
            right[round(x1)] += 1
    return {k: (float(left.most_common(1)[0][0]), float(right.most_common(1)[0][0]))
            for k, (left, right) in per.items()}


def lines_of(ws):
    """The words of one page grouped into lines, keyed by rounded yMin."""
    lines: dict[int, list] = {}
    for w in ws:
        lines.setdefault(round(w[1]), []).append(w)
    return {y: sorted(l, key=lambda w: w[0]) for y, l in lines.items()}


def heading_metrics(pages, blocks, head) -> tuple[float, int]:
    """The word height a numbered section heading is set at, and how many there
    are.

    Calibrated from the document rather than written here, for the reason
    cue_strings is: a hard-coded size stops matching the day the heading font
    changes, and it stops matching silently. The heading is NOT simply "taller
    than the body" -- \\Large bold measures 12.6 pt to the body's 14.2 pt in the
    trade format, because pdftotext reports the font's own box and the two
    fonts have different depths. So the size is learnt, not assumed.

    Returns (height, count); a count of zero means the caller must not trust a
    green result.
    """
    heights = Counter()
    for pno, (_, _, body) in enumerate(pages, start=1):
        lo, _ = blocks[pno % 2]
        for _, line in lines_of(w for w in words(body)
                                if w[1] > head + HEAD_GAP).items():
            if RE_SECNO.match(line[0][4]) and abs(line[0][0] - lo) < MARGIN_SLACK:
                heights[round(line[0][3] - line[0][1], 1)] += 1
    if not heights:
        return 0.0, 0
    height, count = heights.most_common(1)[0]
    return float(height), count


def is_heading(line, lo: float, height: float) -> bool:
    """Is this line a numbered section heading?

    Three things at once, because the section number alone is not enough: an
    English body line may begin `0.9`, and a Polish one may not. The height test
    is what tells the heading from the decimal.
    """
    return (RE_SECNO.match(line[0][4]) is not None
            and abs(line[0][0] - lo) < MARGIN_SLACK
            and abs((line[0][3] - line[0][1]) - height) < 0.3)


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


def chapter_final(pages, head: float) -> set[int]:
    """The pages after which a chapter or appendix opener begins.

    A page with no running head is an opener or a part page: every other page
    carries one. Blank versos are skipped over, because a chapter that starts
    recto leaves one between itself and the page this is really about -- and
    note that a blank verso here is blank in the BODY only: this book's
    \cleardoublepage leaves the running head on it, so a page with nothing but
    a head is what has to be skipped rather than a page with nothing at all.
    """
    inked = [pno for pno, (_, _, body) in enumerate(pages, start=1)
             if any(w[1] > head + HEAD_GAP for w in words(body))]
    openers = {pno for pno, (_, _, body) in enumerate(pages, start=1)
               if pno in inked
               and min(w[1] for w in words(body)) > head + HEAD_GAP}
    final = {inked[-1]} if inked else set()
    for a, b in zip(inked, inked[1:]):
        if b in openers:
            final.add(a)
    return final


def foot_baseline(pages, blocks, head: float) -> float:
    """The y the text block ends at, as the document's own mode.

    A full page ends on the last line of the block, and most pages are full, so
    the mode is the block's foot. It is what the fill fraction is measured
    against, so that a page is judged against the page it could have been and
    not against the paper.
    """
    bottoms = Counter()
    for pno, (_, _, body) in enumerate(pages, start=1):
        lo, hi = blocks[pno % 2]
        ys = [w[3] for w in words(body)
              if w[1] > head + HEAD_GAP
              and lo - MARGIN_SLACK <= w[0] <= hi + MARGIN_SLACK]
        if ys:
            bottoms[round(max(ys))] += 1
    return float(bottoms.most_common(1)[0][0])


def check(path: Path, cues: set[str]):
    """All four defects, from one parse of the artefact.

    Returns (stranded openers, orphaned cues, stranded headings, orphan tails,
    heading count) -- the last so the caller can refuse to report a green
    heading result from a calibration that found nothing to calibrate on.
    """
    xml = subprocess.run(["pdftotext", "-bbox", str(path), "-"],
                         capture_output=True, text=True, check=True).stdout
    pages = RE_PAGE.findall(xml)
    head = head_baseline(pages)
    blocks = text_blocks(pages, head)
    foot = foot_baseline(pages, blocks, head)
    sec_h, sec_n = heading_metrics(pages, blocks, head)
    finals = chapter_final(pages, head)
    top = head + HEAD_GAP
    stranded: list[tuple[int, list[str]]] = []
    orphans: list[tuple[int, str]] = []
    headings: list[tuple[int, str]] = []
    tails: list[tuple[int, float, str]] = []
    for pno, (_, ph, body) in enumerate(pages, start=1):
        ph = float(ph)
        lo, hi = blocks[pno % 2]
        ws = list(words(body))
        if not ws:
            continue
        in_block = [w for w in ws
                    if w[1] > top and lo - MARGIN_SLACK <= w[0] <= hi + MARGIN_SLACK]

        # --- 3. the stranded section heading -------------------------------
        # The last line of the block is a heading, so its section starts on the
        # next page. Worth the same weight as a stranded opener: both promise
        # the reader something the page does not then carry.
        if sec_n and in_block:
            lines = lines_of(in_block)
            last = lines[max(lines)]
            if is_heading(last, lo, sec_h):
                headings.append((pno, " ".join(w[4] for w in last)))

        # --- 4. the orphan tail --------------------------------------------
        # A page with a running head is a body page; a part page and a chapter
        # opener have none, are laid out by their own rules, and are excluded.
        # A page with nothing in the block is a blank verso and is excluded by
        # the same test.
        if in_block and pno not in finals and min(w[1] for w in ws) <= head + HEAD_GAP:
            fill = (max(w[3] for w in in_block) - top) / (foot - top)
            if fill < FILL_FLOOR:
                first = lines_of(in_block)
                head_line = " ".join(w[4] for w in first[min(first)])
                tails.append((pno, fill, head_line[:60]))

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
    return stranded, orphans, headings, tails, sec_n


# The orphaned cue does not fail the build when --cues=warn is passed, and CI
# passes it. THE ORPHAN TAIL NEVER FAILS THE BUILD, on any invocation. Neither
# is the gate going soft; both are the gate being honest about what it can
# know, and the second needs its reasoning stated rather than assumed.
#
# The tail is a PRE-EXISTING CLASS. When the check was written it named 15
# pages -- one in the trade English build, six in the trade Polish, four in
# each A4 -- of which thirteen are in F1, F2 and F3 and two are F4's, both in
# the A4 English build alone. Clearing the thirteen means cutting a sentence of
# prose out of three programs that have already been written and reviewed, in
# two languages, to move one line on ONE of four paginations -- and each such
# cut reshuffles every later break in that language, so all four have to be
# satisfied at once. Measured on the tree this was written on: a line is about
# 180 characters on A4 and 150 in the trade format, and the largest saving
# available in those frames without dropping a claim was about fifty.
#
# So making it fatal would leave `make check` red on a defect nobody can
# responsibly clear, which teaches the next person to stop reading the output.
# It is REPORTED IN FULL on every run instead, page by page, so the ledger
# cannot go quiet -- the same treatment this book gives the 80/80 standard,
# and for the same reason: it is a claim that cannot be gated, so it is
# printed rather than dropped. CLAUDE.md carries the list. WHEN THE COUNT
# GOES UP, that is the signal; the tool cannot give it to you, so read it.
#
# All four defects are defects of PAGINATION, and this repository builds on two
# TeX installations that paginate differently: the container that writes the
# published PDF has neither newtx nor inconsolata, the CI image has both, and
# the same source gives an overfull multiset of [4.1 x 4] here against
# [1.2 x 4] there. Every line in the book breaks in a different place.
#
# The stranded opener and the stranded heading survive that, because the
# reservations behind them are measured in \baselineskip and hold under either
# metric: they are a statement about a frame or a heading and the room in front
# of it, not about where a particular line falls. The orphaned cue and the
# orphan tail do not: each is one frame's tail landing a line past a page
# boundary, so its LOCATION is a property of the installation. Trimming the
# line CI names would fix CI and move the defect here, and trimming the line
# this container names would do the reverse -- an unwinnable loop in which the
# author chases a machine they cannot see.
#
# So: hard where a person can act on it (make check, on the author's own
# build), reported where they cannot (CI). The defect is not dismissed and the
# count is printed either way. The real fix for both is structural -- the tail
# of a frame should be incapable of standing alone -- and it is open; three
# attempts are recorded in preamble.tex with their measurements, and all three
# made it worse or did nothing.
#
# FILL_FLOOR WAS SWEPT, not chosen. It is the fraction of the text block a body
# page's ink has to reach. Against the build this check was written on:
#
#   floor   pages named (en / pl / en-A4 / pl-A4)
#   0.05    0 / 0 / 0 / 0
#   0.10    1 / 6 / 4 / 4
#   0.15    1 / 6 / 4 / 4
#   0.25    1 / 6 / 4 / 4      <- chosen
#   0.35    1 / 6 / 4 / 4
#   0.50    1 / 6 / 4 / 5
#
# The interesting result is that IT IS A PLATEAU. Every page this names carries
# between 7 and 10 per cent of a block, and the next page up the distribution
# is at 50. There is no page in this book that stops between a tenth and a half
# of the way down, so the floor may be put anywhere in that gap and name the
# same set; a quarter is the middle of the gap and it is about ten lines, which
# is where a page stops reading as a page. The plateau is what makes the
# constant safe, and it is the thing to re-measure rather than the constant.


def main() -> int:
    argv = [a for a in sys.argv[1:] if a != "--cues=warn"]
    soft = "--cues=warn" in sys.argv[1:]
    if not argv:
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
    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"== {path} == MISSING")
            ok = False
            continue
        stranded, orphans, headings, tails, sec_n = check(path, cues)
        if not sec_n:
            ok = False
            print(f"== {path.name} == NO NUMBERED SECTION HEADING FOUND")
            print("      The stranded-heading check calibrates itself on the")
            print("      headings it can see. Finding none means it would pass")
            print("      on everything, so it fails here instead.")
        if stranded:
            ok = False
            print(f"== {path.name} == {len(stranded)} STRANDED FRAME OPENER(S)")
            for pno, badges in stranded:
                print(f"      PDF page {pno}: frame {', '.join(badges)} "
                      f"opens at the foot of the page and its body is overleaf")
            print("      Re-sweep the reservation in \\begin{fr} (preamble.tex)")
            print("      against this check. A LARGER number is not a safer one.")
        if headings:
            ok = False
            print(f"== {path.name} == {len(headings)} STRANDED SECTION HEADING(S)")
            for pno, line in headings:
                print(f"      PDF page {pno}: [{line}] is the last thing on the "
                      f"page; its section begins overleaf")
            print("      Re-sweep the reservation in \\mfa@sectionroom (preamble.tex)")
            print("      against this check. A LARGER number is not a safer one.")
        for found, label, fatal, detail in (
                (orphans, "ORPHANED NEXT-FRAME CUE(S)", not soft,
                 lambda d: f"[{d[1]}] is the only thing on the page; "
                           f"its question is overleaf"),
                (tails, "ORPHAN TAIL PAGE(S)", False,
                 lambda d: f"ink stops at {d[1]:.0%} of the block: "
                           f"[{d[2]}...]")):
            if not found:
                continue
            ok = ok and not fatal
            name = label if fatal else label.lower() + ", reported not fatal"
            print(f"== {path.name} == {len(found)} {name}")
            for d in found:
                print(f"      PDF page {d[0]}: {detail(d)}")
            print("      Shorten the frame so its tail fits on one page. Do NOT bolt")
            print("      a penalty onto \\dotline: that was tried, measured and")
            print("      reverted, and it moves every later break.")
            if not fatal:
                print("      Not failing the build: see the note at the top of this")
                print("      file for what this count is and is not.")
        if not (stranded or orphans or headings or tails) and sec_n:
            print(f"== {path.name} == no stranded frame openers, no stranded "
                  f"section headings, no orphaned cues, no orphan tails")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
