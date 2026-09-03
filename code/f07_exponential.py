#!/usr/bin/env python3
"""Program F7 --- Exponential, logistic and hyperbolic functions.

Every number Program F7 prints that the reader cannot do in their head is
computed here and written to figures/values/f07.tex, which the book \\input{}s.

F7's thesis is that e^x is the function that is its own rate of change and the
logistic is what you get when you squash it into [0,1]. Almost nothing in that
sentence can be checked by hand, so this program is the most computed of the
Foundation part so far -- and the two claims that matter most are IDENTITIES,
which means they can be asserted rather than merely evaluated.

STDLIB ONLY, as in F3 to F6: `make numbers` must run on a plain python3. numpy
is opened only at the bottom to cross-check the saturation figures, and it
announces itself when absent.

NOT EMITTED, and none of it should be -- this program teaches reading a curve,
so the values a reader must hold stay inline:

    e^0 = 1;  sigma(0) = 1/2, which F05 emits and F07 does not re-emit;
    the softmax of two equal scores is (1/2, 1/2);
    the claim that k > 0 grows and k < 0 decays.

tanh(0) = 0 IS emitted, and it is the exception that proves the rule: it is a
row of a table whose other rows are computed, and a table with one hand-typed
cell is a table nobody can regenerate. F05's sigma table does the same with
sigma(0). Uniformity inside a table beats the head-arithmetic test.

THE TWO IDENTITIES, and they are the reason this program is not a list of
tables. Both are asserted over a range rather than checked at a point:

  * tanh(x) = 2 sigma(2x) - 1. The hyperbolic tangent is the logistic curve
    stretched to twice its height and slid down -- exactly two of F05's four
    moves. A reader who has met sigma has met tanh and does not know it.
  * softmax on TWO scores is the logistic of their difference. So the softmax
    F07 previews is not a new function; it is the one the reader has been
    reading off a table for two programs, generalised past two outcomes.

THE MEASUREMENT: SATURATION. sigma'(x) = sigma(x)(1 - sigma(x)), which peaks at
0.25 and falls away fast. The frames quote the fall as a RATIO, because the
absolute numbers mean nothing to a reader who has not met a derivative -- and
the ratio is what the vanishing-gradient complaint is about. See the block
below for what may and may not be said about it before F11 exists.

Run:  python3 code/f07_exponential.py      (or: make numbers)
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
# SECTION 1 --- where e comes from
#
# (1 + 1/n)^n as n grows. The frames build the table by hand for n = 1, 2 and
# 12, which a reader can check, and then quote the large-n rows, which they
# cannot. What the table shows is that the sequence CONVERGES rather than
# growing without bound, and that is the whole of the argument for e being a
# number rather than a limit nobody reaches.
# ==========================================================================
COMPOUND_N = (1, 2, 12, 365, 1_000_000)
for _n in COMPOUND_N:
    emit(f"f07.compound.{_n}", (1.0 + 1.0 / _n) ** _n, 6)

emit("f07.e", math.e, 6)

# The sequence is increasing and bounded above by e -- which is the shape of
# the convergence argument, and is asserted rather than asserted-in-prose.
_vals = [(1.0 + 1.0 / n) ** n for n in COMPOUND_N]
assert _vals == sorted(_vals), "the compound sequence no longer increases"
assert all(v < math.e for v in _vals), "the compound sequence no longer sits below e"
# ...and the last row is within a thousandth of a per cent of e, which is what
# lets the frame say the table has arrived rather than that it is on its way.
assert abs(_vals[-1] - math.e) / math.e < 1e-5

# ==========================================================================
# SECTION 1's TRAP --- "exponential growth means fast growth"
#
# It does not. It means growth proportional to the current size, and a
# polynomial can stay ahead of it for a very long way. e^x against x^5 is the
# cleanest demonstration the reader can check by hand at one end and cannot at
# the other: at x = 5 the polynomial is more than twenty times larger, and the
# exponential does not pass it until past x = 12.
#
# The crossover is found by bisection rather than quoted, so that changing the
# power changes the number on the page.
# ==========================================================================
POWER = 5


def gap(x: float) -> float:
    return math.exp(x) - x ** POWER


emit("f07.poly.at5.exp", math.exp(5.0), 1)
# NOT emitted: 5^5 = 3125 is head arithmetic and the frame writes it inline,
# which is the rule this book states for anything the reader can do.
emit("f07.poly.at5.ratio", 5.0 ** POWER / math.exp(5.0), 1)

_lo, _hi = 5.0, 40.0                       # gap(5) < 0 and gap(40) > 0
assert gap(_lo) < 0 < gap(_hi)
for _ in range(200):
    _mid = (_lo + _hi) / 2.0
    if gap(_mid) < 0:
        _lo = _mid
    else:
        _hi = _mid
CROSSOVER = (_lo + _hi) / 2.0
emit("f07.poly.crossover", CROSSOVER, 2)

# The invariant, not the number: the polynomial leads below the crossover and
# the exponential leads above it, and it never changes back.
assert math.exp(CROSSOVER - 1) < (CROSSOVER - 1) ** POWER
assert math.exp(CROSSOVER + 1) > (CROSSOVER + 1) ** POWER
assert all(math.exp(x) > x ** POWER for x in (CROSSOVER + 1, 50.0, 100.0)), \
    "the exponential no longer stays ahead once it passes"

# ==========================================================================
# SECTION 2 --- growth, decay and the half-life
#
# A learning-rate schedule, because it is the exponential decay this reader
# actually meets: lr(t) = lr0 * exp(-k t). The half-life is ln 2 / k and it is
# INDEPENDENT of where you start, which is the property worth the frame.
#
# THE HONEST DETAIL: getting to a tenth is not ten half-lives and it is not
# five. It is ln 10 / ln 2 = 3.32 of them, and the frame quotes that rather
# than letting the reader carry a linear intuition into a ratio.
# ==========================================================================
DECAY_K = 0.05
emit("f07.decay.halflife", math.log(2.0) / DECAY_K, 2)
emit("f07.decay.tenth", math.log(10.0) / DECAY_K, 2)
emit("f07.decay.tenth.halflives", math.log(10.0) / math.log(2.0), 2)
emit("f07.decay.at100", math.exp(-DECAY_K * 100), 4)

# The half-life is independent of the starting value: check it from three.
for _lr0 in (1.0, 0.1, 3.7):
    _t = math.log(2.0) / DECAY_K
    assert abs(_lr0 * math.exp(-DECAY_K * _t) - _lr0 / 2) < 1e-12, \
        "the half-life is no longer independent of the starting value"

# ==========================================================================
# SECTION 3 --- the logistic, and SECTION 5 --- saturation
#
# sigma'(x) = sigma(x)(1 - sigma(x)). The frames may not call it a derivative:
# F11 has not happened yet. What they may say, and what the reader can see, is
# that the curve's STEEPNESS is largest in the middle and collapses at the
# ends, and that the collapse is measured as a ratio.
#
# WHAT THE PAGE MAY NOT SAY. Not "the gradient vanishes" -- that is F12's
# sentence and it needs the chain rule to mean anything, because one small
# factor is survivable and the product of forty is not. F07 owns the SHAPE and
# hands the consequence forward.
# ==========================================================================
def slope(x: float) -> float:
    s = sigmoid(x)
    return s * (1.0 - s)


SLOPE_AT = (0.0, 1.0, 2.0, 4.0, 6.0)

# FOUR SIGNIFICANT FIGURES, not four decimal places, and the difference is the
# whole of a defect the review found. At four decimals sigma'(6) prints 0.0025,
# which carries TWO significant figures -- and frame 17 asks the reader to
# divide it into 0.2500, which gives exactly 100 against an answer box saying
# 101. The table is the operand of a question, so it has to carry enough
# figures to answer it. Four significant figures leaves the top three rows
# unchanged and gives 0.01766 and 0.002467, both of which reproduce.
def _sigfig(value: float, figures: int = 4) -> str:
    """Format to a fixed number of significant figures, trailing zeros kept.

    `f"{x:.4g}"` drops them -- 0.25 rather than 0.2500 -- which would make one
    column carry two conventions. This keeps them, so the column reads as one.
    """
    if value == 0.0:                                         # pragma: no cover
        return "0"
    exponent = math.floor(math.log10(abs(value)))
    decimals = max(figures - 1 - exponent, 0)
    return f"{value:.{decimals}f}"


SLOPE_PRINTED = {x: _sigfig(slope(x)) for x in SLOPE_AT}
for _x in SLOPE_AT:
    emit(f"f07.slope.{int(_x)}", SLOPE_PRINTED[_x])

emit("f07.slope.ratio6", slope(0.0) / slope(6.0), 0)
emit("f07.slope.ratio4", slope(0.0) / slope(4.0), 0)
emit("f07.slope.ratio2", slope(0.0) / slope(2.0), 1)

# AND THE PAGE MUST REPRODUCE ITS OWN RATIOS. Frame 17 tells the reader to
# divide two numbers off the table; frames 18 and 23 print the answers. This
# asserts that dividing the PRINTED forms gives the PRINTED answer, which is
# the check the four-decimal column failed.
for _at, _key, _digits in ((6.0, "ratio6", 0), (4.0, "ratio4", 0), (2.0, "ratio2", 1)):
    _from_page = float(SLOPE_PRINTED[0.0]) / float(SLOPE_PRINTED[_at])
    _printed = f"{slope(0.0) / slope(_at):.{_digits}f}"
    assert f"{_from_page:.{_digits}f}" == _printed, (
        f"f07.slope.{_key} prints {_printed} where the table divides to "
        f"{_from_page:.{_digits}f}: the reader cannot reproduce it")

# Invariants, not observations: the steepness peaks at the centre at exactly a
# quarter, and falls monotonically as you move out.
assert abs(slope(0.0) - 0.25) < 1e-15, "the logistic no longer peaks at a quarter"
_out = [slope(x) for x in SLOPE_AT]
assert _out == sorted(_out, reverse=True), "the steepness no longer falls away from the centre"
assert slope(0.0) / slope(6.0) > 50, "the collapse over six units is no longer dramatic"

# The point at which the mathematics and the arithmetic part company. sigma
# never reaches 1, and in binary64 it rounds to exactly 1.0 from a definite
# place onwards -- so ln(1 - p) is always defined in exact arithmetic and is
# not on a machine. The frame quotes the place rather than "around 37", which
# is what it said when it was written from memory.
#
# AND THE PLACE IS DERIVED RATHER THAN SWEPT, which is a correction. This used
# to walk out from zero in steps of a tenth and report the first grid point
# that rounded to one, which gives 36.8 -- so a reader checking at 36.75 found
# sigma already exactly 1.0 and the page wrong. The threshold is where e^-x
# falls below the last place of 1.0, at 2^-53, so it is exactly 53 ln 2: a
# property of IEEE-754 binary64 rather than of the grid this program swept.
SIG_SATURATES_EXACT = 53.0 * math.log(2.0)
_lo, _hi = 30.0, 45.0
for _ in range(200):
    _mid = (_lo + _hi) / 2.0
    if sigmoid(_mid) == 1.0:
        _hi = _mid
    else:
        _lo = _mid
assert abs(_hi - SIG_SATURATES_EXACT) < 1e-9, (
    f"sigma first returns 1.0 at {_hi}, not at 53 ln 2 = {SIG_SATURATES_EXACT}")
SIG_SATURATES = round(SIG_SATURATES_EXACT, 2)
emit("f07.sig.saturates", SIG_SATURATES, 2)
assert sigmoid(SIG_SATURATES) == 1.0, "sigma no longer rounds to one there"
assert sigmoid(SIG_SATURATES - 0.01) < 1.0, "sigma rounds to one earlier than reported"

# ==========================================================================
# SECTION 4 --- tanh IS the logistic, moved
#
# tanh(x) = 2 sigma(2x) - 1. Asserted over a range rather than shown at a
# point, because "these two curves are the same curve" is the claim and one
# agreeing value would not establish it.
# ==========================================================================
TANH_AT = (-2.0, -1.0, 0.0, 1.0, 2.0)
for _x in TANH_AT:
    _tag = str(_x).replace("-", "m").replace(".0", "")
    emit(f"f07.tanh.{_tag}", math.tanh(_x), 4)

_worst = max(abs(math.tanh(x / 4.0) - (2.0 * sigmoid(x / 2.0) - 1.0)) for x in range(-200, 201))
emit("f07.tanh.identity.err", f"{_worst:.1e}")
assert _worst < 1e-15, "tanh is no longer 2 sigma(2x) - 1 to within a rounding error"

# tanh is zero-centred and the logistic is not, which is the whole of the
# practical difference and is checkable in one line.
assert math.tanh(0.0) == 0.0 and sigmoid(0.0) == 0.5

# tanh saturates HARDER, not less: its steepness is 1 - tanh^2, which peaks at
# 1 against the logistic's quarter and therefore falls further.
def tanh_slope(x: float) -> float:
    return 1.0 - math.tanh(x) ** 2

# Four DECIMALS here, not four significant figures: 0.0707 carries three of
# them, so the division below reproduces and there is no reason to churn two
# committed values. The logistic's column needed the sigfig form because
# sigma'(6) rounds to 0.0025 at four decimals, which is two figures.
TANH_PRINTED = {x: f"{tanh_slope(x):.4f}" for x in (0.0, 2.0)}
emit("f07.tanh.slope0", TANH_PRINTED[0.0])
emit("f07.tanh.slope2", TANH_PRINTED[2.0])
assert tanh_slope(0.0) / tanh_slope(2.0) > slope(0.0) / slope(2.0), \
    "tanh no longer saturates harder than the logistic"

# AND THE COMPARISON IS TWO COMPUTATIONS RATHER THAN ONE VALUE PRINTED TWICE.
# Section 4's whole argument is that only the horizontal squash moves anything
# ALONG the axis, so tanh's flat region comes in by two rather than by four --
# and the evidence for it is that tanh loses over TWO units what the logistic
# takes FOUR to lose. Those are different quantities computed from different
# curves. Emitting one of them under both names would be the two-numbers-that-
# look-like-one defect appearing inside the sentence that needs them to be two,
# so both are emitted and their agreement is asserted rather than assumed.
emit("f07.tanh.ratio2", tanh_slope(0.0) / tanh_slope(2.0), 0)
assert abs(tanh_slope(0.0) / tanh_slope(2.0) - slope(0.0) / slope(4.0)) < 0.5, \
    "tanh's two-unit loss no longer matches the logistic's four-unit loss"
assert f"{tanh_slope(0.0) / tanh_slope(2.0):.0f}" == f"{slope(0.0) / slope(4.0):.0f}", \
    "the two losses no longer print as the same figure, so the frame's evidence is gone"

# And the ratio has to survive the reader dividing the two printed cells of the
# table it sits in, which is what the frame instructs.
_from_page = float(TANH_PRINTED[0.0]) / float(TANH_PRINTED[2.0])
assert f"{_from_page:.0f}" == f"{tanh_slope(0.0) / tanh_slope(2.0):.0f}", \
    "f07.tanh.ratio2 does not reproduce from the two cells beside it"

# ==========================================================================
# SECTION 6 --- softmax on two scores IS the logistic
#
# The program previews softmax as exponentials over their own sum, and the
# check that makes it a preview rather than a new topic is that on two scores
# it collapses to the function the reader already has.
# ==========================================================================
def softmax2(a: float, b: float):
    m = max(a, b)
    ea, eb = math.exp(a - m), math.exp(b - m)
    t = ea + eb
    return ea / t, eb / t


_worst2 = max(abs(softmax2(a / 10.0, b / 10.0)[0] - sigmoid((a - b) / 10.0))
              for a in range(-60, 61) for b in range(-60, 61))
emit("f07.softmax2.err", f"{_worst2:.1e}")
assert _worst2 < 1e-15, "softmax on two scores is no longer the logistic of their difference"

# A worked pair the frames print, and its logistic twin, which must agree.
SM_A, SM_B = 2.0, 0.5
emit("f07.softmax2.a", softmax2(SM_A, SM_B)[0], 4)
emit("f07.softmax2.b", softmax2(SM_A, SM_B)[1], 4)
assert abs(softmax2(SM_A, SM_B)[0] - sigmoid(SM_A - SM_B)) < 1e-15

# ==========================================================================
# A second implementation, for the two identities the program rests on.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the two identities were NOT cross-checked"
else:
    _x = _np.linspace(-20.0, 20.0, 4001)
    assert _np.allclose(_np.tanh(_x), 2.0 / (1.0 + _np.exp(-2.0 * _x)) - 1.0, atol=1e-15)
    _d = _np.linspace(-6.0, 6.0, 1201)
    assert _np.allclose(1.0 / (1.0 + _np.exp(-_d)),
                        _np.exp(_d) / (_np.exp(_d) + 1.0), atol=1e-15)
    NUMPY_NOTE = (f"numpy {_np.__version__}: tanh = 2 sigma(2x) - 1 and the two "
                  f"forms of sigma cross-checked over 4001 and 1201 points")

# ==========================================================================
# Write the file the book reads.
# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f07.tex"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f07_exponential.py --- do not edit.",
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
    print(f"  tanh(x) = 2 sigma(2x) - 1: worst error over 401 points {_worst:.1e}")
    print(f"  softmax on two scores = logistic of the difference: worst {_worst2:.1e}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
