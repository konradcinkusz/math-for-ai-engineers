#!/usr/bin/env python3
"""Decide whether a LaTeX run actually succeeded.

`grep '^!' main.log` is the habit inherited from the companion volumes and it
is not sufficient here, for two reasons that cost this repository a real bug:

  * with -file-line-error, an error line begins with a PATH, not with `!`
    (`./preamble.tex:735: Illegal parameter number ...`), so the usual grep
    cannot see it;
  * -interaction=nonstopmode recovers from errors and still writes a PDF, so
    the exit code and the existence of the PDF both say "fine".

Between them, a broken \\IfFileExists branch stopped siunitx from loading at
all -- which meant the decimal comma, the most visible single feature of a
Polish mathematics book, silently did not work in a build everyone believed
was green.

Usage:
    tools/checklog.py main-en.log [main-pl.log ...]
    tools/checklog.py --summary main-en.log        # machine-readable one-liner

Exit code is non-zero if any log carries an error, an unresolved reference, or
an overfull vbox -- the three things that must never reach a reader.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RE_BANG = re.compile(r"^! (.*)$", re.M)
RE_FILELINE = re.compile(r"^(?:\./|/)[^\s:]+:\d+: (.*)$", re.M)
RE_UNDEF_REF = re.compile(r"Reference `([^']+)' on page \d+ undefined", re.M)
RE_UNDEF_CIT = re.compile(r"Citation `([^']+)' on page \d+ undefined", re.M)
RE_HBOX = re.compile(r"Overfull \\hbox \(([\d.]+)pt")
RE_VBOX = re.compile(r"Overfull \\vbox \(([\d.]+)pt")
RE_PAGES = re.compile(r"Output written on \S+ \((\d+) pages")
RE_MISSING_VAL = re.compile(r"No computed values found")
# Warnings that are always worth surfacing. Font substitution noise is not.
RE_WARN = re.compile(r"^(?:LaTeX|Package|Class) (\w+ )?Warning: (.*)$", re.M)
WARN_IGNORE = ("Font shape", "Some font shapes", "Size substitutions",
               "Token not allowed", "There were undefined references",
               "Label(s) may have changed", "has changed")

HBOX_BUDGET = 15.0   # pt. Anything above this visibly runs into the margin.


def analyse(path: Path) -> dict:
    text = path.read_text(encoding="utf8", errors="replace")
    errors = RE_BANG.findall(text) + RE_FILELINE.findall(text)
    warns = [
        f"{m.group(1) or ''}{m.group(2)}".strip()
        for m in RE_WARN.finditer(text)
        if not any(s in m.group(2) for s in WARN_IGNORE)
    ]
    h = sorted((float(x) for x in RE_HBOX.findall(text)), reverse=True)
    v = sorted((float(x) for x in RE_VBOX.findall(text)), reverse=True)
    pages = RE_PAGES.search(text)
    return {
        "file": path.name,
        "errors": errors,
        "warnings": warns,
        "undef_refs": RE_UNDEF_REF.findall(text),
        "undef_cits": RE_UNDEF_CIT.findall(text),
        "hbox": h,
        "vbox": v,
        "over_budget": [x for x in h if x > HBOX_BUDGET],
        "pages": int(pages.group(1)) if pages else None,
        "no_values": bool(RE_MISSING_VAL.search(text)),
    }


def report(r: dict) -> bool:
    ok = True
    print(f"== {r['file']} ==")
    print(f"  pages           : {r['pages']}")
    if r["errors"]:
        ok = False
        print(f"  ERRORS          : {len(r['errors'])}")
        for e in r["errors"][:12]:
            print(f"      {e}")
    else:
        print("  errors          : 0")
    if r["undef_refs"] or r["undef_cits"]:
        ok = False
        print(f"  UNRESOLVED REFS : {sorted(set(r['undef_refs'] + r['undef_cits']))}")
    else:
        print("  unresolved refs : 0")
    print(f"  overfull hbox   : {len(r['hbox'])} "
          f"{[round(x, 1) for x in r['hbox'][:8]]}")
    if r["over_budget"]:
        ok = False
        print(f"  OVER {HBOX_BUDGET:.0f} pt BUDGET : {[round(x, 1) for x in r['over_budget']]}")
    if r["vbox"]:
        ok = False
        print(f"  OVERFULL VBOX   : {len(r['vbox'])} {[round(x, 1) for x in r['vbox'][:5]]}")
        print("      A vbox means a boxed block grew past a page and could not")
        print("      break. Split the table; do not shrink the text.")
    else:
        print("  overfull vbox   : 0")
    if r["no_values"]:
        ok = False
        print("  NO COMPUTED VALUES: every \\val{} printed a marker. Run `make numbers`.")
    if r["warnings"]:
        print(f"  warnings        : {len(r['warnings'])}")
        for w in r["warnings"][:6]:
            print(f"      {w}")
    return ok


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("logs", nargs="+", type=Path)
    p.add_argument("--summary", action="store_true")
    a = p.parse_args()
    ok = True
    for path in a.logs:
        if not path.exists():
            print(f"== {path} == MISSING")
            ok = False
            continue
        r = analyse(path)
        if a.summary:
            print(f"{r['file']}: pages={r['pages']} errors={len(r['errors'])} "
                  f"refs={len(set(r['undef_refs']))} hbox={len(r['hbox'])} "
                  f"vbox={len(r['vbox'])} warn={len(r['warnings'])}")
            ok &= not (r["errors"] or r["undef_refs"] or r["vbox"] or r["over_budget"])
        else:
            ok &= report(r)
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `checklog.py ... | head` closes the pipe. Exiting quietly is the
        # right behaviour; a traceback here reads as a failure of the check.
        sys.exit(0)
