#!/usr/bin/env python3
r"""Stage an isolated build tree for the KDP volumes, with grayscale diagrams.

WHY A STAGED TREE. \mermaidfig hard-codes figures/diagrams/<lang>/<key>.pdf in
both of its branches, and the KDP work may not edit preamble.tex, so the gray
diagrams have to arrive at that exact relative path.

TWO OTHER ROUTES WERE TRIED AND ONE OF THEM LOOKS RIGHT:

  * figures/diagrams-kdp/ -- needs \mermaidfig changed. Out of bounds.

  * A shadow directory first on TEXINPUTS. kpsewhich confirms kpathsea resolves
    the shadowed name, and the book build ignored it: the log says
    `<./figures/diagrams/en/....pdf>', with the leading `./' that gives it away.
    graphicx opens a name containing a slash relative to the working directory
    and never consults the search path when the file is there. A shadow cannot
    win against a file that exists.

So the build gets a tree in which figures/diagrams IS the gray set. Everything
else is a SYMLINK to the real thing, file by file rather than directory by
directory, for one reason: \include writes <program>.aux beside its source, and
through a symlinked directory those writes would land back in the real tree and
collide with the trade build's -- which is a trap CLAUDE.md already records for
the four existing formats. With files symlinked into real directories, the KDP
build's aux tree is its own.

Run:  python3 tools/kdpstage.py
      python3 tools/kdpstage.py --check
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / "build" / "kdp" / "tex"

# Everything the volume documents read. figures/diagrams is deliberately absent:
# it is the one directory that is generated rather than linked.
LINK_TREES = ["programs", "appendices", "frontmatter", "lang", "kdp",
              "figures/values", "figures/transcripts", "figures/mermaid",
              "tools"]
LINK_FILES = ["preamble.tex", "structure.tex", "body.tex"]

GS = ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
      "-sColorConversionStrategy=Gray", "-dProcessColorModel=/DeviceGray",
      "-dAutoRotatePages=/None", "-dCompatibilityLevel=1.5",
      "-dDetectDuplicateImages=true"]


def page_size(pdf: Path):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Page size:"):
            f = line.split(":")[1].split()
            return float(f[0]), float(f[2])
    return None


def link_into(rel: str) -> int:
    """Mirror one tree as real directories holding symlinks to real files."""
    src, dst = ROOT / rel, STAGE / rel
    n = 0
    for p in src.rglob("*"):
        if p.is_dir():
            (dst / p.relative_to(src)).mkdir(parents=True, exist_ok=True)
            continue
        # Never link build output back in: a stale .aux or .pdf from the real
        # tree would be read as this build's own.
        if p.suffix in (".aux", ".log", ".out", ".toc", ".idx", ".ind", ".ilg",
                        ".fls", ".fdb_latexmk", ".dgm", ".synctex.gz"):
            continue
        t = dst / p.relative_to(src)
        t.parent.mkdir(parents=True, exist_ok=True)
        if t.is_symlink() or t.exists():
            t.unlink()
        t.symlink_to(os.path.relpath(p, t.parent))
        n += 1
    return n


def gray_diagrams() -> tuple[int, list[str]]:
    src, dst = ROOT / "figures" / "diagrams", STAGE / "figures" / "diagrams"
    srcs = sorted(src.glob("*/*.pdf"))
    errs, done = [], 0
    for s in srcs:
        d = dst / s.relative_to(src)
        d.parent.mkdir(parents=True, exist_ok=True)
        if d.exists() and d.stat().st_mtime >= s.stat().st_mtime:
            done += 1
            continue
        r = subprocess.run(GS + ["-o", str(d), str(s)], capture_output=True)
        if r.returncode != 0 or not d.exists():
            errs.append(f"ghostscript failed on {s.name}")
            continue
        a, b = page_size(s), page_size(d)
        # The figure sizing in this book is a formula in the rendered width, so a
        # conversion that resized a diagram would silently invalidate every
        # recorded node-size and rule-2 measurement. Checked per file.
        if a and b and max(abs(a[0] - b[0]), abs(a[1] - b[1])) > 0.01:
            errs.append(f"{s.name} changed size {a} -> {b}")
            continue
        done += 1
    return done, errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    src_dir, pre_dir = ROOT / "figures" / "diagrams", STAGE / "figures" / "diagrams"
    n_src = len(list(src_dir.glob("*/*.pdf")))
    n_pre = len(list(pre_dir.glob("*/*.pdf")))

    # THE COLOUR SET IS THE INPUT TO THE CONVERSION, AND IT IS ABSENT BY DESIGN
    # IN CI'S PER-VOLUME JOB. `diagrams-kdp` renders and converts once and ships
    # the GRAY set as an artifact, which `build-volume` unpacks straight into
    # this staging tree -- so eight volume builds do not each re-run ghostscript
    # over three hundred files. What is still owed there is the OTHER half of
    # this script, the symlink tree, and bailing here skipped it: the job
    # reported "no rendered diagrams found -- run `make diagrams` first" while
    # standing on a complete set of them.
    #
    # This may not become a pass that read nothing, which is the failure mode
    # this pipeline keeps producing: with neither a colour source nor a
    # populated gray stage there is nothing to build against, and that stops.
    if n_src == 0 and n_pre == 0:
        print("  no rendered diagrams found -- run `make diagrams` first, or")
        print(f"  unpack a prebuilt gray set into {pre_dir.relative_to(ROOT)}")
        return 1
    prestaged = n_src == 0

    if a.check:
        missing = ([] if prestaged else
                   [q for q in src_dir.glob("*/*.pdf")
                    if not (pre_dir / q.relative_to(src_dir)).exists()])
        gone = [r for r in LINK_TREES + LINK_FILES if not (STAGE / r).exists()]
        if missing or gone:
            print(f"  the KDP staging tree is incomplete: "
                  f"{len(missing)} gray diagram(s) missing"
                  + (f", {gone} not staged" if gone else "")
                  + ". Run: make kdp-stage")
            return 1
        print(f"  KDP staging tree is current ({n_pre if prestaged else n_src} "
              f"gray diagrams{', prebuilt' if prestaged else ''}).")
        return 0

    STAGE.mkdir(parents=True, exist_ok=True)
    links = sum(link_into(r) for r in LINK_TREES)
    for f in LINK_FILES:
        t = STAGE / f
        if t.is_symlink() or t.exists():
            t.unlink()
        t.symlink_to(os.path.relpath(ROOT / f, t.parent))
        links += 1
    if prestaged:
        done, errs, n_src = n_pre, [], n_pre
    else:
        done, errs = gray_diagrams()
    for e in errs[:5]:
        print(f"  {e}")
    print(f"  staged {links} symlinks and "
          + (f"found {done} prebuilt grayscale diagrams"
             if prestaged else f"{done} of {n_src} grayscale diagrams")
          + f" in {STAGE.relative_to(ROOT)}"
          + (f", {len(errs)} failures" if errs else ""))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
