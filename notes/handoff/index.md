# Hand-off: the Index review (issue #179)

Unit: the Index. Five majors, eleven minors, five nits. Everything below was
read against current source before it was touched; nothing here was fixed on
the review's word alone.

**No build was run and no page-level figure is claimed.** There is no TeX
installation in this container, so every change is source-level and every
LaTeX-level claim below rests on reasoning stated in the comment beside it
rather than on a compiler. CI is the second machine and is the first thing to
read on this branch.

---

## Frames whose length changed

**None.** Every prose edit in this pass inserts, deletes or moves an `\index{}`
mark, which typesets nothing, or rewraps a source line. Three paragraphs gained
or lost a source line break; no frame gained or lost a word.

Two exceptions worth knowing, because both change what sets on the page:

- **The four `see`-references and the one `seealso` add lines to the INDEX**,
  which is back matter and moves no body page. They cannot move a body page —
  an appendix is appended.
- **Two index entries print maths where they printed ASCII**
  (`the $1/\sqrt{d_k}$ divisor` for `the 1/sqrt(d k) scaling`, and three
  siblings). Those set in the index column only.

So the sync session has no cue walk to do on my account. If a cue moves it is
somebody else's edit.

---

## Fixed

### Major — `optimiser / AdamW` named a term the book never prints

Confirmed: `\index{optimiser!AdamW}` at `programs/en/P20-gradient-descent.tex`
line 666 and `programs/pl/P20-gradient-descent.tex` line 636, with `AdamW`
occurring nowhere in either edition's body.

Fixed by the review's second option rather than its first, because the first
asks the program to name a library and P20 declines to on F04's rule. The mark
is now `optimiser!decoupled decay`, on the line that prints *Decoupled decay*
(`Kara odsprzężona` in Polish), and the reader's own word reaches it through
`\index{AdamW|see{optimiser, decoupled decay}}`. A see-reference is the one
form that does not claim a page: it says in as many words that the book calls
this something else.

### Major — index marks parked at a section opener

Confirmed at source, one at a time. Every one was a mark on a `\section`
opener whose section runs several frames before the term it names is printed.
Each has been moved to the line that prints the term, in horizontal mode, so
the page carrying the mark is by construction the page carrying the word.

| entry | was | is |
|---|---|---|
| `matrix!low-rank update` | P08 §opener | the frame that writes `\enquote{low-rank}` |
| `graph!PageRank` | P13 §opener | `That is \textbf{PageRank}` |
| `Jensen's inequality!and the ELBO` | P19 §opener | `That one line is the evidence lower bound` |
| `conjugacy` | P28 §opener, one section AFTER the naming | `That property has a name, \textbf{conjugacy}` |
| `inference!Thompson sampling` | P28 §opener | `The rule has a name, \emph{Thompson sampling}` |
| `inference!calibration` | P28 §opener | the frame that writes `miscalibration` |
| `chain rule!and backpropagation` | F12 program opener AND §opener | the aibox that delivers the sentence |

The P19 mark is the one judgement call. The English prints *evidence lower
bound* in full at the frame I moved it to and the acronym *ELBO* two frames
later; the Polish prints `(ELBO)` at the counterpart line. I put both marks on
the frame that **treats** the object rather than on the later frame that
mentions the acronym in a list, because that is the page a reader wants. It is
a strict improvement on a section opener either way.

`numbers!orders of magnitude` was deleted rather than moved: it sat on the
*scientific notation* section, which does not discuss orders of magnitude at
all. `measurement!orders of magnitude` was deleted too — it sat on the program
opener, which is a promise rather than a treatment, and it duplicated the
`orders of magnitude` head. One head remains, on the section that defines it.

### Major — no cross-references, and no entry for ReLU, SVD, PCA or backpropagation

Confirmed: no `\see`/`\seealso` anywhere, no `ReLU` mark of any kind against
ten programs that use `\relu`, no `PCA` against P10's `\textbf{principal
component analysis}`, no `backpropagation` head against F12's aibox, and SVD
reachable only under its expansion.

- `\index{ReLU}` at F05's definition and at P06's collapse argument.
- `\index{principal component analysis}` + `\index{PCA|see{...}}` at P10.
- `\index{SVD|see{singular value decomposition}}` at P11.
- `\index{KL divergence|see{Kullback--Leibler divergence}}` at P30.
- `\index{backpropagation}` at F12's aibox.
- `\index{gradient|seealso{gradient descent}}` at P15, joining the two routes.

**The `\see`/`\seealso` machinery is new and is the riskiest thing on this
branch.** `preamble.tex` defines both with `\providecommand` and then
`\renewcommand`, deliberately: `imakeidx` may or may not supply `\see` on a
given installation, and where it does it builds the word out of babel's
`\seename`, which this preamble has only when its babel probe found the
language file. The pair is the one form that is the same macro everywhere. The
words themselves are `\lblIndexSee` / `\lblIndexSeeAlso` in `lang/{en,pl}.tex`,
because they are user-visible strings that differ between the editions. Both
macros take two arguments: makeindex passes the page number through the
encapsulation and a see-reference discards it. **Read CI before trusting any
of that.**

### Minor — ASCII pseudo-maths in the index

Confirmed: `the 1/sqrt(d k) scaling`, `the 1/sqrt(n) rate`, `the n-1
correction`, `what its lambda is`, and their Polish twins. Now sort key plus
maths, so the entry sorts where a reader looks and prints what the book
writes: `\index{attention!divisor derived@the $1/\sqrt{d_k}$ divisor, derived}`
and the rest.

### Minor — heads reachable twice under two descriptions

- **The attention divisor**, indexed three ways with two resolving to one page.
  Now two subentries under one name, saying what separates the treatments —
  `the $1/\sqrt{d_k}$ divisor, derived` (P25) and `..., in a block` (P32) —
  which is the distinction the entries did not make and the one that matters.
- **`graph`** merged the graph of a function with graph theory under one head
  whose own page is an adjacency matrix. Split into `graph (of a function)`
  and `graph (vertices and edges)`, **both** qualified, so neither is the
  default. *The Polish edition does not have this defect* — it already writes
  `wykres` and `graf`, so the two objects sort apart on their own, and the
  Polish is untouched.
- **`gradient descent`** was two heads with different pages and nothing joining
  them. One head, `derived` (P15) and `as an optimiser` (P20), with a `seealso`
  from `gradient`.
- **`sample space`** was split, with the head on the later, non-definitional
  page. The head now carries the defining page first: the P23 mark moved to
  `That list is the \textbf{sample space}` and changed from a `probability!`
  subentry to the head. The Polish needed a third change — P24 headed it
  `przestrzeń zdarzeń` where P23 prints `przestrzeń zdarzeń elementarnych`;
  both are the full form now.
- **`estimation`**, a one-line head adjacent to `estimator`, which is a
  different subject. Deleted; `mutual information / estimation bias` on the
  same page carries it.

### Nit — hyphenated heads sorting before their neighbours

`O-notation` and `p-value` have sort keys now. **`cross-entropy` and
`data-processing inequality` deliberately do not**: I checked their actual
neighbours and both already sort where the word-by-word convention would put
them, so a key on either would be a mark to keep consistent forever that
changes nothing. The review's own wording conditions those two on their
neighbours colliding.

### The checker the review asks for — shipped, narrow, proved by mutation

`check_structure.py --index`, wired into `make check`, `make debt` and the CI
`parity:` job.

**The review's version is not implementable and the measurement says so.** It
asks, for every `\index{a!b}` whose leaf is a word, that the word occur on the
page the `.ind` assigns it. Most leaves in this book are *descriptions* rather
than terms — *what it omits*, *as an inverse*, *and the ELBO* — so the naive
form reports most of the book. Measured, by taking each leaf's longest content
word and asking whether it occurs in the file at all: **130 of the 926 marks**,
the Polish far worse than the English because Polish inflects and a stem match
is not available, and almost every one of the 130 is a description doing its
job. That is the permanently red ledger CLAUDE.md refuses.

A **name** is the decidable half, and it is the half both defects fell in. A
capitalised token in an index entry either appears in the file's prose or it
does not; if it does not, the index has named something the reader cannot find.
The check is hard, it exempts see-references by construction, and it learns
`\relu` → `ReLU` from `\DeclareMathOperator` in the preamble rather than
hard-coding it — the way `checkpdf.py` learns the cue string out of
`lang/*.tex`.

Proved by mutation before it was believed: restoring `\index{optimiser!AdamW}`
gives exit 1 naming the file, the line, the entry and the token; a
`PageRank`→`Pagerank` typo gives exit 1; the restored tree gives exit 0 and
`82 names in 926 index entries, every one printed in its own program`.

It found two things the review did not, both in the Polish edition and both
the same class, and both are fixed here because they are what made the gate
shippable:

- `programs/pl/P16-autodiff.tex` headed `\index{Jacobian}` twice while the
  Polish prose writes *jakobian* in eight inflected forms and *Jacobian* never.
- `programs/pl/P03-orders-of-magnitude.tex` had `\index{cost!FLOPs}` where the
  Polish writes `FLOP-y`, `FLOP-ów`, `FLOP-ach`.

---

## Recorded rather than taken, with the mechanism

Every one of these is a book-wide layout change nobody has measured, which is
the P05 review pass's standing practice.

### Major — no `(continued)` head at a column or page break

Real, and confirmed in the review's own evidence. **The mechanism is the one
CLAUDE.md already records at length: the index here is not a `\twocolumn`
region.** `imakeidx` is loaded without its `original` option and in that mode
it replaces `theindex` with `multicols`, so a continuation head has to be
emitted by *multicol's* output routine and not by `\@makecol` — which is why
`\raggedbottom` was inert in this environment for five passes. `idxlayout`
supplies the feature and is **not loaded**, and adding a package that neither
of this project's machines can be checked against is P09's recorded trap,
latent everywhere here and waiting for a reader's installation. And a
continuation head changes the number of lines per column, so it repaginates the
index. That is a pass of its own, and it needs a sweep against all four builds.

### Major — a parent entry stranded as the last line of a page

Same mechanism, from the other end: the reservation has to be one multicol's
output routine reads. The review says this itself. Note also that
`checkpdf.py`'s stranded-heading check learns the **numbered** heading's size
from the document, so it is structurally blind to an index head — an instrument
is owed before the sweep, which is the same thing the Quiz room test has needed
for eight consecutive batches.

### Minor — no letter headings

`idxlayout`'s `\IndexLetterHead`, or a patch on `\indexspace`. Both add lines
per column and repaginate the index; the package half is P09's trap again.

### Minor — the `measurement` head is a topic dump

**I confirmed four same-page duplicate pairs** — a `measurement!` twin on the
line adjacent to a topical mark, so both resolve to one page:
P25:229/230 (`concentration!of an average`), P25:476/477
(`evaluation!how many items`), P27:86/87 (`evaluation!granularity of a score`),
P27:406/407 (`evaluation!paired comparison`).

Not taken, and the reason is the useful part: **the review's two findings
prescribe opposite treatments for one of those four marks.** The ASCII-maths
minor says convert `measurement!the 1/sqrt(n) rate` to maths; this one says
delete it as a duplicate. I did the first, because it was a defect on the page.
Retiring the head is an editorial redesign of the index's top level — sixteen
entries re-filed, and a decision about which of two descriptions a reader will
use — and a half-retirement is worse than either state. Whoever takes it has
the four pairs above already.

### Minor — twelve entries with two page numbers in one hyperlink

**Not verifiable here and the review's stated cause is refuted.** It proposes
"most likely an `\index` mark whose page list was written by hand". No index
mark in either edition contains a page number; I grepped for it. Diagnosing the
real cause needs the `.ind`, which needs a build, which this container cannot
do. Whoever takes it should start from a real `.ind` rather than from the
proposed cause.

### Minor — sub-entries beginning with articles and prepositions

Not taken. The fix is a sort key or a reword on the order of a hundred marks
per edition, and it is a style decision about the whole index rather than a
defect. It is page-neutral and mechanical if somebody wants it.

### Nits

- **Bold for the defining page, plus a headnote.** Needs a `|textbf` mark at
  the definitional frame of every one of the index's 126 heads. A pass of its own; the headnote alone
  is worse than nothing, because it would promise a distinction the marks do
  not make.
- **Turnover lines leaving a bare page number.** Index typography
  (`\rightskip`, `\hyphenpenalty`); repaginates the index.
- **Running head `Index` roman on the verso and italic on the recto.** Contained
  to `theindex`'s `\@mkboth`, and it cannot move a page — but the appendix
  passes deliberately *added* `\markright` to the back-matter replays so the
  recto head names the program, and removing the recto mark for one chapter
  goes the other way. An author decision.
- **Blank verso carrying a running head.** Already recorded in CLAUDE.md, found
  and deliberately left in the F04 review pass, for the reason recorded there.

---

## Retired: nothing

Unusually, **every finding in #179 reproduced against current source.** The two
previous batches each retired a major that had already been fixed or whose
remedy had already shipped; this issue is newer than those fixes. The only
thing I refuted is a proposed *cause* (the merged hyperlink, above), not a
finding.

---

## Found in a neighbouring program and NOT fixed

### The Polish index heads are English, in thirty-three files

Found while mirroring the fixes. `programs/pl/P08-rank-least-squares.tex` files
`\index{matrix!rank}` and `\index{least squares}`; `P16` files `\index{Jacobian}`;
`P06` files `\index{matrix!...}`; `P03` files `\index{cost!...}`,
`\index{measurement!...}`, `\index{memory!...}`. Measured now, by intersecting
the two editions' head sets: thirty-three Polish program files carry at least
one head that is an English word.

Some are legitimate and must stay — `softmax`, `perplexity`, `bias`,
`transformer`, `prior`, `bootstrap` are what Polish engineers say and the
book's own translator rule keeps them. Many are not: `matrix`, `derivative`,
`vector`, `counting`, `set`, `basis`, `determinant`, `gradient`, `proof`,
`memory`, `cost`, `numbers`, `formats`, `troubleshooting`, `measurement`,
`least squares`, `chain rule`, `integral`, `density`, `rotation`, `wave`,
`radian`, `trigonometry` are all objects the Polish prose names in Polish, so a
Polish reader looks them up under the Polish word and finds nothing.

**Nothing sees it.** Parity's C14 counts `\index` occurrences and never reads
the head; C4 does not carry `\index` at all. The new `--index` check catches
only the sliver where the English head is also a capitalised *name*, which is
how the `Jacobian` instance surfaced.

Not swept: it is a translation decision across ~460 marks and it is a pass of
its own.

### Polish index sorting is wrong throughout, and for two reasons

makeindex sorts on byte order, so every Polish head beginning with or
containing `ą ć ę ł ń ó ś ź ż` sorts after all ASCII letters. The fix is an
ASCII sort key on every Polish mark — the same mechanism I used for
`O-notation` — and it is the same ~460-mark sweep as the head-language job, so
they belong together. **I deliberately did not spot-fix `p-wartość`**, because
one ASCII key in a mis-sorted index is churn.

### Two marks in F12 whose head is English in the Polish edition

`programs/pl/F12-chain-rule.tex` keeps `\index{chain rule!and backpropagation}`
because the file's other heads are English and changing one head in isolation
would leave the file inconsistent. The *new* Polish mark I added is
`\index{propagacja wsteczna}`, which is the word the Polish prose prints. So
that one file now carries both conventions, deliberately, until the sweep above
happens.

---

## Gates

Run before anything else and again at the end, all from source, no build:

```
parity.py                56 file pairs | 1864 frames | 0 failures, 0 warnings
check_structure.py       --frames --answers --outcomes --values --elicit
                         --scripts --terms --parts --index   all green, exit 0
                         82 names in 926 index entries, every one printed
gen_stubs.py --check     47 programs, 2418 planned frames; current
make numbers && verify   All computed output is current
```

`figures/values/appf.tex` is untouched and `code/appf_ledgers.py` was not run —
that is the sync session's. **No value was emitted or retired in this pass**, so
the value ledger has not moved on my account.

The prose detector reports three JOIN candidates and zero long lines:
`seealso` and `seename` in `preamble.tex` and `seealso` in `P15-gradient.tex`,
all three real macro names in new comments and code. That is the recorded
two-instrument false-positive pattern — the line-length instrument reports zero
for each — and neither instrument was run alone.
