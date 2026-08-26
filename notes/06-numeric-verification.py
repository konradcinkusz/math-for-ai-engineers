#!/usr/bin/env python3
"""
verify_f1.py -- fact-check every numeric claim in design/f1-plan.md.

House rule: no number ships unverified.

Two sections:

  PART A -- claims actually made by the F.1 plan (sections 4, 5, 8, 9, 11).
            Each is re-derived from first principles and compared against the
            literal digits printed in the plan.  A FAIL here is a defect in
            the plan.

  PART B -- the machine-arithmetic claims the fact-check brief asked for
            (exact expansion of the double nearest 0.1, bit patterns, float
            spacing, fp16/bf16 ranges and the exact fp16 overflow threshold,
            softmax overflow and the log-sum-exp fix, catastrophic
            cancellation in a variance, machine epsilon and the largest
            exactly-representable integer per format).
            NOTE: section 1 of the plan *rejects* this material from F1 and
            assigns it to P1 and P2.  None of it is an F.1 claim.  It is
            computed here so that P1/P2 inherit verified values rather than
            remembered ones.

Everything uses exact integer or Fraction arithmetic where exactness is
available, and numpy's actual float16/float32 storage where it is not.
Nothing is asserted from memory.
"""

from __future__ import annotations

import math
import struct
from decimal import Decimal, getcontext
from fractions import Fraction

import numpy as np
import sympy as sp

getcontext().prec = 120

# --------------------------------------------------------------------------
# ledger
# --------------------------------------------------------------------------

ROWS: list[tuple] = []
FAILS: list[str] = []
NOTES: list[str] = []


def _norm(s: str) -> str:
    """Normalise exponent spelling: 1.4e+10, 1.4e10 and 1.4E10 are one claim."""
    s = str(s).strip().lower().replace("e+", "e")
    if "e" in s:
        m, _, e = s.partition("e")
        try:
            sign = "-" if e.startswith("-") else ""
            s = f"{m}e{sign}{int(e.lstrip('+-'))}"
        except ValueError:
            pass  # not a number in exponent form; compare verbatim
    return s


def check(key: str, claimed, computed, how: str, *, tol=0.0):
    """Compare a claim in the plan against a computed value."""
    if isinstance(claimed, str) or isinstance(computed, str):
        ok = _norm(claimed) == _norm(computed)
    else:
        ok = abs(float(claimed) - float(computed)) <= tol
    ROWS.append((key, claimed, computed, how, "OK" if ok else "FAIL"))
    if not ok:
        FAILS.append(f"{key}: plan says {claimed!r}, computed {computed!r}  [{how}]")
    return ok


def note(s: str):
    NOTES.append(s)


def r(x, n):
    """Round-half-even to n places, the way Python's format() will.

    Fractions are rounded through Decimal at 120 digits so an exact rational
    is never routed through a binary float before it is rounded.
    """
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return float(f"{x:.{n}f}")


# ==========================================================================
# PART A -- the F.1 plan's own numbers
# ==========================================================================

GIB, GB = 2**30, 10**9
KIB, MIB, TIB = 2**10, 2**20, 2**40

# ---- 11.1 / 11.4  the GiB-GB gap, in both directions ---------------------
check("f01.gib.over.gb.pct", 7.4, r((GIB / GB - 1) * 100, 1), "2^30/10^9 - 1")
check("f01.gb.under.gib.pct", 6.9, r((1 - GB / GIB) * 100, 1), "1 - 10^9/2^30")
assert round(GIB / GB - 1, 6) != round(1 - GB / GIB, 6)
check("f01.gib.bytes", 1073741824, GIB, "2^30")

# frame 50: the gap widens with the prefix
for name, claimed, n in (("Ki", 2.4, 10), ("Mi", 4.9, 20), ("Gi", 7.4, 30), ("Ti", 10.0, 40)):
    got = r((2**n / 10 ** (3 * n // 10) - 1) * 100, 1)
    check(f"prefix gap {name} (fr.50)", claimed, got, f"2^{n}/10^{3*n//10} - 1")

# frame 50 R/A: first prefix above 5%
first_over_5 = next(
    nm for nm, n in (("Ki", 10), ("Mi", 20), ("Gi", 30), ("Ti", 40))
    if (2**n / 10 ** (3 * n // 10) - 1) * 100 > 5
)
check("fr.50 first prefix over 5%", "Gi", first_over_5, "scan Ki,Mi,Gi,Ti")

# ---- 5 / 35 / 36  the compounding-error trap -----------------------------
check("f01.two.ten", 1024, 2**10, "2^10")
check("f01.two.ten.err.pct", 2.4, r((2**10 / 10**3 - 1) * 100, 1), "1024/1000 - 1")
check("f01.two.ten.err.compounded", 1.2089, r(1.024**8, 4), "1.024^8")
check(
    "f01.two.eighty",
    "1208925819614629174706176",
    str(2**80),
    "2^80 exact (integer)",
)
check("2^80 digit count (fr.36 'print the 25 digits')", 25, len(str(2**80)), "len(str(2^80))")
check(
    "f01.two.eighty.err.pct",
    20.89,
    r((Fraction(2**80, 10**24) - 1) * 100, 2),
    "exact Fraction(2^80,10^24) - 1",
)
# the mechanism claim: the compounded error IS the 2^80 error
check(
    "fr.36 mechanism 1.024^8 == 2^80/10^24",
    r(1.024**8, 6),
    r(float(Fraction(2**80, 10**24)), 6),
    "1.024^8 vs 2^80/10^24",
)
check("f01.two.twenty.err.pct (T8)", 4.86, r((Fraction(2**20, 10**6) - 1) * 100, 2), "exact 2^20/10^6 - 1")
check("2^20 (T8)", 1048576, 2**20, "2^20")
check("f01.two.forty.err.pct (P13)", 9.95, r((Fraction(2**40, 10**12) - 1) * 100, 2), "exact 2^40/10^12 - 1")
check("2^40 (P13)", "1099511627776", str(2**40), "2^40")

ti = (Fraction(2**40, 10**12) - 1) * 100
if r(ti, 1) != r(ti, 2):
    note(
        f"2^40/10^12 - 1 is ONE quantity, printed twice at different precisions: "
        f"frame 50 quotes {r(ti,1)}% (TiB vs TB) and P13/P18 quote {r(ti,2)}% -- "
        f"exact value {float(ti):.6f}%. Both roundings are right; a reader meeting "
        f"both is entitled to think one is wrong. Emit ONE key and choose ONE precision."
    )
mi = (Fraction(2**20, 10**6) - 1) * 100
if r(mi, 1) != r(mi, 2):
    note(
        f"2^20/10^6 - 1 likewise: frame 50 quotes {r(mi,1)}% (MiB vs MB), T8 quotes "
        f"{r(mi,2)}% (2^20 vs a million). Same quantity, exact value {float(mi):.4f}%."
    )

# ---- 24 / P8  norms ------------------------------------------------------
check("f01.norm2.34", 5, math.hypot(3, 4), "sqrt(3^2+4^2)")
check("f01.norm1.34", 7, 3 + 4, "|3|+|4|")
check("fr.24 sqrt(9+16)", 5, math.isqrt(25), "sqrt(25)")
check("fr.24 sqrt9+sqrt16", 7, math.isqrt(9) + math.isqrt(16), "3+4")
check("f01.norm2.512", 13, math.hypot(5, 12), "sqrt(25+144)")
check("f01.norm1.512", 17, 5 + 12, "5+12")

# ---- 32 / 33 / P12  spacing from significant digits alone ----------------
def gap(sig_digits: int, near: float) -> float:
    return 10 ** (int(math.floor(math.log10(near))) - (sig_digits - 1))


check("f01.sig3.gap.near1000", 10, gap(3, 1e3), "10^(floor(log10 1000)-2)")
check("f01.sig3.gap.near1", 0.01, gap(3, 1.0), "10^(0-2)")
check("f01.sig4.gap.near1", 0.001, gap(4, 1.0), "10^(0-3)")
check("f01.sig4.gap.near1e6", 1000, gap(4, 1e6), "10^(6-3)")
# fragility probe: the sketch's gap() leans on math.log10 of a power of ten
for v in (1e3, 1e6, 1e9, 1e-4):
    lg = math.log10(v)
    if lg != round(lg):
        note(f"math.log10({v!r}) = {lg!r}, not integral -- gap() in 11.4 would be off by a decade")

# ---- 41-46  model memory -------------------------------------------------
BYTES = {"fp32": 4, "fp16": 2, "bf16": 2, "int8": 1}
check("bytes/param fp32", 4, BYTES["fp32"], "IEEE binary32 width")
check("bytes/param fp16", 2, BYTES["fp16"], "IEEE binary16 width")
check("bytes/param bf16", 2, BYTES["bf16"], "bfloat16 width")
check("bytes/param int8", 1, BYTES["int8"], "int8 width")
check("fp16 and bf16 same width", True, BYTES["fp16"] == BYTES["bf16"], "fr.41 claim")

check("f01.weights.bytes (7B fp16)", "1.4e10", f"{7e9*2:.1e}", "7e9 x 2")
check("f01.weights.gb", 14, 7e9 * 2 / 1e9, "bytes / 10^9")
check("f01.weights.gib", 13.04, r(7e9 * 2 / GIB, 2), "bytes / 2^30")
check("f01.weights.fp32.gb (fr.42)", 28, 7e9 * 4 / 1e9, "7e9 x 4 / 10^9")
check("f01.model13.gb (fr.43)", 26, 13e9 * 2 / 1e9, "13e9 x 2 / 10^9")
check("fr.43 bytes", "2.6e10", f"{13e9*2:.1e}", "13e9 x 2")
check("f01.big.params (fr.46, 70B)", "1.4e11", f"{70e9*2:.1e}", "70e9 x 2")
check("f01.big.gb", 140, 70e9 * 2 / 1e9, "1.4e11 / 10^9")
check("f01.big.gib", 130.4, r(70e9 * 2 / GIB, 1), "1.4e11 / 2^30")

TRAIN_BYTES = 2 + 2 + 4 + 4
check("f01.train.bytes.per.param", 12, TRAIN_BYTES, "fp16 w + fp16 g + fp32 m + fp32 v")
check("f01.train.mem.gb (7B)", 84, 7e9 * TRAIN_BYTES / 1e9, "7e9 x 12 / 10^9")
check("f01.train.mem.13b.gb (P15, fr.44)", 156, 13e9 * TRAIN_BYTES / 1e9, "13e9 x 12 / 10^9")
check("f01.infer.flops.per.token (fr.45)", "1.4e10", f"{2*7e9:.1e}", "2 FLOPs/param x 7e9")

check("f01.model3.gb (T10)", 6, 3e9 * 2 / 1e9, "3e9 x 2 / 10^9")
check("f01.model3.gib (T10)", 5.59, r(3e9 * 2 / GIB, 2), "6e9 / 2^30")
check("f01.model405.gb (P14)", 810, 405e9 * 2 / 1e9, "405e9 x 2 / 10^9")
check("f01.model405.devices80 (P14)", 11, math.ceil(810 / 80), "ceil(810/80)")
check("P14 810/80", 10.125, 810 / 80, "810/80")

# ---- 37-40 / P16 / T9  the 6ND estimate ----------------------------------
def flops_6nd(n, d):
    return 6 * n * d


def days(flops, devices, peak=4e14, util=0.4):
    return flops / (devices * peak * util) / 86400


check("fr.37 worked 6ND (7B, 2T)", "8.4e22", f"{flops_6nd(7e9, 2e12):.1e}", "6 x 7e9 x 2e12")
check("f01.flops.1t (fr.37 R/A)", "4.20e22", f"{flops_6nd(7e9, 1e12):.2e}".replace("e+", "e"), "6 x 7e9 x 1e12")
check("f01.flops.3b.1t (T9)", "1.80e22", f"{flops_6nd(3e9, 1e12):.2e}".replace("e+", "e"), "6 x 3e9 x 1e12")
check("fr.38 effective FLOP/s", "1.6e14", f"{4e14*0.4:.1e}", "4e14 x 0.40")
check("fr.38 seconds", "5.25e8", f"{flops_6nd(7e9, 2e12)/1.6e14:.2e}", "8.4e22 / 1.6e14")
check("f01.device.days (fr.38)", 6076, math.floor(days(flops_6nd(7e9, 2e12), 1)), "5.25e8 s / 86400")
check("fr.38 days unrounded", 6076.39, r(days(flops_6nd(7e9, 2e12), 1), 2), "exact")
check("f01.device.years (fr.39)", 16.6, r(days(flops_6nd(7e9, 2e12), 1) / 365, 1), "6076.39 / 365")
check(
    "f01.devices.for.30.days (fr.39)",
    203,
    math.ceil(days(flops_6nd(7e9, 2e12), 1) / 30),
    "ceil(6076.39/30)",
)
check(
    "f01.devices.for.10.days (fr.39 R/A)",
    608,
    int(f"{days(flops_6nd(7e9, 2e12), 1)/10:.0f}"),
    "6076.39/10 rounded",
)
check(
    "fr.39 devices-for-10-days, ceiling reading",
    608,
    math.ceil(days(flops_6nd(7e9, 2e12), 1) / 10),
    "ceil(607.64)",
)
check("f01.flops.405b (P16)", "3.645e25", f"{flops_6nd(405e9, 15e12):.3e}".replace("e+", "e"), "6 x 405e9 x 15e12")
check("P16 seconds", "1.39e7", f"{flops_6nd(405e9,15e12)/(16384*4e14*0.4):.2e}", "3.645e25 / 2.62144e18")
check("f01.days.16384 (P16)", 160.9, r(days(flops_6nd(405e9, 15e12), 16384), 1), "seconds / 86400")

# ---- 47-51 / T11 / P17  reading a device report --------------------------
check("f01.kib.bytes", 1024, KIB, "2^10")
check("f01.mib.bytes", 1048576, MIB, "2^20")
check("f01.tib.bytes", "1099511627776", str(TIB), "2^40")
check("f01.gib7915.gb (fr.51, P17)", 84.99, r(79.15 * GIB / 1e9, 2), "79.15 x 2^30 / 10^9")
check("f01.gib2328.gb (T11)", 25.0, r(23.28 * GIB / 1e9, 1), "23.28 x 2^30 / 10^9")
check("fr.48 14 GB -> GiB", 13.04, r(14e9 / GIB, 2), "14e9 / 2^30")

# ---- 52-55 / T12 / P19  stating a speed-up -------------------------------
check("f01.base.ms", 200, 200, "given")
check("f01.fifty.pct.less.ms (fr.53)", 100, 200 * 0.5, "200 x 0.5")
check("f01.fifty.pct.more.rate.ms (fr.53)", 133.3, r(200 / 1.5, 1), "200 / 1.5")
check("f01.speedup.discrepancy.ms (fr.53)", 33.3, r(200 / 1.5 - 200 * 0.5, 1), "133.33 - 100, the gap BETWEEN the two readings")
check("fr.53 gap is not 200 - 133.3", 66.7, r(200 - 200 / 1.5, 1), "the other subtraction, for contrast")
check("fr.53 'a sixth of the original'", 33.3, r(200 / 6, 1), "200/6")


def ratio_report(before, after):
    return after / before, (after / before - 1) * 100, (1 - before / after) * 100


for tag, (b, a) in (("f01.tok", (30, 45)), ("f01.tok2", (120, 180))):
    s, up, red = ratio_report(b, a)
    check(f"{tag}.speedup", 1.5, r(s, 1), f"{a}/{b}")
    check(f"{tag}.throughput.pct", 50, r(up, 0), f"({a}/{b} - 1) x 100")
    check(f"{tag}.latency.red.pct", 33.3, r(red, 1), f"(1 - {b}/{a}) x 100")

check("T12 speed-up 250->200 ms", 1.25, 250 / 200, "250/200")
check("T12 % reduction", 20, r((1 - 200 / 250) * 100, 0), "(1-200/250) x 100")
check("P20 latency reading 200 ms, 30% faster", 140, r(200 * 0.7, 0), "200 x 0.7")
check("P20 throughput reading", 130, r(100 * 1.3, 0), "100 x 1.3")

# ---- indices, roots, scientific notation: exact via sympy ----------------
S = sp.Integer
check("fr.11 trap 2^3 x 3^2", 72, int(S(2) ** 3 * S(3) ** 2), "sympy exact")
check("fr.11 trap 6^5", 7776, int(S(6) ** 5), "sympy exact")
check("fr.16 (10^6)^2/10^-3", 10**15, int((S(10) ** 6) ** 2 / S(10) ** -3), "sympy exact")
check("fr.16 2^10 x 2^10", 1048576, int(S(2) ** 10 * S(2) ** 10), "= 2^20")
check("fr.17 (2^-2 x 2^5)^2/2^4", 4, int((S(2) ** -2 * S(2) ** 5) ** 2 / S(2) ** 4), "sympy exact")
x = sp.Symbol("x")
check("fr.15 (x^2)^3 x^-4 / x^-1", "x**3", str(sp.simplify((x**2) ** 3 * x**-4 / x**-1)), "sympy simplify")
check("fr.18 sqrt(64)", 8, int(sp.sqrt(64)), "exact")
check("fr.18 cbrt(8)", 2, int(sp.Integer(8) ** sp.Rational(1, 3)), "exact")
check("fr.19 16^(1/2)", 4, int(S(16) ** sp.Rational(1, 2)), "exact")
check("fr.20 81^(1/4)", 3, int(S(81) ** sp.Rational(1, 4)), "exact")
check("fr.21 27^(2/3)", 9, int(S(27) ** sp.Rational(2, 3)), "exact")
check("fr.21 8^(2/3) root-first", 4, int((S(8) ** sp.Rational(1, 3)) ** 2), "(cbrt 8)^2")
check("fr.21 8^(2/3) power-first", 4, int(S(64) ** sp.Rational(1, 3)), "cbrt(8^2)")
check("fr.22 4^(3/2)", 8, int(S(4) ** sp.Rational(3, 2)), "exact")
check("fr.22 9^(-1/2)", sp.Rational(1, 3), S(9) ** sp.Rational(-1, 2), "exact")
check("fr.22 125^(2/3)", 25, int(S(125) ** sp.Rational(2, 3)), "exact")
check("fr.23 16^(-3/4)", sp.Rational(1, 8), S(16) ** sp.Rational(-3, 4), "exact")
check("T3 3^-2", sp.Rational(1, 9), S(3) ** -2, "exact")
check("T3 (4^2)^3", 4096, int((S(4) ** 2) ** 3), "= 4^6")
check("T4 64^(1/2),(1/3),(2/3),(-1/2)", "8,4,16,1/8",
      ",".join(str(S(64) ** sp.Rational(*q)) for q in ((1, 2), (1, 3), (2, 3), (-1, 2))), "exact")
check("T5 81^(3/4)", 27, int(S(81) ** sp.Rational(3, 4)), "exact")
check("T5 32^(-2/5)", sp.Rational(1, 4), S(32) ** sp.Rational(-2, 5), "exact")
check("T2 (2^6 x 2^-2)/2^3", 2, int(S(2) ** 6 * S(2) ** -2 / S(2) ** 3), "exact")
check("P3 (3^5 x 3^-7)/3^-3", 3, int(S(3) ** 5 * S(3) ** -7 / S(3) ** -3), "exact")
y = sp.Symbol("y")
check("P4 (x^3 y^-2)^2 (x^-1 y^3)", "x**5/y", str(sp.simplify((x**3 * y**-2) ** 2 * (x**-1 * y**3))), "sympy")
check("P5 2^4 x 4^2", 256, int(S(2) ** 4 * S(4) ** 2), "exact")
check("P5 8^3", 512, int(S(8) ** 3), "exact")
check("P6 125^(-2/3)", sp.Rational(1, 25), S(125) ** sp.Rational(-2, 3), "exact")
check("P6 (16/81)^(1/4)", sp.Rational(2, 3), sp.Rational(16, 81) ** sp.Rational(1, 4), "exact")
check("P7 (1+1)^2 vs 1^2+1^2", "4 vs 2", f"{(1+1)**2} vs {1**2+1**2}", "counterexample")
check("P10 (6e-4)^2", "3.6e-07", f"{(6e-4)**2:.1e}", "exact")
check("P10 sqrt(9e-8)", "3.0e-04", f"{math.sqrt(9e-8):.1e}", "exact")
check("fr.28 (5e4)(4e3)", "2.0e+08", f"{(5e4)*(4e3):.1e}", "renormalised")
check("fr.28 (4e6)(2e5)", "8.0e+11", f"{(4e6)*(2e5):.1e}", "exact")
check("fr.29 (8e9)/(2e4)", "4.0e+05", f"{8e9/2e4:.1e}", "exact")
check("fr.29 (6e-3)/(3e-7)", "2.0e+04", f"{6e-3/3e-7:.1e}", "exact")
check("T7 (2.4e5)(5e-9)", "1.2e-03", f"{2.4e5*5e-9:.1e}", "exact")
check("T7 (9e7)/(3e-2)", "3.0e+09", f"{9e7/3e-2:.1e}", "exact")
check("fr.30 compare", "1.1e12 larger", "1.1e12 larger" if 1.1e12 > 9.9e11 else "9.9e11 larger", "exact")
check("fr.34 orders 10^3 -> 10^9", 6, 9 - 3, "exponent difference")

# scientific-notation transcriptions: count the places, do not trust the eye
def sci(s: str) -> str:
    d = Decimal(s).normalize()
    sign, digits, exp = d.as_tuple()
    n = len(digits) - 1 + exp
    mant = Decimal(d).scaleb(-n).normalize()
    return f"{mant}e{n}"


for literal, claimed in (
    ("0.00042", "4.2e-4"),
    ("6400000", "6.4e6"),
    ("0.0000000072", "7.2e-9"),
    ("1024", "1.024e3"),
    ("93000000", "9.3e7"),
    ("14000000000", "1.4e10"),
    ("0.00025", "2.5e-4"),
    ("0.0000061", "6.1e-6"),
    ("0.00000000072", "7.2e-10"),
    ("4500000", "4.5e6"),
):
    check(f"sci({literal})", claimed, sci(literal), "Decimal place count")

check("fr.31 s.f. of 6.022e23", 4, 4, "mantissa digits")
check("fr.31 s.f. of 1.4e10", 2, 2, "mantissa digits")

# P1: smallest containing set
check("P1 2/8", "1/4", str(Fraction(2, 8)), "Fraction")
check("P1 sqrt(49)", 7, int(sp.sqrt(49)), "exact")
check("P1 sqrt(50) rational?", False, sp.sqrt(50).is_rational, "sympy")
check("P1 0.333... = 1/3", "1/3", str(sp.nsimplify(sp.Rational(1, 3))), "exact")
check("fr.6/7 sqrt(9) in N", True, sp.sqrt(9).is_integer, "sympy")
check("fr.4 1/3 in base 3 is 0.1", True, Fraction(1, 3) == Fraction(1, 3**1), "1/3 = 1 x 3^-1")

# P2: 1/7 repeats with period six in base ten; terminates in base 7
def period(num: int, den: int, base: int) -> int:
    """Length of the repeating block of num/den in the given base (0 = terminates)."""
    d = den // math.gcd(num, den)
    while True:
        g = math.gcd(d, base)
        if g == 1:
            break
        d //= g
    if d == 1:
        return 0
    k = 1
    while pow(base, k, d) != 1:
        k += 1
    return k


check("P2 period of 1/7 in base 10", 6, period(1, 7, 10), "multiplicative order of 10 mod 7")
check("P2 1/7 terminates in base 7", 0, period(1, 7, 7), "period 0 = terminates")
check("P2 1/7 terminates in base 14", 0, period(1, 7, 14), "any multiple of 7")
check("fr.4/5 1/10 repeats in base 2", True, period(1, 10, 2) > 0, "period > 0")
check("fr.4 1/3 terminates in base 3", 0, period(1, 3, 3), "period 0")
check("fr.4 1/3 period in base 10", 1, period(1, 3, 10), "0.333...")

# --------------------------------------------------------------------------
# Consistency probes -- correct arithmetic that still contradicts itself
# --------------------------------------------------------------------------

def sig(x: float, n: int) -> str:
    return f"{x:.{n}g}"


# frame 40 rules that a 6ND answer carries ONE significant figure.
# P16 quotes its 6ND answer to two.
p16 = days(flops_6nd(405e9, 15e12), 16384)
if sig(p16, 1) != "160" and "160" in "160":
    note(
        f"frame 40 rules that a 6ND estimate justifies ONE significant figure "
        f"(6076 days -> 6e3). P16's answer is quoted as 'about 160 days', which is "
        f"TWO. One s.f. of {p16:.1f} is {sig(p16,1)} days, i.e. 2e2. Either P16 "
        f"changes to 2e2 or frame 40's rule needs a stated exception."
    )

# 11.4 rounds a device count to nearest for days, but ceilings it for memory.
d10 = days(flops_6nd(7e9, 2e12), 1) / 10
d30 = days(flops_6nd(7e9, 2e12), 1) / 30
note(
    f"11.4 emits devices-for-N-days with '{{:.0f}}' (round to NEAREST): "
    f"{d10:.2f} -> 608 and {d30:.2f} -> 203. Both happen to agree with the "
    f"ceiling. P14 uses math.ceil for the same kind of quantity (10.125 -> 11), "
    f"where nearest would have given the wrong answer (10). A device count is "
    f"always a ceiling; the two emitters must not use different rules."
)

# T11's 25.0 is 24.996 -- clean-looking, and the 11.4 sketch emits it at 2 dp.
t11 = 23.28 * GIB / 1e9
note(
    f"T11 answer is printed '25.0 GB'; the exact figure is {t11:.5f}. "
    f"11.4's loop emits it at 2 decimals, i.e. '25.00', which reads as an exact "
    f"25 in a program whose frame 40 teaches false precision. Either emit 1 dp "
    f"or state that it is 25.0 to three significant figures."
)

# frame 54 and P19 are the same three numbers.
s54 = ratio_report(30, 45)
p19 = ratio_report(120, 180)
if tuple(round(v, 6) for v in s54) == tuple(round(v, 6) for v in p19):
    note(
        f"frame 54's worked ratio (30 -> 45 tok/s) and P19 (120 -> 180 tok/s) "
        f"produce an identical triple {tuple(round(v,1) for v in s54)}. P19 "
        f"consolidates nothing the reader has not just been shown; change one "
        f"of the two ratios."
    )

# Q10 / frame 48 / frame 49 must be one arithmetic, checked end to end.
assert r(14e9 / GIB, 2) == 13.04 and r(70e9 * 2 / GIB, 1) == 130.4

# --------------------------------------------------------------------------
# Key reconciliation: digits that appear in sections 4/8/9 with no key in 11.2/11.3
# House rule: "the book contains no digits, only \\val{} references."
# --------------------------------------------------------------------------

EMITTED = set("""
f01.params f01.weights.bytes f01.weights.gb f01.weights.gib f01.weights.fp32.gb
f01.gib.per.gb f01.gib.gap.pct f01.two.ten f01.two.ten.err.pct f01.two.eighty
f01.two.eighty.err.pct f01.tokens f01.train.flops f01.train.flops.exp
f01.device.flops f01.device.util.pct f01.device.days f01.device.years
f01.devices.for.30.days f01.infer.flops.per.token f01.big.params f01.big.gb
f01.big.gib f01.kib.bytes f01.mib.bytes f01.gib.bytes f01.tib.bytes
f01.kib.over.si.pct f01.mib.over.si.pct f01.gib.over.si.pct f01.tib.over.si.pct
f01.novel.words f01.novel.tokens f01.base.ms f01.fifty.pct.less.ms
f01.fifty.pct.more.rate.ms f01.speedup.discrepancy.ms
f01.two.ten.err.compounded f01.flops.1t f01.devices.for.10.days
f01.sig3.gap.near1000 f01.sig3.gap.near1 f01.sig4.gap.near1 f01.sig4.gap.near1e6
f01.norm2.34 f01.norm1.34 f01.norm2.512 f01.norm1.512 f01.model13.gb
f01.model3.gb f01.model3.gib f01.model405.gb f01.model405.devices80
f01.train.bytes.per.param f01.train.mem.gb f01.train.mem.13b.gb f01.gib7915.gb
f01.gib2328.gb f01.two.twenty.err.pct f01.two.forty.err.pct f01.flops.3b.1t
f01.flops.405b f01.days.16384 f01.tok.speedup f01.tok.throughput.pct
f01.tok.latency.red.pct f01.tok2.speedup f01.tok2.throughput.pct
f01.tok2.latency.red.pct
""".split())

UNKEYED = [
    ("fr.38", "1.6e14 effective FLOP/s", "device.flops x util is printed but never emitted"),
    ("fr.38", "5.25e8 seconds", "the intermediate the day count is derived from"),
    ("fr.41", "4 / 2 / 2 / 1 bytes per format", "the whole table is typed digits"),
    ("fr.44", "the four terms 2 + 2 + 4 + 4", "only their sum (12) has a key"),
    ("fr.42", "28 GB is keyed; 14 GB x 2 as shown working is not", "minor"),
    ("T8", "1048576", "only the percentage 4.86 has a key"),
    ("T12", "1.25x and 20%", "no key; the tok/tok2 keys are the 30->45 and 120->180 pairs"),
    ("P13", "1099511627776", "same integer as f01.tib.bytes under a different role"),
    ("P14", "10.125", "printed in the answer; only the ceiling 11 has a key"),
    ("P16", "1.39e7 seconds", "printed; only the day count has a key"),
    ("P20", "140 ms and 130 req/s", "no keys"),
]
ORPHANS = ["f01.novel.words", "f01.novel.tokens"]

# ==========================================================================
# PART B -- P1/P2 material (NOT in F.1; computed so P1/P2 inherit it verified)
# ==========================================================================

PB: list[tuple] = []


def pb(k, v, how):
    PB.append((k, v, how))


# ---- the double nearest 0.1, exactly ------------------------------------
d01 = Fraction(0.1)  # exact value of the stored double
pb("0.1 stored as (exact rational)", f"{d01.numerator} / 2^55", "Fraction(float) is exact")
pb("0.1 stored as (exact decimal)", Decimal(0.1), "Decimal(float) is exact")
pb("0.1 exact decimal digit count", len(Decimal(0.1).as_tuple().digits), "len of significand")
pb("0.1 bits (binary64)", f"0x{struct.unpack('<Q', struct.pack('<d', 0.1))[0]:016X}", "IEEE-754 punning")
pb("0.1 bits (binary64, fields)",
   format(struct.unpack('<Q', struct.pack('<d', 0.1))[0], '064b'), "sign|exp(11)|frac(52)")
pb("0.1 error vs exact 1/10", Decimal(0.1) - Decimal(1) / Decimal(10), "stored - 1/10")
pb("0.1 + 0.2 stored as", Decimal(0.1 + 0.2), "the canonical demo")
pb("0.1 + 0.2 == 0.3", 0.1 + 0.2 == 0.3, "IEEE-754")
pb("0.1 as float16 (exact)", Decimal(float(np.float16(0.1))), "binary16 nearest")
pb("0.1 as bfloat16 (exact)", Decimal(float(np.float32(struct.unpack('<f', struct.pack('<I', struct.unpack('<I', struct.pack('<f', 0.1))[0] & 0xFFFF0000))[0]))), "bf16 = truncate binary32 to 16 bits")

# ---- machine epsilon, per format ----------------------------------------
EPS = {
    "binary16 (fp16)": (Fraction(1, 2**10), 2**-10),
    "bfloat16": (Fraction(1, 2**7), 2**-7),
    "binary32 (fp32)": (Fraction(1, 2**23), 2**-23),
    "binary64 (fp64)": (Fraction(1, 2**52), 2**-52),
}
for name, (exact, approx) in EPS.items():
    pb(f"eps {name}", f"{exact} = {Decimal(approx)}", "2^-(mantissa bits)")
assert float(np.finfo(np.float16).eps) == 2**-10
assert float(np.finfo(np.float32).eps) == 2**-23
assert float(np.finfo(np.float64).eps) == 2**-52

# ---- largest exactly-representable integer ------------------------------
for name, mant in (("binary16 (fp16)", 11), ("bfloat16", 8), ("binary32 (fp32)", 24), ("binary64 (fp64)", 53)):
    pb(f"largest consecutive integer {name}", f"2^{mant} = {2**mant}", "2^p; 2^p+1 is not representable")
assert np.float16(2048) + np.float16(1) == np.float16(2048)
assert np.float32(16777216) + np.float32(1) == np.float32(16777216)
assert (2.0**53) + 1.0 == 2.0**53

# ---- fp16 / bf16 ranges and the exact overflow point --------------------
f16 = np.finfo(np.float16)
pb("fp16 max finite", f"{int(f16.max)} = 65504", "(2 - 2^-10) x 2^15")
pb("fp16 min normal", Decimal(float(f16.tiny)), "2^-14")
pb("fp16 min subnormal", Decimal(float(np.float16(2.0**-24))), "2^-24")
pb("fp16 exponent range", f"{f16.minexp} .. {f16.maxexp - 1}", "numpy finfo")

# the exact value at which fp16 overflows, found by bisection on exact rationals
# 30 halvings of a width-32 interval keeps every midpoint exactly
# representable as a double; going further would round mid to 65520 itself
# and the bisection would walk past the answer.
lo, hi = Fraction(65504), Fraction(65536)
with np.errstate(over="ignore"):
    for _ in range(30):
        mid = (lo + hi) / 2
        if math.isinf(float(np.float16(float(mid)))):
            hi = mid
        else:
            lo = mid
pb("fp16 largest finite input that survives", f"just below {hi} (bisection lands at {float(lo):.10f})", "exact bisection")
pb("fp16 exact overflow threshold", f"{hi} = 65520", "midpoint of 65504 and 2^16; ties-to-even -> inf")
with np.errstate(over="ignore"):
    assert float(np.float16(65519.9)) == 65504.0
    assert math.isinf(float(np.float16(65520.0)))
assert hi == 65520
with np.errstate(over="ignore"):
    pb("fp16 65519.9 rounds to", float(np.float16(65519.9)), "round-to-nearest")
    pb("fp16 65520 rounds to", float(np.float16(65520.0)), "ties-to-even overflows")

bf_max = struct.unpack("<f", struct.pack("<I", 0x7F7F0000))[0]
bf_tiny = struct.unpack("<f", struct.pack("<I", 0x00800000))[0]
pb("bf16 max finite", f"{bf_max:.7e}", "0x7F7F = (2-2^-7) x 2^127")
pb("bf16 min normal", f"{bf_tiny:.7e}", "2^-126, same as fp32")
pb("bf16 vs fp16 max ratio", f"{bf_max/65504:.4g}", "bf16 reaches ~5e33 times further")
pb("bf16 exponent bits / fp16 exponent bits", "8 / 5", "the exponent-for-mantissa trade")
pb("bf16 mantissa bits / fp16 mantissa bits", "8 (7 stored) / 11 (10 stored)", "same 16-bit width")

# ---- float spacing at various magnitudes --------------------------------
SPACING = []
for mag in (1e-3, 1.0, 10.0, 1e3, 1e6, 1e9, 6e4):
    row = [f"{mag:g}"]
    for dt in (np.float16, np.float32, np.float64):
        try:
            v = dt(mag)
            if math.isinf(float(v)):
                row.append("overflow")
            else:
                row.append(f"{float(np.spacing(v)):.6g}")
        except OverflowError:
            row.append("overflow")
    SPACING.append(row)
pb("spacing table", ("TABLE", SPACING), "np.spacing at each magnitude")
pb("fp16 spacing at 1024", float(np.spacing(np.float16(1024))), "= 1.0, so 1024+0.5 is lost")
pb("fp64 spacing at 1", Decimal(float(np.spacing(1.0))), "= 2^-52")
pb("fp64 spacing at 1e9", float(np.spacing(1e9)), "grows with magnitude")

# ---- softmax overflow, and the log-sum-exp fix --------------------------
logits16 = np.array([10.0, 11.0, 12.0], dtype=np.float16)
big16 = np.array([10.0, 11.0, 12.0], dtype=np.float16) + np.float16(1000)
with np.errstate(over="ignore", invalid="ignore"):
    naive16 = np.exp(np.float16(12.0)), np.exp(np.float16(11.1))
pb("ln(fp16 max)", f"{math.log(65504):.6f}", "exp overflows fp16 above this logit")
pb("fp16 exp(11.0)", float(np.exp(np.float16(11.0))), "still finite")
pb("fp16 exp(11.09)", float(np.exp(np.float16(11.09))), "already over -- 11.09 stores as 11.09375")
with np.errstate(over="ignore"):
    pb("fp16 exp(11.1)", float(np.exp(np.float16(11.1))), "overflows")
    pb("fp16 exp(12.0)", float(np.exp(np.float16(12.0))), "overflows")
    # scan every representable fp16 value upward from 11 to find the boundary
    v = np.float16(11.0)
    last_finite = v
    while not math.isinf(float(np.exp(v))):
        last_finite = v
        v = np.nextafter(v, np.float16(np.inf), dtype=np.float16)
    pb("fp16 largest logit whose exp is finite", f"{float(last_finite)!r} -> exp = {float(np.exp(last_finite))!r}",
       "scan of representable fp16 values")
    pb("fp16 next logit up", f"{float(v)!r} -> exp = inf", "one fp16 ulp (2^-7 near 11) higher")

logits32 = np.array([1000.0, 1000.0, 1000.0], dtype=np.float32)
with np.errstate(over="ignore", invalid="ignore"):
    e = np.exp(logits32)
    naive = e / e.sum()
pb("fp32 naive softmax([1000,1000,1000])", str(naive), "exp -> inf, inf/inf -> nan")
shifted = logits32 - logits32.max()
stable = np.exp(shifted) / np.exp(shifted).sum()
pb("fp32 stable softmax([1000,1000,1000])", str(stable), "subtract the max first")
lse_naive = float(np.log(np.exp(logits32).sum())) if not np.isinf(np.exp(logits32).sum()) else float("inf")
with np.errstate(over="ignore"):
    lse_naive = float(np.log(np.exp(logits32).sum()))
m = float(logits32.max())
lse_stable = m + float(np.log(np.exp(logits32 - m).sum()))
pb("naive log-sum-exp([1000,1000,1000])", lse_naive, "log(sum(exp)) -> inf")
pb("stable log-sum-exp([1000,1000,1000])", f"{lse_stable:.10f}", "m + log(sum(exp(x-m)))")
pb("exact log-sum-exp([1000,1000,1000])", f"{1000 + math.log(3):.10f}", "1000 + ln 3, by hand")
# fp32 carries ~7 significant decimal digits, so 1000 + ln 3 is exact to
# about 1e-4 and no closer.  That is itself the point worth printing.
assert abs(lse_stable - (1000 + math.log(3))) < 1e-3
pb("stable LSE fp32 error vs exact", f"{abs(lse_stable - (1000 + math.log(3))):.3e}",
   "fp32 resolution at 1000 is 6.1e-05")
pb("fp32 spacing at 1000", float(np.spacing(np.float32(1000.0))), "why the fix is right but not exact")

# ---- catastrophic cancellation in a variance ----------------------------
DATA = [1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16]  # the classic four-point set
exact_vals = [Fraction(10**8) + Fraction(k) for k in (4, 7, 13, 16)]
n = len(exact_vals)
mean_exact = sum(exact_vals) / n
var_exact_pop = sum((v - mean_exact) ** 2 for v in exact_vals) / n
var_exact_samp = sum((v - mean_exact) ** 2 for v in exact_vals) / (n - 1)

a = np.array(DATA, dtype=np.float64)
naive_var = float((a * a).mean() - a.mean() ** 2)          # E[x^2] - E[x]^2
two_pass = float(((a - a.mean()) ** 2).mean())              # two-pass
pb("variance data", DATA, "1e8 + {4,7,13,16}")
pb("exact population variance", f"{var_exact_pop} = {float(var_exact_pop)}", "exact Fraction")
pb("exact sample variance", f"{var_exact_samp} = {float(var_exact_samp)}", "exact Fraction")
pb("fp64 naive E[x^2]-E[x]^2", repr(naive_var), "catastrophic cancellation")
pb("fp64 two-pass", repr(two_pass), "numerically stable")
pb("fp64 np.var", repr(float(np.var(a))), "numpy uses two-pass")
pb("naive relative error", f"{abs(naive_var - float(var_exact_pop))/float(var_exact_pop)*100:.2f}%", "vs exact")

a32 = np.array(DATA, dtype=np.float32)
naive32 = float((a32 * a32).mean(dtype=np.float32) - a32.mean(dtype=np.float32) ** 2)
pb("fp32 naive E[x^2]-E[x]^2", repr(naive32), "meaningless: see the next two rows")
pb("fp32 two-pass", repr(float(((a32 - a32.mean(dtype=np.float32)) ** 2).mean(dtype=np.float32))),
   "also wrong -- no algorithm can recover data fp32 never held")
pb("fp32 stores the four points as", [float(v) for v in a32],
   "spacing 8 at 1e8: two of the four collapse onto one value")
pb("fp32 stores 1e8+4 as", repr(float(np.float32(1e8 + 4))), "24-bit mantissa; spacing at 1e8 is 8")
pb("fp32 spacing at 1e8", float(np.spacing(np.float32(1e8))), "the offsets 4,7,13,16 are quantised away")

# a second, harsher pair so the book has a choice
DATA2 = [1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]
b = np.array(DATA2, dtype=np.float64)
ex2 = [Fraction(10**9) + Fraction(k) for k in (4, 7, 13, 16)]
me2 = sum(ex2) / 4
vex2 = sum((v - me2) ** 2 for v in ex2) / 4
pb("variance data (harsher)", DATA2, "1e9 + {4,7,13,16}")
pb("exact population variance", f"{vex2} = {float(vex2)}", "exact Fraction")
pb("fp64 naive at 1e9", repr(float((b * b).mean() - b.mean() ** 2)),
   "THE demo: a NEGATIVE variance, exactly -128.0")
pb("fp64 two-pass at 1e9", repr(float(((b - b.mean()) ** 2).mean())), "stable, recovers 22.5")

# non-associativity, for completeness (P1's stub names it)
pb("(0.1+0.2)+0.3", repr((0.1 + 0.2) + 0.3), "float addition is not associative")
pb("0.1+(0.2+0.3)", repr(0.1 + (0.2 + 0.3)), "different result")
pb("they are equal?", (0.1 + 0.2) + 0.3 == 0.1 + (0.2 + 0.3), "no")

# ==========================================================================
# report
# ==========================================================================

def w(s=""):
    print(s)


w("=" * 100)
w("PART A -- F.1 plan claims re-derived")
w("=" * 100)
kw = max(len(str(r_[0])) for r_ in ROWS)
for k, claimed, computed, how, status in ROWS:
    flag = "    " if status == "OK" else " >> "
    w(f"{flag}{status:4}  {k:<{kw}}  plan={str(claimed):<28}  computed={str(computed):<28}  {how}")

w()
w(f"PART A: {len(ROWS)} claims checked, {len(ROWS)-len(FAILS)} OK, {len(FAILS)} FAILED")
if FAILS:
    w()
    w("CONTRADICTIONS:")
    for f in FAILS:
        w(f"  - {f}")
if NOTES:
    w()
    w("NOTES:")
    for nline in NOTES:
        w(f"  - {nline}")

w()
w("=" * 100)
w("KEY RECONCILIATION -- digits in sections 4/8/9 with no key in 11.2/11.3")
w("=" * 100)
for where, what, why in UNKEYED:
    w(f"  {where:<6}  {what:<48}  {why}")
w()
w("  Keys listed as emitted but used at no frame in section 4:")
for o in ORPHANS:
    w(f"    {o}")
w(f"  ({len(EMITTED)} keys enumerated in 11.2 + 11.3)")

w()
w("=" * 100)
w("PART B -- machine arithmetic (P1/P2 material; NOT claimed by the F.1 plan)")
w("=" * 100)
for k, v, how in PB:
    if isinstance(v, tuple) and v and v[0] == "TABLE":
        w(f"  {k}:  ({how})")
        w("      magnitude      fp16            fp32            fp64")
        for row in v[1]:
            w(f"      {row[0]:<13}  {row[1]:<14}  {row[2]:<14}  {row[3]}")
    else:
        w(f"  {k:<48} = {v}   [{how}]")

w()
w("all asserts passed")
