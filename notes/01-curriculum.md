# Matematyka od zera dla inżyniera AI / Mathematics from Zero for the AI Engineer

## Table of contents — the reasoned program list

Design document. Read `llm-book/CLAUDE.md` and `maf-book/CLAUDE.md` first; this
book inherits their conventions and adds Stroud's programmed-learning skeleton
on top.

Status of this document: **a proposal, not a draft.** Nothing here has been
written and none of the measurements listed at the bottom has been run.

---

## 1. What the book is, in one paragraph

A working AI engineer can call `torch.nn.functional.softmax` and cannot say why
it is subtracted from its own maximum first. This book takes a reader who
genuinely remembers nothing past school arithmetic and walks them, in small
numbered frames with an answer demanded at nearly every one, to the point where
they can derive scaled dot-product attention, state what the `1/sqrt(d_k)` is
doing, and defend or demolish a benchmark table. It uses K. A. Stroud's
programmed-learning method exactly, and it fixes the five things that method
leaves out for this audience: real linear algebra, statistical inference and
Bayes, information theory, optimisation, and enough discrete mathematics and
numerics to reason about a program rather than a formula.

It ships in Polish and English from one source tree.

---

## 2. The shape

Nine parts. **13 Foundation programs (F1--F13)** and **33 main programs
(P1--P34)**.

| Part | Programs | Why it exists |
|---|---|---|
| I --- Podstawy / Foundation | F1--F13 | Assumes nothing. Triaged by Quiz; a competent reader skips most of it in an afternoon. |
| II --- Liczba, precyzja i koszt / Number, precision and cost | P1--P3 | What the machine actually computes, and what an operation costs. Placed first because everything after it is arithmetic on a finite machine. |
| III --- Algebra liniowa / Linear algebra | P4--P11 | Stroud's largest gap. Eight programs, because this is the subject the audience uses daily and understands least. |
| IV --- Struktury dyskretne i argumentacja / Discrete structures and argument | P12--P14 | Counting, graphs, and how to read a theorem without believing more than it says. Placed before calculus so that "DAG" and "for all epsilon" are defined when they are first needed. |
| V --- Rachunek różniczkowy i różniczkowanie automatyczne / Calculus and automatic differentiation | P15--P18 | The chain rule, taken all the way to what `loss.backward()` actually does. |
| VI --- Optymalizacja / Optimisation | P19--P22 | Absent from Stroud's first volume entirely. |
| VII --- Prawdopodobieństwo i statystyka / Probability and statistics | P23--P28 | Stroud stops at the normal distribution. This part goes to inference, bootstrap and Bayes, because the audience's real job is deciding whether a measured difference is real. |
| VIII --- Teoria informacji / Information theory | P29--P31 | Absent from Stroud. It is where the loss function comes from. |
| IX --- Złożenie / Assembling it | P32--P34 | Three capstone programs that spend the whole book on one architecture, one training run and one evaluation. No new mathematics. |

Planned **2,418 frames**. The estimate that stood here — 460--540 pages at
this page geometry — **is falsified by the written book and is wrong by a
factor of about three**; see §20 item 1, which now carries the measurement.
All forty-seven programs are written, and they set 1,321 pages in the trade
format. The split into Parts I--VI and Parts VII--IX is still the clean one,
and it is still an open question rather than a decision — but it is now a
question with a number in front of it, and the number will not move again
except by the appendices.

---

## 3. Part I --- Podstawy / Foundation (F1--F13)

Assumes genuinely nothing: no algebra, no trigonometry, no calculus. Every
Foundation program opens with a **Quiz** that is both the diagnostic on entry
and the exit test, exactly as Stroud does it. A reader who passes the Quiz reads
the Summary and moves on.

Foundation is not a watered-down version of the main parts. It is bent
deliberately towards the payoff: logarithms get a whole program because
log-space arithmetic is load-bearing three parts later, and the chain rule gets
the longest Foundation program in the book because backpropagation is the chain
rule and nothing else.

| # | Title (EN) | Tytuł (PL) | Frames |
|---|---|---|---|
| F1 | Numbers, powers and roots | Liczby, potęgi i pierwiastki | 55 |
| F2 | The language of algebra | Język algebry | 50 |
| F3 | Logarithms and logarithmic scales | Logarytmy i skale logarytmiczne | 45 |
| F4 | Sums, products and sequences | Sumy, iloczyny i ciągi | 40 |
| F5 | Functions and graphs | Funkcje i wykresy | 45 |
| F6 | Equations, inequalities and the straight line | Równania, nierówności i prosta | 45 |
| F7 | Exponential, logistic and hyperbolic functions | Funkcja wykładnicza, logistyczna i funkcje hiperboliczne | 40 |
| F8 | Trigonometry and the unit circle | Trygonometria i okrąg jednostkowy | 45 |
| F9 | Vectors in the plane and in space | Wektory na płaszczyźnie i w przestrzeni | 40 |
| F10 | Sets, logic and counting | Zbiory, logika i zliczanie | 40 |
| F11 | The derivative: rate of change | Pochodna: tempo zmian | 45 |
| F12 | Rules of differentiation and the chain rule | Reguły różniczkowania i reguła łańcuchowa | 55 |
| F13 | The integral: accumulation and area | Całka: sumowanie i pole | 45 |

**F1 --- Numbers, powers and roots.** Argument: arithmetic is a set of rules you
can check, and scientific notation is how you hold quantities you cannot
picture. Payoff: a 7-billion-parameter model in `fp16` is 14 GB, and the reader
computes that rather than repeating it; orders of magnitude for tokens, FLOPs
and dollars.

**F2 --- The language of algebra.** Argument: a symbol stands for a quantity you
have not fixed yet, and rearranging is a sequence of legal moves. Payoff: read a
paper's equation as executable code; rearrange a loss so the thing you want is
on the left. Trap: `(a+b)^2` and the reader who writes `a^2+b^2`, elicited
before it sets.

**F3 --- Logarithms and logarithmic scales.** Argument: a logarithm turns
multiplication into addition, and that is the only reason anybody uses one.
Payoff: probabilities of a 2,000-token sequence multiply to something no float
can hold, so we sum log-probabilities instead; perplexity is `exp` of a mean
log; a loss curve is plotted on a log axis because the interesting part is the
ratio, not the difference. This is the most load-bearing Foundation program in
the book.

**F4 --- Sums, products and sequences.** Argument: sigma and pi notation are
loops. Payoff: every loss in machine learning is a sigma divided by `n`; an
exponential moving average is a two-line recurrence, and it is the whole of
momentum and half of Adam, met here with no calculus attached.

**F5 --- Functions and graphs.** Argument: a function is a machine with one
output per input, and shifting, scaling and reflecting its graph are four moves
you can do by eye. Payoff: an activation function is a graph you can recognise;
weight and bias are scale and shift; a monotone transformation does not move the
argmax, which is why temperature changes what you sample but not what is most
likely.

**F6 --- Equations, inequalities and the straight line.** Argument: solving is
undoing. Payoff: `y = wx + b` is the entire linear model; a decision threshold
is an inequality; a clipped value is two inequalities.

**F7 --- Exponential, logistic and hyperbolic functions.** Argument: `e^x` is
the function that is its own rate of change, and the logistic curve is what you
get when you squash it into `[0,1]`. Payoff: sigmoid and tanh drawn rather than
recited; saturation seen as the flat part of a graph, which is the visual form
of the vanishing-gradient complaint; `softmax` previewed as exponentials divided
by their own sum.

**F8 --- Trigonometry and the unit circle.** Argument: sine and cosine are the
coordinates of a point going round a circle. Payoff: cosine similarity is
literally the cosine of an angle; sinusoidal positional encodings and rotary
embeddings are rotations, and this is the program that makes "rotate the query
and key" a sentence rather than an incantation.

**F9 --- Vectors in the plane and in space.** Argument: a vector is a list of
numbers you may also draw as an arrow. Payoff: an embedding is a point in a
space with too many dimensions to draw, and every intuition the reader is about
to build in 2-D will have to be tested against high dimension in P5.

**F10 --- Sets, logic and counting.** Argument: membership, union, intersection,
and the three ways to count without listing. Payoff: a vocabulary is a set and a
tokeniser is a function into it; a boolean mask is a set indicator; counting is
the denominator of every naive probability; a nested loop over a set is
`n^2` before anybody has said "complexity".

**F11 --- The derivative: rate of change.** Argument: the slope of a curve at a
point, built from first principles by shrinking a chord. Payoff: gradient
descent has a mechanism, and the reader has seen it before meeting the word.

**F12 --- Rules of differentiation and the chain rule.** Argument: four rules
and one composition rule cover everything the book will differentiate. Payoff:
**backpropagation is the chain rule applied to a composition of layers**, and
that sentence is the hinge of the entire book. The longest Foundation program
for that reason.

**F13 --- The integral: accumulation and area.** Argument: integration
accumulates, and it undoes differentiation. Payoff: the probability of a
continuous quantity is an area, an expectation is an integral, and the
denominator that makes a density integrate to one is the "normalising constant"
that will keep reappearing.

---

## 4. Part II --- Liczba, precyzja i koszt / Number, precision and cost (P1--P3)

Placed first among the main programs, before linear algebra, and this is a
deliberate departure from every mathematics curriculum. The reason: a maths book
for engineers that waits 400 pages to admit that the machine cannot represent
`0.1` has spent 400 pages teaching a fiction. Everything after this part is
arithmetic performed by a finite machine on a budget, and the reader should know
what both of those mean before they start.

## 5. Part III --- Algebra liniowa / Linear algebra (P4--P11)

Eight programs. Stroud teaches matrices as a set of recipes --- determinants by
cofactor expansion, an inverse by adjugate, eigenvalues by solving a
characteristic polynomial --- and never mentions a vector space. That is exactly
backwards for this audience: the recipes are what a library does for you, and
the structural facts are what you need to read a model architecture.

## 6. Part IV --- Struktury dyskretne i argumentacja / Discrete structures and argument (P12--P14)

Three programs, placed here rather than at the end. The placement is the
argument: a computation graph is a DAG and reverse-mode differentiation is a
reverse topological traversal, so the reader should have met a DAG *before* P16
rather than after it. Logic and proof come before the calculus and probability
parts for the same reason --- the reader is about to start meeting statements of
the form "for every epsilon there exists an N", and being able to parse one is a
prerequisite, not a capstone.

## 7. Part V --- Rachunek różniczkowy i różniczkowanie automatyczne / Calculus and automatic differentiation (P15--P18)

## 8. Part VI --- Optymalizacja / Optimisation (P19--P22)

Stroud has no optimisation in the first volume at all. For this audience it is
the subject the job actually consists of.

## 9. Part VII --- Prawdopodobieństwo i statystyka / Probability and statistics (P23--P28)

Stroud's statistics is descriptive plus the normal distribution: no estimation,
no inference, no Bayes. That is the difference between describing a sample and
deciding whether a difference is real, and deciding whether a difference is real
is what this audience is paid for.

## 10. Part VIII --- Teoria informacji / Information theory (P29--P31)

Entirely absent from Stroud. It is where the loss function comes from, so it
cannot be absent here.

## 11. Part IX --- Złożenie / Assembling it (P32--P34)

Three capstone programs. **No new mathematics.** Everything is a withdrawal from
an account opened earlier, and each frame that uses a result names the program
it came from. This is the part that makes the book's promise concrete, and it is
the analogue of the capstone chapter in both companion volumes.

## 12. Dependencies

Soft dependencies (a program is more rewarding after another, but does not
require it) are marked *soft*. Everything else is hard: the later program uses a
result the earlier one establishes.

**Foundation**

```
F2  <- F1
F3  <- F1, F2
F4  <- F2
F5  <- F2, F4
F6  <- F2, F5
F7  <- F3, F5
F8  <- F5
F9  <- F6, F8
F10 <- F1
F11 <- F5, F6
F12 <- F11, F7
F13 <- F11
```

**Main**

**This list used to be written out here, and it was wrong from `P7` onward.**

The August 2026 curriculum review inserted `P7` (tensors, shapes and index
notation) and moved everything after it up one. It renumbered the sequence and
it re-derived the declared forward-reference list; it did not touch this graph,
so every edge from `P7` on named the program that used to hold the material
— `P11 <- F10, F4` for combinatorics, which is now `P12`, and so on to the end.
It also had 33 main programs where there are now 34.

**The graph lives in `tools/programs.json`**, in each program's `deps` field,
which is what `gen_stubs.py` and the forward-reference check actually read. It
is not duplicated here, and that is the point: the same off-by-one was found in
the manifest's own prose pointers and swept out of it in a pass of its own, and
a corrected copy in this file would simply be the next thing to go stale at the
next insertion. Re-derive from the manifest; do not copy an edge out of a note.

To read the graph:

```
python3 -c "import json;[print(f\"{p['key']:4s}<- {', '.join(p['deps'])}\")
  for p in json.load(open('tools/programs.json'))['programs']]"
```

**The one ordering conflict, and how it is resolved.** P21 (stochastic
optimisation) needs random variables and variance from P24--P25, which sit in
Part VII, two parts later. Three options were considered: move the whole
probability part before optimisation; split P21; or let P21 carry a forward
reference. The resolution is the first one *locally* --- **P21 states its two
probability prerequisites in its Learning outcomes and points at P24 and P25 for
a reader who does not already have them**, and P24 and P25 revisit minibatch
noise as a worked example once the machinery exists. It is the only place in the
book where a program's prerequisite comes after it, it is deliberate, and it is
recorded here so that nobody "fixes" it by reordering the parts and breaking six
other dependencies.

**Discharged, August 2026, in the passes that wrote P24 and P25**, and in two
halves: P24 returned the definition on P21's own population, gated against its
committed mean, and said in as many words that the `1/B` rate is P25's; P25
derived that rate and gated it against P21's committed population spread. It is
the book's oldest declared forward reference and it is closed.

A second, milder case: P22 reads better after P30's KL material, and P20 reads
better after P11's conditioning. Both are marked soft and both are written to
stand alone.

---

## 13. What this book will not teach, and where it sends you

An honest scope statement belongs in the front matter as well as here. The house
rule is that the book may say a topic is not worth its cost to this reader; it
may not pretend the topic does not exist.

| Not taught | Why not | Where to go |
|---|---|---|
| Measure-theoretic probability | Nothing in this book's payoff requires a sigma-algebra, and the machinery costs a semester. | Williams, *Probability with Martingales*; Durrett. |
| Real analysis and proof technique at epsilon-delta level | P14 teaches you to *read* a theorem, deliberately not to write one. This is Stroud's largest gap and the book fixes only half of it, on purpose. | Abbott, *Understanding Analysis*; Tao, *Analysis I*. |
| Partial differential equations | The audience meets them in physics-informed and diffusion work, and neither is served by a shallow treatment. | Strauss; Evans. |
| Stochastic differential equations, and therefore the full mathematics of diffusion models | **No program works a forward process, and this entry used to claim one did.** What the book gives is the Gaussian (P24) and the fact that variances of independent quantities add (P25), which is the whole of a discrete-time chain of Gaussians; it never applies them to one. The continuous-time formulation needs Itô calculus. | Särkkä and Solin, *Applied SDEs*. |
| Complex analysis and the Fourier transform beyond a mention | F8 gives the unit circle; convolution theorems and spectral methods are a book of their own. | Bracewell; Osgood's lecture notes. |
| Numerical linear algebra at implementation level | P09 tells you why not to invert a matrix and P11 why the normal equations square the condition number; it does not teach you to implement a QR factorisation. | Trefethen and Bau; Higham, *Accuracy and Stability*. |
| Convex optimisation theory, duality in full | P19 and P22 give the working subset. The full theory is one of the best-written books in mathematics and there is no case for paraphrasing it. | Boyd and Vandenberghe. |
| Statistical learning theory: VC dimension, PAC bounds, generalisation bounds | Named in P14 as claims to read carefully; the bounds are almost always vacuous at realistic scale, and treating them as engineering guidance would be dishonest. | Shalev-Shwartz and Ben-David. |
| Reinforcement learning theory, MDPs, convergence results | P21 and P22 give the gradient estimators and the KL constraint, which is what an engineer touching RLHF actually manipulates. | Sutton and Barto. |
| Category theory, differential geometry, manifolds | Occasionally invoked in interpretability writing; not load-bearing for the work. | Lee, *Introduction to Smooth Manifolds*, if you must. |

Positive pointers for the parts this book does cover but only to working depth:
Strang and Axler for linear algebra; Deisenroth, Faisal and Ong for the same
ground with a machine-learning slant; Blitzstein and Hwang for probability;
Wasserman, *All of Statistics*, for inference; Gelman et al., *BDA3*, for Bayes;
Cover and Thomas for information theory; Nocedal and Wright for numerical
optimisation; Goodfellow, Bengio and Courville, and Murphy, for the machine
learning that consumes all of it.

---

## 14. The Stroud skeleton, made mechanical

Every program, without exception:

1. **Learning outcomes** --- on entry, numbered.
2. **Quiz** --- Foundation programs only. Diagnostic on the way in, exit test on
   the way out. Each question names the frames that cover it, so a wrong answer
   routes the reader rather than merely scoring them.
3. **Frames** --- numbered, small, nearly all demanding a response. **The answer
   appears at the top of the next frame.** The reader is told, in the front
   matter and again at the first frame of F1, to cover the next frame until they
   have written an answer down.
4. **Summary** --- every item tagged with the frame it came from in square
   brackets, so the summary is also a return index. This is the mechanism that
   makes Stroud's method survive a second reading, and it is the thing that
   turns a linear book into a reference --- one of Stroud's stated weaknesses,
   fixed here by taking his own device seriously.
5. **Can you?** --- a checklist **1:1 with the entry outcomes**, self-rated 1--5.
   The 1:1 correspondence is checked by the build; see the ledgers.
6. **Test exercises** --- exactly what the program taught, no traps.
7. **Further problems** --- the large consolidation set.
8. **Answers** --- Appendix A, keyed by program and problem number.

**The scaffolding gradient inside every program**, in this order:
(1) an example worked in full with the author's commentary; (2) an example
worked with gaps the reader fills; (3) "now one for you to do", checked in the
next frame; (4) the end-of-program problems, unassisted.

**Deliberate misconception traps.** At least one per program, elicited before it
sets, in a `warning` box that says flatly that the expected answer is wrong and
then shows why. The model is Stroud's harmonic series: ask whether it converges,
let the reader say yes because the terms shrink, then group the terms and prove
it diverges. A partial catalogue of the traps this book has already identified:

- `(a+b)^2 = a^2 + b^2` [F2]
- a monotone transformation must change the argmax [F5]
- `0.1 + 0.2 == 0.3` [P1]
- more dimensions means more independent directions [P4]
- cosine and Euclidean must rank neighbours the same way [P5]
- a matrix with no zero entries has full rank [P8]
- the determinant tells you whether a matrix is well conditioned [P9, P11]
- a low training loss means the gradient is small [P15]
- reverse-mode autodiff is free [P16]
- a bigger batch is always a better gradient [P21]
- the probability of the evidence given the hypothesis is the probability of the
  hypothesis given the evidence [P23]
- an unbiased estimator is a good estimator [P26]
- p = 0.04 means a 96% chance the effect is real [P27]
- KL divergence is a distance [P30]
- a high mutual-information estimate means the information is there [P31]

---

## 15. Inherited house conventions, and the four places this book must extend them

Inherited unchanged: British English, second person, senior audience, no
marketing register; measurements over assertions; debt counted rather than
remembered; single source of truth in `preamble.tex`; Mermaid diagram pipeline
with committed sources and gitignored renders; 17 cm x 24 cm geometry; the
U+00A0 literate prohibition; the `\IfFileExists` probe before `babel`; any
`\chaptermark` redefinition after `\pagestyle{fancy}`; `\_` inside
`\code{}`/`\api{}`/`\pkg{}`.

Four extensions are needed, and each is flagged as a decision for the author
rather than taken here.

**(a) Mathematics packages.** Neither companion book loads `amsmath`. This one
needs `amsmath`, `amssymb`, `mathtools` and `bm` at minimum, and probably
`siunitx` for units in the cost arithmetic. All must be probed or accepted as
hard requirements, and the choice recorded, because the current preambles
degrade gracefully on a minimal TeX installation and that property is worth
keeping.

**(b) The frame machinery.** New macros, all of which the build can check:
`\frame{n}`, `\answer{...}` (typeset at the head of the following frame),
`\resp` (the row of dots), `\outcomes{}`, `\quiz{}`, `\canyou{}`,
`\summaryitem{...}{frame}`, `\testex{}`, `\further{}`. The answers appendix is
generated from the same source as the problems, so a problem cannot exist
without an answer.

**(c) The admonition vocabulary.** The seven boxes carry over with their
meanings adjusted rather than their names changed --- `warning` becomes the
misconception trap, `versionbox` becomes the convention box (denominator versus
numerator layout, log base, PyTorch versus paper conventions, IEEE-754
particulars), `verifybox` becomes "this number was not produced by a run",
`projectbox` points at the mini-project stage. **One open question: `dotnetbox`
has no obvious job here.** The natural occupant of that slot is a box that
translates a result into NumPy or PyTorch --- "if you already write the code".
Renaming it `codebox` is proposed, and left for the author to accept or reject,
because the vocabulary was declared non-negotiable.

**(d) Bilingual build.** One source tree, `programs/pXX/{en,pl}.tex`, two roots
(`main-en.tex`, `main-pl.tex`), and a translation-drift ledger in CI comparing
frame counts, answer keys and "Can you?" item counts between the two languages.
Fixing Stroud's English-only extras means the Polish edition is not a
second-class citizen: **a program is not done until both languages build.**
Appendix D carries the Polish--English terminology table, following
`llm-book`'s Appendix E, and states plainly where Polish AI usage has not
settled (`embedding`: *zanurzenie* / *osadzenie* / *embedding*).

---

## 16. Debt ledgers

Counted by `make debt` and published to the CI step summary, in the house
pattern. Seven ledgers, of which four are new to this book:

1. **`make stubs`** --- programs not yet written (`\programstub{}`).
2. **`make answers`** --- *new.* Test exercises and Further problems with no
   entry in Appendix A. A mathematics book's most common defect, and it is
   mechanically detectable.
3. **`make frames`** --- *new.* Per-program frame count against the 30--70 band,
   plus a structural check that every frame containing a `\resp` has an
   `\answer` at the head of the next frame. A frame that asks a question nobody
   answers is the method failing silently.
4. **`make canyou`** --- *new.* "Can you?" items that are not 1:1 with the entry
   outcomes. The 1:1 property is the whole point of the checklist.
5. **`make translate`** --- *new.* Programs present in one language and not the
   other, or diverged in frame count.
6. **`make verify`** --- `verifybox` count: numerical claims not produced by a
   script in `code/`.
7. **`make diagrams` / `make shots`** --- as in both companion books.

**And one ledger that is a claim rather than a count.** Stroud's method is
validated to an **80/80 standard** --- at least 80% of students scoring at least
80%. **This book has not been tested on a single reader, and may not claim
80/80 until it has been.** CI prints the validation status as outstanding on
every build, and the front matter says so in plain words. It would be entirely
in character for a book with this house's rules to quietly inherit its
predecessor's validation claim; it must not.

---

## 17. Measurement: what the book will measure rather than assert

The house rule needs an interpretation for a mathematics book, and it is this:
**every number printed in this book is produced by a script in `code/` and
pulled in mechanically, and every claim about behaviour --- not about a theorem
--- is demonstrated by a run.** A theorem is not measured; a theorem is proved
or, where this book declines to prove it, stated as quoted and attributed. The
measurements are for the claims that sit between the mathematics and the
practice, which is exactly where folklore lives.

Ten candidate experiments. Nine of the ten are free and run on a laptop in
under a minute, which is a real advantage over the companion volumes, where
three measurements are still blocked on a provider budget.

**This paragraph used to say “none has been run”, and it had been false for
five programs.** The Status column below names the pass that ran each one
instead, because a count of how many have run is a claim about this book that
nothing derives from anything and that decays silently — which is the failure
mode CLAUDE.md forbids by name and which this ledger demonstrated twice over.
Fill the column in the pass that runs the experiment; never restate a total.

| # | Program | Experiment | Cost | Status |
|---|---|---|---|---|
| E1 | P2 | The logit at which a naive softmax overflows `fp32` and `fp16`, and the error of naive against stabilised, across magnitudes | Free | see the note below |
| E2 | P3 | Hand-counted FLOPs and bytes for one transformer forward pass against measured wall clock; where the model is wrong and by how much | Free (CPU) | not run |
| E3 | P5 | Angle between random unit vectors as dimension goes 2 -> 4096; the concentration towards orthogonality | Free | see the note below |
| E4 | P11 | Singular-value spectrum of a real open-weights embedding matrix; reconstruction error against rank | Free | not run — needs a trained model |
| E5 | P16 | Forward against reverse mode: time and peak memory against depth; the measured cost of gradient checkpointing | Free | see the note below |
| E6 | P20 | SGD, momentum and Adam on a quadratic of known condition number; iterations to tolerance against the predicted count | Free | **run, P20 pass** |
| E7 | P27 | Bootstrap confidence-interval width against evaluation-set size on a public benchmark; the size needed to resolve one point | Free | not run |
| E8 | P30 | Forward against reverse KL fitted to the same bimodal target; mode covering against mode seeking | Free | **run, P30 pass** — see the note |
| E9 | **P25**, then P32 | **The headline.** Logit variance and softmax entropy with and without `1/sqrt(d_k)`, across head sizes | Free | **run: P25 pass on random vectors, P32 pass through the assembly** |
| E10 | P33 | A scaling-law power fit on published numbers, with the fit's extrapolation uncertainty reported | Cheap | **run, P33 pass — split, see the note** |

**E9's owner moved and the table had not.** The curriculum review put the
derivation of the scaling in P25, so E9 as specified — random vectors, head
sizes, spread and entropy — is P25's, and it was run there: without the
division the softmax entropy falls from 0.951 to 0.109 nats against a maximum
of 2.079 and one key of eight takes 95.5 per cent of the weight, while with it
nothing moves at any head size. What was left for P32 was the same measurement
on an assembled architecture rather than on random vectors, and P25's own
closing frames said so.

**P32 ran that half, and it needed no sampling at all.** Through a block the
score is $q \cdot k = (W_Q^{\mathsf T} x) \cdot (W_K^{\mathsf T} y)
= x^{\mathsf T} M y$ with $M = W_Q W_K^{\mathsf T}$, and for independent
standard-normal inputs that bilinear form has variance **exactly**
$\lVert M \rVert_F^2$ — so one weight draw settles the whole question in
closed form, and $\mathbb{E}\lVert M\rVert_F^2 = d_k$ exactly. Measured at
`d_model = 64` the spreads are 2.86, 3.96, 5.63 and 8.02 against
`sqrt(d_k)`, gated against P25's own committed 2.83 and 7.99. What the closed
form also shows, and P25's method could not, is that a **trained model has one
weight draw rather than an average**, so its own scores sit a few per cent off
the nominal before training starts. The remaining half — whether the
independence the derivation assumes survives training — still needs a trained
model and is stated as outstanding.

**E10 was run in the P33 pass, and P32's question split it.** The
specification says “on published numbers”, and the P32 pass established the
habit of asking whether a claim needs external data or is a statement about
the object itself. Here the half that carries the argument needs nothing
external: **how far a power-law fit can be trusted past its last point is a
property of the fit and of the span**, and it is exactly computable when the
truth is known, because the script chose it. So the truth is the form the
literature itself uses — an irreducible loss plus a power law — and a *pure*
power law is fitted to it, which is what everybody fits. Over three decades
the fit misses by half of one per cent; three decades further out it is six
per cent wrong, the truth lies **outside** its own two-standard-error band,
and about six decades past the last measured point the fitted line predicts a
loss below the irreducible floor. What a published paper would add is one
specific exponent, and the frames say so rather than pretending the general
claim needs it.

**E8 was run in the P30 pass and nobody had claimed it**, which is the fifth
instance of exactly the decay this Status column exists to stop.
`code/p30_cross_entropy_kl.py` fits forward and reverse KL to the same bimodal
targets and reports mode covering against mode seeking, which is the
specification. It differs from the wording in one way and the difference is an
improvement rather than a shortfall: it **enumerates** a finite candidate
family and evaluates every member, so the answer is a proof over that family,
where an optimiser's answer would have depended on where the search started
and stopped. P30's pass note gives that reasoning in full; it simply never
came back to the table.

**Three rows say “see the note below” because nobody has checked them, and
that is the honest answer.** P02 measured the overflow cliff per format and
the cost of a non-maximal pivot; P05 swept the cosine spread over
`d = 2, 3, 10, 100, 768, 4096` and the concentration towards orthogonality;
P16 counted forward against reverse multiplications exactly and derived the
checkpointing peak. Each looks like the experiment beside it and **no pass
claimed one**, so whether the specification is met is a reading job on three
merged programs and not an inference to make from this table. E5 is the
clearest case for “no”: it asks for time and peak memory measured on a
machine, and P16 deliberately counted operations instead.

Until an experiment runs, the claim it supports is labelled as judgement and its
table stays empty. **Do not fill them with plausible numbers.**

---

## 18. The mini-project

The companion volumes each build one system across their length. This one builds
**`odzera`** --- a small, dependency-light numerical library and the training run
that exercises it --- one stage per part.

| Stage | Part | Adds |
|---|---|---|
| 00 | II | Float utilities, stable `logsumexp`, Welford variance, and a numerical-error test suite |
| 01 | III | A minimal linear-algebra layer; PCA and truncated SVD on a real embedding matrix |
| 02 | IV | The computation graph: a DAG of operations and its topological order |
| 03 | V | Reverse-mode autodiff over that DAG, with every gradient checked against finite differences |
| 04 | VI | SGD, momentum, Adam, AdamW; the ill-conditioned quadratic benchmark from E6 |
| 05 | VII | Samplers, the categorical/Gumbel path, and a bootstrap confidence-interval tool |
| 06 | VIII | Cross-entropy, perplexity, and forward/reverse KL diagnostics |
| 07 | IX | A transformer block assembled from stages 00--06 and trained on a toy corpus; the evaluation harness with confidence intervals |

**The rule that keeps it honest**, in the house pattern: **every gradient in the
project is checked against a finite-difference reference in CI, no stage needs a
GPU, and the whole suite runs in under a minute on a laptop.** A stage that
needs a cluster to demonstrate anything has been designed wrong. The second
rule: **every number printed in the book comes from this repository**, so the
book and the code cannot drift --- the same discipline `llm-book` enforces with
`\pyregion{}`.

---

## 19. Front matter and appendices

Front matter: title page; **How to use this book** (the cover-the-next-frame
instruction, the recommended loop, and the honest statement that the 80/80
validation has not been done); **How to read a formula** (the symbol table, so
that a reader who has never seen sigma is not blocked in F4); the scope
statement from section 13.

The recommended loop, stated once and repeated at the head of every program:

> read the outcomes -> take the Quiz -> work the program -> "Can you?" ->
> **retake the Quiz** -> Test exercises -> Further problems

Appendices:

| | Title (EN) | Tytuł (PL) | Purpose |
|---|---|---|---|
| A | Answers | Odpowiedzi | Every Test exercise and Further problem. Generated from the same source as the problems. |
| B | Notation and symbols | Notacja i symbole | The reference the front matter's "How to read a formula" points back to. |
| C | Formula reference | Wzory | **Fixes Stroud's "useless as a reference".** Every result in the book, one line each, tagged with its program and frame. |
| D | Polish--English terminology | Słownik terminów | Following `llm-book` Appendix E; states where Polish usage has not settled. |
| E | Where to go next | Co dalej | Section 13's table, expanded, with what each source is good for and what it is bad for. |
| F | Manifest | Wykaz | Diagrams, measurements and the outstanding-work ledgers, printed. |

---

## 20. Open questions for the author

1. **One volume or two — still open, and the estimate it rested on is now
   measured and was wrong by a factor of about three.** The figure recorded
   here was 460--540 pages for ~2,418 frames, which is 0.21 pages a frame.
   **Measured, September 2026: 1,863 teaching frames set 1,401 pages in the
   trade format**, which is 0.75 — and **that is now the finished book**, with
   every program and every appendix written. (It was 1,757 frames in 1,267
   pages when first taken, before P33, 1,811 in 1,295 after it, 1,321 before
   Appendix C, 1,383 before Appendix D, 1,387 before Appendix E and 1,393
   before Appendix F. The programs' own 1,212 pages account for the ratio; the
   back matter grew from 109 pages to 185, and Appendix C alone is 62 of that,
   with D adding four, E six and F four.) **Nothing here moves except by
   revision**, and the Part II elicitation pass is the first revision to move
   it: four pages, all of them inside Parts II--VI where P1 to P3 live, with
   the other three rows unchanged. This is the number the decision has to be
   made against.

   The estimate is not mysteriously wrong. It was made before the Stroud layout
   pass existed, so a *frame* in it was a paragraph. A frame as built is a rule
   across the measure, a margin badge, 17 pt above and 12 pt below, usually an
   answer box, often a row of dots and a cue — and each program also carries a
   Quiz, an outcomes panel, figures, transcripts, a Summary, Test exercises and
   Further problems, with an answers appendix and a six-page index behind them
   all.

   Measured from the trade build's own part-title pages, so the split can be
   priced rather than guessed:

   | | pages | count |
   |---|---|---|
   | front matter + Part I (F1--F13) | 1--388 | 388 |
   | Parts II--VI (P1--P22) | 389--886 | 498 |
   | Parts VII--IX (P23--P34) | 887--1216 | 330 |
   | back matter (appendices, answers, index) | 1217--1401 | 185 |

   These are **PDF pages**, not printed folios, and the difference is
   twenty-eight — the front matter. `main-en.toc` gives folios, so it puts
   Part II at 361 against this table's 389, and reading one against the other
   invites a twenty-eight page false alarm that four paragraphs cannot explain.
   Each boundary above was confirmed by extracting the page and reading its
   part title rather than by adding twenty-eight to the toc, which is this
   entry's own rule about arithmetic on two measurements.

   So the proposed cut gives an 886-page first volume before any back matter,
   which does not settle it: at this geometry the book is nearer three volumes
   than two, or the geometry has to change. **Decide before the front matter is
   written**, and decide against these numbers rather than against the
   estimate.

   The third row is a correction as well as an update. It previously read
   `883--1295` and was labelled "Parts VII--IX as written + back matter",
   which is 1295 minus the two rows above it — a subtraction rather than a
   measurement, and it was not obvious from the table what it excluded. Read
   off the part-title pages the four rows add to the total exactly. The
   first-volume figure never depended on it.
2. **`dotnetbox` or `codebox`** --- section 15(c).
3. **Whether the mathematics packages may be hard requirements**, breaking the
   graceful degradation both companion preambles maintain --- section 15(a).
4. **Whether P12 (combinatorics) stays in Part IV or opens Part VII ---
   DECIDED, August 2026: it stays, and on a different argument from the one
   recorded here.** The question was numbered `P11` above, from before `P7` was
   inserted, and was restated correctly in §21.

   **One of the two arguments for leaving it is now falsified by the written
   book.** "P11 also feeds P3" is not true: `P03` is written and merged and
   needed nothing from combinatorics, because `F10` supplied every count it
   used. Nor does `P13` declare it --- the manifest has `P13 <- F10, P6, P10`.
   So *nothing in Part IV depends on P12*, and the case for leaving it where it
   is cannot rest on the dependency graph.

   What it rests on instead is stronger. **P12's own three payoffs are counting
   payoffs, not probability ones**: sizing a hash for deduplication, the size of
   a beam search's space, and the exponential cost of an exact Shapley value.
   Only the birthday calculation touches probability at all, and it needs
   nothing beyond `F10`'s two-counts-and-a-division. Moving the program to
   Part VII would present it as a prerequisite for probability when its own
   results are not probabilistic --- and would leave Part IV, *Discrete
   structures and argument*, with two programs and no counting in it.

   The cost of the decision is the gap, and it is paid inside the program
   rather than left: `P12` §4 restates the pair count where it uses it, so a
   reader arriving at `P23` ten programs later does not have to have retained
   it. Reversing the decision is a renumbering of ten stub programs and their
   issues, so whoever reverses it should have a better reason than the one this
   entry used to give.
5. **Whether P14 (logic and proof) is enough of a fix for Stroud's rigour gap,
   or whether the book should carry a second, later program on writing a proof.**
   The current position is that this audience needs to read theorems and does
   not need to write them, and that position should be stated in the front
   matter rather than left implicit.


---

## 21. Addendum — changes forced by the adversarial review, August 2026

This document was rejected as it stood, and five findings are now in
`tools/programs.json` rather than here. Recorded so the design and the manifest
do not disagree.

1. **P7, *Tensors, shapes and index notation*, was missing** and is the largest
   content gap in the book — and in every book in §1. Inserted between P6 and
   the old P7; everything after it moved up one, so the book is now 47
   programs and roughly 2,415 frames.
2. **F13 was curriculum inertia.** Forty-five frames on the integral in a book
   whose §13 excludes every integration technique by name. Cut to twenty and
   retitled *Accumulation, area and expectation*.
3. **P3 asked for a transformer parameter count** three parts before any
   program had said what a matrix is. That count moved to P32.
4. **Initialisation was missing entirely** — no variance propagation, no fan-in
   argument, no He or Xavier — and a training run that diverges at step zero is
   the commonest failure the audience meets. Added to P25.
5. **§3's Part I contract was false.** *Assumes genuinely nothing* is
   contradicted by every Foundation payoff sentence in this document. The two
   floors are now separated in the front matter: no mathematics beyond school
   arithmetic, but the vocabulary of the job assumed throughout.

**And §16's 80/80 obligation was unmeasurable as written.** §14 puts the Quiz on
Foundation programs only, so the standard could not be measured on 34 of the 47
and was contaminated on the other 13, the same items serving as entry and exit
test. The instrument is the scored Test exercises, which every program has.

Three further findings are recorded and **not** acted on, because they are
judgement calls for the author rather than defects:

- whether P12 (combinatorics) should move next to the probability that consumes
  it — §20 already had this open;
- whether the book is one volume or two;
- whether P14 (logic and proof) is enough of a fix for Stroud's rigour gap, or
  whether a second, later program on writing a proof is wanted.
  **DECIDED, August 2026, in the pass that wrote P14: it is enough, and no
  second program is wanted.** Two things settled it, and neither was available
  when the question was posed.

  The first is that P14 is written and it turns out that *reading* a theorem is
  a complete subject rather than a reduced one: the three parts, the four rows
  of the implication table, quantifier order, three proof shapes and where each
  one fails, and three worked misquotations. Nothing in it is a shortened
  version of a proof-writing course, so a second program would not be
  finishing this one, it would be a different book — which is exactly what
  P14's own rigour box says the third option was.

  The second is that the position is now **on the page in two places rather
  than implicit in neither**. P14 §1 states the three options and takes the
  third, and the introduction now says what the reader gets instead of
  proof-writing, where before it named only what they would not get. The
  issue's requirement was that the position not be left implicit; it is not.

  What the book still does not have, and this is the honest residue: nobody has
  read P14, so the claim that reading is the skill this audience needs is
  argued rather than measured — like every other pedagogical claim here, and it
  sits under the same 80/80 ledger.
