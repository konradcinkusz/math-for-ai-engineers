# Mathematics from Zero for the AI Engineer
### Matematyka od zera dla inżyniera AI

[![Build](https://github.com/konradcinkusz/math-for-ai-engineers/actions/workflows/build.yml/badge.svg)](https://github.com/konradcinkusz/math-for-ai-engineers/actions/workflows/build.yml)
[![Pages](https://img.shields.io/github/deployments/konradcinkusz/math-for-ai-engineers/github-pages?label=docs)](https://konradcinkusz.github.io/math-for-ai-engineers/)
[![Text: CC BY-NC-SA 4.0](https://img.shields.io/badge/text-CC%20BY--NC--SA%204.0-0E7C7B)](LICENSE-CONTENT)
[![Code: MIT](https://img.shields.io/badge/code-MIT-B26A00)](LICENSE)

You can call `softmax` and you cannot say why it subtracts its own maximum
first. You have trained a model and never derived the gradient it was
following. You read a paper, understand every sentence around the equations,
and skip the equations.

This book starts at arithmetic and ends at scaled dot-product attention. It
assumes **nothing** — not algebra, not trigonometry, not calculus — and it uses
K. A. Stroud's programmed-learning format, which means it cannot be read. It has
to be worked.

**It ships in Polish and English, built from one repository.** A check on every
build proves the two editions have the same programs, the same frame numbering
and the same numbers, so a correction applied to one cannot silently miss the
other.

**Read it now — both editions, rebuilt on every push to `main`:**

- **[English edition (PDF)](https://konradcinkusz.github.io/math-for-ai-engineers/book-en.pdf)**
- **[Wydanie polskie (PDF)](https://konradcinkusz.github.io/math-for-ai-engineers/book-pl.pdf)**

> **Early draft.** The structure, the build, the bilingual tooling and
> **Program F1 in both languages** are done. Forty-six of forty-seven programs
> are stubs carrying the brief they must satisfy. Every ledger below is printed
> on every CI build, so the debt is visible rather than quietly carried.

---

## What a program looks like

Each of the forty-seven programs is a stream of numbered **frames**. Nearly every
frame ends by asking you for something, and **the answer is at the top of the
next frame** — so you commit before you check. Over one program that happens
forty to seventy times.

Around the frames sits the same skeleton every time:

| | |
|---|---|
| **Learning outcomes** | What you will be able to do, listed before you start |
| **Quiz** | Foundation programs only. Take it *before*: it tells you whether you need the program, and which frames if you only need part of it |
| **Frames** | The program |
| **Summary** | Every item tagged with the frame it came from, `[17]` — so the summary is also the route back |
| **Can you?** | The outcomes again, one for one, rated 1–5. **Generated from the outcomes**, so the two cannot drift |
| **Test exercises** | Exactly what the program taught. No traps |
| **Further problems** | Consolidation, and more of it than you will want |

And it sets traps on purpose. Where a topic has a standard misconception the
text walks you into it, lets you commit to the wrong answer, then says flatly
that it is wrong and shows you why. [Thirty-eight of them](notes/02-grounding-and-traps.md)
are catalogued, each phrased in the reader's own voice.

---

## What is covered

Nine parts, thirteen Foundation programs and thirty-four main programs.

| Part | Programs |
|---|---|
| **I — Foundation** | Numbers · Algebra · Logarithms · Sums and sequences · Functions · Equations · Exponentials · Trigonometry · Vectors · Sets and counting · The derivative · The chain rule · Accumulation and expectation |
| **II — Number, precision and cost** | Floating point · Numerical stability and log-space · O-notation, FLOPs and memory |
| **III — Linear algebra** | Vector spaces · Inner products and norms · Matrices as maps · **Tensors, shapes and index notation** · Rank and least squares · Determinants · Eigenvalues · SVD and conditioning |
| **IV — Discrete structures** | Combinatorics · Graphs and DAGs · Logic and reading theorems |
| **V — Calculus and autodiff** | The gradient · Jacobians and autodiff · The Hessian · Matrix calculus |
| **VI — Optimisation** | Convexity · SGD to Adam · Stochastic optimisation · Lagrange multipliers |
| **VII — Probability and statistics** | Bayes · Distributions · CLT and Monte Carlo · Maximum likelihood · Inference · Bayesian inference |
| **VIII — Information theory** | Entropy · Cross-entropy and KL · Mutual information |
| **IX — Assembling it** | The transformer, derived · Anatomy of a training run · Measuring a model honestly |

Part II comes **before** the linear algebra, which is a departure from every
mathematics curriculum and is deliberate: everything after it is arithmetic
performed by a finite machine on a budget, and a book that waits four hundred
pages to admit the machine cannot represent `0.1` has spent four hundred pages
teaching a fiction.

The parts Stroud's own volume lacks — real linear algebra with decompositions,
statistical inference and Bayes, information theory, optimisation, and enough
discrete mathematics to reason about an algorithm — are the reason this book
exists rather than a recommendation to read his.

---

## Every number is computed, not remembered

A numeric value lives in a script under `code/`, is written to
`figures/values/`, and reaches the page as `\val{key}`. **The book contains
references, not digits.** `figures/values/` is committed, so a changed number
shows up in review as a diff, and CI fails the build when a script no longer
produces what the book prints.

Program F1 alone pulls in twenty-nine of them. A few, so you can see the shape:

| | |
|---|---|
| `2^10` against `10^3` | 2.40% above |
| `2^80` against `10^24` | **20.89% above** — the same error, compounded eight times |
| 7 billion parameters at 2 bytes | 14 GB, and 13.04 GiB |
| A gibibyte against a gigabyte | 7.37% more bytes |
| "Fifty per cent faster" on 200 ms | 100 ms or 133.3 ms, **33.3 ms apart** |

Ten experiments are specified across the book and **none has been run**. Until
one is, the claim it would support is labelled as judgement and its table stays
empty. Nine of the ten are free and finish on a laptop in under a minute.

---

## Two editions that cannot drift apart

`tools/parity.py` compares an **ordered structural signature** of every file
pair — not counts, because a histogram cannot see `\yourturn` moving from frame
2 to frame 3, and every Summary back-reference navigates by frame number.

It also compares per-frame maths digests (a sign fixed in one edition only
changes no count), every numeric literal in order and **strictly** (the Polish
decimal comma is not normalised away, because a hand-localised number is a
number written twice), the two main files' wiring, and the macro histogram.
`tools/reflist.py` then compares what the cross-references actually *resolved*
to, out of both `.aux` files — because `\label{prog:F08}` can point at F8 in one
edition and F9 in the other while both builds stay internally consistent and
neither warns.

Where Polish and English usage genuinely differ, the difference is a macro
rather than a translator's memory. The governing rule is the **keyboard test**:
*if the reader will type the token, both editions use the code spelling; if they
will only read it, the Polish edition uses the Polish form.* So `tg` for the
tangent and `tanh` — not `tgh` — for the hyperbolic tangent.

A bare `\log` is a **build error**. Polish textbooks read it as base ten and
machine-learning writing reads it as base *e*, and the two collide hardest where
it matters most: entropy in bits and cross-entropy in nats are two programs
apart. Write `\ln` or `\logb{2}`.

---

## The evidence, and the adverse evidence

Stroud's programs were validated above an **80/80** standard before publication
— at least 80% of students scoring at least 80% — and the finding worth having
is that the *spread narrowed*, not that the mean rose.

**This book has not been read by anybody**, so it may not borrow that. Every
build prints it as outstanding.

**And the general evidence for programmed instruction is adverse.** Kulik, Cohen
and Ebeling's 1982 meta-analysis found the format did not typically raise
achievement in secondary education, and that small steps and linear sequencing
were not what mattered. That is in the front matter, in a warning box, rather
than left out.

The defence this book actually makes is narrower: **retrieval practice** and
**errorful generation**. Being made to recall beats rereading at a week;
eliciting a wrong answer and correcting it beats studying without the error, and
the benefit is largest exactly when the reader was confident. The frame and the
trap are for those two findings and nothing else.

One consequence is stated plainly in the front matter and should not be
softened: **the method feels worse than reading while you are doing it.**
Readers rate the method they retain less from as the more effective one.

---

## Building it

```bash
git clone https://github.com/konradcinkusz/math-for-ai-engineers.git
cd math-for-ai-engineers
make          # numbers, diagrams, both editions, then the three gates
```

Requires a TeX distribution with `listings`, `tcolorbox`, `titlesec`,
`microtype`, `siunitx`, `csquotes` and `imakeidx`, plus `babel`'s Polish data
for the Polish edition. Optional font packages are used when present and skipped
when not, so a minimal installation still builds. Diagrams additionally need
Node and a Chromium that `mermaid-cli` can drive; without them the build prints
the Mermaid source in place of the figure rather than failing.

| Command | Does |
|---|---|
| `make` | Everything |
| `make en` / `make pl` | One edition, and check its log properly |
| `make numbers` | Regenerate `figures/values` from `code/` |
| `make verify` | Fail if any committed number has drifted from its script |
| `make check` | `checklog` + `parity` + `reflist`, without rebuilding |
| `make debt` | Every outstanding-work ledger |

**Do not check a build with `grep '^!' main.log`.** With `-file-line-error` an
error line begins with a path, and `-interaction=nonstopmode` writes a PDF over
the top of it, so both the exit code and the PDF say fine. That is not
hypothetical: it hid a broken `\IfFileExists` branch here that stopped `siunitx`
loading, which meant the decimal comma silently did not work in a build
everybody believed was green. Use `tools/checklog.py`.

---

## Repository structure

```
main-en.tex  main-pl.tex   the two editions; they differ in \booklang
preamble.tex               all machinery, shared
structure.tex              THE part and program sequence — one list, both editions
lang/en.tex  lang/pl.tex   every user-visible string, and the notation contract
programs/{en,pl}/          the only place prose is duplicated
appendices/{en,pl}/        A answers · B notation · C formulae · D terms · E reading · F manifest
frontmatter/{en,pl}/       title page · how to use this book · introduction
code/                      the scripts that produce every number in the book
figures/values/            what they produced — committed, so drift shows in review
figures/mermaid/{en,pl}/   diagram source, ASCII, committed
tools/                     parity · reflist · checklog · structure ledgers
notes/                     the design research this book was built from
CLAUDE.md                  working notes: conventions, traps hit, resolved questions
```

---

## Links

- **[The two-minute summary](https://konradcinkusz.github.io/math-for-ai-engineers/)** — and the current PDFs:
  [English](https://konradcinkusz.github.io/math-for-ai-engineers/book-en.pdf) ·
  [polski](https://konradcinkusz.github.io/math-for-ai-engineers/book-pl.pdf)
- **[LangChain, LangGraph and Async Python](https://github.com/konradcinkusz/llm-book)** — companion volume
- **[Microsoft Agent Framework for .NET Engineers](https://github.com/konradcinkusz/maf-book)** — companion volume

---

## Contributing

Errata are the most valuable contribution here, and a wrong digit is the most
valuable erratum of all: in a mathematics book it is not a broken example, it is
something a reader will carry. Include the program and frame number.

If you find a misconception this book should trap and does not, that is the
second most valuable thing — the catalogue is in
[`notes/02-grounding-and-traps.md`](notes/02-grounding-and-traps.md).

---

## Licence

The **prose** is [CC BY-NC-SA 4.0](LICENSE-CONTENT). The **code, LaTeX macros
and build tooling** are [MIT](LICENSE).

The programmed-learning method is K. A. Stroud's, from *Engineering Mathematics*
(1970). This book borrows the method. It is not affiliated with, derived from,
or endorsed by his book or its publisher.
