#!/usr/bin/env python3
"""Structural ledgers for the book.

Each check answers one question that a reader would care about and that nobody
can be trusted to remember:

  --frames    Is every program inside the 30-70 frame band the method assumes,
              does every frame that asks a question get answered by the next
              one, and does every frame number the program QUOTES -- every Quiz
              route, every outcome range, every Summary bracket -- name a frame
              that exists?
  --answers   Does every test exercise and further problem have an answer?
  --outcomes  Does every written program declare its learning outcomes?
  --values    Is every \\val{} reference backed by a computed value, and is
              every computed value used?
  --scripts   Does every \\transcript{} name a file that exists?

Exit code is 0 when the ledger is clean and 1 when it is not, so any of these
can be turned into a hard CI gate by dropping the --soft flag.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "pl")
FRAME_BAND = (30, 70)

# The band is a statement about TEACHING LOAD -- how much a reader can hold in
# one sitting -- and it assumes a program that has a subject's worth of
# material. One program deliberately does not, and the deliberateness is the
# point rather than a shortfall.
#
# F13's brief, after the curriculum review cut it from forty-five frames, says
# in as many words: "NOT a course in integration technique: substitution,
# parts and partial fractions are excluded deliberately and by name, because
# nothing this book pays off needs them... Twenty frames rather than
# forty-five, and the difference is the point."
#
# Padding it back into the band would mean writing the material the scope
# excludes, which is exactly what CLAUDE.md warns against. So the band is
# taken from the manifest when the manifest plans fewer frames than the band's
# floor: such a program must land within a quarter of ITS OWN plan, which is a
# real check rather than a waiver -- a twenty-frame plan that came out at
# forty would still fail.
#
# Read from tools/programs.json rather than hard-coded here, so a curriculum
# change moves the check with it.
def _planned() -> dict[str, int]:
    import json
    data = json.loads((ROOT / "tools" / "programs.json").read_text(encoding="utf8"))
    progs = data["programs"] if isinstance(data, dict) and "programs" in data else data
    return {p["file"]: int(p["frames"]) for p in progs if "file" in p and "frames" in p}


PLANNED = _planned()


def band_for(stem: str) -> tuple[int, int]:
    """The band this program is held to, and why it might not be the default."""
    plan = PLANNED.get(stem)
    if plan is not None and plan < FRAME_BAND[0]:
        return (int(plan * 0.75), int(plan * 1.25) + 1)
    return FRAME_BAND


RE_STUB = re.compile(r"\\programstub\{")
# \begin{fr} only, deliberately. The Summary and the Test exercises are
# numbered frames too -- the preamble frames them, so they carry the last two
# numbers a reader sees -- but they are fixed overhead every program pays and
# they are not teaching frames. This ledger counts TEACHING frames, which is
# what the 30--70 band is a statement about, so F01 reports 45 while the book
# prints 47. Do not "fix" one counter without the other; every program's band
# would shift by two.
RE_FRAME = re.compile(r"\\begin\{fr\}")
RE_ANS = re.compile(r"\\ans\{|\\begin\{ansblock\}")
RE_OUTCOME = re.compile(r"\\outcome\{")
RE_ANSWERTO = re.compile(r"\\answerto\{")
RE_VAL = re.compile(r"\\(?:raw)?val\{([^}]+)\}")
RE_TRANSCRIPT = re.compile(r"\\transcript\{([^}]*)\}")
RE_MFAVAL = re.compile(r"\\mfaval\{([^}]+)\}")
# An exercise item: \item at the top level of one of the three list
# environments. Counted per environment rather than globally, because the
# answer key is prefixed by environment.
RE_ENV = re.compile(
    r"\\begin\{(quiz|testexercises|furtherproblems)\}(.*?)\\end\{\1\}", re.S
)
RE_ITEM = re.compile(r"^\s*\\item\b", re.M)
# A frame demands a response if it contains a row of dots, hands the reader a
# worked example to do, or ends by telling them to turn over. The dots and the
# cue are the reliable signals; a question mark is a hint.
#
# \nextframe is in this list because it IS the demand made explicit: it is the
# instruction to cover the page and turn over. That makes the check and the
# placement rule the same rule -- a cue may only sit on a frame the next frame
# answers -- and parity's C16 enforces the converse, that every such frame
# carries one.
RE_DEMANDS = re.compile(r"\\blank|\\dotline|\\yourturn|\\nextframe")

# The four macros whose FIRST argument is a frame number or a range of them.
# Together they are the whole of the book's return index: \teachesat and
# \teachesatone route a failed Quiz question to the frames that teach it,
# \outcome tells the reader where an outcome was earned, and \sumitem carries
# the bracket that sends a Summary line back to the frames behind it.
#
# Until this check existed those payloads were compared BETWEEN the editions
# and never against the program. parity's C4 and C12 both see \teachesat{91--93}
# in a 48-frame program as correct, because the Polish edition says 91--93 too;
# a probe that routed a Quiz question there passed every gate in the repository.
# F02 lost a review round to three of these, found by a person reading.
#
# What is checked here is EXISTENCE and shape -- an endpoint past the last
# frame, a range that runs backwards, a payload that is not a frame range at
# all. Whether frame 20 actually answers the question routed to it stays a
# reading job, and no tool in this repository claims otherwise.
RE_RANGE = re.compile(r"\\(teachesatone|teachesat|outcome|sumitem)\{([^}]*)\}")
RE_RANGE_ARG = re.compile(r"\A(\d+)(?:--(\d+))?\Z")


def program_files(lang: str) -> list[Path]:
    return sorted((ROOT / "programs" / lang).glob("*.tex"))


def written(text: str) -> bool:
    return not RE_STUB.search(text)


def check_frames(soft: bool) -> int:
    bad = 0
    for lang in LANGS:
        for f in program_files(lang):
            t = f.read_text(encoding="utf8")
            if not written(t):
                continue
            frames = RE_FRAME.findall(t)
            n = len(frames)
            band = band_for(f.stem)
            if not (band[0] <= n <= band[1]):
                note = "" if band == FRAME_BAND else "  (its own plan's band)"
                print(f"  {lang}/{f.stem}: {n} frames, outside {band}{note}")
                bad += 1
            # Every frame that demands a response must be followed by a frame
            # that opens with an answer. This is the method failing silently
            # when it is wrong, which is why it is checked rather than trusted.
            blocks = re.split(r"\\begin\{fr\}", t)[1:]
            for i, b in enumerate(blocks[:-1], start=1):
                if RE_DEMANDS.search(b) and not RE_ANS.search(blocks[i]):
                    print(
                        f"  {lang}/{f.stem}: frame {i} asks for a response and "
                        f"frame {i + 1} does not open with an answer"
                    )
                    bad += 1
            # And the cue is the LAST thing in its frame, as preamble.tex says
            # where \nextframe is defined. It tells the reader to cover the
            # page and turn over, so anything printed after it is printed after
            # the reader has gone.
            #
            # This is a LINE test, not a token test, and that is not a style
            # preference. parity's C16 counts cues per frame and cannot see
            # position, so a cue misplaced identically in both editions is
            # invisible to C4, to C14 and to C16 alike; and a token test has
            # its own blind spot, because a cue hoisted above a frame's
            # closing PROSE tokenises to nothing after it and reads as
            # correctly placed. Only the line test catches both.
            for i, b in enumerate(blocks, start=1):
                body = b.split(r"\end{fr}")[0].splitlines()
                for k, line in enumerate(body):
                    if line.strip() != r"\nextframe":
                        continue
                    after = [x for x in body[k + 1:] if x.strip()
                             and not x.lstrip().startswith("%")]
                    if after:
                        print(
                            f"  {lang}/{f.stem}: frame {i}: \\nextframe is not "
                            f"the last thing in the frame -- "
                            f"{after[0].strip()[:44]!r} follows it"
                        )
                        bad += 1
            # And every frame number the program quotes names a frame that
            # exists. The ceiling is the TEACHING frame count, deliberately:
            # the Summary and the Test exercises are printed frames too, but
            # nothing routes a reader to them -- they are where the reader
            # already is -- so a payload reaching past the last teaching frame
            # is a defect in every case seen so far.
            for m in RE_RANGE.finditer(t):
                macro, arg = m.group(1), m.group(2).strip()
                shape = RE_RANGE_ARG.match(arg)
                if shape is None:
                    print(
                        f"  {lang}/{f.stem}: \\{macro}{{{arg}}} is not a frame "
                        f"number or an n--m range"
                    )
                    bad += 1
                    continue
                lo = int(shape.group(1))
                hi = int(shape.group(2)) if shape.group(2) else lo
                if lo < 1:
                    print(f"  {lang}/{f.stem}: \\{macro}{{{arg}}} starts before frame 1")
                    bad += 1
                if shape.group(2) and hi <= lo:
                    print(
                        f"  {lang}/{f.stem}: \\{macro}{{{arg}}} does not ascend "
                        f"-- a range of one frame is written {{{lo}}}"
                    )
                    bad += 1
                if hi > n:
                    print(
                        f"  {lang}/{f.stem}: \\{macro}{{{arg}}} names frame {hi}, "
                        f"and the program has {n} teaching frames"
                    )
                    bad += 1
    if bad == 0:
        print("  Every written program is in band, every question is answered, "
              "and every frame number quoted exists.")
    return 0 if (bad == 0 or soft) else 1


def check_elicitation(soft: bool) -> int:
    """Report what fraction of each program's frames put a question to the reader.

    REPORTED, NEVER FATAL, and for the reason the orphan-tail ledger is: there
    is no defensible threshold, and a gate that is red on something nobody can
    responsibly clear teaches the next person to stop reading the output.

    It exists because this number decayed for seventeen programs and every gate
    in the repository stayed green while it did. A frame carries \nextframe if
    and only if the next frame opens with an answer, so the cue rate IS the
    elicitation rate, measured rather than asserted. It ran at 73-78% through
    F01-F06, 50-66% through F08-F13, and 26-31% across the whole of Part II --
    which is the book turning from programmed instruction into prose, one
    program at a time, in the one property the whole design rests on.

    \blank and \yourturn are counted beside it because they are distinct
    retrieval modes rather than decoration: \blank is a gap inside a worked
    line, \yourturn a question with its answer overleaf. The last \yourturn in
    the book is in F04 and the last \blank is in F07. Nothing noticed.

    RE_DEMANDS treats all four alike, so a program using \nextframe and nothing
    else passes check_frames, parity C16, C4 and C14 without a murmur. This
    counter is the only thing that looks at the ratio.
    """
    rows = []
    for f in program_files("en"):
        t = f.read_text(encoding="utf8")
        if not written(t):
            continue
        n = len(RE_FRAME.findall(t))
        if n < 5:
            continue
        cues = t.count(r"\nextframe")
        rows.append((f.stem, n, cues, t.count(r"\blank"), t.count(r"\yourturn")))
    if not rows:
        print("  No written program to measure.")
        return 0
    for stem, n, cues, blanks, turns in rows:
        print(f"  {stem:<30} {cues:>3}/{n:<3} frames elicit "
              f"({100 * cues // n:>3}%)   blank {blanks:>2}   yourturn {turns:>2}")
    total_f = sum(r[1] for r in rows)
    total_c = sum(r[2] for r in rows)
    print(f"  {'BOOK':<30} {total_c:>3}/{total_f:<3} frames elicit "
          f"({100 * total_c // total_f:>3}%)")
    print("  Reported, never fatal. When the rate falls, that is the signal.")
    return 0


def check_answers(soft: bool) -> int:
    bad = 0
    for lang in LANGS:
        for f in program_files(lang):
            t = f.read_text(encoding="utf8")
            if not written(t):
                continue
            for env, body in ((m.group(1), m.group(2)) for m in RE_ENV.finditer(t)):
                items = len(RE_ITEM.findall(body))
                answers = len(RE_ANSWERTO.findall(body))
                if items != answers:
                    print(
                        f"  {lang}/{f.stem}: {env} has {items} items and "
                        f"{answers} answers"
                    )
                    bad += 1
    if bad == 0:
        print("  Every exercise in every written program has an answer.")
    return 0 if (bad == 0 or soft) else 1


def check_outcomes(soft: bool) -> int:
    bad = 0
    for lang in LANGS:
        for f in program_files(lang):
            t = f.read_text(encoding="utf8")
            if not written(t):
                continue
            n = len(RE_OUTCOME.findall(t))
            if n == 0:
                print(f"  {lang}/{f.stem}: declares no learning outcomes")
                bad += 1
            elif n < 4:
                print(f"  {lang}/{f.stem}: only {n} learning outcomes")
                bad += 1
    if bad == 0:
        print("  Every written program declares its outcomes; 'Can you?' is generated from them.")
    return 0 if (bad == 0 or soft) else 1


def check_values(soft: bool) -> int:
    defined: set[str] = set()
    for f in (ROOT / "figures" / "values").glob("*.tex"):
        defined |= set(RE_MFAVAL.findall(f.read_text(encoding="utf8")))

    used: set[str] = set()
    for d in ("programs", "appendices", "frontmatter"):
        for f in (ROOT / d).rglob("*.tex"):
            used |= set(RE_VAL.findall(f.read_text(encoding="utf8")))

    missing = sorted(used - defined)
    unused = sorted(defined - used)
    for k in missing:
        print(f"  MISSING: \\val{{{k}}} has no computed value. Run `make numbers`.")
    if unused:
        print(f"  {len(unused)} computed value(s) nothing references: {', '.join(unused[:6])}"
              + (" ..." if len(unused) > 6 else ""))
    if not missing and not unused:
        print(f"  {len(defined)} computed values, all referenced, all present.")
    return 0 if (not missing or soft) else 1


# A \transcript{} that names nothing prints a grey marker and builds.
#
# That fallback is deliberate -- figures/transcripts is written by `make
# numbers`, so a clean checkout has none and the draft build has to survive it
# -- and it is also how TEN OF THE TWELVE TRANSCRIPTS IN THIS BOOK went nine
# programs without reaching a page. The macro used to take a path and nine call
# sites passed a stem, so \IfFileExists looked for `p06-order.tex`, failed, and
# printed "TRANSCRIPT NOT COMPUTED" in grey with a label, which reads exactly
# like somebody's decision. Every gate stayed green: `make verify` compares the
# file against the script that wrote it and never asks whether a page includes
# it, checklog reads the log, checkpdf reads the layout, and parity compares
# the two editions -- which agreed, because both were wrong.
#
# The macro now takes the stem, so the wrong call is impossible rather than
# detectable. This check is the second half: on a tree where `make numbers` has
# run, a \transcript naming a file that is not there is a typo and nothing
# else, and it is worth failing on BEFORE the build rather than after it. It
# also refuses a path, because a path is the old form and would silently
# resolve to figures/transcripts/figures/transcripts/....
def check_scripts(soft: bool) -> int:
    tdir = ROOT / "figures" / "transcripts"
    bad = 0
    total = 0
    for lang in LANGS:
        for f in program_files(lang) + sorted((ROOT / "appendices").glob(f"*-{lang}.tex")):
            for stem in RE_TRANSCRIPT.findall(f.read_text(encoding="utf8")):
                total += 1
                if "/" in stem or stem.endswith(".txt"):
                    print(f"  {f.relative_to(ROOT)}: \\transcript{{{stem}}} is a path; "
                          f"the argument is a bare stem")
                    bad += 1
                elif not (tdir / f"{stem}.txt").exists():
                    print(f"  {f.relative_to(ROOT)}: \\transcript{{{stem}}} names no file "
                          f"(figures/transcripts/{stem}.txt). Run `make numbers`.")
                    bad += 1
    if bad == 0:
        print(f"  {total} transcript references, every one backed by a committed file.")
    return 0 if (bad == 0 or soft) else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frames", action="store_true")
    p.add_argument("--answers", action="store_true")
    p.add_argument("--outcomes", action="store_true")
    p.add_argument("--values", action="store_true")
    p.add_argument("--elicit", action="store_true")
    p.add_argument("--scripts", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--soft", action="store_true",
                   help="report but always exit 0 (the default for a draft)")
    a = p.parse_args()
    if not any((a.frames, a.answers, a.outcomes, a.values, a.elicit,
                a.scripts, a.all)):
        a.all = True
    rc = 0
    if a.all or a.frames:
        rc |= check_frames(a.soft)
    if a.all or a.answers:
        rc |= check_answers(a.soft)
    if a.all or a.outcomes:
        rc |= check_outcomes(a.soft)
    if a.all or a.values:
        rc |= check_values(a.soft)
    if a.all or a.elicit:
        rc |= check_elicitation(a.soft)
    if a.all or a.scripts:
        rc |= check_scripts(a.soft)
    return rc


if __name__ == "__main__":
    sys.exit(main())
