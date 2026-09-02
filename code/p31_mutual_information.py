"""P31 --- Mutual information.

Every number Program P31 prints, and the assertions that keep them honest.

WHAT THE NEIGHBOURS ALREADY SPENT.  `grep -rn 'prog:P31' programs/en/*.tex`
prints the list with its contexts, and that grep was the first thing run.  Do
not restate it as a count here; the list is what is checkable.  What it names:

  P30  built the whole of the machinery -- the divergence itself, its
       non-negativity through P19's Jensen, zero exactly on agreement, the
       asymmetry, and that it is not a distance.  Mutual information IS that
       divergence between a joint and the product of its margins, so this
       program defines no new object: sections 1 to 3 are P30's quantity
       applied to one particular pair.  P30's closing frame says so by name
       AND says where the length goes: "P31 defines it, and spends most of
       its length on WHY THE CLAIMS PEOPLE MAKE WITH IT ARE USUALLY NOT
       SUPPORTED."  Its header hands over the data-processing inequality.
  P24  built THIS PROGRAM'S ARRIVAL and wrote the pointer.  Its covariance
       section takes the smallest space that shows a zero correlation proving
       nothing -- Z uniform on {-1, 0, 1} and W = Z^2 -- proves Cov(Z, W) = 0
       exactly over fractions, and then says "P31 builds the quantity that
       does see it".  So the arrival needs no new example: compute the new
       quantity on P24's own pair and the two numbers sit side by side.
  P29  owns entropy, surprise, the code-length theorem and the effective-count
       reading, and its header says "P31 owns mutual information".  Conditional
       entropy is NOT in it, so the chain rule is this program's to state.
  P23  owns independence and conditional independence, and says a table of
       pairwise correlations cannot settle independence.  That is the sentence
       section 1 cashes.
  P26  owns estimation, bias, and that an unbiased estimator is not the best
       one -- so "the estimators are biased in the direction that flatters the
       claim" lands against machinery the reader has rather than as a caution.
  P27  owns what a finite sample does to a comparison, which is section 5's
       setting one level up.

WHAT IS GENUINELY LEFT.  Greps across every written program return NOTHING for
`conditional entropy`, `chain rule of entropy`, `probing`, or the unhyphenated
`data processing`.  So: the chain rule, the estimation hazard, the DPI, and the
probing critique.  That is where the length belongs, which is what P30's
closing frame already said.

METHOD.  P30's discipline: enumerate where you can and let arithmetic do the
scaling, because a demonstration whose answer depends on a seed measures the
sampler.  Section 5's bias is therefore an EXACT EXPECTATION over every
contingency table rather than a mean over trials, and section 6's inequality
is checked against every channel on a rational grid.

Run:  python3 code/p31_mutual_information.py
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from itertools import product
from math import comb, log
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "figures" / "values" / "p31.tex"
TRANSCRIPT = OUT.parent.parent / "transcripts"
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
    """Refuse a percentage that rounds to 0 or 100 and so reads as exact."""
    r = round(x, 1)
    assert r not in (0.0, 100.0), (
        f"{x} rounds to {r} per cent, which reads as exact and is not.")
    return x


def reproduces(value: float, digits: int, *operands, op) -> float:
    """Refuse a quantity that does not come back out of its own printed page."""
    shown = [float(f"{v:.{d}f}") for v, d in operands]
    assert f"{op(*shown):.{digits}f}" == f"{value:.{digits}f}", (
        f"the page prints {value:.{digits}f} beside operands that give "
        f"{op(*shown):.{digits}f}; a reader who checks will find it wrong.")
    return value


# ======================================================================
# The quantities.  Everything is a sum over a finite joint, so the joint is
# a dict and nothing here needs a library.
# ======================================================================
def margins(joint):
    xs = sorted({x for x, _ in joint})
    ys = sorted({y for _, y in joint})
    px = {x: sum(joint.get((x, y), 0) for y in ys) for x in xs}
    py = {y: sum(joint.get((x, y), 0) for x in xs) for y in ys}
    return xs, ys, px, py


def entropy(p):
    return -sum(float(v) * log(float(v)) for v in p if v)


def mi(joint):
    """I(X;Y) in nats: the divergence from the joint to the product of margins."""
    xs, ys, px, py = margins(joint)
    s = 0.0
    for x, y in product(xs, ys):
        p = joint.get((x, y), 0)
        if p:
            s += float(p) * log(float(p) / (float(px[x]) * float(py[y])))
    return s


def cond_entropy(joint):
    """H(Y | X) = H(X, Y) - H(X)."""
    xs, ys, px, py = margins(joint)
    return entropy(list(joint.values())) - entropy(list(px.values()))


# ======================================================================
# 1.  The arrival.  Program P24 built the smallest space that shows a zero
#     correlation proving nothing -- Z uniform on {-1, 0, 1}, W = Z^2 -- and
#     wrote the pointer here.  Nothing new is invented: the new quantity is
#     computed on P24's own pair, and the two numbers sit side by side.
# ======================================================================
_P24_N = committed("p24.tex", "p24.tri.n")
assert _P24_N == "3", ("P24's construction has moved: it now says "
                       f"{_P24_N} outcomes, not 3, so this arrival is about a "
                       "different pair.")
TRI_N = int(_P24_N)

JOINT_ZW = {(z, z * z): Fraction(1, TRI_N) for z in (-1, 0, 1)}
_, _, _pz, _pw = margins(JOINT_ZW)

# the covariance P24 proves is exactly zero, recomputed rather than quoted
_cov = sum(Fraction(z) * Fraction(w) * p for (z, w), p in JOINT_ZW.items()) \
     - sum(Fraction(z) * p for (z, _), p in JOINT_ZW.items()) \
     * sum(Fraction(w) * p for (_, w), p in JOINT_ZW.items())
assert _cov == 0, _cov          # exactly, over fractions, as P24 says

I_ZW = mi(JOINT_ZW)
H_W = entropy(list(_pw.values()))
# W is a FUNCTION of Z, so being told Z removes every nat of W's uncertainty.
# Assert the identity, never the figure: a change of construction moves both.
assert abs(I_ZW - H_W) < 1e-12, (I_ZW, H_W)
emit("p31.zw.mi", I_ZW, 4)
emit("p31.zw.mi.bits", I_ZW / log(2), 4)
NOTES.append(
    f"  * gate: on P24's own zero-correlation pair the covariance is exactly 0"
    f" and I(Z;W) = {I_ZW:.4f} nats = H(W) identically, because W is a"
    f" function of Z -- the arrival needs no new example")

# AND THE TWO CONDITIONAL ENTROPIES ARE NOT EQUAL, which the first draft of
# this file asserted they were and which is a better frame than the claim it
# replaced.  W is a function of Z, so being told Z leaves NOTHING of W
# undetermined; being told W leaves Z ambiguous between -1 and +1.  So the
# pieces the quantity is built from are asymmetric while the quantity itself
# is not -- which is what section 3 elicits.
H_W_GIVEN_Z = cond_entropy(JOINT_ZW)                       # H(W | Z)
H_Z_GIVEN_W = cond_entropy({(w, z): p for (z, w), p in JOINT_ZW.items()})
H_Z = entropy(list(_pz.values()))
assert abs(H_W_GIVEN_Z) < 1e-12, H_W_GIVEN_Z               # exactly zero
assert H_Z_GIVEN_W > 0.4, H_Z_GIVEN_W                      # emphatically not
# the chain rule, both ways round, reaching ONE number from different pieces
assert abs((H_W - H_W_GIVEN_Z) - I_ZW) < 1e-12
assert abs((H_Z - H_Z_GIVEN_W) - I_ZW) < 1e-12
emit("p31.zw.hz", H_Z, 4)
emit("p31.zw.hzw", H_Z_GIVEN_W, 4)
reproduces(I_ZW, 4, (H_Z, 4), (H_Z_GIVEN_W, 4), op=lambda a, b: a - b)
NOTES.append(
    f"  * H(W|Z) = 0 exactly and H(Z|W) = {H_Z_GIVEN_W:.4f} nats: the two"
    f" conditional entropies are ASYMMETRIC while the mutual information they"
    f" both give is not -- one number reached from two different pieces")


# ======================================================================
# 2.  Symmetric, where the program before it was not.  Worth asserting
#     rather than stating: the reader has just spent a program on an
#     asymmetric quantity and will expect this one to be asymmetric too.
# ======================================================================
_SYM_TRIALS = 0
for _num in product(range(4), repeat=6):        # every 2x3 joint on a /15 grid
    _tot = sum(_num)
    if _tot == 0:
        continue
    _j = {(i, j): Fraction(_num[i * 3 + j], _tot) for i in range(2) for j in range(3)}
    _swapped = {(y, x): p for (x, y), p in _j.items()}
    assert abs(mi(_j) - mi(_swapped)) < 1e-12, _num
    assert mi(_j) >= -1e-12, _num               # non-negative, from P30
    _SYM_TRIALS += 1
emit("p31.sym.trials", _SYM_TRIALS)
NOTES.append(
    f"  * symmetric and non-negative on all {_SYM_TRIALS} joints of a 2x3"
    f" rational grid, with no tolerance beyond floating-point noise")


# ======================================================================
# 3.  THE HEADLINE.  The plug-in estimator returns a positive number on data
#     with no dependence at all.  This is an EXACT EXPECTATION, not a mean
#     over trials: for a 2x2 table with total N the outcomes are the
#     compositions of N into four cells, so every one is enumerated and its
#     multinomial weight is a Fraction.  The weights are asserted to sum to
#     exactly 1, which is what makes the enumeration a proof rather than a
#     sample -- P14's distinction, doing the job P05's greedy-packing failure
#     warns about, exactly as P30 §5 does it.
# ======================================================================
def plugin_mi_2x2(cell, N):
    a, b, c, d = cell
    px = ((a + b) / N, (c + d) / N)
    py = ((a + c) / N, (b + d) / N)
    s = 0.0
    for k, (i, j) in zip(cell, ((0, 0), (0, 1), (1, 0), (1, 1))):
        if k:
            p = k / N
            s += p * log(p / (px[i] * py[j]))
    return s


def exact_bias_2x2(N):
    """E[plug-in MI] when X and Y are INDEPENDENT and uniform.  The truth is
    exactly zero, so every nat this returns is the estimator's own."""
    total = Fraction(0)
    expect = 0.0
    tables = 0
    for a in range(N + 1):
        for b in range(N - a + 1):
            for c in range(N - a - b + 1):
                d = N - a - b - c
                w = Fraction(comb(N, a) * comb(N - a, b) * comb(N - a - b, c),
                             4 ** N)
                total += w
                expect += float(w) * plugin_mi_2x2((a, b, c, d), N)
                tables += 1
    assert total == 1, total          # the enumeration is COMPLETE, exactly
    return expect, tables


BIAS_NS = (10, 20, 50, 100)
_bias = {}
for _N in BIAS_NS:
    _e, _t = exact_bias_2x2(_N)
    _pred = 1 / (2 * _N)                       # (|X|-1)(|Y|-1)/2N at 2x2
    _bias[_N] = (_e, _t, _pred, _e / _pred)
    emit(f"p31.bias.n{_N}", _e, 6)
    emit(f"p31.bias.tables{_N}", _t)
    emit(f"p31.bias.ratio{_N}", _e / _pred, 3)
    # every one is POSITIVE on data whose true MI is exactly zero
    assert _e > 0, (_N, _e)

# The correction is worst exactly where the bias is largest, and it converges.
# Assert the SHAPE -- both the ordering and the convergence -- rather than any
# one figure, so a change of grid moves the numbers and cannot falsify the
# frame.
_ratios = [_bias[n][3] for n in BIAS_NS]
assert all(a > b for a, b in zip(_ratios, _ratios[1:])), _ratios
assert _ratios[0] > 1.25 and abs(_ratios[-1] - 1) < 0.05, _ratios
_biases = [_bias[n][0] for n in BIAS_NS]
assert all(a > b for a, b in zip(_biases, _biases[1:])), _biases
NOTES.append(
    f"  * EXACT: on data with no dependence at all the plug-in estimator"
    f" returns {_bias[10][0]:.4f} nats in expectation at N=10, falling to"
    f" {_bias[100][0]:.4f} at N=100 -- every contingency table enumerated and"
    f" the multinomial weights asserted to sum to exactly 1")
NOTES.append(
    f"  * and the textbook correction (|X|-1)(|Y|-1)/2N UNDERSTATES it worst"
    f" where the bias is largest: {_ratios[0]:.3f}x off at N=10, converging to"
    f" {_ratios[-1]:.3f}x by N=100 -- the remedy fails hardest in the regime"
    f" that needs it")

# THE SCALE-UP, and the first draft of it quoted the formula outside its own
# regime.  (|X|-1)(|Y|-1)/2N is asymptotic in N against the number of CELLS,
# and 16 x 16 has 256 of them: at N = 50 that is a fifth of a sample per
# cell, where a probe of this file measured 0.64x what the formula predicts.
# Quoting "2.25 nats, 81 per cent of the maximum" would have been a number
# the formula cannot support -- the very class section 3 is about, one level
# up.  So the scale-up is stated the way round that IS in regime and is
# exact arithmetic: how many items you need before the bias is small.
BIG_K = 16
_cells = BIG_K ** 2
_max_mi = log(BIG_K)
_TOL = Fraction(1, 100)                       # 1 per cent of the maximum
_need = (BIG_K - 1) ** 2 / (2 * float(_TOL) * _max_mi)
BIG_N = math.ceil(_need)
assert BIG_N / _cells > 10, (BIG_N, _cells)   # comfortably inside the regime
emit("p31.big.k", BIG_K)
emit("p31.big.cells", _cells)
emit("p31.big.max", _max_mi, 2)
emit("p31.big.need", BIG_N)
emit("p31.big.per", BIG_N / _cells, 0)
_bias_at_need = (BIG_K - 1) ** 2 / (2 * BIG_N)
emit("p31.big.bias", _bias_at_need, 4)
assert _bias_at_need < float(_TOL) * _max_mi, (_bias_at_need, _max_mi)
NOTES.append(
    f"  * scale-up, stated in regime: {BIG_K} categories each way is"
    f" {_cells} cells, and the bias falls under one per cent of the maximum"
    f" {_max_mi:.2f} nats only at N = {BIG_N} -- about {BIG_N / _cells:.0f}"
    f" items per cell, and nobody reports that alongside the estimate")


# ======================================================================
# 4.  The data-processing inequality, and it is worth reading from BOTH
#     ends.  If X -> Y -> Z then I(X;Z) <= I(X;Y): post-processing cannot
#     create information.  Every channel p(z|y) on a rational grid is
#     enumerated, so this is a proof over that family and not a search.
# ======================================================================
DPI_D = 6                                   # denominator of the channel grid


def _vectors(n, rem=DPI_D):
    """every probability vector of length n on the 1/DPI_D grid"""
    if n == 1:
        yield (Fraction(rem, DPI_D),)
        return
    for k in range(rem + 1):
        for rest in _vectors(n - 1, rem - k):
            yield (Fraction(k, DPI_D),) + rest


# a fixed joint on 2 x 3 with genuine dependence, so there is something to lose
JOINT_XY = {(0, 0): Fraction(3, 12), (0, 1): Fraction(2, 12), (0, 2): Fraction(1, 12),
            (1, 0): Fraction(1, 12), (1, 1): Fraction(2, 12), (1, 2): Fraction(3, 12)}
I_XY = mi(JOINT_XY)

_best = 0.0
_channels = 0
for _c0 in _vectors(2):
    for _c1 in _vectors(2):
        for _c2 in _vectors(2):
            _chan = {0: _c0, 1: _c1, 2: _c2}
            _jz: dict = {}
            for (_x, _y), _p in JOINT_XY.items():
                for _z in (0, 1):
                    _jz[(_x, _z)] = _jz.get((_x, _z), Fraction(0)) + _p * _chan[_y][_z]
            _i = mi(_jz)
            _channels += 1
            # NOTHING may exceed what the layer carried.  No tolerance beyond
            # floating-point noise: this is the inequality, not an estimate.
            assert _i <= I_XY + 1e-12, (_chan, _i, I_XY)
            _best = max(_best, _i)

emit("p31.dpi.ixy", I_XY, 4)
emit("p31.dpi.channels", _channels)
emit("p31.dpi.best", _best, 4)
# The page would print 74.1 per cent beside two values that divide to 74.2,
# which is the class F04, F05, P07, P12, P23 and P27 each paid for -- caught
# here by the guard written to enforce it, before it shipped.  F05's recorded
# fix applies: the exact percentage is not load-bearing, so STATE A BOUND and
# assert that the exact ratio AND the ratio of the printed values both clear
# it.  What the section needs is that a quarter is left behind, not 74.1.
_LEFT = Fraction(1, 4)
assert _best < float(1 - _LEFT) * I_XY, (_best, I_XY)
assert (float(f"{_best:.4f}")
        < float(1 - _LEFT) * float(f"{I_XY:.4f}")), (_best, I_XY)
# The gap is the half nobody says, so it is asserted as a property: the best
# available probe in this family is strictly short of what the layer carries.
assert _best < I_XY, (_best, I_XY)
NOTES.append(
    f"  * DPI: {_channels} channels enumerated on a 1/{DPI_D} grid and not one"
    f" exceeds I(X;Y) = {I_XY:.4f} nats -- post-processing cannot create"
    f" information, so a better probe is a statement about the probe")
NOTES.append(
    f"  * and the same inequality read from the other end: the BEST channel in"
    f" the family reaches {_best:.4f} nats and leaves MORE THAN A QUARTER of"
    f" what the layer carries behind -- a weak probe does not mean little"
    f" information, and the bound is loose by an amount nobody measures")


# ======================================================================
# 5.  What this book has NOT measured, stated rather than constructed.
#     P08, P11 and P19 each set the precedent: the empirical claim needs a
#     trained model's real activations, this book does not have one, and
#     building a plausible-looking one and reporting it is the fabrication
#     these rules forbid.  So the frames say so, and the number below is the
#     only thing about real models this program is entitled to assert -- it
#     is arithmetic about sample sizes, not a measurement of any layer.
# ======================================================================


# ======================================================================
# The transcript.  Deterministic -- no sample, no seed -- because the point
# is that an ORDINARY-looking table from two independent fair coins already
# reports a positive number.  The rounding is INSIDE the function, which is
# P19's rule, so the printed line and the printed result cannot come apart.
# ======================================================================
_lines = [
    ">>> from math import log",
    ">>> def plug_in(t):    # a 2x2 count table, MI in nats",
    "...     N = sum(t)",
    "...     px = ((t[0]+t[1])/N, (t[2]+t[3])/N)",
    "...     py = ((t[0]+t[2])/N, (t[1]+t[3])/N)",
    "...     ij = ((0,0), (0,1), (1,0), (1,1))",
    "...     s = sum((k/N) * log((k/N)/(px[i]*py[j]))",
    "...             for k, (i, j) in zip(t, ij) if k)",
    "...     return round(s, 4)",
    ">>> plug_in([5, 5, 5, 5])      # dead flat: nothing to see",
]
_flat = [5, 5, 5, 5]
_obs = [6, 4, 4, 6]


def _plug_in(t):
    N = sum(t)
    px = ((t[0] + t[1]) / N, (t[2] + t[3]) / N)
    py = ((t[0] + t[2]) / N, (t[1] + t[3]) / N)
    ij = ((0, 0), (0, 1), (1, 0), (1, 1))
    return round(sum((k / N) * log((k / N) / (px[i] * py[j]))
                     for k, (i, j) in zip(t, ij) if k), 4)


_lines.append(repr(_plug_in(_flat)))
_lines += [
    ">>> plug_in([6, 4, 4, 6])      # two fair coins, 20 tosses",
    repr(_plug_in(_obs)),
]
assert _plug_in(_flat) == 0.0                    # the only table that reports 0
assert _plug_in(_obs) > 0                        # and it is not the usual one
assert max(len(x) for x in _lines) <= 64, max(_lines, key=len)
TRANSCRIPT.mkdir(parents=True, exist_ok=True)
(TRANSCRIPT / "p31-plug-in.txt").write_text("\n".join(_lines) + "\n",
                                            encoding="utf8")
NOTES.append(
    f"  * the transcript is deterministic on purpose: an ordinary table from"
    f" two fair coins over {sum(_obs)} tosses reports {_plug_in(_obs)} nats,"
    f" and only the dead-flat table reports zero")


# ======================================================================
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf8") as fh:
    fh.write("% Generated by code/p31_mutual_information.py -- do not edit.\n")
    for k, (body, numeric) in VALUES.items():
        fh.write(f"\\{'mfaval' if numeric else 'mfavaltext'}{{{k}}}{{{body}}}\n")

print(f"P31: {len(VALUES)} values -> {OUT}")
for n in NOTES:
    print(n)
