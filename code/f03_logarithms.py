#!/usr/bin/env python3
"""Program F3 --- Logarithms and logarithmic scales.

Every number Program F3 prints that the reader cannot do in their head is
computed here and written to figures/values/f03.tex, which the book \\input{}s.

F3 is the most load-bearing Foundation program in the book, and its numbers
carry more weight than F1's or F2's: the whole argument is that a product no
float can hold becomes a sum every float holds, and that claim is worth nothing
unless the underflow is measured rather than asserted. So the float formats are
not quoted from a table. Their smallest normal and smallest subnormal are found
by halving until the machine says zero, their significand widths are found by
searching for the epsilon, and the token count at which a sequence probability
underflows is found by running the product one token at a time and watching for
the first exact 0.0. The arithmetic that predicts each count is computed too,
and the script asserts that prediction and measurement agree --- because that
agreement IS frame 33's claim, and a claim the build cannot check is a claim
somebody will eventually break.

STDLIB ONLY, deliberately. float32 arithmetic is done with `struct`, which
round-trips through IEEE-754 binary32 including subnormals, rather than with
numpy. Two reasons: `make numbers` must run on a plain python3, and a result
that agrees between two independent implementations is worth more than a result
from the obvious one. (Cross-checked against numpy 2.4.6 while writing: the
same 44 and 150, the same 311 and 1075.)

NOT EMITTED, and none of it should be --- putting it behind \\val{} would be
theatre. This program teaches logarithms, so most of its arithmetic is the
thing being taught and stays inline as digits in the prose:

    log2 32 = 5;  log2 64 = 6;  log10 1000 = 3;  log_b 1 = 0;  log_b b = 1;
    log2 8 = 3, log10 100 = 2, log5 25 = 2;  3 + 4 = 7 in the index mirror;
    2000 * 2.4 = 4800, the summed log-probability itself, which is one
      multiplication and is the frame's punchline;
    three halvings from a loss of 4.0 to 0.5;  1/7 read as a seven-sided die;
    55, the naive midpoint of a logarithmic axis;
    the four decade ends of the learning-rate sweep, 1e-5 to 1e-2, which the
      exponents already give -- see the logspace note at the bottom of this
      file for the one place where the library and the exponents part company.

THREE VALUES THE PLAN NAMED THAT ARE DELIBERATELY NOT EMITTED HERE, because
emitting them would print one quantity twice --- the defect F1's script calls
out by name, and the reason F1 does not emit the 2^10-against-10^3 error and
the kilo/kibi gap separately:

    f03.two.eighty.err.pct  is f01.two.eighty.err.pct. Frame 7 re-derives F1's
        number by the logarithm route and must be seen to quote it, so it
        references the F01 key. This script asserts the two agree.
    f03.loss.p10 and f03.loss.gap.low are both ln 10, to the digit. One key,
        f03.ln.ten, serves the p = 0.1 row of frame 28's table AND the low gap
        of frame 29 --- which is what makes frame 29's sentence ("a factor of
        ten whose logarithm is ln 10 exactly") visibly true rather than a
        coincidence the reader has to take on trust.

CROSS-PROGRAM REUSE, and it is deliberate. Frames 27, 30 and 38 quote
\\val{f02.loss.nats} and \\val{f02.prob.from.loss} rather than new f03 keys,
because F3 is paying back a debt F2 recorded in its own prose (F2 section 7
rearranged L = -ln p to p = e^-L and said in as many words that the last step
was F3's and was taken on trust). The two programs must be provably quoting one
number. \\mfaval keys are global --- figures/values/all.tex inputs every file
--- so this works; it is the first cross-program value reuse in the book, and
a later pass deleting an f02 key would silently break F3.

Run:  python3 code/f03_logarithms.py      (or: make numbers)
"""
from __future__ import annotations

import math
import struct
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


def f32(x: float) -> float:
    """x rounded to IEEE-754 binary32 and handed back as a Python float.

    struct does the conversion in the C library, so subnormals round correctly
    and the flush to zero happens where the format says it happens rather than
    where this script thinks it should.
    """
    return struct.unpack("<f", struct.pack("<f", x))[0]


IDENTITY = float          # the "rounding" that binary64 arithmetic already does

# ==========================================================================
# SECTION 2 --- the base, and the three constants worth holding
#
# The whole program turns on one fact: changing the base multiplies by a
# constant. Every logarithm curve is every other one scaled vertically, which
# is why the shape of a plotted curve can never tell you its base -- and why
# frame 41's two model cards are the same model.
# ==========================================================================
LN10 = math.log(10.0)
LN2 = math.log(2.0)

# Frame 9's trap needs ln 1000 to enough digits to match a transcript, because
# the frame prints `math.log(1000)` beside it and a truncated copy would read
# as a different number. Six decimals is what the REPL's first seven significant
# figures come to: 6.907755278982137.
emit("f03.ln.thousand", math.log(1000.0), 6)

emit("f03.ln.two", LN2, 4)                       # also -ln 0.5, frame 28's row
emit("f03.inv.ln.two", 1.0 / LN2, 4)             # nats -> bits, frames 11 and 41
emit("f03.log10.two", math.log10(2.0), 5)        # frames 7 and 46: ONE key
emit("f03.log2.ten", math.log(10.0) / LN2, 4)    # derived, not math.log2, so the
                                                 # change-of-base step is visible
emit("f03.ln.ten", LN10, 4)                      # frame 28's p=0.1 row AND
                                                 # frame 29's low gap: one number

# A loss quoted in nats against the same loss quoted in bits. Frame 12 converts
# it forwards; frame 41 is the trap that turns on a reader who did not.
#
#   2.4 / ln 2 = 2.4 * 1.4427 = 3.4625
#
# The percentage is stated the way F1 insists a ratio is stated: N per cent
# ABOVE the nats figure, naming both quantities. It is (1/ln 2 - 1) * 100 and
# therefore does not depend on the 2.4 at all, which is the point of frame 41 --
# the gap is a property of the units, not of the model.
LOSS_NATS = 2.4                                  # F2's loss, quoted not re-chosen
emit("f03.nats.to.bits", LOSS_NATS / LN2, 4)
emit("f03.bits.over.nats.pct", (1.0 / LN2 - 1.0) * 100.0, 2)

# ==========================================================================
# SECTION 1 --- how slowly a logarithm grows, and F1's 2^80 answered again
#
# F1 needed the whole 25-digit integer to compare 2^80 with 10^24. One product
# does it here:  log10(2^80) = 80 * log10 2 = 24.0824, so 2^80 is 10^24.08.
# The number of decimal digits of a positive integer n is floor(log10 n) + 1.
# ==========================================================================
TWO_EIGHTY_EXP = 80.0 * math.log10(2.0)
emit("f03.two.eighty.exp", TWO_EIGHTY_EXP, 4)
emit("f03.two.eighty.digits", math.floor(TWO_EIGHTY_EXP) + 1)

# The digit count is the whole claim of frame 7, so the build checks it against
# the integer itself rather than against the author's memory.
assert math.floor(TWO_EIGHTY_EXP) + 1 == len(str(2**80)), "digit count is wrong"

# And frame 7 quotes F1's percentage back. Re-derived here so that a change to
# F1's emitter cannot leave F3 quoting a number F1 has stopped printing. The
# comparison is on the rounded body, because the rounded body is what prints.
_f1 = (2**80 / 10**24 - 1) * 100
assert f"{_f1:.2f}" == "20.89", f"F01's 2^80 gap moved: {_f1:.2f}"

# ==========================================================================
# SECTION 3 --- the three laws, and the trap that there is no fourth
#
# Frame 21 falsifies ln(a+b) = ln a + ln b at a = 2, b = 3. The wrong answer is
# not merely wrong: ln 2 + ln 3 = ln 6, so the reader computed the logarithm of
# a product they were never given. That is why ONE key is emitted for both the
# claimed sum and ln 6 -- they are the same number, and the frame's sentence
# depends on the reader seeing that they are.
# ==========================================================================
emit("f03.ln.five", math.log(5.0), 4)            # the truth:  ln(2+3)
emit("f03.ln.six", math.log(6.0), 4)             # the wrong rule's answer, = ln 2 + ln 3
assert abs(math.log(6.0) - (LN2 + math.log(3.0))) < 1e-12

# Frame 22-23: what you do when you must have ln(e^u + e^v) and u, v are
# already logarithms. Factor the larger exponential out --
#
#     ln(e^u + e^v) = v + ln(1 + e^(u-v))       for v >= u
#
# -- which never forms e^1000 at all. Computed with log1p, because for a large
# negative u - v the 1 + x loses every significant digit of x otherwise. The
# stability argument in full belongs to P02; this is the algebra it rests on.
LSE_U, LSE_V = 1000.0, 1001.0
_hi, _lo = max(LSE_U, LSE_V), min(LSE_U, LSE_V)
emit("f03.logsumexp.pair", _hi + math.log1p(math.exp(_lo - _hi)), 4)

# ==========================================================================
# SECTION 4 --- undoing an exponential, and F2's debt paid
#
# Solving b^x = c in one move: x = ln c / ln b. Frame 26 works 2^x = 1000.
# ==========================================================================
emit("f03.log2.thousand", math.log(1000.0) / LN2, 4)

# ==========================================================================
# SECTION 4 continued --- a probability and a loss are one quantity on two
# scales. L = -ln p, so p = e^-L.
#
# Frame 28's table, all four rows at ONE precision because the frame sets them
# in one column and a reader comparing 0.1054 with 4.61 is entitled to think
# one of them was rounded for effect. The p = 0.5 row is f03.ln.two and the
# p = 0.1 row is f03.ln.ten, already emitted above.
#
# Frame 29 is the sentence section 7 rests on. In probability the two changes
# are 0.9 -> 0.5 (a fall of 0.4) and 0.1 -> 0.01 (a fall of 0.09), so the first
# looks four times the larger. In loss they are 0.5878 and 2.3026, so the
# second is four times the larger. Neither is wrong: the logarithm converts
# ratios into differences, and 0.1 -> 0.01 is a factor of ten exactly.
# ==========================================================================
emit("f03.loss.p90", -math.log(0.9), 4)
emit("f03.loss.p01", -math.log(0.01), 4)
emit("f03.loss.gap.high", -math.log(0.5) - -math.log(0.9), 4)
# The low gap is -ln(0.01) - -ln(0.1) = ln 10 = f03.ln.ten. Not emitted twice.
assert abs((-math.log(0.01) - -math.log(0.1)) - LN10) < 1e-12

# ==========================================================================
# SECTION 5 --- the payoff. Why a language model works in log space.
#
# The per-token probability is F2's, and it is quoted rather than re-chosen:
# F2 emitted p = e^-2.4 = 0.0907 and the book prints that key in frames 30, 31
# and 38. The arithmetic below therefore uses the exact e^-2.4 and not the
# four-decimal display of it, which is what makes the sequence log-probability
# come out at exactly -4800 nats.
# ==========================================================================
SEQ_TOKENS = 2000
P_TOKEN = math.exp(-LOSS_NATS)                   # = f02.prob.from.loss = 0.0907
emit("f03.seq.tokens", SEQ_TOKENS)

# The thesis, executed. The product cannot be formed -- it has over two
# thousand leading zeros -- but the SUM can, in one multiplication:
#
#     ln p(seq) = sum of 2000 copies of ln p = 2000 * -2.4 = -4800 nats
#
# and a base change puts that on the decimal scale the reader can read:
#
#     log10 p(seq) = -4800 / ln 10 = -2084.614,  so p(seq) = 10^-2084.614
#
# THREE decimals on the exponent, not two, and it is a reproduce-from-the-
# page constraint rather than a precision preference: 10^-2084.61 is
# 2.455e-2085 against the mantissa's 2.43, so the two printed forms of one
# number disagreed. The assertion below holds them together.
#
# The mantissa and exponent are split out so the frame can print an ordinary
# piece of scientific notation. Not emitted separately: -4800 itself, which is
# 2000 x 2.4 and is the head arithmetic the frame is teaching.
SEQ_LOGPROB_NATS = SEQ_TOKENS * math.log(P_TOKEN)
SEQ_LOG10 = SEQ_LOGPROB_NATS / LN10
emit("f03.seq.prod.log10", SEQ_LOG10, 3)

_exponent = math.floor(SEQ_LOG10)
_mantissa = 10.0 ** (SEQ_LOG10 - _exponent)
emit("f03.seq.prod", f"{_mantissa:.2f}e{_exponent}")

# The page prints both forms within four lines of each other, so a reader
# will undo one and compare. Assert on the PRINTED strings, which is the
# only form anybody checks.
_printed_exp = f"{SEQ_LOG10:.3f}"
_undone = 10.0 ** (float(_printed_exp) - math.floor(float(_printed_exp)))
assert f"{_undone:.2f}" == f"{_mantissa:.2f}", (
    f"the page prints 10^{_printed_exp}, which undoes to {_undone:.2f}, "
    f"beside a mantissa of {_mantissa:.2f}: two printed forms of one number "
    f"that a reader can put side by side and find different")

# Two routes to the same number, so the script demonstrates its own thesis:
# summing 2000 logarithms and taking one logarithm of the product are the same
# computation, and only one of them can be carried out.
assert abs(SEQ_LOGPROB_NATS - SEQ_TOKENS * -LOSS_NATS) < 1e-9
assert abs(SEQ_LOG10 - SEQ_TOKENS * math.log10(P_TOKEN)) < 1e-9

# --------------------------------------------------------------------------
# What the two float formats can actually hold. MEASURED, not quoted.
#
# Smallest positive subnormal: halve until the machine says zero, and keep the
# last value that did not. Significand width: halve an epsilon until 1 + eps
# stops being distinguishable from 1, which counts the bits after the leading
# one. Smallest positive NORMAL: the subnormals fill the binade below the
# smallest normal at a fixed spacing, so the smallest normal is the smallest
# subnormal shifted left by the significand width --
#
#     binary32:  2^-149 * 2^23  = 2^-126 = 1.18e-38
#     binary64:  2^-1074 * 2^52 = 2^-1022 = 2.23e-308
#
# -- which is derived from two measurements rather than read off a table. What
# a subnormal IS belongs to P01; F3 needs only the floor it puts under a
# product.
# --------------------------------------------------------------------------
def smallest_subnormal(round_to) -> float:
    x = round_to(1.0)
    while round_to(x / 2.0) != 0.0:
        x = round_to(x / 2.0)
    return x


def significand_bits(round_to) -> int:
    eps, bits = round_to(1.0), 0
    while round_to(1.0 + eps / 2.0) != 1.0:
        eps, bits = round_to(eps / 2.0), bits + 1
    return bits


F32_SUB = smallest_subnormal(f32)
F64_SUB = smallest_subnormal(IDENTITY)
F32_TINY = F32_SUB * 2 ** significand_bits(f32)
F64_TINY = F64_SUB * 2 ** significand_bits(IDENTITY)

emit("f03.f32.tiny", sci(F32_TINY, 2))
emit("f03.f32.sub", sci(F32_SUB, 2))
emit("f03.f64.tiny", sci(F64_TINY, 2))
emit("f03.f64.sub", sci(F64_SUB, 2))

# --------------------------------------------------------------------------
# The cliff. At p per token the running product is p^n, so it reaches the
# format's floor at
#
#     n = ln(smallest subnormal) / ln p
#
# and the first n at which the product rounds to exactly 0.0 is the next whole
# number after that. Both the prediction and the measurement are emitted,
# because frame 33's whole claim is that they agree; the measurement is a loop
# that multiplies one token at a time and rounds to the format at every step,
# which is what a running product in that format actually does.
# --------------------------------------------------------------------------
def tokens_until_zero(round_to, p: float) -> int:
    prod, n = round_to(1.0), 0
    while prod != 0.0:
        n += 1
        prod = round_to(prod * round_to(p))
    return n


def predicted_tokens(sub: float, p: float) -> float:
    return math.log(sub) / math.log(p)


F32_PREDICT = predicted_tokens(F32_SUB, P_TOKEN)
F64_PREDICT = predicted_tokens(F64_SUB, P_TOKEN)
F32_ZERO_AT = tokens_until_zero(f32, P_TOKEN)
F64_ZERO_AT = tokens_until_zero(IDENTITY, P_TOKEN)

emit("f03.f32.predict", F32_PREDICT, 2)
emit("f03.f32.zero.at", F32_ZERO_AT)
emit("f03.f64.predict", F64_PREDICT, 2)
emit("f03.f64.zero.at", F64_ZERO_AT)

# Frame 33 says prediction and measurement agree. The build checks it, because
# a claim of agreement that nobody checks is a claim somebody will break.
assert F32_ZERO_AT == math.floor(F32_PREDICT) + 1, "float32 cliff moved"
assert F64_ZERO_AT == math.floor(F64_PREDICT) + 1, "float64 cliff moved"

# Frame 36-37's \yourturn, at p = 0.5. The predictions are exactly 149 and 1074
# because the smallest subnormals are exactly 2^-149 and 2^-1074, so this case
# also checks that the two derivations above are consistent with each other.
HALF = 0.5
HALF_F32 = tokens_until_zero(f32, HALF)
HALF_F64 = tokens_until_zero(IDENTITY, HALF)
emit("f03.half.f32.zero", HALF_F32)
emit("f03.half.f64.zero", HALF_F64)
assert predicted_tokens(F32_SUB, HALF) == 149.0
assert predicted_tokens(F64_SUB, HALF) == 1074.0
assert (HALF_F32, HALF_F64) == (150, 1075)

# ==========================================================================
# SECTION 6 --- perplexity: the exponential of a mean logarithm
#
# Mean negative log-likelihood -> perplexity is exp of the mean, and that is
# the reciprocal of the geometric mean of the token probabilities:
#
#     PPL = exp(mean NLL) = exp(2.4) = 11.02 = 1 / 0.0907
#
# Both readings are one quantity, so one key. The units question -- perplexity
# as the exponential of a cross-entropy, and what that is in bits -- belongs to
# P29 and F3 hands it over by name.
# ==========================================================================
PPL = math.exp(LOSS_NATS)
emit("f03.ppl", PPL, 2)
assert abs(PPL - 1.0 / P_TOKEN) < 1e-9, "perplexity is not 1 / geometric mean"

# Frame 39 runs it backwards from a reported perplexity of 7: a fair
# seven-sided die at every step.
PPL_SEVEN = 7.0
emit("f03.ppl.seven.p", 1.0 / PPL_SEVEN, 4)
emit("f03.ppl.seven.nats", math.log(PPL_SEVEN), 4)
emit("f03.ppl.seven.bits", math.log(PPL_SEVEN) / LN2, 4)

# ... against the ceiling, which is what makes 7 mean something: a model that
# had learnt nothing would spread its probability over the whole vocabulary,
# giving a perplexity equal to the vocabulary size.
#
# THE VOCABULARY SIZE IS A STATED ROUND FIGURE, NOT A MEASURED ONE. The obvious
# number to print is a particular tokeniser's, and no tokeniser is installed
# here, so printing one would be a remembered number wearing a computed
# number's clothes -- which is the failure mode this whole apparatus exists to
# prevent. Fifty thousand is honest, is what the frame says in words ("about
# fifty thousand"), and is one constant to change if a real vocab_size is ever
# opened at the keyboard.
VOCAB = 50_000
emit("f03.vocab", VOCAB)
emit("f03.vocab.nats", math.log(VOCAB), 4)
emit("f03.vocab.bits", math.log(VOCAB) / LN2, 4)

# ==========================================================================
# SECTION 6 continued --- ranking candidates, and two kinds of mean
#
# Two candidates the model is equally confident about, at 0.9 per token: one 3
# tokens long, one 20. Summed log-probability prefers the short one every time,
# whatever the model thinks, because every extra token adds a negative number.
# The MEANS are identical -- the same ln 0.9 -- which is why implementations
# rank by the mean and not by the sum.
#
# Five decimal places on the mean, and four on everything else in this block.
# That is a deliberate split, not an oversight: the mean's whole job in frame 43
# is to be the SAME for both candidates, and two figures that agree to four
# places invite the reader to wonder about the fifth. Note also that this mean
# is the negative of f03.loss.p90 -- one is a mean log-probability and the other
# a loss, they are printed fourteen frames apart, and the sign is the point.
# ==========================================================================
BEAM_P = 0.9
BEAM_SHORT, BEAM_LONG = 3, 20
emit("f03.beam.short.sum", BEAM_SHORT * math.log(BEAM_P), 4)
emit("f03.beam.long.sum", BEAM_LONG * math.log(BEAM_P), 4)
emit("f03.beam.mean", math.log(BEAM_P), 5)

# Arithmetic against geometric mean of four token probabilities. The geometric
# mean is exp of the mean logarithm, which is the definition F3 has been
# building all program; it is computed that way rather than as a fourth root,
# so the script does what the frames say. The inequality between them -- and
# the fact that an average of perplexities is not the perplexity of the average
# -- has a name and an owner, and both are P19's.
PROBS = (0.5, 0.2, 0.9, 0.05)
_am = sum(PROBS) / len(PROBS)
_gm = math.exp(sum(math.log(p) for p in PROBS) / len(PROBS))
emit("f03.am", _am, 4)
emit("f03.gm", _gm, 4)
assert _gm < _am, "geometric mean must not exceed arithmetic mean"

# ==========================================================================
# SECTION 7 --- logarithmic scales, and reading a plot
#
# Halfway between two ticks on a logarithmic axis is the GEOMETRIC mean, not
# the arithmetic one: equal distances along the axis are equal ratios. Computed
# by the same exp-of-mean-logarithm route as above, because it is the same
# quantity arriving in a second place -- which is the sentence frame 45 makes.
# The naive answer, 55, is head arithmetic and stays inline.
# ==========================================================================
AXIS_LO, AXIS_HI = 10.0, 100.0
emit("f03.axis.mid", math.exp((math.log(AXIS_LO) + math.log(AXIS_HI)) / 2), 2)

# A learning-rate sweep of four trials from 1e-5 to 1e-2. On a log grid the
# four points are the four decade ends and the exponents give them away. On a
# linear grid they are 1e-5 + k * (1e-2 - 1e-5) / 3, which puts three of the
# four in the top decade and nothing at all between 1e-5 and 0.00334 -- which
# is where a learning rate usually lives.
#
# linspace and logspace are written out rather than imported, both because this
# script is stdlib-only and because the arithmetic is the argument. Checked
# against numpy 2.4.6 while writing: the same four values to every digit.
SWEEP_LO_EXP, SWEEP_HI_EXP, SWEEP_N = -5, -2, 4


def linspace(lo: float, hi: float, n: int) -> list[float]:
    return [lo + k * (hi - lo) / (n - 1) for k in range(n)]


def logspace(lo_exp: float, hi_exp: float, n: int) -> list[float]:
    return [10.0**e for e in linspace(lo_exp, hi_exp, n)]


_lin = linspace(10.0**SWEEP_LO_EXP, 10.0**SWEEP_HI_EXP, SWEEP_N)
_log = logspace(SWEEP_LO_EXP, SWEEP_HI_EXP, SWEEP_N)
emit("f03.sweep.lin.second", _lin[1], 5)
emit("f03.sweep.lin.top.decade", sum(1 for x in _lin if x >= 10.0**(SWEEP_HI_EXP - 1)))

# The log grid lands on the decade ends EXACTLY, and "exactly" is now checked
# by bit pattern rather than by rounding. The old form rounded log10 to nine
# decimals, which is a comparison nothing within a few hundred ulp of the right
# answer can fail -- and a guard that cannot fail is a guard that has already
# stopped working. That mattered here: frame 48 used to say np.logspace
# "returns exactly those four", and it does not.
assert [struct.pack("<d", x) for x in _log] == \
       [struct.pack("<d", v) for v in (1e-5, 1e-4, 1e-3, 1e-2)], \
       "the exponent route no longer lands on the decade ends to the bit"

# ...and the claim frame 48 makes ABOUT NUMPY is gated wherever numpy exists.
# numpy is not a dependency of this script -- `make numbers` must run on a
# plain python3 -- so the check ANNOUNCES ITSELF WHEN IT IS SKIPPED rather than
# passing silently. A check that quietly does nothing is how a wrong number
# survives a draft.
#
# What is checked is the sentence in the note box: three of the four values
# are the decade ends to the bit and the first is one ulp below 1e-5, which
# numpy's own repr hides by printing 1.e-05 for it.
NUMPY_NOTE = ("numpy absent: frame 48's np.logspace claim was NOT checked "
              "in this run")
try:
    import numpy as _np
except ImportError:                                  # pragma: no cover
    pass
else:
    _np_log = [float(x) for x in
               _np.logspace(SWEEP_LO_EXP, SWEEP_HI_EXP, SWEEP_N)]

    # DO NOT assert which of the two values comes back. It is not universal:
    # this container returns the value one ulp below 1e-5 and CI returns 1e-5
    # exactly, and the earlier version of this script asserted the first and
    # failed the build on the second. The frame's note box used to assert it
    # too, which is the same defect written into the page rather than into a
    # test -- a claim about a library's behaviour that the reader can run and
    # find false.
    #
    # What IS universal, and is the teaching point, is that the printed form
    # is `1.e-05` either way, so the repr does not tell you which you have.
    # The note box now says exactly that and sends the reader to .hex().
    _lo, _hi = math.nextafter(1e-5, 0.0), math.nextafter(1e-5, 1.0)
    assert _lo <= _np_log[0] <= _hi, (
        f"np.logspace's first element is not within one ulp of 1e-5: "
        f"{_np_log[0]!r}")
    assert _np_log[1:] == [1e-4, 1e-3, 1e-2], (
        f"np.logspace's other three are no longer the decade ends: {_np_log!r}")
    _exact = _np_log[0] == 1e-5
    NUMPY_NOTE = (
        f"numpy {_np.__version__}: np.logspace(-5, -2, 4)[0] is "
        f"{'exactly 1e-5' if _exact else 'one ulp below 1e-5'} "
        f"({float(_np_log[0]).hex()}) -- BUILD-DEPENDENT, and frame 48 says so "
        f"rather than picking one")

# ==========================================================================
# The transcript frame 33 carries.
#
# No transcript in this book is typed. A console block nobody ran is
# indistinguishable from one that was, and that is exactly where a remembered
# number survives review -- the companion volume's only outright factual error
# lived inside one for a whole draft. So the numbers in this file are the
# measurements above, interpolated, and cannot disagree with the values the
# frame prints beside it.
#
# One file serves both editions: listing comments stay English by standing
# rule, so it contributes no digits to either edition's .tex and parity's C12
# has nothing to compare. Parity's C13 cannot see it either -- VERB_ENV_RE
# scans in-source environments only -- so the ASCII rule is enforced here, by
# assertion, rather than by a gate.
#
# EVERY digit below is interpolated, the comment included. It said "about
# 0.0907 per token" as a literal, which is P_TOKEN written twice: change
# LOSS_NATS and the transcript's own comment would have gone on quoting the
# old probability. A transcript is not exempt from the rule that the book
# holds references and the script holds digits -- it is the place that rule is
# easiest to forget, because the file already looks like output.
# ==========================================================================
TRANSCRIPT = Path(__file__).resolve().parents[1] / "figures" / "transcripts" / "f03-underflow.txt"

TRANSCRIPT_TEXT = f""">>> import math, struct
>>> f32 = lambda x: struct.unpack('<f', struct.pack('<f', x))[0]
>>> p = math.exp(-{LOSS_NATS})                 # about {P_TOKEN:.4f} per token
>>> def tokens_until_zero(round_to):
...     prod, n = round_to(1.0), 0
...     while prod != 0.0:
...         n += 1; prod = round_to(prod * round_to(p))
...     return n
...
>>> tokens_until_zero(float)           # float64
{F64_ZERO_AT}
>>> tokens_until_zero(f32)             # float32
{F32_ZERO_AT}
"""

# ==========================================================================
# Write the files the book reads.
# ==========================================================================
OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "f03.tex"


def main() -> None:
    assert TRANSCRIPT_TEXT.isascii(), "transcript must be ASCII: listings cannot set it otherwise"
    assert len(TRANSCRIPT_TEXT.strip().splitlines()) <= 14, "transcript too tall for one frame"
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.write_text(TRANSCRIPT_TEXT, encoding="ascii")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/f03_logarithms.py --- do not edit.",
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
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
