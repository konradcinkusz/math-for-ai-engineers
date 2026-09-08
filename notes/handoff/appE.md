# Appendix E hand-off — issue #51

## The issue was already resolved, and its checklist was not

`appendices/{en,pl}/appE-further-reading.tex` were written under **#107**
(commit `8144096`), which is a different issue for the same appendix. Nothing
in #51's contract is unwritten: the stub is gone, both editions exist, the
survey carries verdicts, and §E.4 already labels its own entries as pointers
rather than recommendations.

So the pass is the **checklist**, not the prose. Two of its items were
verifiably false and one was partly false, and finding that out cost greps
rather than judgement.

## THE FINDING: the appendix was unreachable from the thirty-six places that defer

> `[ ]` Every `rigourbox` in the book that promises "the proof lives here"
> resolves to something in this appendix

**There is no `\ref{app:E}` anywhere in `programs/`, `frontmatter/` or the
other appendices — not one.** (Appendices A, C and D are each referenced from
the body; E is not.) So a reader standing at a rigour box that says *any first
analysis course* had no route to the appendix that names Abbott and Tao, and
the appendix had no route back.

Measured rather than read: the book carries **36 rigour boxes**, and **15 of
them, in 14 programs, contain no `\ref{prog:...}` at all**. A box that defers
*inside* the book cites the program it defers to, so a box with no such
reference is outward-facing **by construction** — an exact, mechanical
criterion, and it is edition-stable (both editions carry the same fourteen:
F04, F13, P04, P05, P10, P12, P14, P15, P19, P20, P25, P26, P27, P30).

Of those fourteen, **five had no destination anywhere in the appendix**:
combinatorics (P12), the capacity question (P05), variational inference (P19),
the bootstrap (P27), asymptotic estimator theory (P26). Two more were only
loosely covered.

### What was done

**§E.5, *Where each unproved statement goes*** — three five-row tables, subject
against the programs that defer it against the destination. Five rows say
**not surveyed**, and a `note` box states the rule that produced them: a
destination here is a work this appendix has already introduced, or it is
nothing, and the column says which. That is the honest discharge of the
checklist item — a reader learns the book has nothing for them and stops
looking, which silence does not give them.

**`check_structure.py --rigour`** gates it, on the mechanical criterion above,
in both editions. Wired into `make check`, `make debt` (a `rigour:` target) and
the CI `parity:` job. **Proved by mutation before it was believed**, three
ways, each restored afterwards:

| probe | reported |
|---|---|
| the P12 row deleted | `P12 has a rigour box that defers outside the book and Appendix E names no destination for it` |
| a program with no rigour box put in the *Deferred from* column | `Appendix E routes a rigour box to P32, which carries none. The row is stale.` |
| `\label{sec:E-route}` renamed | `no route section ... Every rigour box that leaves the book needs a destination` |

The second mutation is not hypothetical — **it fired on the check's first real
run, against my own table**, because the row whose *destination* is
Program P32 was being read as a row whose *source* was P32. The check now
parses the tabularx rows positionally and takes the second column, because the
distinction between a source and a destination is the whole content of it.

Parity is blind to all of this for the reason it was blind to the seven wrong
part ranges: C4, C8, C12 and C14 compare the two **editions**, so a row missing
from both diverges from nothing.

**Still outstanding, and this check cannot see it: nothing in the book
references Appendix E.** Closing that means editing every deferring program,
which is a pass of its own and would have collided with the parallel review
sessions. Recorded in both file headers and in the tool's docstring.

## THE SECOND FINDING: the scope statement had two sources and the appendix opened one

> `[ ]` Every exclusion in the scope statement has a destination

§E.3 was imported from `notes/01-curriculum.md` §13 — ten rows, faithfully.
**`notes/02-grounding-and-traps.md` §4 is a second and larger exclusions list —
fourteen rows plus four "least sure about" — and the appendix never opened
it.** That is P27's finding (*a sweep is as wide as the artefact somebody
thought to open*) arriving at the appendix whose entire subject is what the
book does not teach.

It is not a marginal omission. **The issue's own contract paragraph leads with
an exclusion that was absent**: *"The book excludes every integration
technique"*. Also absent: characteristic polynomials and Jordan form, cofactor
determinants, frequentist estimator theory, the classical test zoo, and — the
most honest thing in either notes file — **causal inference, excluded outright
and flagged as a candidate for a second edition**.

### What was done

A **third table in §E.3**, five rows, *the classical curriculum this book
declines*, with the distinction that makes it worth separating: the first two
tables are subjects the book **borrows from**, so each names a book; these are
techniques whose destination is **not a book at all** — it is a program of this
one and a routine you already have installed. Both are destinations, and the
lead-in says which kind each table carries.

Then **the four exclusions the book is least sure about**, as prose.

## A NEIGHBOUR CLAIM I HAD TO CORRECT — not fixed by me

**`notes/02-grounding-and-traps.md:1699`** (§4.1, the determinants row) says the
replacement is *"P09 teaches what a determinant means; the arithmetic is one
worked 3×3 and then `slogdet`"*.

**The written P09 has neither.** `grep` finds no `slogdet`, no cofactor
expansion and no worked 3×3 determinant; what it has is the $2\times2$ formula
(`programs/en/P09-determinant-inverse.tex:190`) and, at line 195, *"a machine
will compute it by elimination, and so will you"*. The notes describe a plan
the program did not take, which is the recorded class — **the written program
is the authority and a plan document is not**. My table row says what P09 does.
Left unfixed in `notes/02` deliberately: other sessions are appending to that
file and the hunk would collide.

**`programs/en/P25-clt-monte-carlo.tex:1011`** — its rigour box defers residual
connections and normalisation and says *"this book does not measure either"*.
Program P32 **derives the residual stream** (`\label{sec:P32-residual}`), which
that box does not say. The route table sends the reader to P32; the box itself
still does not, and that is a one-clause fix for whoever next opens P25.

## The third checklist item, and where I stopped

> `[ ]` Every recommendation carries good-at / bad-at / how-long /
> first-reading-or-reference

Good-at, bad-at and reference-or-route were already carried in every §E.1
entry. The **floor each work assumes** — the practically decision-bearing half
of "how long" — was carried by six of the eight and missing from Deisenroth and
Goodfellow; both now state it, from `notes/02` §1.12's own column.

**No reading time is quoted for any entry, and §E.1 now says so and why**:
nobody on this project has timed a reading, and a duration invented to fill the
column would be the first unsupported claim in the book. That is the issue's
own rule (*recommend nothing unread*) applied to the checklist item that
invites breaking it. Where a scale is a fact it is already on the page — 432
pages, over a thousand, sixty.

## Values, figures, transcripts

**None emitted, none retired, no figure, no transcript.** `make verify`
reports all computed output current, `figures/values/appf.tex` included —
this pass moves no ledger, so the sync session inherits nothing stale from it.

## The build: what CI settles, and what it does not

There is no TeX installation in this container at all (`pdflatex: command not
found`), so not even a standalone syntax probe was available here — the four
formats were never mine to measure. **CI run 220 came back green on all eight
jobs**, which is the second machine and the only compile this branch has had:

- all four formats compiled, `en`/`pl` × standard/A4;
- `checklog.py` green on each, so on CI's metrics there is no error, no
  unresolved reference, no rerun or label-drift warning, no overfull vbox and
  no hbox over the 15 pt budget;
- `checkpdf.py` green on each: no stranded frame opener, no stranded section
  heading;
- and the new `--rigour` step green in the parity job.

**Stated with its limits rather than as a clean bill.** A box under 15 pt
still passes; the cue check is advisory in CI by design; the orphan tail is
never fatal. The page counts, the exact overfull multiset and both page-level
ledgers remain the sync session's, and CI's metrics are not the container that
writes the published PDF. What it does settle is the thing I could not: the
appendix, its six new tables and the new section are valid LaTeX and typeset
in every format.

## What I deliberately did not do

- **No four-format build here**, per the parallel arrangement, and none was
  possible anyway — see above. What I ran instead: brace balance, environment balance, per-table column counts
  against each `tabularx` spec, and a check that no *new* source line exceeds
  79 characters (the file's own ten pre-existing long lines left alone, on the
  measure-what-HEAD-does rule). **Every one of the six new tables is exactly
  five rows**, which is the ceiling the first Appendix E pass arrived at after
  its eleven-row table gave a 284 pt overfull vbox.
- **No inbound `\ref{app:E}`** — see above.
- **No edit to `notes/02` §4.1** — see above.
- **No new source recommended.** Five rows say *not surveyed* rather than
  naming a plausible book, which is the appendix's own contract.

## Gates, all run before anything else

    parity.py                    56 file pairs | 1864 frames | 0 failures, 0 warnings
    --frames --answers --outcomes --values --elicit --scripts --terms --parts --rigour   all green
    --rigour                     14 programs defer a result outside the book; Appendix E
                                 names a destination, or says it has none, for every one
    gen_stubs.py --check         47 programs, 2418 planned frames; current
    make numbers && make verify  all computed output current
    make debt                    unchanged; elicitation 1028/1864 (55%), untouched

Parity came back clean on its first run for both editions, and the elicitation
rate did not move — this pass converts no frame and adds none.
