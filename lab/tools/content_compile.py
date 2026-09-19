#!/usr/bin/env python3
"""Compile the book into an ab-ovo content bundle (issue #239 §1).

The application never sees LaTeX (constitution P11). This is where that
promise is kept: the book's own tokeniser reads the two editions, and what
comes out is one `bundle.json` that validates against ab-ove's
`content-schema.v1.json` -- all 47 programs, both languages, the sections,
the frames, the covered answers, the cues, the routes back into the frames,
and the lab checks.

    python3 lab/tools/content_compile.py --tag v0 -o build/content/bundle.json
    python3 lab/tools/content_compile.py --only P01 --stdout
    python3 lab/tools/content_compile.py --macros      # the KaTeX table, measured

IT REFUSES RATHER THAN DEGRADES, which is #239 §1's own wording and the
reason this is a compiler and not a scraper. A macro outside the declared
vocabulary, a `\\val` with no computed value behind it, a cue whose successor
does not open with an answer, two editions whose frames do not pair -- each
stops the build and names the program, the line and the token. Silence is
the failure mode a content pipeline has: a bundle that renders a blank where
a reader expected prose looks finished.

WHAT V1 CANNOT CARRY, and this compiler therefore counts rather than drops
silently. ab-ove's ADR-0014 settles the schema's scope in as many words --
"no maths spans, no figures, no transcripts and no Quiz answers ... Adding
them is a v2 with a `schemaVersion` bump". So `\\mermaidfig` and
`\\transcript` have nowhere to go in a v1 bundle. They are removed from the
body, TALLIED, and printed on every run; `--strict` turns the tally into a
failure. That is the treatment this book already gives the orphan-tail
ledger, for the same reason: a gate nobody can clear teaches the next person
to stop reading the output, and a gap nobody counts is a gap that grows.

MATHS IS NOT LATEX HERE. A `$...$` span survives into the body because KaTeX
is the agreed renderer (#239 §1), but every macro inside it is either one
KaTeX knows or one this file expands -- and the expansion is PER LANGUAGE,
because the notation contract IS the i18n table: `\\tg` sets `tan` for an
English reader and `tg` for a Polish one, and no consumer can be expected to
know that. `--macros` prints the table against what the book actually uses,
so it is a measurement rather than a guess.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tarfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import parity  # noqa: E402  -- the book's own tokeniser, never a second parser

LANGS = ("en", "pl")
SCHEMA_VERSION = 1
TRACK_ID = "math-for-ai-engineers"
TRACK_TITLES = {
    "en": "Mathematics from Zero for the AI Engineer",
    "pl": "Matematyka od zera dla inżyniera AI",
}


class Refusal(Exception):
    """A defect the compiler will not paper over. Carries where to look."""

    def __init__(self, where: str, what: str, hint: str = "") -> None:
        super().__init__(f"{where}: {what}" + (f"\n    {hint}" if hint else ""))
        self.where, self.what, self.hint = where, what, hint


# ----------------------------------------------------------------- values
#
# \val{k} is the book's whole discipline in one macro: every number the
# reader cannot do in their head is computed by code/ and committed. Here it
# has to become a STRING, per language, because siunitx is what localises it
# on the page and there is no siunitx in a browser.

VAL_RE = re.compile(r"\\mfaval(text)?\{([^}]+)\}\{(.*)\}$", re.M)


def load_values() -> dict[str, tuple[str, bool]]:
    """key -> (raw, is_text). Every file, because P01 quotes F03's keys."""
    out: dict[str, tuple[str, bool]] = {}
    for f in sorted((ROOT / "figures" / "values").glob("*.tex")):
        for is_text, key, raw in VAL_RE.findall(f.read_text(encoding="utf8")):
            out[key] = (raw.strip(), bool(is_text))
    return out


NUMERIC_RE = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def localise_number(raw: str, lang: str, math: bool = False) -> str:
    """What siunitx prints, in the one respect that is language-dependent.

    `\\num` gives Polish a decimal comma and both editions a thin space
    between thousands -- the notation contract's own row. A non-numeric body
    is passed through: the book has `\\valtext` for exactly that case and
    siunitx would refuse it.

    THE THIN SPACE IS NOT THE SAME CHARACTER IN BOTH PLACES. In prose it is
    U+202F, the narrow no-break space. In maths it has to be `\\,`, because
    KaTeX in strict mode refuses an unrecognised Unicode character outright
    -- which is how this was found: 364 of the bundle's 21 714 spans failed
    the render test, every one of them a number this function had grouped.
    """
    if not NUMERIC_RE.match(raw):
        return raw
    if "e" in raw or "E" in raw:           # keep an exponent an exponent
        mant, exp = re.split(r"[eE]", raw, maxsplit=1)
        sign = "-" if exp.startswith("-") else ""
        digits = exp.lstrip("+-").lstrip("0") or "0"
        return (f"{localise_number(mant, lang, math)}"
                f"\\times 10^{{{sign}{digits}}}")
    sign, body = ("-", raw[1:]) if raw.startswith("-") else ("", raw)
    whole, _, frac = body.partition(".")
    if len(whole) > 4:                     # siunitx groups from five digits
        thin = "\\," if math else "\u202f"
        head = len(whole) % 3 or 3
        whole = thin.join([whole[:head]]
                          + [whole[i:i + 3] for i in range(head, len(whole), 3)])
    point = "," if lang == "pl" else "."
    return sign + whole + (point + frac if frac else "")


# ----------------------------------------------------------- the vocabulary
#
# Every macro the book uses inside a frame, measured rather than remembered:
# `lab/tools/content_probe.py` counts them and this table answers them. A
# macro absent from every table below is a REFUSAL, which is what makes the
# table a contract rather than a best effort.

DROP = {                       # typesetting with no meaning off the page
    "noindent", "medskip", "smallskip", "bigskip", "small", "normalsize",
    "footnotesize", "linewidth", "textwidth", "sisetup", "centering",
    "index", "label", "vspace", "hspace", "par", "clearpage", "newpage",
    "penalty", "strut", "raggedright", "leavevmode", "protect",
}
LITERAL = {                    # macro -> the character it sets
    "textasciitilde": "~", "textasciicircum": "^", "textbackslash": "\\",
    "S": "§", "P": "¶", "%": "%", "&": "&", "_": "_", "#": "#", "$": "$",
    "{": "{", "}": "}", "ldots": "…", "dots": "…", "textellipsis": "…",
    "quad": " ", "qquad": "  ", ",": "\u202f", ";": " ", ":": " ", " ": " ",
    "nobreakspace": "\u00a0", "~": "\u00a0",
}
PER_LANG = {                   # macro -> {lang: text}. The i18n table itself.
    "dash": {"en": " — ", "pl": " – "},
    "blank": {"en": "\\_\\_\\_\\_", "pl": "\\_\\_\\_\\_"},
}
WRAP = {                       # macro -> (before, after) round its one argument
    "textbf": ("**", "**"), "emph": ("*", "*"), "textit": ("*", "*"),
    "code": ("`", "`"), "texttt": ("`", "`"), "textsc": ("", ""),
    "mbox": ("", ""), "text": ("", ""),
}
QUOTES = {"en": ("\u2018", "\u2019"), "pl": ("\u201e", "\u201d")}

# Book macros used INSIDE maths. KaTeX has no idea what any of these mean, so
# each is expanded here -- per language where the notation contract says the
# two editions set different glyphs (the keyboard test, CLAUDE.md).
MATHS_MACROS: dict[str, dict[str, str]] = {
    # notation contract: read or written, so Polish sets its own form
    "tg": {"en": "\\tan", "pl": "\\operatorname{tg}"},
    "ctg": {"en": "\\cot", "pl": "\\operatorname{ctg}"},
    "arctg": {"en": "\\arctan", "pl": "\\operatorname{arc\\,tg}"},
    "gcdop": {"en": "\\gcd", "pl": "\\operatorname{NWD}"},
    "lcmop": {"en": "\\operatorname{lcm}", "pl": "\\operatorname{NWW}"},
    # the same in both editions, and none of them is KaTeX's
    "Ex": "\\operatorname{E}", "Var": "\\operatorname{Var}",
    "Cov": "\\operatorname{Cov}", "Corr": "\\operatorname{Corr}",
    "Prob": "\\operatorname{P}", "KL": "D_{\\mathrm{KL}}",
    "JS": "D_{\\mathrm{JS}}", "relu": "\\operatorname{ReLU}",
    "softmax": "\\operatorname{softmax}", "logit": "\\operatorname{logit}",
    "logsumexp": "\\operatorname{logsumexp}", "clip": "\\operatorname{clip}",
    "diag": "\\operatorname{diag}", "spanof": {"en": "\\operatorname{span}",
                                               "pl": "\\operatorname{lin}"},
    "argmax": "\\operatorname{arg\\,max}", "argmin": "\\operatorname{arg\\,min}",
    "eps": "\\varepsilon", "T": "^{\\mathsf{T}}", "norm": "\\lVert",
    "N": "\\mathbb{N}", "Z": "\\mathbb{Z}", "Q": "\\mathbb{Q}",
    "R": "\\mathbb{R}", "C": "\\mathbb{C}",
    "mfalogplain": "\\log",
    "blank": "\\underline{\\phantom{0000}}",
}
MATHS_ARG1 = {"vect": "\\mathbf{%s}", "norm": "\\lVert %s\\rVert",
              "logb": "\\log_{%s}"}
MATHS_ARG2 = {"intcc": "[%s,%s]", "intoo": "(%s,%s)",
              "intco": "[%s,%s)", "intoc": "(%s,%s]",
              "KL": "D_{\\mathrm{KL}}\\!\\left(%s\\,\\|\\,%s\\right)",
              "JS": "D_{\\mathrm{JS}}\\!\\left(%s\\,\\|\\,%s\\right)",
              }

# KaTeX's own vocabulary. Anything here passes through untouched; anything in
# neither list is refused. Measured against every maths span in the book.
KATEX_OK = set("""
 Bigl Bigr Delta Longleftrightarrow Longrightarrow Omega Rightarrow Sigma
 Theta Vert alpha approx arcsin arccos arctan bar begin beta big bigl bigr
 binom cap cdot cdots circ colon cos cup delta det dfrac div dots emptyset
 end eta exp frac gamma ge hat in infty int kappa lVert lambda land lceil
 ldots le left leftarrow lfloor lim ln lnot longleftarrow longrightarrow lor
 lvert mathbb mathrm mathsf mathbf max mid min mu nabla ne neq notin omega
 operatorname overline partial phi pi pm prod propto qquad quad rVert rceil
 rfloor rho right rightarrow rvert setminus sigma sim sin sqrt subseteq sum
 tan tanh tau text tfrac theta times to underbrace varepsilon wedge vee
 cosh sinh coth sec csc cot log arg deg dim ker Pr sup inf liminf limsup
 subset supset supseteq subsetneq varnothing bmod pmod mapsto implies iff
 ge le gg ll asymp doteq models vdash top bot lnot land lor oint iint
 equiv simeq cong perp parallel angle triangle forall exists neg oplus
 otimes odot boxed substack atop over choose displaystyle textstyle
 scriptstyle limits nolimits nonumber quad ! , ; : > space
 """.split())

BOX_LABEL = {
    "note": {"en": "Note", "pl": "Uwaga"},
    "warning": {"en": "Warning", "pl": "Ostrzeżenie"},
    "trapbox": {"en": "Trap", "pl": "Pułapka"},
    "aibox": {"en": "Where this shows up in AI", "pl": "Gdzie to widać w AI"},
    "rigourbox": {"en": "What we are not proving", "pl": "Czego nie dowodzimy"},
    "notationbox": {"en": "Notation", "pl": "Notacja"},
    "verifybox": {"en": "Verify", "pl": "Sprawdź"},
    "exercisebox": {"en": "Exercise", "pl": "Ćwiczenie"},
}
MATH_ENVS = {"align", "align*", "gather", "gather*", "equation", "equation*",
             "multline", "multline*", "pmatrix", "bmatrix", "vmatrix",
             "smallmatrix", "psmallmatrix", "cases", "array", "matrix"}
TRANSPARENT = {"center", "flushleft", "flushright", "sloppypar"}

# v1 has no home for these; ADR-0014 names both. Counted, never silent.
V2_MACROS = {"mermaidfig": "figure", "transcript": "transcript"}


def balanced(src: str, i: int) -> tuple[str, int]:
    """The brace group starting at src[i]=='{'; returns (body, index after)."""
    assert src[i] == "{"
    depth, j = 0, i
    while j < len(src):
        if src[j] == "\\":
            j += 2
            continue
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[i + 1:j], j + 1
        j += 1
    raise Refusal("brace", "unbalanced group", src[i:i + 60])


def optional(src: str, i: int) -> tuple[str | None, int]:
    if i < len(src) and src[i] == "[":
        j = src.index("]", i)
        return src[i + 1:j], j + 1
    return None, i


# -------------------------------------------------------------- the maths
#
# A maths span survives into the body as maths, because KaTeX is the agreed
# renderer. What does not survive is a macro KaTeX has never heard of.

MACRO_RE = re.compile(r"\\([a-zA-Z@]+)")


def expand_maths(body: str, lang: str, vals, ctx: str, seen: Counter) -> str:
    out, i = [], 0
    while i < len(body):
        ch = body[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        m = MACRO_RE.match(body, i)
        if not m:                       # \{ \} \\ \| and friends
            out.append(body[i:i + 2])
            i += 2
            continue
        name, j = m.group(1), m.end()
        seen[name] += 1

        if name in ("val", "rawval", "valtext"):
            arg, j = balanced(body, skip_ws(body, j, ctx))
            out.append(resolve_val(arg, name, lang, vals, ctx, math=True))
            i = j
            continue
        if name == "num":
            arg, j = balanced(body, skip_ws(body, j, ctx))
            out.append(localise_number(arg.strip(), lang, math=True))
            i = j
            continue
        if name in MATHS_ARG2:
            a, j = balanced(body, skip_ws(body, j, ctx))
            b, j = balanced(body, skip_ws(body, j, ctx))
            out.append(MATHS_ARG2[name] % (
                expand_maths(a, lang, vals, ctx, seen),
                expand_maths(b, lang, vals, ctx, seen)))
            i = j
            continue
        if name in MATHS_ARG1:
            a, j = balanced(body, skip_ws(body, j, ctx))
            out.append(MATHS_ARG1[name] % expand_maths(a, lang, vals, ctx, seen))
            i = j
            continue
        if name in MATHS_MACROS:
            rep = MATHS_MACROS[name]
            out.append(rep[lang] if isinstance(rep, dict) else rep)
            i = j
            continue
        if name == "code":              # \code inside maths: a name, not a symbol
            arg, j = balanced(body, skip_ws(body, j, ctx))
            out.append("\\texttt{" + arg + "}")
            i = j
            continue
        if name in KATEX_OK or name in MATH_ENVS:
            out.append("\\" + name)
            i = j
            continue
        raise Refusal(ctx, f"\\{name} inside maths is in no table",
                      "Add it to MATHS_MACROS (with a per-language form if the "
                      "notation contract gives one) or to KATEX_OK, having "
                      "checked KaTeX renders it.")
    return "".join(out)


def skip_ws(src: str, i: int, ctx: str = "argument") -> int:
    while i < len(src) and src[i] in " \t\n":
        i += 1
    if i >= len(src) or src[i] != "{":
        raise Refusal(ctx, "expected a braced argument",
                      "..." + src[max(0, i - 60):i + 20].replace("\n", " "))
    return i


def resolve_val(key: str, macro: str, lang: str, vals, ctx: str,
                math: bool = False) -> str:
    key = key.strip()
    if key not in vals:
        raise Refusal(ctx, f"\\{macro}{{{key}}} has no computed value",
                      "Run `make numbers`, or fix the script in code/ that "
                      "should emit this key. A bundle carrying [?key] is a "
                      "page with a hole in it.")
    raw, is_text = vals[key]
    if macro == "rawval" or is_text:
        return raw
    return localise_number(raw, lang, math)


# --------------------------------------------------------------- the prose
#
# LaTeX in, Markdown out. Maths spans are lifted out first and put back
# afterwards, so no prose rule can reach inside one.

MATH_SPAN = re.compile(r"\\\[(.*?)\\\]|\$\$(.*?)\$\$|\$([^$]*)\$", re.S)
ENV_RE = re.compile(r"\\begin\{([A-Za-z*]+)\}")


def convert(src: str, lang: str, vals, ctx: str, seen: Counter,
            gaps: Counter) -> str:
    """The whole vocabulary, applied once. Anything outside it is refused."""
    out: list[str] = []
    i = 0
    while i < len(src):
        ch = src[i]

        if ch == "$" or src.startswith("\\[", i):
            m = MATH_SPAN.match(src, i)
            if not m:
                raise Refusal(ctx, "unterminated maths span", src[i:i + 60])
            inner = next(g for g in m.groups() if g is not None)
            display = m.group(0).startswith(("\\[", "$$"))
            body = expand_maths(inner, lang, vals, ctx, seen).strip()
            out.append(f"\n\n$$\n{body}\n$$\n\n" if display else f"${body}$")
            i = m.end()
            continue

        if src.startswith("\\begin{", i):
            name = ENV_RE.match(src, i).group(1)
            inner, j = read_env(src, i, name, ctx)
            out.append(convert_env(name, inner, lang, vals, ctx, seen, gaps))
            i = j
            continue

        if src.startswith("\\end{", i):
            raise Refusal(ctx, "an \\end with no \\begin", src[i:i + 40])

        if ch == "\\":
            m = MACRO_RE.match(src, i)
            if not m:
                if src.startswith("\\\\", i):
                    # A forced line break, and it may carry a spacing
                    # argument -- \\[2pt] -- which is typesetting and has to
                    # be eaten rather than left on the page as "[2pt]".
                    _, j = optional(src, i + 2)
                    out.append("\n\n")
                    i = j
                    continue
                out.append({"\\%": "%", "\\&": "&", "\\_": "_", "\\#": "#",
                            "\\$": "$", "\\{": "{", "\\}": "}"}
                           .get(src[i:i + 2], src[i + 1:i + 2]))
                i += 2
                continue
            name, j = m.group(1), m.end()
            text, j = apply_macro(name, src, j, lang, vals, ctx, seen, gaps)
            out.append(text)
            i = j
            continue

        if ch == "~":                 # LaTeX's non-breaking space, not a macro
            out.append("\u00a0")
            i += 1
            continue

        out.append(ch)
        i += 1
    return "".join(out)


def apply_macro(name, src, j, lang, vals, ctx, seen, gaps) -> tuple[str, int]:
    seen[name] += 1

    if name in V2_MACROS:                 # ADR-0014: a v2 field.
        _, j = balanced(src, skip_ws(src, j, ctx))
        while j < len(src) and src[j] == "{":
            _, j = balanced(src, j)
        return "", j                      # counted per program, not here

    if name in ("val", "rawval", "valtext"):
        arg, j = balanced(src, skip_ws(src, j, ctx))
        return resolve_val(arg, name, lang, vals, ctx), j
    if name == "num":
        arg, j = balanced(src, skip_ws(src, j, ctx))
        return localise_number(arg.strip(), lang), j

    if name in DROP:
        while j < len(src) and src[j] == "{":
            _, j = balanced(src, j)
        return "", j
    if name in LITERAL:
        return LITERAL[name], j
    if name in PER_LANG:
        # \dash{} and \blank take an empty group by convention
        if j < len(src) and src[j] == "{":
            _, j = balanced(src, j)
        return PER_LANG[name][lang], j
    if name in WRAP:
        arg, j = balanced(src, skip_ws(src, j, ctx))
        pre, post = WRAP[name]
        inner = convert(arg, lang, vals, ctx, seen, gaps).strip()
        return (pre + inner + post) if inner else "", j
    if name == "enquote":
        arg, j = balanced(src, skip_ws(src, j, ctx))
        o, c = QUOTES[lang]
        return o + convert(arg, lang, vals, ctx, seen, gaps) + c, j
    if name in ("ref", "eqref", "pageref"):
        arg, j = balanced(src, skip_ws(src, j, ctx))
        return reference_text(arg.strip(), lang, ctx), j
    if name == "item":
        opt, j = optional(src, j)
        return "\n- " + (f"**{opt}** " if opt else ""), j
    if name in ("toprule", "midrule", "bottomrule", "hline"):
        return "\u0000RULE\u0000", j
    if name == "texorpdfstring":
        shown, j = balanced(src, skip_ws(src, j, ctx))
        _, j = balanced(src, skip_ws(src, j, ctx))
        return convert(shown, lang, vals, ctx, seen, gaps), j
    if name == "result":                  # Appendix C's mark: transparent here
        arg, j = balanced(src, skip_ws(src, j, ctx))
        return convert(arg, lang, vals, ctx, seen, gaps), j
    if name in ("dotline", "yourturn"):
        # The row of dots IS the covered answer box, and the step already
        # says so with `cue`. A second marker in the body would have the
        # application draw two.
        while j < len(src) and src[j] == "{":
            _, j = balanced(src, j)
        return "", j
    if name == "nextframe":
        return "", j                      # lifted before conversion; belt and braces

    raise Refusal(ctx, f"\\{name} is in no table",
                  "Add it to DROP, LITERAL, PER_LANG, WRAP or the handlers "
                  "above -- having decided what it MEANS off the page, which "
                  "is the decision this refusal exists to force.")


def read_env(src: str, i: int, name: str, ctx: str) -> tuple[str, int]:
    """Body of \\begin{name}...\\end{name} from i, nesting-aware."""
    open_re = re.compile(r"\\begin\{" + re.escape(name) + r"\}")
    close_re = re.compile(r"\\end\{" + re.escape(name) + r"\}")
    start = open_re.match(src, i).end()
    depth, j = 1, start
    while j < len(src):
        o, c = open_re.search(src, j), close_re.search(src, j)
        if c is None:
            raise Refusal(ctx, f"\\begin{{{name}}} is never closed")
        if o is not None and o.start() < c.start():
            depth, j = depth + 1, o.end()
            continue
        depth, j = depth - 1, c.end()
        if depth == 0:
            return src[start:c.start()], j
    raise Refusal(ctx, f"\\begin{{{name}}} is never closed")


def convert_env(name, inner, lang, vals, ctx, seen, gaps) -> str:
    if name in MATH_ENVS:
        body = expand_maths(inner, lang, vals, ctx, seen).strip()
        if name not in ("equation", "equation*"):
            body = f"\\begin{{{name}}}{body}\\end{{{name}}}" \
                if name not in ("align", "align*", "gather", "gather*") \
                else f"\\begin{{aligned}}{body}\\end{{aligned}}"
        return f"\n\n$$\n{body}\n$$\n\n"
    if name in TRANSPARENT or name == "ansblock":
        return convert(inner, lang, vals, ctx, seen, gaps)
    if name in BOX_LABEL:
        body = convert(inner, lang, vals, ctx, seen, gaps).strip()
        label = BOX_LABEL[name][lang]
        quoted = "\n".join("> " + ln for ln in tidy(body).split("\n"))
        return f"\n\n> **{label}**\n>\n{quoted}\n\n"
    if name in ("itemize", "enumerate"):
        body = convert(inner, lang, vals, ctx, seen, gaps)
        if name == "enumerate":
            parts, n = body.split("\n- "), 0
            body = parts[0]
            for p in parts[1:]:
                n += 1
                body += f"\n{n}. {p}"
        return "\n" + body.strip("\n") + "\n\n"
    if name == "quote":
        body = tidy(convert(inner, lang, vals, ctx, seen, gaps).strip())
        return "\n\n" + "\n".join("> " + ln for ln in body.split("\n")) + "\n\n"
    if name in ("python", "verbatim", "lstlisting"):
        return "\n\n```python\n" + inner.strip("\n") + "\n```\n\n"
    if name in ("tabular", "tabularx"):
        return render_table(name, inner, lang, vals, ctx, seen, gaps)
    raise Refusal(ctx, f"the {name} environment is in no table",
                  "Decide what it MEANS off the page, then add it to "
                  "convert_env -- or, if schema v1 has no home for it, to "
                  "V2_MACROS so it is counted rather than dropped.")


def split_depth0(src: str, sep: str) -> list[str]:
    """Split on a separator that is OUTSIDE every brace group.

    LaTeX's own rule, and the reason it matters here is a cell like
    `\\textbf{a & b}`: splitting on every & cuts the macro's argument in
    half and the brace never closes.
    """
    out, depth, start, i = [], 0, 0, 0
    while i < len(src):
        if src[i] == "\\" and not src.startswith(sep, i):
            i += 2
            continue
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth = max(0, depth - 1)
        elif depth == 0 and src.startswith(sep, i):
            out.append(src[start:i])
            i += len(sep)
            start = i
            continue
        i += 1
    out.append(src[start:])
    return out


def render_table(env, inner, lang, vals, ctx, seen, gaps) -> str:
    """A tabular becomes a Markdown table. A column spec is presentation.

    Maths is hidden before the row and cell splits and put back after. Both
    of a table's separators occur INSIDE maths -- a pmatrix writes its rows
    with \\\\ and its columns with & -- so splitting on them first cuts a
    matrix in half and leaves an unterminated $. P10's frame 17 has one.
    """
    # tabular takes one braced group (the column spec); tabularx takes two, a
    # width and then the spec. A spec contains braces -- @{}lX@{} -- so it is
    # read with balanced() rather than matched with [^{}]*, which is what let
    # P10's spec leak into the table as a row of its own.
    body = inner.lstrip()
    for _ in range(2 if env == "tabularx" else 1):
        if not body.startswith("{"):
            raise Refusal(ctx, f"{env} with no column spec", body[:60])
        _, k = balanced(body, 0)
        body = body[k:].lstrip()

    held: list[str] = []

    def hold(m):
        held.append(m.group(0))
        return f"\u0000M{len(held) - 1}\u0000"

    def put(s):
        return re.sub(r"\u0000M(\d+)\u0000", lambda m: held[int(m.group(1))], s)

    body = MATH_SPAN.sub(hold, body)
    rows = []
    for raw in split_depth0(body, "\\\\"):
        cells = [put(c) for c in split_depth0(raw, "&")]
        cells = [convert(c, lang, vals, ctx, seen, gaps)
                 .replace("\u0000RULE\u0000", "").strip().replace("\n", " ")
                 for c in cells]
        if not any(cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    head, rest = rows[0], rows[1:]
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join([" --- "] * width) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rest]
    return "\n\n" + "\n".join(out) + "\n\n"


# ---------------------------------------------------------- cross-references
#
# `Program~\ref{prog:P05}` prints "Program 5", because \mainnumbering
# restarts the counter at Part II. Resolving it here is the whole reason the
# application never needs an .aux file.

_LABELS: dict[str, str] = {}


def build_label_table(manifest) -> None:
    for p in manifest:
        _LABELS[f"prog:{p['key']}"] = p["id"][1:] if p["id"].startswith("P") \
            else p["id"]
    for lang in LANGS:
        for p in sorted((ROOT / "programs" / lang).glob("*.tex")):
            src = parity.COMMENT_RE.sub("", p.read_text(encoding="utf8"))
            for lbl in re.findall(r"\\label\{(sec:[^}]+)\}", src):
                _LABELS.setdefault(lbl, lbl.split(":", 1)[1])
        # An appendix section prints as a LETTER and an ordinal -- B.1, B.2 --
        # and the letter is in the filename while the ordinal is the order the
        # \section commands come in. Both are in the source, so neither needs
        # an .aux file, which is the whole point of resolving references here.
        for p in sorted((ROOT / "appendices" / lang).glob("app?-*.tex")):
            letter = p.name[3]
            src = parity.COMMENT_RE.sub("", p.read_text(encoding="utf8"))
            n = 0
            for m in re.finditer(r"\\(section)\*?\{|\\label\{(sec:[^}]+)\}", src):
                if m.group(1):
                    if "*" not in m.group(0):
                        n += 1
                elif m.group(2) and n:
                    _LABELS.setdefault(m.group(2), f"{letter}.{n}")
            _LABELS.setdefault(f"app:{letter}", letter)


def reference_text(label: str, lang: str, ctx: str) -> str:
    if label in _LABELS:
        return _LABELS[label]
    raise Refusal(ctx, f"\\ref{{{label}}} names no label this compiler knows",
                  "A reference the bundle cannot resolve would print as a "
                  "hole. Add the label's family to build_label_table.")


def tidy(text: str) -> str:
    text = text.replace("\u0000RULE\u0000", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    return text.strip()


# ---------------------------------------------------------------- one program

# A section title is read with balanced(), never with a nesting-limited
# regex. P07's "\\section{An \\texorpdfstring{\\code{einsum}}{einsum} string
# ...}" nests two deep, and a regex allowing one level dropped the section
# silently -- the bundle came back 274 against the 275 lab/tools/content_probe.py
# had already measured, which is the only reason it was caught. Make the
# wrong match impossible rather than detectable.
RE_SECTION_OPEN = re.compile(r"\\section\{")
RE_LABEL_AFTER = re.compile(r"\s*\\label\{(sec:[^}]+)\}")


def find_sections(src: str, ctx: str) -> list[tuple[int, str, str | None]]:
    out = []
    for m in RE_SECTION_OPEN.finditer(src):
        title, j = balanced(src, m.end() - 1)
        lm = RE_LABEL_AFTER.match(src, j)
        out.append((m.start(), title, lm.group(1) if lm else None))
    return out

RE_FRAME = re.compile(r"\\begin\{fr\}(.*?)\\end\{fr\}", re.S)
RE_RANGE = re.compile(r"^\s*(\d+)\s*(?:-{2,}|–|—)?\s*(\d*)\s*$")


def split_answer(body: str, ctx: str) -> tuple[str | None, str]:
    """`\\ans{}` or an ansblock opening a frame is the PREVIOUS frame's answer.

    Reproducing the book's own mechanic rather than inventing a parallel one
    is what makes ab-ove's hardest requirement structural: deliver a step at
    a time and the answer has not been sent yet (ADR-0014).
    """
    head = body.lstrip()
    while head.startswith("\\label{"):                 # marks a position, sets nothing
        _, k = balanced(head, head.index("{"))
        head = head[k:].lstrip()
    if head.startswith("\\ans"):
        m = MACRO_RE.match(head)
        if m.group(1) == "ans":
            arg, k = balanced(head, skip_ws(head, m.end(), ctx))
            return arg, head[k:]
    if head.startswith("\\begin{ansblock}"):
        inner, k = read_env(head, 0, "ansblock", ctx)
        return inner, head[k:]
    return None, body


def split_worked_answer(answer: str, ctx: str) -> tuple[str, str]:
    """A frame whose WHOLE content is its answer, split at a real boundary.

    Five frames per edition are like this -- the same five in both, which is
    how you know the shape is deliberate rather than a slip. Schema v1 has no
    way to say it: a step requires a non-empty `body`, and a step that is
    only an answer has none. It is one of the places ADR-0014 says v1 "will
    be wrong somewhere", and it is reported to ab-ove as a v1 finding rather
    than worked around silently.

    What ships meanwhile invents nothing and duplicates nothing. The book
    itself distinguishes `\ans{}`, a short covered box, from `ansblock`, a
    WORKED answer -- so the first paragraph is the box and the working is the
    body. Where the working is a list instead of paragraphs, the first item
    is the box and the rest the body, which is what sliding a hand down a
    covered answer does anyway. Neither boundary is invented: both are in the
    source.
    """
    paras = [q for q in re.split(r"\n[ \t]*\n", answer.strip()) if q.strip()]
    if len(paras) > 1:
        return paras[0], "\n\n".join(paras[1:])
    for env in ("itemize", "enumerate"):
        if re.match(r"\s*\\begin\{" + env + r"\}", answer):
            inner, _ = read_env(answer.strip(), 0, env, ctx)
            items = [x for x in re.split(r"\\item\b", inner) if x.strip()]
            if len(items) > 1:
                head = f"\\begin{{{env}}}\\item {items[0]}\\end{{{env}}}"
                tail = f"\\begin{{{env}}}" + \
                    "".join(f"\\item {x}" for x in items[1:]) + f"\\end{{{env}}}"
                return head, tail
    raise Refusal(ctx, "the frame is only an answer, and v1 requires a body",
                  "No paragraph break and no list to split at. Schema v1 "
                  "cannot carry an answer-only step; report it to ab-ove "
                  "rather than inventing prose for the body.")


def compile_program(key: str, lang: str, vals, seen, gaps) -> dict:
    path = next((ROOT / "programs" / lang).glob(f"{key}-*.tex"))
    ctx0 = f"{lang}/{path.name}"
    src = parity.COMMENT_RE.sub("", path.read_text(encoding="utf8"))

    # Sections are HEADINGS (ADR-0014): {id, titles, firstStep}. The id comes
    # from the LaTeX label, which is language-independent by C3, so the two
    # editions pair for free rather than by slugging two different titles.
    for macro, kind in V2_MACROS.items():
        gaps[kind] += len(re.findall(r"\\" + macro + r"\{", src))

    marks = find_sections(src, ctx0)
    frames = list(RE_FRAME.finditer(src))

    steps, sections, pending = [], [], list(marks)
    for n, fm in enumerate(frames, start=1):
        while pending and pending[0][0] < fm.start():
            pos, title, label = pending.pop(0)
            if label is None:
                raise Refusal(ctx0, f"\\section{{{title[:40]}}} carries no \\label",
                              "The section id is the label, because a label is "
                              "identical in both editions and a title is not.")
            sections.append({"id": label.split(":", 1)[1],
                             "title": tidy(convert(title, lang, vals, ctx0, seen, gaps)),
                             "firstStep": n})
        ctx = f"{ctx0} frame {n}"
        raw_answer, rest = split_answer(fm.group(1), ctx)
        cue = "\\nextframe" in rest
        rest = rest.replace("\\nextframe", " ")
        if raw_answer is not None and not rest.strip():
            raw_answer, rest = split_worked_answer(raw_answer, ctx)
            gaps["answer-only step"] += 1
        step = {"n": n, "kind": "frame",
                "body": tidy(convert(rest, lang, vals, ctx, seen, gaps))}
        if sections:
            step["section"] = sections[-1]["id"]
        if raw_answer is not None:
            step["answer"] = tidy(convert(raw_answer, lang, vals, ctx, seen, gaps))
        if cue:
            step["cue"] = True
        if not step["body"]:
            raise Refusal(ctx, "frame has no body after conversion",
                          "A step with an empty body renders as a blank page.")
        steps.append(step)

    return {"titles": {}, "sections": sections, "steps": steps,
            "routes": collect_routes(src, lang, vals, ctx0, seen, gaps, len(steps))}


def parse_range(payload: str, ctx: str, last: int) -> tuple[int, int]:
    m = RE_RANGE.match(payload.strip())
    if not m:
        raise Refusal(ctx, f"frame range {payload!r} is not a range")
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    if not (1 <= a <= last and 1 <= b <= last):
        raise Refusal(ctx, f"route {a}--{b} names a frame outside 1..{last}",
                      "This is the 91--93-of-48 defect the book wrote "
                      "check_structure.py --frames for; it must not reach a bundle.")
    return a, b


def collect_routes(src, lang, vals, ctx, seen, gaps, last) -> list[dict]:
    routes = []
    for name, kind in (("outcome", "outcome"), ("sumitem", "summary")):
        for m in re.finditer(r"\\" + name + r"\{", src):
            payload, j = balanced(src, m.end() - 1)
            text, _ = balanced(src, j)
            a, b = parse_range(payload, ctx, last)
            routes.append({"kind": kind, "from": a, "to": b,
                           "labels": tidy(convert(text, lang, vals, ctx, seen, gaps))})
    for m in re.finditer(r"\\teachesat(one)?\{", src):
        payload, _ = balanced(src, m.end() - 1)
        a, b = parse_range(payload, ctx, last)
        routes.append({"kind": "quiz", "from": a, "to": b})
    return routes


# ----------------------------------------------------------------- the labs

RE_EXERCISE = re.compile(r"^# --- exercise (\d+): ([a-z0-9][a-z0-9_-]*) -*$", re.M)
RE_TEST = re.compile(r"^def (test_(\d+)_[a-z0-9_]*)\(", re.M)
RE_FRAMES_IN_DOC = re.compile(r"frames?\s+(\d+)(?:\s*(?:-{2,}|–|-)\s*(\d+))?")


def load_labs() -> tuple[list[dict], dict[str, list[tuple[str, int]]]]:
    """Labs, and where each exercise's checks say the reader should be.

    The exercise id is the first check's own name and the frames are its own
    docstring: both are already written down, so neither is invented here.
    """
    labs, anchors = [], {}
    for tf in sorted((ROOT / "lab" / "tests").glob("test_*.py")):
        key = tf.stem.replace("test_", "").upper()
        text = tf.read_text(encoding="utf8")
        runtime = "numpy" if re.search(r"^\s*import numpy", text, re.M) else "stdlib"
        ids = dict(RE_EXERCISE.findall(text))
        if not ids:
            raise Refusal(str(tf.relative_to(ROOT)),
                          "no `# --- exercise N: id ---` markers",
                          "The exercise id is a name the reader types at "
                          "`lab/check.py -k`, so the lab declares it. Deriving "
                          "it from a test name gave `two` for `two_orders`.")
        order, tops = list(ids.values()), {}
        for fn, group in RE_TEST.findall(text):
            if group not in ids:
                raise Refusal(str(tf.relative_to(ROOT)),
                              f"{fn} is in exercise {group}, which has no marker")
            doc = text.split(f"def {fn}(", 1)[1].split('"""')
            hit = RE_FRAMES_IN_DOC.search(doc[1]) if len(doc) > 1 else None
            if hit:
                top = int(hit.group(2) or hit.group(1))
                tops[ids[group]] = max(tops.get(ids[group], 0), top)
        # One check per exercise, at the last frame any of its checks names:
        # that is where the reader has read enough to run it.
        anchors[key] = sorted(tops.items(), key=lambda kv: kv[1])
        labs.append({"id": key, "runtime": runtime, "exercises": order})
    return labs, anchors


# --------------------------------------------------------------- the bundle

def merge(key: str, per_lang: dict[str, dict], titles: dict[str, str],
          anchors) -> dict:
    """One unit out of two editions. They must pair, or the build stops.

    C4 already compares the two editions' ordered structural signatures, so
    a divergence here means something changed since parity last ran -- and a
    bundle whose Polish step 12 is not its English step 12 is two books.
    """
    en, pl = per_lang["en"], per_lang["pl"]
    if len(en["steps"]) != len(pl["steps"]):
        raise Refusal(key, f"{len(en['steps'])} frames in en, "
                            f"{len(pl['steps'])} in pl", "Run tools/parity.py.")
    if [s["id"] for s in en["sections"]] != [s["id"] for s in pl["sections"]]:
        raise Refusal(key, "the two editions declare different section labels")
    if len(en["routes"]) != len(pl["routes"]):
        raise Refusal(key, "the two editions declare different route counts")

    check_at = {top: ex for ex, top in anchors.get(key, [])}
    steps = []
    for a, b in zip(en["steps"], pl["steps"]):
        if (a["n"], a.get("section"), a.get("cue")) != \
           (b["n"], b.get("section"), b.get("cue")):
            raise Refusal(f"{key} step {a['n']}",
                          "the two editions disagree about section or cue")
        if ("answer" in a) != ("answer" in b):
            raise Refusal(f"{key} step {a['n']}",
                          "one edition opens with an answer and the other does not",
                          "This is parity's C16 seen from the bundle's side.")
        step = {"n": a["n"], "kind": "frame",
                "body": {"en": a["body"], "pl": b["body"]}}
        if "section" in a:
            step["section"] = a["section"]
        if "answer" in a:
            step["answer"] = {"en": a["answer"], "pl": b["answer"]}
        if a.get("cue"):
            step["cue"] = True
        if a["n"] in check_at:
            step["check"] = {"lab": key, "exercise": check_at[a["n"]]}
        steps.append(step)

    unit = {"id": key, "titles": titles,
            "sections": [{"id": s["id"],
                          "titles": {"en": s["title"], "pl": t["title"]},
                          "firstStep": s["firstStep"]}
                         for s, t in zip(en["sections"], pl["sections"])],
            "steps": steps}
    routes = []
    for ra, rb in zip(en["routes"], pl["routes"]):
        r = {"kind": ra["kind"], "from": ra["from"], "to": ra["to"]}
        if "labels" in ra:
            r["labels"] = {"en": ra["labels"], "pl": rb.get("labels", ra["labels"])}
        routes.append(r)
    if routes:
        unit["routes"] = routes
    return unit


def build(tag: str, only: list[str] | None, seen, gaps,
          survey: list[tuple[str, str]] | None = None) -> dict:
    manifest = json.loads((ROOT / "tools" / "programs.json").read_text("utf8"))["programs"]
    build_label_table(manifest)
    vals = load_values()
    labs, anchors = load_labs()
    wanted = [p for p in manifest if not only or p["key"] in only]
    units = []
    for p in wanted:
        try:
            per = {lang: compile_program(p["key"], lang, vals, seen, gaps)
                   for lang in LANGS}
            units.append(merge(p["key"], per,
                               {"en": p["en"], "pl": p["pl"]}, anchors))
        except Refusal as e:
            # --survey turns fifty round-trips into one reading. It is a
            # measurement of how wide the vocabulary still is not, and it is
            # never a way to ship: a survey run emits no bundle.
            if survey is None:
                raise
            survey.append((e.where, e.what))
    have = {u["id"] for u in units}
    bundle = {
        "schemaVersion": SCHEMA_VERSION,
        "tag": tag,
        "track": {"id": TRACK_ID, "titles": dict(TRACK_TITLES),
                  "languages": list(LANGS)},
        "units": units,
    }
    labs = [lb for lb in labs if lb["id"] in have]
    if labs:
        bundle["labs"] = labs
    return bundle


# ------------------------------------------------------------- the validator
#
# ab-ove owns the schema and validates on the way in; refusing here as well
# is the point of #239 §1's "the compiler REFUSES rather than degrades" --
# a bundle discovered to be wrong by the far end is one attached to a release.

IMPLEMENTED = {"$schema", "$id", "title", "$comment", "$defs", "$ref", "type",
               "required", "additionalProperties", "properties", "items",
               "const", "enum", "pattern", "minLength", "minItems",
               "minProperties", "uniqueItems", "minimum"}


def unimplemented_keywords(node, out: set[str]) -> set[str]:
    """A validator that silently skips a keyword is one that passed nothing."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "properties" or k == "$defs":
                for sub in v.values():
                    unimplemented_keywords(sub, out)
                continue
            if k not in IMPLEMENTED:
                out.add(k)
            unimplemented_keywords(v, out)
    elif isinstance(node, list):
        for v in node:
            unimplemented_keywords(v, out)
    return out


def check_shape(node, schema, root, where, errs: list[str]) -> None:
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].lstrip("#/").split("/"):
            target = target[part]
        return check_shape(node, target, root, where, errs)
    t = schema.get("type")
    if t == "object" and not isinstance(node, dict):
        return errs.append(f"{where}: expected an object")
    if t == "array" and not isinstance(node, list):
        return errs.append(f"{where}: expected an array")
    if t == "string" and not isinstance(node, str):
        return errs.append(f"{where}: expected a string")
    if t == "integer" and not isinstance(node, int):
        return errs.append(f"{where}: expected an integer")
    if t == "boolean" and not isinstance(node, bool):
        return errs.append(f"{where}: expected a boolean")
    if "const" in schema and node != schema["const"]:
        errs.append(f"{where}: must be {schema['const']!r}")
    if "enum" in schema and node not in schema["enum"]:
        errs.append(f"{where}: {node!r} is not one of {schema['enum']}")
    if isinstance(node, str):
        if "pattern" in schema and not re.search(schema["pattern"], node):
            errs.append(f"{where}: {node!r} does not match {schema['pattern']}")
        if len(node) < schema.get("minLength", 0):
            errs.append(f"{where}: shorter than minLength")
    if isinstance(node, int) and not isinstance(node, bool):
        if "minimum" in schema and node < schema["minimum"]:
            errs.append(f"{where}: below minimum")
    if isinstance(node, list):
        if len(node) < schema.get("minItems", 0):
            errs.append(f"{where}: fewer than minItems")
        if schema.get("uniqueItems") and len(node) != len({json.dumps(x, sort_keys=True)
                                                           for x in node}):
            errs.append(f"{where}: items are not unique")
        if "items" in schema:
            for k, v in enumerate(node):
                check_shape(v, schema["items"], root, f"{where}/{k}", errs)
    if isinstance(node, dict):
        for req in schema.get("required", []):
            if req not in node:
                errs.append(f"{where}: missing required {req!r}")
        if len(node) < schema.get("minProperties", 0):
            errs.append(f"{where}: fewer than minProperties")
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties")
        for k, v in node.items():
            if k in props:
                check_shape(v, props[k], root, f"{where}/{k}", errs)
            elif extra is False:
                errs.append(f"{where}: additional property {k!r}")
            elif isinstance(extra, dict):
                check_shape(v, extra, root, f"{where}/{k}", errs)


def check_structure(bundle) -> list[str]:
    """The rules JSON Schema cannot state. ADR-0014 names all of them."""
    errs, langs = [], bundle["track"]["languages"]

    def texts(node, where):
        if not isinstance(node, dict):
            return
        for lg in langs:
            if lg not in node or not str(node[lg]).strip():
                errs.append(f"{where}: no non-empty {lg!r}")

    texts(bundle["track"]["titles"], "/track/titles")
    lab_ex = {lb["id"]: set(lb["exercises"]) for lb in bundle.get("labs", [])}
    if len(lab_ex) != len(bundle.get("labs", [])):
        errs.append("/labs: duplicate lab ids")
    seen_units = set()
    for ui, unit in enumerate(bundle["units"]):
        u = f"/units/{ui}"
        if unit["id"] in seen_units:
            errs.append(f"{u}: duplicate unit id {unit['id']!r}")
        seen_units.add(unit["id"])
        texts(unit["titles"], f"{u}/titles")
        last = len(unit["steps"])
        sec_ids, prev = set(), 0
        for si, sec in enumerate(unit.get("sections", [])):
            s = f"{u}/sections/{si}"
            texts(sec["titles"], f"{s}/titles")
            if sec["id"] in sec_ids:
                errs.append(f"{s}: duplicate section id {sec['id']!r}")
            sec_ids.add(sec["id"])
            if sec["firstStep"] > last:
                errs.append(f"{s}: firstStep {sec['firstStep']} past step {last}")
            if si and sec["firstStep"] <= prev:
                errs.append(f"{s}: sections must ascend strictly")
            prev = sec["firstStep"]
        for si, step in enumerate(unit["steps"]):
            p = f"{u}/steps/{si}"
            if step["n"] != si + 1:
                errs.append(f"{p}: step n is {step['n']}, expected {si + 1}")
            texts(step["body"], f"{p}/body")
            if "answer" in step:
                texts(step["answer"], f"{p}/answer")
            if "titles" in step:
                texts(step["titles"], f"{p}/titles")
            if "section" in step and step["section"] not in sec_ids:
                errs.append(f"{p}: section {step['section']!r} is not declared")
            nxt = unit["steps"][si + 1] if si + 1 < last else None
            answers_next = bool(nxt and "answer" in nxt)
            if step.get("cue") is True and not answers_next:
                errs.append(f"{p}: says the next step answers it, and "
                            + ("it is the last step" if nxt is None
                               else f"step {nxt['n']} carries no answer"))
            if step.get("cue") is not True and answers_next:
                errs.append(f"{p}: step {nxt['n']} opens with an answer and "
                            "nothing here tells the reader to expect it")
            if "check" in step:
                lab = step["check"]["lab"]
                if lab not in lab_ex:
                    errs.append(f"{p}/check: no lab {lab!r} in the bundle")
                elif step["check"]["exercise"] not in lab_ex[lab]:
                    errs.append(f"{p}/check: lab {lab!r} has no exercise "
                                f"{step['check']['exercise']!r}")
        for ri, route in enumerate(unit.get("routes", [])):
            r = f"{u}/routes/{ri}"
            if "labels" in route:
                texts(route["labels"], f"{r}/labels")
            if route["to"] < route["from"]:
                errs.append(f"{r}: runs backwards")
            if route["from"] > last or route["to"] > last:
                errs.append(f"{r}: names a step past {last}")
    return errs


# -------------------------------------------------------------------- packing
#
# #239 §1: "The bundle carries lab/exercises, lab/solutions, lab/tests (with
# labkit.py), lab/check.py and the figures/values files the checks read, so
# the browser runner needs nothing from the application repository."

PACK = ("lab/exercises", "lab/solutions", "lab/tests", "lab/check.py",
        "lab/README.md", "figures/values")


def pack(bundle: dict, out: Path) -> int:
    """One tar: the content, and everything the lab needs to run it.

    Reproducible rather than assembled in YAML -- a release artefact built
    by steps that exist only inside a workflow is one nobody can rebuild
    when it is wrong.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(bundle, indent=1, ensure_ascii=False).encode("utf8")
    with tarfile.open(out, "w") as tar:
        info = tarfile.TarInfo("bundle.json")
        info.size, info.mtime, info.mode = len(payload), 0, 0o644
        tar.addfile(info, io.BytesIO(payload))
        for rel in PACK:
            src = ROOT / rel
            if not src.exists():
                raise Refusal(rel, "is named in the bundle and is not there")
            for f in sorted([src] if src.is_file() else src.rglob("*")):
                if f.is_dir() or "__pycache__" in f.parts:
                    continue
                info = tar.gettarinfo(f, arcname=str(f.relative_to(ROOT)))
                info.mtime, info.uid, info.gid = 0, 0, 0
                info.uname = info.gname = ""
                with f.open("rb") as fh:
                    tar.addfile(info, fh)
    return out.stat().st_size


# ------------------------------------------------------------------- the CLI

SCHEMA = ROOT / "lab" / "content" / "content-schema.v1.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tag", default="dev", help="the bundle's tag (#239 §6)")
    ap.add_argument("-o", "--out", type=Path, help="where to write bundle.json")
    ap.add_argument("--stdout", action="store_true", help="print it instead")
    ap.add_argument("--only", metavar="KEY", action="append",
                    help="one program, e.g. P01 (repeatable)")
    ap.add_argument("--schema", type=Path, default=SCHEMA)
    ap.add_argument("--pack", type=Path, metavar="TAR",
                    help="also write content-<tag>.tar: the bundle plus "
                         "everything lab/check.py needs to run offline")
    ap.add_argument("--macros", action="store_true",
                    help="the macro table, measured against what the book uses")
    ap.add_argument("--cross-check", action="store_true",
                    help="require lab/tools/content_probe.py, written "
                         "separately and reading the same source, to agree")
    ap.add_argument("--survey", action="store_true",
                    help="collect every refusal instead of stopping at the "
                         "first; emits no bundle")
    ap.add_argument("--strict", action="store_true",
                    help="fail on anything schema v1 cannot carry")
    a = ap.parse_args()

    seen, gaps = Counter(), Counter()
    survey: list[tuple[str, str]] | None = [] if a.survey else None
    try:
        bundle = build(a.tag, a.only, seen, gaps, survey)
    except Refusal as e:
        print(f"REFUSED  {e}", file=sys.stderr)
        return 1
    if survey is not None:
        kinds = Counter(what for _, what in survey)
        print(f"{len(survey)} programs refused, {len(kinds)} distinct reasons:")
        for what, n in kinds.most_common():
            first = next(w for w, x in survey if x == what)
            print(f"  {n:>3}  {what}\n       first at {first}")
        return 1

    schema = json.loads(a.schema.read_text("utf8"))
    missing = unimplemented_keywords(schema, set())
    if missing:
        print("REFUSED  the schema uses keywords this validator ignores: "
              + ", ".join(sorted(missing))
              + "\n    A validator that skips a constraint is indistinguishable "
                "from one that checked it (ADR-0014).", file=sys.stderr)
        return 1

    errs: list[str] = []
    check_shape(bundle, schema, schema, "", errs)
    errs += check_structure(bundle)
    if errs:
        print(f"REFUSED  the bundle does not satisfy content-schema v1 "
              f"({len(errs)} problems):", file=sys.stderr)
        for e in errs[:40]:
            print("    " + e, file=sys.stderr)
        if len(errs) > 40:
            print(f"    ... and {len(errs) - 40} more", file=sys.stderr)
        return 1

    if a.macros:
        book = {k: v for k, v in seen.items()
                if k in MATHS_MACROS or k in MATHS_ARG1 or k in MATHS_ARG2}
        print(f"{len(book)} book macros expanded at compile time, "
              f"{sum(book.values())} times:")
        for k, v in sorted(book.items(), key=lambda kv: -kv[1]):
            rep = MATHS_MACROS.get(k) or MATHS_ARG1.get(k) or MATHS_ARG2.get(k)
            if isinstance(rep, dict):
                rep = " / ".join(f"{lg}: {rep[lg]}" for lg in LANGS)
            print(f"  {v:>6}  \\{k:<14} {rep}")

    text = json.dumps(bundle, indent=1, ensure_ascii=False, sort_keys=False)
    if a.stdout:
        print(text)
    elif a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text + "\n", encoding="utf8")

    if a.cross_check and not a.only:
        import content_probe                      # noqa: E402 -- same directory
        files = sorted((ROOT / "programs" / "en").glob("*.tex"))
        probed = [content_probe.probe(f) for f in files]
        want = (len(probed), sum(len(x["sections"]) for x in probed),
                sum(x["frames"] for x in probed),
                sum(x["answer_openers"] for x in probed),
                sum(x["cues"] for x in probed))
        got = (len(bundle["units"]),
               sum(len(u.get("sections", [])) for u in bundle["units"]),
               sum(len(u["steps"]) for u in bundle["units"]),
               sum(1 for u in bundle["units"] for s in u["steps"] if "answer" in s),
               sum(1 for u in bundle["units"] for s in u["steps"] if s.get("cue")))
        names = ("programs", "sections", "frames", "answers", "cues")
        print("  ".join(f"{n}={g}" for n, g in zip(names, got)), file=sys.stderr)
        if want != got:
            # One of the two is wrong and neither knows which. This caught a
            # \section whose title nested two braces deep: the compiler's
            # regex allowed one level and dropped it, and the bundle came
            # back 274 against the probe's 275.
            print("REFUSED  the compiler and the probe disagree:", file=sys.stderr)
            for n, w, g in zip(names, want, got):
                if w != g:
                    print(f"    {n}: probe {w}, bundle {g}", file=sys.stderr)
            return 1

    if a.pack:
        size = pack(bundle, a.pack)
        print(f"packed {a.pack} ({size / 1024:.0f} KiB)", file=sys.stderr)

    units = bundle["units"]
    steps = sum(len(u["steps"]) for u in units)
    answers = sum(1 for u in units for s in u["steps"] if "answer" in s)
    cues = sum(1 for u in units for s in u["steps"] if s.get("cue"))
    print(f"content-schema v{SCHEMA_VERSION}, tag {bundle['tag']!r}: "
          f"{len(units)} units, {sum(len(u.get('sections', [])) for u in units)} "
          f"sections, {steps} steps, {answers} answers, {cues} cues, "
          f"{sum(len(u.get('routes', [])) for u in units)} routes, "
          f"{len(bundle.get('labs', []))} labs, "
          f"{len(text) / 1024:.0f} KiB", file=sys.stderr)
    if gaps:
        # Reported on every run and never silently dropped, which is how this
        # book treats the orphan-tail ledger. --strict makes it fatal.
        print("NOT IN v1 (ADR-0014 names each as a v2 field): "
              + ", ".join(f"{v} {k}{'s' if v != 1 else ''}"
                          for k, v in sorted(gaps.items())), file=sys.stderr)
        if a.strict:
            print("REFUSED  --strict, and the bundle drops content.",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
