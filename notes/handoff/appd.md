# Appendix D hand-off — issue #50

## What the issue asked for, and what was already spent

**Issue #50 was written on 26 August against a build where Appendix D was a
`\programstub{}`.** It was written in the September Appendix D pass, whose note
is already in `CLAUDE.md`. So the first job was the P01/P02 rule — *a review is
a claim about the build it was made on* — applied to a contract rather than to a
review: read every line of the "Done when" checklist against the shipped file
before touching anything.

Four of the seven items were already met and were not touched:

- both editions written, the stub block gone;
- entry-for-entry identical, and gated — args 1 and 2 of `\plterm` are the same
  string in both editions by design, so only the note is translated;
- unsettled terms marked as unsettled, in §D.4;
- `gen_stubs --check` current.

Three were not, and one of them was a false claim on the page.

## The finding: the checklist item caught a real disagreement with Appendix B

The item is *cross-referenced against Appendix B — the two must not disagree*.
They disagreed, twice, and each was decided by opening the thing the sentence
described rather than by preferring one appendix.

**1. The interval convention was said to be flagged at first use, and it is
not.** §D.4 read *"keeps square brackets rather than the angle brackets Polish
schooling uses, flagged at the first interval a reader meets"*. Appendix B says
the opposite in as many words: *"The first interval a reader meets is in
Program~F3, and no program stops to explain the choice, so this appendix is
where it is recorded."* Appendix B is right — `programs/en/F03-logarithms.tex`
lines 1274 and 1435 write `\intcc{0}{1}` in passing, there is no notation box,
and a grep of both editions for any explanation of the bracket choice returns
nothing.

This is the same stale clause the P23 batch corrected **in Appendix B**
(recorded in `CLAUDE.md` under *Appendix B's three stale pointers*), surviving
in Appendix D, which was written later. **The correction reached one appendix
and not the other**, and the same clause is still live in two more places that
were out of scope here:

- `CLAUDE.md`'s notation-contract table: the `\intcc{a}{b}` row still says
  *"flagged to the reader at the first interval"*;
- issue #50's own contract text says *"the reader is told so at the first
  interval"*.

Neither is fixed by this branch. **Both are the sync session's.**

**2. `M(X)` was called residual in Appendix B and current in Appendix D**, and
Appendix D is right. `appendices/{en,pl}/appB-notation.tex` said *"$M(X)$ for
the expectation is residual"*; `programs/en/P24-distributions.tex` line 543's
own notation box — the frame Appendix B cites — says *"Polish teaching materials
write $D^{2}(X)$ for the variance and $M(X)$ for the expectation, and they are
current usage rather than a historical curiosity"*. The "residual" clause comes
from `notes/03-bilingual-and-notation.md` §2.8, which is a plan document written
before P24 existed, and this book's standing rule is that the written program is
the authority and a plan document is not. **Fixed in Appendix B, both editions**
— an appendix contradicting the frame it points at is the defect whichever side
is right about Polish schools.

## What else was missing against the contract

**The reasoning for two of the three splits.** The issue asks for them
*"with their reasoning, not just their outcome, so nobody re-litigates them from
a search result"*. `notes/03` §2.8 gives a reason for each; the appendix gave
outcomes. Added: the interval keeps square brackets because ISO 80000-2 and the
papers do (§D.4), and the book writes `\Var` because that is what the libraries
and the papers write (§D.2). The `tanh` split already had its reason.

**The two rules the lint cannot check were absent entirely.** The issue names
them and neither appendix carried either. New §D.5, *Two rules nothing can
check*: a listing's comments stay English, and a constant's spelling is never
translated.

> The issue's contract gives the constants as `e`, `π`, `i`. **The book has no
> imaginary unit** — `grep -rn 'urojon\|imaginary' programs/` returns nothing —
> so the appendix names `$e$` and `$\pi$` and stops. Writing the issue's own
> list would have been a claim about the book that is false for one of the three.

**Term coverage.** The checklist says *every term the book actually uses is
present; the source is the two editions, not a general glossary*. Twenty rows
omitted, among others, *optimiser* (77 uses in `programs/pl`), *activation*
(67), *normalisation* (56), *cross-entropy* (41), *sampling* (35),
*inference* (27), *perplexity* (15). Twelve rows added to §D.3 and one to §D.4,
every rendering checked against the prose before it was written.

## The row I got wrong, and how

**`inference` shipped in my own first draft with a note that was false, and it
is the exact defect this appendix exists to prevent.** I wrote *"It never means
running a trained model here … the book has no occasion to use that sense and so
has no word for it."* Both halves are wrong. The serving sense is in three
places — `programs/en/F02-language-algebra.tex:116` *"At inference time $x$
varies"*, `P29-entropy.tex:629` *"the distribution a model reports at
inference"*, `P34-measuring-honestly.tex:390` *"inference bill"* — and the
Polish edition renders all three **with the same word**: *przy wnioskowaniu*,
*przy wnioskowaniu*, *rachunek za wnioskowanie*.

So the true note is better than the one I invented: *wnioskowanie* does two
jobs and the Polish carries the English collision rather than resolving it.
Caught by opening the six occurrences rather than by any gate, and it is worth
recording because the frequency audit that found the term is exactly what made
the universal feel safe. **A term's frequency tells you it belongs in the
glossary and nothing at all about what the note should say.**

The same audit demoted a second note: `backpropagation` first read *"F12 names
it and P16 derives it"*. `P16-autodiff.tex` uses the word once, in a
parenthetical about *backpropagation through time*, and never calls reverse mode
by that name; `F12-chain-rule.tex:543` is where the book says what it is. The
row names F12 alone now.

## The collisions, which are the part worth keeping

Five rows exist because one word does two jobs, and each was verified against
both senses on the page rather than assumed:

| term | sense one | sense two |
|---|---|---|
| `precision` / *precyzja* | the classification metric, P23 | significand width, P01 (50 uses) |
| `inference` / *wnioskowanie* | statistical, P27 and P28 | serving, F02, P29, P34 |
| `normalisation` / *normalizacja* | unit length, F09:292 | layer norm, P32 §32.6 |
| `residual` | *rezydualny* — the connection, P32 | *reszta* — what a fit leaves, P08:407 |
| `sample` | *próba* — statistical, P26 | *próbka* — one in hand, P27 |

The last two run opposite ways and both belong on the page: English has one word
for the residual and Polish sensibly has two, which is a thing an English reader
reading a Polish paper needs; and *próba* against *próbka* is one English word
the Polish edition renders two ways, so it went into §D.4 as a fourth unsettled
entry rather than into §D.3.

**§D.4's opening now says four terms rather than three.** That is a count of
occurrences, which this book forbids — it is left as a count only because the
sentence is a lead-in to a table the reader can see entire, which is the one
case where a tally cannot decay silently against something invisible. If a fifth
is found, the sentence has to move with it.

## Also

- **`\arcctg` was missing from §D.1's table.** The file header tells the reader
  to read that table against `lang/en.tex` and `lang/pl.tex` whenever either
  changes, and both define `\arcctg` (`arccot` / `arc\,ctg`). It is unused in
  the body; the table describes the contract rather than usage, so the row is
  honest completeness. Added, both editions.
- **§D.1's *"four that are deliberately not on that list"* was about to go
  stale**, because `\Corr` is a fifth macro both editions set identically.
  Rewritten without the count, and *"the last two"* — which named the wrong two
  as soon as anything was added — now names the variance and the interval
  outright.
- §D.2's ten-row notation-box table was re-verified and is correct:
  `grep -c 'begin{notationbox}'` gives F02, F03, F04, P01, P03, P12, P15, P18
  and P23 one each and P24 three, which the table collapses into one row.

## Values

None emitted, none retired. `code/` is untouched.

**`figures/values/appf.tex` moved and is included in this branch**, against the
parallel-session instruction, because this branch is being merged rather than
handed to a sync session and `make verify` fails on main otherwise. The change
is only the terms ledger and only my doing: `appf.terms.rows` 24 → 37 and
`appf.terms.rend` 27 → 41. No other value moved. Appendix F prints both through
`\val{}` and states neither in words, so nothing in its prose needed touching.
`make debt` reports **82 Polish renderings** against the pre-branch 54.

## Figures

None. Appendix D has none and none was added.

## Not done, deliberately

- **No build of any kind, and not by choice.** `make en` was attempted and
  died with `latexmk: No such file or directory`: **this container has no TeX
  toolchain at all** — no `latexmk`, no `pdflatex`, no `.aux` files. So
  three of the issue's four "make green" items cannot be run here. `checklog`
  needs a log, `reflist` needs the two `.aux` trees, and `checkpdf` needs the
  PDFs. Only `parity` and `gen_stubs --check` are available, and both are
  green, as are every `check_structure` gate, `make verify` and `make debt`.

  What was done instead, statically: every `\ref` target in both appendices
  resolves to a `\label` that exists in the tree; braces balance in all four
  edited files with comments stripped; and every macro used is either defined
  in `preamble.tex`/`lang/*.tex` or is standard LaTeX. **That establishes that
  the references and the grouping are sound and it does not establish that the
  book compiles.** CI is the second machine and is the only thing that can say
  so.

  An earlier draft of this note claimed the two builds had been run. They had
  not — the command was issued, and it failed before reaching TeX.
  Pagination is the sync session's regardless.
- **`CLAUDE.md`'s notation-contract table still carries the stale
  *"flagged to the reader at the first interval"* clause**, and issue #50's own
  text carries it too. Not edited here, per the do-not list.
- **Appendix B's opening still says *"the four places where mathematical usage
  is split"*** and then prints four notation boxes, one of which now carries two
  splits. It is defensible as it stands and it is Appendix B's sentence to
  decide, not Appendix D's.
- **No adjudication of Polish usage from outside the book.** Where the two
  editions and a plan document disagreed, the written program decided. Where the
  profession itself has not settled — *próba* against *próbka* — the appendix
  says where each falls and does not pick.
