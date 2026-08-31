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
(P1--P33)**.

| Part | Programs | Why it exists |
|---|---|---|
| I --- Podstawy / Foundation | F1--F13 | Assumes nothing. Triaged by Quiz; a competent reader skips most of it in an afternoon. |
| II --- Liczba, precyzja i koszt / Number, precision and cost | P1--P3 | What the machine actually computes, and what an operation costs. Placed first because everything after it is arithmetic on a finite machine. |
| III --- Algebra liniowa / Linear algebra | P4--P10 | Stroud's largest gap. Seven programs, because this is the subject the audience uses daily and understands least. |
| IV --- Struktury dyskretne i argumentacja / Discrete structures and argument | P11--P13 | Counting, graphs, and how to read a theorem without believing more than it says. Placed before calculus so that "DAG" and "for all epsilon" are defined when they are first needed. |
| V --- Rachunek różniczkowy i różniczkowanie automatyczne / Calculus and automatic differentiation | P14--P17 | The chain rule, taken all the way to what `loss.backward()` actually does. |
| VI --- Optymalizacja / Optimisation | P18--P21 | Absent from Stroud's first volume entirely. |
| VII --- Prawdopodobieństwo i statystyka / Probability and statistics | P22--P27 | Stroud stops at the normal distribution. This part goes to inference, bootstrap and Bayes, because the audience's real job is deciding whether a measured difference is real. |
| VIII --- Teoria informacji / Information theory | P28--P30 | Absent from Stroud. It is where the loss function comes from. |
| IX --- Złożenie / Assembling it | P31--P33 | Three capstone programs that spend the whole book on one architecture, one training run and one evaluation. No new mathematics. |

Estimated **2,370 frames**, roughly 460--540 pages at this page geometry. That
is a two-volume book if it is printed; Parts I--VI and Parts VII--IX split
cleanly, and the split is worth deciding early because it changes the front
matter. Recorded here as an open question, not a decision.

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

**P1 --- Floating point: what the machine actually computes**
(*Liczby zmiennoprzecinkowe: co maszyna naprawdę liczy*) --- 45 frames.

Argument: a float is a sign, an exponent and a fixed number of significant bits,
so the gap between representable numbers grows with magnitude, and equality is
not a question you should ask.

Payoff: why `bf16` is the training format and `fp16` needs loss scaling --- they
have the same width and different exponent budgets, and the reader computes the
overflow threshold rather than being told it; why a sum of gradients is not
associative and two GPUs therefore disagree in the last bits; what machine
epsilon is and why comparing two loss values that differ in the eighth decimal
is measuring the hardware.

**P2 --- Numerical error, stability and computing in log-space**
(*Błąd numeryczny, stabilność i obliczenia w skali logarytmicznej*) --- 50 frames.

Argument: an algorithm can be correct in exact arithmetic and useless in
floating point; catastrophic cancellation is the mechanism, and there is a small
catalogue of fixes.

Payoff: **why log-sum-exp instead of exponentiating.** The reader computes the
exact logit at which a naive softmax overflows `fp32` and `fp16`, then derives
the max-subtraction trick and shows it changes nothing mathematically. Also: why
cross-entropy is computed from logits and never from probabilities; why the
naive one-pass variance formula gives a negative variance and Welford's does
not; why summing a million small gradients in the wrong order loses them.

**P3 --- Orders of magnitude: O-notation, FLOPs and memory**
(*Rzędy wielkości: notacja O, FLOP-y i pamięć*) --- 45 frames.

Argument: asymptotic notation is a statement about growth and says nothing about
which of two implementations is faster today; both facts matter.

Payoff: count the parameters of a transformer block by hand; count the
activations; count the KV cache and watch it grow linearly in sequence length
while attention grows quadratically --- **the reader derives why long context is
expensive rather than accepting it**. Arithmetic intensity, and why a large
matrix multiply is compute-bound while an elementwise operation is
memory-bound, which is the whole justification for kernel fusion.

---

## 5. Part III --- Algebra liniowa / Linear algebra (P4--P10)

Seven programs. Stroud teaches matrices as a set of recipes --- determinants by
cofactor expansion, an inverse by adjugate, eigenvalues by solving a
characteristic polynomial --- and never mentions a vector space. That is exactly
backwards for this audience: the recipes are what a library does for you, and
the structural facts are what you need to read a model architecture.

**P4 --- Vectors, vector spaces and basis**
(*Wektory, przestrzenie liniowe i baza*) --- 55 frames.

Argument: a vector space is closed under two operations; span, linear
independence, basis and dimension are four words for one idea, and dimension is
the number of independent directions rather than the length of the list.

Payoff: what "embedding dimension 4096" does and does not promise; why a set of
20,000 token embeddings in 4,096 dimensions cannot be linearly independent, and
why the linear-representation and superposition stories are therefore
*hypotheses about structure*, stated here as hypotheses and not as facts.

**P5 --- Inner product, norms and projection**
(*Iloczyn skalarny, normy i rzutowanie*) --- 60 frames.

Argument: an inner product is the only thing that gives a vector space angles
and lengths; a projection is the closest point in a subspace; different norms
measure different things and disagree about which vector is bigger.

Payoff: dot product, cosine and Euclidean distance compared on the same data,
with the case where they rank differently worked out --- the thing a vector
database forces you to choose and nobody explains; why normalising embeddings
makes cosine and dot product the same query and what you lose; L1 against L2 as
a shape rather than a slogan, and why the L1 ball's corners are the whole of the
sparsity argument. Also the fact the book cashes in twice later: **in high
dimension, two random vectors are almost always nearly orthogonal**, measured
rather than asserted.

**P6 --- Matrices as linear maps** (*Macierze jako przekształcenia liniowe*) --- 60 frames.

Argument: a matrix is a function that respects addition and scaling; matrix
multiplication is composition of functions, which is why it is associative and
not commutative; shape is the type signature.

Payoff: a linear layer is a matrix and a batch is one extra index; **two linear
layers with no non-linearity between them are one linear layer**, derived, which
is the reason activations exist; every shape error the reader has ever hit,
explained as a type error in a composition; multi-head attention as a reshape,
which is where most readers' mental model breaks.

**P7 --- Rank, the four subspaces and least squares**
(*Rząd, podprzestrzenie i najmniejsze kwadraty*) --- 60 frames.

Argument: a matrix has a column space, a row space and two null spaces; rank is
the dimension shared by the first two and it is the honest measure of how much a
matrix does.

Payoff: **LoRA is a rank constraint**, and this is the program that makes that
sentence carry information --- a `d x d` update replaced by `B A` with inner
dimension `r`, parameter count `2dr` against `d^2`, and the assumption being
made about the update stated plainly. Solving `Ax = b` when there is no
solution: least squares as a projection, which is linear regression's closed
form. Rank collapse in deep attention stacks, described as the phenomenon it is.

**P8 --- Determinant, inverse and change of basis**
(*Wyznacznik, macierz odwrotna i zmiana bazy*) --- 45 frames.

Argument: the determinant is a signed volume scale factor and zero means
information was destroyed; an inverse exists exactly when nothing was destroyed;
a change of basis is the same vector described in another coordinate system.

Payoff: why production code almost never calls `inv()` and solves a factorised
system instead --- stated here, measured in P10; a rotation as an
orthogonal change of basis, which is what rotary position embedding does; the
log-determinant term in a normalising flow, named so the reader recognises it
later without the book promising to teach flows.

**P9 --- Eigenvalues, quadratic forms and positive definiteness**
(*Wartości własne, formy kwadratowe i dodatnia określoność*) --- 65 frames.

Argument: an eigenvector is a direction the matrix only stretches; a symmetric
matrix has a full orthogonal set of them (the spectral theorem, stated and used,
not proved); a quadratic form is a bowl, a saddle or a ridge, and its eigenvalues
say which.

Payoff: a covariance matrix is symmetric and positive semi-definite, so PCA is
an eigen-decomposition and not a black box; the spectral norm as the largest
stretch, which is the Lipschitz constant that bounds how much a layer can
amplify; **the Hessian's eigenvalues are the shape of the loss basin**, which is
where "ravine", "sharp minimum" and "the learning rate is too high" all become
one statement --- collected here and spent in P16 and P19.

**P10 --- SVD, low-rank approximation and conditioning**
(*Rozkład SVD, aproksymacja niskiego rzędu i uwarunkowanie*) --- 60 frames.

Argument: every matrix, square or not, factors into rotate--stretch--rotate.
Truncating the stretch gives the provably best approximation of a given rank
(Eckart--Young, stated). The ratio of largest to smallest singular value is the
condition number, and it is the amplification factor from input error to output
error.

Payoff: the singular-value spectrum of a real embedding matrix, plotted, showing
how few directions carry the energy --- the empirical case for LoRA and for
embedding compression, measured; the pseudoinverse as least squares done
properly; **why the normal equations square the condition number and a QR
solve does not**, which is the concrete form of "do not invert"; and the
condition number as the number that predicts how many iterations an optimiser
will need, handed forward to P19.

---

## 6. Part IV --- Struktury dyskretne i argumentacja / Discrete structures and argument (P11--P13)

Three programs, placed here rather than at the end. The placement is the
argument: a computation graph is a DAG and reverse-mode differentiation is a
reverse topological traversal, so the reader should have met a DAG *before* P15
rather than after it. Logic and proof come before the calculus and probability
parts for the same reason --- the reader is about to start meeting statements of
the form "for every epsilon there exists an N", and being able to parse one is a
prerequisite, not a capstone.

**P11 --- Combinatorics and counting** (*Kombinatoryka i zliczanie*) --- 45 frames.

Argument: four counting rules --- product, permutation, combination,
inclusion--exclusion --- plus the pigeonhole principle and simple recurrences.

Payoff: the birthday calculation, so the reader can size a hash for dataset
deduplication and say why 64 bits is not enough and 128 is; the size of a beam
search's space and why beam width buys so little; **a Shapley value is an
average over every ordering of the features**, so exact SHAP is exponential by
construction and every implementation you have used is a sampling
approximation --- which changes how much you should trust an attribution plot.

**P12 --- Graphs, DAGs and random walks**
(*Grafy, DAG-i i błądzenie losowe*) --- 50 frames.

Argument: a graph is a set plus a relation; adjacency matrix and adjacency list
are two encodings with different costs; a DAG has a topological order and that
order is what makes evaluation well defined.

Payoff: the computation graph, defined properly, one program before autodiff
needs it; **message passing in a graph neural network is a multiplication by
the adjacency matrix**, which is where Part III and this part meet; PageRank as
the stationary distribution of a random walk, which is the same eigenvector
calculation as P9; an agent workflow, a build system and a neural network as the
same object.

**P13 --- Logic, proof and reading theorems**
(*Logika, dowód i czytanie twierdzeń*) --- 45 frames.

Argument: implication is not equivalence, a quantifier's order changes the
claim, and a proof by induction or contradiction is a shape you can recognise.

Payoff: **the reader can read a paper's theorem and separate its hypotheses from
its conclusion.** Worked on real examples of the gap: a convergence result that
assumes convexity being cited about a neural network; a bound that holds "with
high probability over the draw of the data" quoted as if it held for the dataset
in hand; "universal approximation" quoted as if it said anything about
learnability. This program is the honest, bounded fix for Stroud's absent
rigour: it does not train the reader to *write* proofs, and says so.

---

## 7. Part V --- Rachunek różniczkowy i różniczkowanie automatyczne / Calculus and automatic differentiation (P14--P17)

**P14 --- Functions of several variables and the gradient**
(*Funkcje wielu zmiennych i gradient*) --- 55 frames.

Argument: a partial derivative holds everything else still; the gradient
collects them; the directional derivative is a dot product with the gradient, so
the gradient is the steepest direction and is perpendicular to the level set.

Payoff: gradient descent's direction is derived rather than asserted; **the
zig-zag in a narrow valley is explained by the gradient being perpendicular to
the contour rather than pointing at the minimum**, which is the picture that
makes momentum obvious two parts later.

**P15 --- Jacobians, the chain rule and automatic differentiation**
(*Jakobian, reguła łańcuchowa i różniczkowanie automatyczne*) --- 65 frames.

Argument: for vector-valued functions the chain rule multiplies Jacobians;
nobody forms a Jacobian; forward mode computes a Jacobian--vector product and
reverse mode a vector--Jacobian product, and which is cheaper depends only on
the shape of the problem.

Payoff: **what `loss.backward()` actually computes**, in full: why a scalar loss
with many parameters makes reverse mode cheaper by a factor of the parameter
count; why reverse mode must keep the activations, so memory scales with depth
and batch; gradient checkpointing as an explicit trade of recomputation for
memory, with the arithmetic done; why a numerical finite-difference gradient is
a testing tool and not an implementation; the three places autodiff silently
gives you something other than the derivative you meant (a non-differentiable
point, a detached tensor, an in-place write).

**P16 --- The Hessian, curvature and the Taylor expansion**
(*Hesjan, krzywizna i rozwinięcie Taylora*) --- 50 frames.

Argument: the second-order Taylor expansion is the best local quadratic model,
and its matrix is the Hessian.

Payoff: **why the largest stable learning rate is bounded by the inverse of the
curvature**, derived on a quadratic, which turns "the loss exploded" into an
arithmetic statement; the condition number of the Hessian as the ratio of
fastest to slowest direction, joining P9 and P10 to the optimiser; second-order
methods explained and then dismissed on cost for this problem size; and an
honest section on sharp-versus-flat minima --- what is measured, what is
reparameterisation-dependent, and why the claim is contested.

**P17 --- Matrix calculus** (*Rachunek macierzowy*) --- 60 frames.

Argument: differentiating with respect to a vector or a matrix is bookkeeping
plus a layout convention, and most of the pain in the literature is the
convention rather than the mathematics.

Payoff: the identities the reader actually needs, derived once each: the
gradient of `Wx` with respect to `W`; of a squared error; of a softmax; of a
log-softmax; of layer normalisation. The headline: **the gradient of
cross-entropy through a softmax is `p - y`**, the single most reused fact in
applied machine learning, derived in full --- and the reason the two operations
are fused in every serious implementation. Also a versionbox on numerator versus
denominator layout, because the reader will meet both in the same week.

---

## 8. Part VI --- Optymalizacja / Optimisation (P18--P21)

Stroud has no optimisation in the first volume at all. For this audience it is
the subject the job actually consists of.

**P18 --- Convexity and Jensen's inequality**
(*Wypukłość i nierówność Jensena*) --- 45 frames.

Argument: a convex function has one basin and every local minimum is global;
that is a promise about the problem, not about the algorithm. Deep learning
breaks the promise, and what survives anyway is worth naming precisely.

Payoff: Jensen's inequality, and **why you cannot average perplexities** ---
the mean of the exponentials is not the exponential of the mean, so a
leaderboard that averages per-document perplexity is reporting a different
quantity from one that exponentiates the mean loss; the same inequality is the
ELBO in one line, named for recognition; and the honest statement that
"non-convex" does not mean "hopeless", with the reasons.

**P19 --- Gradient descent: from SGD to Adam**
(*Metoda gradientu prostego: od SGD do Adama*) --- 65 frames.

Argument: every optimiser in common use is the same update with a different
estimate of "how far and in which direction", and each addition fixes a specific
named failure of the one before it.

Payoff: the step-size bound from P16; momentum as the exponential moving average
met in F4, fixing the zig-zag from P14; per-coordinate scaling fixing badly
scaled features; **why Adam divides by the square root of the second moment ---
it is a per-coordinate estimate of the gradient's scale, so the update becomes
approximately unit-sized regardless of how large the gradient is**, which is
also precisely why Adam is insensitive to loss scaling and why the epsilon must
sit outside the square root; bias correction derived from the initialisation at
zero; **weight decay is not L2 regularisation once you divide by a running
scale**, which is the entire content of AdamW; warmup and cosine schedules
described as what they do to the effective step rather than as ritual.

**P20 --- Stochastic optimisation and differentiating through randomness**
(*Optymalizacja stochastyczna i różniczkowanie losowania*) --- 50 frames.

Argument: a minibatch gradient is an unbiased estimator with variance
proportional to `1/B`, and the noise is a property of the algorithm rather than
a defect in it.

Payoff: why the loss curve is noisy and what a moving average of it hides; the
linear scaling rule for batch size and learning rate, presented as **widely
repeated folklore with a limited empirical basis**, not as a law; gradient
clipping as a bound on the update rather than on the gradient; and the two ways
to get a gradient through a sampling step --- the score-function estimator
(REINFORCE, unbiased and high variance) and the reparameterisation trick
(low variance, requires a differentiable path) --- which is the fork that
separates policy-gradient RLHF from a VAE.

**P21 --- Constrained optimisation and Lagrange multipliers**
(*Optymalizacja z ograniczeniami i mnożniki Lagrange'a*) --- 50 frames.

Argument: at a constrained optimum the gradients of objective and constraint are
parallel; the multiplier is the exchange rate between them.

Payoff: **a Lagrange multiplier is a price** --- how much objective you buy per
unit of constraint relaxed --- and that reading turns the `beta` in a
KL-penalised objective from a tuning knob into a quantity with units; the
equivalence between a hard KL constraint and a KL penalty, which is why PPO and
DPO are talking about the same problem; projection onto a set as the other way
to enforce a constraint; KKT conditions stated for recognition, with the
inequality case sketched rather than developed.

---

## 9. Part VII --- Prawdopodobieństwo i statystyka / Probability and statistics (P22--P27)

Stroud's statistics is descriptive plus the normal distribution: no estimation,
no inference, no Bayes. That is the difference between describing a sample and
deciding whether a difference is real, and deciding whether a difference is real
is what this audience is paid for.

**P22 --- Probability and Bayes' theorem**
(*Prawdopodobieństwo i twierdzenie Bayesa*) --- 55 frames.

Argument: probability is a measure on a sample space obeying three rules;
conditioning is restricting the space; Bayes' theorem is one line of algebra
from the definition and is derived, never asserted.

Payoff: **the base-rate calculation an engineer must be able to do in a
meeting** --- a classifier with 99% accuracy on a fault that occurs once in a
thousand requests, and what fraction of its alarms are real. Independence and
conditional independence distinguished, because the naive Bayes assumption and
most "these two evals are independent signals" claims live on the difference.
Trap: the prosecutor's fallacy, elicited from the reader before it is named.

**P23 --- Random variables and distributions**
(*Zmienne losowe i rozkłady*) --- 60 frames.

Argument: a random variable is a function on the sample space; expectation and
variance are its first two summaries; six distributions cover almost everything
in this field.

Payoff: **sampling a token is a draw from a categorical distribution**, and
temperature, top-k and top-p are three ways of editing that distribution before
drawing --- described as distribution surgery, with what each destroys; the
Gumbel-max trick, so the reader can see that `argmax(logits + gumbel)` is exact
categorical sampling and not an approximation; the Gaussian introduced through
its role rather than its formula; expectation as the linear operator that makes
almost every derivation later in the book short.

**P24 --- Sums of random variables: the central limit theorem, concentration and Monte Carlo**
(*Sumy zmiennych losowych: centralne twierdzenie graniczne i metoda Monte Carlo*) --- 55 frames.

Argument: variances of independent quantities add; averages concentrate; the
error of an average falls as `1/sqrt(n)` and that single rate governs an
astonishing amount of practice.

Payoff: **the derivation of the `1/sqrt(d_k)` in attention.** A dot product of
two `d_k`-dimensional vectors with independent unit-variance entries has
variance `d_k`, so its standard deviation grows as `sqrt(d_k)`; feed that into a
softmax and it saturates, and the gradient dies; divide by `sqrt(d_k)` and the
logits have unit variance regardless of head size. The scaling is a variance
correction and nothing else, and the reader derives it here and measures it in
P31. Also: Monte Carlo error is the same `1/sqrt(n)`, so the number of samples
needed to halve an error bar is four times as many --- the fact that prices
every evaluation run in the book.

**P25 --- Estimation and maximum likelihood**
(*Estymacja i metoda największej wiarogodności*) --- 55 frames.

Argument: an estimator is a function of the sample; bias and variance are two
different ways of being wrong; maximum likelihood picks the parameter that makes
the observed data least surprising.

Payoff: **training a language model is maximum likelihood**, and the
cross-entropy loss is the negative log-likelihood of the observed tokens ---
one derivation that reframes the entire training objective, and from which label
smoothing, class weighting and the `n-1` in a sample variance all fall out. MAP
as maximum likelihood with a prior, which is exactly weight decay with a
Gaussian prior --- the cleanest available statement of what regularisation *is*.

**P26 --- Statistical inference for the engineer**
(*Wnioskowanie statystyczne dla inżyniera*) --- 60 frames.

Argument: a measured difference is a random quantity, and the question is
whether it is larger than the noise in the measurement.

Payoff: the program that carries this house's first rule into a mathematics
book. **"Model B scored 71.4 and model A scored 70.9 on 200 evaluation items"
--- is that real?** Worked end to end: the standard error of a proportion; a
bootstrap confidence interval on an evaluation set; the paired comparison,
because A and B saw the same prompts and a paired test has far more statistical power;
what a p-value does and does not say, stated flatly; the multiple-comparisons
problem, which is what a leaderboard with forty models is; and a power
calculation answering how many evaluation items are needed to detect a
one-point difference at all. The honest conclusion --- that most published
leaderboard deltas of this size are not distinguishable from noise, and the
reader can now check.

**P27 --- Bayesian inference** (*Wnioskowanie bayesowskie*) --- 50 frames.

Argument: put a distribution on the parameter, condition on the data, report the
posterior. Conjugacy makes the arithmetic closed-form in the one case that
matters most.

Payoff: Beta--Binomial worked fully, which covers "what is this model's success
rate and how sure am I"; a credible interval and a confidence interval
contrasted, because they answer different questions and are routinely conflated;
Bayesian A/B testing on evaluation results, giving "the probability that B is
better" which is the quantity people wanted from a p-value; Thompson sampling
as model routing under uncertainty; calibration of a judge model's stated
probability, and what it costs downstream when the judge is confidently wrong.

---

## 10. Part VIII --- Teoria informacji / Information theory (P28--P30)

Entirely absent from Stroud. It is where the loss function comes from, so it
cannot be absent here.

**P28 --- Entropy and the measure of surprise**
(*Entropia i miara zaskoczenia*) --- 45 frames.

Argument: surprise is the negative log of a probability; entropy is average
surprise; it is the shortest average code length, and that is why the units are
bits.

Payoff: **perplexity is the exponential of the cross-entropy, and it is the
effective number of equally likely choices at each step** --- so a perplexity of
7 is a concrete statement about a model and not a leaderboard number; entropy of
the next-token distribution as a usable runtime signal for when a model is
guessing; the entropy of a tokeniser's output as a bound on how much a
compression-style argument can claim.

**P29 --- Cross-entropy and the Kullback--Leibler divergence**
(*Entropia krzyżowa i dywergencja Kullbacka--Leiblera*) --- 55 frames.

Argument: cross-entropy is the cost of coding one distribution with another's
code; KL is the excess; it is non-negative, zero only when the distributions
agree, **and it is not symmetric**.

Payoff: the question the brief asks for --- **what the asymmetry costs you when
you pick a loss.** Forward KL is mode-covering: it pays an unbounded price for
putting no mass where the target has some, so it spreads. Reverse KL is
mode-seeking: it pays for putting mass where the target has none, so it
collapses onto one mode. Distillation minimises one, a variational objective and
a KL-regularised policy the other, and the difference is visible in the output.
Measured on a bimodal target, not asserted. Also: "KL distance" is a misnomer
and the triangle inequality fails; Jensen--Shannon as the symmetric alternative
and what it costs; and the observation that minimising cross-entropy against a
fixed dataset is minimising forward KL to the empirical distribution, which
closes the loop with P25.

**P30 --- Mutual information** (*Informacja wzajemna*) --- 50 frames.

Argument: mutual information is the reduction in uncertainty about one quantity
given another; it is symmetric, non-negative, and zero exactly under
independence.

Payoff: the vocabulary behind a large class of claims the reader will meet ---
"layer 12 contains information about syntax", "this feature is informative about
the label" --- together with the reason to discount most of them:
**mutual information in high dimension is extremely hard to estimate, and the
common estimators are biased in the direction that flatters the claim.** The
data-processing inequality, which says post-processing cannot create
information, and is the clean argument against several popular interpretability
claims. A folklore-puncturing program by design.

---

## 11. Part IX --- Złożenie / Assembling it (P31--P33)

Three capstone programs. **No new mathematics.** Everything is a withdrawal from
an account opened earlier, and each frame that uses a result names the program
it came from. This is the part that makes the book's promise concrete, and it is
the analogue of the capstone chapter in both companion volumes.

**P31 --- The transformer, derived** (*Transformer wyprowadzony od podstaw*) --- 70 frames.

The whole book spent on one architecture. Embeddings as vectors in a space
[P4]; the query--key dot product as an inner product and its high-dimensional
behaviour [P5]; **the `1/sqrt(d_k)` as a variance correction** [P24], with the
measurement; softmax and its stable implementation [P2]; the value-weighted sum
as a convex combination [P18]; multi-head as a reshape and a block-diagonal map
[P6]; the residual stream as repeated addition and why that keeps gradients
alive [P15]; layer normalisation and its gradient [P17]; positional information
as rotation [F8, P8]; the parameter count, the FLOP count and the KV cache
arithmetic [P3]; and attention's quadratic cost stated as the thing every
long-context method is trying to avoid.

**P32 --- Anatomy of a training run** (*Anatomia treningu*) --- 60 frames.

The loss as maximum likelihood [P25]; its gradient as `p - y` [P17]; the
optimiser and its bias correction [P19]; precision and loss scaling [P1]; the
schedule and the curvature bound [P16]; gradient clipping and minibatch noise
[P20]. Then the diagnostic half: **a loss curve read as evidence** --- what a
plateau, a spike, a divergence and a suspiciously smooth descent each imply, and
which of them are distinguishable from noise [P26]. Scaling laws presented as
**an empirical power-law fit with reported uncertainty**, plotted on log-log
axes [F3], with the fit's extrapolation error stated --- not as a law of nature.

**P33 --- Measuring a model honestly** (*Uczciwy pomiar modelu*) --- 55 frames.

Evaluation design as an estimation problem [P25]; the confidence interval and
the bootstrap [P26]; the paired comparison; the judge model as a
miscalibrated instrument [P27]; the arithmetic of cost per token and per
conversation [P3]; and information-theoretic evaluation measures and their
limits [P28--P30]. Closes with the discipline both companion volumes are built
on, now with the mathematics behind it: **a claim needs a method and a number,
or it is labelled judgement.**

---

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

**The one ordering conflict, and how it is resolved.** P20 (stochastic
optimisation) needs random variables and variance from P23--P24, which sit in
Part VII, two parts later. Three options were considered: move the whole
probability part before optimisation; split P20; or let P20 carry a forward
reference. The resolution is the first one *locally* --- **P20 states its two
probability prerequisites in its Learning outcomes and points at P23 and P24 for
a reader who does not already have them**, and P24 revisits minibatch noise as a
worked example once the machinery exists. It is the only place in the book where
a program's prerequisite comes after it, it is deliberate, and it is recorded
here so that nobody "fixes" it by reordering the parts and breaking six other
dependencies.

A second, milder case: P21 reads better after P29's KL material, and P19 reads
better after P10's conditioning. Both are marked soft and both are written to
stand alone.

---

## 13. What this book will not teach, and where it sends you

An honest scope statement belongs in the front matter as well as here. The house
rule is that the book may say a topic is not worth its cost to this reader; it
may not pretend the topic does not exist.

| Not taught | Why not | Where to go |
|---|---|---|
| Measure-theoretic probability | Nothing in this book's payoff requires a sigma-algebra, and the machinery costs a semester. | Williams, *Probability with Martingales*; Durrett. |
| Real analysis and proof technique at epsilon-delta level | P13 teaches you to *read* a theorem, deliberately not to write one. This is Stroud's largest gap and the book fixes only half of it, on purpose. | Abbott, *Understanding Analysis*; Tao, *Analysis I*. |
| Partial differential equations | The audience meets them in physics-informed and diffusion work, and neither is served by a shallow treatment. | Strauss; Evans. |
| Stochastic differential equations, and therefore the full mathematics of diffusion models | P23 gives the discrete-time forward process as a Markov chain of Gaussians and stops there. The continuous-time formulation needs Itô calculus. | Särkkä and Solin, *Applied SDEs*. |
| Complex analysis and the Fourier transform beyond a mention | F8 gives the unit circle; convolution theorems and spectral methods are a book of their own. | Bracewell; Osgood's lecture notes. |
| Numerical linear algebra at implementation level | P10 tells you why not to invert a matrix; it does not teach you to implement a QR factorisation. | Trefethen and Bau; Higham, *Accuracy and Stability*. |
| Convex optimisation theory, duality in full | P18 and P21 give the working subset. The full theory is one of the best-written books in mathematics and there is no case for paraphrasing it. | Boyd and Vandenberghe. |
| Statistical learning theory: VC dimension, PAC bounds, generalisation bounds | Named in P13 as claims to read carefully; the bounds are almost always vacuous at realistic scale, and treating them as engineering guidance would be dishonest. | Shalev-Shwartz and Ben-David. |
| Reinforcement learning theory, MDPs, convergence results | P20 and P21 give the gradient estimators and the KL constraint, which is what an engineer touching RLHF actually manipulates. | Sutton and Barto. |
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
- a matrix with no zero entries has full rank [P7]
- the determinant tells you whether a matrix is well conditioned [P8, P10]
- a low training loss means the gradient is small [P14]
- reverse-mode autodiff is free [P15]
- a bigger batch is always a better gradient [P20]
- the probability of the evidence given the hypothesis is the probability of the
  hypothesis given the evidence [P22]
- an unbiased estimator is a good estimator [P25]
- p = 0.04 means a 96% chance the effect is real [P26]
- KL divergence is a distance [P29]
- a high mutual-information estimate means the information is there [P30]

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

Ten candidate experiments. **None has been run.** Nine of the ten are free and
run on a laptop in under a minute, which is a real advantage over the companion
volumes, where three measurements are still blocked on a provider budget.

| # | Program | Experiment | Cost |
|---|---|---|---|
| E1 | P2 | The logit at which a naive softmax overflows `fp32` and `fp16`, and the error of naive against stabilised, across magnitudes | Free |
| E2 | P3 | Hand-counted FLOPs and bytes for one transformer forward pass against measured wall clock; where the model is wrong and by how much | Free (CPU) |
| E3 | P5 | Angle between random unit vectors as dimension goes 2 -> 4096; the concentration towards orthogonality | Free |
| E4 | P11 | Singular-value spectrum of a real open-weights embedding matrix; reconstruction error against rank | Free |
| E5 | P16 | Forward against reverse mode: time and peak memory against depth; the measured cost of gradient checkpointing | Free |
| E6 | P20 | SGD, momentum and Adam on a quadratic of known condition number; iterations to tolerance against the predicted count | Free |
| E7 | P27 | Bootstrap confidence-interval width against evaluation-set size on a public benchmark; the size needed to resolve one point | Free |
| E8 | P30 | Forward against reverse KL fitted to the same bimodal target; mode covering against mode seeking | Free |
| E9 | P32 | **The headline.** Logit variance and softmax entropy with and without `1/sqrt(d_k)`, across head sizes | Free |
| E10 | P33 | A scaling-law power fit on published numbers, with the fit's extrapolation uncertainty reported | Cheap |

E9 is the one to run first: it is the measurement the whole book is arranged
around, it costs nothing, and it converts the book's central worked derivation
from an argument into a demonstration.

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

1. **One volume or two.** ~2,370 frames is 460--540 pages at this geometry.
   Parts I--VI and VII--IX split cleanly. Decide before the front matter is
   written.
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
