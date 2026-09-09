#!/usr/bin/env python3
"""On-page node type size for every rendered diagram, and the one predicate
that is a defect rather than a taste.

WHY THIS EXISTS.  A `\mermaidfig` is an `\includegraphics` scaled to the
measure, so the type inside a diagram lands at whatever size the scaling
leaves it -- and nothing in this repository looked at that number.  Every
reviewer of every unit said the same thing about the figures, and the only
evidence anybody had was a handful of hand measurements in CLAUDE.md's own
pass notes, taken with `pdfinfo` on the files somebody happened to open.

The formula is CLAUDE.md's, re-derived here from the two things that set it:
`\mermaidfig` scales to `min(0.95\linewidth, 0.42\textheight)`, and mermaid
writes its PDF with `--pdfFit`, so the page IS the graph and its MediaBox is
the W x H the scaling divides into.  Reproduced to a hundredth of a point
against every figure CLAUDE.md records by hand.

WHAT IS GATED, AND WHAT IS ONLY REPORTED.  The type size is a ratio and there
is no defensible floor for it -- a threshold picked so today's book passes is
not an assertion, which this repository has paid for five times.  So the size
is a LEDGER, printed in full and never fatal, on the orphan tail's reasoning.

What IS a hard gate is a predicate: a figure whose aspect ratio falls below
the crossover is set to its full allowed HEIGHT whatever its width, so it
cannot share a page with the frames it belongs to and floats away with a
quarter of its own page blank.  That is a defect rather than a preference, it
is a property of the geometry rather than of the TeX installation, and both
formats' crossovers are computed below rather than quoted.

Reads build output.  With no rendered diagrams it says so and exits 0, so a
clean checkout is not a failure.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import statistics
import sys

# The two boxes `\mermaidfig` scales into, in points, per format. Taken from
# the geometry in preamble.tex: 0.95\linewidth by 0.42\textheight.
FORMATS = {
    "trade": (350.9, 229.2),   # 17 x 24 cm at 11pt
    "a4":    (398.4, 284.9),   # A4 at 12pt
}
# Mermaid's own base font, themeVariables.fontSize in figures/mermaid/config.json.
BASE_PT = 12.57

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIABOX = re.compile(
    rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]")


def page_size(path: pathlib.Path) -> tuple[float, float]:
    """Width and height in points, from the first MediaBox in the file.

    A pdfinfo stand-in, because pdfinfo is not installed on either of this
    project's two machines. --pdfFit means the page is the graph.
    """
    m = MEDIABOX.search(path.read_bytes())
    if not m:
        raise ValueError(f"{path}: no MediaBox")
    x0, y0, x1, y1 = (float(g) for g in m.groups())
    return x1 - x0, y1 - y0


def type_size(w: float, h: float, fmt: str) -> float:
    """On-page size of the diagram's node text, in points."""
    box_w, box_h = FORMATS[fmt]
    return BASE_PT * min(box_w / w, box_h / h)


def crossover(fmt: str) -> float:
    """The aspect ratio at which the binding cap changes from width to height.

    Below it the HEIGHT cap binds: the figure is set to its full allowed
    height however narrow it is, so it cannot share a page with its frames.
    """
    box_w, box_h = FORMATS[fmt]
    return box_w / box_h


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="figures/diagrams",
                    help="where the rendered diagrams are (build output)")
    ap.add_argument("--quiet", action="store_true",
                    help="print the ledger's summary and the failures only")
    args = ap.parse_args()

    root = (ROOT / args.dir) if not pathlib.Path(args.dir).is_absolute() else pathlib.Path(args.dir)
    pdfs = sorted(root.glob("*/*.pdf"))
    if not pdfs:
        print(f"  no rendered diagrams under {args.dir} -- run `make diagrams` first.")
        print("  (nothing to check; this is not a failure on a clean checkout)")
        return 0

    rows = []
    for p in pdfs:
        try:
            w, h = page_size(p)
        except ValueError as exc:
            print(f"  FAIL  {exc}")
            return 1
        rows.append((f"{p.parent.name}/{p.stem}", w, h,
                     type_size(w, h, "trade"), type_size(w, h, "a4")))

    # The hard gate: below the crossover the height cap binds.
    x_trade, x_a4 = crossover("trade"), crossover("a4")
    stranded = [r for r in rows if r[1] / r[2] < x_trade or r[1] / r[2] < x_a4]

    if not args.quiet:
        for name, w, h, t, a in sorted(rows, key=lambda r: r[3]):
            mark = "  <-- height-bound" if w / h < x_trade or w / h < x_a4 else ""
            print(f"  {name:34s} {w:7.2f} x {h:7.2f}  ratio {w/h:6.2f}"
                  f"   trade {t:5.2f} pt   a4 {a:5.2f} pt{mark}")

    trade = [r[3] for r in rows]
    a4 = [r[4] for r in rows]
    print(f"  {len(rows)} rendered diagrams. Node text on the page:")
    print(f"    trade  {min(trade):.2f} to {max(trade):.2f} pt, median {statistics.median(trade):.2f}")
    print(f"    a4     {min(a4):.2f} to {max(a4):.2f} pt, median {statistics.median(a4):.2f}")
    print("  Reported, never fatal: there is no defensible floor for a ratio,")
    print("  and a threshold chosen so today's book passes is not an assertion.")

    if stranded:
        print(f"  FAIL  {len(stranded)} diagram(s) below the aspect-ratio crossover")
        print(f"        (trade {x_trade:.2f}, a4 {x_a4:.2f}). The height cap binds, so each")
        print("        is set to its full allowed height however narrow it is and")
        print("        cannot share a page with the frames it belongs to.")
        for name, w, h, t, a in sorted(stranded, key=lambda r: r[1] / r[2]):
            print(f"          {name:34s} ratio {w/h:6.2f}   trade {t:5.2f} pt   a4 {a:5.2f} pt")
        print("        Fix by adding a rank, or by shortening the node text so the")
        print("        graph comes off mermaid's own wrapping cap.")
        return 1

    print("  Every diagram is above the aspect-ratio crossover in both formats.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
