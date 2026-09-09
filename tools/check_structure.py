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
  --results   Does every \\result{} mark for Appendix C sit inside the
              Summary item whose frame range it prints?
  --terms     Does every Polish rendering Appendix D names actually occur
              in the prose of programs/pl?
  --rigour    Does Appendix E name a destination for every rigour box that
              sends the reader outside the book?
  --index     Does every NAME an \\index{} entry prints occur in the prose of
              the file the mark sits in?

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
# The same declaration read for its VALUE as well as its key, which is what
# lets a page outside the book be checked against the book's own arithmetic.
RE_MFAVAL_PAIR = re.compile(r"\\mfaval(?:text)?\{([^}]+)\}\{([^}]*)\}")
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
            # DECLARING the outcomes is not the same as PRINTING the panel,
            # and this check said the second while testing only the first. Its
            # own message -- "'Can you?' is generated from them" -- is the
            # sentence a reader takes it for, and under it P05, P06, P07 and
            # P08 shipped with no panel at all. C14 is blind to it too, because
            # both editions lacked it and the histograms therefore agreed.
            if "\\canyou" not in t:
                print(f"  {lang}/{f.stem}: declares outcomes but never calls "
                      f"\\canyou, so no 'Can you?' panel is printed")
                bad += 1
            else:
                # And the ORDER carries meaning: \lblCanYouFooter sends the
                # reader from the self-rating to the scored Test exercises as
                # the instrument, so a program that scores first inverts its
                # own footer. Four did.
                i_can = t.index("\\canyou")
                i_test = t.find("\\begin{testexercises}")
                if 0 <= i_test < i_can:
                    print(f"  {lang}/{f.stem}: Test exercises come before "
                          f"'Can you?', which inverts the footer's own logic")
                    bad += 1
    if bad == 0:
        print("  Every written program declares its outcomes, prints its "
              "'Can you?' panel, and prints it before the Test exercises.")
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


# ---------------------------------------------------------------------------
# --results: Appendix C's coordinates, which cannot be wrong ONLY IF the mark
# sits where it can pick one up.
#
# The whole design of that appendix is that nothing in it is transcribed:
# \result{...} marks a span of a Summary item, and the program key and frame
# range it stores are the ones LaTeX is on when it reads the mark. Appendix B
# was hand-authored, shipped four false pointers, and cost two separate passes
# to find them by reading; Appendix C is built so that class cannot arise.
#
# The range does not come from the mark. It comes from \sumitem, which stashes
# it in \mfa@sumfr for the mark to pick up -- so a \result written ANYWHERE
# ELSE silently inherits whichever Summary item was read last, or, in a program
# whose Summary has not been reached, the \providecommand fallback, and prints
# `[?]`. Either way the appendix carries a coordinate the mark never earned,
# which is exactly the defect it exists to make impossible.
#
# NOTHING ELSE SEES IT, and that was measured rather than assumed: a probe
# \result placed outside every Summary item, in BOTH editions, left parity,
# --frames, --answers, --outcomes, --values, --scripts and gen_stubs --check
# all green. It has to be both editions to be interesting -- C14 counts every
# macro generically, so a mark added to one edition alone already fails -- and
# an edit made in both is the recorded shape of the defect this repository
# keeps being bitten by: a check that is wrong in the same way in both editions
# stays green and only the ledger lies.
#
# Two smaller faults ride along on the same parse, because both cost one line
# and neither is visible anywhere else. A mark nested inside another mark
# stores its text twice, so the appendix prints the inner formula on its own
# line and again inside the outer one. And an empty mark prints a bullet, no
# formula and a coordinate, which reads as damage.
RE_RESULT = re.compile(r"\\result\{")
RE_SUMITEM = re.compile(r"\\sumitem\{")


def _blank_comments(s: str) -> str:
    """TeX comments out, offsets preserved.

    The line numbers this check reports have to name the line in the file, so
    the comment is replaced by spaces of its own length rather than removed.
    """
    return re.sub(r"(?<!\\)%[^\n]*", lambda m: " " * len(m.group(0)), s)


def _group_end(s: str, open_brace: int) -> int | None:
    """Index one past the `}` matching the `{` at open_brace, or None."""
    depth = 0
    i = open_brace
    while i < len(s):
        c = s[i]
        if c == "\\":            # \{ and \} are literal braces, not grouping
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def _second_arg_spans(text: str, opener: re.Pattern) -> list[tuple[int, int]]:
    """The body (second argument) of every \\sumitem{range}{body} in text."""
    out = []
    for m in opener.finditer(text):
        first = _group_end(text, m.end() - 1)
        if first is None:
            continue
        j = first
        while j < len(text) and text[j] in " \n\t":
            j += 1
        if j < len(text) and text[j] == "{":
            second = _group_end(text, j)
            if second is not None:
                out.append((j, second))
    return out


def check_results(soft: bool) -> int:
    bad = 0
    marked = 0
    items = 0
    for lang in LANGS:
        for f in program_files(lang):
            raw = f.read_text(encoding="utf8")
            text = _blank_comments(raw)
            bodies = _second_arg_spans(text, RE_SUMITEM)
            items += len(bodies)
            marks = []
            for m in RE_RESULT.finditer(text):
                end = _group_end(text, m.end() - 1)
                if end is None:
                    continue
                marks.append((m.start(), m.end(), end))
            for start, body_open, end in marks:
                marked += 1
                where = f"{f.relative_to(ROOT)}:{text[:start].count(chr(10)) + 1}"
                if not any(a <= start < b for a, b in bodies):
                    print(f"  {where}: \\result outside every \\sumitem body. "
                          f"The frame range comes from \\sumitem, so this mark "
                          f"would print whichever range was read last.")
                    bad += 1
                if any(o < start and end <= e for o, _, e in marks
                       if (o, e) != (start, end)):
                    print(f"  {where}: \\result nested inside another one; "
                          f"Appendix C would print its text twice.")
                    bad += 1
                if not text[body_open:end - 1].strip():
                    print(f"  {where}: empty \\result{{}} -- a bullet and a "
                          f"coordinate with no formula between them.")
                    bad += 1
    if bad == 0:
        print(f"  {marked // len(LANGS)} results marked for Appendix C in each "
              f"edition, every one inside the Summary item whose frame range "
              f"it prints ({items // len(LANGS)} Summary items in all; an item "
              f"that is a caveat rather than a result is deliberately unmarked).")
    _report_contract_bypass()
    return 0 if (bad == 0 or soft) else 1


# The second half, and it is REPORTED rather than fatal.
#
# Appendix C is the one place in the book where the notation contract has to
# hold exactly: it is entered by somebody looking a formula up, with none of
# the section around it, so a spelling that disagrees with Appendix B there is
# worse than no reference at all.
#
# The contract is implemented as macros in lang/{en,pl}.tex so the SOURCE is
# identical and only the output differs -- \gcdop sets `gcd` in English and
# `NWD` in Polish, \spanof sets `span` and `lin`. Writing \operatorname{gcd}
# instead sets `gcd` in both, which is a one-edition divergence that no parity
# check can see, because both editions carry the same wrong token.
#
# C10 forbids exactly one of these spellings, \operatorname{lcm}. The contract
# owns ten operators. So the list here is READ OUT OF lang/en.tex rather than
# typed, and an operator added to the contract is covered the day it is added.
#
# It does not fail the build, on the treatment this book gives every ledger
# nobody can responsibly clear in the pass that finds it: the sites it names
# are in a merged program, the fix is a substitution that changes no glyph
# today, and a gate that is red on somebody else's file teaches the next person
# to stop reading the output. Printed on every run instead. When the count goes
# up, that is the signal.
RE_DECLARE_OP = re.compile(r"\\DeclareMathOperator\{\\(\w+)\}\{([^{}]*)\}")


def _contract_operators() -> dict[str, str]:
    """{raw spelling -> the macro that owns it}, read from the contract."""
    text = (ROOT / "lang" / "en.tex").read_text(encoding="utf8")
    out: dict[str, str] = {}
    for macro, setting in RE_DECLARE_OP.findall(text):
        for wrapper in ("operatorname", "mathrm", "text"):
            out[f"\\{wrapper}{{{setting}}}"] = f"\\{macro}"
    return out


def _report_contract_bypass() -> None:
    ops = _contract_operators()
    hits: list[tuple[str, str, str]] = []
    for lang in LANGS:
        for f in program_files(lang):
            text = _blank_comments(f.read_text(encoding="utf8"))
            for mo in RE_RESULT.finditer(text):
                end = _group_end(text, mo.end() - 1)
                if end is None:
                    continue
                span = text[mo.end():end - 1]
                for raw, macro in ops.items():
                    if raw in span:
                        line = text[:mo.start()].count(chr(10)) + 1
                        hits.append((f"{f.relative_to(ROOT)}:{line}", raw, macro))
    if not hits:
        print("  Every marked span spells the contract's operators through "
              "their macros.")
        return
    print(f"  {len(hits)} marked spans hard-code an operator the notation "
          f"contract owns a macro for. Both editions carry the same token, so "
          f"no parity check can see it, and Appendix C replays it verbatim:")
    for where, raw, macro in hits:
        print(f"    {where}: {raw} -- use {macro}")
    print("  Reported, never fatal.")


# ---------------------------------------------------------------------------
# --terms: Appendix D is a claim about the body on every line.
#
# A glossary row naming a word the book does not use is the failure that
# matters, and it is not hypothetical: the suggested table in notes/03 carries
# rows for `dropout` and `ground truth`, neither of which appears anywhere in
# either edition. Nothing else in this repository would have said so.
#
# TWO THINGS THIS CHECK LEARNED FROM BEING WRONG FIRST.
#
# It reads PROSE, not source. A substring count over raw LaTeX counts a label
# and a value key as usage: an audit of this appendix reported `feature` used
# four times in the Polish edition (all four were \val{f10.features}) and
# `attention` used once (it was \label{sec:P25-attention}). Both would have
# licensed a row for a word the prose never writes. Maths spans go too, because
# \partial contains `parti` and would vouch for `partia` on its own.
#
# And it matches on a STEM rather than the whole word, because Polish inflects
# every one of these -- uwaga/uwagi/uwage, warstwa/warstwie. The stem is crude
# on purpose. The gate's job is to catch a word that occurs ZERO times in any
# inflection, which is a gross failure; a stem loose enough to over-match is
# the safe direction, and a word-boundary match would fail on nearly every row.
RE_PLTERM = re.compile(r"\\plterm\{[^{}]*\}\{([^{}]*)\}")
RE_TEX_COMMENT = re.compile(r"(?<!\\)%.*")
RE_TEX_ARGS = re.compile(
    r"\\(?:label|index|ref|val|rawval|cite|code|api|pkg)\{[^{}]*\}")
RE_MATHS = re.compile(r"\$[^$]*\$")


def _stem(word: str) -> str:
    w = word.lower()
    return w[:-2] if len(w) > 6 else (w[:-1] if len(w) > 4 else w)


def check_terms(soft: bool) -> int:
    prose = []
    for f in program_files("pl"):
        t = RE_TEX_COMMENT.sub("", f.read_text(encoding="utf8"))
        t = RE_TEX_ARGS.sub(" ", t)
        t = RE_MATHS.sub(" ", t)
        prose.append(t.lower())
    body = "\n".join(prose)

    bad = 0
    total = 0
    for lang in LANGS:
        f = ROOT / "appendices" / lang / "appD-terminology.tex"
        if not f.exists():
            continue
        src = f.read_text(encoding="utf8")
        for arg in RE_PLTERM.findall(src):
            for rendering in (r.strip() for r in arg.split(",")):
                if not rendering:
                    continue
                total += 1
                missing = [w for w in rendering.split()
                           if _stem(w) not in body]
                if missing:
                    print(f"  {f.relative_to(ROOT)}: \\plterm names "
                          f"{rendering!r}, which the prose of programs/pl does "
                          f"not use ({', '.join(missing)} absent). A glossary "
                          f"row for a word the book does not write is a claim "
                          f"about the body that is false.")
                    bad += 1
    if bad == 0:
        print(f"  {total} Polish renderings named in Appendix D, "
              f"every one used in the prose.")
    return 0 if (bad == 0 or soft) else 1


RE_INDEX = re.compile(r"\\index\{((?:[^{}]|\{[^{}]*\})*)\}")
# A NAME, for this check: a run of letters, at least two long, carrying at
# least one capital. That is the decidable half of an index entry and the only
# half worth a gate -- see the note above check_index().
RE_NAME = re.compile(r"[A-Za-z]*[A-Z][A-Za-z]*")
# \DeclareMathOperator{\relu}{ReLU} and \newcommand{\tg}{...}: what the source
# writes as a macro and the page prints as a word. Learnt from the preamble
# and the language files rather than listed here, the way checkpdf.py learns
# the next-frame cue out of lang/*.tex rather than hard-coding it -- so a new
# operator cannot make this check start lying.
RE_OPERATOR = re.compile(
    r"\\(?:DeclareMathOperator\*?|newcommand\*?|providecommand\*?)"
    r"\{?\\([A-Za-z@]+)\}?(?:\[\d\])?\{([^{}]*)\}")


def _printed_forms() -> dict[str, str]:
    forms: dict[str, str] = {}
    for f in (ROOT / "preamble.tex", ROOT / "lang" / "en.tex",
              ROOT / "lang" / "pl.tex"):
        if f.exists():
            for macro, body in RE_OPERATOR.findall(f.read_text(encoding="utf8")):
                forms.setdefault("\\" + macro, body)
    return forms


def check_index(soft: bool) -> int:
    r"""An index entry that names something the page never prints.

    The index is the one artefact in this book whose coordinates rest entirely
    on where an \index{} mark happens to sit, and a review of it found the two
    ways that goes wrong: a mark parked at a section opener several pages
    before the term it names, and -- worse -- \index{optimiser!AdamW} against a
    program that deliberately never writes the word, so the index asserted by
    its existence that the book discusses AdamW under that name.

    Only the second is checkable from the source, and only for part of an
    entry. Most index leaves in this book are DESCRIPTIONS rather than terms
    ("what it omits", "as an inverse", "and the ELBO"), so the obvious check --
    assert the leaf occurs in the prose -- reports most of the book and is the
    permanently red ledger CLAUDE.md refuses. Measured before this was
    written, by taking each leaf's longest content word and asking whether it
    occurs in the file at all: of the 926 marks across the two editions it
    reports a hundred and thirty, the Polish far worse than the English
    because Polish inflects and a stem match is not available. Almost every
    one of the hundred and thirty is a description doing its job.

    A NAME is the decidable half. AdamW, PageRank, Thompson, ELBO, PCA, SVD,
    Jacobian: a capitalised token either appears in the file or it does not,
    and if it does not then the index has named something the reader cannot
    find. Over the same 926 marks about eighty carry such a token, and once
    the three this pass found were cleared every one of them is printed. So
    this is a hard gate on a clean, narrow class rather than a ledger on a
    wide one, and the count it prints is the ledger.

    A see-reference is exempt by construction: \index{SVD|see{singular value
    decomposition}} names another ENTRY, not a word in the body, and saying so
    is the whole point of the device.
    """
    forms = _printed_forms()
    bad = 0
    marks = names = 0
    for lang in LANGS:
        for f in program_files(lang):
            src = f.read_text(encoding="utf8")
            prose = RE_TEX_COMMENT.sub("", RE_INDEX.sub("", src))
            # A macro the page prints as a word counts as the word.
            for macro, body in forms.items():
                if macro in prose:
                    prose += " " + body
            for m in RE_INDEX.finditer(src):
                marks += 1
                entry = m.group(1)
                # A see-reference names another ENTRY rather than a word in
                # the body, and its head is by construction a word the book
                # does NOT print -- that is why it needs a see. Both halves
                # are exempt, and the whole mark is skipped.
                if re.search(r"\|\s*(?:seealso|see)\b", entry):
                    continue
                payload = entry.split("|")[0]
                shown = " ".join(seg.split("@")[-1]
                                 for seg in payload.split("!"))
                for token in RE_NAME.findall(shown):
                    if len(token) < 2:
                        continue
                    names += 1
                    if token not in prose:
                        line = src[:m.start()].count("\n") + 1
                        print(f"  {f.relative_to(ROOT)}:{line}: index entry "
                              f"{payload!r} names {token!r}, which this file "
                              f"never prints. An index entry for a word the "
                              f"body does not write sends the reader to a page "
                              f"that does not carry it.")
                        bad += 1
    if bad == 0:
        print(f"  {names} names in {marks} index entries, "
              f"every one printed in its own program.")
    return 0 if (bad == 0 or soft) else 1


# THE README AND THE LANDING PAGE PRINT DIGITS AND NOTHING PUT A SCRIPT
# BEHIND THEM.
#
# `README.md` and `docs/index.html` are the shop window: each argues that
# every number in this book is computed rather than remembered, and each made
# that argument with the same five figures typed into a table by hand -- one
# defect in two artefacts, which is this repository's own recurring finding
# that fixing an instance is not fixing the class. They were correct when this check was
# written -- all five re-derived from figures/values/f01.tex -- which is the
# same standing every fabricated console block in this repository's record had
# on the day it was written. The book's own numbers are gated by `make verify`;
# these sat outside every gate the repository has, in the one artefact a reader
# meets before the book.
#
# So a figure on that page carries the key it came from, and this compares the
# rendered text against what the script now computes. It fires in the direction
# that actually breaks it -- a value moving under a page nobody edited -- and
# `make verify` cannot see that, because the values file and its script still
# agree perfectly.
#
# Note the asymmetry in where it runs: build.yml carries `paths-ignore:
# docs/**`, so a docs-only pull request runs no CI at all, and it is pages.yml
# -- which has no paths-ignore -- that catches an edit to the page itself
# before anything is published.
RE_SITE_VAL = re.compile(r'data-val="([^"]+)"\s*>([^<]*)<')


SITE_PAGES = ("docs/index.html", "README.md")


def check_site(soft: bool) -> int:
    computed: dict[str, str] = {}
    for f in sorted((ROOT / "figures" / "values").glob("*.tex")):
        for key, value in RE_MFAVAL_PAIR.findall(f.read_text(encoding="utf8")):
            computed[key] = value

    bad = 0
    total = 0
    for rel in SITE_PAGES:
        page = ROOT / rel
        if not page.exists():
            print(f"  {rel} is not there; a page this check is written for "
                  f"has been renamed or removed.")
            bad += 1
            continue

        tagged = RE_SITE_VAL.findall(page.read_text(encoding="utf8"))
        if not tagged:
            print(f"  {rel} tags no figure with the value that produced it. "
                  f"A digit on that page is a claim with no script behind it.")
            bad += 1
            continue
        total += len(tagged)

        for key, shown in tagged:
            shown = shown.strip()
            if key not in computed:
                print(f"  {rel}: data-val=\"{key}\" names no computed value. "
                      f"Run `make numbers`, or correct the key.")
                bad += 1
            elif shown != computed[key]:
                print(f"  {rel}: {key} is shown as {shown!r} and code/ now "
                      f"computes {computed[key]!r}.")
                bad += 1

    if not bad:
        print(f"  {total} figures across {len(SITE_PAGES)} pages a reader "
              f"meets before the book, every one the value its script "
              f"computes.")
    return 0 if (not bad or soft) else 1


RE_PARTRANGE = re.compile(r"\(([FP]\d+)--([FP]\d+)\)")


def check_parts(soft: bool) -> int:
    """Every part range the introduction prints against the manifest.

    This is the one class of claim that the parity checks are structurally
    blind to. C4, C8, C12 and C14 all compare the two EDITIONS, so a range
    that is stale in both stays green -- and both introductions carried the
    P7-insertion off-by-one in seven of their nine ranges for the whole of
    the book, on page one, with every gate passing. The fix is the one this
    repository has reached for every other time: compare against the source
    of truth (tools/programs.json) rather than between the editions.

    The ranges are read positionally, in document order, because the part
    names differ between the editions by design and the manifest carries
    both. A missing or extra range is therefore a failure too.
    """
    import json
    manifest = json.loads((ROOT / "tools" / "programs.json")
                          .read_text(encoding="utf8"))
    want = [(p["ids"][0], p["ids"][-1]) for p in manifest["parts"]]

    bad = 0
    for lang in LANGS:
        f = ROOT / "frontmatter" / lang / "introduction.tex"
        if not f.exists():
            continue
        src = RE_TEX_COMMENT.sub("", f.read_text(encoding="utf8"))
        got = RE_PARTRANGE.findall(src)
        if len(got) != len(want):
            print(f"  {f.relative_to(ROOT)}: prints {len(got)} part ranges "
                  f"where the manifest has {len(want)} parts.")
            bad += 1
            continue
        for i, (g, w) in enumerate(zip(got, want), start=1):
            if g != w:
                print(f"  {f.relative_to(ROOT)}: part {i} prints "
                      f"({g[0]}--{g[1]}) where the manifest says "
                      f"({w[0]}--{w[1]}). The introduction is the book's own "
                      f"map and it prints on page one.")
                bad += 1
    if bad == 0:
        print(f"  {len(want)} part ranges in each introduction, "
              f"every one matching the manifest.")
    return 0 if (bad == 0 or soft) else 1


RE_RIGOUR = re.compile(r"\\begin\{rigourbox\}(.*?)\\end\{rigourbox\}", re.S)
RE_PROGREF = re.compile(r"\\ref\{prog:(\w+)\}")
RE_ROUTE_SECTION = re.compile(
    r"\\label\{sec:E-route\}(.*?)(?=\n\\section|\Z)", re.S)
RE_TABULARX = re.compile(
    r"\\begin\{tabularx\}\{[^}]*\}\{[^}]*\}(.*?)\\end\{tabularx\}", re.S)


def check_rigour(soft: bool) -> int:
    """Appendix E names a destination for every rigour box that leaves the book.

    A rigour box says: here is a result, it is not proved here, and here is
    where the proof lives. Most point at another program; the ones that point
    OUTSIDE the book named a kind of course and, with one exception, no title,
    so the reader was sent to "any first analysis course" and left to find
    one. The count is deliberately not stated here -- a tally of occurrences
    decays silently, which is why this prints the number it has just computed
    rather than one somebody wrote down.

    STILL OUTSTANDING, and this check cannot see it: nothing in the book
    references Appendix E. There is no \\ref{app:E} in any program, so a
    reader standing at a rigour box has no way to know the destination exists.
    Fixing that means editing every deferring program, which is a pass of its
    own.

    The mechanical half is exact and is what this checks. A box that defers
    INSIDE the book cites the program it defers to, so a box containing no
    \\ref{prog:...} cannot be deferring inside it: it is outward-facing by
    construction, and Appendix E owes it a row. The criterion is
    edition-stable -- both editions carry the same fourteen -- which is why
    the check can be run against each and is not merely comparing them.

    Parity is blind to this in the way it is blind to every claim about the
    book: C4, C8, C12 and C14 all compare the two EDITIONS, so a row missing
    from both stays green. That is the same shape as the seven part ranges
    that were wrong in both introductions for the whole of the book.

    WHAT THIS DOES NOT CHECK, and the tool says so rather than letting a green
    ledger imply otherwise: whether the destination named actually contains
    the proof. That is a reading job, and five of Appendix E's own rows say
    "not surveyed" precisely because nobody has done it for those subjects.
    """
    bad = 0
    for lang in LANGS:
        app = ROOT / "appendices" / lang / "appE-further-reading.tex"
        if not app.exists():
            continue
        src = RE_TEX_COMMENT.sub("", app.read_text(encoding="utf8"))
        m = RE_ROUTE_SECTION.search(src)
        if not m:
            print(f"  {app.relative_to(ROOT)}: no route section "
                  f"(\\label{{sec:E-route}}). Every rigour box that leaves "
                  f"the book needs a destination and this is where they live.")
            bad += 1
            continue
        # The SECOND column of every route row is "Deferred from" and is
        # the only one that names a source; the third names a destination,
        # which may itself be a program of this book (P25's residual box is
        # answered in P32) and must not be read as a program that defers.
        # Parsed positionally rather than by the shape of the reference,
        # because that distinction is the whole content of the check.
        routed: set[str] = set()
        for body in RE_TABULARX.findall(m.group(1)):
            for row in body.split(r"\\"):
                cells = row.split("&")
                if len(cells) >= 2:
                    routed |= set(RE_PROGREF.findall(cells[1]))

        outward: dict[str, int] = {}
        for f in program_files(lang):
            text = RE_TEX_COMMENT.sub("", f.read_text(encoding="utf8"))
            if not written(text):
                continue
            stem = f.name.split("-")[0]
            for box in RE_RIGOUR.findall(text):
                if not RE_PROGREF.search(box):
                    outward[stem] = outward.get(stem, 0) + 1

        for stem in sorted(set(outward) - routed):
            print(f"  {lang}: {stem} has a rigour box that defers outside "
                  f"the book and Appendix E names no destination for it. "
                  f"A reader sent to \"a first course\" with no title is "
                  f"sent nowhere.")
            bad += 1
        have = {f.name.split("-")[0] for f in program_files(lang)
                if RE_RIGOUR.search(f.read_text(encoding="utf8"))}
        for stem in sorted(routed - have):
            if stem in {f.name.split("-")[0] for f in program_files(lang)}:
                print(f"  {lang}: Appendix E routes a rigour box to {stem}, "
                      f"which carries none. The row is stale.")
                bad += 1
    if bad == 0:
        print(f"  {len(outward)} programs defer a result outside the book; "
              f"Appendix E names a destination, or says it has none, for "
              f"every one.")
    return 0 if (bad == 0 or soft) else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frames", action="store_true")
    p.add_argument("--answers", action="store_true")
    p.add_argument("--outcomes", action="store_true")
    p.add_argument("--values", action="store_true")
    p.add_argument("--elicit", action="store_true")
    p.add_argument("--scripts", action="store_true")
    p.add_argument("--results", action="store_true")
    p.add_argument("--terms", action="store_true")
    p.add_argument("--parts", action="store_true")
    p.add_argument("--site", action="store_true")
    p.add_argument("--rigour", action="store_true")
    p.add_argument("--index", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--soft", action="store_true",
                   help="report but always exit 0 (the default for a draft)")
    a = p.parse_args()
    if not any((a.frames, a.answers, a.outcomes, a.values, a.elicit,
                a.scripts, a.results, a.terms, a.parts, a.rigour,
                a.site,
                a.index, a.all)):
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
    if a.all or a.results:
        rc |= check_results(a.soft)
    if a.all or a.terms:
        rc |= check_terms(a.soft)
    if a.all or a.parts:
        rc |= check_parts(a.soft)
    if a.all or a.site:
        rc |= check_site(a.soft)
    if a.all or a.rigour:
        rc |= check_rigour(a.soft)
    if a.all or a.index:
        rc |= check_index(a.soft)
    return rc


if __name__ == "__main__":
    sys.exit(main())
