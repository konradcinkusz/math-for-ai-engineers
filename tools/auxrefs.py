#!/usr/bin/env python3
r"""Dump what every \label in one edition resolved to, as label<TAB>number.

This exists for ONE comparison: the same book built twice, at two commits, to
prove a change moved no cross-reference. That is not what tools/reflist.py
does -- reflist compares the two EDITIONS against each other, English against
Polish, and prints a summary line rather than the resolutions themselves. The
KDP regression job used reflist for this and the mistake was invisible for
three separate reasons at once:

  1. reflist answers "do en and pl agree?", not "did head move against base?";
  2. its output is a COUNT, so two builds differing by a moved \ref print the
     identical "484 labels in en, 484 in pl, 0 mismatches";
  3. the job compiles main-en only, so reflist failed on the missing
     main-pl.aux on BOTH sides and the diff compared two error strings --
     which differed solely by the absolute path each tree sat at. Had the two
     trees shared a path, the guard would have gone GREEN having compared
     nothing whatever.

Takes the tree root explicitly and resolves the \@input{} chain against it,
rather than against this file's own location, because the base side of that
comparison is a worktree of an OLDER commit: it does not contain this script,
so this script has to be able to read a tree it is not standing in.

Usage:  python3 tools/auxrefs.py <tree-root> [main-en]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NEWLABEL = re.compile(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}\{([^}]*)\}")
INPUT = re.compile(r"\\@input\{([^}]*)\}")


def collect(aux: Path, root: Path, seen: set[Path] | None = None) -> dict[str, str]:
    r"""Read an .aux and everything it \@input{}s, relative to root."""
    seen = set() if seen is None else seen
    aux = aux.resolve()
    if aux in seen or not aux.is_file():
        return {}
    seen.add(aux)
    text = aux.read_text(encoding="utf8", errors="replace")
    out = {m.group(1): m.group(2) for m in NEWLABEL.finditer(text)}
    for m in INPUT.finditer(text):
        out.update(collect(root / m.group(1), root, seen))
    return out


def main() -> int:
    if not 2 <= len(sys.argv) <= 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    stem = sys.argv[2] if len(sys.argv) > 2 else "main-en"
    aux = root / f"{stem}.aux"
    if not aux.is_file():
        print(f"auxrefs: {aux} missing -- compile {stem} first", file=sys.stderr)
        return 1

    labels = collect(aux, root)

    # An empty answer is what a guard reads as "nothing moved". The aux tree is
    # an \@input{} chain, so being handed a main file whose per-program .aux
    # files are absent finds zero labels and prints zero lines -- and two empty
    # files diff clean. Refuse, rather than report a vacuous pass.
    if not labels:
        print(f"auxrefs: no labels under {aux}. The per-program .aux files are "
              f"part of the \\@input{{}} chain and must be present.",
              file=sys.stderr)
        return 1

    print(f"# {len(labels)} labels", file=sys.stderr)
    for k in sorted(labels):
        print(f"{k}\t{labels[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
