#!/usr/bin/env python3
r"""Every cross-volume pointer, checked against the manifest.

A volume build cannot catch a bad pointer: its own references all resolve BY
CONSTRUCTION, because kdp/generated/volmap-vN.tex defines every label the volume
does not carry. That is the point of the mechanism, and it is also why it needs
a check outside the build -- a map that named a program which does not exist
would produce a clean compile and a pointer into nothing.

Two things are FATAL:
  * a \ref{prog:...} anywhere in the book naming a program the manifest does
    not have;
  * a generated map naming a volume that volumes.json does not have.

One thing is REPORTED and never fatal: how many pointers run FORWARD, from a
volume to a later one. The book cross-references forward on purpose -- 163 of
its program references do -- and it declares its genuine forward prerequisites
in the owning program's Learning outcomes. A gate here would be red on the
book's own design, and CLAUDE.md is explicit about what a permanently red gate
teaches the next person. The count is printed so that a split which suddenly
doubles it is visible.

Run:  python3 tools/checkxvol.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RE_REF = re.compile(r"\\ref\{prog:([A-Za-z0-9]+)\}")
RE_MAP = re.compile(r"\\mfavolref\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}")
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]


def main() -> int:
    progs = json.loads((ROOT / "tools" / "programs.json").read_text("utf8"))
    vols = json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))
    part_ids = {ROMAN[i]: p["ids"] for i, p in enumerate(progs["parts"])}
    key_of = {p["key"]: p["id"] for p in progs["programs"]}
    vol_of = {pid: v["n"] for v in vols["volumes"]
              for part in v["parts"] for pid in part_ids[part]}
    vol_roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
    known_numerals = {vol_roman[v["n"]] for v in vols["volumes"]}

    bad = 0

    # 1. Every \ref{prog:...} in the book names a program the manifest has.
    dangling = collections.Counter()
    for d in ("programs", "appendices", "frontmatter"):
        for f in (ROOT / d).rglob("*.tex"):
            for key in RE_REF.findall(f.read_text("utf8")):
                if key not in key_of:
                    dangling[(f.relative_to(ROOT).as_posix(), key)] += 1
    for (f, key), n in sorted(dangling.items()):
        print(f"  {f}: \\ref{{prog:{key}}} names no program in the manifest "
              f"({n} time(s))")
        bad += 1

    # 2. Every generated map entry names a real program and a real volume.
    gen = ROOT / "kdp" / "generated"
    maps = sorted(gen.glob("volmap-v*.tex"))
    if not maps:
        print("  no generated volume maps -- run: make volumes")
        return 1
    entries = 0
    for m in maps:
        for label, num, numeral in RE_MAP.findall(m.read_text("utf8")):
            entries += 1
            if numeral not in known_numerals:
                print(f"  {m.name}: {label} points at volume {numeral}, which "
                      f"volumes.json does not have")
                bad += 1
            if label.startswith("prog:"):
                key = label.split(":", 1)[1]
                if key not in key_of:
                    print(f"  {m.name}: {label} names no program in the manifest")
                    bad += 1

    # 3. The ledger: pointers that run forward, per volume. Reported, never fatal.
    fwd = collections.Counter()
    back = collections.Counter()
    for p in progs["programs"]:
        f = ROOT / "programs" / "en" / f"{p['file']}.tex"
        if not f.exists():
            continue
        here = vol_of.get(p["id"])
        for key in RE_REF.findall(f.read_text("utf8")):
            there = vol_of.get(key_of.get(key, ""), None)
            if there is None or there == here:
                continue
            (fwd if there > here else back)[here] += 1

    if bad == 0:
        print(f"  {entries} cross-volume pointers, every one naming a program "
              f"in the manifest and a volume in volumes.json.")
        print(f"  Pointers leaving their volume: "
              f"{sum(back.values())} backward, {sum(fwd.values())} forward "
              f"(reported, not gated -- the book cross-references forward by "
              f"design).")
        for v in sorted(set(fwd) | set(back)):
            print(f"    volume {v}: {back[v]} backward, {fwd[v]} forward")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
