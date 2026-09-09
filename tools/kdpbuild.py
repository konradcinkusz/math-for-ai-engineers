#!/usr/bin/env python3
r"""Build one KDP volume, converging the gutter, and stop if it will not settle.

KDP's minimum inside margin is a function of the page count, and the page count
is a function of the inside margin, so this is a fixed point rather than a
build. Pass one compiles with whatever gutter is on disk, reads the true page
count, and if that count implies a different bracket writes the new gutter and
compiles again.

THREE PASSES, then stop. A book whose page count sits within a page or two of a
bracket boundary can oscillate between two gutters forever, and a build that
never finishes is worse than one that says why it did not.

Run:  python3 tools/kdpbuild.py 3 en
      python3 tools/kdpbuild.py --all
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / "build" / "kdp" / "tex"
# The gutter and pad leaf are read by the document, and the document is
# compiled IN the staging tree -- so they have to be written there. Written
# to the real kdp/gutter they were invisible to the build, and the pad leaf
# silently did nothing while the driver reported it as applied.
GUTTER_DIR = STAGE / "kdp" / "gutter"
MAX_PASSES = 4   # gutter convergence, then page parity

# KDP's minimum inside margin by page count. Kept here and in
# tools/checkkdp.py's GUTTER_TABLE; they are checked against each other by
# tools/test_gen_volumes.py so the two cannot drift.
GUTTER_TABLE = [(150, 0.375), (300, 0.500), (500, 0.625),
                (700, 0.750), (828, 0.875)]


def bracket_in(pages: int) -> float | None:
    for lim, g in GUTTER_TABLE:
        if pages <= lim:
            return g
    return None


def gutter_mm(pages: int, safety: float) -> float | None:
    g = bracket_in(pages)
    return None if g is None else round(g * 25.4 + safety, 2)


def page_count(pdf: Path) -> int | None:
    if not pdf.exists():
        return None
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    return None


def compile_once(vol: int, lang: str, job: str, force: bool = False) -> int:
    src = f"kdp/generated/v{vol}-{lang}.tex"
    # Bytes, not text. TeX writes the log in its own encoding and a Polish
    # program's output is not valid UTF-8, so text=True raises UnicodeDecodeError
    # and the build looks like a crash in the driver rather than a compile.
    # Compiled IN the staging tree, not in the repository root: that tree's
    # figures/diagrams is the grayscale set, and everything else in it is a
    # symlink to the real file. See tools/kdpstage.py for why a TEXINPUTS
    # shadow does not work here.
    # -g on any pass after the first. The gutter and the pad leaf are \input by
    # the preamble, and on the pass that CREATES one of them latexmk has no
    # record of it as a dependency -- so it decides nothing changed and does not
    # recompile. The tell was that the .log was written 0.2 s BEFORE the gutter
    # file it was supposed to have read, and the driver reported a pad leaf it
    # had applied to nothing.
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error"]
    if force:
        cmd.append("-g")
    r = subprocess.run(cmd + [f"-jobname={job}", src],
                       cwd=STAGE, capture_output=True)
    (STAGE / f"{job}.build.log").write_bytes(r.stdout + r.stderr)
    return r.returncode


def build(vol: int, lang: str, cfg: dict, verbose=True) -> tuple[int, int | None]:
    job = f"kdp-v{vol}-{lang}"
    safety = cfg["margins_mm"]["gutter_safety"]
    GUTTER_DIR.mkdir(parents=True, exist_ok=True)
    gfile = GUTTER_DIR / f"{vol}-{lang}.tex"

    for p in range(1, MAX_PASSES + 1):
        # EVERY pass forces. Pass 1 was left unforced at first and reported a
        # stale 428-page PDF from a previous run after its gutter file had been
        # deleted -- a measurement of a tree that no longer existed. A volume
        # build is a measurement, so it starts from the source every time.
        rc = compile_once(vol, lang, job, force=True)
        n = page_count(STAGE / f"{job}.pdf")
        if rc != 0 or n is None:
            print(f"  v{vol}-{lang}: latexmk exit {rc} on pass {p}"
                  f" -- see {job}.build.log")
            return 1, n
        want = gutter_mm(n, safety)
        if want is None:
            print(f"  v{vol}-{lang}: {n} pages is above the black-ink ceiling; "
                  f"no gutter bracket applies")
            return 1, n
        # Parsed by name. Splitting on the last brace read the pad leaf's `{1}'
        # as a gutter the moment parity handling was added.
        have = float(cfg["_default_gutter_mm"])
        if gfile.exists():
            m = re.search(r"\\def\\kdpinner\{([\d.]+)mm\}",
                          gfile.read_text("utf8"))
            if m:
                have = float(m.group(1))
        # Parity is settled AFTER the gutter, because the gutter moves the page
        # count and a pad leaf does not move the gutter -- one direction only,
        # so the two cannot chase each other.
        if abs(have - want) < 0.005:
            if n % 2 == 0:
                if verbose:
                    print(f"  v{vol}-{lang}: {n} pages, gutter {want} mm, "
                          f"converged on pass {p}")
                return 0, n
            if "mfapadleaf" in (gfile.read_text("utf8") if gfile.exists() else ""):
                print(f"  v{vol}-{lang}: {n} pages is still odd with a pad leaf "
                      f"already in place -- something else is adding a page")
                return 1, n
            if verbose:
                print(f"  v{vol}-{lang}: pass {p} gave {n} pages, which is odd "
                      f"-- adding a blank verso and rebuilding")
            gfile.write_text(f"%% GENERATED by tools/kdpbuild.py -- pass {p} "
                             f"measured {n} pages.\n"
                             f"\\def\\kdpinner{{{want}mm}}\n"
                             f"\\def\\mfapadleaf{{1}}\n", "utf8")
            continue
        if verbose:
            print(f"  v{vol}-{lang}: pass {p} gave {n} pages, which wants "
                  f"{want} mm not {have} mm -- rebuilding")
        pad = "\\def\\mfapadleaf{1}\n" if gfile.exists() and \
            "mfapadleaf" in gfile.read_text("utf8") else ""
        gfile.write_text(f"%% GENERATED by tools/kdpbuild.py -- pass {p} measured "
                         f"{n} pages.\n\\def\\kdpinner{{{want}mm}}\n" + pad, "utf8")
    print(f"  v{vol}-{lang}: did not converge in {MAX_PASSES} passes. The page "
          f"count sits on a bracket boundary; set the gutter by hand in "
          f"{gfile.relative_to(ROOT)}.")
    return 1, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("volume", nargs="?", type=int)
    ap.add_argument("lang", nargs="?", choices=("en", "pl"))
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    cfg = json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))
    # The default the preamble uses when no gutter file exists.
    cfg["_default_gutter_mm"] = round(0.625 * 25.4
                                      + cfg["margins_mm"]["gutter_safety"], 2)

    jobs = []
    if a.all:
        jobs = [(v["n"], l) for v in cfg["volumes"] for l in ("en", "pl")]
    elif a.volume:
        jobs = [(a.volume, l) for l in ([a.lang] if a.lang else ["en", "pl"])]
    else:
        ap.error("give a volume number, or --all")

    rc = 0
    for vol, lang in jobs:
        r, _ = build(vol, lang, cfg)
        rc |= r
    return rc


if __name__ == "__main__":
    sys.exit(main())
