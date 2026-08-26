#!/usr/bin/env python3
"""Fail a build that only looked like it succeeded.

This exists because of a real incident in this repository. The scaffold's
smoke build produced a 12-page PDF and `grep -c '^!' _smoke.log` returned 0,
so it was recorded as clean. It was not: siunitx never loaded, because a `#1`
inside an \\IfFileExists branch raised

    ./preamble.tex:702: Illegal parameter number in definition of \\reserved@a.

Two things hid it. `-interaction=nonstopmode` recovers from errors and still
writes a PDF, and with file-line-error formatting an error line begins with a
path rather than with `!`, so the usual grep misses it. The consequence was
that the decimal comma -- the single most visible thing about a Polish maths
book -- silently did not work, in a build everyone believed was green.

Usage:  python3 tools/checklog.py main-en.log [main-pl.log ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# An error in either of the two formats pdflatex emits.
ERR = re.compile(r"^(?:!(?! *Undefined control sequence *$).*|[^\s:]+\.\w+:\d+:.*)$", re.M)
UNDEF_REF = re.compile(r"Reference `([^']*)' on page \d+ undefined", re.M)
UNDEF_CIT = re.compile(r"Citation `([^']*)' on page \d+ undefined", re.M)
MULTI = re.compile(r"Label `([^']*)' multiply defined", re.M)
OVERFULL_H = re.compile(r"Overfull \\hbox \(([\d.]+)pt", re.M)
OVERFULL_V = re.compile(r"Overfull \\vbox \(([\d.]+)pt", re.M)
PAGES = re.compile(r"Output written on \S+ \((\d+) pages")

# The margin budget inherited from the sibling books.
HBOX_LIMIT_PT = 15.0


def check(path: Path) -> int:
    if not path.is_file():
        print(f"  FAIL  {path} does not exist -- the build did not run")
        return 1
    log = path.read_text(encoding="utf8", errors="replace")
    fails = 0

    errs = [m.group(0).strip() for m in ERR.finditer(log)]
    # "! " lines are also used for the recovery banner; keep only real ones.
    errs = [e for e in errs if not e.startswith("! ==> Fatal error occurred")]
    for e in errs[:10]:
        print(f"  FAIL  {path.name}: {e}")
        fails += 1
    if len(errs) > 10:
        print(f"  FAIL  {path.name}: ... and {len(errs)-10} more errors")

    for rx, what in ((UNDEF_REF, "undefined reference"),
                     (UNDEF_CIT, "undefined citation"),
                     (MULTI, "multiply-defined label")):
        for m in rx.finditer(log):
            print(f"  FAIL  {path.name}: {what} `{m.group(1)}'")
            fails += 1

    h = sorted((float(m.group(1)) for m in OVERFULL_H.finditer(log)), reverse=True)
    v = [float(m.group(1)) for m in OVERFULL_V.finditer(log)]
    over = [x for x in h if x > HBOX_LIMIT_PT]
    for x in over:
        print(f"  FAIL  {path.name}: overfull hbox {x}pt exceeds the "
              f"{HBOX_LIMIT_PT}pt margin budget")
        fails += 1
    for x in v:
        print(f"  FAIL  {path.name}: overfull vbox {x}pt -- a centred table or "
              f"box grew past a page and cannot break; split it")
        fails += 1

    # No "Output written on" line means no PDF came out of this run. A log with
    # no errors and no output is still a failed build, and without this it
    # scores as clean.
    pages = PAGES.search(log)
    if not pages:
        print(f"  FAIL  {path.name}: no PDF was written by this run")
        fails += 1

    print(f"  {'FAIL ' if fails else 'ok   '} {path.name}: "
          f"{pages.group(1) if pages else 'no'} pages, "
          f"{len(h)} overfull hbox (max {h[0] if h else 0}pt), "
          f"{len(v)} overfull vbox, {len(errs)} errors")
    return fails


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = sum(check(Path(a)) for a in sys.argv[1:])
    print("-" * 68)
    print(f"  {total} problems")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
