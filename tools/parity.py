#!/usr/bin/env python3
"""Prove that the Polish and English editions are the same book.

The two editions live in parallel trees (programs/en, programs/pl, ...). Prose
is duplicated on purpose; *structure* must not be. This script extracts an
ordered structural signature from each source file and compares the twins.

It is deliberately stricter than "same number of frames". A book taught by
numbered frames breaks the moment frame 12 of the Polish edition teaches
something other than frame 12 of the English one, because the Summary, the
Quiz and the "Can you?" checklist all navigate by frame number.

Run:  python3 tools/parity.py            (from the repository root)
Exit: 0 clean, 1 divergence, 2 usage error.

A deliberate divergence is declared by putting

    % parity: allow-divergence <reason>

in BOTH files at the corresponding point. The next token is then dropped from
both signatures. Those markers are debt and `make debt` counts them.
"""

from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("en", "pl")
TREES = ("programs", "appendices", "frontmatter")

# --------------------------------------------------------------------------
# Tokenising
# --------------------------------------------------------------------------

# Environments whose \item is a numbered, answerable exercise. The key is what
# the answer at the back of the book is filed under, so a mismatch here means a
# reader looking up "T3" gets a different question in the two editions.
ITEM_ENVS = {"quiz": "Q", "testexercises": "T", "furtherproblems": "P"}

# Admonitions. A trap present in one edition and not the other means the two
# editions correct different misconceptions, which is a content difference
# wearing a translation's clothes.
BOXES = (
    "note warning trapbox aibox rigourbox notationbox verifybox exercisebox "
    "outcomes quiz summarybox testexercises furtherproblems ansblock fr"
).split()

MATH_ENVS = ("equation", "equation*", "align", "align*", "gather", "gather*",
             "multline", "multline*", "eqnarray")

# Macros that carry a payload which must be identical across editions, because
# the payload is a number, a key or a cross-reference rather than prose.
KEYED = {
    "label": "LABEL", "ref": "REF", "eqref": "REF", "pageref": "REF",
    "val": "VAL", "rawval": "VAL", "mermaidfig": "FIG",
    "teachesat": "TEACHESAT", "sumitem": "SUMITEM", "outcome": "OUTCOME",
}

# Macros with no payload worth comparing, but whose presence and position are
# the pedagogy.
BARE = {
    "yourturn": "YOURTURN", "dotline": "DOTLINE", "blank": "BLANK",
    "canyou": "CANYOU", "ans": "ANS", "answerto": "ANSWERTO",
    "programstub": "STUB", "program": "PROGRAM", "printanswers": "PRINTANSWERS",
    "foundationnumbering": "FNUM", "mainnumbering": "MNUM",
}

ALLOW_RE = re.compile(r"^[ \t]*%[ \t]*parity:[ \t]*allow-divergence\b(.*)$", re.M)
COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.M)


@dataclass
class Token:
    kind: str
    payload: str
    line: int

    def key(self) -> str:
        return f"{self.kind}({self.payload})" if self.payload else self.kind


@dataclass
class Doc:
    path: Path
    tokens: list[Token] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    refs: list[str] = field(default_factory=list)
    vals: list[str] = field(default_factory=list)
    figs: list[str] = field(default_factory=list)
    answer_keys: list[str] = field(default_factory=list)
    frames: int = 0
    allows: int = 0
    # frame index -> list of math digests taught in that frame
    frame_math: dict[int, list[str]] = field(default_factory=dict)


def _balanced(src: str, i: int) -> tuple[str, int]:
    """Read a brace group starting at src[i] == '{'. Returns (body, next_index)."""
    if i >= len(src) or src[i] != "{":
        return "", i
    depth, j = 0, i
    while j < len(src):
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[i + 1:j], j + 1
        j += 1
    return src[i + 1:], len(src)


def _norm_math(body: str) -> str:
    """Normalise a maths body so that only its mathematical content survives.

    Whitespace and \\, spacing are noise. Nothing else is stripped: if the two
    editions disagree about a sign or an exponent, that must show up.
    """
    b = COMMENT_RE.sub("", body)
    b = re.sub(r"\\[,;:!> ]", "", b)
    b = re.sub(r"\s+", "", b)
    return hashlib.sha1(b.encode("utf8")).hexdigest()[:10]


def tokenise(path: Path) -> Doc:
    src = path.read_text(encoding="utf8")
    doc = Doc(path=path)

    # Record the allow-divergence markers by line before comments are stripped.
    allow_lines = {src[:m.start()].count("\n") + 1 for m in ALLOW_RE.finditer(src)}
    doc.allows = len(allow_lines)

    src_nc = COMMENT_RE.sub("", src)
    envstack: list[str] = []
    counters: dict[str, int] = {}
    i, n = 0, len(src_nc)
    cur_frame = 0

    def line_at(pos: int) -> int:
        return src_nc.count("\n", 0, pos) + 1

    def emit(kind: str, payload: str, pos: int) -> None:
        doc.tokens.append(Token(kind, payload, line_at(pos)))

    while i < n:
        c = src_nc[i]

        # ---- maths -------------------------------------------------------
        if c == "$":
            display = src_nc.startswith("$$", i)
            close = "$$" if display else "$"
            j = i + len(close)
            while j < n:
                if src_nc[j] == "\\":
                    j += 2
                    continue
                if src_nc.startswith(close, j):
                    break
                j += 1
            body = src_nc[i + len(close):j]
            d = _norm_math(body)
            emit("MATH", d, i)
            doc.frame_math.setdefault(cur_frame, []).append(d)
            i = j + len(close)
            continue

        if src_nc.startswith("\\[", i):
            j = src_nc.find("\\]", i)
            j = n if j < 0 else j
            d = _norm_math(src_nc[i + 2:j])
            emit("MATH", d, i)
            doc.frame_math.setdefault(cur_frame, []).append(d)
            i = j + 2
            continue

        if c != "\\":
            i += 1
            continue

        m = re.match(r"\\([A-Za-z@]+)\*?", src_nc[i:])
        if not m:
            i += 2
            continue
        name = m.group(1)
        after = i + m.end()

        # ---- environments ------------------------------------------------
        if name in ("begin", "end"):
            body, nxt = _balanced(src_nc, after)
            if name == "begin":
                envstack.append(body)
                if body in MATH_ENVS:
                    endtok = "\\end{%s}" % body
                    j = src_nc.find(endtok, nxt)
                    j = n if j < 0 else j
                    d = _norm_math(src_nc[nxt:j])
                    emit("MATH", d, i)
                    doc.frame_math.setdefault(cur_frame, []).append(d)
                    envstack.pop()
                    i = j + len(endtok)
                    continue
                if body in BOXES:
                    if body == "fr":
                        doc.frames += 1
                        cur_frame = doc.frames
                        emit("FRAME", str(doc.frames), i)
                    else:
                        emit("BEGIN", body, i)
                    if body in ITEM_ENVS:
                        counters[body] = 0
            else:
                if envstack and envstack[-1] == body:
                    envstack.pop()
                if body in BOXES and body != "fr":
                    emit("END", body, i)
            i = nxt
            continue

        # ---- \item -------------------------------------------------------
        if name == "item":
            env = next((e for e in reversed(envstack) if e in ITEM_ENVS), None)
            if env:
                counters[env] = counters.get(env, 0) + 1
                key = f"{ITEM_ENVS[env]}{counters[env]}"
                doc.answer_keys.append(key)
                emit("EXITEM", key, i)
            else:
                emit("ITEM", "", i)
            i = after
            continue

        # ---- keyed macros -------------------------------------------------
        if name in KEYED:
            body, nxt = _balanced(src_nc, after)
            kind = KEYED[name]
            if kind == "LABEL":
                doc.labels.append(body)
            elif kind == "REF":
                doc.refs.append(body)
            elif kind == "VAL":
                doc.vals.append(body)
            elif kind == "FIG":
                doc.figs.append(body)
            # \outcome{frames}{text} and \sumitem{frame}{text}: only the frame
            # reference is compared. The text is prose and is expected to differ.
            emit(kind, body.strip(), i)
            i = nxt
            continue

        if name in BARE:
            emit(BARE[name], "", i)
            i = after
            continue

        i = after

    # Apply the allow-divergence markers: drop the first token on or after
    # each marked line.
    if allow_lines:
        keep, dropped = [], set()
        for t in doc.tokens:
            cand = min((l for l in allow_lines if l <= t.line and l not in dropped),
                       default=None)
            if cand is not None and t.line - cand <= 3:
                dropped.add(cand)
                continue
            keep.append(t)
        doc.tokens = keep
    return doc


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

class Report:
    def __init__(self) -> None:
        self.fail: list[str] = []
        self.warn: list[str] = []
        self.ok: list[str] = []

    def bad(self, check: str, msg: str) -> None:
        self.fail.append(f"[{check}] {msg}")

    def soft(self, check: str, msg: str) -> None:
        self.warn.append(f"[{check}] {msg}")

    def good(self, check: str, msg: str) -> None:
        self.ok.append(f"[{check}] {msg}")


def twin(path: Path, lang: str) -> Path:
    parts = list(path.relative_to(ROOT).parts)
    for k, p in enumerate(parts):
        if p in LANGS:
            parts[k] = lang
            break
    return ROOT.joinpath(*parts)


def check_filesets(rep: Report) -> list[tuple[Path, Path]]:
    pairs = []
    for tree in TREES:
        base = ROOT / tree
        if not base.is_dir():
            continue
        sets = {}
        for lang in LANGS:
            d = base / lang
            sets[lang] = {p.name for p in d.glob("*.tex")} if d.is_dir() else set()
        only_en = sorted(sets["en"] - sets["pl"])
        only_pl = sorted(sets["pl"] - sets["en"])
        for f in only_en:
            rep.bad("C1-files", f"{tree}/en/{f} has no Polish twin")
        for f in only_pl:
            rep.bad("C1-files", f"{tree}/pl/{f} has no English twin")
        for f in sorted(sets["en"] & sets["pl"]):
            pairs.append((base / "en" / f, base / "pl" / f))
    if not pairs:
        rep.soft("C1-files", "no paired .tex sources found yet")
    else:
        rep.good("C1-files", f"{len(pairs)} file pairs")
    return pairs


def check_includes(rep: Report) -> None:
    got = {}
    for lang in LANGS:
        m = ROOT / f"main-{lang}.tex"
        if not m.is_file():
            rep.soft("C2-order", f"main-{lang}.tex missing")
            return
        src = COMMENT_RE.sub("", m.read_text(encoding="utf8"))
        got[lang] = [re.sub(rf"/{lang}/", "/<lang>/", x)
                     for x in re.findall(r"\\include\{([^}]*)\}", src)]
    if got["en"] != got["pl"]:
        a, b = got["en"], got["pl"]
        for k in range(max(len(a), len(b))):
            x = a[k] if k < len(a) else "<missing>"
            y = b[k] if k < len(b) else "<missing>"
            if x != y:
                rep.bad("C2-order", f"include #{k+1} differs: en={x} pl={y}")
                break
    else:
        rep.good("C2-order", f"{len(got['en'])} includes in the same order")


def check_lang_catalogue(rep: Report) -> None:
    defs = {}
    for lang in LANGS:
        p = ROOT / "lang" / f"{lang}.tex"
        if not p.is_file():
            rep.bad("C3-lang", f"lang/{lang}.tex missing")
            return
        src = COMMENT_RE.sub("", p.read_text(encoding="utf8"))
        names = set(re.findall(r"\\newcommand\{\\([A-Za-z@]+)\}", src))
        names |= set(re.findall(r"\\DeclareMathOperator\*?\{\\([A-Za-z@]+)\}", src))
        defs[lang] = names
    for miss in sorted(defs["en"] - defs["pl"]):
        rep.bad("C3-lang", f"\\{miss} defined in en but not pl")
    for miss in sorted(defs["pl"] - defs["en"]):
        rep.bad("C3-lang", f"\\{miss} defined in pl but not en")
    if defs["en"] == defs["pl"]:
        rep.good("C3-lang", f"{len(defs['en'])} macros defined in both")


def check_signature(rep: Report, en: Doc, pl: Doc) -> None:
    name = en.path.name
    a = [t.key() for t in en.tokens]
    b = [t.key() for t in pl.tokens]
    if a == b:
        rep.good("C4-structure", f"{name}: {len(a)} tokens, {en.frames} frames")
        return
    for k in range(max(len(a), len(b))):
        x = a[k] if k < len(a) else None
        y = b[k] if k < len(b) else None
        if x != y:
            el = en.tokens[k].line if k < len(en.tokens) else "EOF"
            pll = pl.tokens[k].line if k < len(pl.tokens) else "EOF"
            rep.bad(
                "C4-structure",
                f"{name}: diverge at token {k+1} -- "
                f"en:{el} {x or '<end of file>'} != pl:{pll} {y or '<end of file>'}",
            )
            break
    if en.frames != pl.frames:
        rep.bad("C4-structure",
                f"{name}: frame count en={en.frames} pl={pl.frames}")


def check_sets(rep: Report, en: Doc, pl: Doc) -> None:
    name = en.path.name
    for what, ea, pa, check in (
        ("label", en.labels, pl.labels, "C5-labels"),
        ("answer key", en.answer_keys, pl.answer_keys, "C6-answers"),
        ("value key", en.vals, pl.vals, "C7-values"),
        ("diagram key", en.figs, pl.figs, "C9-diagrams"),
    ):
        se, sp = set(ea), set(pa)
        for k in sorted(se - sp):
            rep.bad(check, f"{name}: {what} {k!r} in en only")
        for k in sorted(sp - se):
            rep.bad(check, f"{name}: {what} {k!r} in pl only")


def check_math(rep: Report, en: Doc, pl: Doc) -> None:
    """A sign fixed in one edition and not the other is the drift that matters.

    This works only because the notation contract is executed by macros: both
    editions write \\tg, \\Var, \\intcc, so the maths *source* is byte-identical
    even though the two PDFs set different symbols. Hard-code `tan` in the
    English edition and this check is what tells you.
    """
    name = en.path.name
    frames = sorted(set(en.frame_math) | set(pl.frame_math))
    bad = 0
    for f in frames:
        a = en.frame_math.get(f, [])
        b = pl.frame_math.get(f, [])
        if a != b:
            bad += 1
            if bad <= 3:
                rep.bad("C8-math",
                        f"{name}: frame {f} maths differs "
                        f"(en {len(a)} expr, pl {len(b)} expr)")
    if bad > 3:
        rep.bad("C8-math", f"{name}: ... and {bad-3} more frames")
    if not bad and frames:
        rep.good("C8-math", f"{name}: maths identical across {len(frames)} frames")


def check_value_defs(rep: Report, docs: list[Doc]) -> None:
    defined = set()
    vdir = ROOT / "figures" / "values"
    if vdir.is_dir():
        for p in vdir.glob("*.tex"):
            defined |= set(re.findall(r"\\mfaval\{([^}]*)\}", p.read_text(encoding="utf8")))
    used = {v for d in docs for v in d.vals}
    for k in sorted(used - defined):
        rep.bad("C7-values", f"\\val{{{k}}} used but no script produces it")
    unused = sorted(defined - used)
    if unused:
        rep.soft("C7-values", f"{len(unused)} computed values are unused: "
                              + ", ".join(unused[:5]))


def check_diagram_sources(rep: Report, docs: list[Doc]) -> None:
    keys = {f for d in docs for f in d.figs}
    for k in sorted(keys):
        for lang in LANGS:
            p = ROOT / "figures" / "mermaid" / lang / f"{k}.mmd"
            if not p.is_file():
                rep.bad("C9-diagrams", f"missing {p.relative_to(ROOT)}")


# ---- notation lint --------------------------------------------------------

FORBIDDEN = {
    r"\\tan\b(?!h)": r"\tan -- use \tg (the contract macro); it sets tan in en and tg in pl",
    r"\\cot\b(?!h)": r"\cot -- use \ctg",
    r"\\arctan\b": r"\arctan -- use \arctg",
    r"\\arccot\b": r"\arccot -- use \arcctg",
    r"\\gcd\b": r"\gcd -- use \gcdop (NWD in the Polish edition)",
    r"\\operatorname\{lcm\}": r"lcm -- use \lcmop (NWW in the Polish edition)",
    r"\\Pr\b": r"\Pr -- use \Prob",
    r"\\log(?![a-zA-Z_])(?!\s*_)": (
        r"a bare \log -- Polish textbooks read bare log as base 10 and AI papers "
        r"read it as base e. Write \ln or \log_2 explicitly."
    ),
}

MATH_SPAN = re.compile(r"\$[^$]*\$|\\\[.*?\\\]", re.S)
LISTING_SPAN = re.compile(
    r"\\begin\{(python|console|shellcmd|lstlisting|verbatim)\}.*?\\end\{\1\}", re.S)


def check_notation(rep: Report, path: Path) -> None:
    raw = path.read_text(encoding="utf8")
    src = COMMENT_RE.sub("", raw)
    rel = path.relative_to(ROOT)

    listings = list(LISTING_SPAN.finditer(src))

    def in_listing(pos: int) -> bool:
        return any(m.start() <= pos < m.end() for m in listings)

    for pat, why in FORBIDDEN.items():
        for m in re.finditer(pat, src):
            if in_listing(m.start()):
                continue
            rep.bad("C10-notation",
                    f"{rel}:{src.count(chr(10), 0, m.start())+1} {why}")

    # A decimal point inside maths defeats the locale. Numbers belong in
    # \num{} or \val{} so that the Polish edition gets its comma for free.
    for m in MATH_SPAN.finditer(src):
        if in_listing(m.start()):
            continue
        body = m.group(0)
        for d in re.finditer(r"(?<![\w.\\])\d+\.\d+", body):
            seg = body[max(0, d.start() - 12):d.start()]
            if "\\num" in seg or "\\val" in seg or "\\rawval" in seg:
                continue
            rep.bad("C10-notation",
                    f"{rel}:{src.count(chr(10), 0, m.start())+1} "
                    f"bare decimal {d.group(0)!r} in maths -- wrap it in "
                    f"\\num{{}} or \\val{{}} or the Polish edition prints a "
                    f"full stop where it owes a comma")

    # \val expands to nothing useful inside a verbatim listing. Verified: it
    # prints the macro name. Console transcripts must be generated files.
    for m in listings:
        for bad in re.finditer(r"\\(raw)?val\{", m.group(0)):
            rep.bad("C10-notation",
                    f"{rel}:{src.count(chr(10), 0, m.start()+bad.start())+1} "
                    f"\\val inside a verbatim listing does not expand -- "
                    f"\\lstinputlisting a transcript written by code/ instead")

    if path.parts[-2] == "pl":
        for m in re.finditer(r'(?<![\\%])"', src):
            if not in_listing(m.start()):
                rep.soft("C10-notation",
                         f"{rel}:{src.count(chr(10), 0, m.start())+1} "
                         f'straight quote -- Polish opens with \\pq{{...}} (,,...")')
                break


# --------------------------------------------------------------------------

def main() -> int:
    rep = Report()
    pairs = check_filesets(rep)
    check_includes(rep)
    check_lang_catalogue(rep)

    docs: list[Doc] = []
    for en_p, pl_p in pairs:
        en, pl = tokenise(en_p), tokenise(pl_p)
        docs += [en, pl]
        check_signature(rep, en, pl)
        check_sets(rep, en, pl)
        check_math(rep, en, pl)
        check_notation(rep, en_p)
        check_notation(rep, pl_p)

    check_value_defs(rep, docs)
    check_diagram_sources(rep, docs)

    allows = sum(d.allows for d in docs)
    frames = sum(d.frames for d in docs if d.path.parts[-2] == "en")

    print("=" * 68)
    print("EDITION PARITY")
    print("=" * 68)
    for line in rep.ok:
        print("  ok    " + line)
    for line in rep.warn:
        print("  warn  " + line)
    for line in rep.fail:
        print("  FAIL  " + line)
    print("-" * 68)
    print(f"  {len(pairs)} file pairs | {frames} frames | "
          f"{allows} declared divergences | "
          f"{len(rep.fail)} failures, {len(rep.warn)} warnings")
    return 1 if rep.fail else 0


if __name__ == "__main__":
    sys.exit(main())
