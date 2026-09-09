# Hand-off: issue #194 — no copyright page and no ISBN

Unit: the book itself (front matter, Appendix B, Appendix F). Branch
`claude/book`. Verified against `origin/main` at `c9b8bb6`; the issue was
written against `f0a5660`.

## Every finding, with its disposition

**1. There is no copyright page. — FIXED, both editions.**

Reproduces exactly as reported: `frontmatter/{en,pl}/` held three files, and
everything a copyright page carries was set in grey at the foot of the title
page. `frontmatter/{en,pl}/copyright.tex` is new and carries the copyright
notice and year, the two licences, the self-published statement, the missing
catalogue identifiers named rather than left blank, both languages and both
paper formats, the pin date, and the Stroud disclaimer. The title pages keep
the title, the subtitle, the author and the edition number and nothing else.

`\bookyear` is new, in `preamble.tex`'s PINNED FACTS block beside
`\bookedition`, with a comment saying why it is not `\pinnedon`: the pin date
moves with every `make numbers` and the copyright year does not. They read
`2026` both, today, which is a coincidence with a lifetime.

**2. No preface and no acknowledgements. — RECORDED as a decision, no action.**

The issue says the absence may be deliberate and asks only that the decision
be recorded rather than inferred from an empty directory. It is now a comment
in `body.tex` beside the front-matter wiring, which is the file that would
carry them: the Introduction already does a preface's work, and a second
chapter saying the same thing before it reads as throat-clearing.

**3. Appendix B has no symbol table. — DECISION CLOSED, recorded in the file.**

The reader-facing half was already done in #113 and I retired nothing: the
appendix's own opening says it is deliberately not a table of every symbol and
gives the reason. What was missing is the note for the next *author*, which is
what the issue asks for ("so the next reader of the file does not re-open
it"). Both editions' `appB-notation.tex` now opens with a comment block
recording the decision, the evidence, and what reversing it would cost.

The evidence was checked rather than accepted, because the appendix's reason is
a claim about two other programs: `programs/en/F02-language-algebra.tex:165`
introduces the subscript in as many words ("A subscript is nearly always an
index"), and `programs/en/F04-sums-products-sequences.tex` builds the sigma
from nothing. Both hold. Note that the appendix's prose cites `F02` and `F04`
by program label and the *files* are `F02-language-algebra` and
`F04-sums-products-sequences` — the filenames the issue's phrasing might lead
you to grep for do not exist.

CLAUDE.md's *What is left* item 5 still carries this as an open choice. I did
not edit CLAUDE.md; the sync session should close that item.

**4. Knock-on: Appendix F says "That is the whole of what is outstanding". —
FIXED, both editions.**

The ISBN is now the last entry in that list, and the sentence is true again.
The lead-in said "Three other things are owed", which is a count of a list
that has just grown; it is retired rather than incremented, and names the
reason the experiment table already gives. That cross-reference was checked:
`appendices/en/appF-manifest.tex:86` does give it.

## Superseded by #224 while this branch was open — read this first

`main` moved thirty commits under this branch and another session fixed the
program count **better than I did**, so a third of my work is not in the merge
and the record of it matters more than the work would have.

I found, independently and before that landed, that
`frontmatter/{en,pl}/introduction.tex:80` and both title-page subtitles read
"forty-six programs" against a manifest of forty-seven — the P7-insertion
off-by-one in one more artefact, contradicted four times per edition by
Appendix E. The reason nobody had opened it is still worth having: the **other**
number in that six-word sentence, the nine parts, has been gated since that
insertion was found, and gating one number in a sentence does not gate the
sentence.

My fix was to correct the word and extend `check_structure.py --parts` with a
compositional English/Polish numeral reader over 1–99, mutation-tested in four
directions. **#224's fix is strictly better and mine is gone from this branch.**
It makes the count a computed value, `\val{appf.programs}`, emitted by
`code/appf_ledgers.py` — which is this book's own first convention, cannot go
stale, and needs no checker at all. A spelt-numeral gate on top of it would be
a second mechanism for one fact, which is the defect this repository keeps
recording rather than a guard against it. All that survives in
`check_structure.py` is a docstring paragraph in `check_parts` saying the count
is deliberately not checked there, and why, so the next person does not add the
checker back.

The knock-on the issue named is also partly superseded: #196 cut the companion
library from Appendix F and replaced *"That is the whole of what is
outstanding, as far as anybody knows"* with a much more careful sentence. My
edit to that sentence is dropped; the ISBN entry is re-applied on top of #196's
text, and the lead-in tally is retired — it has read "Three" and "Two" inside a
fortnight and **neither was wrong when it was written**, which is the argument
for not having it.

The one thing I did not take from `main` is the title page's grey imprint
block, because moving it to the copyright page is this issue.

## What I found that the issue did not, and fixed

**The introduction miscounted the book's own programs, on page one, in both
editions — superseded by #224, see above.** `frontmatter/{en,pl}/introduction.tex:80` read "Nine parts,
forty-six programs." / "Dziewięć części, czterdzieści sześć programów." The
manifest has forty-seven and `gen_stubs.py --check` prints forty-seven. So the
book contradicted itself: Appendix E says forty-seven four times per edition.
It is the P7-insertion off-by-one surviving in a further artefact, and it is
the one nobody had opened because the *other* number in the same six-word
sentence — the nine parts — has been gated since that insertion was found.

Gating one number in a sentence does not gate the sentence. Both the
introductions and both title-page subtitles now carry `\val{appf.programs}`
from #224, taken verbatim from `main` — including the Polish subtitle, which
differs from the English by a word and is another session's decision, not this
issue's business.

**`lang/en.tex:80`** carried "forty-six programs deep" in a comment. Corrected;
that one is a comment rather than a printed value and #224 did not reach it.

## Claims of my own I had to withdraw

Three, all caught by re-reading my own additions rather than by any gate.

- The copyright page said the ISBN's absence is "the last entry in
  Appendix F". That is a positional claim and it stops being true the day
  somebody adds an entry. It names the thing instead.
- The copyright page said the pin date "says when the arithmetic was last run".
  `\pinnedon` is a hand-maintained string in `lang/*.tex`, so that over-claims
  automation. It now says only that it is a different date from the copyright
  year and means a different thing.
- Appendix F said the ISBN is "the only entry on this list that no amount of
  writing closes". **False** — the trained-model measurements are not closed by
  writing either. What is actually distinctive is that it is the only entry
  that is not about the contents at all, and that is what it says now.

## Pagination — READ THIS

**No frame was lengthened or shortened. Nothing in the body moved.** Every edit
is in the front matter, in two appendices' prose, in a preamble comment block
and in a tool. `\mainmatter` starts the body on a fresh page with the counter
reset, so front-matter length cannot reach it, and the Appendix B change is
comment-only.

**Prediction, labelled as judgement because there is no TeX in this container
to test it against** — no `pdflatex`, no `latexmk`, not even a `book.cls` on
disk, so this could not be measured and must not be read as measured:

> The copyright page costs **zero pages** in all four formats. `titlepage.tex`
> ended with `\cleardoublepage`, which from the recto page i inserts a blank
> verso ii and lands on iii. It now ends with `\clearpage` and the copyright
> page fills page ii. The front matter should therefore be exactly as long as
> before, and the four PDF page counts unchanged.

If that is wrong the build will say so in one number, and the failure mode is
benign: one extra leaf in the front matter, which still cannot move the body.

The two appendices gained roughly ten typeset lines each (Appendix F's new
paragraph; Appendix B's addition is a comment and typesets nothing), so
Appendix F may turn a leaf at the very end of the back matter. Nothing before
it moves.

So: **no cue walk should be needed.** Please confirm rather than assume — if
the four page counts move by anything other than 0 or the Appendix F leaf, the
`\clearpage`/`\cleardoublepage` reasoning above is what to re-examine first.

**CI built all four formats green** on the pre-merge head (run 34334457718; all
nine checks success, including `Compile en/pl (standard)` and `(a4)`), so the
copyright page compiles and no overfull box, stranded opener or stranded
heading came with it. That does **not** settle the page counts: they are
printed into each compile job's step summary, and the Actions log artefacts
live on `productionresultssa10.blob.core.windows.net`, which this session's
egress policy blocks — so an agent session cannot read them. Read them from the
run's step summaries in a browser, or just from your own `make all-formats`.

And note what CI's green cannot cover: `checkpdf.py` runs there with
`--cues=warn`, so an **orphaned cue** would not have turned it red. The
argument that this change cannot produce one is structural — `\mainmatter`
restarts the body on a fresh page — but it is an argument, not a measurement.

## Ledgers the sync session owns

- `figures/values/appf.tex` was **not** touched and `code/appf_ledgers.py` was
  not run. `make verify` reports everything current on this branch; no emitted
  value was added or retired, so I do not expect that file to move.
- CLAUDE.md's *What is left* item 5 (Appendix B's symbol table) is now closed
  in the book and should be closed there.
- CLAUDE.md's page table and `notes/01-curriculum.md` §20's part-page table are
  in **PDF pages**. If the prediction above holds they do not move; if it does
  not, every row shifts by the same constant and the first-volume figure with
  them.
- The parity file-pair count goes 56 → 57.

## Unverifiable here, named so it is checked once

`\textcopyright` is the only token on the new page whose availability I could
not compile-test. It is kernel-provided and `preamble.tex` already ships
`\textbullet` unconditionally (line 1917) from the same family, with
`\usepackage[T1]{fontenc}` at line 90, so the precedent is in the tree rather
than in my memory — but it has never been set in this book before.

## Not taken

Nothing was classified (b) or (c). No book-wide layout change was needed and
nothing here needs a trained model.

## Gates

All run before any edit and again after, source-level and before any build,
which is the standing order.

```
parity.py                    57 file pairs | 1866 frames | 0 failures, 0 warnings
check_structure.py           --frames --answers --outcomes --values --elicit
                             --scripts --terms --parts   all green
  9 part ranges in each introduction, every one matching the manifest,
  and both count 47 programs.
gen_stubs.py --check         47 programs, 2418 planned frames; current
make numbers && make verify  All computed output is current: values and transcripts.
make debt                    0 of 47 programs are stubs, 0 of 6 appendices,
                             elicitation 1030/1866 (55%), unmoved
```

`make debt` also reports `main-en.aux missing`, which is the cross-reference
comparison asking for a build. There is no TeX in this container; it is the
sync session's.
