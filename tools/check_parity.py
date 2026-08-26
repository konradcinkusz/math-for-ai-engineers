#!/usr/bin/env python3
"""Prove that the Polish and English editions have not drifted apart.

A bilingual book fails in one particular way: a correction is applied to one
edition and quietly missed in the other, and nobody notices until a reader of
the neglected language hits the error. Nothing about the writing process
prevents that. This does.

It compares, per program:

  * frame count and frame numbering
  * the set of \\label{}s
  * the number of quiz questions, test exercises and further problems
  * every numeric literal, in order, once the Polish decimal comma has been
    normalised to a full stop -- the check that catches a translated number
    silently changing
  * the histogram of macro usage, so a macro dropped in translation is caught
  * that no listings, console or python environment contains a non-ASCII
    character in either edition

It also checks that lang/en.tex and lang/pl.tex define the same macro set,
because a label defined in one language and not the other is an undefined
control sequence in exactly one of the two builds.

Usage:
    tools/check_parity.py                    # the whole book
    tools/check_parity.py A.tex B.tex        # one pair, for a draft in progress
Exit code is non-zero on any mismatch.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RE_FRAME = re.compile(r"\\begin\{fr\}")
RE_LABEL = re.compile(r"\\label\{([^}]+)\}")
RE_MACRO = re.compile(r"\\([a-zA-Z@]+)")
RE_VERB_ENV = re.compile(
    r"\\begin\{(python|console|shellcmd)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}", re.S
)
RE_ENVCOUNT = re.compile(
    r"\\begin\{(quiz|testexercises|furtherproblems)\}(.*?)\\end\{\1\}", re.S
)
RE_ITEM = re.compile(r"^\s*\\item\b", re.M)
RE_COMMENT = re.compile(r"(?<!\\)%.*$", re.M)

# Numbers inside prose. The Polish edition writes 0,1 where the English writes
# 0.1, so the comma is normalised before comparison; a number that differs by
# more than its separator is a translation defect.
RE_NUMBER = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?")

# Macros whose count is allowed to differ: they belong to prose rather than to
# structure, and a good translation legitimately uses more or fewer of them.
PROSE_MACROS = {
    "emph", "textbf", "textit", "quad", "qquad", "noindent", "par", "medskip",
    "smallskip", "bigskip", "hfill", "vspace", "mbox", "footnote", "-", "\\",
    "textasciitilde", "textasciicircum", "ldots", "dots", "text",
}


def strip_comments(t: str) -> str:
    return RE_COMMENT.sub("", t)


def numbers(t: str) -> list[str]:
    return [n.replace(",", ".") for n in RE_NUMBER.findall(t)]


def macro_counts(t: str) -> Counter:
    c = Counter(RE_MACRO.findall(t))
    for m in PROSE_MACROS:
        c.pop(m, None)
    return c


def non_ascii_in_verbatim(t: str) -> list[str]:
    out = []
    for env, body in ((m.group(1), m.group(2)) for m in RE_VERB_ENV.finditer(t)):
        for ch in body:
            if ord(ch) > 127:
                out.append(f"{env}: U+{ord(ch):04X} {ch!r}")
    return out


def compare(a: Path, b: Path) -> list[str]:
    ta, tb = (strip_comments(p.read_text(encoding="utf8")) for p in (a, b))
    bad: list[str] = []
    name = a.stem

    na, nb = len(RE_FRAME.findall(ta)), len(RE_FRAME.findall(tb))
    if na != nb:
        bad.append(f"{name}: frame count en={na} pl={nb}")

    la, lb = set(RE_LABEL.findall(ta)), set(RE_LABEL.findall(tb))
    if la != lb:
        if la - lb:
            bad.append(f"{name}: labels only in en: {sorted(la - lb)}")
        if lb - la:
            bad.append(f"{name}: labels only in pl: {sorted(lb - la)}")

    ea = {m.group(1): len(RE_ITEM.findall(m.group(2))) for m in RE_ENVCOUNT.finditer(ta)}
    eb = {m.group(1): len(RE_ITEM.findall(m.group(2))) for m in RE_ENVCOUNT.finditer(tb)}
    for env in set(ea) | set(eb):
        if ea.get(env) != eb.get(env):
            bad.append(f"{name}: {env} item count en={ea.get(env)} pl={eb.get(env)}")

    va, vb = numbers(ta), numbers(tb)
    if va != vb:
        # Report the first divergence rather than the whole list; the whole
        # list is unreadable and the first one is usually the cause of the rest.
        for i, (x, y) in enumerate(zip(va, vb)):
            if x != y:
                bad.append(f"{name}: numeric literal #{i + 1} en={x} pl={y}")
                break
        else:
            bad.append(f"{name}: numeric literal count en={len(va)} pl={len(vb)}")

    ma, mb = macro_counts(ta), macro_counts(tb)
    for k in sorted(set(ma) | set(mb)):
        if ma.get(k, 0) != mb.get(k, 0):
            bad.append(f"{name}: \\{k} used {ma.get(k, 0)}x in en, {mb.get(k, 0)}x in pl")

    for p, t in ((a, ta), (b, tb)):
        for issue in non_ascii_in_verbatim(t):
            bad.append(f"{p}: non-ASCII inside a listing -- {issue}")

    return bad


def check_lang_files() -> list[str]:
    rx = re.compile(r"\\(?:newcommand|DeclareMathOperator\*?)\{?\\([A-Za-z]+)")
    sets = {}
    for lang in ("en", "pl"):
        p = ROOT / "lang" / f"{lang}.tex"
        sets[lang] = set(rx.findall(p.read_text(encoding="utf8")))
    only_en = sets["en"] - sets["pl"]
    only_pl = sets["pl"] - sets["en"]
    bad = []
    if only_en:
        bad.append(f"lang: defined only in en: {sorted(only_en)}")
    if only_pl:
        bad.append(f"lang: defined only in pl: {sorted(only_pl)}")
    return bad


def main() -> int:
    if len(sys.argv) == 3:
        bad = compare(Path(sys.argv[1]), Path(sys.argv[2]))
    else:
        bad = check_lang_files()
        en = {p.name for p in (ROOT / "programs" / "en").glob("*.tex")}
        pl = {p.name for p in (ROOT / "programs" / "pl").glob("*.tex")}
        for missing in sorted(en - pl):
            bad.append(f"programs: {missing} exists in en and not in pl")
        for missing in sorted(pl - en):
            bad.append(f"programs: {missing} exists in pl and not in en")
        for name in sorted(en & pl):
            bad += compare(ROOT / "programs" / "en" / name,
                           ROOT / "programs" / "pl" / name)

    for line in bad:
        print(f"  {line}")
    if not bad:
        print("  The two editions are in step.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
