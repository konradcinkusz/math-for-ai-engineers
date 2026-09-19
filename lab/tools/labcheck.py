#!/usr/bin/env python3
"""The lab's own gates. Run from the repository root.

    python3 lab/tools/labcheck.py --files    the exercise and solution files
                                             agree with each other and with the
                                             checks that call them
    python3 lab/tools/labcheck.py --tests    the reference solutions pass every
                                             check and the untouched stubs pass
                                             none
    python3 lab/tools/labcheck.py --guard REF   nothing the book's build reads
                                             changed relative to REF
    python3 lab/tools/labcheck.py --all      --files and --tests

Exit 0 clean, 1 defect, 2 usage.

WHY --tests RUNS THE STUBS AS WELL AS THE SOLUTIONS. A check that passes on an
empty exercise file is not a check, and CLAUDE.md records five instruments in
three passes that accepted their input and returned a plausible answer. So the
gate watches the instrument produce a KNOWN answer in both directions before
anything else is believed: every check must pass on lab/solutions/ and every
check must fail, or report itself as not implemented, on lab/exercises/.

WHY --guard IS AN ALLOW-LIST AND NOT A DENY-LIST. The lab is additive on the
KDP pattern: it reads preamble.tex and figures/values/ and writes nothing the
book reads. The cheapest proof of that is the diff -- every changed path must be
one the lab is allowed to change -- and an allow-list stays correct when the
book grows a directory, where a deny-list silently stops covering it.
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "lab"

# The widest line the exercise files may carry. A half-screen editor pane
# beside the book shows about this much of a line without wrapping; it is a
# first figure, not a measurement, and is here to be swept rather than assumed.
MEASURE = 72

RE_REGION = re.compile(r"^# region: ([\w-]+)\s*$", re.M)
RE_ENDREGION = re.compile(r"^# endregion: ([\w-]+)\s*$", re.M)
RE_TEST = re.compile(r"^def (test_\w+)\(", re.M)

# Paths a change to the lab may touch. Everything else is the book's, or the
# book's build's, and a diff reaching it means the lab stopped being additive.
# `.gitignore` is here because the content compiler's render test installs
# KaTeX, and a node_modules the guard forbids ignoring is a guard that makes
# the tree dirty. It is not a file any of the four PDFs reads.
ALLOWED = ("lab/", ".github/workflows/lab.yml",
           ".github/workflows/content.yml", ".gitignore",
           "notes/", "CLAUDE.md", "README.md", "docs/")


def labs() -> list[str]:
    """Every lab id with an exercise file: p01, p02, ..."""
    return sorted(p.stem.split("_", 1)[0] for p in (LAB / "exercises").glob("*.py"))


def module_of(lab: str) -> Path:
    found = sorted((LAB / "exercises").glob(f"{lab}_*.py"))
    if len(found) != 1:
        sys.exit(f"lab {lab!r}: expected one exercise file, found {found}")
    return found[0]


def public_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf8"))
    return {n.name for n in tree.body
            if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")}


def check_files() -> int:
    bad = 0
    for lab in labs():
        ex = module_of(lab)
        sol = LAB / "solutions" / ex.name
        tests = LAB / "tests" / f"test_{lab}.py"
        for p in (sol, tests):
            if not p.exists():
                print(f"  {lab}: {p.relative_to(ROOT)} is missing")
                bad += 1
        if bad:
            continue
        ex_src, sol_src = ex.read_text(encoding="utf8"), sol.read_text(encoding="utf8")
        for label, src in (("exercise", ex_src), ("solution", sol_src)):
            if not src.isascii():
                print(f"  {lab}: the {label} file is not ASCII; a listing cannot set it")
                bad += 1
            opened, closed = RE_REGION.findall(src), RE_ENDREGION.findall(src)
            if opened != closed:
                print(f"  {lab}: {label} regions open {opened} but close {closed}")
                bad += 1
        ex_regions, sol_regions = RE_REGION.findall(ex_src), RE_REGION.findall(sol_src)
        if ex_regions != sol_regions:
            print(f"  {lab}: exercise regions {ex_regions} != solution regions {sol_regions}")
            bad += 1
        ex_names, sol_names = public_names(ex), public_names(sol)
        if ex_names != sol_names:
            print(f"  {lab}: the exercise file exports {sorted(ex_names)} and the "
                  f"solution {sorted(sol_names)}; a check can only call what both define")
            bad += 1
        for lineno, line in enumerate(ex_src.splitlines(), 1):
            if len(line) > MEASURE:
                print(f"  {lab}: {ex.relative_to(ROOT)}:{lineno} is {len(line)} "
                      f"characters, over the {MEASURE} a half-screen pane shows")
                bad += 1
        # Every region is called by at least one check, and every check names
        # a region -- so an exercise nobody checks, or a check of nothing, is
        # visible here rather than in a reader's afternoon.
        test_names = RE_TEST.findall(tests.read_text(encoding="utf8"))
        for region in ex_regions:
            if not any(region in t for t in test_names):
                print(f"  {lab}: region {region!r} has no check whose name mentions it")
                bad += 1
        if not test_names:
            print(f"  {lab}: {tests.relative_to(ROOT)} defines no test_ functions")
            bad += 1
        if not bad:
            print(f"  {lab}: {len(ex_regions)} exercises, {len(test_names)} checks, "
                  f"exercise and solution files agree")
    return 0 if bad == 0 else 1


def _run_check(lab: str, solutions: bool) -> tuple[int, int, int]:
    env = dict(os.environ)
    env.pop("LAB_SOLUTIONS", None)
    if solutions:
        env["LAB_SOLUTIONS"] = "1"
    proc = subprocess.run([sys.executable, str(LAB / "check.py"), lab],
                          cwd=ROOT, env=env, capture_output=True, text=True)
    m = re.search(r"^SUMMARY ok=(\d+) fail=(\d+) todo=(\d+)$", proc.stdout, re.M)
    if not m:
        sys.exit(f"lab/check.py {lab} printed no SUMMARY line:\n{proc.stdout}{proc.stderr}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def check_tests() -> int:
    bad = 0
    for lab in labs():
        ok, fail, todo = _run_check(lab, solutions=True)
        if fail or todo or ok == 0:
            print(f"  {lab}: the reference solutions do NOT pass every check "
                  f"(ok={ok} fail={fail} todo={todo})")
            bad += 1
        s_ok, s_fail, s_todo = _run_check(lab, solutions=False)
        if s_ok:
            print(f"  {lab}: {s_ok} check(s) pass on the UNTOUCHED stubs, so they "
                  f"are not checking anything")
            bad += 1
        if (s_ok + s_fail + s_todo) != (ok + fail + todo):
            print(f"  {lab}: the two runs saw different numbers of checks")
            bad += 1
        if not bad:
            print(f"  {lab}: {ok} checks pass on the solutions; {s_todo} report "
                  f"todo and {s_fail} fail on the stubs; none passes")
    return 0 if bad == 0 else 1


def check_guard(ref: str) -> int:
    base = subprocess.run(["git", "merge-base", ref, "HEAD"], cwd=ROOT,
                          capture_output=True, text=True)
    if base.returncode != 0:
        sys.exit(f"cannot find a merge base with {ref!r}: {base.stderr.strip()}")
    diff = subprocess.run(["git", "diff", "--name-only", base.stdout.strip()],
                          cwd=ROOT, capture_output=True, text=True, check=True)
    untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                               cwd=ROOT, capture_output=True, text=True, check=True)
    changed = sorted(set(diff.stdout.split()) | set(untracked.stdout.split()))
    outside = [p for p in changed if not p.startswith(ALLOWED)]
    if outside:
        print("  the lab may not change these, and the diff does:")
        for p in outside:
            print(f"    {p}")
        return 1
    print(f"  {len(changed)} changed path(s) relative to {ref}, every one inside "
          f"{', '.join(ALLOWED)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--files", action="store_true")
    ap.add_argument("--tests", action="store_true")
    ap.add_argument("--guard", metavar="REF")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if not (a.files or a.tests or a.guard or a.all):
        ap.print_help()
        return 2
    rc = 0
    if a.files or a.all:
        print("files:")
        rc |= check_files()
    if a.tests or a.all:
        print("tests:")
        rc |= check_tests()
    if a.guard:
        print(f"guard against {a.guard}:")
        rc |= check_guard(a.guard)
    return rc


if __name__ == "__main__":
    sys.exit(main())
