#!/usr/bin/env python3
"""Mutation tests for tools/gen_volumes.py.

Every check in the generator is introduced as a fault here and the generator is
required to refuse it. A check nobody has watched fire is exactly what this
repository keeps finding: an instrument that accepts the input and returns a
plausible answer. These are the known answers.

Run:  python3 tools/test_gen_volumes.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_volumes as gv                                   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def with_volumes(mutate):
    """Run validate() over a mutated copy of volumes.json."""
    progs = json.loads((ROOT / "tools" / "programs.json").read_text("utf8"))
    vols = json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))
    part_ids = {gv.ROMAN[i]: p["ids"] for i, p in enumerate(progs["parts"])}
    mutate(vols)
    return gv.validate(progs, vols, part_ids)


CASES = []


def case(name, wants):
    def deco(fn):
        CASES.append((name, fn, wants))
        return fn
    return deco


@case("a part in no volume", "in no volume")
def _drop_part(v):
    v["volumes"][3]["parts"].remove("IX")


@case("a part in two volumes", "more than one volume")
def _dupe_part(v):
    v["volumes"][0]["parts"].append("IX")


@case("a volume that is not contiguous", "not a contiguous run")
def _gap(v):
    v["volumes"][1]["parts"] = ["II", "IV"]
    v["volumes"][2]["parts"] = ["III", "V", "VI"]


@case("volumes out of manifest order", "does not follow programs.json")
def _order(v):
    v["volumes"][1]["parts"], v["volumes"][2]["parts"] = (
        v["volumes"][2]["parts"], v["volumes"][1]["parts"])


@case("a part the manifest does not have", "which programs.json does not have")
def _unknown(v):
    v["volumes"][0]["parts"] = ["I", "XI"]


@case("a volume with no Polish title", "has no pl title")
def _notitle(v):
    v["volumes"][2]["title"]["pl"] = ""


@case("volume numbers that do not run 1..N", "must run 1..N")
def _renumber(v):
    v["volumes"][2]["n"] = 9


def main() -> int:
    bad = 0

    # The tree as it stands must be clean, or every case below is meaningless.
    if with_volumes(lambda v: None):
        print("  FAIL: the committed volumes.json does not validate")
        return 1
    print("  ok    the committed split validates")

    for name, mutate, wants in CASES:
        errs = with_volumes(mutate)
        hit = [e for e in errs if wants in e]
        if hit:
            print(f"  ok    refuses {name}")
        else:
            print(f"  FAIL  {name}: expected an error containing {wants!r}, "
                  f"got {errs or 'no error at all'}")
            bad += 1

    # The generator must be deterministic: two runs, byte-identical output.
    a, _ = gv.build_all()
    b, _ = gv.build_all()
    if a == b:
        print("  ok    generation is deterministic")
    else:
        print("  FAIL  two runs of build_all() disagree")
        bad += 1

    # Every program must appear in exactly one volume's structure file, and the
    # numbering offset must put the first main program at its own number.
    files, _ = gv.build_all()
    progs = json.loads((ROOT / "tools" / "programs.json").read_text("utf8"))
    misplaced = 0
    for p in progs["programs"]:
        n = sum(f"\\includeprogram{{{p['file']}}}" in t
                for k, t in files.items() if k.startswith("structure-"))
        if n != 1:
            print(f"  FAIL  {p['id']} appears in {n} volume structures, not 1")
            misplaced += 1
    bad += misplaced
    if not misplaced:
        print(f"  ok    all {len(progs['programs'])} programs appear exactly once")
    if "\\setcounter{chapter}{11}" in files["structure-v3.tex"]:
        print("  ok    volume 3 offsets its chapter counter so P12 prints as 12")
    else:
        print("  FAIL  volume 3 has no numbering offset; P12 would print as 1")
        bad += 1

    print(f"\n  {len(CASES) + 3} checks, {bad} failures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
