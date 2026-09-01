# Grounding: *Matematyka od zera dla inżyniera AI* / *Mathematics from Zero for the AI Engineer*

Competitive and pedagogical grounding for the table of contents in `structure.tex`
(F01–F13 Foundation, P01–P33 main programs). Written August 2026.

Everything below that is a *claim about the world* carries a source or is labelled
as judgement. Everything that is a *claim about what readers will do* is labelled
as unmeasured, because it is: no cohort has read this book, and the honest
position is that the pedagogy is a bet with a stated falsification condition, not
a finding. See §5.

---

## 1. What already exists, and what each does well and badly

The survey is ordered by how close each work sits to this book's intended reader:
a working software engineer, competent in code, whose school mathematics has
decayed, who is now shipping models or LLM systems.

### 1.1 Deisenroth, Faisal, Ong — *Mathematics for Machine Learning* (CUP, 2020)

**What it aims at.** It is the closest competitor and it names our gap in its own
words: the authors write that *"the gap between high school mathematics and the
mathematics level required to read a standard machine learning textbook is too
big for many people"*, and the book exists to narrow or close that skills gap.
Part I is linear algebra, analytic geometry, matrix decompositions, vector
calculus, probability, continuous optimisation. Part II derives four methods:
linear regression, PCA, Gaussian mixture models, SVM.

**Does well.** The single best-organised map of the territory. Free PDF, a
genuinely coherent narrative from vector spaces to four worked methods, and the
Part I/Part II split is the right idea — maths first, then the payoff. The
matrix-decomposition chapter is the best short treatment available. Exercises in
every chapter.

**Does badly, for our reader.**
- It states the school-to-ML gap as its target and then **starts above it.**
  Chapter 2 opens on systems of linear equations and vector spaces. Nothing in
  the book teaches you to rearrange an inequality, shift a summation index,
  manipulate logarithms, or handle exponent arithmetic without stopping to think.
  It assumes the algebra is automatic. For our reader it is not.
- **Read-then-exercise.** Exposition runs for pages; the reader is never required
  to respond mid-paragraph. Nothing forces retrieval (§2.2).
- **The four target methods are pre-deep-learning.** Linear regression, PCA, GMM,
  SVM. There is no transformer, no attention, no cross-entropy training loop, no
  softmax, no autodiff, no floating point. A reader who finishes it still cannot
  read the model card of the thing they are deploying.
- **Nothing numerical.** Not one page on overflow, cancellation, conditioning as
  a runtime failure, or dtype. These are the errors that cost money.
- **Solutions.** Worked solutions are not in the book for most exercises, so a
  self-studying engineer has no feedback loop.

**Verdict.** The best reference to *point at*. Not a path from zero, despite the
preface. It is the book this one should cite constantly and never duplicate.

### 1.2 Goodfellow, Bengio, Courville — *Deep Learning* (MIT, 2016), Part I

**Does well.** Chapter 4, *Numerical Computation*, is the most valuable sixty
pages in this entire survey and it is the one nobody imitates. Overflow and
underflow, the softmax/log-sum-exp stabilisation, poor conditioning,
gradient-based optimisation, the Jacobian and Hessian, constrained optimisation.
It is the only work here that treats the machine as a finite-precision object.
Chapter 3 on probability and information theory is compact and correct.

**Does badly.** Part I is a **refresher, not a teacher** — roughly four chapters
standing in for two years of undergraduate mathematics. Reviews note that a
non-mathematical reader finds the book difficult, and that the measure-theoretic
asides in the probability chapter are unnecessary at this level and lose
beginners. Zero exercises. Zero worked examples in the maths chapters. And it is
frozen in 2016: no transformer, no modern mixed-precision practice, no
bfloat16.

**Verdict.** Chapter 4 is the intellectual ancestor of this book's Part
*Number, precision and cost* (P01–P03). Say so in the introduction. Then go an
order of magnitude deeper, with numbers, and bring it to 2026.

### 1.3 Strang — *Linear Algebra and Learning from Data* (Wellesley-Cambridge, 2019)

**Does well.** Strang is the finest expositor of linear algebra alive, and this
book is where he connects the four fundamental subspaces, SVD, and low-rank
approximation to data. The SVD-as-the-central-fact framing is exactly right and
this book made it mainstream.

**Does badly.** Reviewers are blunt: the author *"has tried to cram far too much
material into the 432 pages"*, so each topic gets a very quick presentation;
results are stated without proof or citation (the NMF optimality conditions are
the cited example); *"Strang loves to introduce an idea without explaining it"*;
and the layout is genuinely odd — a three-page essay on neural networks sits in
the front matter before the table of contents with no explanation. It also
assumes a completed first course in linear algebra; it is a second course.

**Verdict.** A source of framing, not a model of construction. The lesson to
steal is "SVD is the centre of gravity" (P10). The lesson to avoid is coverage
outrunning explanation.

### 1.4 Boyd & Vandenberghe — *Introduction to Applied Linear Algebra* (VMLS, CUP 2018)

**Does well.** The best-designed applied linear algebra text there is, and the
closest to this book in temperament. It is deliberately, aggressively narrow:
built on **two ideas only — linear independence and QR factorisation** — and
organised around least squares and modelling rather than around the traditional
nullspace/rank/complex-eigenvalue curriculum. Free PDF, lecture slides, Julia
and Python companions, and a large separate additional-exercises set. It proves
the point that a book can omit most of a subject and be better for it.

**Does badly, for our reader.** By design it omits eigenvalues, SVD,
determinants and matrix decompositions beyond QR — precisely the parts an AI
engineer needs for PCA, conditioning, attention and covariance. No probability,
no calculus, no numerics beyond passing remarks. And it still assumes you can do
algebra.

**Verdict.** The scoping discipline to imitate. Cite it as the model for
"omitting is a design decision" (§4). Its omissions are not our omissions.

### 1.5 Boyd & Vandenberghe — *Convex Optimization* (CUP, 2004)

**Does well.** The reference. Convexity, duality, and the recognition problem —
*is my problem convex?* — are permanently useful vocabulary, and the modelling
chapters teach you to see structure. Free PDF, extensive exercises, Appendix A
reviews the required background.

**Does badly, for our reader.** It requires *good* knowledge of linear algebra
up front, by its own statement. More importantly, **deep learning is not in its
class of problems.** Non-convex, stochastic, over-parameterised objectives are
outside the theory; the algorithms it analyses are mostly not the ones you run,
and the convergence-rate proofs do not transfer. Reading it as an AI engineer is
a large investment for a small, real, but mostly conceptual return.

**Verdict.** Take the vocabulary (convexity, Jensen, duality, the constrained
Lagrangian) into P18 and P21. Do not take the curriculum.

### 1.6 Bishop — *PRML* (2006) and Bishop & Bishop — *Deep Learning: Foundations and Concepts* (2024)

**Does well.** Organisation, figures, and the probabilistic-model material are
among the best written anywhere; the 2024 volume brings the same treatment to
transformers and diffusion. If you want to understand a model as a probabilistic
object, this is where to go.

**Does badly.** Both are **more advanced than most other introductions**, by
reviewers' consensus, and assume multivariable calculus, linear algebra and
probability as working tools. The 2024 book is a companion to PRML and reviewers
note the first part is visibly patched from older PRML material, with sections
retained for no evident reason (in-depth maximum-likelihood on particular
distributions, K-means and EM). The maths is in service of models; it is never
taught from the floor.

**Verdict.** A destination, not a route. This book's success condition is that a
reader can *open* Bishop afterwards.

### 1.7 Murphy — *Probabilistic Machine Learning: An Introduction* (MIT, 2022) and *Advanced Topics* (2023)

**Does well.** The most complete and most current single treatment, unified by
probabilistic modelling and Bayesian decision theory, with an excellent
mathematical-background section and open code.

**Does badly.** Aimed at a **graduate-level readership** and explicitly assumes
calculus, statistics and linear algebra. Best described by a reviewer as an
*"encyclopedic reference"* — which is praise, and also the problem. It is
1,000+ pages and is not paced for anyone learning the mathematics for the first
time.

**Verdict.** The reference this book's appendices should route the reader to,
per topic.

### 1.8 Blum, Hopcroft, Kannan — *Foundations of Data Science* (CUP, 2020)

**Does well.** The only book in this list that takes seriously the thing
engineers most reliably get wrong: **the counter-intuitive behaviour of data in
high dimensions.** Concentration of measure, random projection, SVD, random
walks and Markov chains, clustering, network models. The authors state their aim
as covering the theory expected to be useful over the next forty years.

**Does badly, for our reader.** It is a **theory course**. A reviewer's
description is exact: the fundamentals here are *"abstract, mathematical, and
theoretical"*, and someone looking for practical tools to solve real problems
needs a different foundation. Proof-driven, aimed at CS-theory students, and its
progression does not resemble a practitioner's need.

**Verdict.** The source for P05's high-dimensional-geometry content, translated
out of theorem-proof form into consequences an engineer can act on ("your
nearest-neighbour index is meaningless at 768 dimensions unless the intrinsic
dimension is much lower").

### 1.9 3Blue1Brown (Grant Sanderson)

**Does well.** The best intuition-building mathematics media ever produced.
*Essence of Linear Algebra* and *Essence of Calculus* do something no book does:
they make the geometric content of a determinant or a derivative visible in
seconds. The neural-network and attention series are the standard reference
explanations.

**Does badly — and the author says so himself.** Sanderson has publicly
acknowledged the risk that his work is *"intellectual candy"* offering *"a
glimpse of feeling like you understand something"*, and that unless the viewer
actively engages — reinvents it, does problems — *"it's not actually going to
stick."* He extends the point to Feynman's lectures: how satisfying content is
to consume *"does not correlate with long term learning."* Beyond that: no
exercises, no assessment, no way to be told you are wrong, not searchable as a
reference, and English-only.

**Verdict.** This is the single strongest external endorsement of this book's
method, offered by the person with the most to lose from it. Quote it in the
introduction. The right relationship is complementary: watch the video for the
picture, work the program for the retention. Several programs should name the
specific video to watch first.

### 1.10 fast.ai (Howard, Gugger) — the "you need less maths than you think" position

**The position.** Deep learning is not exclusively for maths PhDs; a programmer
comfortable with Python can get real results with little maths background;
university maths is not needed up front, and the necessary calculus and linear
algebra is introduced as needed, top-down, with additional resources consulted
only when relevant.

**Where it is right, and this book must concede it.** It is right about
**entry**. Requiring two years of mathematics before anyone may train a
classifier has gatekept the field, produced nothing, and is empirically false.
Top-down order is also right: motivation before machinery.

**Where it is incomplete.** The fast.ai claim is about *starting*, not about
*debugging*, *evaluating*, or *deciding*. It answers "can I ship something?"
It does not answer:
- why the loss went to NaN at step 4,000 and only in fp16;
- whether the 3% eval improvement is real or is one draw from a noisy
  distribution;
- why the retrieval quality collapsed when the embedding dimension went up;
- whether the gradient-accumulation config changed the objective (it did — §3.17);
- what the p-value in the vendor's benchmark table actually licenses.

Those are the questions that arrive **after** you ship, and they are mathematics
questions. This book's stance: fast.ai is correct that you should not learn the
maths first, and this book is what you reach for second — when something is
wrong and you cannot see why.

### 1.11 Stroud, *Engineering Mathematics* — the method, not a competitor

Not a competitor on subject matter; it is the method being borrowed. It is the
product of roughly eight years of programmed-learning development at Lanchester
College of Technology, Coventry, and each programme was validated before final
publication to a stated success level **above 80/80** (at least 80% of students
scoring at least 80%).

Its limitations, restated as this book's obligations, are already in the brief:
no rigour; recipe-level linear algebra with no vector spaces, no decompositions
and no SVD; descriptive statistics and the normal distribution with no inference
and no Bayes; no discrete mathematics, combinatorics, graph theory or logic;
optimisation only in the advanced volume; low information density; useless as a
reference; digital extras English-only. The TOC in `structure.tex` fixes every
one of these — P04–P10 supply the vector spaces and decompositions Stroud omits,
P11–P13 the discrete mathematics, P18–P21 the optimisation, P22–P27 the
inference and Bayes, and Appendices B/C exist so the book is usable as a
reference. The Polish/English parity fixes the last one.

### 1.12 Summary table

| Work | Floor it assumes | Forces a response? | Numerics? | Modern DL? | Reference-usable? |
|---|---|---|---|---|---|
| Deisenroth et al. | Fluent algebra, some calculus | No | No | No (pre-2015 methods) | Partly |
| Goodfellow Pt I | Undergraduate maths | No | **Yes (ch. 4)** | 2016 | No |
| Strang LALFD | A first linear algebra course | No | Conditioning only | Partly | Poorly |
| Boyd VMLS | Fluent algebra | Exercises only | Lightly | No | Yes |
| Boyd CVX | Good linear algebra | Exercises only | Some | No | Yes |
| Bishop | Multivariable calculus + probability | No | No | 2024 vol. yes | Yes |
| Murphy | Graduate: calc + stats + LA | No | Some | Yes | **Yes** |
| Blum et al. | Proof maturity | Exercises only | No | No | Partly |
| 3Blue1Brown | None | **No** (author concedes) | No | Yes | No |
| fast.ai | None (by design) | Code, not maths | Practical only | Yes | No |
| **This book** | **None. Starts at arithmetic** | **Every frame** | **Part II is nothing else** | **Yes (P31–P33)** | **App. B/C by design** |

---

## 2. The gap, and the thesis

### 2.1 The gap in one paragraph

Every book in §1 is a *second* book. Each assumes a floor — algebraic
automaticity — that it does not teach and does not test, and each delivers its
content in the read-then-exercise form whose read half the retention evidence
says is nearly wasted. Meanwhile the mathematics that actually costs AI
engineers money is barely in any of them: floating-point behaviour, numerical
stability, normalisation denominators, high-dimensional geometry, and the
statistics of deciding whether a measured improvement is real. Goodfellow's
Chapter 4 is the only serious treatment of the first two, in sixty exercise-free
pages written in 2016.

### 2.2 The thesis, stated sharply

> **The binding constraint on a working engineer learning the mathematics of AI
> is not conceptual difficulty. It is two other things: algebra that has not been
> automated, and exposition that never forces retrieval. Every book in the field
> addresses neither, because every book in the field is written by someone for
> whom the algebra was automatic thirty years ago.**
>
> **Corollary (scope).** The mathematics that costs AI engineers money is
> numerical and statistical, not analytic. The expensive failures are dtype
> range, cancellation, a wrong denominator, a misread evaluation number and a
> geometric intuition transplanted from three dimensions to seven hundred — not
> an inability to prove a theorem. A curriculum that optimises for proof maturity
> is optimising the wrong variable for this reader.
>
> **Therefore:** a programmed-learning book that (a) drills algebraic
> manipulation to automaticity before it is needed, (b) demands a written
> response every few hundred words with the answer revealed only afterwards,
> and (c) spends its second half on numerics, high-dimensional geometry and
> statistical inference, will take an engineer from decayed school mathematics
> to reading a transformer paper and debugging a numerical failure — where a
> conventional exposition of identical content will not.

The evidence for (b) is not Skinner. It is retrieval practice: with total
exposure time controlled, active retrieval produces better long-term retention
than restudying — Roediger and Karpicke's students retained 61% of a passage
after a week under practised recall versus 40% under repeated rereading, and the
advantage is absent or reversed at immediate test and appears at two days and a
week. That last detail matters more than the headline: **the method is expected
to feel worse than reading while you do it.** Say so in the front matter, or
readers will abandon it for feeling inefficient.

The evidence for the trap frames (§3) is the pretesting/errorful-generation
literature: eliciting an error and then correcting it beats errorless study of
the same material for the same time, retrieval attempts help whether or not they
succeed, and the benefit is *largest when the learner strongly believed the wrong
answer* — which is exactly the design specification for a misconception trap.
Corrective feedback, including analysis of the reasoning that led to the mistake,
is what makes it work; a trap frame that merely says "wrong" is a trap frame
that does nothing.

### 2.3 What would falsify it

The house rule is that a claim needs a method and a number or an explicit label
as judgement. **All five below are unrun.** They are the book's measurement debt
and Appendix B's tables for them stay empty until they are run.

| # | Falsifier | Method | Cost | State |
|---|---|---|---|---|
| 1 | **The floor claim is wrong.** If practising AI engineers are already algebraically fluent, F01–F13 are a waste of 40% of the book. | 20-item timed diagnostic (log laws, index shift in a summation, rearranging an inequality with a negative multiplier, exponent arithmetic, function composition) to ≥50 practising engineers. Predicted: median under 60%. If median is above 85%, the thesis is dead. | Low; needs recruiting | not run |
| 2 | **The method claim is wrong.** If responding to frames adds nothing over reading them, the format is decoration. | Two arms on one program: frames-with-response vs identical prose. Same content, same time on task. Test at 7 days, not immediately. | Moderate; needs a cohort | not run |
| 3 | **The 80/80 standard is not met.** Stroud's own criterion; if a program cannot reach 80% of readers scoring 80% on its exit quiz, the program is not finished. | Instrument the exit quiz of each program with a reader cohort. | Moderate, per program | not run |
| 4 | **The trap list is folklore.** If the misconceptions in §3 are rare in the wild, the trap frames are the author's hobby-horses. | Mine a defined corpus — framework issue trackers, public postmortems, StackOverflow tags — for each of the 41 items, count incidences, and report the counts including the zeros. | Low; free; do this first | not run |
| 5 | **The prior evidence says no.** Kulik et al.'s 1982 meta-analysis of secondary programmed instruction found it *"did not typically raise student achievement […] nor did it make students feel more positively about the subjects."* Small steps and linear sequencing did not prove essential; immediate reinforcement did not prove critical. | This is already a finding, not a proposed experiment. | — | **known adverse evidence** |

Falsifier 5 must be met head-on in the front matter rather than hidden, because
it is real and because a reviewer will find it. The defensible answer, which is
itself falsifiable by experiment 2:

> Programmed instruction's *Skinnerian* claims — that steps must be small, that
> sequencing must be linear, that reinforcement must be immediate — did not
> survive scrutiny, and this book does not rest on them. What survived, and has
> since accumulated substantially more evidence than Skinner ever had, is the
> narrower mechanism the format happens to deliver: **forced retrieval with
> corrective feedback, and errors elicited before they set.** Stroud's frame
> structure is a delivery vehicle for those, not for behaviourist shaping. If
> experiment 2 shows no effect, the vehicle is wrong and the book should be
> rewritten as prose with the same trap and quiz apparatus.

That paragraph is the difference between a defensible TOC and a nostalgic one.

### 2.4 Two claims that are *not* the thesis, and should not be smuggled in

- **"You need more maths than fast.ai says."** Not claimed. You need *different*
  maths, and you need it at a different time — after shipping, when debugging.
- **"Understanding the maths makes you a better modeller."** Not claimed and not
  evidenced. The claim is narrower and testable: it makes you better at
  diagnosing failures and at judging whether a number is real.

---

## 3. The misconception list — the traps AI engineers actually fall into

Format: the **wrong belief in the reader's own voice** (this is the wording that
goes in the trap frame, because a trap only works if the reader recognises
themself), the correction, the owning program, and how well documented it is.

> **Some program numbers in this section are one low.** This list
> was written *before* P7 (tensors, shapes and index notation) was inserted by
> the curriculum review, and everything after it moved up one. The section
> headings say "(P18–P21)" for optimisation where the manifest now says
> P19–P22, and "(P22–P27)" for probability where it says P23–P28. **Do not copy
> an owner out of this file.** Re-derive it from `tools/programs.json`, which is
> the single source of the sequence. Found while writing F4, which needed the
> owner of item 25.

Frames built from these are `trapbox` in `preamble.tex`. Stroud's own model is
the harmonic series: ask whether it converges, let the reader say yes because the
terms shrink, then state flatly that this is wrong and prove it by grouping. The
error must be *elicited*, not warned against — and the correction must explain
the reasoning that produced it, or the pretesting literature says it will not
stick.

### Number, precision and cost (P01–P03)

**1. "Floating-point addition is addition, so I can sum a batch in any order."**
It is not associative. `(a+b)+c ≠ a+(b+c)` in general, and summing 10⁶ small
gradients into a large accumulator loses the small ones entirely (absorption).
Order changes the result; non-determinism in reduction order is why two runs of
the same seed differ on GPU. → **P01** for the mechanism and the threshold
(below half a gap a contribution moves the total by exactly nothing), **P02**
for what a million such losses cost and the catalogue of fixes (delivered:
naive `float32` recovers 0% of a million `1e-8` values, sorting 99.6733%, and
the other three fixes more than 99.9999%). This entry used
to route the whole of it to P01; P02's brief undertakes the accumulated loss by
name, and writing P01 was what made the split visible. Well documented; trivially
demonstrable in three lines of Python.

**2. "float16 and bfloat16 are the same thing, both are 16 bits."** They spend
the bits completely differently. fp16 is 1/5/10 (sign/exponent/mantissa),
bf16 is 1/8/7. bf16 keeps fp32's *dynamic range* and throws away precision; fp16
keeps precision and loses range, with smallest normal ≈ 6.1×10⁻⁵. This is exactly
why fp16 training needs loss scaling and bf16 usually does not. → **P01**.
Documented in vendor and framework guides.

**3. "My variance computation is fine, it's just the textbook formula."** The
naive one-pass formula `E[x²] − E[x]²` suffers catastrophic cancellation when the
mean is large relative to the spread, and can return a *negative* variance. Use
Welford. → **P01**. Classic numerical-analysis result.

**4. "Subtracting the max before softmax is a hack that changes the answer
slightly."** It changes nothing. Softmax is exactly invariant to an additive
constant on the logits, so subtracting the max is algebraically exact and merely
prevents `exp` overflowing. The stabilised form is the *same function*, not an
approximation. → **P02**. This is the single best first trap in the book: it is
provable in two lines of algebra the reader can do in F03.

**5. "I'll apply sigmoid and then take the log."** `log(sigmoid(x))` overflows or
underflows at moderate |x|; the fused form does not. PyTorch's own documentation
says `BCEWithLogitsLoss` is more numerically stable than `Sigmoid` followed by
`BCELoss` because combining them *"takes advantage of the log-sum-exp trick"*.
Same argument for `log_softmax` versus `log(softmax(·))`. → **P02**. Documented
by the framework itself.

**6. "The epsilon in LayerNorm is just a small number, it doesn't matter where I
put it."** `x/(√(σ²) + ε)` and `x/√(σ² + ε)` are different functions, and they
differ most exactly where it matters — when σ² is tiny. Frameworks differ on the
placement, and a port between them that moves the epsilon changes the numbers.
→ **P02**. Judgement on how often it bites; the algebraic difference is fact.

**7. "A 3% relative error is a 3% relative error, wherever it happens."** Not
under an ill-conditioned map. The condition number bounds how much a relative
input perturbation is amplified; κ ≈ 10⁸ in fp32 means you have no significant
digits left. Conditioning is a property of the *problem*, not of your code, and
no amount of careful implementation removes it. → **P02, P10**.

### Linear algebra (P04–P10)

**8. "My embeddings are 768-dimensional, so nearest neighbours by Euclidean
distance work like they do in 3-D — just more so."** Under broad conditions the
ratio of the farthest to the nearest distance tends to 1 as dimension grows, so
"nearest neighbour" stops being meaningful (Beyer, Goldstein, Ramakrishnan &
Shaft 1999; Aggarwal, Hinneburg & Keim 2001). It is rescued in practice only
because real embeddings have low *intrinsic* dimension — later work shows
Euclidean distance does not concentrate when the number of relevant dimensions
grows with the ambient dimension. So the escape route is a property of your data
that you should check, not a law. → **P05**. Well documented.

**9. "Two random 768-dimensional unit vectors are usually somewhere between
parallel and opposite, like in 2-D."** They are almost exactly orthogonal.
Cosine similarity of independent random unit vectors concentrates at 0 with
standard deviation ≈ 1/√d, so a "surprisingly high" cosine of 0.1 at d=768 is
2.8 standard deviations — the baseline is not 0.5, it is 0. Every similarity
threshold you have inherited is dimension-dependent. → **P05**.

**10. "Cosine similarity measures semantic similarity."** For learned embeddings
this can be false. Steck, Ekanadham and Kallus (Netflix, 2024) show cosine
similarity of embeddings from regularised linear models *"can yield arbitrary
and therefore meaningless similarities"* — not unique for some models, and
implicitly determined by the regularisation for others. Their remedy is to train
*for* cosine similarity, or normalise during/before training rather than at
measurement time. → **P05**. Well documented and recent.

**11. "My matrix has 512 columns, so the space it spans is 512-dimensional."**
That is the number of columns, not the rank. Rank is the dimension of the span
and can be far lower; and numerically the distinction is worse than binary,
because a matrix of full rank with tiny singular values behaves like a rank-
deficient one. Rank is a *cliff*; the condition number is the *slope*. → **P04,
P07**.

**12. "The determinant is nearly zero, so the matrix is nearly singular."**
Determinant scales like the product of singular values, so it is exponential in
the dimension and tells you almost nothing about conditioning. det(0.1·I₁₀₀) =
10⁻¹⁰⁰ for a perfectly conditioned matrix. Use σ_max/σ_min. → **P08, P10**.

**13. "I need the inverse, so I'll compute the inverse."** You need to *solve*.
`solve(A, b)` is faster and numerically better conditioned than `inv(A) @ b`,
and forming an explicit inverse to multiply by it is the standard beginner tell
in numerical code. → **P09**, which wrote it up in full as items 129 and 130
below — the operation count measured there, the accuracy argument owned by
**P11**. (This entry said P08 until P09 was written; P08 is rank and least
squares and never forms an inverse.)

**14. "Eigenvectors are orthogonal."** Only for symmetric (Hermitian) matrices,
by the spectral theorem. A general square matrix can have non-orthogonal
eigenvectors, complex eigenvalues, or fail to be diagonalisable at all. Attention
matrices, transition matrices and Jacobians are not symmetric. → **P10**,
which elicits it before naming it: the reader is given a non-symmetric matrix's
two eigenvectors and asked whether they are perpendicular. (This entry said P09
until P10 was written; P09 is the determinant and has no eigenvector in it.)

**15. "Singular values are eigenvalues."** They coincide only for symmetric
positive semi-definite matrices. In general σᵢ(A) = √λᵢ(AᵀA), the singular values
are real and non-negative for *every* matrix including rectangular ones, and the
eigenvalues may not exist over the reals. → **P11**, delivered: its worked
matrix has singular values 10 and 2 and eigenvalues 9.5327 and 2.0980, a 5 per
cent difference chosen so that the confusion is understandable rather than
absurd — no plot would show it. (This entry said P10 until P10 was written.)

**16. "PCA on my feature matrix."** Two silent preconditions. PCA without
*centring* returns a first component pointing at the mean, and PCA without
*scaling* returns components dominated by whichever feature is measured in the
largest units. Neither raises an error. → **P10**, delivered: its derivation
assumes centring outright and its trapbox works the metres-against-millimetres
case, whose variance differs by a factor of a million.

### Calculus and autodiff (P14–P17)

**17. "Gradient descent moves in the direction of the gradient."** It moves in
the *negative* gradient direction. The gradient points uphill — it is the
direction of steepest *increase*. This survives as a sign error in hand-written
update rules, in custom losses where a term is meant to be maximised, and in
anything involving a reward. → **P14, P19**.

**18. "The gradient of a scalar loss with respect to a weight matrix is some
shape or other; I'll transpose until it runs."** It has exactly the shape of the
weight matrix — that is the definition and it is your dimension check.
Numerator-layout versus denominator-layout conventions differ between textbooks
and a paper that does not say which it uses is genuinely ambiguous; the shape
rule is the invariant that survives the convention. → **P17**.

**19. "Backpropagation builds the Jacobian and multiplies."** It never forms one.
Reverse mode computes vector–Jacobian products; forming the Jacobian of a layer
with 10⁴ inputs and 10⁴ outputs would need 10⁸ entries per layer. This is *why*
reverse mode is cheap for scalar losses and forward mode is cheap for scalar
inputs, and it is why `jacrev` and `jacfwd` are different functions. → **P15**.

**20. "Autodiff differentiates my code symbolically / numerically."** Neither. It
is neither symbolic differentiation nor finite differences; it applies the chain
rule to a recorded trace of elementary operations, and it is exact to floating
point. The confusion produces both the belief that autodiff has truncation error
(it does not) and the belief that it can differentiate through control flow it
never recorded (it cannot). → **P15**.

### Optimisation (P19–P22)

**21. "My loss surface has local minima, and that's what training gets stuck
in."** In high dimensions, critical points are overwhelmingly *saddles*, not
local minima: a critical point is a local minimum only if all d Hessian
eigenvalues are positive, which is exponentially unlikely at random. What
training gets stuck near is plateaux around saddles. → **P17**, which elicits
the sign count and delivers it. (This entry said "P16, P18", which predates the
insertion of P7 — see the warning at the head of §3, and re-derive owners from
`tools/programs.json`.)

**22. "Adam with weight_decay is L2 regularisation."** It is not. L2
regularisation and weight decay are equivalent for plain SGD (up to a learning-
rate rescaling), but Loshchilov and Hutter showed *this is not the case for
adaptive methods such as Adam* — coupling the penalty into the gradient means
the adaptive denominator rescales it, so the effective regularisation strength
becomes a time-varying function of each parameter's gradient history. That is
the whole reason `AdamW` exists. → **P20**, which measures it: one lambda
settles the steep coordinate at 0.909 and the flat one at 0.091, and for plain
descent the two forms are the same line. Well documented; ICLR 2019.

**23. "`gamma=0.1` in my scheduler means the learning rate goes to 0.1."** It
multiplies. `StepLR(gamma=0.1)` multiplies the LR by 0.1 at each step boundary,
so three boundaries take 1e-3 to 1e-6, not to 0.1. Cosine, linear-warmup and
exponential schedules are each parameterised differently, and reading one as
another is a routine cause of "the model stopped learning at epoch 30". →
**P20**, whose brief owns warmup and cosine schedules and which elicits this
one. (This entry said "P19", which predates the insertion of P7 — P19 is
*Convexity and Jensen's inequality* and has nothing to do with schedulers.)

**24. "I halved the batch size, so I'll keep the learning rate."** Batch size and
learning rate are coupled: the gradient noise scale changes with batch size, and
the linear-scaling heuristic (scale LR with batch size, with warm-up) exists
precisely because keeping it fixed is wrong. Whether linear or √-scaling is right
is model-dependent and contested — this is one to present as *judgement with a
named disagreement*, not as a rule. → **P21**, which delivers it as two exact
invariants rather than as a recommendation: see item 220. P20 owns the
schedules; this is about the batch.

**25. "Gradient accumulation over 4 micro-batches is identical to a 4× batch."**
It is not, if the loss is a mean over a varying number of tokens. In October 2024
this was found to be wrong across most popular LLM trainers: cross-entropy is
normalised by the number of non-ignored tokens, and computing that mean *per
micro-batch* and then summing weights each micro-batch equally regardless of how
many real tokens it contains. A mean of means is not the mean. The denominator
must be computed across the whole accumulated batch. → **F04**, which elicits
the average-of-averages error itself, and **P21**, which delivers it: three
micro-batches holding 1000, 10 and 500 real tokens give a pooled loss of 2.3709
and an accumulated one of 4.3333, and with equal token counts the two are
identical over fractions — which is exactly why it ships. (This entry said "P19, P24", which predates
the insertion of P7.) Documented, recent, and expensive — it silently changed
the objective in production training runs.

**26. "Clipping gradients at 1.0 caps each gradient at 1.0."** Clipping *by norm*
rescales the whole gradient vector so its norm is at most 1.0, preserving
direction; clipping *by value* truncates each component independently and does
not. They are different operations with different failure modes and the API names
are one word apart. Measured in F06 on `(6, 0.5, −0.25)` at a threshold of 1.0:
by value the length is still **1.1456**, above the threshold it was supposedly
clipped to, and the vector has turned **23.9°**; by norm the length lands on
1.0 exactly and the direction is untouched. → **F06** for the two operations
and that measurement; **P21** for why the enormous step happens at all and what
else answers it. (This entry said "P19", which predates the insertion of P7 —
see the warning at the head of §3, and re-derive owners from
`tools/programs.json`.)

### Probability and statistics (P22–P27)

**27. "p = 0.03 means there's a 3% chance the null hypothesis is true."** It is
P(data at least this extreme | H₀ true), not P(H₀ | data). This is the first and
most common entry in Greenland et al.'s catalogue of 25 misinterpretations of
p-values, confidence intervals and power (Eur J Epidemiol, 2016) — a paper that
exists because these errors are endemic among people who have had statistical
training. → **P26**. Extremely well documented.

**28. "Our classifier is 99% accurate, so a positive result is almost certainly
correct."** At 1% prevalence, a test with 99% sensitivity and 99% specificity has
a positive predictive value near 50%; make it 0.1% prevalence and PPV falls
below 10% — a positive is *wrong more often than it is right*. And a model that
predicts "negative" always scores 99% accuracy while catching nobody (the
accuracy paradox). The base rate is not a detail; it dominates. → **P23**,
whose brief names this as "the base-rate calculation an engineer must be able
to do in a meeting" and which delivers it exactly, over fractions: the positive
predictive value is `11/122` at one fault in a thousand, and *exactly* `1/2` at
one in a hundred, where the base rate meets the error rate. (This entry said
"P22, P26", which predates the insertion of P7 — P22 is *Constrained
optimisation* — and see the warning at the head of §3.) **P28** returns to it
with a prior on the parameter rather than a point estimate.

**29. "Correlation is zero, so they're independent."** Zero correlation means no
*linear* relationship. y = x² on symmetric x has correlation exactly 0 and
complete dependence. This is the cleanest motivation for mutual information,
which does detect it. → **P23, P30**.

**30. "Covariance and correlation are the same thing up to a constant, so I'll
read the covariance matrix."** Correlation is covariance normalised by the two
standard deviations, so it is unit-free and bounded in [−1, 1]; covariance is
not, and its entries are dominated by whichever variable has the largest scale.
Reading a covariance matrix as if it were a correlation matrix means reading
your units. → **P23**.

**31. "I ran 200 hyperparameter configurations and the best one beat baseline
with p < 0.05."** With 200 comparisons at α = 0.05 you expect about 10 spurious
"significant" results under a true null. Selecting the maximum of many noisy
runs and then reporting its significance is the same error as p-hacking, and
Greenland et al. flag exactly this — that selecting analyses by the p-values they
produce breaks the guarantee the p-value was supposed to give. The reported
best-run number is an *upward-biased* estimate of that config's true performance.
→ **P26**. This one is worth being blunt about: most published model-comparison
tables contain it.

**32. "Perplexity is the average of the per-token perplexities."** It is
exp(mean NLL), not mean(exp NLL). By Jensen's inequality with a convex exp, the
two differ and the naive one is always at least as large. The same error appears
in averaging any exponentiated or log-scaled metric — and in averaging metrics
across batches of unequal size, which is item 25 wearing a different hat.
→ **P18, P29**.

**33. "Standard deviation, standard error — same thing."** SD describes the
spread of the data; SE = SD/√n describes the spread of the *estimate*. Quoting
SD as an error bar on a mean overstates uncertainty; quoting SE as if it
described the population understates the spread. And an error bar with no stated
n is uninterpretable either way. → **P26**.

### Information theory and the transformer (P28–P31)

**34. "Cross-entropy and KL divergence are the same loss."** H(p,q) = H(p) +
D_KL(p‖q). They differ by the entropy of the target, which is *constant* when the
target is a fixed one-hot label — which is why they are interchangeable for
supervised classification and why everyone believes they are always the same.
They are not, the moment the target has entropy: distillation against a soft
teacher, label smoothing, and any KL-regularised objective. → **P29**.

**35. "KL divergence is a distance between distributions."** It is not a metric.
It is asymmetric — D(p‖q) ≠ D(q‖p) — and it fails the triangle inequality.
"KL distance" is a misnomer and the asymmetry has a visible consequence: forward
KL is mode-covering (it pays an unbounded price for putting no mass where the
target has some), reverse KL is mode-seeking (it collapses onto one mode). Which
one your objective minimises changes what your model outputs. → **P29**.

**36. "Entropy is 2.3, that's fine."** 2.3 *what*? Bits (log₂) or nats (ln), and
the two differ by a factor of ln 2 ≈ 0.693. A loss quoted in nats compared
against a benchmark quoted in bits is a 44% error in the direction that flatters
you. → **P28**.

**37. "The 1/√d_k in attention is a normalisation constant someone chose."** It
is derived. If query and key components are independent with mean 0 and variance
1, their dot product has mean 0 and variance d_k — so the scores grow like √d_k,
and the original paper's stated reason for scaling is that for large d_k *"the
dot products grow large in magnitude, pushing the softmax function into regions
where it has extremely small gradients."* Dividing by √d_k holds the score
variance at 1 regardless of head dimension. The reader can derive this in P23 and
should. → **P23, P31**. Documented in *Attention Is All You Need*.

**38. "Logits are probabilities that just don't sum to 1 yet."** They are
unnormalised log-probabilities, on (−∞, ∞), and they are only meaningful up to an
additive constant (item 4). Thresholding a logit at 0.5, averaging logits across
models, or feeding a logit to something expecting a probability are all the same
mistake. → **P29**.

**39. "Output size is (W − k + 2p)/s + 1, so I'll compute it."** With a *floor*.
`⌊(W + 2p − k)/s⌋ + 1`, and when s does not divide the numerator, the trailing
input positions are silently dropped — no error, just a shape that is one smaller
than you expected three layers downstream. Dilation adds another term. Dumoulin
and Visin's guide exists because this is the standard place people lose an
element. → **F02, P03**.

**40. "Temperature 0 in softmax."** Softmax with T → 0 is a limit, not a value;
at T = 0 the expression divides by zero. Implementations that "support
temperature 0" special-case it to argmax. And note the direction: T < 1 sharpens,
T > 1 flattens, and T does not change the argmax of a single softmax at all — so
"raising temperature made the model pick a different top token" is impossible
*before* sampling and expected *after* it. → the argmax half is **F05**, which
proves it from strict monotonicity and measures how much the distribution moves
while the argmax does not; the T = 0 limit and the sampling behaviour are
**P22, P28**.

**41. "log(a + b) = log a + log b."** There is no rule for the logarithm of a
sum. `ln a + ln b` is the logarithm of the *product*, so the wrong rule does not
produce a near miss — it answers a different question: at a = 2, b = 3 it
returns ln 6 = 1.7918 where ln 5 = 1.6094 was asked for. The reasoning is a true
rule generalised past its hypothesis, and **the same reasoning keeps arriving
under a new sign**: F01's √(a+b) ≠ √a + √b, F02's (a+b)² ≠ a² + b², this, and
F4's Σaᵢbᵢ ≠ (Σaᵢ)(Σbᵢ) at item 42 below. Name the places, never a count — the
count was stated here as "three in three programs" and F4 made it four. Where the reader genuinely needs ln(e^u + e^v),
the move is to factor the larger exponential out — v + ln(1 + e^(u−v)) — which
is why the library ships `logaddexp` and `logsumexp` rather than an identity.
→ **F03**, and it hands the stability half to **P02**.

*This one is the book's own rather than sourced.* It was added while F03 was
being written, because F03 needed a headline trap and the catalogue had none for
the Foundation part. The list above is a catalogue of misconceptions observed in
practice; this entry is a claim about what a reader will write when asked
quickly, and it has not been counted. Falsifier 4 in §2.3 applies to it more
than to the others.

### Foundation (F01–F13)

The entries in this section came out of writing the Foundation programs
themselves rather than out of the literature: item 41 out of F3, items 42 to 46
out of F4, items 47 and 48 out of F5, item 49 out of F6, items 50 and 51 out of
F7, items 52 to 54 out of F8, items 55 to 57 out of F9, items 58 to 62 out of
F10, items 63 to 66 out of F11, items 67 to 70 out of F12 and items 71 to 73
out of F13. Say which program produced which, never how many there are — the count at the head of §3 was stated once and had
drifted by five before anybody reread it.

They carry the same health warning: the list above is a catalogue of
misconceptions *observed in practice*, and these are claims about what a reader
will write when asked quickly. **None of them has been counted.** Falsifier 4 in §2.3 applies to
them more than to the sourced entries.

**42. "A sigma distributes, so the sum of the products is the product of the
sums."** Σaᵢbᵢ is not (Σaᵢ)(Σbᵢ): at a = (1,2), b = (3,4) the first is 11 and the
second is 21. The two rules that *are* true — Σ(aᵢ+bᵢ) splits, and a constant
comes out of the front — are both about a **sum** inside the sigma, and the
reader carried them across a product. It is item 41's reasoning wearing the
fourth of its signs, and the AI payoff is direct: an attention score is Σqᵢkᵢ, so
it cannot be recovered from two running totals. → **F04**, and **P05** for what
the dot product means.

**43. "Σ from i = 0 to n has n terms — it says n."** Both limits are included, so
the count is stop − start + 1 and the answer is n + 1. It is the fence-post: a
hundred-metre fence with a post every ten metres carries eleven posts. The third
shape, Σ from 0 to n−1, is the one `range(n)` walks and the one that does have n
terms, which is why the three get confused. → **F04**.

**44. "An empty sum and an empty product are both zero"** — or, from the other
side, "both are undefined." `sum([]) == 0` and `math.prod([]) == 1`, and neither
is a convention picked for tidiness: each is the identity element of its
operation, and no other value leaves the next term alone. *Nothing* has one name
and the two operations have two identities. It pays twice: a⁰ = 1 is the empty
product, which is a second and independent route to F01's division-law argument,
and ln of the empty product is ln 1 = 0, which is the empty sum, so ln ∏ = Σ ln
holds at zero terms with no special case. The live version is a fully masked
batch: the empty **sum** is safe and the empty **mean** is not, so the guard
belongs on the denominator. → **F04**, and **P01** for what the division then
does.

**45. "To combine two batch losses, average them."** A mean of ratios is not the
ratio of the sums. 1000 tokens at mean loss 2.0 and 10 tokens at mean loss 8.0
pool to 2.06, not 5.0 — the reader gave weight one half to two numbers that were
already averages of very different amounts of evidence. Both quantities are
real: the **micro** average pools the items, the **macro** average averages the
group numbers, and they agree exactly when every denominator is equal. So the
fault is never "you computed the wrong one", it is not knowing which one you are
holding — they are reported in the same column, under the same word, to the same
number of decimal places. Item 25 is the training instance of this and item 32
is its non-linear cousin, and the two have different mechanisms and different
fixes. → **F04**, with the evaluation half at **P27** and the accumulation half
at **P21**.

**46. "β = 0.9 means ninety per cent of the new value, so a bigger β reacts
faster."** β weights the **old** value. With m ← βm + (1−β)g at β = 0.9, m = 1.0
and g = 11.0, the next reading is 2.0 and not 10.0, and raising β makes the
average *slower*, not quicker. The misreading is easy because β is the number
written in the configuration file and the coefficient on g is written nowhere —
it is 1 − β, computed. Two further corrections come with it: "β = 0.9 averages
the last ten" names 1/(1−β), which is a scale rather than a count, and half the
weight actually sits in the last seven; and the coefficient is written both ways
round in real code, so the same word names two opposite numbers. → **F04**, and
**P20** for momentum and Adam.

**47. "f(x − 3) shifts the graph three to the left — the sign says minus."**
It shifts three to the **right**. Outside the bracket a minus really does move
the graph down, and that is the true rule the reader is carrying across; inside
the bracket the number adjusts the *question* rather than the answer, so to see
the value f gave at 0 you must now stand at x = 3. It is item 41's reasoning
under a fifth sign, and the parabola settles it without argument: (x − 3)² has
its lowest point at x = 3. → **F05**.

**48. "The bias is where the unit fires."** σ(wx + b) crosses a half at
x = −b/w, not at b and not at −b, so one bias sets a different threshold at
every weight: at b = −2 the crossing is at 2 when w = 1 and at 0.4 when w = 5.
The misreading is natural because b is the number written in the configuration
and the weight dividing it is written nowhere. It is the inside-the-bracket
rule of item 47 with a scaling stacked on it. → **F05**. No program undertakes
the obvious remedy (parametrise the unit by its threshold rather than by its
bias), and none is claimed here for it.

**49. "Every rule of equation-solving carries across to an inequality."** All
but one. Adding, subtracting and scaling by a *positive* number are safe;
multiplying or dividing by a *negative* number reverses the sign, and nothing
in the notation marks the moment it happens. `2 < 5` but `−2 > −5`: multiplying
by a negative reflects the line, and a reflection swaps left and right. The
error is easy precisely because the other four habits are correct, so it is the
same shape as items 41 and 47 — a true rule carried one step past its
hypothesis. The reliable fix is not to remember the exception but to avoid the
step: move the term across instead of dividing. → **F06**.

**50. "Exponential growth means fast growth."** It means growth proportional
to the current size, and says nothing about where on the curve you are
standing. At x = 5 the polynomial x^5 is 21.1 times larger than e^x, and e^x
does not overtake until x = 12.71. What is true, and is why the word is worth
using, is the other end: once it passes it never comes back, and no polynomial
of any degree stays ahead forever. → **F07**, and **P03** for what the same
confusion does to a cost estimate.

**51. "tanh was preferred to the logistic because it saturates more gently."**
It saturates *harder*. Its steepness runs 1.0 to 0.0707 over two units against
the logistic's 0.25 to 0.105 — a factor of about 14 against about 2 — and this
follows from tanh(x) = 2σ(2x) − 1 rather than being a separate fact: two
squashes make it four times as steep at the centre and move its flat region
four times closer in. The real case for tanh was always that it is centred on
zero, which is a claim about where its outputs sit and not about how it bends.
→ **F07**, and **F12** for why the flatness costs what it costs.

**52. "`math.sin(90)` gives 1, because sin 90 degrees is 1."** It gives 0.8940.
Every library reads the argument as radians, and 90 radians is 14.32 full
turns, so the point has gone round more than fourteen times and stopped
somewhere unremarkable. What makes it expensive is what does *not* happen:
nothing raises, nothing warns, and the answer is an ordinary number between
−1 and 1, so it flows on and the first symptom is a result that is merely
wrong. → **F08**.

**53. "A cosine similarity of 0.99 means the two vectors are essentially the
same direction."** It is an angle of 8.1 degrees, and 0.98 is 11.5 — cosine is
flat at zero, so its turning point is exactly where thresholds get set and a
small change in the number is a large change in the angle it admits. The
similarity scale is not linear in the quantity anybody cares about, and it is
least linear in the region everybody tunes. → **F08**.

**54. "A high cosine similarity means the two documents are similar in
meaning."** It means the two vectors point nearly the same way, to fifteen
decimal places. That the angle tracks meaning is a claim about how the vectors
were trained, holds better for some pairs than others, and has to be measured
on the task. The exactness of the geometry is easy to let launder the
interpretation. → **F08** for the geometry, **P05** for the baseline it sits
against, **P34** for how to find out whether a score means anything on your
data.

**55. "`v + 1` adds one to the vector."** In the mathematics it means
nothing: `v` is a list and `1` is not, so there is no component-by-component
pairing to make. An array library will read it as adding `1` to every
component, which is a reasonable convention with its own rules and is not what
the mathematics says. The habit worth building is noticing that the line's
meaning came from the library rather than from the mathematics, because that
is the line whose behaviour changes when the shapes do. → **F09** for the
distinction, **P07** for the rules.

**56. "Lengths add: two vectors of length 3 and 4 give one of length 7."**
Only if they point the same way. At right angles they give 5, and in general
`|a + b| <= |a| + |b|` with equality exactly when one is a non-negative
multiple of the other. Two lengths laid end to end on a line *do* measure 7,
which is where the habit comes from, and a vector carries a direction as well
as a size. Same shape as items 41, 47 and 51 — a rule carried one step past
its hypotheses because nothing announced that the setting had changed.
→ **F09**.

**57. "Nearest neighbour and most similar are the same ranking, so cosine or
Euclidean makes no difference."** On the unit sphere that is exactly right and
provably so: `|a - b|^2 = 2 - 2 cos(theta)`, a strictly decreasing function of
the cosine, which cannot reorder anything. Off it the two name different
winners — on one query and two candidates, A can be the more similar while B
is the nearer — and what makes it expensive is that both queries run, both
return plausible results, and nothing in the output says they disagreed. The
question to ask of an index is therefore not which measure it uses but whether
what went into it was normalised. → **F09** for the identity that says when
they cannot disagree, **P05** for which to prefer when they do and what
normalising costs.

**58. "We trained on ten million tokens" and "our vocabulary is ten million"
are the same claim.**  `len(tokens)` and `len(set(tokens))` are one function
call apart and answer different questions; on a repetitive corpus they differ
by a large factor. Neither number is more correct, and the words for them are
not interchangeable — when a count appears in a claim, say whether it counted
occurrences or distinct things. → **F10**.

**59. "Two evaluation sets of 1000 and 1200 give 2200 examples."** Only if
they are disjoint. `|A ∪ B| = |A| + |B| − |A ∩ B|`, and the shared part was
counted once too often. What makes it expensive is that the error has two
halves and only one is visible: the count overstates coverage, *and* every
shared example is scored twice, so it weights double in whatever average comes
out. → **F10** for two sets, **P12** for inclusion–exclusion in general — **delivered**, as item 146, where the third set makes the alternating sign necessary rather than decorative.

**60. "`not (a and b)` is `not a and not b`."** It is `not a or not b` — the
`and` becomes an `or`, because failing *both* only requires failing one. The
wrong negation of a conjunction **always keeps too little, never too much**,
and that is why it survives: a filter that keeps too much shows you rows you
did not expect and you go and look, while a filter that keeps too little shows
you nothing at all and the only symptom is a dataset smaller than it should be
— which is the symptom everybody attributes to the data. → **F10**.

**61. "Just try all the combinations."** A set of n things has 2^n subsets,
and doubling per element is not a rate anybody's intuition handles: twenty
features is a million, forty is more than a million million, and the step
between them is twenty more yes-or-no choices. When a plan enumerates
combinations, write the count down before writing the loop. → **F10** for the
count, **P12** for the four rules formally — **delivered**, as items 144 to
147. Note also that the product rule needs its condition stated: it applies to
*independent* choices, and one forbidden combination makes the multiplication
wrong. P12 refines that condition rather than repeating it: what has to be
fixed is the **number** of options at each step and not the options
themselves, which is why a shrinking pool multiplies anyway.

**62. "Twice the data is twice the work."** Not when the work is per pair.
n items make n(n−1)/2 pairs, so doubling multiplies the work by
(4n−2)/(n−1) — 4.020 at a hundred, 4.002 at a thousand, falling towards four
**from above**. The overnight job on last month's corpus does not run
overnight on twice the corpus; it runs for four nights. Worth knowing as a
count before it is known as a growth rate: → **F10** for the count, **P03**
for the notation and for what that notation does not say.

**63. "The derivative is the slope of a chord with a very small gap."** It is
not a chord slope at all. Every chord slope of `x²` at 3 is `6 + h` and none
of them is 6; the derivative is the number they approach, which is a statement
about the whole family rather than about any one of them. The distinction
sounds like pedantry until a machine is asked to shrink `h` and the answer
gets *worse* — if the derivative were just "the chord with a tiny gap", that
could not happen. Read `lim h → 0` as *as close as you like, by choosing h*,
never as *at h = 0*. → **F11**.

**64. "Smaller h is more accurate."** True in the mathematics, false on the
machine, and the two part company sooner than anybody expects. Two errors pull
opposite ways — the chord not yet being the tangent, and the two values of `f`
becoming too close to subtract — so the error curve is a **U**, and its bottom
is nowhere near the smallest `h` you can type. At `h = 1e-16` the answer is
exactly zero, because `x + h` *is* `x`. The consequence: a gradient check
agrees to a handful of digits and one demanding more fails on correct code.
→ **F11** for the shape, **P01** for the right-hand branch.

**65. "A zero gradient means we have reached a minimum."** It means the curve
is level, and a maximum is level too, and so is a flat spot on the way up. The
first derivative is computed from an arbitrarily small neighbourhood and
cannot tell the three apart; the non-committal word is *stationary point*.
**Stopping is not the same as arriving.** → **F11** for the distinction,
**F12** and **P17** for what the second derivative adds, **P19** for whether a
minimum found is the only one.

**66. "The gradient is still large, so we are far from convergence."** Not an
inference, and neither is its opposite. A derivative is local: it says how
steep the ground is *here* and cannot know how far anything is. On
`x⁴ − 4x²` the point at 1.9 has slope 12.2 and is 0.49 from the minimum, while
the point at 0.4 has slope −2.9 and is 1.01 away — the steeper point is the
nearer one, by a factor of two. Reading distance out of a gradient is asking
one number for information it was never given. → **F11**.

**67. "The derivative of `fg` is `f'g'`."** Differentiation distributes over
a *sum*, which is exactly why the guess is so natural, and it does not
distribute over a product. On `x²` and `x³` at `x = 2` the truth is 80 and the
guess gives 48, and the two expressions agree at exactly two points in the
whole range swept — there is no region where the guess is even approximately
right. When `x` moves, *both* factors move; the guess multiplies two rates,
which is not a rate of anything. Same shape as items 41, 47, 51 and 56.
→ **F12**.

**68. "`f'` is evaluated at `x`."** In `f(g(x))`, the outer derivative is
evaluated at `g(x)` — at the value the inner function produced, not at the
input. It is the half of the chain rule that gets dropped, and dropping it
gives an expression that is dimensionally fine and numerically wrong, so
nothing complains. → **F12**.

**69. "Backpropagation is a special algorithm for neural networks."** It is
the chain rule applied to a composition of layers, with the intermediate
values kept rather than recomputed, and there is nothing else in it.
"Backward" names the direction the multiplication accumulates in. Two things
follow immediately and are usually learnt the hard way: the activations must
be *stored*, so memory grows with depth and batch size; and a deep weight's
gradient contains every factor between it and the loss, so nothing about
training one layer is local to that layer. → **F12**, **P16** for the vector
version and the memory trade.

**70. "Deep networks have vanishing gradients."** What is true is narrower and
arithmetic: a chain of logistic layers multiplies one factor of `w·σ'(z)` per
layer, and `σ' ≤ ¼` always, so forty layers at unit weight give at most
`0.25⁴⁰ ≈ 8e-25` — *at their very best*, with every unit sitting exactly at
its most responsive point. Nothing there is a property of neural networks; it
is what happens when forty numbers below one are multiplied. And the exploding
side is **not symmetric**: the factor is at most `w/4`, so a logistic chain
cannot amplify at all unless `|w| > 4`. Change the activation, add a residual
path, or normalise, and the factors change — which is why each of those was
adopted. → **F12** for the mechanism and both bounds, **P32** for the
architecture's answer.

**71. "A density's value at a point is a probability."** It is a probability
**per unit of x** — a rate, as a speed is not a distance. What is bounded by
one is the *area*, and nothing bounds the height: the uniform density on an
interval of width 0.1 has height 10, and narrowing the interval raises the
height without limit while the area stays 1. So a likelihood a library prints
above one is not a bug, two of them can be compared as a ratio, and neither
can be read as a probability. → **F13**, and it is F10's count-against-
denominator point in its continuous form.

**72. "`dx` is notation you can ignore."** It is the *width of the strip*, and
an area needs a width — drop it and the expression is a height, which is a
different kind of thing. It is also what makes the units work: an integrand in
requests per second times `dx` in seconds gives requests, which is what an
accumulated total should be. **Reading the units off an integral is the
cheapest check there is**, and it catches a dropped `dx` immediately.
→ **F13**.

**73. "An integral is an antiderivative."** They are different objects joined
by a theorem: one is an accumulated total, a number or an area; the other is a
function whose derivative is the integrand. Treating them as synonyms hides
the theorem's conditions, and it obscures why plenty of ordinary functions
have an integral you can compute numerically and no antiderivative anybody can
write down — `e^(-x²)` being the one you will meet, whose accumulated total is
the normal distribution's. → **F13**.

### Number, precision and cost, written (P01)

Items 1 to 7 above came out of the literature before Part II was drafted. These
came out of writing P01 itself, on the Foundation section's pattern: items 74 to
79 out of P01.

**74. "Floating-point error is a small random wobble."** It is a *spacing*, and
the spacing is a fixed fraction of the number rather than a fixed distance. The
gap to the next double is 2.22e-16 at 1 and 1.19e-07 at a billion — six orders
of magnitude apart, because a fixed budget of significant bits is a fixed
*relative* precision. Anybody carrying a mental model of a small absolute
inaccuracy has it wrong at exactly the magnitudes where it matters. → **P01**.

**75. "`abs(a - b) < 1e-9` is a reasonable equality test."** It is wrong at both
ends and for the same reason as 74. Near a billion it demands agreement finer
than the format can express, so it calls equal numbers different; near 1e-12 it
calls everything equal, including values differing by a factor of a thousand. A
tolerance has to be relative — some multiple of epsilon times the size of the
numbers. → **P01**.

**76. "One of these two devices is computing the gradient wrong."** Neither is.
They partition the reduction differently, so they add the same numbers in a
different order, and a different order is a different *correctly rounded*
answer. Bit-exact reproducibility across hardware is something you buy with a
fixed reduction order, at the cost of parallelism — not something you have.
→ **P01**.

**77. "A very small contribution makes a very small difference."** Below *half*
the gap at the running total it makes exactly none: under round-to-nearest the
nearest representable result is the number you started with, so the addition is
a no-op that returns successfully. `1.0 + 1e-17 == 1.0` is `True`. The threshold
is half an epsilon of the total — 6.0e-08 in fp32, 3.9e-03 in bf16 — which is
why accumulators are kept wider than the values entering them. → **P01** for the
threshold, **P02** for what it costs at scale.

**78. "bf16 is the better format, so it must be the more precise one."** It is
the *less* precise one, by a factor of eight, and that is what it was designed
to be: three bits moved off the significand and onto the exponent buy thirty-
three orders of magnitude of extra reach. bf16 is fp32 with the bottom of the
significand removed — same exponent budget, so a conversion between them cannot
overflow. The design question was never "how accurate" but "what fails first",
and for training the answer is range. → **P01**.

**79. "A vanishing gradient is a gradient that has become small."** Often it is
one that has left the number system. F12's forty-layer product reaches 4.8e-105,
which is a small number in fp64 and *exactly zero* in fp32 — whose smallest
subnormal is 1.40e-45 — and fp32 is the training format. "Very little" and
"nothing" behave differently downstream, and only one of them can be rescued by
scaling. → **P01**, with **F12**.

### Numerical stability, written (P02)

Items 80 to 86 came out of writing P02, on the same pattern.

**80. "The one-pass variance formula is fine — it is just algebra."** The
algebra is beyond reproach and the arithmetic is not. On five latency readings
of 30000 and the four microseconds after it, `E[x^2] - (E[x])^2` in `float32`
returns **-64**, against a true variance of 2. A variance cannot be negative.
The two quantities agree to nine significant figures where the format holds
seven, so the subtraction cancels every digit they share and hands back the
rounding — and -64 is exactly one `float32` gap at that magnitude, which is
the smallest non-zero answer it could have given. → **P02**.

**81. "Then run it in float64 and it is fine."** A wider format moves the
cliff; it does not remove it. The subtraction of two nearly equal large
quantities is still there, so the same formula fails on data a few orders of
magnitude larger. The fix is a different algorithm — Welford's never forms
`E[x^2]`, so every subtraction is of the size of the spread rather than of the
data. **Every fix in this area has that shape**: remove the destroying
operation rather than making it more accurate. → **P02**.

**82. "My softmax pivots on the first score rather than the maximum, and it
has never failed."** That is a fact about the data, not about the code.
`ln sum exp(z) = c + ln sum exp(z - c)` holds for *every* c, and `fp16`
tolerates a shortfall of up to 11.09 between the largest score and the pivot,
so on an ordinary row most choices work. Measured: **three of five pivots keep
every term inside `fp16`** on one ordinary row. Only the maximum bounds every
remaining exponent at or below zero, so only the maximum is safe for every
input — which is what "numerically stable" means as a technical term: not
*more accurate*, but *safe for inputs you have not tried*. → **P02**.

**83. "Sorting the values before summing fixes it."** It fixes the catastrophe
and leaves the drift. A million values of `1e-8` added to a `float32` total of
1 gives exactly 1 naively — every one lost — and sorting ascending
recovers **99.6733%**, where compensated summation and a pairwise tree recover
99.9999% and a wider accumulator recovers all of it. Sorting is the cheapest
fix and the weakest one, and it is the one most often described as sufficient.
→ **P02**.

**84. "A confident *correct* prediction cannot produce a `nan` loss."** It can,
and it is the failure that sends people looking for a bug in their data.
`sigma` rounds to exactly 1.0 from x = 37, so `1 - p` is exactly zero and
`ln(1 - p)` is `-inf` — the same `-inf` a confident *wrong* prediction
gives. The other end fails too: below about x = -746 `sigma` underflows to
zero and `ln(sigma)` is `-inf`. Both ends are removed by keeping the logit and
letting the loss compose, which is why the library ships one function.
→ **P02**, with **F05** and **F07**.

**85. "The worst-case error bound is what my network does."** A bound is not a
prediction. Over 96 layers `fp16`'s worst case is 9.82% and `bf16`'s is
111.08%, but that assumes every rounding pushes the same way; roundings of
random sign accumulate like the square root of the depth, about **ten times
smaller** for `fp16`. Neither number is what your network does — one is an
upper bound and the other assumes an independence nobody checked. What both
establish is that depth multiplies your format's epsilon by something between
sqrt(n) and n. → **P02**, paying **F01**'s compounding argument.

**86. "The epsilon in the layer norm protects the division."** Only if it is
scaled to the format. `fp16`'s epsilon is around `1e-3`, so an `eps` of `1e-8`
added inside the square root changes no bit at any variance the format can
represent, and the division it was supposed to protect is unprotected. That is
why mixed-precision recipes compute normalisation statistics in `float32` even
when everything around them is sixteen bits. → **P02**, paying **F02**.

### Cost and orders of magnitude, written (P03)

Items 87 to 92 came out of writing P03.

**87. "It is O(n log n), so it is the faster one."** A growth rate is not a
ranking. It says which algorithm wins *eventually*, and eventually may be past
every input the system will see. Measured: `n^2` against `200 n log2 n` trade
places at **n = 2224**, and at n = 100 the asymptotically better one costs
**13 times as much**. Every sorting library in wide use ships an O(n^2)
insertion sort on short subarrays for exactly this reason, and nobody calls it
a compromise. → **P03**, paying **F10**'s request for a worked account.

**88. "An algorithm that takes n steps is O(n), not O(n^2)."** It is both. O is
an *upper bound* on growth, not a description of it, so a linear algorithm is
honestly O(n^2), O(n^3) and O(2^n) as well. The notation for *exactly this
growth, no better* is Theta, and it is usually what was meant. The practical
consequence is that "our retrieval is O(n)" cannot be falsified by a benchmark:
it is compatible with any constant whatsoever, and the constant is what you
pay. → **P03**.

**89. "The model is 14 GB, so a 24 GB card can train it."** The weights are
**12%** of the training bill. Gradients add another copy, and a
moment-based optimiser with a full-width master copy adds three more at double
the width: **112 GB in all, eight times the number on the model card.** Each
remedy removes a *row* rather than shrinking all of them, which is what lets
you predict whether it will be enough. → **P03**, paying **F01**'s "this is a
floor" twice over.

**90. "Attention is quadratic, so the cache is quadratic."** The *arithmetic*
is quadratic in the sequence and the **cache is linear**. It holds one key and
one value per *position*, not per pair — the pairs are formed and consumed
inside the computation and never stored. Two quantities, two exponents, one
layer: 4 GiB at 8192 tokens and 8 at twice that, or about 0.5 MB per token in
flight. It is usually larger than the weights and it decides how many users a
card serves. → **P03**.

**91. "Matrix multiplies are compute-bound."** The large ones are. Intensity is
`2n/(3b)`, which *grows with n*, so on a device doing 200 operations per byte
delivered a multiply is compute-bound only above about **n = 600**. A batch of
small multiplies — narrow heads, low-rank adapters, a mixture of narrow experts
— sits on the wrong side of that line and is governed by data layout rather
than by operation count. → **P03**.

**92. "Fusing the kernels will make it compute-bound."** It will not. Fusing
three elementwise operations divides the bytes by three for the same
operations, taking the intensity from 0.17 to 0.5 — against a device ratio of
200. **Fusion helps and does not rescue**, because the bytes have a floor: the
input must be read once and the output written once whatever happens between.
A plan that assumes otherwise is a plan a profile will disappoint. → **P03**.

### Vector spaces and basis, written (P04)

Items 93 to 98 came out of writing P04.

**93. "Embedding dimension 4096 means the model has 4096 independent
directions to give things."** It means the embeddings live in a space of that
many dimensions, so at most that many of them *can* be independent. A
vocabulary of 20,000 in 4096 dimensions leaves **at least 15,904 of the
embeddings — 80% — as combinations of the others**, and it is a counting
theorem: no amount of training changes it and no architecture avoids it. The
only way to move the number is to change one of the two integers.
→ **P04**.

**94. "So the model cannot represent more than 4096 concepts."** A different
claim, and the counting bound does not support it. A space of `d` dimensions
holds exactly `d` mutually independent directions and vastly more that are
*nearly* independent. Relaxing "exactly" to "nearly" is not a technicality, it
is the whole of the interesting question — and answering it needs a way to
measure "almost", which means angles. The bound establishes only that some
account of the packing is needed, never which one. → **P04** for the bound,
**P05** for the measurement.

**95. "Superposition explains it, and the counting bound proves superposition."**
The bound is a theorem; the linear-representation and superposition accounts
are hypotheses about how a trained network is structured. They are motivated
and have evidence behind them, and neither is established by the bound. The
confusion is common because the bound is quoted immediately before the account,
as though the first entailed the second. It entails only that *some* such
account is needed. → **P04**.

**96. "Neuron 2317 detects X."** A component is a coordinate against whatever
basis training happened to land on. A basis is not unique — another run, or the
same one with a different seed, lands on a different one for a space that may
be doing the same job. The working test is one line: **a method that works in
any basis measures something real; a method that needs a particular basis
measures your choice of axes.** Length, independence and the dimension of a
span are in the first category; the value of one component is in the second.
→ **P04**.

**97. "Eight vectors, so eight directions."** Three numbers get attached to a
list of vectors in the same breath and only the last is the dimension: how many
vectors there are, how many components each has, and how many independent
directions they reach between them. Eight vectors of five components each can
span a plane. The first two are properties of how the data was written down;
the third is a property of the data. → **P04**.

**98. "Adding more vectors adds more directions."** Rank saturates at the
number of components, and the reasoning needs no machinery: each new vector
either points somewhere the earlier ones could not reach, growing the span by
one, or is already a combination of them and grows it by nothing. Measured in 8
dimensions: 2, 4, 8 vectors reach 2, 4, 8 directions, and 12, 20 and 40 all
reach 8. The random draws are testing the code, not the claim — a
counterexample would refute a proof. → **P04**.

### Inner product, norms and high dimension, written (P05)

Items 99 to 105 came out of writing P05.

**99. "A cosine similarity of 0.3 means the two are weakly similar."** Read on
two-dimensional intuition, where 0.3 is a fairly open angle. In 768 dimensions
the cosine between two random directions has spread 1/sqrt(768) = 0.036, so 0.3
sits about **eight spreads** out from what chance produces. It is an enormous
similarity, not a weak one. The correction is not a threshold to memorise: it
is to divide by 1/sqrt(d) and ask how many spreads out you are, which has an
answer at any dimension. → **P05**, paying **F09**'s deferred "what a typical
pair looks like".

**100. "Normalising the embeddings is a preprocessing step."** It is the
decision, taken silently, to throw the lengths away. On unit vectors the dot
product *is* the cosine — checked to 3.3e-16 over 2000 pairs — so normalising
does not make one behave like the other, it makes the two queries the same
query. An embedding's length can track token frequency, encoder confidence or
input length; declaring none of that worth ranking on may well be right, and it
should not happen in a utility function nobody reviewed. → **P05**.

**101. "Cosine and dot product are rival similarity measures."** One is the
other multiplied by both lengths. They can only disagree when the lengths
differ, and the choice is a question about what your embeddings encode in their
magnitude — which the formulas cannot answer and a benchmark usually will not
either. → **P05**, extending **F09**'s worked disagreement case.

**102. "High dimension gives you exponentially many nearly-orthogonal
directions."** True above a threshold, and always quoted without it. The
tolerance has to sit several spreads out and the spread is 1/sqrt(d), so at a
tolerance of 0.2 the crossover is at **d = 488**. Below it the relaxation is a
*harder* requirement than exact orthogonality: at d = 64 the capacity is about
4, against the 64 that are exactly orthogonal. Above it the capacity runs away
— about 9,500 at d = 768 and 8e18 at d = 4096. → **P05**, paying **P04**'s
counting bound its relaxation.

**103. "L1 gives sparsity because the penalty is harsher."** It gives sparsity
because its unit ball is a diamond and a diamond has corners, and a corner is a
point where all but one coordinate is zero. A contour arriving from a generic
direction meets a corner far more often than chance suggests. It is a statement
about shape, and it would still be true if the optimiser were replaced. → **P05**.

**104. "The L2 norm is the real size and the others approximate it."** Three
norms are three answers to three different questions, and they do not order
vectors the same way: (3,-4) and (5,0) are equal under L2, and each is larger
than the other under one of the remaining two. Only L2 comes from an inner
product, which is why only L2 has angles attached. → **P05**.

**105. "Most of a ball is somewhere in the middle."** The fraction inside
radius r is r^d, so in 768 dimensions the inner nine tenths of the radius hold
7.2e-36 of the volume and the inner half holds 6.4e-232. Essentially all of a
high-dimensional ball is in its outermost skin — which is why sampling to find
a point near the centre would return nothing, and finding nothing is not
measuring nothing. → **P05**, paying **F09**'s "how much of the space is near
the middle".

### Matrices as linear maps, written (P06)

Items 106 to 111 came out of writing P06.

**106. "Linear means a straight line."** The English word and the mathematical
word have drifted apart, and the most quoted straight line there is, y = mx + c,
is linear only when c = 0. Linear means two properties — f(u+v) = f(u)+f(v) and
f(cv) = c f(v) — which together force f(0) = 0, and that is the quickest test.
Every layer in a network is *affine*, not linear, because of the bias, and the
distinction is what makes the collapse argument need two lines of algebra rather
than one. → **P06**.

**107. "Matrix multiplication is a rule about rows and columns."** It is
composition of functions, and the rows-into-columns procedure is a consequence.
The difference is not stylistic: associativity is a hard theorem about
reordering a triple sum when read as a procedure, and nothing at all to prove
when read as composition, because A(B(C(x))) never had a bracketing. Whenever a
fact about matrices looks arbitrary, the reading has slipped back to the
rectangle. → **P06**.

**108. "AB and BA are two ways of writing the same thing."** The habit is not
careless — it is a generalisation from the only case anybody had, since every
multiplication before this one commuted, and a one-dimensional layer's weight is
a number. Measured: of 5,000 random 3x3 pairs, **none** commute, and none could,
because commuting is a condition on a set of measure zero. Rotations of the
*plane* about one centre do commute, which is exactly why two dimensions is the
misleading case: rotations in three dimensions do not. → **P06**.

**109. "A shape error is a bookkeeping problem, so reshape until it stops
complaining."** The shape is the domain and the codomain written down, so a
shape error is a **type** error reported by arithmetic. `(32x768 and 512x768)`
names two plausible and different bugs — a layer given the wrong width, or
something transposed that should not have been — and the shapes say which, by
saying what each factor claims to be a map *between*. → **P06**.

**110. "Stacking linear layers makes the model deeper."** k affine layers with
nothing between them are one affine layer: W2(W1x + b1) + b2 = (W2W1)x +
(W2b1 + b2). So (k-1)/k of the parameters are redundant **whatever the width**
— 87.5% at eight layers — and the waste is exactly the depth that was supposed
to have been bought. → **P06**, doing **F05**'s one-dimensional argument in more
than one dimension.

**111. "An activation squashes values into a range."** ReLU is unbounded above
and squashes nothing, and it works. The requirement met by every activation in
use is only that it is **not affine**, because an affine one lets the layers
collapse. The clean test in more than one dimension needs no picture: an affine
map cannot bend a straight line, so three collinear inputs that come out bent
rule out every affine map at once rather than failing to find one. That is why
the field could swap the logistic for ReLU for GELU without rewriting the
theory. → **P06**.

### Tensors, shapes and index notation, written (P07)

Items 112 to 118 came out of writing P07. The curriculum review called this the
largest content gap in the book and in every book in its own survey; the
catalogue had **nothing** on shapes before this pass, which is the same finding
arriving from a second direction.

**112. "It is a three-dimensional array, so I am reasoning in three
dimensions."** Three things in that sentence are called a dimension and they
answer different questions. For a shape of (32, 128, 768): the number of axes
is 3, the length of an axis is 32, 128 or 768 depending which, and the
dimension of the space a stored vector lives in is 768 — a fact about one axis
rather than about the array. A picture makes it worse, because a picture of
three axes is a picture of three directions and it is not that. An axis is a
position in the index tuple. → **P07**, naming the collision with **P04**'s
dimension.

**113. "Rank is rank."** An array's rank is how many axes it has. A matrix's
rank is how many independent directions it maps onto, which is a statement
about what it *does*. A rank-3 array says nothing about either, and neither
reading implies the other. Two programs apart is close enough to collide and
far enough to forget. → **P07** and **P08**, which is why P07 writes *number of
axes* wherever there is doubt.

**114. "A shape mismatch would have raised an error."** Predictions of shape
(n,) minus targets of shape (n,1) broadcast to (n,n) — every prediction against
every target — and the mean of n² numbers is still a number, so the training
loop is content. The excess is **exact**: the reported loss is the true loss
plus 2·Cov(p, t). Two consequences make this the worst shape a bug can have.
The error *grows* as the model improves, because a covariance is precisely what
training increases; and at a perfect fit the reported loss is 2·Var(t) and
cannot fall below it. Measured, the reported number is 1.8 times the true one
at a poor fit and 286 times at a good one. What the engineer sees is a loss
that falls, plateaus at a number nobody can account for, and stays there — read
as a model that has stopped learning, and in fact a missing `keepdims`.
→ **P07**.

**115. "Adding the bias worked, so the axes lined up."** A (3) added to a (3,3)
goes along each *row*; adding it down each *column* needs (3,1). Both are legal,
both run, and only one is what was meant. Broadcasting aligns from the right and
pads the shorter shape with 1s in front, so the shape is the whole of the
instruction and (3) and (3,1) are different instructions. → **P07**.

**116. "A repeated index is summed."** That is the rule for the *summation
convention*, where there is no arrow and nothing else it could mean. In an
`einsum` string the arrow makes it optional: a repeated index that also appears
on the right is a **batch** index. `'bij,bjk->bik'` sums only over j.
Getting it backwards is not an error — `'bij,bjk->ik'` runs, returns the right
shape for a single example, and has added together results belonging to
different members of the batch. → **P07**.

**117. "Same shape, so same array."** `x.reshape(b, s, h, d).transpose(1, 2)`
and `x.reshape(b, h, s, d)` both produce (b, h, s, d) and differ in 100 of 120
entries on a small case. Only the first splits heads correctly, because the
buffer runs with d fastest, then h, then s. This is exactly where **P06**'s
guarantee stops: P06 made a shape a type signature and a shape error a type
error, and these two really do have the same type. What differs is which index
means what, and that is carried in the names you used and nowhere a machine can
read it. The rule that decides it: a reshape is safe exactly where the axes
being split or merged are adjacent and already in the buffer's order.
→ **P07**.

**118. "Reshape is cheap and transpose is expensive."** Wrong twice over.
Reshape leaves the buffer alone and changes the shape; transpose leaves the
buffer alone and changes the *rule* for turning an index tuple into a position.
Neither moves a number. What moves data is asking for the result **contiguous**,
which is a third operation with its own name, and it is usually the copy nobody
wrote down that gets attributed to the transpose. → **P07**, with the cost
itself belonging to **P03**.

### Rank, the four subspaces and least squares, written (P08)

Items 119 to 125 came out of writing P08.

**119. "Rank plus nullity is the size of the matrix."** It is the number of
**columns**, and only that: every input either survives into the column space or
is sent to zero, and the output side is not being counted at all. The
consequence is the useful half — a matrix wider than it is tall **must** discard
something, and one taller than it is wide **cannot** reach everything — and both
are readable off the shape before a single entry is chosen. → **P08**.

**120. "The bottleneck compresses because training learned to."** It compresses
because the shape forces it to. A layer narrower than the one before it is a
wide matrix, a wide matrix has a null space it cannot avoid having, and training
only chooses *which* directions get discarded. The same sentence covers an
autoencoder's code, a projection head and an adapter's down-projection:
**choosing a width is choosing how much to throw away**, and the amount is fixed
before the weights exist. → **P08**.

**121. "Full rank means every right-hand side is solvable."** Full rank on a
tall matrix means nothing is lost on the way in, not that everything is
reachable on the way out. A $9 \times 4$ matrix of rank 4 has a four-dimensional
column space inside a space of nine, so almost every $b$ lies outside it and
$Ax = b$ has no solution — which is the ordinary situation in every fitting
problem, not a pathology. → **P08**.

**122. "There is no solution, so I will solve it approximately."** The move is
sharper than that and it is a change of question, not a relaxation of one. There
is an exact test that never attempts a solution: **a right-hand side that raises
the rank when added as a column is one the columns cannot build.** And the
replacement question — the closest point of the column space — has an exact
answer characterised by a property rather than by an optimisation: the residual
is orthogonal to every column of $A$. That is all least squares is, and it is
**P05**'s projection with a subspace swapped in for the line. → **P08**.

**123. "A small residual means the model is right; orthogonality means it
fits."** Backwards on both. Orthogonality says the fit is the best one
*available*, which is a statement about optimality and not about quality; the
size of the residual is the separate question and is the one worth reporting. A
large residual that is orthogonal to every column says the relationship is not a
combination of the features you supplied, and **the fit can only ever land in
the column space** — so it will show in the residual rather than in the
coefficients. → **P08**.

**124. "A low-rank adapter is free."** It costs $2dr$ against $d^{2}$, so the
ratio is $2r/d$ and depends on nothing about the model — at $d = 4096$ and
$r = 8$, 0.39%. Two things get lost in the enthusiasm. **The saving stops at
$r = d/2$**, above which the adapter costs more than the dense update while
still constraining it. And the constraint is an **assumption**: that the change
the task needs lies in a few directions rather than being spread over all $d$.
Every parameter not stored is a matrix not reachable — the refusal *is* the
saving. Testing the assumption needs singular values and belongs to **P11**;
**P08** states it.

**125. "A later layer can learn to undo the bottleneck."** This is the one place
where more capacity provably does not help. A product cannot have more rank than
either factor, so a rank-$r$ map caps everything after it however deep the stack
gets: two inputs sent to the same place arrive at every later layer as one
vector, and a function cannot return two answers for one argument. **Rank is
lost forwards only.** Note the contrast with **P06**'s collapse, which is the
mirror image — there depth without a non-linearity was *waste* and had a fix;
here a narrow layer is *loss* and has none. And note what this does **not**
establish: rank collapse in deep attention stacks is a claim about what training
and the softmax do to a stack with no narrow layer in it, which is a different
statement, is architecture-dependent, and is not measured in this book.
→ **P08**.

### SVD, low-rank approximation and conditioning, written (P11)

Items 138 to 143 came out of writing P11. Item 15 above is this program's as
well, and is delivered rather than warned about.

**138. "This matrix has no eigenvalues, so there is nothing to decompose."** A
rectangular matrix cannot have an eigenvector at all — $Av$ and $v$ live in
spaces of different sizes, so $Av = \lambda v$ is not a statement that can be
made. It still has a full singular value decomposition, with as many singular
values as its smaller dimension. The whole of the eigenvalue apparatus applies
to square matrices and most of the matrices in a network are not square, which
is the reason the SVD is the one worth knowing. → **P11**.

**139. "The truncated SVD is a good rank-$r$ approximation."** It is **the
best one there is** — Eckart–Young, quantified over every matrix of that rank.
The weaker version is what most people carry away, and the difference matters
in a design review: *good* invites somebody to look for a better one, and there
is not one. → **P11**.

**140. "This matrix is huge, so a low-rank approximation will help."** The
condition is that the singular values **decay**, not that the matrix is large.
A spectrum of $(100, 99, 98, 97)$ keeps about a quarter of its content at rank
one; $(100, 3, 2, 1)$ keeps over 99 per cent. Size does not appear in the
argument anywhere. → **P11**.

**141. "The condition number tells me something is wrong."** It is a fact about
the problem, not about the algorithm and not a bug report: a perfect method on
a badly conditioned problem still returns a poor answer, because the answer
really is that sensitive to the input. It is closer to a weather forecast — the
honest response is to budget for the $\log_{10}\kappa$ digits it will cost
rather than to hunt for the mistake that caused it. Program P10's ravine had a
large condition number by design. → **P11**.

**142. "The determinant is small, so the matrix is nearly singular"** — item 127
above, now with the instrument that answers it properly. Scaling a matrix by
1000 multiplies every singular value by 1000, moves the determinant by $1000^n$,
and **leaves the condition number and the digits lost exactly where they were**,
because $\kappa$ is a ratio. That is why $\kappa$ is the honest measure of
*nearly singular* and $\det$ is not. → **P11**, and → **P09** for the trap it
completes.

**143. "The closed form is `inv(A.T @ A) @ A.T @ b`, so that is what I write."**
Forming $A^{\mathsf{T}}A$ **squares** the condition number, so it doubles the
digits lost. Measured: a degree-8 fit through 24 points solved both ways, the
factorisation clearing $10^{-10}$ and the normal equations failing $10^{-6}$ —
at least four decimal digits given away. And nothing raises: the coefficients
that come back have the right signs and magnitudes and are wrong from the sixth
significant figure. **A defect that looks like an answer is worse than one that
looks like a crash.** → **P11**, with the operation count owned by **P09**.

### Eigenvalues, quadratic forms and positive definiteness, written (P10)

Items 132 to 137 came out of writing P10. Item 14 above is this program's as
well, and is elicited rather than warned about.

**132. "A matrix has as many independent eigenvectors as it has eigenvalues."**
An eigenvalue can arrive twice and bring only one direction with it. The shear
with rows $(1,1)$ and $(0,1)$ has trace 2 and determinant 1, so
$(\lambda-1)^2$ and the only eigenvalue is 1 — and only the horizontal survives.
A matrix like that is **defective** and has no basis of eigenvectors at all,
which matters because almost everything done with eigenvectors starts by
writing a vector in terms of them. → **P10**.

**133. "Every real matrix has real eigenvalues."** A quarter turn has none: its
characteristic equation is $\lambda^2 + 1 = 0$. Nothing in the plane survives a
right-angle turn, so there is no direction for a real eigenvalue to describe.
What it has instead is a complex pair, and a complex eigenvalue is the algebra's
way of saying *this map rotates* rather than a sign that something has gone
wrong. Worth knowing chiefly so that a complex number in a library's output is
not read as an error. → **P10**.

**134. "The basin has a curvature ratio of 100, so it is 100 times longer than
it is wide."** It is 10 times. The half-axis of a level set along an eigenvector
goes as $1/\sqrt{\lambda}$, because the form carries the coordinate *squared*,
so the ratio of the axes is the **square root** of the ratio of the eigenvalues.
Measured in P10: eigenvalues 20 and 1 give an ellipse 4.47 times longer than
wide. The square root is a large correction in the reassuring direction, and it
is why a basin with a hundredfold spread in curvature still looks merely oval.
→ **P10**, with the step-size consequence handed to **P17**.

**135. "I tried a thousand directions and the form was positive in all of them,
so it is positive definite."** A semi-definite form's flat direction is *one*
direction out of infinitely many, and no amount of sampling will land on it.
This one is recorded because the script's own assertion made the mistake first:
`min over 720 directions == 0` failed immediately, and the honest replacement is
sampling for non-negativity plus an exact evaluation at the eigenvector. **You
cannot find a flat direction by looking for it**, which is the argument for
computing eigenvectors at all. → **P10**.

**136. "Positive semi-definite is basically positive definite."** The word
*semi* carries the whole difference: a positive definite matrix is invertible,
because none of its eigenvalues is zero, and a positive semi-definite one need
not be. A covariance matrix is only guaranteed the weaker one, which is why a
covariance can be singular and a routine that inverts one can fail on real
data. → **P10**.

**137. "The spectral norm is about how big the entries are."** It is the
largest $|\lambda|$, and it is the factor by which a layer can amplify a
vector's length **in the worst case over every input, including the ones nobody
has tried** — the Lipschitz constant. Entries and eigenvalues are not the same
size in general, which is the whole reason the norm has to be computed rather
than eyeballed. → **P10**, and → **P11** for the non-symmetric case, where the
number wanted is the largest singular value rather than the largest eigenvalue.

### Determinant, inverse and change of basis, written (P09)

Items 126 to 131 came out of writing P09.

**126. "The determinant is the area, so take the absolute value."** That throws
away the half of it that matters. $|\det A|$ is the area; $\det A$ is the area
**and the orientation**, and a negative determinant is a different kind of map
rather than a smaller one. The checkable consequence: no product of rotations is
ever a mirror, because every rotation has determinant $+1$ and a product of
$+1$s is $+1$. → **P09**.

**127. "A small determinant means the matrix is nearly singular."** The
determinant scales like the $n$th power of the matrix, so in any dimension worth
caring about its size is dominated by scaling. Multiply a $100 \times 100$
matrix by $0.1$ and the determinant falls to $10^{-100}$ while nothing about the
map got worse — same rank, same directions, same behaviour under a solver. *Is
anything destroyed* is the determinant's question and it answers exactly, in yes
and no; *how nearly* is the condition number's, → **P11**. Reading the first as
an approximate answer to the second is how an engineer ends up chasing a number
that was never about what they thought. → **P09**, **P11**.

**128. "Determinant 1 means it is a rotation."** Two independent conditions,
each with a counterexample against the other. A shear has determinant $1$ and
stretches almost every vector it touches; a reflection has determinant $-1$ and
preserves every length there is. What makes a rotation is $R^{\mathsf{T}}R = I$
**and** $\det R = 1$ — the first for lengths, the second for orientation — and
dropping either gives a different family. The first alone is the orthogonal
matrices, which include the reflections. → **P09**.

**129. "`inv(A)` is how you solve `Ax = b`."** Two separable claims and the
weaker one is the one people quote. On operation count, measured rather than
quoted: at $n = 50$, elimination costs 45 375 multiplications and divisions
against 252 100 for forming the inverse and multiplying, a factor of 5.6 for
exactly the same answer — because elimination builds $n$ numbers and the inverse
builds $n^2$ of which you use $n$. The stronger claim is accuracy, and it is
**P11**'s. The line to recognise is `inv(A.T @ A) @ A.T @ b`, which appears in a
great deal of working code because it is the formula as written on the page —
and a formula is a description of the answer, not an instruction for computing
it. → **P09**, **P11**.

**130. "Many right-hand sides, so form the inverse once."** The case exists and
is narrower than it looks: a *factorisation* of $A$ is also formed once, each
later solve is two triangular substitutions of the same order of cost, and the
answers are more accurate. The inverse wins on neither count, so the reasoning
that reaches for it has skipped the alternative rather than compared with it.
→ **P09**, **P11**.

**131. "Adding position by rotation must cost the model something."** It costs
nothing, and the reason needs a determinant, which is why Program F08 could not
say it. A rotation is an *orthogonal change of basis*: invertible, determinant
$1$, transpose equal to inverse, so every length and every angle survives. The
position is added by **re-describing** the query and the key rather than by
altering them, and no direction of the embedding is spent on carrying it.
→ **P09**, and **F08** for the identity underneath.

**Selection note.** The list is numbered above and the count is deliberately not
restated here, because it was stated and it decayed. What the brief asked for
was at least twenty. Items 4, 8, 17, 22, 25, 27, 28, 34, 35, 37 are the strongest — each is
documented outside this book, each has a cheap in-frame demonstration, and each
has cost somebody real money. Falsifier 4 in §2.3 is the honest way to rank the
rest: **count how often each actually occurs before deciding which get a frame.**
Until that runs, the ordering above is judgement.

---

## 4. What an AI engineer can safely not learn

The test applied to every exclusion: *would not knowing this cause you to ship a
wrong number, misread a paper you must read, or fail to debug a real failure?*
If no to all three, it is out. This is the same discipline as Boyd's VMLS, which
omits eigenvalues, determinants and the SVD entirely and is a better book for it.

Exclusion here means **not taught and not tested**. Where a term will appear in
papers, the glossary (Appendix D) defines it so the reader is not blocked; that
is cheaper than a program by two orders of magnitude.

### 4.1 Out, with the defence

| Excluded | Why it is safe | What replaces it |
|---|---|---|
| **ε–δ limits, Cauchy sequences, completeness, real analysis** | You will never write a proof, and no framework behaviour depends on it. What you *do* need is that a limit is a claim about a process, which fits in one frame. | F11 defines the derivative as a limit informally and moves on. |
| **Measure theory, σ-algebras, Lebesgue integration** | Reviewers criticise Goodfellow for including it at this level. Nothing you build distinguishes Riemann from Lebesgue. | P22 works with densities and sums directly. |
| **Cayley–Hamilton, characteristic polynomials, Jordan normal form** | Stroud teaches this and it is the clearest example of his linear algebra being recipe-level rather than useful. Nothing in ML computes eigenvalues from a characteristic polynomial — LAPACK does not. | P09 does eigenvalues as invariant directions; P10 does SVD, which is what you actually use. |
| **Hand computation of determinants beyond 3×3, cofactor expansion, Cramer's rule** | O(n!) and never used. The determinant matters as a *volume scale factor* (normalising flows, change of variables) and as log-det, not as an arithmetic exercise. | P08 teaches what a determinant means; the arithmetic is one worked 3×3 and then `slogdet`. |
| **Hand computation of matrix decompositions at scale** (Gram–Schmidt on a 6×6, hand QR, hand SVD) | You must know what QR and SVD *produce* and when they fail. You will never compute one. | P07/P10: one small worked example for mechanism, then properties and failure modes. |
| **Integration techniques: partial fractions, trigonometric substitution, integration by parts drills** | Nothing in a training loop integrates symbolically. Integrals appear as expectations and are estimated by sampling. | F13 and P24: the integral as an accumulated total, then Monte Carlo. |
| **ODEs and PDEs as a solution-technique curriculum** | Genuine exception: diffusion models, neural ODEs, and continuous normalising flows. But those readers need SDEs specifically, not the classical solution zoo. | Named as out of scope in the introduction, with a pointer. |
| **Complex analysis, contour integration, residues** | Complex numbers appear in FFT-based methods and in rotary position embeddings, where all you need is e^{iθ} as a rotation. | F08 covers e^{iθ} as rotation; that is the whole requirement. |
| **Abstract algebra: groups, rings, fields** | Real for geometric deep learning and for cryptography-adjacent work. Not for the target reader. | Out. Named as out. |
| **The classical hypothesis-test zoo: t-test tables, χ², ANOVA, F-tests** | You have a computer. Bootstrap and permutation tests answer the same questions with fewer assumptions, are harder to misapply, and generalise to statistics with no closed form — which is most of the ones you care about. | P26 teaches bootstrap and permutation first; the classical tests get a table showing which resampling procedure replaces which. |
| **Frequentist estimator theory: sufficiency, Cramér–Rao, UMVU** | Beautiful and inert for this reader. | P25 does maximum likelihood as an objective, which is the part that shows up in every loss function. |
| **PAC learning, VC dimension, Rademacher complexity** | The bounds are real theorems and are numerically vacuous for over-parameterised networks — they permit error rates above 1. Knowing they exist is worth a paragraph; deriving them is worth nothing here. | One frame in P33 on why generalisation bounds do not predict your validation loss. |
| **Convergence-rate proofs in convex optimisation** | Deep learning objectives are outside the hypotheses. Knowing convexity as a *recognition problem* transfers; the rate proofs do not. | P18 teaches recognition and Jensen; P19–P20 teach what actually runs. |
| **Numerical quadrature, spline theory, classical interpolation** | Superseded by sampling for the uses in scope. | Out. |

### 4.2 The exclusions this book is least sure about

Stating these is cheaper than defending them later.

- **Convex optimisation theory.** Excluded on the grounds that DL is non-convex.
  Counter-argument: quantisation, calibration, LP/QP-shaped serving and routing
  problems, and constrained decoding *are* convex, and an engineer who cannot
  recognise one solves it with a for-loop. P18 and P21 keep the recognition
  skill for this reason. If readers report needing more, this is the first
  exclusion to revisit.
- **Discrete maths depth.** P11–P13 fix Stroud's total omission, but stop well
  short of algorithms and complexity. Defensible only because the reader is a
  software engineer who has met graphs before — an assumption the book makes
  nowhere else, and should state.
- **Causal inference.** Excluded entirely. Increasingly wrong as evaluation and
  A/B analysis become part of the job. Flag as a candidate for a second edition
  rather than pretending it does not belong.
- **SDEs / diffusion.** Excluded above. This is a defensible line in 2026 and may
  not be in 2028.

### 4.3 What is emphatically *in*, against the tradition

Stated because the TOC will otherwise look eccentric next to §1:

- **Floating point as a first-class subject (P01–P03).** No maths-for-ML book
  has a part on this. Goodfellow has one chapter. It is where the money goes.
- **Orders of magnitude and cost (P03).** Estimating FLOPs, memory, and spend
  before running anything is a mathematical skill and nobody teaches it.
- **Discrete structures (P11–P13).** Stroud has none; tokenisation, beam search,
  attention masks, DAG-shaped computation graphs and dependency scheduling are
  all discrete.
- **Inference and Bayes (P26–P27).** Stroud stops at the normal distribution.
  Deciding whether an eval improvement is real is the most common mathematical
  act in the job.
- **Honest measurement (P33).** The house convention as a program: methods,
  distributions rather than best runs, and the discipline of leaving a table
  empty.

---

## 5. Consequences for the TOC as it stands

The TOC in `structure.tex` survives this grounding largely intact. Specific
findings:

1. **F01–F13 are the differentiator, not the throat-clearing.** Every book in §1
   assumes what they teach. Falsifier 1 in §2.3 is the experiment that decides
   whether they earn their pages, and it is cheap. Run it first.
2. **P01–P03 have no competitor.** This is the sharpest positioning in the book
   and the introduction should lead with it, crediting Goodfellow ch. 4 as the
   only precedent.
3. **P05 needs the concentration-of-distance material** from Blum–Hopcroft–Kannan
   and Beyer et al., translated out of theorem form — plus the Steck cosine
   result, which is recent enough that no textbook has it.
4. **P26 should teach resampling before the classical tests**, per §4.1, and
   should carry items 27, 28, 31 and 33 as trap frames. This is the program most
   likely to change what a reader does on Monday.
5. **P31 (transformer derived) should be a payoff program, not a new-material
   program** — every piece assembled there (softmax stability from P02, the
   variance argument for 1/√d_k from P23, cross-entropy from P29) must already
   have been taught. If P31 needs to teach something, that thing is in the wrong
   place.
6. **Register measurement debt now.** Five experiments in §2.3, all unrun,
   reported by `make debt`, with Appendix B's tables empty until they are run.
   The same rule as the other two books: do not fill them with plausible numbers.
7. **The 80/80 standard should be a stated, counted obligation**, not a homage.
   Stroud validated to it and said so; a book that borrows the format and not the
   validation has borrowed the least valuable half.

---

## Sources

Competitive survey:
- Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* — https://mml-book.github.io/ ; https://www.cambridge.org/highereducation/books/mathematics-for-machine-learning/5EE57FD1CFB23E6EB11E130309C7EF98
- Strang, *Linear Algebra and Learning from Data*: MAA review https://old.maa.org/press/maa-reviews/linear-algebra-and-learning-from-data ; https://math.mit.edu/~gs/learningfromdata/ ; insideAI News review https://insideainews.com/2020/06/11/book-review-linear-algebra-and-learning-from-data-by-gilbert-strang/
- Boyd & Vandenberghe, VMLS — http://vmls-book.stanford.edu/ ; https://web.stanford.edu/~boyd/vmls/vmls.pdf
- Boyd & Vandenberghe, *Convex Optimization* — https://stanford.edu/~boyd/cvxbook/
- Goodfellow et al., *Deep Learning*: Springer review https://link.springer.com/article/10.1007/s10710-017-9314-z
- Bishop & Bishop, *Deep Learning: Foundations and Concepts* — https://link.springer.com/content/pdf/10.1007/978-3-031-45468-4.pdf ; review https://www.tandfonline.com/doi/full/10.1080/14697688.2024.2436137
- Murphy, *Probabilistic Machine Learning* — https://mitpressbookstore.mit.edu/book/9780262046824
- Blum, Hopcroft & Kannan, *Foundations of Data Science* — https://www.cs.cornell.edu/jeh/book.pdf ; https://www.cambridge.org/core/books/foundations-of-data-science/6A43CE830DE83BED6CC5171E62B0AA9E
- 3Blue1Brown / Sanderson on the illusion of understanding — https://www.dwarkesh.com/p/grant-sanderson ; https://en.wikipedia.org/wiki/3Blue1Brown
- fast.ai — https://course.fast.ai/ ; https://www.fast.ai/posts/2022-07-21-dl-coders-22.html
- Stroud, *Engineering Mathematics* (80/80 validation, Lanchester College) — https://archive.org/details/engineeringmathe0004stro ; https://en.wikipedia.org/wiki/Ken_Stroud

Pedagogy:
- Roediger & Karpicke, testing effect — https://files.eric.ed.gov/fulltext/ED599273.pdf ; https://www.sciencedirect.com/science/article/abs/pii/S0959475217301810
- Pretesting / errorful generation — https://pubmed.ncbi.nlm.nih.gov/19751074/ ; https://link.springer.com/article/10.3758/s13423-021-02022-8 ; https://journalofcognition.org/articles/10.5334/joc.455 ; Metcalfe, *Learning from Errors* https://www.annualreviews.org/content/journals/10.1146/annurev-psych-010416-044022
- Programmed instruction, adverse evidence (Kulik et al. 1982) — https://www.tandfonline.com/doi/full/10.1080/2331186X.2023.2189889 ; https://edtechbooks.org/lidtfoundations/programmed_instruction ; https://adaptivelearninginelt.wordpress.com/2020/02/20/the-unlearned-lessons-of-programmed-learning/

Misconceptions:
- Greenland et al., 25 misinterpretations of P values — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4877414/
- Beyer et al. / Aggarwal et al., distance concentration — https://www.sciencedirect.com/science/article/pii/S0885064X09000260 ; https://arxiv.org/pdf/0906.0684
- Steck, Ekanadham & Kallus, cosine similarity — https://arxiv.org/abs/2403.05440 ; https://research.netflix.com/publication/is-cosine-similarity-of-embeddings-really-about-similarity
- Loshchilov & Hutter, decoupled weight decay (AdamW) — https://arxiv.org/pdf/1711.05101 ; https://openreview.net/pdf?id=Bkg6RiCqY7
- Gradient accumulation loss-normalisation bug — https://unsloth.ai/blog/gradient
- Vaswani et al., 1/√d_k rationale — https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf
- PyTorch BCEWithLogitsLoss / log-sum-exp — https://docs.pytorch.org/docs/2.13/generated/torch.nn.BCEWithLogitsLoss.html
- Dumoulin & Visin, convolution arithmetic — https://arxiv.org/pdf/1603.07285 ; https://github.com/vdumoulin/conv_arithmetic
- bfloat16 vs float16, loss scaling — https://www.tensorflow.org/guide/mixed_precision ; https://docs.fast.ai/callback.fp16.html
- Accuracy paradox / base rates — https://en.wikipedia.org/wiki/Accuracy_paradox ; https://arxiv.org/pdf/2010.09470

**144. "Pick three of ten --- that's 120."** It is 120, 220, 720 or 1000, and
the question does not say which. Two questions decide it and neither is
usually asked: does the **order** matter, and may anything **repeat**? The
same ten things taken three at a time span a factor of more than eight
depending on the answers, and "pick three of ten" sounds in ordinary speech
like a complete instruction. → **P12**.

**145. "C(20,3) is much smaller than C(20,17)."** They are equal, both 1140.
Choosing which three to keep *is* choosing which seventeen to drop, so there
is one act and two descriptions of it. The reason almost everyone says the
smaller one is easier is that naming three things is quicker than naming
seventeen --- a fact about writing them down, not about how many there are.
→ **P12**.

**146. "Three sets of 1000, 1200 and 850 hold 3050 examples."** They hold
2500. The two-set correction is the one people have; the third term is the one
they drop. It is a *plus* because subtracting the three pairwise overlaps
removes the triple region three times after it was counted three times, so it
has been removed altogether and must come back once. → **F10** for two sets,
**P12** for three and the alternating sign.

**147. "Inclusion--exclusion is how you size a union of many sets."** It has
one term per non-empty subset, so 2^n − 1 of them: 7 for three sets and 1023
for ten, each an intersection that is itself a computation. That is exactly
the enumeration the rule was meant to avoid, which is why past three sets the
answer is to build the union and take its size. → **P12**.

**148. "A 64-bit hash has 1.8e19 values and I have a billion documents, so a
collision is one in eighteen billion."** It is about 2.67 per cent --- a
factor of 4.9e8 out --- because the quantity is the number of **pairs**, not
the number of documents, and a billion documents make 5e17 pairs. The rule
that survives: **a hash's safe capacity is about the square root of its number
of values**, so 64 bits holds about 2^32 items and a 64-bit hash is a coin
flip at 5.06e9 documents, which is a corpus that exists. → **P12**, using
**F10**'s pair count.

**149. "The collision probability came out as 0.0, so we are safe."**
`1 - prod(1 - i/N)` in float64 at 128 bits returns *exactly* zero, because
every factor is within one part in 10^33 of one and rounds to 1.0. There is no
exception and no `nan`; the answer looks reasonable and it ends the
conversation. Note also that the same expression at 64 bits with only 100 000
items has **already** lost five significant figures --- a formula does not
stop working at a threshold, it degrades, and the degradation is invisible
until somebody computes the same thing another way. → **P02** for the rule,
**P12** for the instance.

**150. "Widening the beam explores more of the search space."** It doubles a
fraction of 2e-84. Twenty tokens from a 32 000-token vocabulary is a
ninety-digit number of sequences, and a beam of 4 scores 2.56e6 continuations
against it. A wider beam demonstrably helps; the count settles only that
**coverage cannot be why**, so whatever it buys it buys from the ordering the
model imposes on the space. That is a claim about the model, and it is the one
to argue with when somebody proposes doubling the beam. → **P12**.

**151. "The SHAP plot shows feature 3 is the most important."** A Shapley
value is an average over every ordering of the features, which collapses to a
weighted sum over 2^n subsets and no fewer --- 1e6 at twenty features and
1.1e12 at forty, which is 35 years at a millisecond apiece. **So every
implementation you have used is a sampling approximation**, the bars carry a
sampling error that is not usually drawn, and it is largest exactly where the
features interact, which is where the plot is being used to make an argument.
Two runs of the same explainer on one input can reorder the middle of the
ranking. The question to ask is a counting question: how many of the 2^n were
actually evaluated? → **P12**.

**152. "A graph is a picture."** It is two sets: the things, and the pairs of
them that are joined. A drawing is one rendering of that relation and there
are infinitely many; nothing in the definition mentions position, or crossing
lines, or which way is up. The consequence is practical rather than pedantic —
a relation survives being a million vertices wide and a picture does not.
→ **P13**.

**153. "The degrees sum to the number of edges."** Twice it, on an undirected
graph, because every edge is counted once at each of its two ends. On a
directed graph the *out-degrees* sum to |E| exactly — each edge leaves one
vertex — so the two answers differ by a factor of two and which one is right
depends on a word people skip. It is Program P12's double counting in a new
coat, and the immediate consequence is that the number of odd-degree vertices
is even. → **P13**, using **P12**.

**154. "Store the adjacency matrix, it is the definition."** Both the matrix
and the list are encodings of the same relation and neither is more real. At a
million vertices and ten million edges the matrix is 1e12 cells against 2.1e7
slots — a factor of 4.8e4 — and the density is 2e-5, which is what almost
every real graph looks like. **The matrix earns its place by being
multipliable, not by being lookupable**, which is the whole of why it survives
in a subject where it is far too large to store. → **P13**.

**155. "A^k counts the routes from i to j."** It counts *walks*, which may
revisit a vertex. On an undirected graph (A²)ᵢᵢ is the degree of i, counting
"step to a neighbour, step back" — a perfectly good walk of length two and
certainly not a route. Counting **paths**, which do not repeat a vertex, is a
genuinely harder problem that matrix powers do not solve, because "does not
repeat" is a condition on the whole sequence and multiplication combines steps
without knowing what came before them. → **P13**.

**156. "Message passing is like multiplying by the adjacency matrix."** It *is*
one. The sentence "each vertex aggregates from its neighbours" and the
expression AX are the same statement, not an analogy and not an implementation
convenience. Program P06's theorem — a matrix product is a composition — is
what makes the whole of a graph network's forward pass ordinary linear algebra.
→ **P13**.

**157. "More layers, more capacity"** — said of a graph neural network. Depth
there is **reach**, not capacity: k layers apply A k times, so a vertex
aggregates from exactly those within k steps. On a graph of diameter 3 a fourth
layer adds parameters, computation and no new information to any vertex, and
the question "how many layers" has an answer that comes from the graph rather
than from the budget. (The failure mode past that — representations converging
because everything aggregates from everything — is called over-smoothing and
**this book has not measured it**; the reach is a fact about Aᵏ and needs no
experiment, the collapse is a claim about trained networks and would need one.)
→ **P13**.

**158. "The topological order."** There are usually many — four out of 720 for
a six-node graph — and the definite article is what hides the useful fact.
**Every one of them computes the same values**, because each vertex depends
only on its parents and every valid order computes the parents first. That is
exactly why a build system may parallelise, why a scheduler may reorder, and
why a forward pass is deterministic; and it is why a build system, an agent
workflow, a query plan and a neural network are one object rather than four
things that rhyme. → **P13**.

**159. "A dependency cycle makes the build slow."** It makes evaluation
**undefined**. There is no order in which each target follows what it needs, so
there is genuinely nothing for the tool to do and reporting the cycle is the
only correct behaviour. The two ways out are to break the cycle — in a call
graph usually a layering violation — or to unroll it, which is what a recurrent
network is: a cycle in the architecture and a DAG in the computation, and the
reason its memory grows with the number of steps unrolled. → **P13**.

**160. "PageRank is circular: a page is important because important pages link
to it."** A circular *definition* explains a term using itself. This is a
*condition*: PᵀP = p says nothing about what the ranking is and instead demands
that whatever it is, it agrees with itself after one step of the walk. Whether
such a ranking exists is then a real question with a real answer, and the
answer is an eigenvector for eigenvalue 1 — which is Program P10's calculation
under another name. → **P13**.

**161. "The damping factor is a fudge to make the numbers work."** It buys two
things the theorem needs. Every entry of the matrix becomes positive, so no set
of pages can trap the walk, which is what makes the fixed point unique; and
every row sums to one even for a page with no outgoing links, so nothing
drains. Without it a dangling node takes the probability mass to **exactly**
zero — measured over the rationals, gone by the third step — and there is no
stationary distribution at all. The story about a bored surfer motivates it;
those two properties are what it is for. The constant 0.85 is conventional; the
need for damping is not. → **P13**.

### Logic, proof and reading theorems, written (P14)

Items 162 to 169 came out of writing P14.

**162. "The theorem says X, so X applies here."** The commonest misuse of a
result in this field, and it is not misunderstanding the argument — it is
keeping the **conclusion** and dropping a **hypothesis**. The reason is about
people rather than mathematics: a conclusion is quotable, transferable and
short, while a hypothesis is a restriction, is boring, and is usually the
technical clause in the middle of the sentence. So the sentence that travels
is the conclusion, and it travels without the thing that made it true. The
defence is a habit that costs one sentence: *when a result is quoted at you,
ask what it assumed*. → **P14**.

**163. "The training loss is down, so we are overfitting."** Affirming the
consequent: taking *if P then Q*, observing Q, concluding P. The premise may be
perfectly true and the conclusion still does not follow, because a model that
has genuinely learnt the task also has a low training loss. The test is
mechanical — write the claim as *if P then Q*, write down what was observed,
and check which of the two letters it is. If it is Q you have the converse and
you have nothing. → **P14**.

**164. "It has not seen the test set, so the score is trustworthy."** Denying
the antecedent, which is the same mistake as 163 seen from the other side —
indeed ¬P ⇒ ¬Q *is* the converse's contrapositive. It is the more dangerous
half because it reads as reassurance rather than as a claim: it removes one
explanation for a high score and leaves every other one untouched. → **P14**.

**165. "The converse is basically the same thing."** It disagrees in two of the
four rows, so knowing one tells you nothing about the other. What *is* the same
statement is the **contrapositive**, in all four rows — which is why proving it
proves the original, and why proof by contraposition is a method rather than a
trick. The two rewritings look alike on the page and one of them is a different
theorem. → **P14**.

**166. "Neural networks can approximate any function."** The conclusion with
the quantifier and the silence both removed. The theorem is *for every function
and every tolerance, there exists a network*, so the network may depend on both
— and it says nothing about how large it must be, how that size grows, how the
weights are found, whether training finds them, or how much data that takes.
Using it to justify an architecture treats an existence claim as a
construction. A polynomial of high enough degree approximates any continuous
function on a bounded region too, and nobody argues from that. → **P14**.

**167. "The bound holds with 95% probability, so we are 95% covered."** The
confidence is per use. Applied twenty times over independent draws all of them
hold only 35.8% of the time, so more likely than not one of the twenty
statements in that table is false and nothing marks which. It is a coin flip
after fourteen uses, and holding twenty together needs 99.74% each — a failure
probability of 0.26% rather than 5, nearly twenty times tighter. Independence
is usually false as well, since the experiments share data; the union bound,
which needs none, gives 100% here, which is to say no guarantee survives.
Both calculations agree about what to do: tighten the per-use bound. → **P14**.

**168. "It passed on forty consecutive inputs, so it holds."** n² + n + 41 is
prime for every n from 0 to 39 and composite at 40, where it is 41². Any test
suite would have passed it; the claim is false. The honest half matters as
much: **checking every case is a proof, checking many cases is evidence**, and
the difference is not how many but whether any were left. This book uses
enumeration as a proof several times and only ever over domains that are finite
and exhausted — four truth-table rows, 512 relations, 36 pairs. → **P14**.

**169. "A rigour box is where the book gave up."** It is the opposite. A
theorem has three parts — hypotheses, conclusion, quantifiers — and a proof is
none of them, which is why a result can be used correctly without ever seeing
one. A rigour box withholds the argument and supplies all three parts, so a
reader may use the result exactly as if they had seen the proof. What they may
not do is extend it, weaken a hypothesis, or apply it outside its quantifiers,
because those are the moves the argument would have had to justify. → **P14**.

### Functions of several variables and the gradient, written (P15)

Items 170 to 176 came out of writing P15.

**170. "Holding the other inputs still removes them from the answer."** It does
not. ∂f/∂x for f = x²y + 3y is 2xy — the y is still there. The other inputs are
held still *while you differentiate* and then go back to being variables, so a
partial derivative is a function of everything the original was. That is why it
has to be evaluated at a point before it is a number, and why "the derivative"
on its own is not yet an answer to anything. → **P15**.

**171. "The gradient is the slope."** Two different objects wearing one word,
and this book uses both. Programs F06 and F11 say gradient for the slope of a
line — one number, the m in y = mx + c, which is standard British usage and was
right there. P15 says gradient for a vector with one component per input. In one
dimension the vector has one component and that component is the slope, which is
why the collision survives; but "the gradient is large" means different things in
the two senses, and a reader who has only met the first will read the second as a
number. → **P15**.

**172. "Gradient descent moves in the direction of the gradient."** The
*negative* gradient, and this is the commonest sign error in a hand-written
training loop. What makes it survive is that nothing complains: the loop runs,
the numbers stay finite, and the loss climbs — which reads as a bad learning
rate or a bad initialisation far more often than as a missing minus. Measured on
a quadratic, one small step the right way takes the value from 10.50 to 4.08 and
one step the wrong way takes it to 20.12. → **P15**.

**173. "The gradient points at the minimum."** It points at right angles to the
contour you are standing on, which is a *local* statement, where the minimum's
position is a *global* one. The two coincide only when the contours are circles.
On Program P10's own bowl — eigenvalues 20 and 1 — the negative gradient at
(1, 1) is 42.1 degrees away from the direction home, which is nearly half a right
angle rather than a rounding error. → **P15**.

**174. "Steepest descent takes the shortest path."** It takes the locally
steepest one, which in a valley is mostly sideways. Measured over twenty steps
on that bowl: the walk crosses from one side to the other every single step and
travels 6.88 times as far as it actually moves. The mechanism is one line — each
coordinate is multiplied by (1 − ηλ) with its own λ, so the steep direction's
factor is negative and flips sign while the shallow one's is positive and creeps
— and it is Program F11's own recurrence per eigendirection. → **P15** for the
picture, **P17** for what bounds η, **P20** for momentum, which fixes it.

**175. "A zero gradient means a minimum."** F11 said this fails in one dimension;
in more than one there is a shape with no one-dimensional analogue at all — a
point that is a minimum along one direction and a maximum along another, which
P10 named a saddle. Its gradient is the zero vector, so anything that stops when
the gradient vanishes stops there quite happily. → **P15**, with the test in
**P17**.

**176. "A big gradient means you are far from the minimum, or making fast
progress."** Neither follows. The length of the gradient says how steep the
ground is in the steepest direction and says nothing about whether that direction
goes anywhere useful — which is exactly the valley case, where the length is
large, the progress is slow, and both are true at once for the same reason. The
length is a local rate; the distance home is not local. → **P15**.

### Jacobians, the chain rule and automatic differentiation, written (P16)

Items 177 to 184 came out of writing P16.

**177. "The framework computes the Jacobian."** It never does. A network's
Jacobian has one row per output and one column per parameter, which for a real
model is a matrix nobody can store. What is computed is a *product* with it —
`Jv` or `uᵀJ` — and every intermediate in that product is a vector the size of a
layer. "Nobody forms a Jacobian" is not a simplification of what happens; it is
a statement about which brackets are used. → **P16**.

**178. "Reverse mode is faster."** It is faster *for this shape*, and the shape
is the whole reason. Forward mode costs one pass per input and reverse one per
output, so a scalar loss with many parameters makes reverse cheaper by a factor
of the parameter count — and a function with one input and ten thousand outputs
makes it exactly as wasteful in the other direction. Measured exactly over the
rationals: 40 400 multiplications forward against 2 020 reverse for an identical
gradient, with the ratio equal to the input count over four widths. → **P16**.

**179. "Backpropagation is a deep-learning algorithm."** It is the chain rule
evaluated on a DAG, bracketed from the output end. Nothing in the argument for
it mentions networks, layers, losses or gradients descent — only that there are
many inputs and one output. The name is a name for one bracketing of a matrix
product, and Program P06 measured the cost difference between the two
bracketings one program before it had that name. → **P16**.

**180. "Autodiff is numerical differentiation, or symbolic differentiation."**
Neither. It approximates nothing, so it has none of a finite difference's error
floor; and it never builds an expression for the derivative, so it has none of
the blow-up symbolic differentiation of a deep expression would produce. It
evaluates the chain rule on the graph the program actually ran, one edge at a
time, to the same precision as the forward pass. → **P16**.

**181. "The gradient check only agrees to five digits, so the gradient is
wrong."** Five digits is what a correct implementation looks like. A central
difference has an error floor no step size gets under — Program F11 measured
that U-curve — so demanding fifteen digits is demanding that the test be better
than the instrument can be. The finite difference is the *test*, never the
implementation: it costs one evaluation per input, which is forward mode's price
without forward mode's accuracy. → **P16**, resting on **F11**.

**182. "ReLU's gradient at zero is wrong."** There is no gradient at zero to be
wrong about: the one-sided limits are 0 and 1, so the derivative does not exist
and every implementation must *choose*. The number you get back is a convention,
two implementations may disagree while both being defensible, and neither says
so. It rarely matters because hitting exactly zero in floating point is rare —
and a mask, a padded batch, or a layer whose inputs are all zero hits it every
time. → **P16**.

**183. "The loss looks right, so the gradient is right."** The three ways
autodiff silently answers a different question all leave the forward pass exactly
correct. A detached value leaves the loss *identical to the last bit* and simply
drops a term from the gradient; an in-place write leaves the tape a record of a
computation that no longer exists, so the gradient is consistent with a different
problem; and a non-differentiable point returns a convention. Nothing raises in
any of the three, every forward-looking diagnostic agrees with a correct run, and
the only instrument that looks at the derivative directly is a finite-difference
check. → **P16**.

**184. "Gradient checkpointing is a heuristic and √L is a rule of thumb."**
Keeping every k-th activation holds L/k + k of them at once, and the minimum of
that is exactly where its derivative vanishes, at k = √L. At 10 000 layers that
is a checkpoint every 100, 200 activations held instead of 10 000 — a factor of
50 — for exactly two forward passes rather than one, because each segment is
recomputed exactly once. It is a stationary point, not folklore. → **P16**,
paying the arithmetic **P03** named and left.

**185. "The quadratic model is more accurate than the tangent line."** True and
useless. "More accurate" is a fact about whichever *h* you happened to try; what
the Taylor model buys is an **order**, so halving *h* divides the linear error by
about 4 and the quadratic one by about 8 — measured over eight halvings rather
than quoted as two error figures. A claim about one step and a claim about all of
them are different claims, and only the second is checkable. → **P17**.

**186. "The second-order model tells you where the minimum is."** It is local, in
exactly the sense Program P15's gradient was: it describes the surface near the
point and has no opinion about anywhere else. Adding curvature makes the local
description *better*, not *wider*. A model fitted at one point cannot locate a
minimum somewhere it was never evaluated. → **P17**.

**187. "The learning rate was too high" is a judgement.** It is an inequality:
η > 2/λ_max at the point the run was standing on. That follows from a geometric
sequence and nothing about networks — each eigendirection is multiplied by
1 − ηλ every step, so bounded means |1 − ηλ| < 1, which is η < 2/λ. The quantity
on the right is a property of the *loss surface*, not of the optimiser or the
data, so a run can be stable for a thousand steps and then not. → **P17**.

**188. "The step size is set by the model, or by the data."** It is set by the
single fastest-curving direction, and every other direction lives with what it is
given. On Program P10's bowl the steep direction allows η = 0.10 and the shallow
one would allow 2.0 — twenty times larger and irrelevant, because taking it would
blow the other one up. That is the zig-zag Program P15 drew, stated as the
arithmetic underneath it. → **P17**.

**189. "Second-order methods are better, they are just slow."** They are not
merely slow; at this scale the matrix does not exist. A Hessian for 7e9
parameters has 4.9e19 entries — one per *pair* of parameters — and solving with
it is cubic on top of that. The line worth remembering is not a list of methods
but where it falls: anything needing n² storage is out and anything needing n is
in, and the per-parameter scaling several optimisers do is the diagonal idea
under another name. → **P17**.

**190. "Newton's method finds minima."** It finds *stationary points* and does
not distinguish between them: the step divides by the curvature in each
direction, so where a curvature is negative it steps *towards* the saddle. That
is Program F11's "a zero derivative is not a minimum" in many dimensions — and
combined with the counting argument (a minimum needs every one of n eigenvalue
signs positive, while the ways to be a saddle grow with n) it is a real problem
rather than a curiosity. → **P17**.

**191. "This minimum is flatter, so it will generalise better."** Not a claim you
can evaluate until somebody says what *flatter* is measured in. Rescale one
parameter — write w = cu and divide that parameter's input by c — and every
output is identical while the curvature is multiplied by c², exactly. So one
model has two sharpnesses. No quantity built from the raw eigenvalues survives it
either: not the largest, not the trace, not the ratio. This is not exotic — any
elementwise scaling admits the reparameterisation, and normalisation layers make
it a symmetry the architecture has by construction. The book does not adjudicate
the empirical claim; it supplies the filter. → **P17**.

**192. "So the step-size bound is meaningless too, since λ_max rescales."** It
rescales, and it does not matter, because η rescales with it in the opposite
direction and the *step actually taken* is unchanged. That is the difference
between the two uses in one sentence: in the step-size bound the curvature
appears alongside something with the same units and the pair is invariant though
neither member is; in a sharpness claim it is quoted alone. The right question
about a curvature is never *is it big* but *compared with what*. → **P17**.

**193. "The gradient of a scalar loss with respect to a weight matrix is some
shape or other; I'll transpose until it runs."** That works, which is why the
habit survives: with two shapes to try, guessing terminates. It stops working
the moment two dimensions are equal — a square weight matrix, an attention head
with as many keys as queries, a batch size that matches a width — because then
the *wrong* transpose runs too, and you have a program that trains to a loss
that will not fall with nothing in it that raises. The gradient of a scalar has
the shape of the thing it is taken with respect to, in either convention, and
that check is available before the derivative is written down. → **P18**.

**194. "These two accounts of backpropagation disagree; one of them is
wrong."** Probably neither. They are written in the two layout conventions,
which differ by exactly one transpose: numerator layout puts one row per
output, denominator layout is that table transposed. Neither is more correct
and both are common — it is a split between disciplines, not between countries.
What is wrong is mixing them inside one derivation, and it shows up as a shape
error far from where the mixing happened. → **P18**.

**195. "Matrix calculus is a separate subject with its own rules."** It is
bookkeeping plus that convention. Every identity in it is a partial derivative
taken one entry at a time and then arranged: `d(Wx)/dx` is `W` because
`dy_i/dx_j = W_ij`; a weight's gradient is an outer product `g x^T` because the
weight multiplies the input. A table of identities has to be trusted and a
three-line derivation can be checked, which is why the table is the thing to be
suspicious of — especially since it will be written in a convention nobody
stated. → **P18**.

**196. "The softmax has a derivative, so I can multiply by it elementwise."**
Its derivative is a full `n × n` matrix, `diag(p) − p pᵀ`, because every output
shares a denominator with every input: raise one score and every other
probability falls. The cheapest check on any implementation of it is that every
row sums to zero, which is "the probabilities sum to one" differentiated — a
softmax moves probability around and can never make more of it. → **P18**.

**197. "The p − y in the cross-entropy gradient is a happy coincidence."** It
is one cancellation, and the cancellation is the content. Differentiating
`−ln p_c` gives `−1/p_c`; the softmax Jacobian's row carries a factor `p_c`;
the two meet and the reciprocal disappears. Read as an instruction the result
is exactly what you would want: lower every score in proportion to the
probability it holds, raise the true one by the probability it lacks, so the
size of the correction is the size of the mistake. → **P18**.

**198. "Fusing the softmax and the cross-entropy is an optimisation."** It is
cheaper — about 50 001 times fewer operations at a vocabulary of 50 000, and
the Jacobian nobody forms would be 5 GiB — but if that were the whole story you
could keep the two-step route for clarity and pay for it. You cannot, because
the two are not the same function. The two-step route forms `−1/p_c`, and once
a logit falls about 744 below the largest, `p_c` underflows to exactly zero in
float64 and the route divides by zero. The fused route never forms the
reciprocal and returns an ordinary, maximally informative gradient. The rows
where they differ are the rows a run meets *early*, when the model is worst.
That is Program P01's floor and Program P02's sense of "numerically stable" —
not more accurate, but safe on inputs you have not tried. → **P18**.

**199. "A gradient check that fails means the gradient is wrong."** Not if it
fails only on the batches where the model is badly wrong and passes on the
others, and not if it passes for a squared error on the same network. That
pattern is the signature of the previous item: a softmax and a cross-entropy
computed as two operations rather than one. The check is doing its job; what it
found is not in the network. → **P18**, resting on **P16**'s account of what a
finite-difference check can and cannot see.

**200. "Layer normalisation scales each input, so its gradient is a scale."**
The mean and the variance are computed over the whole vector, so every output
depends on every input and the derivative is no more elementwise than the
softmax's. Its gradient carries two correction terms, one from the mean and one
from the variance, and an implementation that applies `1/s` and stops is wrong
in a way that trains anyway — slowly, and for a reason nobody will find in the
loss curve. → **P18**.

**201. "Perplexity is the average of the per-token perplexities."** It is the
exponential of the average loss, and the two are different numbers. Jensen's
inequality says which way: `e^x` is convex, so the average of the exponentials
is always the larger, and a harness with this bug always reports a model as
worse than it is. The belief survives because it is *almost* true — the two
agree exactly when every token costs the same, which is what a test fixture
looks like. → **P19**, spending the demonstration **F04** set up.

**202. "The two perplexity numbers are close enough."** The size of the gap is
`exp(Var/2)` in the per-token losses, so it is a property of the evaluation set
rather than of the code: 1.00 at zero spread, 1.65 at one nat, 7.42 at two,
with the correct number unmoved throughout. Which is the worst possible
behaviour for a bug — it is quietest on the homogeneous fixture it was tested
on and largest on the diverse corpus that was the point of the exercise. → **P19**.

**203. "Convex means easy to optimise."** It means the answer is unique, which
is a different property, and neither implies the other. A convex bowl with a
large condition number is slow (Program P17 measured 47 steps to close 99 per
cent of one direction's gap on one), and non-convex problems are routinely
fast — that is the entire empirical history of deep learning. Convexity is a
statement about *ambiguity*, not about difficulty. → **P19**.

**204. "The loss is convex, so gradient descent will converge."** Convexity is
a property of the *function* and says nothing about the algorithm. A step size
above `2/λ_max` diverges on a convex function exactly as it does on any other.
What convexity promises is conditional: *if* the walk converges to a stationary
point, that point is the global minimum. → **P19**, resting on **P17**.

**205. "Convex functions are smooth."** `|x|` is convex and has a corner. That
matters rather than being a curiosity, because ReLU is exactly that shape on
one side, and a hinge loss is built from the same operation — the objects this
field calls convex are frequently not differentiable, and the chord definition
never asked them to be. → **P19**.

**206. "Non-convex means a landscape of bad local minima you might get stuck
in."** That is the two-dimensional picture carried somewhere it does not
survive. A minimum needs *every* eigenvalue sign positive and a saddle needs
one to differ, so in high dimension a stationary point is overwhelmingly likely
to be a saddle — which has a downhill direction the gradient is too small to
follow quickly, a different problem with different remedies. What this book has
*not* done is measure the loss surface of a trained network; the argument is
about the arithmetic of signs. → **P19**, resting on **P17**'s counting.

**207. "A network's loss is non-convex because of the activation functions."**
It is non-convex before any activation and at any depth, because the loss is a
function of the *weights* and the weights of different layers multiply each
other. Two linear layers give a loss containing `w₂w₁`, and a product of two
variables is a saddle. The non-convexity comes from the thing that makes a
network a network. → **P19**.

**208. "Jensen's inequality is a probability result."** It is the chord
definition of convexity read as an average, and it turns up three times in this
field wearing different clothes: as the perplexity-averaging error, as the ELBO
(`ln E[x] ≥ E[ln x]`, because `ln` is concave and the inequality turns round),
and as the statement that a variance cannot be negative (`E[x²] ≥ (E[x])²`,
which is Jensen for `x²`). Recognising one inequality is cheaper than meeting
three results. → **P19**.

**209. "Every optimiser is a different algorithm."** They are one update —
`w <- w - eta * d` — with a different estimate of `d`, and each addition
repairs a *named* failure of the one before it: the step-size ceiling set by
the steepest direction, then the zig-zag that ceiling causes, then the fact
that one step size has to serve coordinates whose gradients differ by orders of
magnitude. Read as six recipes it is six things to memorise; read as one line
and five arguments it is reconstructable. → **P20**.

**210. "Momentum gives a √κ speedup."** It gives a *rate* that improves like
√κ, which is a different claim, and the gap is not a tuning failure. At the
optimal coefficients the two roots of the iteration coincide, so the decay
carries a factor of `k` and the rate is approached from above; and the walk
first overshoots, because the average has to be built out of gradients before
it is useful. Measured on a quadratic: 14.6× at κ = 1000 against a √κ of 31.6,
and 2.8× at κ = 20 against 4.5. Plain descent's predicted count, by contrast,
is *exact* at every condition number tried. Quote the rate or quote a measured
count; quoting the rate as though it were a count is how a bound becomes
folklore. → **P20**.

**211. "`momentum=0.9` means the same thing in every library."** Two forms are
both in use — `v <- beta v + g` and `v <- beta v + (1-beta) g` — and they point
the same way while differing in length by `1/(1-beta)`, a factor of ten at
0.9. Neither is wrong, because a constant on the step is indistinguishable from
a change of step size. What does not survive is a step size carried across:
measured, rescaling by ten reproduces a 67-step walk exactly, and not rescaling
diverges. Read the line that updates the state, not the name of the argument.
→ **P20**, and **F04** for the average itself.

**212. "Epsilon is a numerical guard, so where it goes doesn't matter."** It
decides what the guard is compared against. Outside the root it is added to
`sqrt(v)`, which has the units of a gradient, so its effect is `eps/|g|`.
Inside, it is added to `v`, a gradient *squared*, so `1e-8` becomes a floor on
`|g|` of `1e-4` — an enormous gradient to treat as noise. Measured at
`|g| = 1e-6`: the step is 0.99 per cent short with the epsilon outside and 99
per cent short with it inside, and the coordinates it silences are exactly the
small-gradient ones the whole mechanism exists to rescue. → **P20**.

**213. "Adam is faster than SGD."** What is provable is not speed but
*invariance*. Writing a parameter as `w = c u` leaves the function a network
computes completely unchanged and multiplies that direction's curvature by
`c²`, so plain descent at the same step size diverges — measured, 95 times past
its own bound at `c = 10` — while Adam takes the same number of steps in both
coordinate systems, because numerator and denominator scale together. Whether
it reaches a better answer on a real surface is an empirical question this book
does not settle. → **P20**, resting on **P17**'s rescaling argument.

**214. "A cosine schedule spends less learning rate than a linear one."** Both
average half the peak over the run, to better than one part in `1e15`, because
both are symmetric about their midpoint. What differs is entirely *where* the
budget is spent: a cosine is still at 0.854 of the peak a quarter of the way
through, where a line is at 0.75, and it gives that back at the end. An
argument for one shape over another has to be about when the step is spent, not
about how much of it there is. → **P20**.

**215. "A warmup is there because the model is fragile early."** It is there
because `sqrt(v)` is an estimate of a coordinate's typical gradient built from
almost no samples, and it sits in a denominator. Measured on a stream whose
gradients vary by a factor of 25, the corrected estimate swings by 17.7× over
the first ten steps and by 1.005× after three hundred. A warmup keeps the step
small exactly while the quantity it is divided by is least trustworthy, which
is a statement about the estimator rather than about the model. → **P20**.

**216. "The gradient is unbiased, so I can trust it."** Unbiased is a statement
about the *ensemble*: average over every batch that could have been drawn and
the answer is exact. It says nothing about the batch in front of you. Measured
on a population of ten with batches of three, all 120 of them: the batch means
average to the population mean exactly over fractions, and they run from −4.0
to 7.33 around a mean of 2.0, with one of them pointing the opposite way. The
two words that go together are *unbiased* and *variance*. → **P21**.

**217. "Sixteen times the batch means sixteen times less noise."** Four times
less. The *variance* of a batch mean falls like `1/B`, so the *spread* — which
is what you see — falls like `1/sqrt(B)`. That square root is the whole of
"diminishing returns on batch size" and it is exact rather than a rule of
thumb: doubling the batch buys a factor of √2 in noise for a factor of 2 in
compute, at every batch size, for ever, with nothing about the model entering
the statement. → **P21**.

**218. "An enormous gradient step means something is wrong."** It means a batch
mean has a spread and this batch was in the tail of it, which is a property the
method has by construction. Nothing is wrong with the model, the data or the
optimiser. The frequency is set by the spread and the batch size and by nothing
else, which is what makes a clipping threshold a decision about a distribution
rather than a constant. → **P21**, with the two clipping operations in **F06**.

**219. "Clipping is a safety net, so a tighter threshold is safer."** A
threshold below the typical gradient size is not a net, it is a redesign: the
optimiser then follows the gradient's *direction* with a length you fixed by
hand and discards its magnitude, on nearly every step. Measured: a threshold at
half the typical size clips 77 per cent of steps and one at four times it clips
1 in 20 000. The question to ask of a threshold is not whether the number looks
reasonable but what fraction of steps it clips — a guess against a measurement,
and the measurement is two lines of logging. → **P21**.

**220. "The linear scaling rule is what you do when you change the batch
size."** It is one of two rules and they hold different things fixed, both
exactly. The update is `eta * ghat`, so its variance is `eta² σ²/B`: scaling
`eta` by `sqrt(k)` leaves that exactly unchanged, and scaling it by `k`
multiplies it by `k` while holding the ground covered per example fixed
instead. Which invariant matters is an empirical question that is not settled,
the reported evidence for the linear rule comes with a warm-up and a ceiling,
and the arithmetic above holds regardless. → **P21**, and it replaces item 24's
framing with the two invariants written out.

**221. "The loss stopped falling around step 4000."** On a smoothed curve it
stopped falling around step `4000 − h`, where `h` is the half-life of the
smoothing. The lag *is* the half-life, by construction: measured, a smoothed
curve crosses the midpoint of a genuine step change 7 steps later at
`beta = 0.9`, whose half-life is 6.58, and the lag does not depend on how large
the change was. Two runs smoothed differently are two different delays, and an
intervention that appears to take effect late gets credited to whatever came
next. Read the raw curve when the question is *when*. → **P21**, on **F04**'s
machinery.

**222. "Both estimators are unbiased, so they are interchangeable."** An
estimator is used a finite number of times, so what decides usability is the
variance. Measured on one problem where both apply, at 40 000 samples: the
reparameterised estimator's variance is 4.0 at *every* dimension, because the
estimator for one component is a function of that component alone; the
score-function estimator's goes from 15.9 at one dimension to 12 705 at a
hundred, and its estimate is still 47 per cent from the true value after all
40 000 samples. That is the fork between a policy-gradient method and a
variational auto-encoder, and it is why the first has a literature about
variance reduction and the second does not. → **P21**.

**223. "A Lagrange multiplier is a bookkeeping variable you eliminate."** It is
a *price*: how much objective you buy per unit of constraint relaxed, with
units of objective divided by constraint. Checked as an equality rather than an
approximation — for a quadratic under a linear constraint, `lambda` equals
`d f*/dc` exactly at every level, over fractions, with no tolerance anywhere
because a central difference is exact for a quadratic. It is the same object a
solver reports beside each constraint and economics calls a shadow price, and
it is usually the most interesting number in the answer. → **P22**.

**224. "The multiplier tells me what relaxing the constraint by one unit is
worth."** It prices the *first* unit. It is a derivative, so it describes an
infinitesimal relaxation; over a whole unit the curvature of the optimal-value
function adds the rest. Measured: relaxing from 3 to 4 gains 4.67 against a
multiplier of 4. Using a multiplier as a price for a large change is the same
error as using a gradient as a step. → **P22**.

**225. "I project onto the constraint set, so my answer satisfies the
constraint and is therefore right."** It satisfies the constraint, which is
half of what *right* means. Projection answers *which feasible point is
nearest*; the multiplier answers *which feasible point is best*, and they are
different questions with different answers — measured, the projection of
`(5, 0)` onto `x + y = 3` has objective value 18 against the constrained
optimum's 6. Projected gradient methods invite the confusion: it is the
*stepping* that finds the optimum and the projection only keeps the iterate
legal. → **P22**, on **P05**'s projection.

**226. "`beta` in a KL-penalised objective is just a hyperparameter."** It is a
multiplier, which makes it a price with units: reward per nat. Measured along
the family of solutions, the slope of expected reward against KL is `beta`
itself, to better than `1e-4`. So — unlike a learning rate — it can be reasoned
about before it is searched, and a `beta` tuned against one reward model does
not transfer to a reward model on a different scale, because the two rewards
are in different units. → **P22**, resting on **P30** for KL itself.

**227. "A hard KL constraint and a KL penalty are different methods."** They
are the same problem parameterised differently. Each `beta` produces exactly
one divergence level and a smaller `beta` always buys more, so choosing a level
determines the multiplier and choosing a multiplier determines the level;
neither is more fundamental, and which one an implementation exposes is a
matter of what is convenient to control. Methods presented as rivals on this
axis are arguing about parameterisation rather than about objectives. →
**P22**.

**228. "The KKT conditions prove my point is optimal."** They make it a
candidate. They are necessary at an optimum only when a constraint
qualification holds, so a point failing them may still be optimal in a badly
behaved feasible set; and they are sufficient only under convexity, which
**P19** says is the property most problems in this field do not have. On a
non-convex problem, satisfying KKT makes a point one candidate among many. →
**P22**.

**229. "A negative multiplier means the constraint is hurting me."** It means
the sign convention is not the one you assumed. For a constraint written
`g <= 0` the multiplier cannot be negative, because relaxing a bound enlarges
the feasible set and a larger set cannot contain a worse best point. Books
differ between `grad f = lambda grad g` and `grad f + lambda grad g = 0`, which
give multipliers of opposite sign for the same problem, so the *magnitude* of a
multiplier is a property of the problem and its sign is a property of how
somebody wrote the constraint. → **P22**.

**230. "The prosecutor said the chance of a match given innocence is one in a
million, so the chance of innocence is one in a million."** The two conditionals
have different denominators, and swapping them is the whole of the prosecutor's
fallacy. In this book's own detector, measured over fractions: `P(alarm |
clean)` is 1.0 per cent and `P(clean | alarm)` is 91.0 per cent — both true, of
the same detector, on the same day. The first is a property of the instrument
and the second is a property of the traffic, and only the first travels when the
instrument is deployed somewhere else. → **P23**.

**231. "These two signals are independent, so I can treat them separately."**
Independence is not a property two events carry around with them; it is a
statement about a particular measure, and conditioning changes the measure. Two
fair coins are independent, and given that exactly one landed heads they are
perfectly dependent — `P(A and B | C) = 0` where the product of the conditionals
is `1/4`. Every filtered dataset, every evaluation restricted to a subgroup and
every "requests that reached the model" is a conditioning, so whatever
independence held before is now a claim about a different space that nobody has
checked. → **P23**.

**232. "All the pairwise correlations are near zero, so the features are
independent."** Pairwise independence does not give independence of the
collection, and no amount of checking pairs will find that out. The same three
coin events are independent in every one of their three pairs and have
`P(A and B and C) = 0` against a product of `1/8`. A table of pairwise
correlations — which is what people actually produce — is structurally incapable
of settling the question it is produced to settle. (Note also **29**: zero
correlation is not independence either, so the table is weak in two directions
at once.) → **P23**.

**233. "We have two independent signals, so the evidence multiplies."** The
likelihood ratios multiply only when the two signals are conditionally
independent *given the truth*, and nothing in either signal tells you whether
they are. Measured: two genuinely independent alarms at likelihood ratio 99 take
a 9.0 per cent posterior to 90.75 per cent, while a second detector keyed on the
same log pattern as the first has likelihood ratio 1 and leaves it at 9.0. That
gap **is** what the independence assumption is worth. Two detectors sharing a
feature, two evaluations sharing prompts, two reviewers who read each other's
comments: each is the duplicate case in different clothes, and each gets
reported as corroboration. → **P23**.

**234. "Our model is 99 per cent accurate."** On an unbalanced population that
is a weighted average with the weights left out, and the weights are the base
rate. Measured on this book's detector: it is correct on 99.0 per cent of
requests, and a model that raises no alarm ever, under any circumstances, scores
99.9 per cent while catching nobody. The accuracy paradox is not a curiosity
about a contrived metric; it is the same base-rate arithmetic as item **28**,
read from the other end. Report the two counts the rate came from — **F10**'s
rule — and it cannot form. → **P23**.

**235. "P(A or B) is P(A) + P(B)."** Only for events that cannot both happen.
The third rule of probability carries that condition and the condition is doing
work: **F10**'s two evaluation sets, of 1000 and 1200 cases sharing 200 out of
2000 distinct, give probabilities of `1/2` and `3/5`, which add to `11/10`. The
tell is an answer above 1, and it is a tell only when the overlap is large
enough to push it there — a small overlap gives a wrong answer that looks
entirely reasonable. → **P23**, on **F10**'s union rule.

**236. "Bayes' theorem is a formula to memorise."** It is one quantity written
two ways and then divided, and the derivation is shorter than the mnemonic. The
useful consequence of knowing that is knowing what may be rebuilt and what may
not: `P(A|B) = P(A and B)/P(B)` is a *definition* with nothing behind it, and
Bayes' theorem is a *theorem* you can reconstruct at a desk in three lines. The
memorised version is the one people write upside down, and the names — prior,
likelihood, evidence, posterior — do not help, because two of them mean
something other than what the English words suggest. → **P23**.
