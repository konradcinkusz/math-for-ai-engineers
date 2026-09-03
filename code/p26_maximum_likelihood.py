"""P26 --- Estimation and maximum likelihood.

Every number Program P26 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT, read before a line of this was written.
The estimate in the manifest is 55 frames; what is left after the reading is
narrower than that and better, because five written programs each deliver one
of this program's ingredients and say so.

  P21  OWNS unbiasedness outright: the definition, the exact proof over every
       subset of a population, and the trapbox saying unbiased is not enough.
       So this program may NOT re-teach it -- it owes the SECOND axis, and the
       decomposition that puts the two together.
       P21 also defers TWO things here by name.  Its section 8 says the
       score-function and reparameterised estimators are "a line of algebra
       that Programs P24 and P26 are better placed to give".  P24 did not give
       it.  Section 6 does, and it is the same object maximum likelihood
       differentiates -- so it costs this program four lines rather than a
       section.
  P24  OWNS the random variable, the expectation and the variance with its two
       routes.  Nothing here re-derives any of them.
  P25  OWNS the 1/n rate and the evaluation sizing.  A variance of an estimator
       is quoted from there, never recomputed.
  P18  gives cross-entropy a DEFINITIONAL frame and says in as many words that
       "why it is the right thing to minimise is Program P26's".  Section 4 is
       the frame that returns it.  P18 also owns the p - y gradient in full, so
       this program owes the justification and never the derivative.
  P20  OWNS weight decay outright, including the measured L2-against-decoupled
       equilibrium at lambda = 0.1.  Section 5 therefore says what that lambda
       IS rather than what it does: the log of a Gaussian prior.  It matches
       P20's own convention -- L2 adds lambda*w to the GRADIENT -- rather than
       a formula quoted from memory, which is the trap F04 recorded.
  P19  OWNS Jensen and states the concave case explicitly.  Section 2's second
       finding is that inequality applied to a square root, not a new theorem.
  F03  already prints ln p(sequence) = sum_i ln p_i and computes a sequence
       probability from F02's loss of 2.4 nats.  Section 4 runs that chain
       BACKWARDS and gates on it, which makes three programs one computation.
  F02  owns the loss itself.
  P15  supplies the gradient that finds a maximum.

WHAT THIS PROGRAM MUST NOT SPEND.
  P27  owns the bootstrap, the paired test, the p-value, multiple comparisons
       and the power calculation.  Section 1 stops at an estimator's two ways
       of being wrong and never asks whether a difference is real.
  P28  owns the POSTERIOR as a distribution, conjugacy and credible intervals.
       Section 5's MAP is a point estimate and says so.
  P30  owns KL and closes the loop the other way round.

Run:  python3 code/p26_maximum_likelihood.py
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p26.tex"
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
    """Another program's committed value, read back so the two cannot drift."""
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


def pct(x: float) -> float:
    """A percentage, refusing the two values that read as exact and are not.

    Program P05 met this at the top of the range and Program P21 at the
    bottom: a quantity that rounds to 0 or to 100 must be reported as a count
    or as its complement, where every figure means something."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not. "
        f"Report the count or the complement instead.")
    return x


# ======================================================================
# 1.  An estimator is a function of the sample, and there are two ways to
#     be wrong.
#
# Program P21 proved unbiasedness exactly over every subset of a population
# and then said, in its own trapbox, that unbiased is not enough.  This is
# what it is not enough OF.  Everything below is exact over Fraction: there
# is no tolerance anywhere in this section, because every statement in it is
# an identity rather than a measurement.
# ======================================================================

POP = (Fraction(1), Fraction(2), Fraction(3), Fraction(6))
N_DRAW = 2

POP_MEAN = sum(POP) / len(POP)
POP_VAR = sum((x - POP_MEAN) ** 2 for x in POP) / len(POP)
assert POP_MEAN == 3 and POP_VAR == Fraction(7, 2), (POP_MEAN, POP_VAR)

# Every sample of size N_DRAW, drawn independently -- which is the model a
# minibatch actually is, so the samples are WITH replacement.
SAMPLES = list(product(POP, repeat=N_DRAW))
assert len(SAMPLES) == len(POP) ** N_DRAW


def mse_of_shrunk(c: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    """(bias, variance, mean squared error) of c * sample_mean, exactly."""
    ests = [c * (sum(s) / len(s)) for s in SAMPLES]
    mean_est = sum(ests) / len(ests)
    bias = mean_est - POP_MEAN
    var = sum((e - mean_est) ** 2 for e in ests) / len(ests)
    mse = sum((e - POP_MEAN) ** 2 for e in ests) / len(ests)
    return bias, var, mse


# The decomposition itself, asserted as the identity it is rather than
# checked at one convenient c.
for _num in range(0, 21):
    _c = Fraction(_num, 10)
    _b, _v, _m = mse_of_shrunk(_c)
    assert _m == _b ** 2 + _v, (_c, _m, _b, _v)

BIAS_1, VAR_1, MSE_1 = mse_of_shrunk(Fraction(1))
assert BIAS_1 == 0, "the sample mean is unbiased -- P21's own result"
assert VAR_1 == POP_VAR / N_DRAW, "and its variance is sigma^2/n -- P25's rate"

# The shrinkage that minimises the mean squared error.  d/dc of
# mu^2 (c-1)^2 + c^2 sigma^2/n vanishes at mu^2 / (mu^2 + sigma^2/n), and the
# script finds it by exact search rather than by quoting that.
BEST_C, BEST_MSE = None, None
for _num in range(0, 1001):
    _c = Fraction(_num, 1000)
    _, _, _m = mse_of_shrunk(_c)
    if BEST_MSE is None or _m < BEST_MSE:
        BEST_C, BEST_MSE = _c, _m
_closed = POP_MEAN ** 2 / (POP_MEAN ** 2 + POP_VAR / N_DRAW)
assert abs(BEST_C - _closed) <= Fraction(1, 1000), (BEST_C, _closed)

# THE POINT, and it failed as first written.  The draft asserted the biased
# estimator beats the unbiased one "by a third"; it is nothing like a third,
# and a threshold picked so a claim passes is what Programs F11, P15, P20 and
# P21 each paid for.  What is asserted is the ORDERING, which is structural.
assert BEST_MSE < MSE_1, (BEST_MSE, MSE_1)
SHRINK_GAIN = float(1 - BEST_MSE / MSE_1)

BIAS_BEST, VAR_BEST, _ = mse_of_shrunk(BEST_C)

emit("p26.pop.n", len(POP))
emit("p26.pop.mean", int(POP_MEAN))
emit("p26.pop.var", float(POP_VAR), 2)
emit("p26.draw.n", N_DRAW)
emit("p26.samples", len(SAMPLES))
emit("p26.mse.unbiased", float(MSE_1), 3)
emit("p26.shrink.c", float(BEST_C), 3)
emit("p26.mse.shrunk", float(BEST_MSE), 3)
emit("p26.shrink.gain.pct", pct(100 * SHRINK_GAIN), 1)
emit("p26.shrink.bias", float(BIAS_BEST), 3)
emit("p26.shrink.var", float(VAR_BEST), 3)
emit("p26.var.unbiased", float(VAR_1), 2)

NOTES.append(
    f"MSE = bias^2 + variance holds EXACTLY at all 21 shrinkages tried, over "
    f"fractions; and the best shrinkage {float(BEST_C):.3f} beats the unbiased "
    f"estimator by {100 * SHRINK_GAIN:.1f} per cent of its MSE -- so 'unbiased' "
    f"and 'best' are different words")

# The page prints the two mean squared errors and then their gap as a
# percentage.  Programs F04, F05, P07, P12 and P23 each paid for this: divide
# the two numbers AS THE PAGE PRINTS THEM before writing the sentence.
_shown = 100 * (1 - float(f"{float(BEST_MSE):.3f}") / float(f"{float(MSE_1):.3f}"))
assert f"{_shown:.1f}" == f"{100 * SHRINK_GAIN:.1f}", (_shown, 100 * SHRINK_GAIN)
# And the decomposition has to reproduce from the page too.
assert (f"{float(BIAS_BEST) ** 2 + float(VAR_BEST):.3f}"
        == f"{float(BEST_MSE):.3f}"), "bias^2 + variance must add up as printed"


# ======================================================================
# 2.  The n - 1, computed rather than quoted.
#
# Everybody knows the correction and almost nobody can say what it corrects.
# It is a bias, it is exactly (n-1)/n, and it is provable by enumeration on a
# finite population -- which is a PROOF for that population rather than
# evidence about it, Program P14's distinction doing a second job.
# ======================================================================


def sample_variances(n: int) -> tuple[Fraction, Fraction]:
    """Mean over every sample of size n of the n- and (n-1)-denominator
    sample variances, exactly."""
    tot_n = Fraction(0)
    tot_n1 = Fraction(0)
    samples = list(product(POP, repeat=n))
    for s in samples:
        bar = sum(s) / n
        ss = sum((x - bar) ** 2 for x in s)
        tot_n += ss / n
        tot_n1 += ss / (n - 1)
    return tot_n / len(samples), tot_n1 / len(samples)


for _n in (2, 3, 4, 5):
    _en, _en1 = sample_variances(_n)
    assert _en == Fraction(_n - 1, _n) * POP_VAR, (_n, _en)
    assert _en1 == POP_VAR, (_n, _en1)

E_VAR_N, E_VAR_N1 = sample_variances(N_DRAW)
UNDERSTATE_PCT = pct(100 * float(1 - E_VAR_N / POP_VAR))

# And now the half nobody says.  Correcting the VARIANCE does not correct the
# STANDARD DEVIATION, because a square root is not linear -- which is exactly
# Program P19's Jensen inequality for a concave function, and P19 states the
# concave case in as many words.  So the corrected sample standard deviation
# is STILL biased, downwards, and the shortfall is worth a number.
def mean_sample_sd(n: int) -> float:
    samples = list(product(POP, repeat=n))
    tot = 0.0
    for s in samples:
        bar = sum(s) / n
        ss = sum((x - bar) ** 2 for x in s)
        tot += math.sqrt(float(ss / (n - 1)))
    return tot / len(samples)


POP_SD = math.sqrt(float(POP_VAR))
SD_ROWS = []
for _n in (2, 3, 5, 10):
    _m = mean_sample_sd(_n)
    # Jensen, and it is strict here because the sample variance is not
    # constant across samples.  An assertion that could not fail would be
    # Program P05's "finding nothing is not measuring nothing".
    assert _m < POP_SD, (_n, _m, POP_SD)
    SD_ROWS.append((_n, _m, 100 * (1 - _m / POP_SD)))
# The shortfall must shrink with n -- structural, so it is what is asserted
# rather than any one figure.
assert all(SD_ROWS[i][2] > SD_ROWS[i + 1][2] for i in range(len(SD_ROWS) - 1)), \
    SD_ROWS

emit("p26.var.n.expected", float(E_VAR_N), 2)
emit("p26.var.n1.expected", float(E_VAR_N1), 2)
emit("p26.var.understate.pct", UNDERSTATE_PCT, 0)
emit("p26.pop.sd", POP_SD, 4)
for _n, _m, _short in SD_ROWS:
    emit(f"p26.sd.mean.{_n}", _m, 4)
    emit(f"p26.sd.short.{_n}", pct(_short), 1)

NOTES.append(
    f"the n-denominator sample variance is short by EXACTLY (n-1)/n of the "
    f"population variance, enumerated at n = 2, 3, 4 and 5 over fractions -- "
    f"and the (n-1) denominator is exactly right, which is the whole of what "
    f"the correction corrects")
NOTES.append(
    f"but it corrects the VARIANCE and not the standard deviation: the "
    f"corrected sample sd averages {SD_ROWS[0][1]:.4f} against a population "
    f"{POP_SD:.4f} at n = 2, short by {SD_ROWS[0][2]:.1f} per cent, falling to "
    f"{SD_ROWS[-1][2]:.1f} per cent at n = {SD_ROWS[-1][0]}. That is Program "
    f"P19's Jensen for a concave function, and ddof=1 does not fix it")


# ======================================================================
# 3.  Maximum likelihood: the parameter that makes the data least surprising.
#
# The whole derivation is Program F03's logarithm turning a product into a
# sum, and Program P15's gradient finding where a maximum is.  Nothing here
# is new machinery; what is new is the object.
# ======================================================================

TRIALS, SUCCESSES = 20, 7


def bernoulli_loglik(p: Fraction) -> Fraction:
    """log-likelihood, up to the constant that does not depend on p -- and it
    is returned as the two EXPONENTS rather than a logarithm, so the
    comparison below is exact.  Comparing p^k (1-p)^(n-k) directly is the
    same ordering, because ln is strictly increasing (Program F05)."""
    return p ** SUCCESSES * (1 - p) ** (TRIALS - SUCCESSES)


MLE_P = Fraction(SUCCESSES, TRIALS)
# The estimating equation, exactly: k/p - (n-k)/(1-p) = 0 at p = k/n.
_score = SUCCESSES / MLE_P - (TRIALS - SUCCESSES) / (1 - MLE_P)
assert _score == 0, _score
# And it really is the maximum, not merely a stationary point: checked
# against a grid rather than by quoting the second derivative.
for _num in range(1, 1000):
    _p = Fraction(_num, 1000)
    if _p != MLE_P:
        assert bernoulli_loglik(_p) < bernoulli_loglik(MLE_P), _p

# The Gaussian MLE, and the collision this program is built around: its
# variance carries the n denominator, which section 2 just proved is biased.
GAUSS_SAMPLE = (Fraction(2), Fraction(4), Fraction(4), Fraction(4),
                Fraction(5), Fraction(5), Fraction(7), Fraction(9))
_n = len(GAUSS_SAMPLE)
MLE_MU = sum(GAUSS_SAMPLE) / _n
MLE_SIGMA2 = sum((x - MLE_MU) ** 2 for x in GAUSS_SAMPLE) / _n
UNBIASED_SIGMA2 = sum((x - MLE_MU) ** 2 for x in GAUSS_SAMPLE) / (_n - 1)
assert MLE_SIGMA2 == Fraction(_n - 1, _n) * UNBIASED_SIGMA2
assert MLE_MU == 5 and MLE_SIGMA2 == 4, (MLE_MU, MLE_SIGMA2)

# The frame writes "twenty trials give seven successes" in words, so
# emitting the two counts would be a second copy nobody would correct
# -- Program F11's finding, and F02's rule about a clause that would
# otherwise start with a digit.
emit("p26.bern.mle", float(MLE_P), 2)
emit("p26.gauss.n", _n)
emit("p26.gauss.mu", int(MLE_MU))
emit("p26.gauss.mle.var", int(MLE_SIGMA2))
emit("p26.gauss.unbiased.var", float(UNBIASED_SIGMA2), 3)

NOTES.append(
    f"the Bernoulli MLE is k/n = {float(MLE_P):.2f}, with the estimating "
    f"equation exactly zero there over fractions and every other p on a "
    f"thousand-point grid strictly worse -- so it is the maximum rather than a "
    f"stationary point")
NOTES.append(
    f"and the Gaussian MLE's variance is {int(MLE_SIGMA2)} against the "
    f"unbiased {float(UNBIASED_SIGMA2):.3f}: MAXIMUM LIKELIHOOD IS NOT "
    f"UNBIASED, and the factor is section 2's (n-1)/n exactly")


# ======================================================================
# 4.  Training a language model is maximum likelihood.
#
# The payoff, and the frame that returns Program P18's forward reference.
# The chain runs F02 -> F03 -> here and the gate below runs it backwards,
# which makes three programs one computation rather than three that agree.
# ======================================================================

F02_LOSS = float(committed("f02.tex", "f02.loss.nats") or "nan")
F03_TOKENS = int(committed("f03.tex", "f03.seq.tokens") or 0)
F03_LOG10 = float(committed("f03.tex", "f03.seq.prod.log10") or "nan")
assert F03_TOKENS and math.isfinite(F02_LOSS) and math.isfinite(F03_LOG10)

# Forwards: F02's per-token loss, F03's token count, F03's committed exponent.
_log10 = F03_TOKENS * math.log10(math.exp(-F02_LOSS))
assert f"{_log10:.2f}" == f"{F03_LOG10:.2f}", (_log10, F03_LOG10)
# Backwards, which is what this section is: divide a log-likelihood by the
# token count and negate, and the cross-entropy loss comes back.  The
# tolerance is not chosen -- it is what rounding F03's exponent to three
# decimals can account for, and nothing wider.
BACK_LOSS = -F03_LOG10 * math.log(10) / F03_TOKENS
_rounding_slack = 0.0005 * math.log(10) / F03_TOKENS
assert abs(BACK_LOSS - F02_LOSS) <= _rounding_slack, (BACK_LOSS, F02_LOSS)

# Label smoothing, which is maximum likelihood against a different target.
# For one example the loss -sum_j t_j ln p_j over the simplex is minimised at
# p = t, so a smoothed target names a FINITE optimal logit gap where the
# one-hot target names an infinite one.  Found by search, not quoted.
CLASSES, EPS = 8, 0.1
SMOOTH_TRUE = 1 - EPS * (CLASSES - 1) / CLASSES
SMOOTH_OTHER = EPS / CLASSES
assert abs(SMOOTH_TRUE + (CLASSES - 1) * SMOOTH_OTHER - 1) < 1e-12


def smoothed_loss(p_true: float) -> float:
    p_other = (1 - p_true) / (CLASSES - 1)
    return -(SMOOTH_TRUE * math.log(p_true)
             + (CLASSES - 1) * SMOOTH_OTHER * math.log(p_other))


_best, _arg = None, None
for _i in range(1, 100000):
    _p = _i / 100000
    _l = smoothed_loss(_p)
    if _best is None or _l < _best:
        _best, _arg = _l, _p
assert abs(_arg - SMOOTH_TRUE) < 1e-4, (_arg, SMOOTH_TRUE)
SMOOTH_GAP = math.log(SMOOTH_TRUE / SMOOTH_OTHER)

emit("p26.f02.loss", F02_LOSS, 1)
emit("p26.f03.tokens", F03_TOKENS)
emit("p26.back.loss", BACK_LOSS, 3)
emit("p26.ls.classes", CLASSES)
emit("p26.ls.eps", EPS, 1)
emit("p26.ls.true", SMOOTH_TRUE, 4)
emit("p26.ls.other", SMOOTH_OTHER, 4)
emit("p26.ls.gap", SMOOTH_GAP, 2)

NOTES.append(
    f"F02's loss of {F02_LOSS} nats and F03's {F03_TOKENS}-token sequence "
    f"reconstruct each other in both directions: forwards to F03's committed "
    f"exponent {F03_LOG10} to the printed digit, backwards to "
    f"{BACK_LOSS:.4f} nats within what rounding that exponent can account for")
NOTES.append(
    f"label smoothing at eps = {EPS} over {CLASSES} classes wants "
    f"{SMOOTH_TRUE:.4f} on the true class and {SMOOTH_OTHER:.4f} on each "
    f"other, so the optimal logit gap is {SMOOTH_GAP:.2f} -- FINITE, where a "
    f"one-hot target's optimum is unattainable")


# ======================================================================
# 5.  MAP is maximum likelihood with a prior, and that prior is weight decay.
#
# Program P20 owns weight decay and MEASURED what its lambda does.  This says
# what it IS.  The correspondence depends on a convention -- whether the
# penalty is lambda*||w||^2 or half of it -- so it is settled by matching the
# GRADIENTS P20 actually adds, never by quoting a formula.  That is the trap
# Program F04 recorded about momentum, and it is the same trap.
# ======================================================================

P20_LAMBDA = float(committed("p20.tex", "p20.wd.lambda") or "nan")
assert math.isfinite(P20_LAMBDA) and P20_LAMBDA > 0

# P20's own comment: "L2 adds lambda*w to the GRADIENT".  A Gaussian prior of
# width tau contributes -ln prior = ||w||^2 / (2 tau^2) + const to the
# objective, whose gradient is w / tau^2.  Match those two and tau follows.
PRIOR_TAU = 1.0 / math.sqrt(P20_LAMBDA)
for _w in (-3.0, -0.25, 0.0, 0.75, 4.0):
    penalty_grad = P20_LAMBDA * _w
    prior_grad = _w / PRIOR_TAU ** 2
    assert abs(penalty_grad - prior_grad) < 1e-12, (_w, penalty_grad, prior_grad)

# The sentence that buys: a weight decay is a claim about how large the
# weights are believed to be, and it is checkable.  Two decades of lambda
# either side, so the reader can see it is a width rather than a strength.
TAU_ROWS = [(l, 1.0 / math.sqrt(l)) for l in (0.001, 0.01, P20_LAMBDA, 1.0)]
assert all(TAU_ROWS[i][1] > TAU_ROWS[i + 1][1] for i in range(len(TAU_ROWS) - 1))

emit("p26.p20.lambda", P20_LAMBDA, 1)
emit("p26.prior.tau", PRIOR_TAU, 3)
for _l, _t in TAU_ROWS:
    emit(f"p26.tau.{str(_l).replace('.', '')}", _t, 2)

NOTES.append(
    f"P20's weight decay of lambda = {P20_LAMBDA} is exactly a Gaussian prior "
    f"of width {PRIOR_TAU:.3f} on every weight -- matched on the GRADIENTS P20 "
    f"adds rather than on a formula, at five values of w")


# ======================================================================
# 6.  The score, and the estimator Program P21 could not derive.
#
# P21 measured two ways of differentiating through a draw and said both were
# "a line of algebra that Programs P24 and P26 are better placed to give".
# P24 did not give it.  It is one line, it is the same object maximum
# likelihood sets to zero, and both halves below are exact over fractions.
# ======================================================================

SCORE_PS = [Fraction(k, 10) for k in range(1, 10)]


def bernoulli_score(x: int, p: Fraction) -> Fraction:
    """d/dp of log p(x | p) for x in {0, 1}, exactly."""
    return Fraction(1, 1) / p if x == 1 else Fraction(-1, 1) / (1 - p)


# (a) The score has expectation zero -- which is WHY the estimating equation
#     in section 3 is the thing to set to zero, rather than a convenience.
for _p in SCORE_PS:
    _e = _p * bernoulli_score(1, _p) + (1 - _p) * bernoulli_score(0, _p)
    assert _e == 0, (_p, _e)

# (b) grad E[f] = E[f * score], which IS the score-function estimator.
#     Checked against the derivative computed the other way, exactly: for a
#     Bernoulli, E[f] = p f(1) + (1-p) f(0), so d/dp is f(1) - f(0).
F_CASES = [(Fraction(3), Fraction(-1)), (Fraction(0), Fraction(7)),
           (Fraction(5, 2), Fraction(5, 2))]
for _f1, _f0 in F_CASES:
    direct = _f1 - _f0
    for _p in SCORE_PS:
        via_score = (_p * _f1 * bernoulli_score(1, _p)
                     + (1 - _p) * _f0 * bernoulli_score(0, _p))
        assert via_score == direct, (_f1, _f0, _p, via_score, direct)

emit("p26.score.ps", len(SCORE_PS))
emit("p26.score.cases", len(F_CASES))

NOTES.append(
    f"the score has expectation EXACTLY zero at all {len(SCORE_PS)} rates "
    f"tried, over fractions -- which is why the estimating equation is the "
    f"thing to set to zero -- and grad E[f] = E[f * score] reproduces the "
    f"derivative taken the other way exactly, at every rate and all "
    f"{len(F_CASES)} functions. That is P21's score-function estimator, "
    f"returned")


# ======================================================================
# The listing.  Section 2's finding is the one a reader will disbelieve, so
# it is the one they get to paste: the (n-1) denominator fixes the variance
# and leaves the standard deviation short.  Every rounding is INSIDE the
# listing rather than applied to its output -- Programs P19 and P24 each
# shipped a draft where it was not, and a session prints what a session
# prints.
TRANSCRIPT = Path(__file__).resolve().parent.parent / "figures" / "transcripts"
_lines = [
    ">>> from p26_maximum_likelihood import sample_variances, POP_VAR",
    ">>> en, en1 = sample_variances(2)",
    ">>> en == POP_VAR, en1 == POP_VAR",
    repr((E_VAR_N == POP_VAR, E_VAR_N1 == POP_VAR)),
    ">>> from p26_maximum_likelihood import mean_sample_sd, POP_SD",
    ">>> round(mean_sample_sd(2), 4), round(POP_SD, 4)",
    repr((round(mean_sample_sd(2), 4), round(POP_SD, 4))),
]
assert max(len(l) for l in _lines) <= 64, max(_lines, key=len)
(TRANSCRIPT / "p26-still-short.txt").write_text(
    "\n".join(_lines) + "\n", encoding="utf8")


# ======================================================================
OUT.write_text(
    "% Generated by code/p26_maximum_likelihood.py --- do not edit.\n"
    "% Regenerate with `make numbers`; `make verify` fails if this file and\n"
    "% the script disagree, which is what stops a number in the book drifting\n"
    "% away from the computation that justifies it.\n\n"
    + "".join(f"\\mfaval{{{k}}}{{{v}}}\n" if numeric
             else f"\\mfavaltext{{{k}}}{{{v}}}\n"
             for k, (v, numeric) in VALUES.items()),
    encoding="utf8")
print(f"P26: {len(VALUES)} values -> {OUT}")
for note in NOTES:
    print(f"  * {note}")
