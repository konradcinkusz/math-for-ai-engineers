#!/usr/bin/env python3
"""Program P20 --- Gradient descent: from SGD to Adam.

Every number Program P20 prints that the reader cannot do in their head is
computed here and written to figures/values/p20.tex, which the book \\input{}s.

P20's thesis is that EVERY OPTIMISER IN COMMON USE IS ONE UPDATE WITH A
DIFFERENT ESTIMATE OF HOW FAR AND IN WHICH DIRECTION, and that each addition
fixes a NAMED failure of the one before it. Written as a list of algorithms it
is six recipes to memorise; written as a sequence of repairs it is one line of
code and five arguments.

WHAT P20 IS OWED, read out of the files rather than remembered:

  F04  OWNS THE EXPONENTIAL MOVING AVERAGE OUTRIGHT -- the recurrence, the
       unrolled weights, the half-life, the bias correction derived from the
       initialisation at zero, and the (1 - beta) convention question, which
       its review pass settled by MEASURING rather than by naming a library.
       F04 says in as many words: "Program P20 supplies the gradient and the
       rest of the optimiser; what it does not have to supply is the average."
       So momentum here is F04's average with a gradient in it, and Adam is
       that recurrence run twice -- both of which F04 already states.
       F04 also hands over the CONSEQUENCE of the (1 - beta) convention:
       "a step size carried across from the other one" does not survive, and
       "Program P20 is where that has consequences".
  P15  OWNS THE ZIG-ZAG, measured on P10's bowl: 42.1 degrees off the way
       home, 20 crossings in 20 steps, 6.88 times as far travelled as moved.
       Its rigour box hands the FIX here by name and says why: the sideways
       components alternate in sign and cancel, the forward ones do not.
  P17  OWNS eta < 2/lambda_max, derived and then measured, plus the optimal
       eta = 0.095, the rate 0.905 and the 47 steps to 99% ON THE SAME BOWL.
       So the baseline of this program's comparison is already committed and
       is gated rather than recomputed.
       P17 ALSO OWNS THE RESCALING ARGUMENT -- w = c u leaves the function
       identical and multiplies the curvature by c^2 -- which turns out to be
       exactly the transformation the per-coordinate methods are invariant to.
       That is the sharpest available statement of what dividing by sqrt(v)
       buys, and it costs nothing because P17 has already done the work.
  P11  owns the condition number, which is the ratio of P17's two eigenvalues.
  P19  owns convexity, so "one basin" is an object the reader already has.
  P18  owns the gradient of the loss, so nothing here has to derive one.

WHAT P20 LEAVES ALONE, checked against tools/programs.json:
    minibatch noise, the linear scaling rule, clipping, accumulation  -> P21
    the multiplier as the price of a constraint                       -> P22
    what the variance of an estimator is                              -> P24

EXPERIMENT E6, which issue #34 names and which is free. SGD, momentum and Adam
on a quadratic of KNOWN condition number, iterations to tolerance AGAINST THE
PREDICTED COUNT. The prediction is the point: for a quadratic both classical
rates are known in closed form, so the measurement either confirms an
inequality derived two programs ago or refutes it, and P11's condition number
becomes a PREDICTION rather than a definition.

  plain descent at its best eta:   rate (k-1)/(k+1)
  momentum at its best eta, beta:  rate (sqrt(k)-1)/(sqrt(k)+1)

so momentum buys A SQUARE ROOT OF THE CONDITION NUMBER, which is a statement
about the problem rather than about the implementation.

Adam is NOT a linear method, so it has no such rate, and quoting one would be
inventing a number. What Adam does have is an INVARIANCE, and it is exactly
P17's rescaling: the script measures that instead, which is both honest and a
better argument than a rate comparison would have been.

Run:  python3 code/p20_gradient_descent.py      (or: make numbers)
"""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p20.tex"
TRANSCRIPTS = Path(__file__).resolve().parents[1] / "figures" / "transcripts"
VALUES: dict[str, tuple[str, bool]] = {}
NOTES: list[str] = []


def emit(key: str, value, digits: int | None = None) -> None:
    if isinstance(value, float) and digits is not None:
        body = f"{value:.{digits}f}"
    elif isinstance(value, float):
        body = repr(value)
    else:
        body = str(value)
    try:
        numeric = math.isfinite(float(body.replace("e", "E")))
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


def committed(fname: str, key: str) -> str | None:
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    import re
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def bound(x: float) -> str:
    """A residual is a property of the machine, so commit a CEILING it clears
    on any of them -- P06's rule, which CI enforced the hard way."""
    assert x >= 0.0
    return "0" if x == 0.0 else f"1e{math.ceil(math.log10(x)):d}"


# ---------------------------------------------------------------------------
# 0. THE BOWL. It is Program P10's, used by P15 and P17 and now by this
#    program, so all four are talking about ONE surface rather than four that
#    resemble each other. That is P04's rule for a cross-programme gate.
#
#        f(x, y) = (1/2)(LAM_HI x^2 + LAM_LO y^2),  grad = (LAM_HI x, LAM_LO y)
# ---------------------------------------------------------------------------
LAM_HI = 20.0
LAM_LO = 1.0
KAPPA = LAM_HI / LAM_LO

for _f, _k, _want in (("p10.tex", "p10.basin.hi", LAM_HI),
                      ("p10.tex", "p10.basin.lo", LAM_LO),
                      ("p15.tex", "p15.lam.hi", LAM_HI),
                      ("p15.tex", "p15.lam.lo", LAM_LO),
                      ("p17.tex", "p17.lam.hi", LAM_HI),
                      ("p17.tex", "p17.lam.lo", LAM_LO),
                      ("p17.tex", "p17.kappa", KAPPA)):
    _got = committed(_f, _k)
    if _got is not None:                       # gate, not a recomputation
        assert abs(float(_got) - _want) < 1e-9, (_f, _k, _got, _want)

emit("p20.lam.hi", LAM_HI, 0)
emit("p20.lam.lo", LAM_LO, 0)
emit("p20.kappa", KAPPA, 0)


def grad(w):
    return (LAM_HI * w[0], LAM_LO * w[1])


def dist(w):
    return math.hypot(w[0], w[1])


START = (1.0, 1.0)
TOL = 0.01                        # 99% of the way in, which is P17's target


def run(step, start=START, cap=100_000):
    """Iterate an update rule until the distance to the minimum falls under
    TOL of where it began. Returns the step count, or cap if it never does."""
    w, state, d0 = start, {}, dist(start)
    for k in range(1, cap + 1):
        w = step(w, grad(w), state, k)
        if not all(math.isfinite(c) for c in w):
            return cap                                       # diverged
        if dist(w) <= TOL * d0:
            return k
    return cap


# ---------------------------------------------------------------------------
# 1. PLAIN DESCENT, and the baseline that is ALREADY COMMITTED.
#
# The optimal step size for a quadratic balances the two extreme directions:
#     eta* = 2/(lambda_hi + lambda_lo),  rate = (k-1)/(k+1)
# P17 committed both. This gates against them rather than reporting them
# again, so the two programs cannot come apart about one walk.
# ---------------------------------------------------------------------------
def sgd(eta):
    def step(w, g, state, k):
        return (w[0] - eta * g[0], w[1] - eta * g[1])
    return step


ETA_BEST = 2.0 / (LAM_HI + LAM_LO)
RATE_SGD = (KAPPA - 1.0) / (KAPPA + 1.0)
_p17_eta = committed("p17.tex", "p17.best.eta")
_p17_rate = committed("p17.tex", "p17.rate")
if _p17_eta:
    assert abs(float(_p17_eta) - ETA_BEST) < 5e-4, (_p17_eta, ETA_BEST)
if _p17_rate:
    assert abs(float(_p17_rate) - RATE_SGD) < 5e-4, (_p17_rate, RATE_SGD)

STEPS_SGD = run(sgd(ETA_BEST))
PRED_SGD = math.ceil(math.log(TOL) / math.log(RATE_SGD))
# The prediction is the invariant; the measurement must MATCH it, not merely
# be close to it, because for a quadratic the rate is exact rather than
# asymptotic. One step of slack is the ceiling, nothing more.
assert abs(STEPS_SGD - PRED_SGD) <= 1, (STEPS_SGD, PRED_SGD)
_p17_steps = committed("p17.tex", "p17.steps.99")
if _p17_steps:
    assert abs(int(_p17_steps) - STEPS_SGD) <= 1, (_p17_steps, STEPS_SGD)

emit("p20.eta.best", ETA_BEST, 3)
emit("p20.rate.sgd", RATE_SGD, 3)
emit("p20.steps.sgd", STEPS_SGD)
emit("p20.pred.sgd", PRED_SGD)

# And the zig-zag P15 measured is the reason those steps are wasted. Recount
# the sign changes in the steep coordinate at this eta, so the two programs
# quote one walk rather than two.
_signs, _w = 0, START
_prev = _w[0]
_st = sgd(ETA_BEST)
for _k in range(1, 21):
    _w = _st(_w, grad(_w), {}, _k)
    if _w[0] * _prev < 0:
        _signs += 1
    _prev = _w[0]
assert _signs >= 15, _signs         # it alternates essentially every step
# P15 counted the same crossings on the same walk, so this is a GATE rather
# than a second copy of one number: printing it twice under two names would be
# Program F08's defect, and letting the two programs disagree would be worse.
_p15_cross = committed("p15.tex", "p15.zig.crossings")
if _p15_cross:
    assert int(_p15_cross) == _signs, (_p15_cross, _signs)


# ---------------------------------------------------------------------------
# 2. MOMENTUM. F04's average, with a gradient in it.
#
# The classical optimum for a quadratic (Polyak) is
#     beta = ((sqrt(k)-1)/(sqrt(k)+1))^2,  eta = (2/(sqrt(lo)+sqrt(hi)))^2
# with rate (sqrt(k)-1)/(sqrt(k)+1). THE SQUARE ROOT IS THE WHOLE STORY, and
# it is a statement about the problem's condition number rather than about any
# implementation, which is why it can be predicted before it is measured.
#
# Written in F04's form: v <- beta v + (1 - beta) g, and the (1 - beta) is
# folded back into the step size so that the two conventions give the SAME
# walk. That is F04's finding used rather than restated.
# ---------------------------------------------------------------------------
def heavy_ball(eta, beta):
    """v <- beta v + g;  w <- w - eta v.  The convention WITHOUT (1 - beta)."""
    def step(w, g, state, k):
        v = state.get("v", (0.0, 0.0))
        v = (beta * v[0] + g[0], beta * v[1] + g[1])
        state["v"] = v
        return (w[0] - eta * v[0], w[1] - eta * v[1])
    return step


def ema_momentum(eta, beta):
    """v <- beta v + (1 - beta) g;  w <- w - eta v.  F04's form."""
    def step(w, g, state, k):
        v = state.get("v", (0.0, 0.0))
        v = (beta * v[0] + (1 - beta) * g[0], beta * v[1] + (1 - beta) * g[1])
        state["v"] = v
        return (w[0] - eta * v[0], w[1] - eta * v[1])
    return step


SQK = math.sqrt(KAPPA)
BETA_BEST = ((SQK - 1.0) / (SQK + 1.0)) ** 2
ETA_MOM = (2.0 / (math.sqrt(LAM_LO) + math.sqrt(LAM_HI))) ** 2
RATE_MOM = (SQK - 1.0) / (SQK + 1.0)

STEPS_MOM = run(heavy_ball(ETA_MOM, BETA_BEST))
PRED_MOM = math.ceil(math.log(TOL) / math.log(RATE_MOM))
assert STEPS_MOM < STEPS_SGD, (STEPS_MOM, STEPS_SGD)

emit("p20.beta.best", BETA_BEST, 3)
emit("p20.eta.mom", ETA_MOM, 4)
emit("p20.rate.mom", RATE_MOM, 3)
emit("p20.steps.mom", STEPS_MOM)
emit("p20.pred.mom", PRED_MOM)
emit("p20.speedup", STEPS_SGD / STEPS_MOM, 1)
emit("p20.sqrt.kappa", SQK, 2)

# --- THE DRAFT ASSERTED |STEPS_MOM - PRED_MOM| <= 2 AND IT FAILED, 17 AGAINST
# 11, AND THE FAILURE IS THE SECTION. Two things are going on and both are
# checkable, so neither is left as an excuse:
#
#   (a) THE RATE IS ASYMPTOTIC. A step count to a fixed tolerance includes a
#       transient the rate says nothing about.
#   (b) AT THE OPTIMAL PARAMETERS THE TWO ROOTS OF THE ITERATION COINCIDE.
#       M_lambda = [[1 - eta*lambda, -eta*beta], [lambda, beta]] has
#       discriminant (1 - eta*lambda + beta)^2 - 4*beta, and Polyak's choice
#       sets it to ZERO in BOTH eigendirections at once -- which is what makes
#       it optimal. A repeated root with one eigenvector decays like
#       k * rho^k rather than rho^k, so the predicted rate is approached from
#       ABOVE and never quite attained.
#
# So what is asserted is the invariant rather than the count: the discriminant
# vanishes exactly, the measured tail decay tracks the predicted rate, and the
# advantage grows with the condition number towards -- but never past -- its
# square root.
def hb_discriminant(lam, eta, beta):
    a = 1.0 - eta * lam + beta
    return a * a - 4.0 * beta


for _lam in (LAM_HI, LAM_LO):
    assert abs(hb_discriminant(_lam, ETA_MOM, BETA_BEST)) < 1e-12, _lam
emit("p20.disc", 0)

_d, _w, _v = [], START, (0.0, 0.0)
for _k in range(1, 121):
    _g = grad(_w)
    _v = (BETA_BEST * _v[0] + _g[0], BETA_BEST * _v[1] + _g[1])
    _w = (_w[0] - ETA_MOM * _v[0], _w[1] - ETA_MOM * _v[1])
    _d.append(dist(_w))
TAIL = (_d[110] / _d[60]) ** (1.0 / 50.0)
assert abs(TAIL - RATE_MOM) < 0.01, (TAIL, RATE_MOM)
emit("p20.tail.rate", TAIL, 3)

# The overshoot, which is the part a reader does not expect and which the
# repeated root explains: the FIRST move is away from the minimum.
OVERSHOOT = max(_d[:5]) / dist(START)
assert OVERSHOOT > 1.0, OVERSHOOT
emit("p20.overshoot", OVERSHOOT, 2)
emit("p20.overshoot.pct", round(100 * (OVERSHOOT - 1)))

# And the comparison swept, because one bowl is an anecdote. Plain descent's
# prediction is EXACT at every condition number tried; momentum's is a floor
# it approaches. Stating both is more useful than reporting either.
SWEEP = (4.0, 9.0, 25.0, 100.0, 400.0, 1000.0)
_rows, _ratios = [], []
for _k in SWEEP:
    _hi, _lo = _k, 1.0
    _sq = math.sqrt(_k)
    _b = ((_sq - 1) / (_sq + 1)) ** 2
    _e = (2 / (math.sqrt(_lo) + math.sqrt(_hi))) ** 2

    def _mk(eta, beta, hi=_hi, lo=_lo):
        def step(w, g, state, k):
            v = state.get("v", (0.0, 0.0))
            v = (beta * v[0] + hi * w[0], beta * v[1] + lo * w[1])
            state["v"] = v
            return (w[0] - eta * v[0], w[1] - eta * v[1])
        return step

    def _run(step, cap=200_000):
        w, state, d0 = START, {}, dist(START)
        for k in range(1, cap + 1):
            w = step(w, None, state, k)
            if dist(w) <= TOL * d0:
                return k
        return cap

    _s = _run(_mk(2 / (_hi + _lo), 0.0))
    _m = _run(_mk(_e, _b))
    _ps = math.ceil(math.log(TOL) / math.log((_k - 1) / (_k + 1)))
    # PLAIN DESCENT'S PREDICTION IS EXACT, at every condition number.
    assert _s == _ps, (_k, _s, _ps)
    assert _m < _s, (_k, _m, _s)
    _ratios.append(_s / _m)
    _rows.append((_k, _s, _m, _s / _m, _sq))

assert _ratios == sorted(_ratios), _ratios            # the advantage GROWS
for _k, _s, _m, _r, _sq in _rows:
    assert _r < _sq, (_k, _r, _sq)                    # and is capped by sqrt
emit("p20.sweep.kappas", len(SWEEP))
emit("p20.sweep.k.lo", int(SWEEP[0]))
emit("p20.sweep.k.hi", int(SWEEP[-1]))
emit("p20.sweep.ratio.lo", _rows[0][3], 1)
emit("p20.sweep.ratio.hi", _rows[-1][3], 1)
emit("p20.sweep.sqrt.hi", _rows[-1][4], 1)
NOTES.append("plain descent's predicted step count is EXACT at all "
             f"{len(SWEEP)} condition numbers swept; momentum's is a floor it "
             f"approaches, and the measured advantage grows from "
             f"{_rows[0][3]:.1f}x at kappa {int(SWEEP[0])} to "
             f"{_rows[-1][3]:.1f}x at kappa {int(SWEEP[-1])}, against a "
             f"ceiling of {_rows[-1][4]:.1f}")

# THE (1 - beta) CONVENTION, MEASURED rather than argued, and at F04's own
# coefficient rather than at Polyak's, because 0.9 is the number people write.
# F04 establishes that the two forms give the same direction and differ in
# length by 1/(1 - beta) -- a factor of TEN at beta = 0.9 -- and hands the
# consequence here. The consequence has a direction: moving a step size from
# the normalised form to the un-normalised one multiplies it by ten, and ten
# times a working step size on this bowl is not a slower run, it is no run.
#
# A first draft asserted that carrying it across "takes more than three times
# as long". That is a threshold chosen so a claim would pass -- F11's failure
# mode, and P15's -- and it was FALSE at Polyak's beta, where the factor is
# only 1.67. What is asserted now is what is actually true and does not depend
# on a tolerance: rescaling reproduces the walk EXACTLY, and not rescaling
# leaves the bowl.
BETA_F04 = 0.9
ETA_F04 = 0.3
FOLD = 1.0 / (1.0 - BETA_F04)
# 1/(1 - 0.9) is 10.000000000000002 in binary64, which is Program P01's
# subject rather than this one's: the invariant is that the factor is ten in
# the algebra, so that is what is checked and what is printed.
assert abs(FOLD - 10.0) < 1e-9, FOLD

STEPS_EMA = run(ema_momentum(ETA_F04, BETA_F04))
STEPS_HB_RESCALED = run(heavy_ball(ETA_F04 / FOLD, BETA_F04))
STEPS_HB_CARRIED = run(heavy_ball(ETA_F04, BETA_F04))
CAP = 100_000

assert STEPS_EMA == STEPS_HB_RESCALED, (STEPS_EMA, STEPS_HB_RESCALED)
assert STEPS_HB_CARRIED == CAP, STEPS_HB_CARRIED        # it diverges
emit("p20.conv.beta", BETA_F04, 1)
emit("p20.conv.eta", ETA_F04, 1)
emit("p20.fold", FOLD, 0)
emit("p20.conv.same", STEPS_EMA)
NOTES.append(f"at beta = {BETA_F04} the two conventions differ by a factor of "
             f"{FOLD:.0f}: rescaling by it reproduces a {STEPS_EMA}-step walk "
             "exactly, and carrying the step size across unchanged diverges")


# ---------------------------------------------------------------------------
# 3. PER-COORDINATE SCALING, and the invariance that is the real argument.
#
# Adam divides each coordinate by the square root of a running average of its
# squared gradient. The units argument is the whole of it: g / sqrt(g^2) is
# DIMENSIONLESS, so the step is about eta whatever the gradient's size. Hence
# insensitivity to loss scaling, and hence the epsilon must sit OUTSIDE the
# root -- inside, it is added to a SQUARED quantity and its size means
# something different at every scale.
# ---------------------------------------------------------------------------
B1, B2, EPS = 0.9, 0.999, 1e-8


def adam(eta, b1=B1, b2=B2, eps=EPS, eps_inside=False):
    def step(w, g, state, k):
        m = state.get("m", (0.0, 0.0))
        v = state.get("v", (0.0, 0.0))
        m = tuple(b1 * mi + (1 - b1) * gi for mi, gi in zip(m, g))
        v = tuple(b2 * vi + (1 - b2) * gi * gi for vi, gi in zip(v, g))
        state["m"], state["v"] = m, v
        mh = tuple(mi / (1 - b1 ** k) for mi in m)           # F04's correction
        vh = tuple(vi / (1 - b2 ** k) for vi in v)
        if eps_inside:
            den = tuple(math.sqrt(vi + eps) for vi in vh)
        else:
            den = tuple(math.sqrt(vi) + eps for vi in vh)
        return tuple(wi - eta * mi / di for wi, mi, di in zip(w, mh, den))
    return step


# THE UNIT-STEP PROPERTY, measured on the first step from a cold start, where
# the bias correction makes m-hat and v-hat exactly g and g^2. The ratio is
# then g/(|g| + eps), so the step is eta EXACTLY in the limit of a large
# gradient -- and that is the claim: the size of the gradient cancels.
#
# --- A DRAFT ASSERTED THE STEP IS eta TO 1e-6 FOR EVERY GRADIENT AND IT
# FAILED, at |g| = 3e-6, where the step is 0.09967 rather than 0.1. The
# failure is the frame, because the shortfall is EXACTLY 1/(1 + eps/|g|):
# THE EPSILON IS WHERE THE UNIT-STEP PROPERTY STOPS. It is negligible for
# every gradient a training run sees and it is not an approximation -- it is
# an identity, so it can be checked rather than hedged.
ETA_ADAM = 0.1
SCALES = (1e-6, 1.0, 1e6)
_shortfalls = []
for _s in SCALES:
    _st, _state = adam(ETA_ADAM), {}
    _w = _st((0.0, 0.0), (_s * 3.0, -_s * 7.0), _state, 1)
    for _c, _g in zip(_w, (_s * 3.0, _s * 7.0)):
        predicted = ETA_ADAM / (1.0 + EPS / _g)
        assert abs(abs(_c) - predicted) < 1e-12, (_s, _c, predicted)
    _shortfalls.append(1.0 - abs(_w[0]) / ETA_ADAM)

# The step is within a part in a thousand of eta over twelve decades, and the
# only departure is the epsilon, which is largest where the gradient is
# smallest -- the opposite end from the one people worry about.
assert max(_shortfalls) < 4e-3, _shortfalls
assert _shortfalls == sorted(_shortfalls, reverse=True), _shortfalls
emit("p20.adam.eta", ETA_ADAM, 1)
emit("p20.adam.decades", 12)
emit("p20.adam.shortfall", 100 * max(_shortfalls), 2)
NOTES.append("Adam's first step is eta/(1 + eps/|g|) in every coordinate, so "
             f"over 12 decades of gradient it is within "
             f"{100 * max(_shortfalls):.2f} per cent of eta, and the epsilon "
             "is what accounts for all of the difference")

# THE EPSILON'S PLACE, measured, and the argument is a units argument.
# OUTSIDE the root it is added to sqrt(v), which has the units of a gradient,
# so it is compared with |g| and its effect is eps/|g|.
# INSIDE the root it is added to v, which is a gradient SQUARED, so it is
# compared with g^2 and its effect is eps/(2 g^2) -- which is not small when
# the gradient is small, and a small-gradient coordinate is exactly the one
# per-coordinate scaling exists to rescue.
#
# --- ANOTHER DRAFT ASSERTION FAILED HERE, that the outside form is scale-free
# to 1e-9. It is not: it is short by eps/|g|, which is a part in a hundred at
# a gradient of 1e-6. Measuring the two SHORTFALLS instead of asserting that
# one of them is zero produces a far stronger frame, because the same gradient
# that costs the outside form one per cent costs the inside form ninety-nine.
SHORT_G = 1e-6
_out = ETA_ADAM * SHORT_G / (math.sqrt(SHORT_G ** 2) + EPS)
_in = ETA_ADAM * SHORT_G / math.sqrt(SHORT_G ** 2 + EPS)
SHORT_OUT = 100.0 * (1.0 - _out / ETA_ADAM)
SHORT_IN = 100.0 * (1.0 - _in / ETA_ADAM)
# The closed forms, checked rather than quoted: eps/|g| and 1 - 1/sqrt(1+eps/g^2)
assert abs(SHORT_OUT - 100 * (EPS / SHORT_G) / (1 + EPS / SHORT_G)) < 1e-9
assert abs(SHORT_IN - 100 * (1 - 1 / math.sqrt(1 + EPS / SHORT_G ** 2))) < 1e-9
assert SHORT_IN > 50 * SHORT_OUT, (SHORT_IN, SHORT_OUT)

# And the invariant rather than either figure, because a claim about one
# gradient is an anecdote. Both shortfalls grow as the gradient falls; what
# separates them is that ACROSS THE WHOLE RANGE WHERE THE OUTSIDE FORM IS
# STILL UNDER ONE PER CENT, THE INSIDE FORM IS ALREADY LOSING MOST OF THE
# STEP. A first draft asserted the RATIO grows, and it does not -- the inside
# shortfall saturates below 100 per cent while the outside one keeps climbing,
# so the ratio peaks and falls. The ratio was never the claim.
_outs, _ins = [], []
for _g in (1e-3, 1e-4, 1e-5, 1e-6):
    _outs.append(1 - 1 / (1 + EPS / _g))
    _ins.append(1 - 1 / math.sqrt(1 + EPS / _g ** 2))
assert _outs == sorted(_outs), _outs                 # both grow as g falls
assert _ins == sorted(_ins), _ins
assert max(_outs) < 0.01, _outs                      # outside: still under 1%
assert min(_ins[1:]) > 0.25, _ins                    # inside: already gone
emit("p20.eps", "1e-8")
emit("p20.eps.g", "1e-6")
emit("p20.eps.short.out", SHORT_OUT, 2)
emit("p20.eps.short.in", SHORT_IN, 0)
NOTES.append(f"at a gradient of {SHORT_G:g} the epsilon costs "
             f"{SHORT_OUT:.2f} per cent of the step outside the root and "
             f"{SHORT_IN:.0f} per cent inside it, and the gap grows as the "
             "gradient falls")

# THE INVARIANCE, which is P17's rescaling used rather than restated.
# w = c u leaves the function identical and multiplies the curvature by c^2.
# Plain descent's step count changes; Adam's does not.
C = 10.0
_p17_c = committed("p17.tex", "p17.rescale.c")
if _p17_c:
    assert abs(float(_p17_c) - C) < 1e-9, (_p17_c, C)


def rescaled_grad(w):
    """The same bowl in coordinates where the steep axis is written w = c u:
    the loss is unchanged and its gradient in u picks up a factor of c^2."""
    return (LAM_HI * C * C * w[0], LAM_LO * w[1])


def run_g(step, gfun, start=START, cap=100_000):
    w, state, d0 = start, {}, dist(start)
    for k in range(1, cap + 1):
        w = step(w, gfun(w), state, k)
        if not all(math.isfinite(c) for c in w):
            return cap
        if dist(w) <= TOL * d0:
            return k
    return cap


CAP_RUN = 100_000
SGD_PLAIN = run_g(sgd(ETA_BEST), grad)
SGD_RESCALED = run_g(sgd(ETA_BEST), rescaled_grad)
ADAM_PLAIN = run_g(adam(ETA_ADAM), grad)
ADAM_RESCALED = run_g(adam(ETA_ADAM), rescaled_grad)

# The invariant, not the two figures: plain descent's answer MOVES under a
# reparameterisation that changes nothing about the function, and Adam's does
# not. Exact equality is asserted for Adam, because approximate equality here
# would be a threshold chosen to make a claim pass -- F11's failure mode.
assert ADAM_PLAIN == ADAM_RESCALED, (ADAM_PLAIN, ADAM_RESCALED)
# And plain descent does not merely slow down: the rescaling multiplies the
# steep curvature by c^2, so Program P17's own bound eta < 2/lambda_max is
# violated by a factor of c^2 and the walk LEAVES THE BOWL. That is a stronger
# statement than a step count and it is predicted before it is measured.
assert SGD_RESCALED == CAP_RUN, SGD_RESCALED
ETA_NEEDED = 2.0 / (LAM_HI * C * C)
assert ETA_BEST > ETA_NEEDED, (ETA_BEST, ETA_NEEDED)
SGD_FACTOR = ETA_BEST / ETA_NEEDED
# and the closed form, checked rather than quoted: the ratio is
#   [2/(hi+lo)] / [2/(c^2 hi)] = c^2 * hi/(hi+lo) = c^2 * kappa/(kappa+1),
# which is essentially c^2 for any bowl worth worrying about.
assert abs(SGD_FACTOR - C * C * KAPPA / (KAPPA + 1.0)) < 1e-9, SGD_FACTOR

emit("p20.rescale.c", C, 0)
emit("p20.rescale.csq", C * C, 0)
emit("p20.sgd.overshoot", SGD_FACTOR, 0)
emit("p20.adam.plain", ADAM_PLAIN)
emit("p20.adam.rescaled", ADAM_RESCALED)
NOTES.append(f"under Program P17's reparameterisation plain descent at the "
             f"same step size diverges -- it is {SGD_FACTOR:.0f} times past "
             f"P17's own bound -- while Adam takes {ADAM_PLAIN} steps in both "
             "coordinate systems, which is the invariance rather than a speed "
             "claim")


# ---------------------------------------------------------------------------
# 4. WEIGHT DECAY IS NOT L2 ONCE YOU DIVIDE BY A RUNNING SCALE.
#
# L2 adds lambda*w to the GRADIENT, so it goes through the adaptive
# denominator and its effective strength becomes lambda/sqrt(v) -- a different
# number for every coordinate and every step. Decoupled decay subtracts
# eta*lambda*w from the WEIGHT, after the adaptive part, so the strength is
# lambda for everybody. That is the whole of AdamW, and it is one line.
# ---------------------------------------------------------------------------
LAMBDA = 0.1
ETA_WD = 0.001
CURV = (1.0, 0.01)             # two coordinates, curvatures 100 apart
TARGET = (1.0, 1.0)            # and the same minimum, so only the scale differs


def data_grad(w):
    return tuple(a * (wi - ti) for a, wi, ti in zip(CURV, w, TARGET))


def adam_l2(eta, lam):
    base = adam(eta)
    def step(w, g, state, k):
        return base(w, tuple(gi + lam * wi for gi, wi in zip(g, w)), state, k)
    return step


def adamw(eta, lam):
    base = adam(eta)
    def step(w, g, state, k):
        w2 = base(w, g, state, k)
        return tuple(wi2 - eta * lam * wi for wi2, wi in zip(w2, w))
    return step


def settle(rule, lam, steps=200_000):
    """Run to equilibrium and report where each coordinate ends up. The
    penalty is measured by WHERE THE WEIGHT SETTLES, which is the only place
    a regularisation strength is observable, rather than by dividing lambda
    by lambda -- a first draft did exactly that and could not have failed."""
    w, state, r = TARGET, {}, rule(ETA_WD, lam)
    for k in range(1, steps + 1):
        w = r(w, data_grad(w), state, k)
    return w


W_L2 = settle(adam_l2, LAMBDA)
W_WD = settle(adamw, LAMBDA)
W_NONE = settle(adamw, 0.0)
for _c in W_NONE:                                    # sanity: it does settle
    assert abs(_c - 1.0) < 1e-4, W_NONE

# L2's equilibrium has a closed form, so it is checked rather than reported:
# a(w - t) + lambda w = 0 gives w = a t / (a + lambda), which depends on the
# CURVATURE. The same lambda therefore shrinks the two coordinates by
# different fractions, and it is the flat one that is nearly annihilated.
for _c, _a, _t in zip(W_L2, CURV, TARGET):
    assert abs(_c - _a * _t / (_a + LAMBDA)) < 1e-3, (_c, _a)

SHRINK_L2 = tuple(1.0 - c / t for c, t in zip(W_L2, TARGET))
SHRINK_WD = tuple(1.0 - c / t for c, t in zip(W_WD, TARGET))
L2_SPREAD = max(SHRINK_L2) / min(SHRINK_L2)
# Decoupled decay subtracts eta*lambda*w, which knows nothing about the
# gradient or the curvature, so both coordinates are pulled identically and
# both settle in the same place.
assert abs(W_WD[0] - W_WD[1]) < 1e-3, W_WD
assert L2_SPREAD > 5.0, (SHRINK_L2, L2_SPREAD)

emit("p20.wd.lambda", LAMBDA, 1)
emit("p20.wd.curvratio", int(CURV[0] / CURV[1]))
emit("p20.wd.l2.steep", W_L2[0], 3)
emit("p20.wd.l2.flat", W_L2[1], 3)
emit("p20.wd.l2.spread", L2_SPREAD, 1)
emit("p20.wd.decoupled", W_WD[0], 3)
emit("p20.wd.gap", bound(abs(W_WD[0] - W_WD[1])))
NOTES.append(f"with one lambda of {LAMBDA}, L2 settles the steep coordinate "
             f"at {W_L2[0]:.3f} and the flat one at {W_L2[1]:.3f} -- a factor "
             f"of {L2_SPREAD:.1f} in how hard the same penalty pulls -- while "
             f"decoupled decay settles both at {W_WD[0]:.3f}")

# And the other half of the AdamW argument, which is what makes it about
# ADAPTIVITY rather than about penalties: for PLAIN descent the two are the
# same update up to a rescaling, so there is nothing to decouple.
def sgd_l2(eta, lam):
    def step(w, g, state, k):
        return tuple(wi - eta * (gi + lam * wi) for wi, gi in zip(w, g))
    return step


def sgd_wd(eta, lam):
    def step(w, g, state, k):
        return tuple(wi - eta * gi - eta * lam * wi for wi, gi in zip(w, g))
    return step


_a = settle(sgd_l2, LAMBDA, steps=50_000)
_b = settle(sgd_wd, LAMBDA, steps=50_000)
assert max(abs(x - y) for x, y in zip(_a, _b)) < 1e-12, (_a, _b)
emit("p20.wd.sgd.gap", bound(max(abs(x - y) for x, y in zip(_a, _b))))
NOTES.append("for plain descent the two forms are the same update and settle "
             "in identical places, which is why the distinction is a fact "
             "about adaptive methods rather than about penalties")


# ---------------------------------------------------------------------------
# 5. SCHEDULES, described as what they do to the effective step.
#
# The trap the issue names in the reader's own voice: gamma=0.1 MULTIPLIES.
# ---------------------------------------------------------------------------
LR0 = 1e-3
GAMMA = 0.1
BOUNDARIES = 3
STEP_LR = LR0 * GAMMA ** BOUNDARIES
# 1e-3 * 0.1**3 is 1.0000000000000002e-06 in binary64 -- Program P01's subject
# rather than this one's, so the invariant is checked and the algebra printed.
assert abs(STEP_LR / 1e-6 - 1.0) < 1e-9, STEP_LR
# The misreading is a FLOOR where the schedule is a PRODUCT, and the two
# answers differ by five orders of magnitude, which is why "the model stopped
# learning at epoch 30" is the symptom rather than "it learned a bit slower".
assert GAMMA / STEP_LR > 1e4, (GAMMA, STEP_LR)
emit("p20.sched.lr0", "1e-3")
emit("p20.sched.gamma", GAMMA, 1)
emit("p20.sched.boundaries", BOUNDARIES)
emit("p20.sched.after", "1e-6")
emit("p20.sched.factor", int(round(GAMMA / STEP_LR)))

# Cosine, as a fraction of the peak at the halfway point -- which is the one
# number people are surprised by, because a cosine spends a long time near
# its ends and passes the midpoint at exactly half.
def cosine(t, total, peak=1.0):
    return peak * 0.5 * (1.0 + math.cos(math.pi * t / total))


TOTAL = 1000
assert abs(cosine(TOTAL // 2, TOTAL) - 0.5) < 1e-12
COS_QUARTER = cosine(TOTAL // 4, TOTAL)
COS_THREE = cosine(3 * TOTAL // 4, TOTAL)
assert abs(COS_QUARTER + COS_THREE - 1.0) < 1e-12       # symmetric about half
# The fraction of the run spent above HALF the peak learning rate: it is
# exactly half, by that symmetry, and a linear decay gives the same. What
# differs is the SHAPE at the two ends, not the area.
_above = sum(1 for t in range(TOTAL) if cosine(t, TOTAL) > 0.5)
assert abs(_above - TOTAL // 2) <= 1, (_above, TOTAL)
_area_cos = sum(cosine(t, TOTAL) for t in range(TOTAL)) / TOTAL
_area_lin = sum(1.0 - t / TOTAL for t in range(TOTAL)) / TOTAL
assert abs(_area_cos - _area_lin) < 1e-3, (_area_cos, _area_lin)
emit("p20.cos.quarter", COS_QUARTER, 3)
emit("p20.cos.area", _area_cos, 3)
emit("p20.cos.lin.gap", bound(abs(_area_cos - _area_lin)))
NOTES.append(f"a cosine schedule and a linear one spend the same total "
             f"budget -- {_area_cos:.3f} of the peak, agreeing to better than "
             f"{bound(abs(_area_cos - _area_lin))} -- and differ only in "
             "where they spend it")

# Warmup, and what it is for: the first Adam steps have almost no history in
# v, so the denominator is a poor estimate and the step is a full eta in a
# direction chosen by one gradient. Measure the spread of the second-moment
# estimate over the first steps against its settled value.
def vhat_after(steps, g=1.0, noise=(0.2, 5.0, 0.5, 3.0, 1.0)):
    v, out = 0.0, []
    for k in range(1, steps + 1):
        gk = g * noise[(k - 1) % len(noise)]
        v = B2 * v + (1 - B2) * gk * gk
        out.append(math.sqrt(v / (1 - B2 ** k)))
    return out


_vh = vhat_after(400)
EARLY = max(_vh[:10]) / min(_vh[:10])
LATE = max(_vh[300:]) / min(_vh[300:])
assert EARLY > 3 * LATE, (EARLY, LATE)
emit("p20.warm.early", EARLY, 2)
emit("p20.warm.late", LATE, 3)
NOTES.append(f"over the first ten steps Adam's scale estimate swings by "
             f"{EARLY:.2f}x and after three hundred by {LATE:.3f}x, which is "
             "what a warmup is protecting against")


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    # The rounding is written INTO the listing rather than applied to its
    # output, on P19's finding: a transcript showing a number the session does
    # not print is a fabricated console block whatever generated the file.
    lines = [
        ">>> from p20_gradient_descent import adam",
        ">>> tiny, huge = (3e-6, -7e-6), (3e6, -7e6)",
        ">>> step = adam(0.1)",
        ">>> [round(abs(c), 4) for c in step((0,0), tiny, {}, 1)]",
        f"{[round(abs(c), 4) for c in adam(0.1)((0.0, 0.0), (3e-6, -7e-6), {}, 1)]}",
        ">>> [round(abs(c), 4) for c in step((0,0), huge, {}, 1)]",
        f"{[round(abs(c), 4) for c in adam(0.1)((0.0, 0.0), (3e6, -7e6), {}, 1)]}",
    ]
    for line in lines:
        assert len(line) <= 64, (len(line), line)
    (TRANSCRIPTS / "p20-unit-step.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf8")

    out = [
        "% Generated by code/p20_gradient_descent.py --- do not edit.",
        "% Regenerate with `make numbers`; `make verify` fails if this file and",
        "% the script disagree, which is what stops a number in the book drifting",
        "% away from the computation that justifies it.",
        "",
    ] + [
        f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}"
        for k, (body, numeric) in VALUES.items()
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf8")

    w = max(len(k) for k in VALUES)
    items = list(VALUES.items())
    for i in range(0, len(items), 3):
        print("  " + "   ".join(f"{k:{w}s} {b:>10s}"
                                for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
