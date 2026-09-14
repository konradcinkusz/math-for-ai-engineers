#!/usr/bin/env python3
"""How much of the book is already a content model, measured rather than asserted.

The learning application proposed in notes/10-learning-app.md rests on one
claim: the book's LaTeX is structured enough to compile into frames, answers,
cues, quizzes, routes and values without hand work. This probe tests the claim
with the book's own tokeniser, tools/parity.py, which every build already runs
over every program. It reads programs/en and reports, per program and in total:

  * frames, and how many open with an answer (\ans or ansblock) -- the
    covered box the whole method rests on;
  * frames that end with the next-frame cue (which is the elicitation rate,
    since C16 makes the cue sit exactly where the next frame answers);
  * the retrieval modes a frame carries (dotline, blank, yourturn);
  * admonition boxes by kind; maths spans; \val{} references; figures;
  * Quiz / Test / Further items, and the Quiz routes back into the frames.

    python3 lab/tools/content_probe.py             # totals, one line per program
    python3 lab/tools/content_probe.py --json P01  # one program as the model
                                                   # the compiler would emit

Nothing here is a compiler. It is the measurement that says whether writing
one is a week or a year, and it costs one import of a tool the book already
trusts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import parity  # noqa: E402  -- the book's own tokeniser

RE_SECTION = re.compile(r"\\section\{([^}]*)\}")
RE_TRANSCRIPT = re.compile(r"\\transcript\{([^}]*)\}")
RE_TEACHES = re.compile(r"\\teachesat(?:one)?\{([^}]*)\}")
OPENERS = ("ANS", "BEGIN(ansblock)")
MODES = ("DOTLINE", "BLANK", "YOURTURN", "NEXTFRAME")
BOX_KINDS = ("note", "warning", "trapbox", "aibox", "rigourbox", "notationbox",
             "verifybox", "exercisebox")


RE_VALREF = re.compile(r"\\(?:raw)?val\{([^}]+)\}")


def frames_of(doc: parity.Doc, src: str) -> list[dict]:
    """Split the token stream at FRAME tokens; each frame is what follows it.

    \val{} is counted from the SOURCE slice of each frame rather than from the
    tokens: the tokeniser harvests a \val inside a maths span into doc.vals
    without emitting a token for it, so a token count sees the prose ones only
    -- which is how the first run of this probe reported zero values in P01.
    """
    lines = src.split("\n")
    frames: list[dict] = []
    current: dict | None = None
    for t in doc.tokens:
        if t.kind == "FRAME":
            current = {"n": int(t.payload), "line": t.line, "tokens": []}
            frames.append(current)
        elif current is not None:
            current["tokens"].append(t)
    out = []
    for k, f in enumerate(frames):
        end = frames[k + 1]["line"] - 1 if k + 1 < len(frames) else len(lines)
        slice_ = "\n".join(lines[f["line"] - 1:end])
        keys = [t.key() for t in f["tokens"]]
        first = next((k for k in keys if not k.startswith("LABEL(")), "")
        boxes = Counter(t.payload for t in f["tokens"]
                        if t.kind == "BEGIN" and t.payload in BOX_KINDS)
        out.append({
            "n": f["n"],
            "line": f["line"],
            "opens_with_answer": first in OPENERS,
            "cue": "NEXTFRAME" in keys,
            "modes": sorted({k for k in keys if k in MODES and k != "NEXTFRAME"}),
            "boxes": dict(boxes),
            "maths": sum(1 for t in f["tokens"] if t.kind == "MATH"),
            "vals": sorted(set(RE_VALREF.findall(slice_))),
            "figs": [t.payload for t in f["tokens"] if t.kind == "FIG"],
        })
    return out


def probe(path: Path) -> dict:
    doc = parity.tokenise(path)
    src = parity.COMMENT_RE.sub("", path.read_text(encoding="utf8"))
    frames = frames_of(doc, src)
    items = Counter(k[0] for k in doc.answer_keys)
    routes = [r for r in RE_TEACHES.findall(src)]
    return {
        "program": path.stem,
        "sections": RE_SECTION.findall(src),
        "frames": len(frames),
        "answer_openers": sum(f["opens_with_answer"] for f in frames),
        "cues": sum(f["cue"] for f in frames),
        "boxes": dict(sum((Counter(f["boxes"]) for f in frames), Counter())),
        "maths": sum(f["maths"] for f in frames),
        "vals": len({v for f in frames for v in f["vals"]}),
        "figs": [x for f in frames for x in f["figs"]],
        "transcripts": RE_TRANSCRIPT.findall(src),
        "quiz": items.get("Q", 0), "tests": items.get("T", 0),
        "further": items.get("P", 0), "routes": routes,
        "frame_list": frames,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", metavar="KEY", help="emit one program's model, e.g. P01")
    a = ap.parse_args()
    files = sorted((ROOT / "programs" / "en").glob("*.tex"))
    if a.json:
        f = next((p for p in files if p.stem.startswith(a.json)), None)
        if f is None:
            sys.exit(f"no program {a.json!r}")
        print(json.dumps(probe(f), indent=1, ensure_ascii=False))
        return 0
    tot = Counter()
    boxes = Counter()
    keys: set[str] = set()      # the union, not the sum: P01 quotes F03's keys
    print(f"{'program':<34}{'frames':>7}{'answer':>8}{'cues':>6}{'boxes':>7}"
          f"{'maths':>7}{'vals':>6}{'figs':>6}{'Q':>4}{'T':>4}{'P':>4}")
    for f in files:
        p = probe(f)
        nb = sum(p["boxes"].values())
        boxes.update(p["boxes"])
        for k in ("frames", "answer_openers", "cues", "maths", "vals", "quiz",
                  "tests", "further"):
            tot[k] += p[k]
        tot["boxes"] += nb
        keys |= {v for f in p["frame_list"] for v in f["vals"]}
        tot["figs"] += len(p["figs"])
        tot["transcripts"] += len(p["transcripts"])
        tot["routes"] += len(p["routes"])
        tot["sections"] += len(p["sections"])
        print(f"{p['program']:<34}{p['frames']:>7}{p['answer_openers']:>8}{p['cues']:>6}"
              f"{nb:>7}{p['maths']:>7}{p['vals']:>6}{len(p['figs']):>6}"
              f"{p['quiz']:>4}{p['tests']:>4}{p['further']:>4}")
    print("-" * 93)
    print(f"{len(files)} programs, {tot['sections']} sections, {tot['frames']} frames: "
          f"{tot['answer_openers']} open with an answer, {tot['cues']} end with a cue "
          f"({100 * tot['cues'] // tot['frames']}% elicitation)")
    print(f"{tot['boxes']} admonition boxes: " +
          ", ".join(f"{k} {v}" for k, v in boxes.most_common()))
    print(f"{tot['maths']} maths spans, {len(keys)} distinct \\val{{}} keys referenced, "
          f"{tot['figs']} figures, {tot['transcripts']} transcripts")
    print(f"{tot['quiz']} Quiz items with {tot['routes']} routes back into the frames, "
          f"{tot['tests']} Test exercises, {tot['further']} Further problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
