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
the same seed differ on GPU. → **P01**. Well documented; trivially demonstrable
in three lines of Python.

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
in numerical code. → **P08**.

**14. "Eigenvectors are orthogonal."** Only for symmetric (Hermitian) matrices,
by the spectral theorem. A general square matrix can have non-orthogonal
eigenvectors, complex eigenvalues, or fail to be diagonalisable at all. Attention
matrices, transition matrices and Jacobians are not symmetric. → **P09**.

**15. "Singular values are eigenvalues."** They coincide only for symmetric
positive semi-definite matrices. In general σᵢ(A) = √λᵢ(AᵀA), the singular values
are real and non-negative for *every* matrix including rectangular ones, and the
eigenvalues may not exist over the reals. → **P10**.

**16. "PCA on my feature matrix."** Two silent preconditions. PCA without
*centring* returns a first component pointing at the mean, and PCA without
*scaling* returns components dominated by whichever feature is measured in the
largest units. Neither raises an error. → **P10**.

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

### Optimisation (P18–P21)

**21. "My loss surface has local minima, and that's what training gets stuck
in."** In high dimensions, critical points are overwhelmingly *saddles*, not
local minima: a critical point is a local minimum only if all d Hessian
eigenvalues are positive, which is exponentially unlikely at random. What
training gets stuck near is plateaux around saddles. → **P16, P18**.

**22. "Adam with weight_decay is L2 regularisation."** It is not. L2
regularisation and weight decay are equivalent for plain SGD (up to a learning-
rate rescaling), but Loshchilov and Hutter showed *this is not the case for
adaptive methods such as Adam* — coupling the penalty into the gradient means
the adaptive denominator rescales it, so the effective regularisation strength
becomes a time-varying function of each parameter's gradient history. That is
the whole reason `AdamW` exists. → **P20**. Well documented; ICLR 2019.

**23. "`gamma=0.1` in my scheduler means the learning rate goes to 0.1."** It
multiplies. `StepLR(gamma=0.1)` multiplies the LR by 0.1 at each step boundary,
so three boundaries take 1e-3 to 1e-6, not to 0.1. Cosine, linear-warmup and
exponential schedules are each parameterised differently, and reading one as
another is a routine cause of "the model stopped learning at epoch 30". → **P19**.

**24. "I halved the batch size, so I'll keep the learning rate."** Batch size and
learning rate are coupled: the gradient noise scale changes with batch size, and
the linear-scaling heuristic (scale LR with batch size, with warm-up) exists
precisely because keeping it fixed is wrong. Whether linear or √-scaling is right
is model-dependent and contested — this is one to present as *judgement with a
named disagreement*, not as a rule. → **P20**.

**25. "Gradient accumulation over 4 micro-batches is identical to a 4× batch."**
It is not, if the loss is a mean over a varying number of tokens. In October 2024
this was found to be wrong across most popular LLM trainers: cross-entropy is
normalised by the number of non-ignored tokens, and computing that mean *per
micro-batch* and then summing weights each micro-batch equally regardless of how
many real tokens it contains. A mean of means is not the mean. The denominator
must be computed across the whole accumulated batch. → **P19, P24**. Documented,
recent, and expensive — it silently changed the objective in production training
runs.

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
accuracy paradox). The base rate is not a detail; it dominates. → **P22, P26**.

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
F7, and items 52 to 54 out of F8. Say which program produced which,
never how many there are — the count at the head of §3 was stated once and had
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
