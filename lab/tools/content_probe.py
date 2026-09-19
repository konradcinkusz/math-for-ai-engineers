#!/usr/bin/env python3
"""How much of the book is already a content model, measured rather than asserted.

The learning application proposed in notes/10-learning-app.md rests on one
claim: the book's LaTeX is structured enough to compile into frames, answers,
cues, quizzes, routes and values without hand work. This probe tests the claim
with the book's own tokeniser, tools/parity.py, which every build already runs
over every program. It reads programs/en and reports, per program and in total:

  * frames, and how many open with an answer (\ans or ansblock) -- the
    covered box the whole method rests on, each one classified by the
    strongest machine check its content admits (--answers);
  * frames that end with the next-frame cue (which is the elicitation rate,
    since C16 makes the cue sit exactly where the next frame answers);
  * the retrieval modes a frame carries (dotline, blank, yourturn);
  * admonition boxes by kind; maths spans; \val{} references; figures;
  * Quiz / Test / Further items, and the Quiz routes back into the frames.

    python3 lab/tools/content_probe.py             # totals, one line per program
    python3 lab/tools/content_probe.py --json P01  # one program as the model
                                                   # the compiler would emit
    python3 lab/tools/content_probe.py --answers   # the answer classification,
                                                   # per program, both editions
    python3 lab/tools/content_probe.py --selftest  # the classifier watched
                                                   # producing known answers

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
LANGS = ("en", "pl")
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


# --------------------------------------------------------------------------
# Classifying an answer opener
# --------------------------------------------------------------------------
# The covered box is the method, so "how many frames open with an answer" is
# the first number anybody wants. The second is what KIND of answer each one
# is, because a checker can compare a printed value to the character and can
# do nothing whatever with a sentence. The four classes below are ordered by
# the strength of the check the answer's own content admits:
#
#   val         at least one \val{} -- a number the book computes, commits to
#               figures/values/ and gates with `make verify`. Checkable by
#               string comparison at printed precision, per language, which is
#               the lab's own rule (a check compares strings, never floats).
#   literal     no \val{}, but a maths span that is a bare number the book
#               writes inline. Still a string comparison -- against a literal
#               in the prose, so no script stands behind it and nothing gates
#               it. This class is NOT one of the four the requirement named;
#               it exists because the book deliberately writes head arithmetic
#               inline rather than behind \val{}, and calling those answers
#               `expression` would overstate how hard they are to check.
#   expression  a formula. Checkable only under a canonical digest, and the
#               probe that measured one reports it is not an invariant.
#   prose       no maths at all: a sentence, a word, a name. Self-assessment.
#
# `choice` -- one of a stated set -- is deliberately NOT reported, and the
# reason is structural rather than an omission: an opener carries the ANSWER,
# and being one of a stated set is a property of the QUESTION. A surface test
# on the answer reads language rather than question shape; the pass that added
# this ran one (does the answer open Yes/No/Tak/Nie) and it fired a different
# number of times in the two editions over the identical 1030 frames, every
# difference being Polish fronting `Nie` where English writes "There is no
# solution". The question is recoverable -- it is the preceding frame, which
# C16 makes carry the cue -- so a later pass has the input; classifying it is
# a reading job in two languages and the probe does not pretend otherwise.

MATH_SPAN = re.compile(
    r"\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]"
    r"|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray)\}"
    r".*?\\end\{\1\}", re.S)

# A maths span whose whole content is a number written inline: 15, (3, 6),
# \num{3.1e-6}, 2^{10}, \frac{1}{2}, with a sign, brackets, a percent or a
# trailing full stop allowed around it.
NUMERIC_SPAN = re.compile(r"""^[\s+\-()]*(?:
      \\num\{[^{}]*\}
    | \d[\d\s,.]*(?:\\?[eE][-+]?\d+)?
    | \\d?frac\{\d+\}\{\d+\}
    | \d+\^\{?[-+]?\d+\}?
    )[\s%)]*(?:\\%|\\,)?[\s.,]*$""", re.X)

LEAD = re.compile(r"\s*(?:\\label\{[^{}]*\}\s*)*")
# Macros whose braces hold prose that survives; and macros whose whole call goes.
KEEP_BODY = "emph|textbf|textit|enquote|code|api|pkg|text|textrm|mbox"
DROP_WHOLE = "ref|eqref|pageref|label|index|cite"


def answer_opener(slice_: str) -> tuple[str, str] | None:
    """(kind, body) of the answer a frame opens with, or None.

    A leading \\label marks a position and typesets nothing, so it is skipped
    -- which is the same rule C16 applies when it decides where a cue belongs.
    """
    m = re.match(r"\s*\\begin\{fr\}", slice_)
    if not m:
        return None
    i = LEAD.match(slice_, m.end()).end()
    if slice_.startswith(r"\ans", i):
        # parity's own brace reader, not a second one written here
        return "ans", parity._balanced(slice_, i + len(r"\ans"))[0]
    if slice_.startswith(r"\begin{ansblock}", i):
        j = slice_.find(r"\end{ansblock}", i)
        head = i + len(r"\begin{ansblock}")
        return "ansblock", slice_[head:j if j >= 0 else len(slice_)]
    return None


def _residue(body: str) -> str:
    """The prose left when every checkable token is taken out of an answer.

    Deliberately carries NO word list. One would put `About $\\val{k}$` and
    `Okolo $\\val{k}$` in different buckets, because a word list is a fact about
    a language and those two are the same answer. Two were tried while this was
    written and they disagreed between the editions by DIFFERENT amounts, which
    is the argument against both: the amount is a property of the list rather
    than of the book. Requiring the residue to be empty disagrees 0 times, and
    --answers prints that number on every run.
    """
    prev, b = None, body
    while prev != b:                       # a display can hold an inline span
        prev, b = b, MATH_SPAN.sub(" ", b)
    b = re.sub(r"\\(?:%s)\s*\{" % KEEP_BODY, "{", b)
    b = re.sub(r"\\(?:%s)\s*\{[^{}]*\}" % DROP_WHOLE, " ", b)
    b = re.sub(r"\\dash\{\}|\\ldots|\\quad|\\qquad|\\\\|\\%|\\,|\\;|\\:", " ", b)
    b = re.sub(r"\\[A-Za-z@]+\*?", " ", b)
    b = re.sub(r"[{}$~^_&%]", " ", b)
    return re.sub(r"\s+", " ", b).strip()


# A \code{} answer was measured for a branch of its own and did not earn one.
# Nearly every answer that carries a \code{} carries it inside a larger answer,
# where it is a format name or an API call rather than the thing being asked
# for. The two where the whole answer IS a \code{} disagree with each other
# about what kind of token that is -- one is an einsum string, which is a
# literal, and the other a boolean expression -- so a rule keyed on \code{}
# would be wrong about one of the two whichever way it went. Both fall to
# `prose`, which says truthfully that this taxonomy does not check them.
def classify_answer(body: str) -> tuple[str, str]:
    """(class, shape) for one answer opener.

    The class is the strongest check the answer's content admits. The shape is
    `bare` when that content is the whole answer and `wrapped` when a sentence
    surrounds it -- so `bare` is the count a checker can be certain about and
    `wrapped` is the count where a person has to decide which part was the
    answer. A \\val inside a maths span counts: the tokeniser digests a maths
    body whole, which is the trap that made the first run of this probe report
    zero values in P01, so the scan is over the source of the answer.
    """
    spans = [re.sub(r"^\$\$|\$\$$|^\$|\$$|^\\\[|\\\]$", "", m.group(0)).strip()
             for m in MATH_SPAN.finditer(body)]
    if RE_VALREF.search(body):
        cls = "val"
    elif any(NUMERIC_SPAN.match(x) for x in spans):
        cls = "literal"
    elif spans:
        cls = "expression"
    else:
        return "prose", "n/a"
    stripped = re.sub(r"[.,;:!?()\[\]\u2014\u2013-]", " ", _residue(body))
    return cls, ("bare" if not stripped.split() else "wrapped")


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
        opener = answer_opener(slice_) if first in OPENERS else None
        answer = None
        if opener is not None:
            cls, shape = classify_answer(opener[1])
            answer = {"kind": opener[0], "class": cls, "shape": shape,
                      # what a checker would compare the reader's typing against
                      "vals": sorted(set(RE_VALREF.findall(opener[1])))}
        out.append({
            "n": f["n"],
            "line": f["line"],
            "opens_with_answer": first in OPENERS,
            "answer": answer,
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
        "answers": dict(Counter(f"{f['answer']['class']}.{f['answer']['shape']}"
                                for f in frames if f["answer"])),
        "answer_kinds": dict(Counter(f["answer"]["kind"]
                                     for f in frames if f["answer"])),
        "quiz": items.get("Q", 0), "tests": items.get("T", 0),
        "further": items.get("P", 0), "routes": routes,
        "frame_list": frames,
    }


# --------------------------------------------------------------------------
# The two watches
# --------------------------------------------------------------------------
# A classifier that has only ever been watched saying "prose" has told you
# nothing, so the fixtures below are hand-classified answers the classifier
# must agree with, and MUTATIONS of them where one edit must change the
# answer. Both directions, because a test that only ever passes is the same
# shape as a check that cannot fail.
#
# The first four rows are the trap this file already records from the other
# end: the tokeniser digests a maths body whole, so a \val inside a display --
# and a \val inside a \text{} inside a display -- is invisible to a token
# count. Each is paired with the same body minus the \val, which must stop
# being `val`.

# Each row is an answer body, what it must classify as, and why it is here.
# Rows marked `mutation` are the previous row with one edit that must change
# the answer -- both directions, because a test that only ever passes is the
# same shape as a check that cannot fail.
SELFTEST = [
    (r"$\val{f09.len3d}$", "val.bare",
     r"one \val and nothing else"),
    (r"$11$", "literal.bare",
     r"mutation: the \val goes and a bare numeral stays"),
    (r"\[ \text{gap} = \val{p01.gap.one} \]", "val.bare",
     r"a \val inside a \text{} inside a display -- invisible to a token count"),
    (r"\[ \text{gap} = 2^{-52} \]", "expression.bare",
     r"mutation: the \val goes"),
    (r"$\logb{2} 10 = \dfrac{\ln 10}{\ln 2} = \val{f03.log2.ten}$", "val.bare",
     r"a \val at the end of a formula, also inside one maths span"),
    (r"$\logb{2} 10 = \dfrac{\ln 10}{\ln 2}$", "expression.bare",
     r"mutation: the \val goes"),
    (r"Fewer. About $\val{p05.near.n.64}$.", "val.wrapped",
     "a hedge is prose, and prose wraps"),
    (r"$\val{p05.near.n.64}$", "val.bare",
     "mutation: the sentence goes"),
    (r"$\val{f01.weights.bytes}$ bytes.", "val.wrapped",
     "a unit is a word, and a word list would have called this bare"),
    (r"$\val{p33.eta.margin}$ per cent", "val.wrapped",
     "so would this one"),
    (r"Exactly $0$", "literal.wrapped",
     "and this -- `Dokladnie $0$` in the twin, which is the whole point"),
    (r"$\num{3.1e-6}$", "literal.bare", r"a \num{} is a number"),
    (r"$(3, 6)$", "literal.bare", "so is a pair of them"),
    (r"$\cos\theta = \dfrac{a \cdot b}{\lVert a \rVert \lVert b \rVert}$",
     "expression.bare", "a formula, and the whole answer"),
    (r"It falls like $\sigma/\sqrt{n}$", "expression.wrapped",
     "a formula inside a sentence"),
    (r"No", "prose.n/a", "the shortest answer in the book"),
    (r"The uniform one", "prose.n/a", "and a choice, which this taxonomy cannot see"),
    (r"\code{'bhqd,bhkd->bhqk'}", "prose.n/a",
     "a code token is prose here, deliberately -- see above classify_answer"),
    (r"\code{True}. The sum is $\val{p01.swamp.sum}$.", "val.wrapped",
     r"mutation: one \val and the class changes"),
]


def selftest() -> int:
    """Watch the classifier produce answers that are known before it runs."""
    bad = 0
    for body, want, why in SELFTEST:
        got = ".".join(classify_answer(body))
        ok = got == want
        bad += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {want:<18} "
              f"{'' if ok else 'got ' + got + '  '}{why}")
    # And the opener parser itself, which decides what gets classified at all.
    cases = [
        (r"\begin{fr}" "\n" r"\ans{$5$}" "\n" r"\end{fr}",           ("ans", r"$5$")),
        (r"\begin{fr}\label{x}" "\n" r"\ans{$5$}",                   ("ans", r"$5$")),
        (r"\begin{fr}" "\n" r"\begin{ansblock}Yes.\end{ansblock}",   ("ansblock", "Yes.")),
        (r"\begin{fr}" "\n" "Plain prose, no answer here.",          None),
    ]
    for src, want in cases:
        got = answer_opener(src)
        ok = got == want
        bad += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} opener {'' if ok else 'got %r ' % (got,)}"
              f"{src.splitlines()[0][:40]!r}")
    print(f"{len(SELFTEST) + len(cases)} watches, {bad} failed")
    return 1 if bad else 0


def answers_table() -> int:
    """The classification, per program and per edition, and the totals."""
    cols = [f"{c}.{s}" for c in ("val", "literal", "expression")
            for s in ("bare", "wrapped")] + ["prose.n/a"]
    head = ["v.bare", "v.wrap", "l.bare", "l.wrap", "e.bare", "e.wrap", "prose"]
    grand: dict[str, Counter] = {}
    per: dict[str, dict[str, dict]] = {}
    for lang in LANGS:
        grand[lang] = Counter()
        per[lang] = {}
        for f in sorted((ROOT / "programs" / lang).glob("*.tex")):
            p = probe(f)
            per[lang][p["program"].split("-")[0]] = p
            grand[lang].update(p["answers"])
    # The per-program rows are the English edition; the two totals under them,
    # and the line after, are what says whether that was a fair thing to print.
    print(f"{'program':<8}{'openers':>8}" +
          "".join(f"{h:>9}" for h in head) + f"{'ans':>6}{'block':>6}")
    for key in sorted(per["en"]):
        p = per["en"][key]
        a = Counter(p["answers"])
        print(f"{key:<8}{p['answer_openers']:>8}" +
              "".join(f"{a.get(c, 0):>9}" for c in cols) +
              f"{p['answer_kinds'].get('ans', 0):>6}"
              f"{p['answer_kinds'].get('ansblock', 0):>6}")
    print("-" * 93)
    for lang in LANGS:
        g = grand[lang]
        print(f"{lang:<8}{sum(g.values()):>8}" +
              "".join(f"{g.get(c, 0):>9}" for c in cols))
    # The finding the two rows above are there to make checkable.
    diff = sum(per["en"][k]["answers"] != per["pl"][k]["answers"] for k in per["en"])
    same = "identical in both editions" if grand["en"] == grand["pl"] else \
           "NOT identical between the editions"
    print(f"class x shape totals are {same}; "
          f"{diff} of {len(per['en'])} programs differ")
    g = grand["en"]
    tot = sum(g.values())
    print(f"of {tot} openers, {g['val.bare'] + g['literal.bare']} are a number and "
          f"nothing else, which a check can be certain about; "
          f"{g['val.wrapped'] + g['literal.wrapped']} carry a number inside a "
          f"sentence, and a check can only ever be certain about the number; "
          f"{g['expression.bare'] + g['expression.wrapped']} are a formula, which "
          f"needs a canonical digest; {g['prose.n/a']} are prose.")
    print("`choice` is not reported: an opener carries the answer, and being one "
          "of a stated set is a property of the question. See the comment above "
          "MATH_SPAN.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", metavar="KEY", help="emit one program's model, e.g. P01")
    ap.add_argument("--answers", action="store_true",
                    help="classify every answer opener, per program, both editions")
    ap.add_argument("--selftest", action="store_true",
                    help="watch the classifier produce answers known in advance")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.answers:
        return answers_table()
    files = sorted((ROOT / "programs" / "en").glob("*.tex"))
    if a.json:
        f = next((p for p in files if p.stem.startswith(a.json)), None)
        if f is None:
            sys.exit(f"no program {a.json!r}")
        print(json.dumps(probe(f), indent=1, ensure_ascii=False))
        return 0
    tot = Counter()
    boxes = Counter()
    answers: Counter = Counter()
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
        answers.update(p["answers"])
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
    print(f"answer openers by strongest check available: " +
          ", ".join(f"{k} {answers[k]}" for k in sorted(answers)) +
          "  (--answers for the table, and for the other edition)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
