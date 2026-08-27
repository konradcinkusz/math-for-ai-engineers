#!/usr/bin/env python3
"""Program F2 --- The language of algebra.

Every number Program F2 prints that the reader cannot do in their head is
computed here and written to figures/values/f02.tex, which the book \\input{}s.

F2 leans on the standing exception harder than F1 did, and deliberately: almost
all of this program's arithmetic is the thing being taught, so it stays inline
as digits in the prose. None of the following is emitted, and none of it should
be --- putting it behind \\val{} would be theatre:

    2 + 3 * 4^2 = 50;  -3^2 = -9 against (-3)^2 = 9;
    (3+4)^2 = 49 against 3^2 + 4^2 = 25;  8/2 = 4 against 6;
    (7-3)/2 + 1 = 3;  floor(2.5) + 1 = 3;  3.5 and 4, the two wrong
    convolution answers;  every expansion, factorisation and solved equation;
    the chained sizes 30 -> 14.5 -> 6.75 -> 2.875, which is the reader's own
    no-floor arithmetic done a step at a time.

What is emitted is what the reader would have to reach for a calculator to
check: the two readings of a printed layer-norm line, the squared error opened
out, a rearranged formula solved, and the convolution stack's arithmetic.

Run:  python3 code/f02_algebra.py      (or: make numbers)
"""
from __future__ import annotations

import math
from pathlib import Path

VALUES: dict[str, tuple[str, bool]] = {}


def emit(key: str, value, digits: int | None = None) -> None:
    """Record one value under the name the book will reference it by.

    Also decides here whether the value is a number, because this end knows for
    free and the LaTeX end does not. \\val passes its body to siunitx, which
    raises a fatal error on anything that is not a number; the book's \\val
    refuses a value emitted as text and names \\valtext instead.
    """
    if isinstance(value, float) and digits is not None:
        body = f"{value:.{digits}f}"
    elif isinstance(value, float):
        body = repr(value)
    else:
        body = str(value)
    try:
        float(body.replace("e", "E"))
        numeric = True
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


def sci(value: float, digits: int = 0) -> str:
    """Scientific notation with the exponent written the way siunitx reads it.

    Python gives `1e-06`; siunitx sets that with a leading zero in the exponent,
    which reads as a typo on the page. The mantissa's precision is an argument
    because it is a precision decision like any other, not a formatting detail.
    """
    mantissa, exponent = f"{value:.{digits}e}".split("e")
    return f"{mantissa}e{int(exponent)}"


# --------------------------------------------------------------------------
# Layer normalisation, (x - mu) / sqrt(sigma^2 + eps), against the misreading
# that puts the epsilon outside the root. This is the program's demonstration
# that a printed root sign is an invisible bracket.
#
# The variance is small on purpose. With a healthy variance the two readings
# agree to five decimal places and the frame would prove nothing; a
# near-constant row is exactly the case the epsilon exists for, and it is where
# the misreading stops being cosmetic. Say so in the frame rather than picking
# a flattering variance and letting the reader assume it is typical.
# --------------------------------------------------------------------------
LN_X = 0.5
LN_MU = 0.2
LN_VAR = 1e-6                          # a near-constant feature row
LN_EPS = 1e-5                          # the usual value, unchanged

emit("f02.lnorm.x", LN_X, 1)
emit("f02.lnorm.mu", LN_MU, 1)
emit("f02.lnorm.var", sci(LN_VAR))
emit("f02.lnorm.eps", sci(LN_EPS))

ln_inside = (LN_X - LN_MU) / math.sqrt(LN_VAR + LN_EPS)      # as printed
ln_outside = (LN_X - LN_MU) / (math.sqrt(LN_VAR) + LN_EPS)   # as misread
emit("f02.ln.eps.inside", ln_inside, 2)
emit("f02.ln.eps.outside", ln_outside, 2)
# Stated the way F1 insists a ratio is stated: N per cent ABOVE the printed
# value, naming both quantities. The reciprocal reading is also true, is a
# different number, and is not used -- so it is not emitted.
emit("f02.ln.eps.diff.pct", (ln_outside / ln_inside - 1) * 100, 1)

# --------------------------------------------------------------------------
# The squared error opened out: (y - yhat)^2 = y^2 - 2*y*yhat + yhat^2. The
# trap's own algebra turned into the payoff, so the three quantities are
# emitted at ONE precision each and side by side, because the frame prints them
# side by side and a reader comparing 6.25 with 20.5 is entitled to think one
# of them was rounded for effect.
#
# Note that wrong = correct + cross exactly. That is the arithmetic closing,
# not a fourth quantity, and it is not emitted a second time.
# --------------------------------------------------------------------------
ERR_Y = 4.2
ERR_YHAT = 1.7
emit("f02.err.y", ERR_Y, 1)
emit("f02.err.yhat", ERR_YHAT, 1)
emit("f02.sq.correct", (ERR_Y - ERR_YHAT) ** 2, 2)
emit("f02.sq.wrong", ERR_Y**2 + ERR_YHAT**2, 2)      # the trap's answer
emit("f02.sq.cross", 2 * ERR_Y * ERR_YHAT, 2)        # the term it discards

# --------------------------------------------------------------------------
# The memory formula rearranged: bytes = params * bytes-per-parameter, solved
# for params. F1 computed the memory from the parameters; F2 runs the same
# formula backwards, which is the whole of section 7.
#
# A COUNT OF PARAMETERS THAT FIT IS A FLOOR -- the mirror of F1's count of
# devices, which is a ceiling. Half a parameter does not fit and 203 devices
# were needed because 202.5 do not finish the job. The floor happens not to
# bite at this budget; it is applied anyway, because a rounding rule chosen to
# suit one arithmetic is a rule that stops holding at the next one.
# --------------------------------------------------------------------------
BUDGET_GB = 24                          # one accelerator's memory
BYTES_PER_PARAM = 2                     # a two-byte format, as in F1
emit("f02.budget.gb", BUDGET_GB)
emit("f02.params.in.budget", math.floor(BUDGET_GB * 10**9 / BYTES_PER_PARAM))

# --------------------------------------------------------------------------
# Cross-entropy for one example, rearranged: L = -ln p, so p = e^(-L). The
# algebra is this program's; the exponential step is F3's and the frame says
# so rather than borrowing it.
#
# The loss is quoted in nats. Writing it as a bare `log` would be a build error
# and C10 would catch it first: in Polish schooling `log` is base ten, in
# machine-learning writing it is base e, and the two readerships collide here.
# --------------------------------------------------------------------------
LOSS_NATS = 2.4                         # a plausible mid-training LM loss
emit("f02.loss.nats", LOSS_NATS, 1)
emit("f02.prob.from.loss", math.exp(-LOSS_NATS), 4)

# --------------------------------------------------------------------------
# The convolution output size, floor((W + 2p - k)/s) + 1. Catalogue trap 39.
#
# The single-layer case is the one the Quiz and the Test exercises share, so it
# is emitted rather than typed in three places. Its two wrong answers -- 3.5,
# which cannot be a shape, and 4, which is the natural repair and the wrong
# direction -- are the arithmetic the frame is teaching and stay inline.
# --------------------------------------------------------------------------
CONV_W, CONV_K, CONV_S, CONV_P = 8, 3, 2, 0
emit("f02.conv.w", CONV_W)
emit("f02.conv.k", CONV_K)
emit("f02.conv.s", CONV_S)
emit("f02.conv.p", CONV_P)


def conv_out(w: int, k: int, s: int, p: int) -> int:
    """The formula exactly as printed, floor and all."""
    return (w + 2 * p - k) // s + 1


def conv_dropped(w: int, k: int, s: int, p: int) -> int:
    """Input positions no window ever covers. This is what the floor discards."""
    return (w + 2 * p) - (k + s * (conv_out(w, k, s, p) - 1))


emit("f02.conv.dropped", conv_dropped(CONV_W, CONV_K, CONV_S, CONV_P))

# Three such layers. Not chained from W = 8: that stack dies at the second
# layer, which is a different lesson. A 30-wide map loses one input column at
# every one of the three layers, which is the compounding the trap is about.
#
# `expected` is the naive reader's OWN answer, computed by their own two moves:
# ignore the floor, then round the fraction up at the end because a shape has
# to be an integer. That is what makes the gap an integer and lets the frame
# use the catalogue's own words -- one smaller than you expected, three layers
# downstream -- rather than reporting a gap of 0.875 nobody would recognise.
CONV_STACK_W = 30
CONV_STACK_LAYERS = 3
emit("f02.conv.stack.w", CONV_STACK_W)

naive = float(CONV_STACK_W)
actual = CONV_STACK_W
for _ in range(CONV_STACK_LAYERS):
    naive = (naive + 2 * CONV_P - CONV_K) / CONV_S + 1          # no floor
    actual = conv_out(actual, CONV_K, CONV_S, CONV_P)           # the truth

emit("f02.conv.expected.3", math.ceil(naive))
emit("f02.conv.actual.3", actual)
emit("f02.conv.gap.3", math.ceil(naive) - actual)

# --------------------------------------------------------------------------
# The Adam update, theta <- theta - eta * mhat / (sqrt(vhat) + eps), against
# the precedence error that reads the epsilon as added to the whole quotient.
#
# The parameter here has seen a steady gradient of 1e-8, so mhat = 1e-8 and
# vhat = 1e-16 are consistent with each other rather than chosen to flatter the
# comparison: sqrt(vhat) then lands exactly on eps, which is the point at which
# the epsilon is doing half the work. The printed form halves the step; the
# misread form leaves it alone and has no bound at all as vhat goes to zero.
#
# Both step sizes at the same precision, because the frame sets them side by
# side and the interesting digits are in the tail.
# --------------------------------------------------------------------------
ADAM_ETA = 1e-3
ADAM_MHAT = 1e-8
ADAM_VHAT = 1e-16
ADAM_EPS = 1e-8
emit("f02.adam.eta", sci(ADAM_ETA))
emit("f02.adam.mhat", sci(ADAM_MHAT))
emit("f02.adam.vhat", sci(ADAM_VHAT))
emit("f02.adam.eps", sci(ADAM_EPS))

adam_correct = ADAM_ETA * ADAM_MHAT / (math.sqrt(ADAM_VHAT) + ADAM_EPS)
adam_wrong = ADAM_ETA * ADAM_MHAT / math.sqrt(ADAM_VHAT) + ADAM_EPS
emit("f02.adam.correct", adam_correct, 8)
emit("f02.adam.wrong.prec", adam_wrong, 8)
# Five decimal places, not two: the ratio is not quite 2 and the digits should
# say so. Rounding it to 2.00 would print a number the reader could check in
# their head and find exact, which it is not.
emit("f02.adam.ratio", adam_wrong / adam_correct, 5)

# --------------------------------------------------------------------------
# Write the file the book reads.
# --------------------------------------------------------------------------
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f02.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f02_algebra.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ]
    lines += [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in VALUES.items()
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf8")
    width = max(len(k) for k in VALUES)
    for k, (body, numeric) in VALUES.items():
        print(f"  {k:<{width}}  {body}{'' if numeric else '   (text)'}")
    print(f"\n  {len(VALUES)} values -> {OUT.relative_to(OUT.parents[2])}")


if __name__ == "__main__":
    main()
