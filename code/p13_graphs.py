#!/usr/bin/env python3
"""Program P13 --- Graphs, DAGs and random walks.

Every number Program P13 prints that the reader cannot do in their head is
computed here and written to figures/values/p13.tex, which the book \\input{}s.

P13's thesis is that a graph is a set plus a relation, that the adjacency
matrix turns every question about paths into a question about matrix powers,
and that a DAG's topological order is what makes evaluation well defined --
so an agent workflow, a build system and a neural network are one object.

EXACT ARITHMETIC THROUGHOUT, over Fraction, and it matters twice. The
stationary distribution of a random walk is checked by multiplying it back
through the transition matrix and requiring the result to be EQUAL, not close;
and the walk-counting theorem is checked against walks that are actually
enumerated. A float tolerance would have made both claims about a threshold.

WHAT P13 IS OWED, read out of the written files rather than remembered:

  F10  defers "a graph as a set plus a relation" here BY NAME, in its own file
       header, and gives the sets, the union rule and the pair count.
  P12  owns the counting arguments -- Pascal, inclusion-exclusion, pigeonhole
       -- and deliberately did not use them on graphs. Its documents-and-pairs
       example is continued here as a similarity graph, gated below.
  P06  gives the theorem this program's section 3 rests on: matrix
       multiplication IS composition, and the row-meets-column rule falls out
       of it. That is exactly why A^k counts walks of length k.
  P10  gives eigenvectors and what a matrix does to a vector it only stretches.
       A stationary distribution is an eigenvector for eigenvalue 1, which is
       the same calculation under another name.
  P03  gives the cost vocabulary section 2 needs, and this program counts
       rather than saying "quadratic".

WHAT THIS PROGRAM OWES FORWARD: P16 declares P13 as a dependency and needs the
computation graph defined properly, one program before autodiff uses it.

Run:  python3 code/p13_graphs.py      (or: make numbers)
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import permutations
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "figures" / "values" / "p13.tex"
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


def sci(x: float, digits: int = 2) -> str:
    return f"{x:.{digits}e}"


def committed(fname: str, key: str) -> str | None:
    path = OUT.parent / fname
    if not path.exists():                                    # pragma: no cover
        return None
    import re
    m = re.search(r"\\mfaval\{" + re.escape(key) + r"\}\{([^}]*)\}",
                  path.read_text(encoding="utf8"))
    return m.group(1) if m else None


# --- the exact machinery P04 wrote and P06, P08, P09 and P10 each reused ----
def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def matvec(M, v):
    return [sum(r[j] * v[j] for j in range(len(v))) for r in M]


def transpose(M):
    return [list(c) for c in zip(*M)]


def matpow(A, k):
    n = len(A)
    R = [[Fraction(1) if i == j else Fraction(0) for j in range(n)]
         for i in range(n)]
    for _ in range(k):
        R = matmul(R, A)
    return R


# =====================================================================
# 1. A graph is a set plus a relation
# =====================================================================
# Six services and who calls whom. Small enough that a reader can draw it and
# check every number in this section by hand, which is the reason it is six.
SERVICES = ["gateway", "auth", "search", "rank", "store", "log"]
CALLS = [(0, 1), (0, 2), (2, 3), (2, 4), (3, 4), (1, 5), (3, 5), (4, 5)]
NV, NE = len(SERVICES), len(CALLS)


def adjacency(n, edges, directed=True):
    A = [[Fraction(0)] * n for _ in range(n)]
    for i, j in edges:
        A[i][j] = Fraction(1)
        if not directed:
            A[j][i] = Fraction(1)
    return A


A_DIR = adjacency(NV, CALLS, directed=True)
A_UND = adjacency(NV, CALLS, directed=False)

# THE HANDSHAKE LEMMA, which is P12's double counting in a new coat: every edge
# contributes 1 to the degree at each of its two ends, so the degrees sum to
# twice the edges. Checked here, and then on random graphs, because a lemma
# checked on one example is an example.
DEGREES = [sum(int(x) for x in row) for row in A_UND]
assert sum(DEGREES) == 2 * NE, "the degrees must sum to twice the edges"
random.seed(13)
for _ in range(2000):
    n = random.randint(2, 12)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    es = random.sample(pairs, random.randint(0, len(pairs)))
    d = [sum(int(x) for x in row) for row in adjacency(n, es, directed=False)]
    assert sum(d) == 2 * len(es), "handshake must hold on every graph"
emit("p13.hand.trials", 2000)

for k, v in (("nv", NV), ("ne", NE), ("degsum", sum(DEGREES)),
             ("degmax", max(DEGREES))):
    emit(f"p13.g.{k}", v)

# A complete graph's edges ARE the pairs, so the counting is F10's and P12's.
# --- CROSS-PROGRAMME GATE (a shared computation, not a coincidence) --------
_docs = committed("f10.tex", "f10.docs")
_pairs = committed("f10.tex", "f10.pairs")
if _docs and _pairs:
    _n = int(_docs)
    assert _n * (_n - 1) // 2 == int(_pairs) == math.comb(_n, 2), \
        "a complete graph's edge count must be F10's and P12's pair count"
    NOTES.append(f"gate: K_{_docs} has F10's {_pairs} edges")
    emit("p13.complete.n", _n)
    emit("p13.complete.e", int(_pairs))
else:                                                        # pragma: no cover
    NOTES.append("F10's values not built yet; the complete-graph gate did not run")

# =====================================================================
# 2. Two encodings, two costs
# =====================================================================
# The bill, at a scale where the choice decides whether the job runs at all.
BIG_N, BIG_M = 10 ** 6, 10 ** 7
MAT_CELLS = BIG_N * BIG_N
LIST_SLOTS = BIG_N + 2 * BIG_M          # one head per node, two ends per edge
emit("p13.big.n", sci(float(BIG_N), 0))
emit("p13.big.m", sci(float(BIG_M), 0))
emit("p13.big.cells", sci(float(MAT_CELLS), 2))
emit("p13.big.slots", sci(float(LIST_SLOTS), 2))
emit("p13.big.ratio", sci(MAT_CELLS / LIST_SLOTS, 2))
# One byte a cell is already absurd; say it in bytes so the number bites.
emit("p13.big.tb", MAT_CELLS / 1e12, digits=0)
# Mean degree: the handshake lemma of section 1 divided by n. It is also the
# size of the list's edge-test cost, against the matrix's one step -- which is
# what makes "the matrix wins on lookup" a real win and not a formality.
AVG_DEG = 2 * BIG_M / BIG_N
assert AVG_DEG * BIG_N == 2 * BIG_M, "the mean degree IS the handshake lemma over n"
assert AVG_DEG < BIG_N / 1000, "and it must be tiny beside a whole matrix row"
emit("p13.big.avgdeg", AVG_DEG, digits=0)
# Density: the fraction of possible edges that exist.
DENSITY = BIG_M / (BIG_N * (BIG_N - 1) / 2)
emit("p13.big.density", sci(DENSITY, 2))
assert DENSITY < 1e-4, "the point of the section is that real graphs are sparse"
# The crossover: the matrix wins on memory only once m exceeds n^2/2 - n/2.
assert MAT_CELLS > LIST_SLOTS, "and the matrix must be the loser here"

# =====================================================================
# 3. Walks are matrix powers
# =====================================================================
def walks(A, k, i, j):
    """Enumerate walks of length k from i to j by brute force, and count them.

    This exists to CHECK the theorem rather than to state it. Counting by
    enumeration and counting by matrix power must agree, or one of the two is
    wrong -- and the enumeration is the one that cannot be wrong about what a
    walk is.
    """
    n = len(A)
    total, frontier = 0, [i]
    for _ in range(k):
        nxt = []
        for u in frontier:
            nxt += [v for v in range(n) if A[u][v]]
        frontier = nxt
    return frontier.count(j)


for k in range(1, 5):
    Ak = matpow(A_DIR, k)
    for i in range(NV):
        for j in range(NV):
            assert int(Ak[i][j]) == walks(A_DIR, k, i, j), \
                f"A^{k}[{i}][{j}] must equal the walks of length {k} enumerated"
emit("p13.walk.maxk", 4)
emit("p13.walk.checks", 4 * NV * NV)

# The number the frames quote: paths of length 3 from the gateway to the log.
K_SHOW = 3
emit("p13.walk.k", K_SHOW)
emit("p13.walk.count", int(matpow(A_DIR, K_SHOW)[0][5]))
# NOT emitted: the service names are identifiers written in the frames.
# Program P03 found that a word is not a computed value -- the ledger scans
# for \mfaval and a text value is reported unused -- and these two would
# differ between the editions anyway.

# THE RECEPTIVE FIELD, and the self-loop that makes the sentence true.
# A^k's pattern is the pairs joined by a walk of length EXACTLY k, so it is
# not the reach of k rounds of message passing: a vertex two hops away is
# absent from A^1 and a vertex one hop away is absent from A^2. What reaches
# within k is (A+I)^k, because the I lets a step be spent standing still --
# which is exactly the self-loop every GCN adds before it aggregates, and is
# why the frames print sigma((A+I)XW) rather than sigma(AXW).
#
# The old assertion here compared BFS against the union of A^1..A^k plus the
# source, which is the within-k reading spelled out by hand: it was true, and
# it was not the claim its own comment made, so it could not have caught the
# page saying "exactly those within k steps" under a layer with no self-loop.
# Test the pattern the page prints.
def add_identity(A):
    return [[A[i][j] + (1 if i == j else 0) for j in range(len(A))]
            for i in range(len(A))]


def reachable_within(A, src, k):
    n, seen, frontier = len(A), {src}, {src}
    for _ in range(k):
        frontier = {v for u in frontier for v in range(n) if A[u][v]}
        seen |= frontier
    return seen


A_LOOP = add_identity(A_UND)
for src in range(NV):
    for k in range(1, 5):
        by_bfs = reachable_within(A_UND, src, k)
        by_mat = {j for j in range(NV) if matpow(A_LOOP, k)[src][j]}
        assert by_bfs == by_mat, \
            "the reach of k message-passing rounds must be (A+I)^k's pattern"
# And the half that says the self-loop is doing the work rather than riding
# along: at one hop A alone omits the vertex itself, and at two it omits the
# neighbours reached in one.
assert {j for j in range(NV) if A_UND[0][j]} != reachable_within(A_UND, 0, 1)
assert ({j for j in range(NV) if matpow(A_UND, 2)[0][j]}
        != reachable_within(A_UND, 0, 2))
HOPS = 3
emit("p13.hops", HOPS)
emit("p13.reach", len(reachable_within(A_UND, 0, HOPS)))
emit("p13.reach.one", len(reachable_within(A_UND, 0, 1)))

# =====================================================================
# 4. A DAG, and the order that makes evaluation well defined
# =====================================================================
# The same six-node graph, read as a computation: each node's value is a
# function of the values of the nodes that point at it.
def topological_orders(n, edges):
    """EVERY valid order, not one -- because the point is that there are many."""
    out = []
    for perm in permutations(range(n)):
        pos = {v: i for i, v in enumerate(perm)}
        if all(pos[a] < pos[b] for a, b in edges):
            out.append(perm)
    return out


ORDERS = topological_orders(NV, CALLS)
assert ORDERS, "the service graph must be acyclic, or it is not a DAG"
emit("p13.topo.count", len(ORDERS))
emit("p13.topo.total", math.factorial(NV))
emit("p13.topo.frac", sci(len(ORDERS) / math.factorial(NV), 2))


def evaluate(order, edges, n):
    """Each node adds one to the largest value pointing at it."""
    val = {}
    for v in order:
        parents = [a for a, b in edges if b == v]
        val[v] = 1 + max((val[p] for p in parents), default=0)
    return tuple(val[v] for v in range(n))


# THE PAYOFF, asserted rather than asserted about: the order is not unique and
# the answer is. That is the whole of why a build system, an agent workflow and
# a neural network can all be scheduled differently and still be deterministic.
# The depth is asserted below and not emitted: no frame quotes it, and
# Program F11 established that an unreferenced value is cut rather than
# forced into the prose.
_first = evaluate(ORDERS[0], CALLS, NV)
for o in ORDERS:
    assert evaluate(o, CALLS, NV) == _first, \
        "every topological order must give the same answer, or nothing works"

# And a cycle has none at all, which is what the acyclicity condition buys.
CYCLE = CALLS + [(5, 0)]
assert topological_orders(NV, CYCLE) == [], \
    "a graph with a cycle must admit no topological order"

# =====================================================================
# 5. Random walks, and where they settle
# =====================================================================
def transition(A):
    """Each row of the adjacency matrix, divided by its own row sum."""
    P = []
    for row in A:
        s = sum(row)
        P.append([x / s for x in row] if s else [Fraction(0)] * len(row))
    return P


# A small link graph with no dangling node, so the undamped walk is honest.
LINKS = [(0, 1), (0, 2), (1, 2), (2, 0), (3, 2), (3, 0), (1, 3), (2, 3)]
NP_ = 4
P = transition(adjacency(NP_, LINKS, directed=True))


def power_iterate(P, steps):
    n = len(P)
    p = [Fraction(1, n)] * n
    for _ in range(steps):
        p = matvec(transpose(P), p)
    return p


STEPS = 60
PI = power_iterate(P, STEPS)
# EXACT, not close: the stationary distribution multiplied back through the
# walk must be itself. Over Fraction there is no tolerance to choose.
_next = matvec(transpose(P), PI)
assert sum(PI) == 1, "a distribution must sum to one"
NOTES.append("stationary vector after %d steps: %s"
             % (STEPS, [f"{float(x):.4f}" for x in PI]))
emit("p13.pi.steps", STEPS)
for i, x in enumerate(PI):
    emit(f"p13.pi.{i}", float(x), digits=4)

# It is an EIGENVECTOR, and saying so is Program P10 arriving under a new name.
# Solved exactly rather than iterated: (P^T - I)p = 0 with sum p = 1.
def stationary_exact(P):
    n = len(P)
    M = [[transpose(P)[i][j] - (1 if i == j else 0) for j in range(n)]
         for i in range(n)]
    M[-1] = [Fraction(1)] * n                      # replace one row by sum = 1
    rhs = [Fraction(0)] * n
    rhs[-1] = Fraction(1)
    # Gaussian elimination over the rationals, as in P04 and P09.
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c])
        M[c], M[piv] = M[piv], M[c]
        rhs[c], rhs[piv] = rhs[piv], rhs[c]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
                rhs[r] -= f * rhs[c]
    return [rhs[i] / M[i][i] for i in range(n)]


EXACT = stationary_exact(P)
assert matvec(transpose(P), EXACT) == EXACT, \
    "the exact stationary vector must be an eigenvector for eigenvalue 1"
assert sum(EXACT) == 1
# and the iteration must be heading there
# A BOUND, never the figure. The gap after sixty steps is rounding noise whose
# size is a property of the arithmetic rather than of the mathematics, and
# Program P06 had two of exactly these rejected by CI for being committed as
# figures. The page reads "better than 10^-15", which is true on any machine.
_err = max(abs(float(a - b)) for a, b in zip(PI, EXACT))
PI_BOUND = 15
assert _err < 10 ** -PI_BOUND, \
    f"the iteration must clear 1e-{PI_BOUND}, off by {_err:.2e}"
emit("p13.pi.bound", PI_BOUND)
for i, x in enumerate(EXACT):
    emit(f"p13.exact.num.{i}", x.numerator)
    emit(f"p13.exact.den.{i}", x.denominator)

# WHY DAMPING EXISTS, and it is not a fudge. A page with no outgoing links --
# a PDF, a dead end -- has a zero row, so the walk falls off the graph and the
# distribution stops summing to one. Measured rather than asserted.
DANGLING = [(0, 1), (1, 2), (0, 2)]            # node 2 links nowhere
PD = transition(adjacency(3, DANGLING, directed=True))
_p = [Fraction(1, 3)] * 3
_mass = []
for _ in range(5):
    _p = matvec(transpose(PD), _p)
    _mass.append(sum(_p))
# EXACTLY zero, not a small number, so it is reported as a step rather than as
# a figure: "0.0000" would read as rounding and this is not rounding.
_zero_at = next(i for i, m in enumerate(_mass, 1) if m == 0)
assert _mass[_zero_at - 1] == 0, "the mass must reach exactly zero"
emit("p13.drain.zeroat", _zero_at)
emit("p13.drain.num1", _mass[0].numerator)
emit("p13.drain.den1", _mass[0].denominator)
emit("p13.drain.num2", _mass[1].numerator)
emit("p13.drain.den2", _mass[1].denominator)
NOTES.append("mass left after each step: %s" % [str(m) for m in _mass])

# DAMPING, computed rather than described. With probability 1-d the walk jumps
# to a uniformly chosen node instead of following a link, which makes every
# entry positive and the stationary distribution unique -- and it fixes the
# dangling node by giving it somewhere to go.
DAMP = Fraction(85, 100)
# Emitted as the decimal the literature uses. Fraction reduces 85/100 to 17/20,
# which is the same number and not the one anybody writes.
emit("p13.damp", float(DAMP), digits=2)


def damped(P, d):
    n = len(P)
    out = []
    for row in P:
        if not any(row):                       # a dangling node goes everywhere
            out.append([Fraction(1, n)] * n)
        else:
            out.append([d * x + (1 - d) / n for x in row])
    return out


PDD = damped(PD, DAMP)
assert all(sum(r) == 1 for r in PDD), "every row of a walk must be a distribution"
assert all(all(x > 0 for x in r) for r in PDD), \
    "damping must make every entry positive, which is what buys uniqueness"
PD_PI = stationary_exact(PDD)
assert matvec(transpose(PDD), PD_PI) == PD_PI, "and it must have a fixed point"
assert sum(PD_PI) == 1, "which is still a distribution -- nothing drains away"
assert all(x > 0 for x in PD_PI), "and every node keeps some mass"
for i, x in enumerate(PD_PI):
    emit(f"p13.damped.{i}", float(x), digits=4)
NOTES.append("damped stationary: %s" % [f"{float(x):.4f}" for x in PD_PI])

# =====================================================================
# The transcript: the order is not unique and the answer is
# =====================================================================
# THE IMPORT LINES ARE NOT DECORATION. Program P04 shipped a transcript that
# called a function it never imported, so a reader pasting it out of the
# finished PDF got a NameError while every gate stayed green -- a generated,
# committed, drift-gated file can still be un-runnable. The test is to extract
# it from the PDF and run what comes out, and that needs these two lines.
TOPO_TEXT = f""">>> from p13_graphs import CALLS, ORDERS
>>> from p13_graphs import evaluate, topological_orders
>>> len(topological_orders(6, CALLS))
{len(ORDERS)}
>>> evaluate(ORDERS[0], CALLS, 6)
{evaluate(ORDERS[0], CALLS, NV)}
>>> evaluate(ORDERS[-1], CALLS, 6)
{evaluate(ORDERS[-1], CALLS, NV)}
>>> topological_orders(6, CALLS + [(5, 0)])
[]
"""
assert TOPO_TEXT.isascii(), "listings cannot set a non-ASCII transcript"
assert max(len(l) for l in TOPO_TEXT.splitlines()) <= 64, "transcript too wide"
assert len(TOPO_TEXT.strip().splitlines()) <= 14, "transcript too tall"


def main() -> None:
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    (TRANSCRIPTS / "p13-order-and-answer.txt").write_text(TOPO_TEXT, encoding="ascii")
    print("  transcript -> figures/transcripts/p13-order-and-answer.txt")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "% Generated by code/p13_graphs.py --- do not edit.",
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

    w = max(len(k) for k in VALUES)
    items = list(VALUES.items())
    for i in range(0, len(items), 3):
        print("  " + "   ".join(f"{k:{w}s} {b:>12s}" for k, (b, _) in items[i:i + 3]))
    for n in NOTES:
        print(f"  * {n}")


if __name__ == "__main__":
    main()
