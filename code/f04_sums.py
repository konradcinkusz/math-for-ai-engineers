#!/usr/bin/env python3
"""Program F4 --- Sums, products and sequences.

Every number Program F4 prints that the reader cannot do in their head is
computed here and written to figures/values/f04.tex, which the book \\input{}s.

F4's thesis is that sigma and pi are loops, so almost everything in it is
checkable by writing the loop out and comparing. That is what this script does:
where the program states a closed form, the closed form is computed AND the
loop is run, and the build asserts they agree. The reader is being taught that
n(n+1)/2 counts the pairs a causal mask computes and that an exponential moving
average is a weighted sum of everything it has ever seen; both claims are
executed here rather than trusted.

STDLIB ONLY, deliberately, as in F3: `make numbers` must run on a plain
python3. numpy is used nowhere in the arithmetic. It is opened at the bottom
purely to CHECK frame 16's claims about it, and that block announces itself
when numpy is absent rather than passing silently.

NOT EMITTED, and none of it should be --- putting it behind \\val{} would be
theatre. This program teaches summation, so most of its arithmetic is the thing
being taught and stays inline as digits in the prose:

    2 + 5 + 1 + 7 = 15;  1 + 4 + 9 = 14;  3 + 8 = 11 against 3 x 7 = 21;
    n + 1 terms in a sum from 0 to n;  4! = 24;
    sum([]) = 0, math.prod([]) = 1 and 0! = 1 -- the transcript below carries
      them as run output, and the frame states them as the answer;
    8 x 9 / 2 = 36 against 64;  100 x 101 / 2 = 5050;
    3 x 2^4 = 48;  the two weights 0.10 and 0.09;  1 / (1 - 0.9) = 10;
    the biases 0.1 and 0.001 after one step;
    the three MACRO figures 5.0, 0.50 and 50.5, each of which the reader must
      be able to produce in their head or the trap in section 5 cannot fire.

TWO PAIRS OF KEYS THAT LOOK LIKE ONE NUMBER PRINTED TWICE, AND ARE NOT. Both
pairs are the program's own punchline arriving in two places, and the frames
should say so rather than leave the reader to spot the coincidence:

    f04.geom.ten (6.5132) and f04.ema.w10 (0.6513) differ by exactly the factor
        (1 - beta) = 0.1. The first is the sum of the first ten terms of the
        geometric series; the second is the weight an EMA at beta = 0.9 puts on
        the last ten observations. The second IS the first scaled, which is
        precisely why section 6 has to come before section 7.
    f04.geom.inf (10) is 1 / (1 - 0.9), and the EMA's effective window is the
        same 10 for the same reason. ONE key, quoted in both places.

CROSS-PROGRAM REUSE, and it is deliberate. Frame 17 opens by paying F3's debt:
F3 wrote `ln p(sequence) = sum_i ln p(token i | ...)` and then divided by the
token count, using a sigma it never defined and a subscript the reader had not
met. That sentence is L = -(1/n) sum ln p_i, and F4 gives every symbol in it a
name. The frame quotes \\val{f03.seq.tokens} and \\val{f02.loss.nats} rather
than new f04 keys, because the three programs must be provably quoting one
computation. \\mfaval keys are global -- figures/values/all.tex inputs every
file -- so this works, and a later pass deleting an f02 or f03 key would break
F4 silently.

TWO THINGS THE .TEX AUTHOR MUST NOT WRITE, both found by running rather than
by reasoning, and both recorded at their computation below:

  * The bias-corrected EMA is NOT exactly 1.0 on a constant sequence. It is
    exactly 1 in exact arithmetic and 1 to within about 1.4e-14 in binary64,
    measured. Write "exactly right" of the algebra, never of the float.
  * numpy emits TWO RuntimeWarnings from `np.array([]).mean()`, not one, on
    this container. Warning text is a library-version fact; the invariant is
    that the empty mean RETURNS nan and RAISES nothing, and that is what the
    frame may state. See the numpy block at the bottom.

Run:  python3 code/f04_sums.py      (or: make numbers)
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


# ==========================================================================
# SECTION 2 --- where the index starts, and what a causal mask actually costs
#
# Row i of a causal mask attends to keys 0..i, so over n positions the number
# of query-key pairs computed is 1 + 2 + ... + n = n(n+1)/2 against n^2 for the
# full square. Gauss's pairing gives the closed form in one line and the frame
# shows it; the script runs the loop as well, because "the closed form counts
# the same thing as the loop" is the whole of section 1's claim and it should
# not be the one thing nobody checked.
#
# THE HONEST DETAIL, and it is what makes the frame worth its space: the ratio
# is never exactly a half. The excess is the diagonal -- every query attends to
# its own key -- so the ratio is (n+1)/(2n), which falls TOWARDS a half from
# above and reaches it nowhere. At n = 8 it is 0.5625, which is 12.5 per cent
# more work than half. "Causal masking halves the work" is an asymptotic
# statement quoted as an exact one.
# ==========================================================================
def triangle(n: int) -> int:
    return n * (n + 1) // 2


CAUSAL_N = 2048
CAUSAL_SMALL = 8

CAUSAL_PAIRS = triangle(CAUSAL_N)
emit("f04.causal.pairs", CAUSAL_PAIRS)
emit("f04.causal.sq", CAUSAL_N**2)
emit("f04.causal.ratio", CAUSAL_PAIRS / CAUSAL_N**2, 4)
emit("f04.causal.ratio.eight", triangle(CAUSAL_SMALL) / CAUSAL_SMALL**2, 4)

# The closed form against the loop, at both n. This is section 1's claim
# executed, not asserted.
for _n in (CAUSAL_SMALL, CAUSAL_N):
    assert triangle(_n) == sum(range(1, _n + 1)), f"n(n+1)/2 is not the loop at n={_n}"

# ...and the direction of the approach, which is the sentence the frame makes.
# Stated as an invariant of the ratio rather than as the two rounded figures on
# the page: it is above a half at every n, and it falls as n grows.
_r8 = triangle(CAUSAL_SMALL) / CAUSAL_SMALL**2
_rbig = triangle(CAUSAL_N) / CAUSAL_N**2
assert 0.5 < _rbig < _r8, "the causal ratio no longer falls towards a half from above"

# ==========================================================================
# SECTION 4 --- every loss is a sigma over n
#
# Mean squared error on four points, which is the same machine as the sigma of
# section 1 with (yhat - y)^2 in the body:
#
#     y    = ( 3, -0.5, 2, 7)
#     yhat = (2.5,  0,  2, 8)
#     residuals   -0.5, 0.5, 0, 1
#     squares      0.25, 0.25, 0, 1   ->  sum 1.5, over 4 -> 0.375
#
# Mean absolute error on the same data is the same shape with |.| in the body
# and comes to 0.5, which is the point: the sigma and the divisor do not move,
# only the per-example term.
#
# The three keys are exact at the precision they print, so the digits are the
# arithmetic and not a rounding of it.
# ==========================================================================
MSE_Y = (3.0, -0.5, 2.0, 7.0)
MSE_YHAT = (2.5, 0.0, 2.0, 8.0)

_resid = [yh - y for yh, y in zip(MSE_YHAT, MSE_Y)]
SQ_SUM = math.fsum(r * r for r in _resid)
emit("f04.mse.sum", SQ_SUM, 1)
emit("f04.mse", SQ_SUM / len(MSE_Y), 3)
emit("f04.mae", math.fsum(abs(r) for r in _resid) / len(MSE_Y), 1)

# Cross-entropy over a batch of four, which is the third loss in that same
# shape:  L = -(1/n) sum ln p_i.
CE_PROBS = (0.9, 0.5, 0.2, 0.05)
CE_SUM = math.fsum(-math.log(p) for p in CE_PROBS)
CE_MEAN = CE_SUM / len(CE_PROBS)
emit("f04.ce.sum", CE_SUM, 4)
emit("f04.ce.mean", CE_MEAN, 4)

# Perplexity is the exponential of that mean --- F3's quantity, reached from
# F4's notation. The number a leaderboard should print is exp(mean); the mean
# of the four per-example perplexities is a different quantity and a larger
# number, and F4 states the difference in one sentence and hands the general
# inequality to P19, which is where Jensen lives.
#
# The INEQUALITY is asserted, not the gap: that exp of a mean is below the mean
# of the exponentials is a theorem and holds on every machine, whereas the size
# of the gap is a property of these four probabilities.
CE_PPL = math.exp(CE_MEAN)
CE_PPL_NAIVE = math.fsum(1.0 / p for p in CE_PROBS) / len(CE_PROBS)
emit("f04.ce.ppl", CE_PPL, 4)
emit("f04.ce.ppl.naive", CE_PPL_NAIVE, 4)
assert CE_PPL < CE_PPL_NAIVE, "the exponential of the mean must sit below the mean of the exponentials"

# ==========================================================================
# SECTION 5 --- when you may not average the averages
#
# THE HEADLINE TRAP, and the reason it gets a number instead of an adjective.
# Two micro-batches, 1000 tokens at mean loss 2.0 and 10 tokens at mean loss
# 8.0. Averaging the two group means gives 5.0, because it hands a 10-token
# batch the same weight as a 1000-token one. Pooling the tokens gives
#
#     (1000 x 2.0 + 10 x 8.0) / 1010 = 2080 / 1010 = 2.0594
#
# and 5.0 is 2.43 times that. Both quantities are real and both have names ---
# the MICRO average pools the items, the MACRO average averages the group
# numbers --- so the fault is never "you computed the wrong one", it is not
# knowing which one you are holding.
#
# EVERY POOLED FIGURE HERE IS RECOMPUTED FROM THE ITEM LIST, not from the group
# means. Deriving it from the means would be assuming the thing the section is
# about. math.fsum rather than sum, because section 6's warning frame says a
# floating-point sum has an order and it would be poor form for this script to
# rely on one; fsum rounds once, so the answer does not depend on the order the
# groups happen to be listed in.
# ==========================================================================
def micro(groups: list[tuple[float, int]]) -> float:
    """Pool the items and divide once: sum of all values over count of all."""
    items = [v for value, count in groups for v in [value] * count]
    return math.fsum(items) / len(items)


def macro(groups: list[tuple[float, int]]) -> float:
    """Average the group numbers, each with weight one, whatever it stands for."""
    return math.fsum(value for value, _ in groups) / len(groups)


# (mean loss, token count) --- the pair of columns the trap lives in.
BATCHES = [(2.0, 1000), (8.0, 10)]
BATCH_POOLED = micro(BATCHES)
BATCH_NAIVE = macro(BATCHES)
emit("f04.batch.pooled", BATCH_POOLED, 4)
emit("f04.batch.factor", BATCH_NAIVE / BATCH_POOLED, 4)

# The weighted form the frame writes on the page must be the same number as the
# pooled item list. If these ever part company the frame is teaching one thing
# and printing another.
_weighted = math.fsum(v * c for v, c in BATCHES) / sum(c for _, c in BATCHES)
assert abs(BATCH_POOLED - _weighted) < 1e-12, "pooled loss disagrees with the weighted mean"
assert BATCH_NAIVE == 5.0, "the macro figure the reader computes in their head has moved"

# The second instance, in a different unit, because one instance is an anecdote.
# Evaluation shards: (correct, total). Micro is 91/110 = 0.8273; the macro
# average of 0.90 and 0.10 is 0.50, which is head arithmetic and stays inline.
#
# This is the mean of ratios against the ratio of means, on the pair of columns
# an evaluation harness actually reports, and it is computed from the 0/1 items
# rather than from the two accuracies.
SHARDS = [(90, 100), (1, 10)]
_items = [1.0] * sum(c for c, _ in SHARDS) + \
         [0.0] * sum(t - c for c, t in SHARDS)
ACC_MICRO = math.fsum(_items) / len(_items)
ACC_MACRO = math.fsum(c / t for c, t in SHARDS) / len(SHARDS)
emit("f04.acc.micro", ACC_MICRO, 4)
assert abs(ACC_MICRO - sum(c for c, _ in SHARDS) / sum(t for _, t in SHARDS)) < 1e-12
assert ACC_MACRO == 0.50, "the macro accuracy the frame quotes in its head has moved"

# The third instance, and the one where the gap is largest, because a rate has
# its count in the DENOMINATOR. 100 tokens in 1 second and 100 tokens in 100
# seconds: the two rates are 100 and 1 tok/s, whose mean is 50.5, and the rate
# over the whole run is 200 tokens / 101 seconds = 1.9802 tok/s. Twenty-five
# times smaller, and neither number is a typo.
#
# Worth stating because it is exact and checkable: when the NUMERATORS are
# equal the pooled rate is the HARMONIC mean of the rates, and here it is
# 1.9802 to the digit. Checked with a tolerance rather than for bit equality:
# 1/100 is not a binary fraction, so the two routes round differently in the
# last place and an exact comparison would be asserting an observation about
# this machine's rounding rather than the identity.
WORK = [(100.0, 1.0), (100.0, 100.0)]        # (tokens, seconds)
RATE_MICRO = math.fsum(w for w, _ in WORK) / math.fsum(t for _, t in WORK)
RATE_MACRO = math.fsum(w / t for w, t in WORK) / len(WORK)
emit("f04.rate.micro", RATE_MICRO, 4)
emit("f04.rate.factor", RATE_MACRO / RATE_MICRO, 4)

_harmonic = len(WORK) / math.fsum(t / w for w, t in WORK)
assert abs(_harmonic - RATE_MICRO) < 1e-12, "equal numerators: the pooled rate is not the harmonic mean"
assert RATE_MACRO == 50.5, "the macro rate the frame quotes in its head has moved"

# And the rule the three instances share, checked in the form the frame states
# it: a mean of ratios is not the ratio of the sums, and the two agree exactly
# when every denominator is equal. Run both ways, so the condition in the
# \yourturn at the end of section 5 is demonstrated and not merely claimed.
_equal = [(9, 10), (1, 10)]
assert abs(math.fsum(c / t for c, t in _equal) / len(_equal)
           - sum(c for c, _ in _equal) / sum(t for _, t in _equal)) < 1e-12, \
    "with equal denominators macro and micro must coincide"
assert ACC_MACRO != ACC_MICRO, "with unequal denominators they must not"

# ==========================================================================
# SECTION 6 --- the geometric series, and a product of factors near one
#
# S = sum_{k=0}^{n-1} r^k = (1 - r^n) / (1 - r), derived in the frame by
# subtracting a shifted copy. At r = 0.9 and n = 10 that is 6.5132, and as the
# number of terms grows with |r| < 1 the r^n term goes to nothing and S tends
# to 1 / (1 - r) = 10.
#
# Closed form against the loop again, with a tolerance rather than an exact
# comparison. The two differ in the last place here --- 6.513215599 against
# 6.5132155990000005 --- which is not a defect and is worth knowing, because it
# is section 4's closing warning happening inside this script: the same sum by
# two routes is the same real number and not the same float.
# ==========================================================================
GEOM_R, GEOM_N = 0.9, 10
GEOM_CLOSED = (1.0 - GEOM_R**GEOM_N) / (1.0 - GEOM_R)
emit("f04.geom.ten", GEOM_CLOSED, 4)
emit("f04.geom.inf", round(1.0 / (1.0 - GEOM_R)))

_loop = math.fsum(GEOM_R**k for k in range(GEOM_N))
assert abs(GEOM_CLOSED - _loop) < 1e-12, "the geometric closed form is not the loop"
assert abs(1.0 / (1.0 - GEOM_R) - round(1.0 / (1.0 - GEOM_R))) < 1e-12, \
    "1/(1-r) is no longer the integer the frame prints"

# The other direction: a product of many factors NEAR one. Fifty layers, each
# scaling a signal by 0.9 or by 1.1 --- two factors 0.2 apart --- and after
# fifty multiplications they are four orders of magnitude apart. That ratio is
# (1.1/0.9)^50 and it is the arithmetic under every sentence about a signal
# crossing a deep stack.
#
# THE RATIO IS EMITTED TO THREE SIGNIFICANT FIGURES, AND THAT IS NOT TIDINESS.
# The frame prints the two products next to it, at the precision a reader can
# hold: 0.005154 and 117.39. Divide those two and you get 22776; the exact
# ratio is 22778. A ratio printed to five figures is therefore a number the
# page cannot reproduce, which is exactly the defect F03 shipped when it
# printed a mantissa taken from an unrounded logarithm. Three significant
# figures is the widest precision the two routes agree on, and the assertion
# below is what keeps them agreeing when any of the three precisions moves.
DECAY_R, GROW_R, LAYERS = 0.9, 1.1, 50
DECAY_DIGITS, GROW_DIGITS, RATIO_FIGURES = 6, 2, 3
DECAY = DECAY_R**LAYERS
GROW = GROW_R**LAYERS


def to_figures(x: float, figures: int) -> int:
    """`x` rounded to `figures` significant figures, as a whole number."""
    step = 10 ** (math.floor(math.log10(x)) - figures + 1)
    return int(round(x / step) * step)


DECAY_RATIO = to_figures(GROW / DECAY, RATIO_FIGURES)
emit("f04.decay.fifty", DECAY, DECAY_DIGITS)
emit("f04.grow.fifty", GROW, GROW_DIGITS)
emit("f04.decay.ratio", DECAY_RATIO)
emit("f04.decay.log", LAYERS * math.log(DECAY_R), 4)

# The page has to reproduce: dividing the two products the frame prints must
# give the ratio the frame prints, at the precision the frame prints it.
assert to_figures(round(GROW, GROW_DIGITS) / round(DECAY, DECAY_DIGITS),
                  RATIO_FIGURES) == DECAY_RATIO, \
    "the ratio no longer reproduces from the two products beside it"

# The identity that joins this program's two symbols, and F3's first law
# written over a pi rather than over two factors:
#
#     ln prod_i x_i = sum_i ln x_i
#
# Fifty factors, both routes, so frame 34's claim is executed. The product is
# formed here because fifty factors of 0.9 is nowhere near a float's floor ---
# F3 measured where that floor is and it takes 311 factors of 0.0907 to reach
# it in binary64 --- so this is the case where both routes CAN be run, which is
# exactly why it is the case the frame uses to demonstrate the law.
_factors = [DECAY_R] * LAYERS
_prod = 1.0
for _x in _factors:
    _prod *= _x
assert abs(math.log(_prod) - math.fsum(math.log(x) for x in _factors)) < 1e-9, \
    "ln of the product is no longer the sum of the logs"
assert abs(LAYERS * math.log(DECAY_R) - math.fsum(math.log(x) for x in _factors)) < 1e-9

# ==========================================================================
# SECTION 7 --- the exponential moving average
#
#     m <- beta * m + (1 - beta) * g
#
# Two lines, no calculus, and it is the whole of momentum and half of Adam.
# beta weights the OLD value, which is the trap: read the other way round,
# beta = 0.9 would mean nine-tenths of the news and a bigger beta would react
# faster, and it is the reverse.
#
# THE FRAME THE PROGRAM EXISTS TO REACH is the unrolling, because it turns the
# loop into a sigma the reader has spent six sections learning to read:
#
#     m_t = (1 - beta) sum_{k=0}^{t-1} beta^k g_{t-k}  +  beta^t m_0
#
# The weights are section 6's geometric sequence, and section 6's series is why
# they add to 1 - beta^t. Both statements are computed below against the loop
# rather than asserted, on a sequence that is not constant, because a constant
# sequence would satisfy the claim for the wrong reason.
# ==========================================================================
def ema(values, beta: float, m0: float = 0.0) -> list[float]:
    """The two lines, run. Returns m after each observation."""
    m, out = m0, []
    for g in values:
        m = beta * m + (1.0 - beta) * g
        out.append(m)
    return out


def ema_unrolled(values, beta: float, m0: float = 0.0) -> float:
    """The same quantity as the weighted sum the unrolling claims it is."""
    t = len(values)
    weighted = math.fsum((1.0 - beta) * beta**k * values[t - 1 - k] for k in range(t))
    return weighted + beta**t * m0


BETA = 0.9
# A sequence with no pattern in it, so that agreement between the loop and the
# weighted sum cannot come from the values being all alike. Written out rather
# than generated, so the check is the same computation on every machine and in
# every future run --- a seeded generator would be one library version away
# from being a different test.
NOISY = [4.0, 9.0, 1.0, 7.0, 2.0, 8.0, 3.0, 6.0, 5.0, 0.5, 11.0, 2.5]

assert abs(ema(NOISY, BETA)[-1] - ema_unrolled(NOISY, BETA)) < 1e-12, \
    "the recurrence and its unrolled weighted sum have parted company"
assert abs(ema(NOISY, BETA, m0=3.0)[-1] - ema_unrolled(NOISY, BETA, m0=3.0)) < 1e-12, \
    "the beta^t m_0 term of the unrolling is wrong"

# The weights, and the folklore. "beta = 0.9 averages the last ten" is the
# sentence everybody repeats. What is true is that the weights are
# (1 - beta) beta^k, so the last ten carry 1 - beta^10 of the total and the
# last twenty carry 1 - beta^20:
WEIGHT_LAST_TEN = 1.0 - BETA**10
WEIGHT_LAST_TWENTY = 1.0 - BETA**20
emit("f04.ema.w10", WEIGHT_LAST_TEN, 4)
emit("f04.ema.w20", WEIGHT_LAST_TWENTY, 4)

# ...checked against the weights themselves, summed. Note this is
# (1 - beta) x f04.geom.ten: the series of section 6, scaled. The frames should
# say so; it is why section 6 comes first.
assert abs(WEIGHT_LAST_TEN - math.fsum((1.0 - BETA) * BETA**k for k in range(10))) < 1e-12, \
    "the weight on the last ten is not the sum of those ten weights"
assert abs(WEIGHT_LAST_TEN - (1.0 - BETA) * GEOM_CLOSED) < 1e-12, \
    "the EMA weights are no longer section 6's series scaled"

# Three descriptions of "how far back this thing looks", none of which is "ten",
# and all three computed:
#
#   effective window   sum of the weights' scale, 1 / (1 - beta)      = 10
#   centre of mass     sum_k k (1-beta) beta^k = beta / (1 - beta)    = 9
#   HALF-LIFE          the k at which beta^k = 1/2, ln(1/2) / ln beta = 6.58
#
# The half-life is the one to carry, because it is the smallest and it is the
# one that answers the question a reader actually has: half the weight is in
# the last SEVEN observations, not the last ten.
#
# The centre of mass is computed both ways -- the closed form, and the series
# truncated far past where its terms matter -- so the closed form is checked
# rather than quoted.
def half_life(beta: float) -> float:
    """Steps for a weight to fall by half. Also, and this is not a coincidence,
    the steps an EMA started at zero takes to cover half of a constant signal:
    the uncorrected average reads 1 - beta^t of the truth, so it reaches a half
    when beta^t does. One number, two readings, and section 7 uses both."""
    return math.log(0.5) / math.log(beta)


def steps_to_half(beta: float) -> int:
    """The same quantity as an integer, measured by running the recurrence on a
    constant signal of 1 until it reads half of it. This is the operational
    definition; half_life() is the closed form, and they are asserted equal."""
    m, t = 0.0, 0
    while m < 0.5:
        m = beta * m + (1.0 - beta) * 1.0
        t += 1
    return t


EMA_COM_CLOSED = BETA / (1.0 - BETA)
_com_series = math.fsum(k * (1.0 - BETA) * BETA**k for k in range(2000))
assert abs(EMA_COM_CLOSED - _com_series) < 1e-6, "beta/(1-beta) is not the weights' centre of mass"
assert abs(EMA_COM_CLOSED - round(EMA_COM_CLOSED)) < 1e-9, "the centre of mass is no longer an integer"
emit("f04.ema.com", round(EMA_COM_CLOSED))

emit("f04.ema.halflife", half_life(BETA), 4)
emit("f04.ema.halflife.steps", math.ceil(half_life(BETA)))

# Adam's two betas. Cited from Kingma and Ba, which is a stable source that
# needs no install; a library default is a thing you must RUN to know, and
# there is no framework in this container. The second moment's half-life is
# what makes bias correction matter for hundreds of steps rather than for
# three, and it is the number frame 40 turns on.
emit("f04.ema.b99.halflife", half_life(0.99), 4)
emit("f04.ema.b99.steps", math.ceil(half_life(0.99)))
emit("f04.ema.b999.halflife", half_life(0.999), 4)
emit("f04.ema.b999.steps", math.ceil(half_life(0.999)))

# The closed form against the measurement, for all three betas: the number of
# steps to cover half of a constant signal is the ceiling of the half-life.
for _b in (BETA, 0.99, 0.999):
    assert steps_to_half(_b) == math.ceil(half_life(_b)), \
        f"steps to half a constant signal is not ceil(half-life) at beta={_b}"

# --------------------------------------------------------------------------
# The initialisation, and the one division that removes it.
#
# m starts at 0, so on a constant signal of 1 the average reads 1 - beta^t: a
# tenth of the truth after one step at beta = 0.9, and a THOUSANDTH at
# beta = 0.999. That is not a slow start, it is a wrong number, and a smoothed
# loss curve that climbs to meet the real one is showing you the bias and not
# the model.
#
# The fix is one division:  mhat_t = m_t / (1 - beta^t).
#
# READ THIS BEFORE WRITING THE FRAME. In exact arithmetic the correction is
# exact at every t on a constant sequence, because m_t is exactly (1-beta^t)
# times the constant. In binary64 it is NOT: the two routes round differently
# and the corrected value comes back 1.0 to within about 1.4e-14, measured
# below and printed by this script on every run. The frame may say the
# correction is exactly right; it may not say the float prints 1.0 to the bit,
# because on this machine at beta = 0.999, t = 2 it does not. This is the same
# shape as F3's np.logspace claim, which asserted an observation, and CI
# disagreed with the container.
# --------------------------------------------------------------------------
BIAS_STEPS = 5
BIAS_WORST = 0.0
for _b in (BETA, 0.999):
    _m = 0.0
    for _t in range(1, BIAS_STEPS + 1):
        _m = _b * _m + (1.0 - _b) * 1.0
        _uncorrected = _m
        _corrected = _m / (1.0 - _b**_t)
        # The uncorrected reading is 1 - beta^t, which is the whole complaint.
        assert abs(_uncorrected - (1.0 - _b**_t)) < 1e-12, \
            f"the uncorrected EMA of a constant 1 is not 1 - beta^t at beta={_b}, t={_t}"
        BIAS_WORST = max(BIAS_WORST, abs(_corrected - 1.0))
assert BIAS_WORST < 1e-12, \
    f"bias correction no longer recovers the constant: worst error {BIAS_WORST!r}"

# ==========================================================================
# SECTION 3 --- the two empty cases, and the transcript that carries them
#
# sum([]) is 0 and math.prod([]) is 1, and neither is a convention picked for
# tidiness: each is the only value that leaves the next term alone. That is the
# identity element of the operation, and it is checked here as the property
# rather than as the two literals, because the property is the frame's
# argument.
#
# THE TRANSCRIPT CARRIES THE TWO EMPTY CASES AND NOTHING ELSE. It must not
# carry 0.0/0.0, tempting though that is: the frame after the transcript ends
# by asking what `total / count` does when a batch is entirely masked, and a
# traceback sitting two frames above the question would answer it before it is
# put.
#
# AND IT MUST NOT CARRY math.factorial(0), WHICH IT DID. The frame the
# transcript sits IN ends by asking what 0! is, so the answer was printed four
# lines above the question, on the same page, where no pagination could put
# them apart. A generated file is under the same rule as a figure: it may not
# answer the frame it sits in, nor the frame on either side of it. ZERO_FACTORIAL
# is still computed and still asserted below -- a further problem asks for 0!
# by two routes -- it is only kept off this page.
# ==========================================================================
EMPTY_SUM = sum([])
EMPTY_PROD = math.prod([])
ZERO_FACTORIAL = math.factorial(0)

for _x in (0.0, 1.0, -3.5, 7.0):
    assert EMPTY_SUM + _x == _x, "the empty sum is not the identity for addition"
    assert EMPTY_PROD * _x == _x, "the empty product is not the identity for multiplication"

# 0! = 1 is the empty product wearing a different hat, and n! = n (n-1)! read
# downwards from 1! = 1 gives the same answer by a second route. Both checked,
# because frame 15 offers the reader both and a further problem asks for them.
assert ZERO_FACTORIAL == EMPTY_PROD, "0! is no longer the empty product"
assert math.factorial(1) == 1 * ZERO_FACTORIAL, "the recurrence no longer forces 0! = 1"
assert math.prod(range(1, 5)) == math.factorial(4) == 24, "4! has moved"

TRANSCRIPT = Path(__file__).resolve().parents[1] / "figures" / "transcripts" / "f04-empty.txt"

# Every value below is interpolated from the run above. Nothing here is typed.
# A console block nobody ran is indistinguishable from one that was, which is
# exactly where a remembered number survives review.
TRANSCRIPT_TEXT = f""">>> import math
>>> sum([])                 # the loop never runs: total stays as it started
{EMPTY_SUM}
>>> math.prod([])           # the same loop, with a different accumulator
{EMPTY_PROD}
"""

# ==========================================================================
# Frame 16's claims about numpy, checked wherever numpy exists.
#
# numpy is NOT a dependency of this script -- `make numbers` must run on a
# plain python3 -- so this block ANNOUNCES ITSELF WHEN IT IS SKIPPED. A check
# that quietly does nothing is how a wrong number survives a draft.
#
# WHAT IS ASSERTED IS THE INVARIANT: the empty sum and the empty product agree
# with the stdlib's identities, and the two zero-divided-by-zero cases RETURN
# nan and RAISE NOTHING. That is the frame's whole point --- an empty sum is
# safe and an empty mean is not, so the guard belongs on the denominator.
#
# WHAT IS ONLY REPORTED is the warning text, because a warning string is a
# library-version fact. It is printed with the numpy version so the .tex author
# can see it and then NOT quote it. Note that np.array([]).mean() emits TWO
# warnings on this container, not the one the plan expected; a frame that
# quoted "the RuntimeWarning" would already be wrong.
# ==========================================================================
NUMPY_NOTE = "numpy absent: frame 16's nan claims were NOT checked in this run"
try:
    import warnings as _warnings

    import numpy as _np
except ImportError:                                  # pragma: no cover
    pass
else:
    assert float(_np.sum([])) == float(EMPTY_SUM), "np.sum([]) disagrees with sum([])"
    assert float(_np.prod([])) == float(EMPTY_PROD), "np.prod([]) disagrees with math.prod([])"

    _seen: list[str] = []
    for _label, _fn in (("scalar 0.0/0.0", lambda: _np.float64(0.0) / _np.float64(0.0)),
                        ("empty mean", lambda: _np.array([]).mean())):
        with _warnings.catch_warnings(record=True) as _w:
            _warnings.simplefilter("always")
            try:
                _got = _fn()
            except Exception as exc:                 # pragma: no cover
                raise AssertionError(
                    f"numpy's {_label} raised {type(exc).__name__}; the frame's "
                    f"claim is that it returns nan and carries on") from exc
        assert math.isnan(float(_got)), f"numpy's {_label} is no longer nan"
        _seen.append(f"{_label} -> nan, warnings: "
                     + ("; ".join(str(x.message) for x in _w) or "none"))
    NUMPY_NOTE = (f"numpy {_np.__version__}: " + " | ".join(_seen)
                  + "  -- warning TEXT is an observation, not an invariant: "
                    "do not quote it on the page")

# ==========================================================================
# Write the files the book reads.
# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f04.tex"


def main() -> None:
    assert TRANSCRIPT_TEXT.isascii(), "transcript must be ASCII: listings cannot set it otherwise"
    assert len(TRANSCRIPT_TEXT.strip().splitlines()) <= 14, "transcript too tall for one frame"
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.write_text(TRANSCRIPT_TEXT, encoding="ascii")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f04_sums.py --- do not edit.",
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
    print(f"  transcript -> {TRANSCRIPT.relative_to(TRANSCRIPT.parents[2])}")
    print(f"  bias correction on a constant sequence: worst |mhat - 1| over "
          f"t=1..{BIAS_STEPS} at beta 0.9 and 0.999 is {BIAS_WORST:.3e} "
          f"-- exact in algebra, NOT to the bit")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
