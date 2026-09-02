"""P28 --- Bayesian inference.

Every number Program P28 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT, read before a line of this was written.
The brief lists six things and they were ticked off one at a time against the
written neighbours, which is the discipline that made P27 come in at
thirty-nine frames against sixty.  Here the answer is different: FOUR OF THE
SIX ARE OWED IN FULL, so this program lands near its estimate.

  P23  OWNS Bayes' theorem, conditioning, the base rate, and -- the piece this
       program actually builds on -- the ODDS form:
           posterior odds = prior odds x likelihood ratio
       That is Bayes for TWO hypotheses.  Section 1's move is to notice the
       reader has already computed a posterior and to put the same theorem on
       a CONTINUUM of hypotheses instead.  So the theorem is not re-derived
       here; only the object it acts on changes.  Section 6 uses the odds form
       again, unchanged, to price a miscalibrated judge.
  P26  OWNS the estimator, maximum likelihood and the MAP, and says in as many
       words that a MAP "cannot say how sure it is, cannot say whether the
       maximum was sharp or nearly flat, and cannot be propagated" -- naming
       this program for "a distribution over the parameter rather than a
       point, with credible intervals and the arithmetic that makes them
       computable".  So P28 owes the DISTRIBUTION, never the arithmetic that
       finds its mode.
  P27  §4 hands over "the probability that B is better" BY NAME, saying flatly
       that no p-value answers it and that P28 computes it.  The motivation is
       therefore already on the page and the reader has felt the gap: this
       program's first job is to answer a question already asked.
       §2 also built and MEASURED one side of the credible/confidence contrast
       the brief asks for -- the interval on 143 of 200 -- so section 3 quotes
       it rather than inventing a second example, and gates on it.
       §1's grid of 0.5 points per item is the yardstick section 3 uses to say
       how much the two intervals differ BY.
  P24  owns the random variable and the expectation.
  P12  owns the binomial coefficient, which is the whole of the exact
       arithmetic here.
  P19  owns Jensen, used once in section 6.

WHAT THIS PROGRAM MUST NOT SPEND.
  P30  owns KL and cross-entropy.  Section 6 prices a miscalibrated judge in
       ODDS, using P23's form, and never in nats -- the information-theoretic
       reading of the same defect is P30's and section 6 says so.
  P34  owns evaluation design end to end.

Run:  python3 code/p28_bayesian_inference.py
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from math import comb, exp, factorial, lgamma
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p28.tex"
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
    """Program P05's and P21's guard: a percentage that rounds to 0 or to 100
    reads as exact and is not.  Report the count or the complement."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Program P27's guard: can the reader redo this on the page in front of
    them?  Formats the operands as the page will, applies the operation to
    THOSE, and compares printed forms."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


# ======================================================================
# The exact machinery.  A Beta with INTEGER parameters has a polynomial
# density, so every quantity this program prints is a rational number and is
# computed as one -- no quadrature, no sampling, no tolerance.  That is
# deliberate: the claims in sections 2 to 5 are identities, and Program P24's
# rule is that a sampled check of an identity demonstrates it is approximately
# true, which is the reading these sections exist to refuse.
# ======================================================================

def beta_cdf(a: int, b: int, x: Fraction) -> Fraction:
    """P(theta <= x) for Beta(a, b), exactly, for integer a and b.

    The regularised incomplete beta with integer parameters is a finite
    binomial sum -- Program P12's coefficient, and nothing else."""
    n = a + b - 1
    return sum(Fraction(comb(n, k)) * x ** k * (1 - x) ** (n - k)
               for k in range(a, n + 1))


def beta_mean(a: int, b: int) -> Fraction:
    return Fraction(a, a + b)


def beta_quantile(a: int, b: int, q: Fraction, steps: int = 60) -> float:
    """The q-quantile, by bisection on the exact CDF."""
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(steps):
        mid = (lo + hi) / 2
        if beta_cdf(a, b, mid) < q:
            lo = mid
        else:
            hi = mid
    return float((lo + hi) / 2)


def p_greater_exact(a1: int, b1: int, a2: int, b2: int) -> Fraction:
    """P(X > Y) for independent X ~ Beta(a1,b1), Y ~ Beta(a2,b2), exactly.

    Both densities are polynomials, so the double integral is rational:
    integrate f_X(x) F_Y(x) over [0,1] term by term, using
    int_0^1 x^(p-1) (1-x)^(q-1) dx = B(p, q).

    EXACT, and therefore SMALL PARAMETERS ONLY.  At the two hundred items an
    evaluation actually has, the factorials run to six hundred digits and
    every Fraction normalises with a gcd on them; a first version of this file
    was killed by the machine rather than merely being slow.  Program P19's
    accidental quadratic was a hoisting error and this is not -- it is the
    cost of exactness itself, and the answer is not to make it faster but to
    notice that exactness is only warranted where the CLAIM is an identity.
    P(B is better) at n = 200 is a measurement reported to two significant
    figures, so it goes through the float version below."""
    n = a2 + b2 - 1
    inv_B1 = Fraction(factorial(a1 + b1 - 1),
                      factorial(a1 - 1) * factorial(b1 - 1))
    denom = factorial(a1 + b1 + n - 1)
    total = Fraction(0)
    for k in range(a2, n + 1):
        total += Fraction(
            comb(n, k) * factorial(a1 + k - 1) * factorial(b1 + n - k - 1),
            denom)
    return inv_B1 * total


def p_greater(a1: int, b1: int, a2: int, b2: int) -> float:
    """The same quantity in log space, which is where it is computed for any
    parameters an evaluation produces.

    Every term is a ratio of gamma functions, so lgamma turns the whole thing
    into additions -- which is Program F03's move and Program P02's reason for
    it: the factorials that overflow in one form are ordinary numbers in the
    other.  Checked against the exact version wherever the exact version can
    be afforded."""
    n = a2 + b2 - 1
    log_inv_B1 = (lgamma(a1 + b1) - lgamma(a1) - lgamma(b1))
    log_denom = lgamma(a1 + b1 + n)
    total = 0.0
    for k in range(a2, n + 1):
        total += exp(log_inv_B1
                     + lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
                     + lgamma(a1 + k) + lgamma(b1 + n - k)
                     - log_denom)
    return total


# The machinery is checked against cases whose answers are known before it is
# used on any case whose answer is not.
#
# THE SYMMETRIC CASES ARE NOT ENOUGH, and a first draft of this file learnt
# that the expensive way: `p_greater` returned the COMPLEMENT of the right
# answer, and the three checks below it were all symmetric, where 1 - 1/2 is
# 1/2 and a complement bug is invisible.  That is Program P17's shape and
# Program P27's parity trap for the second time in two programs -- a formula
# whose two readings agree on exactly the cases somebody happened to choose.
# So the two checks that matter here are the ASYMMETRIC ones: a case with a
# closed form, and a direction.
assert beta_cdf(1, 1, Fraction(1, 3)) == Fraction(1, 3)      # uniform
assert beta_cdf(1, 1, Fraction(1, 1)) == 1
assert beta_mean(1, 1) == Fraction(1, 2)
assert p_greater_exact(2, 2, 2, 2) == Fraction(1, 2)         # by symmetry
assert p_greater_exact(3, 5, 3, 5) == Fraction(1, 2)
# X uniform, Y with density 2y: P(X > Y) = int_0^1 2y(1-y) dy = 1/3, exactly.
assert p_greater_exact(1, 1, 2, 1) == Fraction(1, 3)
assert p_greater_exact(2, 1, 1, 1) == Fraction(2, 3)
# And the direction: one more success must make X more likely to be larger.
for a, b in ((2, 2), (5, 3), (17, 15)):
    assert p_greater_exact(a + 1, b, a, b) > Fraction(1, 2), (a, b)
    assert p_greater_exact(a, b + 1, a, b) < Fraction(1, 2), (a, b)
# And the float route agrees with the exact one wherever the exact one can be
# afforded -- which is what licenses using it where the exact one cannot.
P_GREATER_BOUND = 1e-12
for args in ((2, 2, 2, 2), (1, 1, 2, 1), (4, 2, 2, 4), (17, 15, 15, 17),
             (30, 12, 25, 17), (60, 40, 55, 45)):
    assert abs(p_greater(*args) - float(p_greater_exact(*args))) \
        < P_GREATER_BOUND, args


# ======================================================================
# 1.  From two hypotheses to a continuum.
#
# Program P23 put a posterior on TWO hypotheses.  Nothing about the theorem
# needs there to be two.
# ======================================================================

# THE GATE ON P23.  Its odds form is used unchanged in section 6, so this
# program must agree with it about the worked case it committed.
_p23_lr = committed("p23.tex", "p23.lr")
_p23_den = committed("p23.tex", "p23.prev.den")
if _p23_lr and _p23_den:
    lr, den = int(_p23_lr), int(_p23_den)
    post_odds = Fraction(1, den - 1) * lr
    ppv = post_odds / (1 + post_odds)
    _num = committed("p23.tex", "p23.ppv.num")
    _den2 = committed("p23.tex", "p23.ppv.den")
    assert ppv == Fraction(int(_num), int(_den2)), (ppv, _num, _den2)
    emit("p28.p23.lr", lr)
    emit("p28.p23.den", den)
    NOTES.append(f"P23's odds form reproduces: prior odds 1 to {den-1}, "
                 f"likelihood ratio {lr}, posterior {_num}/{_den2}.")


# ======================================================================
# 2.  Conjugacy: the update is adding counts, and a prior is worth items.
# ======================================================================

PRIOR_A, PRIOR_B = 1, 1                    # uniform, Beta(1,1)
emit("p28.prior.a", PRIOR_A)
emit("p28.prior.b", PRIOR_B)

# Program P27's own evaluation, continued rather than reinvented.
K = int(committed("p27.tex", "p27.boot.k") or 143)
N = int(committed("p27.tex", "p27.boot.n") or 200)
emit("p28.k", K)
emit("p28.n", N)

POST_A, POST_B = PRIOR_A + K, PRIOR_B + N - K
emit("p28.post.a", POST_A)
emit("p28.post.b", POST_B)

# The posterior mean is a weighted average of the prior mean and the data
# mean, with weights (a+b) and n.  So a Beta(a,b) prior is worth EXACTLY
# a+b observations, and that is what makes a prior a checkable quantity
# rather than a philosophical position.
def is_weighted_average(pa: int, pb: int, k: int, n: int) -> bool:
    prior_w, data_w = Fraction(pa + pb), Fraction(n)
    mixed = (prior_w * beta_mean(pa, pb) + data_w * Fraction(k, n)) \
        / (prior_w + data_w)
    return mixed == beta_mean(pa + k, pb + n - k)


for pa, pb in ((1, 1), (2, 3), (10, 10), (7, 1)):
    for k, n in ((143, 200), (4, 5), (0, 3), (20, 20)):
        assert is_weighted_average(pa, pb, k, n), (pa, pb, k, n)
emit("p28.prior.worth", PRIOR_A + PRIOR_B)

POST_MEAN = beta_mean(POST_A, POST_B)
emit("p28.post.mean.pct", 100.0 * float(POST_MEAN), 1)
MLE = Fraction(K, N)
emit("p28.mle.pct", 100.0 * float(MLE), 1)
# The two differ by less than the grid Program P27 measured, at this n.
_grid = float(committed("p27.tex", "p27.grid.pts") or 0.5)
assert abs(100.0 * float(POST_MEAN - MLE)) < _grid, (POST_MEAN, MLE)

# And at a small n the same prior moves the answer a great deal, which is the
# honest statement about when the choice of prior matters.
SMALL_K, SMALL_N = 3, 5
emit("p28.small.k", SMALL_K)
emit("p28.small.n", SMALL_N)
emit("p28.small.mle.pct", 100.0 * SMALL_K / SMALL_N, 1)
emit("p28.small.post.pct",
     100.0 * float(beta_mean(PRIOR_A + SMALL_K, PRIOR_B + SMALL_N - SMALL_K)), 1)
# A strong prior, to show the weight doing its work.
STRONG = 10
emit("p28.strong", STRONG)
emit("p28.strong.post.pct",
     100.0 * float(beta_mean(STRONG + SMALL_K, STRONG + SMALL_N - SMALL_K)), 1)


# ======================================================================
# 3.  A credible interval, and the contrast that is NOT about the digits.
# ======================================================================

CRED_LO = 100.0 * beta_quantile(POST_A, POST_B, Fraction(1, 40))
CRED_HI = 100.0 * beta_quantile(POST_A, POST_B, Fraction(39, 40))
emit("p28.cred.lo", CRED_LO, 1)
emit("p28.cred.hi", CRED_HI, 1)

_conf_lo = float(committed("p27.tex", "p27.closed.lo") or 65.2)
_conf_hi = float(committed("p27.tex", "p27.closed.hi") or 77.8)
emit("p28.conf.lo", _conf_lo, 1)
emit("p28.conf.hi", _conf_hi, 1)

# THE FINDING, and it is the opposite of what a reader expects.  The two
# intervals AGREE -- to within less than one evaluation item, which is
# Program P27 section 1's grid and the finest thing this evaluation can
# resolve.  So the contrast between them cannot be made on the numbers and
# has to be made on what each one claims.
GAP_LO = abs(CRED_LO - _conf_lo)
GAP_HI = abs(CRED_HI - _conf_hi)
# NOT EMITTED AS A FIGURE.  The larger gap is 0.4978, which prints as 0.5 at
# one decimal -- the very grid it is meant to be under, so the page would read
# as a contradiction while being right.  That is Program P20's rounding
# boundary, and Program F05's fix applies: state the bound the claim actually
# is.  Both intervals are printed, so a reader can do the two subtractions.
assert max(GAP_LO, GAP_HI) < _grid, (GAP_LO, GAP_HI, _grid)
NOTES.append(f"credible and confidence intervals differ by at most "
             f"{max(GAP_LO, GAP_HI):.2f} points, under P27's {_grid}-point grid")

# Where the prior DOES matter: the same two priors at n = 5.
S_POST = (PRIOR_A + SMALL_K, PRIOR_B + SMALL_N - SMALL_K)
T_POST = (STRONG + SMALL_K, STRONG + SMALL_N - SMALL_K)
emit("p28.small.cred.lo", 100.0 * beta_quantile(*S_POST, Fraction(1, 40)), 1)
emit("p28.small.cred.hi", 100.0 * beta_quantile(*S_POST, Fraction(39, 40)), 1)
emit("p28.strong.cred.lo", 100.0 * beta_quantile(*T_POST, Fraction(1, 40)), 1)
emit("p28.strong.cred.hi", 100.0 * beta_quantile(*T_POST, Fraction(39, 40)), 1)
# The widths, so the page can say which one the data actually chose.
W_SMALL = (100.0 * beta_quantile(*S_POST, Fraction(39, 40))
           - 100.0 * beta_quantile(*S_POST, Fraction(1, 40)))
W_BIG = (CRED_HI - CRED_LO)
emit("p28.width.small", W_SMALL, 1)
emit("p28.width.big", W_BIG, 1)
assert W_SMALL > 4 * W_BIG, (W_SMALL, W_BIG)


# ======================================================================
# 4.  The probability that B is better -- the quantity P27 handed over.
#
# Continuing Program P27's OWN worked example rather than inventing one:
# 30 discordant items with a net of 1 to B is 16 to B and 14 to A, and the
# parameter is the probability that a discordant item goes to B.
# ======================================================================

DISC = int(committed("p27.tex", "p27.disc") or 30)
NET = int(committed("p27.tex", "p27.net") or 1)
assert (DISC + NET) % 2 == 0, (DISC, NET)
TO_B = (DISC + NET) // 2
TO_A = DISC - TO_B
assert TO_B - TO_A == NET and TO_B + TO_A == DISC
emit("p28.disc", DISC)
emit("p28.to.b", TO_B)
emit("p28.to.a", TO_A)

BA, BB = PRIOR_A + TO_B, PRIOR_B + TO_A
emit("p28.bpost.a", BA)
emit("p28.bpost.b", BB)
P_B_BETTER = 1 - beta_cdf(BA, BB, Fraction(1, 2))
emit("p28.p.better.pct", pct(100.0 * float(P_B_BETTER)), 0)
assert Fraction(1, 2) < P_B_BETTER < Fraction(7, 10), P_B_BETTER

# It is consistent with P27's p-value rather than in tension with it, and the
# script says so rather than the prose asserting it: an answer that mildly
# favours B is exactly what "the data is unremarkable under a tie" looks like
# once you ask the other question.
_p27_p = float(committed("p27.tex", "p27.p.exact") or 0.86)
emit("p28.p27.p", _p27_p, 2)
assert _p27_p > 0.5 and 0.5 < float(P_B_BETTER) < 0.75

# How much more evidence before it reaches a threshold anybody would act on?
TARGET = Fraction(19, 20)
extra = 0
while 1 - beta_cdf(BA + extra, BB, Fraction(1, 2)) < TARGET:
    extra += 1
emit("p28.more.needed", extra)
emit("p28.reach.b", TO_B + extra)
emit("p28.reach.disc", DISC + extra)
assert extra > 0

# The UNPAIRED case, which is what "Bayesian A/B testing" usually means, and
# it is the same integral with two parameters instead of one.
# THE CONTROL HAS TO BE THE SAME GAP, and a first version of this comparison
# was not: it set the unpaired case a TWO-item lead against the paired case's
# one, and then asserted the paired analysis was the more confident.  It is,
# and the assertion failed anyway, because the two arms were not describing
# the same observed difference.  A comparison is only as good as what it holds
# fixed -- which is the whole of Program P21's scaling-rules section, arriving
# in this script's own setup rather than on its page.
UA_K, UA_N = K - 1, N                      # the same one-item lead
UB_K, UB_N = K, N
PA_POST = (PRIOR_A + UA_K, PRIOR_B + UA_N - UA_K)
PB_POST = (PRIOR_A + UB_K, PRIOR_B + UB_N - UB_K)
emit("p28.unp.a.k", UA_K)
emit("p28.unp.b.k", UB_K)
emit("p28.unp.n", UA_N)
P_UNPAIRED = p_greater(*PB_POST, *PA_POST)
emit("p28.unp.better.pct", pct(100.0 * float(P_UNPAIRED)), 0)
# Pairing is worth more than the unpaired comparison, on the same underlying
# gap -- which is Program P27 section 3's whole point arriving in a posterior.
assert P_B_BETTER > P_UNPAIRED, (P_B_BETTER, P_UNPAIRED)


# ======================================================================
# 5.  Thompson sampling, and the identity that makes it need no simulation.
#
# Draw one sample from each posterior and route to whichever is larger.  The
# probability of routing to B is then, BY CONSTRUCTION, P(theta_B > theta_A)
# -- which is the number section 4 already computed.  So the routing rule
# needs no experiment to describe: it explores in exact proportion to how
# likely each arm is to be the best one.
# ======================================================================

ROUTE_B = p_greater(*PB_POST, *PA_POST)
assert ROUTE_B == P_UNPAIRED
emit("p28.route.b.pct", pct(100.0 * float(ROUTE_B)), 0)

# And it self-corrects: give B ten more successes and the routing follows.
MORE = 10
PB2 = (PB_POST[0] + MORE, PB_POST[1])
emit("p28.route.more", MORE)
emit("p28.route.b2.pct", pct(100.0 * float(p_greater(*PB2, *PA_POST))), 0)
assert p_greater(*PB2, *PA_POST) > ROUTE_B

# The contrast with the fixed-epsilon rule is exact and needs no run: an
# epsilon-greedy router sends a FIXED fraction to the arm it believes worse,
# whatever the evidence, where Thompson's fraction is the posterior itself.
EPS = Fraction(1, 10)
emit("p28.eps.pct", pct(100.0 * float(EPS / 2)), 0)
# After enough evidence the posterior probability goes below epsilon/2, and
# from that point the fixed rule is spending more on the worse arm than the
# evidence supports.  Found by search rather than asserted.
# The evidence has to accumulate for B, not for A.  A first version added
# successes to A and then waited for A's advantage to FALL, which is a loop
# that cannot terminate -- and it did not: the script ran until the machine
# stopped it.  A search needs its quantity to move towards its threshold, and
# saying out loud which way it moves is the whole of checking that.
gap = 0
while p_greater(*PA_POST, PB_POST[0] + gap, PB_POST[1]) > float(EPS) / 2:
    gap += 1
    assert gap < 5000, "the search is not converging; check its direction"
emit("p28.eps.crossover", gap)
assert gap > 0


# ======================================================================
# 6.  A judge model's stated probability, priced in Program P23's odds.
#
# The information-theoretic reading of the same defect is Program P30's.
# This section stays in odds, which is P23's form and needs nothing new.
# ======================================================================

SAYS = Fraction(9, 10)                     # what the judge states
MEANS = Fraction(7, 10)                    # how often it is right when it does
emit("p28.judge.says.pct", pct(100.0 * float(SAYS)), 0)
emit("p28.judge.means.pct", pct(100.0 * float(MEANS)), 0)

ODDS_SAYS = SAYS / (1 - SAYS)              # 9 to 1
ODDS_MEANS = MEANS / (1 - MEANS)           # 7 to 3
emit("p28.judge.odds.says", float(ODDS_SAYS), 1)
emit("p28.judge.odds.means", float(ODDS_MEANS), 2)
FACTOR = ODDS_SAYS / ODDS_MEANS
# Three decimals, not two: at two the page prints 3.86 and 3.86^5 is 857
# against a true 854.  The extra digit is what makes the line checkable by
# the reader rather than merely correct.
emit("p28.judge.factor", float(FACTOR), 3)
assert FACTOR > 3

# Program P23's odds form is a MULTIPLICATION, so the error compounds
# geometrically over independent judgements -- which is the cost, and it is
# the reason "slightly overconfident" is not a small problem.
ROUNDS = 5
emit("p28.judge.rounds", ROUNDS)
COMPOUND = FACTOR ** ROUNDS
emit("p28.judge.compound",
     reproduces(float(COMPOUND), 0, (float(FACTOR), 3), (float(ROUNDS), 0),
                op=lambda a, r: a ** r),
     0)
assert COMPOUND > 100

# What it costs on the accept set, which is the number an engineer sees.
# Filtering on "the judge said 0.9" and believing it gives an error rate of
# 1 - SAYS; the true rate is 1 - MEANS.
ERR_BELIEVED = 1 - SAYS
ERR_TRUE = 1 - MEANS
emit("p28.judge.err.believed.pct", pct(100.0 * float(ERR_BELIEVED)), 0)
emit("p28.judge.err.true.pct", pct(100.0 * float(ERR_TRUE)), 0)
ERR_RATIO = ERR_TRUE / ERR_BELIEVED
emit("p28.judge.err.ratio",
     reproduces(float(ERR_RATIO), 0,
                (100.0 * float(ERR_TRUE), 0), (100.0 * float(ERR_BELIEVED), 0),
                op=lambda a, b: a / b),
     0)

# And the repair is counting, not modelling: a judge is calibrated by
# comparing what it said against what happened, in buckets.  The measurement
# is the same two counts Program F10 owns.
BUCKET_N, BUCKET_RIGHT = 200, 140
emit("p28.bucket.n", BUCKET_N)
emit("p28.bucket.right", BUCKET_RIGHT)
BUCKET_POST = (PRIOR_A + BUCKET_RIGHT, PRIOR_B + BUCKET_N - BUCKET_RIGHT)
emit("p28.bucket.lo",
     100.0 * beta_quantile(*BUCKET_POST, Fraction(1, 40)), 1)
emit("p28.bucket.hi",
     100.0 * beta_quantile(*BUCKET_POST, Fraction(39, 40)), 1)
# The stated 0.9 is outside that interval, which is what makes it a
# measurement rather than an impression -- asserted, not asserted-about.
assert 100.0 * float(SAYS) > 100.0 * beta_quantile(*BUCKET_POST, Fraction(39, 40))


# ======================================================================
# The transcript.  Every transformation is INSIDE the listing, because
# Programs P19, P24 and P27 each shipped a draft where it was not.
# ======================================================================
TRANSCRIPT = Path(__file__).resolve().parent.parent / "figures" / "transcripts"
_lines = [
    ">>> from fractions import Fraction",
    ">>> from math import comb",
    f">>> a, b = {BA}, {BB}          # {PRIOR_A} + {TO_B}, {PRIOR_B} + {TO_A}",
    ">>> n = a + b - 1",
    ">>> below = sum(Fraction(comb(n, k), 2 ** n)",
    "...             for k in range(a, n + 1))",
    ">>> round(float(1 - below), 4)",
    repr(round(float(P_B_BETTER), 4)),
]
assert max(len(line) for line in _lines) <= 64, max(_lines, key=len)
(TRANSCRIPT / "p28-how-sure.txt").write_text(
    "\n".join(_lines) + "\n", encoding="utf8")


# ======================================================================
OUT.write_text(
    "% Generated by code/p28_bayesian_inference.py --- do not edit.\n"
    "% Regenerate with `make numbers`; `make verify` fails if this file and\n"
    "% the script disagree, which is what stops a number in the book drifting\n"
    "% away from the computation that justifies it.\n\n"
    + "".join(f"\\mfaval{{{k}}}{{{v}}}\n" if numeric
             else f"\\mfavaltext{{{k}}}{{{v}}}\n"
             for k, (v, numeric) in VALUES.items()),
    encoding="utf8")
print(f"P28: {len(VALUES)} values -> {OUT}")
for note in NOTES:
    print(f"  * {note}")
