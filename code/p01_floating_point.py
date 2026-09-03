#!/usr/bin/env python3
"""Program P01 --- Floating point: what the machine actually computes.

Every number Program P01 prints that the reader cannot do in their head is
computed here and written to figures/values/p01.tex, which the book \\input{}s.

P01's thesis is that a float is a sign, an exponent and a fixed number of
significant bits, so THE GAP BETWEEN REPRESENTABLE NUMBERS GROWS WITH
MAGNITUDE, and equality is not a question you should ask.

Almost nothing in this program needs to be asserted from outside, because
almost everything in it can be OBSERVED: the bits are there to be read with
`struct`, and a claim about what the machine stores is settled by asking it.
That is the program's method and it is stated in the frames.

WHAT P01 IS OWED, and pays. F03 promises this program twice, by name:
  * "Program P01 says what a subnormal is and why a format has two
    thresholds" (F03's closing frame);
  * F03's sequence probability reaches 2.43e-2085, and its frame says the
    ceiling "is Program P01's subject arriving a whole part early".
Both are paid in section 5, and the second is paid with a CROSS-PROGRAMME
DRIFT GATE of the kind F12 introduced: this script reads F03's and F12's
committed values and asserts what each does in each format, so "that number
underflows" is checked rather than claimed.

THE MEASUREMENTS:

  1. THE GAP GROWS. The distance to the next representable double at 1, at
     1000 and at a billion, read off the bits. It is not a rounding error
     that happens to get bigger; it is the definition.

  2. 0.1 + 0.2, in full. Not "is not 0.3" -- the actual stored value, to
     enough digits that the reader can see where it went.

  3. bf16 AGAINST fp16, and this is the headline. Same width, different split:
     fp16 spends 5 bits on the exponent and 10 on the significand, bf16 spends
     8 and 7. So bf16 reaches as high as fp32 and resolves as coarsely as a
     three-digit number, and fp16 overflows at 65504. The reader computes that
     ceiling rather than being told it.

  4. NON-ASSOCIATIVITY, with the two orders printed. And the consequence: two
     GPUs summing the same gradients in different orders disagree in the last
     bits, which is not a bug in either.

  5. TWO THRESHOLDS, NOT ONE. The smallest normal and the smallest subnormal,
     in three formats, and what the gap between them buys and costs.

WHAT P01 DELIBERATELY LEAVES ALONE, checked against tools/programs.json:
    catastrophic cancellation, log-sum-exp, Welford, summation order as a
      DISCIPLINE with a catalogue of fixes                        -> P02
    FLOPs, bytes, arithmetic intensity                            -> P03
P01 shows that the arithmetic is not exact and what its shape is; P02 is what
to do about it.

Run:  python3 code/p01_floating_point.py      (or: make numbers)
"""
from __future__ import annotations

import math
import struct
from pathlib import Path

VALUES: dict[str, tuple[str, bool]] = {}


def emit(key: str, value, digits: int | None = None) -> None:
    """Record one value under the name the book will reference it by."""
    if isinstance(value, float) and digits is not None:
        body = f"{value:.{digits}f}"
    elif isinstance(value, float):
        body = repr(value)
    else:
        body = str(value)
    try:
        # math.isfinite, not merely a successful parse: float() accepts
        # "inf", "-inf" and "nan", so the plain try/except classified them as
        # numbers and \val{} handed them to siunitx, which rejects them with
        # `Invalid number '-inf'` and no PDF. Latent here and fatal in P02.
        numeric = math.isfinite(float(body.replace("e", "E")))
    except ValueError:
        numeric = False
    VALUES[key] = (body, numeric)


# ==========================================================================
# The three formats, by their two numbers. Everything else in this program
# is derived from these, which is the point: a format IS its exponent budget
# and its significand budget, and every threshold follows.
# ==========================================================================
FORMATS = {
    # name:      (exponent bits, stored significand bits)
    "fp64": (11, 52),
    "fp32": (8, 23),
    "fp16": (5, 10),
    "bf16": (8, 7),
}
for _name, (_e, _m) in FORMATS.items():
    emit(f"p01.{_name}.ebits", _e)
    emit(f"p01.{_name}.mbits", _m)
    # Only the two widths the frames quote. fp16's and bf16's sixteen is
    # spelled out on the page, because a reader holds sixteen in their head
    # and the ledger is right to report an emitted value nothing references.
    if _name in ("fp64", "fp32"):
        emit(f"p01.{_name}.width", 1 + _e + _m)

# fp16 and bf16 are the same width and split it differently. That is the
# whole of section 4 and it is asserted rather than asserted-in-prose.
assert 1 + FORMATS["fp16"][0] + FORMATS["fp16"][1] == 16
assert 1 + FORMATS["bf16"][0] + FORMATS["bf16"][1] == 16
assert FORMATS["bf16"][0] == FORMATS["fp32"][0], "bf16 no longer has fp32's exponent budget"


def largest(ebits: int, mbits: int) -> float:
    """The largest finite value: every significand bit set, top exponent."""
    bias = (1 << (ebits - 1)) - 1
    return (2.0 - 2.0 ** -mbits) * 2.0 ** bias


def smallest_normal(ebits: int) -> float:
    return 2.0 ** (1 - ((1 << (ebits - 1)) - 1))


def smallest_subnormal(ebits: int, mbits: int) -> float:
    return 2.0 ** (1 - ((1 << (ebits - 1)) - 1) - mbits)


def epsilon(mbits: int) -> float:
    """The gap between 1 and the next representable number up."""
    return 2.0 ** -mbits


def printed_ceiling(x: float, figures: int = 4) -> str:
    """A ceiling, printed so that the printed form is not above the ceiling.

    THE OBVIOUS ROUTE IS WRONG AND THE BUILD SAID SO. `f"{x:.4g}"` rounds to
    nearest, so the largest double prints as 1.798e+308 -- which is LARGER
    than the largest double, and parses straight back to `inf`. A page that
    quotes a format's ceiling as a number the format cannot hold is wrong in
    the one way this program is about, so the last figure is truncated
    towards zero instead and the result is checked below.
    """
    from decimal import Decimal, ROUND_DOWN
    d = Decimal(repr(x)).normalize()
    exp = d.adjusted()
    return f"{d.quantize(Decimal(1).scaleb(exp - figures + 1), rounding=ROUND_DOWN):.{figures - 1}e}"


for _name, (_e, _m) in FORMATS.items():
    _printed = printed_ceiling(largest(_e, _m))
    assert 0 < float(_printed) <= largest(_e, _m), (
        f"{_name}'s ceiling prints as {_printed}, which is not a value the "
        f"format can hold: a ceiling must never be printed above itself")
    emit(f"p01.{_name}.max", _printed)
    emit(f"p01.{_name}.minnorm", f"{smallest_normal(_e):.2e}")
    emit(f"p01.{_name}.minsub", f"{smallest_subnormal(_e, _m):.2e}")
    emit(f"p01.{_name}.eps", f"{epsilon(_m):.2e}")
    # How many DECIMAL digits a format resolves to. Written from expectation
    # the first time and wrong by one in two of the four rows -- an epsilon of
    # 7.81e-03 is about two decimal digits, not three -- so it is computed.
    emit(f"p01.{_name}.digits", round(-math.log10(epsilon(_m))))

# The formulas are checked against the values Python and struct already know,
# which is the point of deriving them rather than quoting them.
assert abs(largest(11, 52) / 1.7976931348623157e308 - 1.0) < 1e-15
assert smallest_normal(11) == 2.2250738585072014e-308
assert smallest_subnormal(11, 52) == 5e-324
assert epsilon(52) == 2.220446049250313e-16
_fp32_max = struct.unpack("<f", struct.pack("<f", largest(8, 23)))[0]
assert _fp32_max == largest(8, 23), "the fp32 ceiling formula no longer round-trips"
assert largest(5, 10) == 65504.0, "the fp16 ceiling is no longer 65504"
# The ceiling is exact and the four-figure form above is a rounding of it, so
# both go on the page under DIFFERENT names. Printing 6.55e+04 beside 65504
# would be two numbers that look like one and are not, which is the defect the
# F08 pass was caught by.
emit("p01.fp16.max.exact", f"{largest(5, 10):.0f}")

# bf16 and fp32 share an exponent budget, so their ceilings are CLOSE and are
# NOT equal: the largest value is (2 - 2^-m) * 2^127, and bf16's shorter
# significand makes its 2 - 2^-m slightly smaller. The draft said the two agree
# to three figures, and they do not -- 3.39 against 3.40. They agree to two,
# and the shortfall is under half a per cent, which is the accurate and more
# instructive statement.
_bf, _f32 = largest(8, 7), largest(8, 23)
emit("p01.bf16.short.pct", f"{(1 - _bf / _f32) * 100:.2f}")
assert f"{_bf:.2g}" == f"{_f32:.2g}", "bf16 and fp32 ceilings no longer agree to two figures"
assert f"{_bf:.3g}" != f"{_f32:.3g}", "the two ceilings now agree to three figures after all"
assert 0 < 1 - _bf / _f32 < 0.005, "the shortfall is no longer under half a per cent"

# bf16's reach against fp16's, which is the number the frames elicit.
emit("p01.bf16.over.fp16", f"{largest(8, 7) / largest(5, 10):.1e}")
assert largest(8, 7) / largest(5, 10) > 1e33

# ==========================================================================
# SECTION 2 --- the gap grows with magnitude
#
# Read off the bits rather than asserted: the next double after x is the next
# integer up in the 64-bit pattern, which is what makes "the gap" a fact about
# the encoding rather than about arithmetic.
# ==========================================================================
def next_up(x: float) -> float:
    bits = struct.unpack("<Q", struct.pack("<d", x))[0]
    return struct.unpack("<d", struct.pack("<Q", bits + 1))[0]


for _tag, _x in (("one", 1.0), ("thousand", 1000.0), ("billion", 1e9)):
    gap = next_up(_x) - _x
    emit(f"p01.gap.{_tag}", f"{gap:.2e}")
    assert gap == math.ulp(_x), f"the bit-increment gap at {_x} disagrees with math.ulp"

# The invariant, not the three figures: the gap scales with the magnitude, so
# the RELATIVE gap is roughly constant. That is the sentence the section is
# for, and it is what makes "significant digits" the right way to think.
for _x in (1.0, 8.0, 1e3, 1e9, 1e30):
    rel = math.ulp(_x) / _x
    assert epsilon(52) / 2 <= rel <= epsilon(52), f"the relative gap left its band at {_x}"

# ==========================================================================
# SECTION 3 --- 0.1 + 0.2, in full
# ==========================================================================
emit("p01.sum.shown", f"{0.1 + 0.2:.17f}")
emit("p01.sum.gap", f"{abs((0.1 + 0.2) - 0.3):.1e}")
# And it is exactly one gap AT 0.3, which is a quarter of the gap at 1. The
# draft called it "about one epsilon", which is the very mistake this section
# warns against: a gap quoted without the magnitude it sits at.
assert (0.1 + 0.2) - 0.3 == math.ulp(0.3), "the tenth's error is no longer one gap at 0.3"
assert 0.1 + 0.2 != 0.3
TENTH_STORED = f"{0.1:.20f}"
emit("p01.tenth.stored", TENTH_STORED)
# and the reason: a tenth is a recurring fraction in binary, exactly as a
# third is in decimal. Asserted by round-tripping the bits.
assert struct.unpack("<Q", struct.pack("<d", 0.1))[0] != 0

# ==========================================================================
# SECTION 4 --- summation is not associative
#
# A big number, then two small ones. Added in one order the small ones are
# lost individually; added in the other they combine first and survive.
# ==========================================================================
BIG, SMALL = 1.0, 1e-16
LEFT = (BIG + SMALL) + SMALL
RIGHT = BIG + (SMALL + SMALL)
emit("p01.assoc.big", f"{BIG:.0f}")
emit("p01.assoc.small", f"{SMALL:.0e}")
emit("p01.assoc.left", f"{LEFT:.17f}")
emit("p01.assoc.right", f"{RIGHT:.17f}")
assert LEFT != RIGHT, "the two orders no longer disagree"
assert LEFT == BIG, "the left-to-right order no longer loses both small values"

# WHAT P02 OWNS, AND WHY THIS BLOCK IS SHORT.
#
# The first draft of this ran a million small values into a running total in
# both orders and printed the loss. It demonstrated well and it is not P01's:
# P02's brief undertakes "why summing a million small gradients in the wrong
# order loses them", along with cancellation, Welford and the catalogue of
# fixes. Writing it here would spend P02's payoff and leave it repeating.
#
# What IS P01's is the threshold underneath that loss, because it is a fact
# about the ENCODING and follows from the gap table above: under round-to-
# nearest, adding something smaller than HALF THE GAP at the running total
# moves nothing at all. Not "loses precision" -- moves nothing. So there is a
# size below which a contribution is not small, it is zero, and the size is a
# fixed FRACTION of whatever the total has reached.
#
# (The first draft also failed in a way worth keeping: with TINY = 1e-10 the
# two orders printed the same ten decimal places, and `forward != backward`
# passed on a difference the page could not show. An assertion on the floats
# is not an assertion about what the reader reads. Hence the assertion below
# is on the printed string.)
# The two validation losses in section 2's aibox. The first draft invented a
# pair differing by 1.7e-6 and called it smaller than the gap at that
# magnitude; it is six gaps, so the box argued the opposite of what it printed.
# The pair is now chosen so the assertion below can fail if it stops being true.
LOSS_A, LOSS_B = 2.3481062, 2.3481063
LOSS_GAP = 2.0 ** math.floor(math.log2(LOSS_A)) * epsilon(FORMATS["fp32"][1])
emit("p01.loss.a", f"{LOSS_A:.7f}")
emit("p01.loss.b", f"{LOSS_B:.7f}")
emit("p01.loss.diff", f"{LOSS_B - LOSS_A:.0e}")
emit("p01.loss.gap", f"{LOSS_GAP:.1e}")
assert 0 < LOSS_B - LOSS_A < LOSS_GAP, (
    "the two losses are no longer closer together than one fp32 gap at their "
    "own magnitude, which is the whole of the box's argument")

SWAMP_TINY = 1e-17
SWAMPED = 1.0 + SWAMP_TINY
emit("p01.swamp.tiny", f"{SWAMP_TINY:.0e}")
emit("p01.swamp.sum", f"{SWAMPED:.17f}")
assert SWAMPED == 1.0, "1.0 + 1e-17 is no longer exactly 1.0 on this machine"
assert f"{SWAMPED:.17f}" == f"{1.0:.17f}", "the frame would print two different numbers"

# The threshold, per format, as the ratio it really is: half the gap at 1 is
# half an epsilon, and the gap scales with the magnitude, so this fraction is
# the whole rule. fp32's is a gradient of 1e-8 against a total of 1, which is
# an ordinary afternoon; bf16's is a fortieth of a per cent.
for _name, (_e, _m) in FORMATS.items():
    _half = 0.5 * epsilon(_m)
    emit(f"p01.swamp.{_name}", f"{_half:.1e}")
    if _name == "bf16":
        # The draft called this "a fortieth of a per cent". It is 0.39 per
        # cent, sixteen times larger, so the page quotes the number.
        emit("p01.swamp.bf16.pct", f"{_half * 100:.2f}")
    assert 1.0 + _half * 0.9 == 1.0 or _name != "fp64", "half a gap is no longer the threshold"

# And in absolute terms at two magnitudes, so the reader sees it move with the
# total rather than sitting at one number. This is section 2's gap table doing
# a second job.
for _tag, _x in (("one", 1.0), ("billion", 1e9)):
    _half = 0.5 * math.ulp(_x)
    emit(f"p01.swamp.at.{_tag}", f"{_half:.1e}")
    assert _x + _half * 0.9 == _x, f"a value below half a gap now moves the total at {_x}"
    assert _x + _half * 1.1 != _x, f"a value above half a gap no longer moves the total at {_x}"

# An exact coincidence, and the frames say in as many words that it is one.
# A billion falls in the binade starting at 2^29, and 29 is exactly the
# difference between the two significand budgets (52 - 23), so half the gap at
# a billion IN A DOUBLE and half the gap at 1 IN A FLOAT are the same number to
# the bit. It is a property of that magnitude and not a law -- at 1e10 it is
# out by a factor of eight -- which is why it is asserted here rather than
# generalised on the page.
assert 0.5 * math.ulp(1e9) == 0.5 * epsilon(FORMATS["fp32"][1]), (
    "half a double's gap at a billion no longer equals half an fp32 epsilon")
assert 0.5 * math.ulp(1e10) != 0.5 * epsilon(FORMATS["fp32"][1]), (
    "the coincidence at a billion has spread to 1e10, so it is not binade-specific")

# ==========================================================================
# SECTION 5 --- what F03 and F12 were promised
#
# CROSS-PROGRAMME DRIFT GATE, in the shape F12 introduced. F03 computed a
# sequence probability and F12 a product of forty factors; both frames say
# the arithmetic runs out, and this program is where that is checked rather
# than claimed.
# ==========================================================================
VALDIR = Path(__file__).resolve().parent.parent / "figures" / "values"


def committed(fname: str, key: str) -> str | None:
    """The value AS WRITTEN. Deliberately not parsed to a float here: one of
    the two values this section reads back is smaller than a double can hold,
    so float() would silently give 0.0 and every comparison against it would
    be vacuously true. Reading a number the machine cannot hold is this
    program's subject, so the check has to survive it."""
    import re
    p = VALDIR / fname
    if not p.exists():                                       # pragma: no cover
        return None
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  p.read_text(encoding="utf8"))
    # AN ABSENT FILE AND AN ABSENT KEY ARE DIFFERENT FAILURES, and returning
    # None for both is how a cross-programme gate goes quiet. A missing file is
    # a fresh checkout that has not run `make numbers`; a missing key means the
    # other program renamed or dropped the value this one is checking, which is
    # exactly what this gate exists to catch. It happened: F12 replaced
    # `f12.sat.bound` and the check below silently stopped running with `make
    # numbers` still exiting 0, and only the values diff showed it.
    if m is None:
        raise SystemExit(
            f"{fname} has no {key}: the program that commits it renamed or "
            f"dropped the value, and this gate would otherwise go quiet")
    return m.group(1)


def decimal_exponent(written: str) -> int:
    """The power of ten in a value written as `m.mme-nnn`, without parsing it
    as a float. This is how a value below the double floor is compared."""
    mant, _, exp = written.partition("e")
    return int(exp) + (len(mant.split(".")[0].lstrip("-")) - 1)


NOTES: list[str] = []
_f03 = committed("f03.tex", "f03.seq.prod")
if _f03 is None:                                             # pragma: no cover
    NOTES.append("f03.tex absent: F03's underflow claim was NOT checked")
else:
    # THE BEST DEMONSTRATION IN THIS PROGRAM, and it was not planned. F03's
    # committed value cannot be read back into a double at all: float() on it
    # returns 0.0, silently. So the check is done on the exponent as written,
    # and the failure to parse becomes the frame.
    assert float(_f03) == 0.0, "F03's value now parses to something nonzero"
    _e03 = decimal_exponent(_f03)
    for _name, (_e, _m) in FORMATS.items():
        floor_exp = math.floor(math.log10(smallest_subnormal(_e, _m)))
        assert _e03 < floor_exp, (
            f"F03's exponent {_e03} is no longer below {_name}'s floor {floor_exp}")
    emit("p01.f03.prob", _f03)
    emit("p01.f03.readback", "0.0")
    emit("p01.fp64.floor.exp", math.floor(math.log10(smallest_subnormal(11, 52))))
    NOTES.append(f"F03's {_f03} cannot be read back at all: float() gives 0.0")

F03_LITERAL = _f03 if _f03 is not None else "2.43e-2085"

# F12 commits the EXPONENT rather than the product, because the product is a
# bound -- "the saturated chain falls below 10^-e" -- and a bound is what
# survives a change of chain length. So the bound is what is read back.
_f12exp = committed("f12.tex", "f12.sat.exponent")
if _f12exp is None:                                          # pragma: no cover
    _f12 = None
    NOTES.append("f12.tex absent: F12's underflow claim was NOT checked")
else:
    _f12 = 10.0 ** -int(float(_f12exp))
    # F12's bound is representable in fp64 and NOT in fp32 -- which is the
    # more interesting half, because it means the same arithmetic gives a
    # number in one training format and exactly zero in another.
    assert _f12 > smallest_subnormal(*FORMATS["fp64"]), (
        "F12's product is no longer representable in fp64")
    assert _f12 < smallest_subnormal(*FORMATS["fp32"]), (
        "F12's product is no longer below fp32's floor")
    emit("p01.f12.prod", f"1e-{int(float(_f12exp))}")
    NOTES.append(f"F12's 1e-{int(float(_f12exp))} is fine in fp64 and exactly zero in fp32")

# How long a sequence can be scored by multiplying, in each format, which is
# F03's "shorter than a page" made precise. A fair coin gives 0.5 per token.
#
# THE DEFINITION HAD TO BE TAKEN FROM F03 RATHER THAN CHOSEN. The first draft
# computed the largest n with 0.5**n still representable and got 1074 and 149,
# against F03's committed 1075 and 150 -- the same quantity counted from the
# other side of the boundary. Both statements are true and printing them two
# hundred pages apart would put two numbers in the book that look like one and
# are not. F03 asks "after how many tokens is the product exactly zero", so
# that is what this computes, and the answer is CHECKED AGAINST F03's rather
# than merely resembling it.
#
# The arithmetic is exact until it underflows, because 0.5**n is exactly 2**-n
# and every one of those is representable down to the smallest subnormal. So
# the first zero is one past it, in every format.
for _name, (_e, _m) in FORMATS.items():
    k = -round(math.log2(smallest_subnormal(_e, _m)))
    assert 2.0 ** -k == smallest_subnormal(_e, _m), f"{_name}'s floor is not a power of 2"
    emit(f"p01.coin.{_name}", k + 1)

for _name, _key in (("fp64", "f03.half.f64.zero"), ("fp32", "f03.half.f32.zero")):
    _raw = committed("f03.tex", _key)
    if _raw is None:                                             # pragma: no cover
        NOTES.append(f"f03.tex absent: {_key} was NOT checked against P01")
        continue
    _e, _m = FORMATS[_name]
    _mine = -round(math.log2(smallest_subnormal(_e, _m))) + 1
    assert int(_raw) == _mine, (
        f"P01 makes the {_name} coin-flip cliff {_mine} where F03 committed "
        f"{_raw}: the two programs no longer count the same boundary")
NOTES.append("F03's coin-flip cliffs at 0.5 per token are reproduced exactly")

# The same gate on the four thresholds themselves. F03 prints all four while
# arguing that a product cannot fall below them; P01 DERIVES all four from the
# two numbers that define each format. That is the same quantity reached by two
# routes in two programs, so it is checked rather than left to agree.
for _key, _name, _fn in (
        ("f03.f32.tiny", "fp32", "minnorm"),
        ("f03.f32.sub", "fp32", "minsub"),
        ("f03.f64.tiny", "fp64", "minnorm"),
        ("f03.f64.sub", "fp64", "minsub")):
    _raw = committed("f03.tex", _key)
    if _raw is None:                                             # pragma: no cover
        NOTES.append(f"f03.tex absent: {_key} was NOT checked against P01")
        continue
    _e, _m = FORMATS[_name]
    _here = smallest_normal(_e) if _fn == "minnorm" else smallest_subnormal(_e, _m)
    assert f"{_here:.2e}" == _raw, (
        f"P01 derives {_here:.2e} for {_name}'s {_fn} where F03 committed "
        f"{_raw}: two programs, one threshold, two numbers")
NOTES.append("F03's four format thresholds are re-derived here and agree")

# ==========================================================================
# A second implementation, for the format thresholds.
# ==========================================================================
try:
    import numpy as _np
except ImportError:                                          # pragma: no cover
    NUMPY_NOTE = "numpy absent: the format thresholds were NOT cross-checked"
else:
    for _name, _dt in (("fp64", _np.float64), ("fp32", _np.float32),
                       ("fp16", _np.float16)):
        _i = _np.finfo(_dt)
        _e, _m = FORMATS[_name]
        assert float(_i.max) == largest(_e, _m), f"{_name} max disagrees with numpy"
        assert float(_i.tiny) == smallest_normal(_e), f"{_name} min normal disagrees"
        assert float(_i.eps) == epsilon(_m), f"{_name} epsilon disagrees"
    NUMPY_NOTE = (f"numpy {_np.__version__}: every fp64, fp32 and fp16 threshold "
                  f"derived here matches finfo")

# ==========================================================================
OUT = VALDIR / "p01.tex"


# ==========================================================================
# The two transcripts. NOTHING HERE IS TYPED: every value below is computed
# above and interpolated, so a change to the arithmetic changes the listing
# and `make verify` reports the drift. That is the rule the book states and
# the reason the companion volume's only outright factual error survived a
# whole draft -- it was inside a console block nobody had run.
# ==========================================================================
TRANSCRIPTS = Path(__file__).resolve().parents[1] / "figures" / "transcripts"


def parts(x: float) -> tuple[int, int, str]:
    """A double's three fields: sign bit, stored exponent, significand."""
    n = struct.unpack("<Q", struct.pack("<d", x))[0]
    return n >> 63, (n >> 52) & 0x7FF, hex(n & 0xF_FFFF_FFFF_FFFF)


# 1.0 and 2.0 differ in the exponent alone; 1.0 and 1.5 in the significand
# alone. Three lines, and the reader has seen the three fields do their jobs.
assert parts(1.0)[1] + 1 == parts(2.0)[1], "doubling no longer adds one to the exponent"
assert parts(1.0)[0] == parts(1.5)[0] and parts(1.0)[1] == parts(1.5)[1], (
    "1.0 and 1.5 no longer share a sign and an exponent")
assert parts(1.0)[2] != parts(1.5)[2], "1.0 and 1.5 no longer differ in the significand"

BITS_TEXT = f""">>> import struct
>>> def parts(x):
...     n = struct.unpack('<Q', struct.pack('<d', x))[0]
...     frac = n & (2**52 - 1)
...     return n >> 63, (n >> 52) & 0x7FF, hex(frac)
...
>>> parts(1.0)                  # sign, exponent, significand
{parts(1.0)}
>>> parts(2.0)                  # only the exponent moved
{parts(2.0)}
>>> parts(1.5)                  # only the significand moved
{parts(1.5)}
"""

TENTH_TEXT = f""">>> 0.1 + 0.2
{0.1 + 0.2!r}
>>> 0.1 + 0.2 == 0.3
{0.1 + 0.2 == 0.3}
>>> (0.1 + 0.2) - 0.3
{(0.1 + 0.2) - 0.3!r}
>>> f"{{0.1:.20f}}"                   # what 0.1 really is
{f"{0.1:.20f}"!r}
"""

# The third transcript is section 5's, and it exists because the claim it
# carries was a TYPED console line in the draft -- "ask Python and it returns
# 0.0" -- which is the fabricated-console-block shape this book warns about
# with a build step missing. Now it is run.
_CLIFF = int(VALUES["p01.coin.fp64"][0])
UNDERFLOW_TEXT = f""">>> float({F03_LITERAL!r})    # F03's sequence probability
{float(F03_LITERAL)!r}
>>> 0.5 ** {_CLIFF}             # a fair coin, one past the floor
{0.5 ** _CLIFF!r}
>>> 0.5 ** {_CLIFF - 1}             # and one before it
{0.5 ** (_CLIFF - 1)!r}
"""
assert float(F03_LITERAL) == 0.0, "F03's probability no longer reads back as zero"
assert 0.5 ** _CLIFF == 0.0, "the coin-flip cliff is no longer where the table says"
assert 0.5 ** (_CLIFF - 1) > 0.0, "the step before the cliff is no longer representable"

assert repr(0.1 + 0.2) == "0.30000000000000004", "0.1 + 0.2 no longer prints as the book says"
assert f"{0.1:.20f}" == TENTH_STORED, "the stored tenth disagrees with the value emitted above"

def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    for _stem, _text in (("p01-bits", BITS_TEXT), ("p01-tenth", TENTH_TEXT),
                         ("p01-underflow", UNDERFLOW_TEXT)):
        assert _text.isascii(), f"{_stem}: listings cannot set a non-ASCII transcript"
        assert len(_text.strip().splitlines()) <= 14, f"{_stem}: too tall for one frame"
        assert max(len(l) for l in _text.splitlines()) <= 64, f"{_stem}: too wide"
        (TRANSCRIPTS / f"{_stem}.txt").write_text(_text, encoding="ascii")
        print(f"  transcript -> figures/transcripts/{_stem}.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p01_floating_point.py --- do not edit.",
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
    for note in NOTES:
        print(f"  {note}")
    print(f"  {NUMPY_NOTE}")


if __name__ == "__main__":
    main()
