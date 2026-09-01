#!/usr/bin/env python3
"""Program P24 --- Random variables and distributions.

Every number Program P24 prints that the reader cannot do in their head is
computed here and written to figures/values/p24.tex, which the book \\input{}s.

P24's thesis is that A RANDOM VARIABLE IS A FUNCTION ON THE SAMPLE SPACE, that
expectation and variance are its first two summaries, and that sampling a token
is a draw from a categorical distribution which temperature, top-k and top-p
edit before the draw.

WHAT P24 IS OWED, read out of the files rather than remembered:

  F13  ends on the SHAPE of an expectation -- a value times a density,
       accumulated -- and says in as many words that it "deliberately does not
       give it a name", because naming it needs three words the book has not
       defined. Those words are P23's and this program's. So P24 opens by
       naming what F13 built.
  P23  owns the measure, conditioning, Bayes and BOTH kinds of independence,
       and its closing frame hands over "a way to summarise a distribution
       rather than compute with it". It also says, at the end of its
       independence section, that "a table of pairwise correlations cannot
       settle it" -- so the word arrives here already owing a demonstration.
  F05  owns temperature: a strictly increasing function keeps the order of a
       list, so temperature CANNOT move the argmax, and it commits the same
       four-token distribution at three temperatures. This program continues
       that worked example rather than inventing one.
  F07  owns the two-score softmax identity, softmax(a,b) = sigma(a-b), which
       turns out to be exactly the two-token case of the Gumbel-max trick.
  P21  borrowed the word "variance" two parts early, in a rigourbox that gives
       the reader one sentence and points here. It also commits an explicit
       ten-number population whose MEAN it computes exactly. P24 repays the
       loan the way it was taken: the definition, applied to P21's own numbers.
  P07  prints 2*Cov(p, t) in its headline identity and declares neither Cov
       nor Var. This is where both are defined.

WHAT P24 LEAVES ALONE, checked against tools/programs.json:
    variances of independent quantities add; averages
      concentrate; 1/sqrt(n); the central limit theorem       -> P25
    estimation, bias, maximum likelihood                      -> P26
    entropy, cross-entropy, KL                                -> P29, P30
    mutual information, which DOES detect the dependence
      that a zero correlation hides                           -> P31

  In particular the minibatch-noise rate is NOT repaid here. The issue asks
  P24 to revisit it; P21's own rigourbox names P25, CLAUDE.md names P25, and
  P25's brief owns "variances of independent quantities add" outright -- and
  P21 has ALREADY measured the 1/B law and the sqrt(B) spread. What P21
  actually borrowed was a DEFINITION, so that is what is returned, computed on
  P21's own population and gated against its committed mean.

EVERYTHING IN SECTIONS 1 TO 5 IS EXACT, over Fractions. Section 6 is exact
where the arithmetic allows and integrates numerically where it does not, and
says which is which.

Run:  python3 code/p24_distributions.py      (or: make numbers)
"""
from __future__ import annotations

import math
import re
from fractions import Fraction
from itertools import product
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p24.tex"
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
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# 1. A RANDOM VARIABLE IS A FUNCTION ON THE SAMPLE SPACE.
#
# The space is Program P21's own ten-number population, drawn uniformly. It is
# used rather than invented for two reasons: it is already in the book with a
# committed mean, and its numbers are small enough to hold in the head, which
# every claim below depends on the reader being able to check.
# ---------------------------------------------------------------------------
POP = [Fraction(g) for g in (3, -1, 4, 1, -5, 9, 2, -6, 5, 8)]
N = len(POP)
OMEGA = list(range(N))                    # the sample space: which one was drawn
W = Fraction(1, N)                        # uniform weight, from P23's rules


def Ex(f) -> Fraction:
    """The expectation of a random variable f, as F13's shape: value x weight,
    accumulated. On a finite space the integral is a sum and nothing else."""
    return sum(W * f(o) for o in OMEGA)


X = lambda o: POP[o]                      # the number drawn
Y = lambda o: POP[o] ** 2                 # its square -- a SECOND variable on
                                          # the SAME space, and a deterministic
                                          # function of the first
POSITIVE = lambda o: Fraction(1) if POP[o] > 0 else Fraction(0)   # an indicator

EX = Ex(X)
assert EX == Fraction(2), EX

# CROSS-PROGRAMME GATE, of Program P12's third kind: the same worked example
# CONTINUED. P21 computed the mean of this population exactly and used the word
# "variance" without defining it. If P21's mean ever moves, this program is
# quietly about a different population and the build says so.
_p21_mean = committed("p21.tex", "p21.pop.mean")
if _p21_mean is not None:
    assert float(EX) == float(_p21_mean), (EX, _p21_mean)
    NOTES.append("the population is Program P21's own ten numbers and its mean "
                 f"is gated against P21's committed {_p21_mean}")

# THE BRIDGE FROM P23, and it is one line: the expectation of an indicator is
# the probability of the event. Nothing new is defined to get it.
assert Ex(POSITIVE) == Fraction(sum(1 for g in POP if g > 0), N)
emit("p24.pos.num", sum(1 for g in POP if g > 0))
emit("p24.pop.n", N)
emit("p24.ex.x", float(EX), 1)
NOTES.append("the expectation of an indicator IS the probability of the event, "
             f"here {Ex(POSITIVE)} -- which is the whole bridge from P23")


# ---------------------------------------------------------------------------
# 2. LINEARITY, AND THAT IT NEEDS NOTHING.
#
# E[aX + bY] = a E[X] + b E[Y] holds for ANY two random variables on the same
# space. The demonstration is deliberately run on X and Y = X^2, which are as
# dependent as two variables can be: one IS a function of the other. Most
# readers answer that linearity needs independence, so it is elicited first.
# ---------------------------------------------------------------------------
EY = Ex(Y)
assert EY == Fraction(131, 5), EY

for a, b in ((Fraction(1), Fraction(1)), (Fraction(2), Fraction(3)),
             (Fraction(-1), Fraction(7)), (Fraction(1, 2), Fraction(-5, 3))):
    lhs = Ex(lambda o, a=a, b=b: a * X(o) + b * Y(o))
    assert lhs == a * EX + b * EY, (a, b, lhs)

emit("p24.ex.y", float(EY), 1)
emit("p24.ex.sum", float(EX + EY), 1)
NOTES.append("linearity checked on X and X^2, which are as dependent as two "
             "variables get, at four (a, b) pairs -- it needs no independence")

# And the thing that is NOT linear, which is what independence actually buys.
EXY = Ex(lambda o: X(o) * Y(o))           # = E[X^3]
assert EXY == Fraction(562, 5), EXY
assert EXY != EX * EY, (EXY, EX * EY)
emit("p24.ex.xy", float(EXY), 1)
emit("p24.ex.xtimesy", float(EX * EY), 1)
NOTES.append("E[XY] is not E[X]E[Y] here -- 112.4 against 52.4 -- and that gap "
             "is the whole of what a covariance measures")


# ---------------------------------------------------------------------------
# 3. VARIANCE, BY TWO ROUTES THAT MUST AGREE.
#
# Var(X) = E[(X - E X)^2], and the computational form E[X^2] - (E X)^2 is the
# same number rather than an approximation of it. Both are computed and
# asserted equal over Fractions, because "the same number" is the claim.
# ---------------------------------------------------------------------------
VAR_DEF = Ex(lambda o: (X(o) - EX) ** 2)
VAR_COMP = EY - EX ** 2
assert VAR_DEF == VAR_COMP == Fraction(111, 5), (VAR_DEF, VAR_COMP)
emit("p24.var.x", float(VAR_DEF), 1)
emit("p24.sd.x", math.sqrt(float(VAR_DEF)), 3)
NOTES.append("Var(X) by definition and by E[X^2] - (E X)^2 agree exactly over "
             f"fractions at {VAR_DEF} = {float(VAR_DEF)}")

# THE SQUARE IS THE WHOLE STORY, and it is where the square root in "spread"
# comes from. Var(aX) = a^2 Var(X), so a change of units squares.
for a in (Fraction(2), Fraction(60), Fraction(-3), Fraction(1, 4)):
    scaled = Ex(lambda o, a=a: (a * X(o) - a * EX) ** 2)
    assert scaled == a ** 2 * VAR_DEF, (a, scaled)
emit("p24.var.scale", 60)
emit("p24.var.scale.sq", 3600)
NOTES.append("Var(aX) = a^2 Var(X) at four scale factors, exactly -- minutes "
             "to seconds multiplies a variance by 3600 and a spread by 60")

# A variance is never negative, and it is zero exactly when nothing varies.
assert VAR_DEF >= 0
assert Ex(lambda o: (Fraction(7) - Fraction(7)) ** 2) == 0


# ---------------------------------------------------------------------------
# 4. COVARIANCE, CORRELATION, AND THE TWO TRAPS THIS PROGRAM OWNS.
# ---------------------------------------------------------------------------
def cov(f, g) -> Fraction:
    ef, eg = Ex(f), Ex(g)
    return Ex(lambda o: (f(o) - ef) * (g(o) - eg))


COV_XY = cov(X, Y)
assert COV_XY == EXY - EX * EY, (COV_XY, EXY - EX * EY)
assert COV_XY == Fraction(60), COV_XY
assert cov(X, X) == VAR_DEF                       # a variance IS a covariance
VAR_Y = cov(Y, Y)
assert VAR_Y == Fraction(16734, 25), VAR_Y

CORR_XY = float(COV_XY) / math.sqrt(float(VAR_DEF) * float(VAR_Y))
assert 0.49 < CORR_XY < 0.50, CORR_XY
emit("p24.cov.xy", float(COV_XY), 0)
emit("p24.corr.xy", CORR_XY, 2)
NOTES.append(f"Y IS X squared -- a perfect, exact dependence -- and their "
             f"correlation is {CORR_XY:.2f}, because correlation measures the "
             "straight-line part and nothing else")

# TRAP 30: covariance carries units and correlation does not. Asserted as an
# INVARIANCE over fractions rather than by comparing two rounded square roots:
# cross-multiplying keeps it exact.
for a, b in ((Fraction(60), Fraction(1)), (Fraction(1), Fraction(1000)),
             (Fraction(60), Fraction(60)), (Fraction(1, 7), Fraction(3))):
    aX = lambda o, a=a: a * X(o)
    bY = lambda o, b=b: b * Y(o)
    assert cov(aX, bY) == a * b * COV_XY, (a, b)
    # corr(aX, bY) == corr(X, Y), squared and cross-multiplied to stay exact
    assert (cov(aX, bY) ** 2 * VAR_DEF * VAR_Y
            == COV_XY ** 2 * cov(aX, aX) * cov(bY, bY)), (a, b)
NOTES.append("changing units multiplies a covariance and leaves a correlation "
             "alone, checked at four pairs of scale factors, exactly")

# TRAP 29: zero correlation with complete dependence. The population above has
# a non-zero covariance, so the point needs a SYMMETRIC space -- three outcomes
# is the smallest one that makes it, and everything stays exact.
TRI = [Fraction(-1), Fraction(0), Fraction(1)]
WT = Fraction(1, 3)
Z = lambda i: TRI[i]
Wq = lambda i: TRI[i] ** 2


def ex3(f):
    return sum(WT * f(i) for i in range(3))


def cov3(f, g):
    ef, eg = ex3(f), ex3(g)
    return sum(WT * (f(i) - ef) * (g(i) - eg) for i in range(3))


assert ex3(Z) == 0
assert cov3(Z, Wq) == 0, cov3(Z, Wq)              # EXACTLY zero
# ...and they are as dependent as anything can be: W is determined by Z, and
# conditioning changes the answer completely.
p_w_zero = sum(WT for i in range(3) if Wq(i) == 0)
p_w_zero_given_z_zero = Fraction(1)                # Z = 0 forces W = 0
assert p_w_zero == Fraction(1, 3)
assert p_w_zero_given_z_zero != p_w_zero
emit("p24.tri.n", 3)
# ONE VALUE AND NOT THREE: P(W = 0) is 1/3 for exactly the reason each outcome
# has weight 1/3 -- the space is uniform on three outcomes -- so printing it
# under a second name would put two numbers on the page that look like one and
# are not, which is Program F08's defect.
NOTES.append("Z uniform on {-1, 0, 1} and W = Z^2 have covariance EXACTLY "
             "zero and W is a function of Z: P(W = 0) is 1/3 and P(W = 0 given "
             "Z = 0) is 1")


# ---------------------------------------------------------------------------
# 5. DISTRIBUTIONS THROUGH THEIR ROLES.
#
# The binomial is enumerated rather than quoted: the mean and the variance come
# out of the eight outcomes and are then asserted against np and np(1-p), so
# the closed form is checked rather than recited.
# ---------------------------------------------------------------------------
PREV = Fraction(1, 1000)                  # Program P23's detector, unchanged
SENS = Fraction(99, 100)
SPEC = Fraction(99, 100)
Q_ALARM = PREV * SENS + (1 - PREV) * (1 - SPEC)
assert Q_ALARM == Fraction(549, 50000), Q_ALARM

_p23_num = committed("p23.tex", "p23.alarm.num")
_p23_den = committed("p23.tex", "p23.alarm.den")
if _p23_num and _p23_den:
    assert Q_ALARM == Fraction(int(_p23_num), int(_p23_den)), Q_ALARM
    NOTES.append("the alarm rate is gated against Program P23's committed "
                 f"{_p23_num}/{_p23_den}")

TRIALS = 3
binom = {}
for outcome in product((0, 1), repeat=TRIALS):
    w = Fraction(1)
    for bit in outcome:
        w *= Q_ALARM if bit else (1 - Q_ALARM)
    binom[sum(outcome)] = binom.get(sum(outcome), Fraction(0)) + w
assert sum(binom.values()) == 1, sum(binom.values())
mean_enum = sum(k * w for k, w in binom.items())
var_enum = sum(w * (k - mean_enum) ** 2 for k, w in binom.items())
assert mean_enum == TRIALS * Q_ALARM, (mean_enum, TRIALS * Q_ALARM)
assert var_enum == TRIALS * Q_ALARM * (1 - Q_ALARM), var_enum
emit("p24.binom.n", TRIALS)
NOTES.append(f"the binomial's np and np(1-p) are checked against all "
             f"{2 ** TRIALS} enumerated outcomes rather than quoted")

# WHAT AN EXPECTATION BUYS AN ENGINEER: it turns P23's probability into a count
# a capacity plan can use, and the ratio of two of those counts is P23's own
# headline arriving from the other side.
MILLION = 1_000_000
alarms = MILLION * Q_ALARM
real = MILLION * PREV * SENS
assert alarms == 10980 and real == 990, (alarms, real)
assert real / alarms == Fraction(11, 122), real / alarms
_p23_ppv = committed("p23.tex", "p23.ppv.pct")
if _p23_ppv is not None:
    assert abs(float(real / alarms) * 100 - float(_p23_ppv)) < 0.05
    NOTES.append("the two expected counts divide to Program P23's committed "
                 f"positive predictive value of {_p23_ppv} per cent")
emit("p24.million", MILLION)
emit("p24.alarms.million", int(alarms))
emit("p24.real.million", int(real))

# THE GAUSSIAN THROUGH ITS ROLE. The two landmarks, and they are asserted as
# bounds rather than committed as figures, because erf is a library function
# and this book has been bitten by committing one machine's answer.
def phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


one_sd = phi(1.0) - phi(-1.0)
two_sd = phi(2.0) - phi(-2.0)
assert 0.6826 < one_sd < 0.6828, one_sd
assert 0.9544 < two_sd < 0.9546, two_sd
emit("p24.gauss.one", one_sd, 2)
emit("p24.gauss.two", two_sd, 2)
NOTES.append(f"the Gaussian's two landmarks, {one_sd:.4f} and {two_sd:.4f}, "
             "asserted as bounds because erf is a library function")


# ---------------------------------------------------------------------------
# 6. DISTRIBUTION SURGERY, on Program F05's own four tokens.
#
# F05 committed this distribution at three temperatures and proved that
# temperature cannot move the argmax. This program continues that example
# rather than inventing one, and asks the question F05 could not: what does
# each of the three knobs DESTROY?
# ---------------------------------------------------------------------------
LOGITS = (2.0, 1.5, 0.5, -1.0)            # Program F05's, unchanged
TEMPS = (0.5, 1.0, 2.0)


def softmax(z, temperature: float = 1.0):
    scaled = [zi / temperature for zi in z]
    m = max(scaled)                       # the shift Program P01 owns
    exps = [math.exp(s - m) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


PROBS = {t: softmax(LOGITS, t) for t in TEMPS}

# GATE against F05's twelve committed probabilities. If F05's distribution ever
# moves, every number in this section is about a different example.
for _t in TEMPS:
    _tag = str(_t).replace(".", "")
    for _i, _p in enumerate(PROBS[_t]):
        _c = committed("f05.tex", f"f05.sm.t{_tag}.p{_i + 1}")
        if _c is not None:
            assert abs(_p - float(_c)) < 5e-5, (_t, _i, _p, _c)
NOTES.append("the four-token distribution is Program F05's, gated against all "
             "twelve of its committed probabilities")


def top_k(p, k: int):
    """Keep the k largest, zero the rest, renormalise."""
    order = sorted(range(len(p)), key=lambda i: p[i], reverse=True)
    keep = set(order[:k])
    total = sum(p[i] for i in keep)
    return [p[i] / total if i in keep else 0.0 for i in range(len(p))]


def top_p(p, mass: float):
    """Keep the smallest prefix of the sorted distribution whose total reaches
    `mass`, zero the rest, renormalise."""
    order = sorted(range(len(p)), key=lambda i: p[i], reverse=True)
    keep, running = set(), 0.0
    for i in order:
        keep.add(i)
        running += p[i]
        if running >= mass:
            break
    total = sum(p[i] for i in keep)
    return [p[i] / total if i in keep else 0.0 for i in range(len(p))]


# WHAT TRUNCATION DESTROYS, and it is a different kind of thing from what
# temperature changes. F05 proved temperature cannot move the argmax; neither
# can truncation, since it keeps the top. What truncation does is change the
# SUPPORT: after it, some tokens have probability exactly zero, and no later
# temperature can bring them back.
K = 2
deleted = {}
for t in TEMPS:
    p = PROBS[t]
    cut = top_k(p, K)
    assert cut.count(0.0) == len(p) - K
    assert abs(sum(cut) - 1.0) < 1e-12
    assert max(range(len(cut)), key=lambda i: cut[i]) == \
           max(range(len(p)), key=lambda i: p[i])          # the argmax survives
    deleted[t] = sum(p[i] for i in range(len(p)) if cut[i] == 0.0)

# The mean absolute distance, which the page quotes beside the standard
# deviation to say they are different summaries. It is head arithmetic from the
# ten distances the frame prints, so it is written inline rather than emitted --
# but it is asserted here so the sentence cannot go stale.
MAD = Ex(lambda o: abs(X(o) - EX))
assert MAD == Fraction(19, 5), MAD
assert math.sqrt(float(VAR_DEF)) > float(MAD), (VAR_DEF, MAD)
NOTES.append(f"the average distance from the mean is {float(MAD)} and the "
             f"standard deviation is {math.sqrt(float(VAR_DEF)):.3f} -- the "
             "second is larger, always, and the page says so")

# --- A DRAFT ASSERTED THAT top-k DELETES "ABOUT THE SAME" AT EVERY TEMPERATURE
# AND IT FAILED, which is the better frame: the mass top-k throws away GROWS
# with the temperature, so the two knobs are working against each other. What
# is asserted is the ordering, which is structural, and not the three figures.
assert deleted[0.5] < deleted[1.0] < deleted[2.0], deleted
RATIO = deleted[2.0] / deleted[0.5]
assert RATIO > 5, RATIO
emit("p24.topk.k", K)
emit("p24.topk.del.t05", deleted[0.5] * 100, 1)
# T = 1.0 is measured and asserted but not emitted: the frames quote the two
# ends of the sweep, and a value nothing references is a second copy nobody
# would correct. F11's finding, applied on sight.
emit("p24.topk.del.t20", deleted[2.0] * 100, 1)
emit("p24.topk.del.ratio", RATIO, 1)
NOTES.append(f"top-{K} deletes {deleted[0.5] * 100:.1f} per cent of the mass "
             f"at T = 0.5 and {deleted[2.0] * 100:.1f} at T = 2.0, a factor of "
             f"{RATIO:.1f} -- raising the temperature and then truncating "
             "spends most of what the temperature bought")

# TOP-P KEEPS A NUMBER OF TOKENS THAT IS AN OUTCOME, NOT A SETTING, and that is
# the whole difference between it and top-k. Same p, three temperatures.
PMASS = 0.9
kept = {t: sum(1 for v in top_p(PROBS[t], PMASS) if v > 0.0) for t in TEMPS}
assert kept[0.5] < kept[2.0], kept
emit("p24.topp.mass", PMASS, 1)
emit("p24.topp.kept.t05", kept[0.5])
emit("p24.topp.kept.t20", kept[2.0])

# ...and over a sweep, so the range is measured rather than read off three rows.
sweep = {}
for i in range(1, 61):
    t = i / 20.0
    sweep[t] = sum(1 for v in top_p(softmax(LOGITS, t), PMASS) if v > 0.0)
assert min(sweep.values()) == 1 and max(sweep.values()) == len(LOGITS), sweep
emit("p24.topp.sweep.lo", min(sweep.values()))
emit("p24.topp.sweep.hi", max(sweep.values()))
emit("p24.topp.sweep.n", len(sweep))
NOTES.append(f"over {len(sweep)} temperatures from 0.05 to 3.0 the same "
             f"top-p = {PMASS} keeps between {min(sweep.values())} and "
             f"{max(sweep.values())} of the four tokens")


# ---------------------------------------------------------------------------
# 7. THE GUMBEL-MAX TRICK, EXACT.
#
# Claim: with G_i independent standard Gumbel and s_i = log p_i, the index that
# maximises s_i + G_i is distributed exactly as p. Not approximately.
#
# THE TWO-TOKEN CASE IS EXACT AND IT IS ALREADY IN THE BOOK. The difference of
# two independent Gumbels is logistic, so P(1 beats 2) = sigma(s_1 - s_2), and
# sigma(s_1 - s_2) = p_1 / (p_1 + p_2) is exactly Program F07's two-score
# softmax identity. So the two-token trick is F07's frame read backwards, and
# the check here is that same identity recomputed rather than remembered.
# ---------------------------------------------------------------------------
def sigma(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


F07_ERR = 0.0
for a in [i / 4.0 for i in range(-40, 41)]:
    for b in [j / 4.0 for j in range(-40, 41)]:
        two = softmax((a, b))
        F07_ERR = max(F07_ERR, abs(two[0] - sigma(a - b)))
assert F07_ERR < 1e-12, F07_ERR
NOTES.append("Program F07's identity softmax(a, b) = sigma(a - b) recomputed "
             f"over an 81 x 81 grid, worst gap {F07_ERR:.1e} -- which is what "
             "makes the two-token Gumbel case exact rather than sampled")

P_TWO = (Fraction(7, 10), Fraction(3, 10))
s1, s2 = math.log(float(P_TWO[0])), math.log(float(P_TWO[1]))
assert abs(sigma(s1 - s2) - float(P_TWO[0])) < 1e-12
emit("p24.gumbel.two.num", 7)
emit("p24.gumbel.two.den", 10)

# THE GENERAL CASE cannot be done in closed form on the page, so it is
# integrated rather than sampled: sampling would give an estimate with its own
# error bar, and the claim is EXACTNESS. P(k wins) is the probability that k's
# Gumbel beats every other shifted one, integrated over k's own density.
def gumbel_pdf(g: float) -> float:
    return math.exp(-g - math.exp(-g))


def gumbel_cdf(g: float) -> float:
    return math.exp(-math.exp(-g))


def gumbel_max_prob(p, k: int, lo: float = -8.0, hi: float = 35.0,
                    steps: int = 100_000) -> float:
    """P(argmax_i (log p_i + G_i) == k), by Simpson over k's Gumbel density."""
    s = [math.log(pi) for pi in p]
    h = (hi - lo) / steps

    def integrand(g: float) -> float:
        out = gumbel_pdf(g)
        for j in range(len(p)):
            if j != k:
                out *= gumbel_cdf(g + s[k] - s[j])
        return out

    total = integrand(lo) + integrand(hi)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * integrand(lo + i * h)
    return total * h / 3.0


# The range is chosen rather than guessed: the Gumbel tail beyond `hi` is
# under exp(-hi), so 35 leaves 6e-16 outside and 22 leaves 3e-10, which a first
# draft found the hard way when the four answers summed to 0.9999999989.
#
# AND MORE STEPS MADE IT WORSE, which is worth knowing before anybody tunes
# this: at 200,000 the worst gap is 2.1e-13 and at 100,000 it is 1.1e-13,
# because past a point the rounding accumulated over the sum grows faster than
# Simpson's error falls. That is Program P02's subject arriving in a
# quadrature. The committed bound is two orders looser than the measurement,
# on this book's rule that a residual is a property of the machine.
GUMBEL_BOUND = 1e-11
worst = 0.0
for t in TEMPS:
    p = PROBS[t]
    got = [gumbel_max_prob(p, k) for k in range(len(p))]
    assert abs(sum(got) - 1.0) < GUMBEL_BOUND, sum(got)
    worst = max(worst, max(abs(g - pi) for g, pi in zip(got, p)))
assert worst < GUMBEL_BOUND, worst
# NOT EMITTED: the bound is a decision rather than a measurement, and 10^{-11}
# is a number the reader reads rather than one they could not do in their head.
# C7 would report it as unproduced anyway, because a text value is written with
# \mfavaltext and the ledger scans for \mfaval -- which is F10's, P03's, P18's
# and P22's finding, applied on sight.
NOTES.append(f"argmax(log p + Gumbel) reproduces all four probabilities at "
             f"all three temperatures to better than {GUMBEL_BOUND:g} "
             f"(measured {worst:.1e}), integrated rather than sampled, "
             "because the claim is exactness")

# AND THE TWO SECTIONS MEET, on one number that is deliberately NOT emitted
# twice. Truncate first and tokens 3 and 4 are impossible; add the noise first
# and they win the argmax exactly as often as their probability says. That
# frequency IS the mass top-k deletes -- the same 28 per cent under two names --
# and the equality is the theorem rather than a coincidence, which is why the
# script asserts it and the page quotes one value.
p20 = PROBS[2.0]
before = top_k(p20, K)
assert before[2] == 0.0 and before[3] == 0.0
after_wins = gumbel_max_prob(p20, 2) + gumbel_max_prob(p20, 3)
assert abs(after_wins - deleted[2.0]) < GUMBEL_BOUND, (after_wins, deleted[2.0])
NOTES.append("the tokens top-2 deletes would have won the argmax exactly "
             f"{deleted[2.0] * 100:.1f} per cent of the time -- the same number, "
             "because Gumbel-max is exact, so truncation does not discourage "
             "them, it removes them")


# ---------------------------------------------------------------------------
# The transcript. Both listings are extracted from the finished PDF and run;
# every transformation the page shows is written into the listing itself, so
# the printed line and the printed result cannot come apart.
# ---------------------------------------------------------------------------
# repr(), never a format string: a first draft wrote the four kept values with
# ":.4f" and printed 0.0000 where a session prints 0.0, which is Program P19's
# fabricated-console defect -- the rounding was applied to the OUTPUT instead of
# being written into the listing's own code.
TRANSCRIPT = [
    ">>> from p24_distributions import PROBS, top_k, top_p",
    ">>> [round(v, 4) for v in PROBS[2.0]]",
    repr([round(v, 4) for v in PROBS[2.0]]),
    ">>> [round(v, 4) for v in top_k(PROBS[2.0], 2)]",
    repr([round(v, 4) for v in top_k(PROBS[2.0], 2)]),
    ">>> sum(1 for v in top_p(PROBS[0.5], 0.9) if v > 0)",
    repr(sum(1 for v in top_p(PROBS[0.5], 0.9) if v > 0.0)),
]
for line in TRANSCRIPT:
    assert len(line) <= 64, (len(line), line)
TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
(TRANSCRIPTS / "p24-surgery.txt").write_text("\n".join(TRANSCRIPT) + "\n",
                                             encoding="utf8")


# ---------------------------------------------------------------------------
OUT.parent.mkdir(parents=True, exist_ok=True)
lines = [
    "% Generated by code/p24_distributions.py --- do not edit.",
    "% Regenerate with `make numbers`; `make verify` fails if this file and",
    "% the script disagree, which is what stops a number in the book drifting",
    "% away from the computation that justifies it.",
    "",
]
for key, (body, numeric) in VALUES.items():
    lines.append(("\\mfaval{%s}{%s}" if numeric else "\\mfavaltext{%s}{%s}")
                 % (key, body))
OUT.write_text("\n".join(lines) + "\n", encoding="utf8")

print(f"P24: {len(VALUES)} values -> {OUT}")
for n in NOTES:
    print("  *", n)
print("  transcript: figures/transcripts/p24-surgery.txt")
