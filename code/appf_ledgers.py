#!/usr/bin/env python3
"""Appendix F's ledgers, counted from the tree rather than typed.

Appendix F prints what the build otherwise only counts, because a reader
holding the paper cannot run `make debt` and is entitled to know what the
book still owes them. That makes every number on those pages a claim about
this repository -- which is the one class nothing here can check, and the
class that produced a stale 27 in the debt ledger, a stale 0.71 pages a
frame, a stale label count and seven wrong part ranges on page one, all
inside one week.

So Appendix F's counts go through the same machinery as every other number
in the book: computed here, written to figures/values/appf.tex, pulled in
with \\val{}, and gated by `make verify`. A ledger that moves while the
appendix does not is then a failed build rather than a page nobody reread.

TWO THINGS THIS SCRIPT DELIBERATELY DOES NOT EMIT.

  * How many of the ten experiments have run. CLAUDE.md forbids that
    class by name -- it is a claim about the book that nothing derives
    from anything, and notes/01 section 17 records that the sentence
    "none has been run" stayed on the page for five programs after one
    had. The appendix prints the ten rows and each row's own status, and
    never a total.

  * The page-level ledgers -- stranded openers, orphaned cues, orphan
    tails. Those are properties of the TYPESETTING, and CLAUDE.md
    records that this book's two TeX installations paginate differently,
    so the counts are facts about the machine that produced a given PDF
    rather than about the book. The appendix says what the build checks
    and does not print a number that is false on the other machine.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "values" / "appf.tex"

RE_FRAME = re.compile(r"\\begin\{fr\}")
RE_VALUE = re.compile(r"\\mfaval(?:text)?\{")
RE_PLTERM = re.compile(r"\\plterm\{[^{}]*\}\{([^{}]*)\}")
RE_PARTRANGE = re.compile(r"\(([FP]\d+)--([FP]\d+)\)")
RE_TEX_COMMENT = re.compile(r"(?<!\\)%.*")

# The cue is placed by rule -- a frame carries \nextframe if and only if the
# next frame opens with an answer -- so counting cues counts elicitation.
# Copied VERBATIM from check_structure.py's own RE_DEMANDS -- and the
# percentage below uses that tool's own floor division for the same reason.
# A first draft here used round(), which gives 52 where the ledger prints 51,
# because 968/1863 is 51.96: two implementations agreeing on the definition
# and differing on the rounding disagree only at the boundary, which is
# exactly where a reader compares this appendix with `make debt`. When a
# script re-derives a number another tool prints, copy that tool's
# ARITHMETIC, not its definition.
RE_DEMANDS = re.compile(r"\\blank|\\dotline|\\yourturn|\\nextframe")


def program_files(lang: str) -> list[Path]:
    return sorted((ROOT / "programs" / lang).glob("*.tex"))


def main() -> None:
    manifest = json.loads((ROOT / "tools" / "programs.json").read_text(encoding="utf8"))
    programs = manifest["programs"]
    planned = sum(p.get("frames", 0) for p in programs)

    # Teaching frames: \begin{fr} only, which is what every ledger in this
    # repository counts. The reader sees two more per program (the Summary and
    # the Test exercises are named frames), and that divergence is deliberate.
    frames = 0
    elicit = 0
    for f in program_files("en"):
        body = f.read_text(encoding="utf8")
        blocks = RE_FRAME.split(body)[1:]
        frames += len(blocks)
        elicit += sum(1 for b in blocks if RE_DEMANDS.search(b))

    diagrams_en = len(list((ROOT / "figures" / "mermaid" / "en").glob("*.mmd")))
    diagrams_pl = len(list((ROOT / "figures" / "mermaid" / "pl").glob("*.mmd")))
    assert diagrams_en == diagrams_pl, (
        f"the two editions carry different diagram sets: {diagrams_en} vs {diagrams_pl}"
    )

    # Per EDITION, because that is what the reader holds. `make debt` prints
    # 2x this, counting both -- the same two-quantities-under-one-number shape
    # that let CLAUDE.md's ledger say 27 where the tool printed 54. Appendix F
    # prints the reader's own copy throughout and says so once.
    def per_edition(pattern: str, lang: str) -> int:
        return sum(
            len(re.findall(pattern, f.read_text(encoding="utf8")))
            for f in program_files(lang)
            + sorted((ROOT / "appendices" / lang).glob("*.tex"))
        )

    transcripts = per_edition(r"\\transcript\{", "en")
    assert transcripts == per_edition(r"\\transcript\{", "pl"), (
        "the two editions carry different numbers of transcripts"
    )

    # Per edition like everything else, and asserted equal -- NOT en + pl.
    # The first draft summed the two here, inside the script whose whole
    # subject is not mixing the two quantities, and the mistake was invisible
    # because the answer is 0 either way. A convention that only holds where
    # you happen to check the number is not a convention; enforce it in the
    # code. (A verifybox in one edition and not the other is a real defect and
    # C14 already fails on it, so the assertion costs nothing.)
    verifyboxes = per_edition(r"\\begin\{verifybox\}", "en")
    assert verifyboxes == per_edition(r"\\begin\{verifybox\}", "pl"), (
        "the two editions carry different numbers of verifybox blocks"
    )

    appd = (ROOT / "appendices" / "en" / "appD-terminology.tex").read_text(encoding="utf8")
    term_rows = RE_PLTERM.findall(appd)
    term_renderings = [r.strip() for row in term_rows for r in row.split(",") if r.strip()]

    intro = RE_TEX_COMMENT.sub(
        "", (ROOT / "frontmatter" / "en" / "introduction.tex").read_text(encoding="utf8"))
    part_ranges = len(RE_PARTRANGE.findall(intro))
    assert part_ranges == len(manifest["parts"]), (
        "the introduction and the manifest disagree about how many parts there are; "
        "check_structure.py --parts says which"
    )

    # The computed-value ledger counts every \mfaval across figures/values,
    # and this file is one of them -- so count the others and add what this
    # script is about to write. Reading the count off a file the same run
    # overwrites would be a measurement of the previous run.
    others = sum(
        len(RE_VALUE.findall(p.read_text(encoding="utf8")))
        for p in sorted((ROOT / "figures" / "values").glob("*.tex"))
        if p.name != OUT.name
    )

    values: dict[str, tuple[str, bool]] = {
        "appf.programs":       (str(len(programs)), True),
        "appf.frames":         (str(frames), True),
        "appf.frames.planned": (str(planned), True),
        "appf.diagrams":       (str(diagrams_en), True),
        "appf.diagrams.both":  (str(diagrams_en + diagrams_pl), True),
        "appf.transcripts":    (str(transcripts), True),
        "appf.transcripts.both": (str(2 * transcripts), True),
        "appf.verifybox":      (str(verifyboxes), True),
        "appf.elicit":         (str(elicit), True),
        "appf.elicit.pct":     (str(100 * elicit // frames), True),
        "appf.terms.rows":     (str(len(term_rows)), True),
        "appf.terms.rend":     (str(len(term_renderings)), True),
        "appf.parts":          (str(part_ranges), True),
    }
    # +1 for appf.values itself, which is not in the dict yet.
    values["appf.values"] = (str(others + len(values) + 1), True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/appf_ledgers.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops Appendix F's ledgers drifting",
        "% away from the tree they describe.",
        "",
    ]
    lines += [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in values.items()
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf8")

    width = max(len(k) for k in values)
    for k, (body, _n) in values.items():
        print(f"  {k:<{width}}  {body}")
    print(f"\n  {len(values)} values -> {OUT.relative_to(ROOT)}")
    print("  the experiment statuses and the page-level ledgers are NOT emitted;")
    print("  see this script's docstring for why each is a claim rather than a count")


if __name__ == "__main__":
    main()
