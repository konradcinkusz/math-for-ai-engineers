"""Lab P1 -- the checks.

Every expected value below is read from figures/values/p01.tex, the file
Program P1 prints from. Each check's docstring names the frames it rests on,
and a failure message names them again, because the frames are where a
reader who failed should go -- not to lab/solutions/.

Runs under pytest and under lab/check.py alike: plain functions, plain
asserts, nothing pytest-specific.
"""
import math

from labkit import load, values

V = values("p01")
M = load("p01_floating_point")

FORMATS = ("fp64", "fp32", "fp16", "bf16")


# --- exercise 1: gap ---------------------------------------------------------
def test_1_gap_matches_the_table():
    """Program P1, frames 7--8: the distance to the next double, at three
    magnitudes, printed to two figures as the program's table prints it."""
    for key, x in (("one", 1.0), ("thousand", 1000.0), ("billion", 1e9)):
        got, want = f"{M.gap(x):.2e}", V[f"p01.gap.{key}"]
        assert got == want, (
            f"gap({x}) prints {got}; the program's table says {want}. "
            f"Re-read frames 7-8: the gap is read off the bits, not deduced.")


def test_1_gap_is_the_ulp_everywhere():
    """Program P1, frame 8: the invariant behind the table, not the three
    figures -- the gap at x is math.ulp(x) at every magnitude."""
    for x in (1.0, 8.0, 1e3, 1e9, 1e30, 0.3, 123456.789):
        assert M.gap(x) == math.ulp(x), (
            f"gap({x}) = {M.gap(x)!r} but the gap at {x} is {math.ulp(x)!r}")


# --- exercise 2: epsilon -----------------------------------------------------
def test_2_epsilon_matches_the_four_formats():
    """Program P1, frame 9: epsilon is the significand budget as a number."""
    for fmt in FORMATS:
        mbits = int(V[f"p01.{fmt}.mbits"])
        got, want = f"{M.epsilon(mbits):.2e}", V[f"p01.{fmt}.eps"]
        assert got == want, (
            f"epsilon({mbits}) prints {got} for {fmt}; the program says "
            f"{want}. Re-read frame 9.")


def test_2_decimal_digits_match():
    """Program P1, frame 9: about how many decimal digits each format has."""
    for fmt in FORMATS:
        mbits = int(V[f"p01.{fmt}.mbits"])
        got, want = M.decimal_digits(mbits), int(V[f"p01.{fmt}.digits"])
        assert got == want, (
            f"decimal_digits({mbits}) = {got} for {fmt}; the program says "
            f"{want}. It counts to the NEAREST digit.")


# --- exercise 3: tenth -------------------------------------------------------
def test_3_tenth_error_is_exactly_one_gap():
    """Program P1, frames 10--11: 0.1 + 0.2 is off by exactly one gap at
    0.3 -- the smallest error the format can make there."""
    got = M.error_in_gaps()
    assert got == 1.0, (
        f"error_in_gaps() = {got!r}; the error is exactly one gap at 0.3, "
        f"not approximately. Re-read frame 11.")
    shown = f"{abs(got * math.ulp(0.3)):.1e}"
    assert shown == V["p01.sum.gap"], (
        f"that gap prints {shown}; the program prints {V['p01.sum.gap']}")


# --- exercise 4: orders ------------------------------------------------------
def test_4_two_orders_disagree_as_printed():
    """Program P1, frames 13--14: the same sum, bracketed two ways, printed
    to seventeen decimals, is the pair the program prints."""
    a, b = float(V["p01.assoc.big"]), float(V["p01.assoc.small"])
    left, right = M.two_orders(a, b, b)
    got = (f"{left:.17f}", f"{right:.17f}")
    want = (V["p01.assoc.left"], V["p01.assoc.right"])
    assert got == want, (
        f"two_orders gives {got}; the program prints {want}. Re-read frame "
        f"14: each addition rounds immediately, so the ORDER decides.")


# --- exercise 5: threshold ---------------------------------------------------
def test_5_threshold_is_half_the_gap():
    """Program P1, frames 16--17: a contribution below half the gap at the
    running total vanishes; one above it moves the total."""
    for x in (1.0, 1e9, 0.3, 12345.0):
        t = M.threshold(x)
        assert x + t != x, f"threshold({x}) = {t!r} does not move {x}"
        assert x + t * 0.999 == x, (
            f"a value just under threshold({x}) = {t!r} still moves {x}, so "
            f"it is not the smallest such value")
        ratio = t / math.ulp(x)
        assert abs(ratio - 0.5) < 1e-9, (
            f"threshold({x}) is {ratio:.6f} gaps; frame 17 says half a gap")


def test_5_threshold_matches_the_table():
    """Program P1, frames 17--18: at 1 and at a billion, to two figures."""
    for key, x in (("one", 1.0), ("billion", 1e9)):
        got, want = f"{M.threshold(x):.1e}", V[f"p01.swamp.at.{key}"]
        assert got == want, (
            f"threshold({x}) prints {got}; the program prints {want}")


def test_5_the_coincidence_and_where_it_stops():
    """Program P1, frame 19: half a double's gap at a billion IS the fp32
    threshold at 1, exactly -- and at ten billion it is not. The second
    half is what stops a true sentence becoming a law."""
    at_billion = f"{M.threshold(1e9):.1e}"
    assert at_billion == V["p01.swamp.fp32"], (
        f"at a billion the threshold prints {at_billion}, not the fp32 row "
        f"{V['p01.swamp.fp32']}. Re-read frame 19.")
    at_ten_billion = f"{M.threshold(1e10):.1e}"
    assert at_ten_billion != V["p01.swamp.fp32"], (
        "at ten billion the coincidence should be gone; it is a property of "
        "the magnitude, not a law")


# --- exercise 6: store -------------------------------------------------------
def test_6_store_rounds_to_the_format():
    """Program P1, frames 20--24 and 32: storing in a narrower format is a
    rounding, and fp16's ceiling is the number the program says."""
    assert M.store(1.0, "fp64") == 1.0
    assert M.store(0.1, "fp32") != 0.1, "fp32 cannot hold 0.1 exactly"
    assert M.store(0.1, "fp32") == M.store(M.store(0.1, "fp32"), "fp32"), (
        "storing twice must be the same as storing once")
    assert M.store(float(V["p01.fp16.max.exact"]), "fp16") == float(
        V["p01.fp16.max.exact"]), "fp16's ceiling is representable in fp16"
    assert M.store(2.0 ** -150, "fp32") == 0.0, (
        "2**-150 is below fp32's second floor and must store as zero")


def test_6_flips_to_zero_match_the_table():
    """Program P1, frames 32--33: a fair coin, multiplied in, hits exactly
    zero one step past the format's second floor."""
    for fmt in ("fp64", "fp32", "fp16"):
        got, want = M.flips_to_zero(fmt), int(V[f"p01.coin.{fmt}"])
        assert got == want, (
            f"flips_to_zero({fmt!r}) = {got}; the program's table says "
            f"{want}. Round to the format after EVERY step.")


# --- exercise 7: bf16 --------------------------------------------------------
def test_7_bf16_rounds_to_nearest_even():
    """Program P1, frames 21--22: bf16 is fp32 with the bottom of the
    significand cut off, seven bits kept, ties to even."""
    assert M.to_bf16(1.0) == 1.0
    assert M.to_bf16(1.0 + 2.0 ** -7) == 1.0 + 2.0 ** -7, (
        "1 + 2**-7 is exactly representable in bf16 (seven significand bits)")
    assert M.to_bf16(1.0 + 2.0 ** -8) == 1.0, (
        "1 + 2**-8 is exactly half a bf16 gap above 1: a tie, which rounds "
        "to the even neighbour, 1.0")
    assert M.to_bf16(1.0 + 3 * 2.0 ** -8) == 1.0 + 2.0 ** -6, (
        "1 + 3*2**-8 is a tie between 1+2**-7 and 1+2**-6; the even one wins")


def test_7_bf16_row_and_further_problem_3():
    """Program P1, frame 33 and Further problem 3: bf16's coin-flip count,
    and a total of 100 that a quarter cannot move but anything above it can."""
    got, want = M.flips_to_zero("bf16"), int(V["p01.coin.bf16"])
    assert got == want, (
        f"flips_to_zero('bf16') = {got}; the program's table says {want}")
    total = float(V["p01.bf16.total"])
    half = float(V["p01.bf16.total.half"])
    assert M.to_bf16(total) == total, f"{total} must be exact in bf16"
    assert M.to_bf16(total + half) == total, (
        f"{total} + {half} is a tie and rounds back to {total}")
    assert M.to_bf16(total + half * 1.001) > total, (
        f"anything above {half} moves a bf16 total of {total}")
