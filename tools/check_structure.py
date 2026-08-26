#!/usr/bin/env python3
"""Structural ledgers for the book.

Each check answers one question that a reader would care about and that nobody
can be trusted to remember:

  --frames    Is every program inside the 30-70 frame band the method assumes,
              and does every frame that asks a question get answered by the
              next one?
  --answers   Does every test exercise and further problem have an answer?
  --outcomes  Does every written program declare its learning outcomes?
  --values    Is every \\val{} reference backed by a computed value, and is
              every computed value used?

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

RE_STUB = re.compile(r"\\programstub\{")
RE_FRAME = re.compile(r"\\begin\{fr\}")
RE_ANS = re.compile(r"\\ans\{|\\begin\{ansblock\}")
RE_OUTCOME = re.compile(r"\\outcome\{")
RE_ANSWERTO = re.compile(r"\\answerto\{")
RE_VAL = re.compile(r"\\(?:raw)?val\{([^}]+)\}")
RE_MFAVAL = re.compile(r"\\mfaval\{([^}]+)\}")
# An exercise item: \item at the top level of one of the three list
# environments. Counted per environment rather than globally, because the
# answer key is prefixed by environment.
RE_ENV = re.compile(
    r"\\begin\{(quiz|testexercises|furtherproblems)\}(.*?)\\end\{\1\}", re.S
)
RE_ITEM = re.compile(r"^\s*\\item\b", re.M)
# A frame demands a response if it contains a row of dots or ends in a
# question. The dots are the reliable signal; the question mark is a hint.
RE_DEMANDS = re.compile(r"\\blank|\\dotline|\\yourturn")


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
            if not (FRAME_BAND[0] <= n <= FRAME_BAND[1]):
                print(f"  {lang}/{f.stem}: {n} frames, outside {FRAME_BAND}")
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
    if bad == 0:
        print("  Every written program is in band and every question is answered.")
    return 0 if (bad == 0 or soft) else 1


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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frames", action="store_true")
    p.add_argument("--answers", action="store_true")
    p.add_argument("--outcomes", action="store_true")
    p.add_argument("--values", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--soft", action="store_true",
                   help="report but always exit 0 (the default for a draft)")
    a = p.parse_args()
    if not any((a.frames, a.answers, a.outcomes, a.values, a.all)):
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
    return rc


if __name__ == "__main__":
    sys.exit(main())
