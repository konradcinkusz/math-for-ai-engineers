#!/usr/bin/env python3
"""Program F5 --- Functions and graphs.

Every number Program F5 prints that the reader cannot do in their head is
computed here and written to figures/values/f05.tex, which the book \\input{}s.

F5's thesis is that a function is a machine with one output per input, and that
shifting, scaling and reflecting its graph are four moves you can do by eye.
Almost all of its arithmetic is therefore the thing being taught and stays
inline. What is computed here is the part the reader cannot do in their head,
and it is concentrated in two places: the logistic curve, whose values nobody
evaluates mentally, and SECTION 7's temperature table, which is the program's
payoff and has to be a table of real numbers or the claim it supports is
folklore.

STDLIB ONLY, as in F3 and F4: `make numbers` must run on a plain python3.
numpy appears nowhere in the arithmetic. It is opened at the bottom purely to
CHECK the argmax claim against a second implementation, and that block
announces itself when numpy is absent rather than passing silently.

NOT EMITTED, and none of it should be --- putting it behind \\val{} would be
theatre. This program teaches graph reading, so its arithmetic is the thing
being taught and stays inline as digits in the prose:

    f(x) = x^2 at 0, 1, 2, 3 -> 0, 1, 4, 9;  f(x-3) at x = 3 -> 0;
    the shifts +2 and -3;  the reflections -f and f(-x);
    2x + 1 at x = 0, 1, 2 -> 1, 3, 5;
    |x| at -2 and 2 -> 2;  relu(-2) = 0, relu(2) = 2;
    sigma(0) = 0.5, which is the one logistic value a reader must know cold;
    the composition (2x+1)^2 at x = 1 -> 9 against 2x^2+1 -> 3.

THE PROGRAM'S PAYOFF, AND THE ONE CLAIM THAT MUST BE MEASURED. Section 7 says
that a strictly increasing function does not move the argmax, and therefore
that temperature cannot change which token is most likely -- only how often the
others get sampled instead. Both halves are computed below over one fixed logit
vector, at three temperatures, and the argmax invariance is ASSERTED rather
than printed and hoped for. A table of probabilities that shift by a factor of
four while the argmax does not move is the whole argument; a sentence saying so
is not.

TWO THINGS THE .TEX AUTHOR MUST NOT WRITE, both found by running rather than
by reasoning, and both recorded at their computation below:

  * "Temperature does not change the probabilities" is NOT the claim and is
    false. It changes them a great deal, and the striking figure is not the
    top of the distribution but the bottom: over the range used here the most
    likely token falls from 0.7042 to 0.4042, a factor of 1.7, while the LEAST
    likely rises from 0.0017 to 0.0902, a factor of 51.7. What does not change
    is which of them is largest. Write the invariance of the ARGMAX, never of
    the distribution -- and quote the tail, because the top understates it by
    thirty-fold.
  * The bias-free line through those three points is NOT a bad fit by a
    little. Its best slope is 2.5714 and its worst residual is 0.5714 against
    a bias line that passes through every point exactly. Quote the residual,
    not an adjective.

Run:  python3 code/f05_functions.py      (or: make numbers)
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


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


# ==========================================================================
# SECTION 4 --- weight and bias are scale and shift
#
# sigma(wx + b) is the logistic curve with the two moves of section 3 applied
# to its INPUT: w squashes it horizontally and b slides it sideways. The frame
# has to give the reader numbers, because nobody evaluates a logistic in their
# head beyond sigma(0) = 0.5.
#
# THE HONEST DETAIL, and it is the sentence worth the space: b is not "where
# the curve crosses a half". The crossing is at x = -b/w, so the SAME bias
# moves the curve a different distance depending on the weight. At w = 1,
# b = -2 the crossing is at 2; at w = 5, b = -2 it is at 0.4. A reader who
# reads the bias as a position will be wrong by a factor of the weight.
# ==========================================================================
SIG_AT = (-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0)
for _x in SIG_AT:
    emit(f"f05.sig.{str(_x).replace('-', 'm').replace('.0', '')}", sigmoid(_x), 4)

# The one value the whole section turns on, and the reader must be able to
# check it: sigma(0) is a half exactly, because e^0 = 1 and 1/(1+1) = 1/2.
assert sigmoid(0.0) == 0.5, "sigma(0) is not exactly a half"

# Steepness. The weight is the horizontal squash, so the width of the band in
# which the curve does its work shrinks by exactly the factor w. Measured as
# the x-distance from sigma = 0.1 to sigma = 0.9, which is the part of the
# curve a reader can point at on the page.
def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


BAND = logit(0.9) - logit(0.1)          # the width at w = 1
emit("f05.band.w1", BAND, 4)
emit("f05.band.w5", BAND / 5.0, 4)
emit("f05.band.whalf", BAND / 0.5, 4)

# ...and that it IS exactly a division by w, which is the claim the frame
# makes. Checked over three weights rather than asserted from the algebra.
for _w in (0.5, 1.0, 5.0):
    _lo = logit(0.1) / _w
    _hi = logit(0.9) / _w
    assert abs((_hi - _lo) - BAND / _w) < 1e-12, f"the band is not BAND/w at w={_w}"
    # and the curve really does read 0.1 and 0.9 at those two points
    assert abs(sigmoid(_w * _lo) - 0.1) < 1e-12
    assert abs(sigmoid(_w * _hi) - 0.9) < 1e-12

# The crossing point, and the trap that the bias is not a position.
# NOT emitted: -b/w at b = -2 is 2 and 0.4 at the two weights, and both are
# head arithmetic, which this book writes inline. The assertion stays, because
# what is being checked is that the logistic really does read a half there.
CROSS_W1 = 2.0
CROSS_W5 = 0.4
for _w, _cross in ((1.0, CROSS_W1), (5.0, CROSS_W5)):
    assert abs(sigmoid(_w * _cross - 2.0) - 0.5) < 1e-12, "the crossing is not at -b/w"

# What the bias buys. Three points on the line y = 2x + 1. With a bias the fit
# is exact; without one the best line through the origin misses every point,
# and the frame quotes the worst miss rather than calling the fit poor.
POINTS = ((1.0, 3.0), (2.0, 5.0), (3.0, 7.0))
# least squares through the origin: slope = sum(xy) / sum(x^2)
_num = sum(x * y for x, y in POINTS)
_den = sum(x * x for x, _ in POINTS)
NOBIAS_SLOPE = _num / _den
NOBIAS_WORST = max(abs(NOBIAS_SLOPE * x - y) for x, y in POINTS)
emit("f05.nobias.slope", NOBIAS_SLOPE, 4)
emit("f05.nobias.worst", NOBIAS_WORST, 4)
# The bias line is exact on all three, which is what makes the comparison fair.
for _x, _y in POINTS:
    assert 2.0 * _x + 1.0 == _y, "the three points are not on y = 2x + 1"
assert NOBIAS_WORST > 0.5, "the no-bias fit is supposed to miss visibly"

# ==========================================================================
# SECTION 6 --- inverses
#
# The logit is the inverse of the logistic, and the round trip is the cheapest
# demonstration in the program. Note what is emitted: the round-trip ERROR, not
# the round-trip value, because the value is the input and printing it back
# proves nothing a reader would not assume.
# ==========================================================================
ROUND_TRIP = 0.9
emit("f05.logit.p9", logit(ROUND_TRIP), 4)
RT_ERR = abs(sigmoid(logit(ROUND_TRIP)) - ROUND_TRIP)
# Emitted in scientific notation: 17 decimal places prints a row of zeros and a
# digit, which is unreadable on the page and says nothing a reader can use.
emit("f05.roundtrip.err", f"{RT_ERR:.1e}")
assert RT_ERR < 1e-15, "the logistic and the logit are not inverse to the bit"

# ==========================================================================
# SECTION 7 --- THE PAYOFF. Monotone functions and the argmax that does not
# move.
#
# One fixed logit vector, three temperatures. Dividing by T > 0 is strictly
# increasing, and exponentiating is strictly increasing, so the ORDER of the
# scores is the same at every temperature and therefore so is the argmax. The
# probabilities are not the same at all -- that is the point, and it is why
# raising the temperature changes what gets sampled without changing what is
# most likely.
#
# THE CLAIM IS ABOUT THE ARGMAX, NOT THE DISTRIBUTION. See the module
# docstring. Across this table the top probability falls by a factor of 1.7 and
# the bottom one rises by a factor of 51.7, and the argmax never moves. The
# tail is the figure to quote: temperature is a knob on the unlikely tokens,
# which is exactly what "more creative" means and exactly what the argmax
# cannot tell you.
# ==========================================================================
LOGITS = (2.0, 1.5, 0.5, -1.0)
TEMPS = (0.5, 1.0, 2.0)


def softmax(z, temperature: float = 1.0):
    scaled = [zi / temperature for zi in z]
    m = max(scaled)                       # the shift Program P1 owns
    exps = [math.exp(s - m) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def argmax(xs) -> int:
    return max(range(len(xs)), key=lambda i: xs[i])


PROBS = {t: softmax(LOGITS, t) for t in TEMPS}
for _t in TEMPS:
    _tag = str(_t).replace(".", "")       # 05, 10, 20
    for _i, _p in enumerate(PROBS[_t]):
        emit(f"f05.sm.t{_tag}.p{_i + 1}", _p, 4)

# The invariance, asserted rather than eyeballed off the table above. This is
# the program's central claim and it is the one thing here that must not be
# able to rot quietly.
BASE = argmax(LOGITS)
for _t in TEMPS:
    assert argmax(PROBS[_t]) == BASE, f"temperature {_t} moved the argmax"
# ...and over a wide sweep, not merely the three the book prints.
for _i in range(1, 400):
    _t = _i / 20.0
    assert argmax(softmax(LOGITS, _t)) == BASE, f"temperature {_t} moved the argmax"

# The half of the sentence that IS true: what the reader samples changes a
# great deal. The chance of drawing something other than the most likely token
# is the number to quote, because it is the observable consequence.
#
# The two ENDS of the range only. The middle temperature's pair is derivable
# from the table above it and the page does not print it, and a value nothing
# references is a value nobody will notice going stale -- which is what
# parity's C7 is for and why it caught this loop emitting six.
for _t in (min(TEMPS), max(TEMPS)):
    _tag = str(_t).replace(".", "")
    emit(f"f05.sm.t{_tag}.top", max(PROBS[_t]), 4)
    emit(f"f05.sm.t{_tag}.other", 1.0 - max(PROBS[_t]), 4)

TOP_LO = min(max(PROBS[t]) for t in TEMPS)
TOP_HI = max(max(PROBS[t]) for t in TEMPS)
emit("f05.sm.top.ratio", TOP_HI / TOP_LO, 2)

# The tail, which is where temperature actually does its work and which the top
# of the distribution understates by thirty-fold. LAST is the least likely of
# the four at every temperature -- checked, not assumed, because "the last
# entry" and "the smallest entry" are only the same while the vector stays
# sorted.
LAST = len(LOGITS) - 1
for _t in TEMPS:
    assert min(range(len(LOGITS)), key=lambda i: PROBS[_t][i]) == LAST
TAIL_LO = min(PROBS[t][LAST] for t in TEMPS)
TAIL_HI = max(PROBS[t][LAST] for t in TEMPS)

# A BOUND, not the ratio, and the reason is worth keeping. The exact ratio is
# 51.7; the table prints the tail probabilities rounded to four decimals, where
# the smaller of them (0.0017) carries two significant figures, so a reader who
# divides what is on the page gets 53.1. Quoting 51.7 beside a table that
# yields 53.1 is F4's 22778-against-22776 defect wearing different digits.
#
# The fix is not more decimals in one row of an otherwise uniform table. It is
# to say only what the page can support -- and both divisions clear fifty, so
# fifty is what the page says.
TAIL_FLOOR = 50
emit("f05.sm.tail.floor", TAIL_FLOOR)
_page = round(TAIL_HI, 4) / round(TAIL_LO, 4)
assert TAIL_HI / TAIL_LO > TAIL_FLOOR, "the exact tail ratio no longer clears the printed bound"
assert _page > TAIL_FLOOR, "the ROUNDED table no longer clears the printed bound"

# Two INVARIANTS rather than two thresholds. The maximum of a softmax falls
# monotonically as the temperature rises -- it tends to 1 as T -> 0 and to 1/n
# as T -> infinity -- and the minimum rises for the same reason. Asserting the
# direction survives a change of logits; asserting a magnitude does not.
_tops = [max(PROBS[t]) for t in sorted(TEMPS)]
_bots = [min(PROBS[t]) for t in sorted(TEMPS)]
assert _tops == sorted(_tops, reverse=True), "the top probability no longer falls with T"
assert _bots == sorted(_bots), "the bottom probability no longer rises with T"
assert TAIL_HI / TAIL_LO > TOP_HI / TOP_LO, "the tail no longer moves more than the top"

# The top ratio IS reproducible from the page: both its terms carry four
# significant figures, so 0.7042 / 0.4042 gives the printed 1.74. Checked,
# because that is the property the tail turned out not to have.
assert round(round(TOP_HI, 4) / round(TOP_LO, 4), 2) == round(TOP_HI / TOP_LO, 2), \
    "the top ratio no longer reproduces from the rounded table"

# The order itself, over the whole vector, at every temperature: not just the
# argmax but every rank. Strict monotonicity preserves the entire ordering, and
# that is the general statement the argmax result is a corollary of.
_ranks = sorted(range(len(LOGITS)), key=lambda i: LOGITS[i], reverse=True)
for _t in TEMPS:
    assert sorted(range(len(LOGITS)), key=lambda i: PROBS[_t][i], reverse=True) == _ranks, \
        f"temperature {_t} reordered the vector"

# And the log-space corollary, which is F3's payoff cashed here: ln is strictly
# increasing, so the argmax of a probability is the argmax of its logarithm.
# This is why a decoder never has to leave log space to pick a token.
_logp = [math.log(p) for p in PROBS[1.0]]
assert argmax(_logp) == BASE, "ln moved the argmax"

# The direction matters. A strictly DECREASING function swaps argmax and
# argmin, which is the trap: negating a loss is exactly this move, and it is
# how "minimise the loss" and "maximise the likelihood" are the same
# instruction.
_neg = [-p for p in PROBS[1.0]]
assert argmax(_neg) == min(range(len(PROBS[1.0])), key=lambda i: PROBS[1.0][i]), \
    "negation did not swap argmax and argmin"

# ==========================================================================
# A second implementation, for the one claim the whole program rests on.
#
# numpy is not used in any arithmetic above; it is opened here only to check
# the argmax invariance against code this script did not write. It ANNOUNCES
# itself when it is skipped, because `make numbers` must run on a plain
# python3 and a check that silently does not run is worse than no check --
# that is F3's np.logspace lesson, and the reason the note below is printed on
# every run rather than only on failure.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the argmax invariance was NOT cross-checked"
else:
    _z = _np.array(LOGITS, dtype=_np.float64)
    for _t in TEMPS:
        _s = _z / _t
        _e = _np.exp(_s - _s.max())
        assert int((_e / _e.sum()).argmax()) == BASE, f"numpy disagrees at T={_t}"
    NUMPY_NOTE = (f"numpy {_np.__version__}: argmax invariance cross-checked "
                  f"at T = {', '.join(str(t) for t in TEMPS)}")

# ==========================================================================
# Write the file the book reads.
# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f05.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f05_functions.py --- do not edit.",
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
    print(f"  argmax at every temperature: index {BASE} (logit {LOGITS[BASE]}); "
          f"top {TOP_LO:.4f}-{TOP_HI:.4f} ({TOP_HI / TOP_LO:.2f}x), "
          f"tail {TAIL_LO:.4f}-{TAIL_HI:.4f} ({TAIL_HI / TAIL_LO:.1f}x)")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
