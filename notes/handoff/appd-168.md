# Appendix D hand-off — issue #168 (review)

`notes/handoff/appd.md` is a **different, still-pending** note, for issue #50
(PR #208). This one is the review issue and does not supersede it.

## First: the review is a claim about a build this repository has moved past

Issue #168 was written against `main` at **9402620**. Two merges have landed on
Appendix D and Appendix B since. Reading every finding against current source
before touching anything retired **five of the seventeen**, including the one
major — and in one case the review's own *suggested fix* would have introduced
a defect.

**0 blocker · 1 major · 11 minor · 5 nit → 10 fixed, 5 retired, 2 recorded.**

## Retired, with the evidence

- **🟧 major — "Appendix B contradicts D.1: it says the Polish edition sets
  tan, cot and arctan."** `appendices/en/appB-notation.tex:109` now reads
  *"Nobody types* tg *into a program, so the Polish edition sets* tg, ctg *and*
  arc tg*, as Polish mathematics does"* — verbatim the fix the review asked
  for, plus the `\tg`/`\ctg`/`\arctg` attribution. Corrected by the blocker
  batch, whose own pass note in `CLAUDE.md` records it under *"Appendix B: the
  stub that printed, and four claims the book contradicted"*. Nothing in
  Appendix D needed changing; the two appendices now agree.
- **The `\programstub{}` "NOT YET WRITTEN" banner on Appendix B** (the aside
  in the same finding). `grep -rn programstub appendices/` returns nothing;
  same batch.
- **🟨 "Page 1116 is stretched into three blank bands around the D.2 table"**
  and **🟨 "D.4 heading and its three-line intro sit below a quarter-page gap,
  with the table overleaf."** Both diagnoses are float stretch. There are no
  floats in Appendix D in either edition — `grep -n 'begin{table\|begin{figure\|\[htbp\]'`
  returns nothing, every table is a plain `center` + `tabularx` in the text.
  That is exactly the remedy the review proposed ("Make the two tables
  non-floating, plain tabularx in the text, as the D.1 table already is"), so
  this is the *remedy-already-shipped* class the P01/P02 and Part V/VI batches
  each recorded. **Residual, stated honestly:** a `tabularx` cannot break
  across a page, so a long one can still push itself whole to the next page
  and leave `\flushbottom` to stretch what it left behind. Whether that still
  happens is a page measurement and I did not build. If the sync build shows
  it, the cause is now the unbreakable table rather than a float, and the
  remedy is different.
- **🟨 "'four that are deliberately not on that list' names five things."**
  Already reads "And **some** that are deliberately not on that list" (#208).
- **🟨 "'flagged at the first interval a reader meets' is contradicted by
  Appendix B."** Already corrected by #208 to *"No program stops to explain
  that, so Appendix~B is where it is recorded rather than the first interval a
  reader meets"*, which is what Appendix B says.

## Fixed, both editions

- **The D.1 forward pointer sent the variance to the wrong section.** It said
  the variance and the interval "are both taken up in section D.4". The
  interval is; the variance is taken up in **D.2**, whose P24 row and closing
  paragraph carry $\Var$ against $D^{2}(X)$ at length. In a reference appendix
  whose whole value is that its pointers hold, a reader following that one
  found nothing. Now names a section each. (The review reported this as "Cov
  never reappears"; the sentence had already been narrowed to the variance and
  the interval by #208, so the surviving defect is the section number.)
- **D.1 claimed to list the symbols the two editions set differently and
  omitted the punctuation contract.** The quotation marks are the most visible
  divergence between the editions and are on every page of both. A paragraph
  now names `\dash` and `\enquote` as the same mechanism applied to
  punctuation, and says they are named rather than tabulated — **the rows were
  deliberately not added**, because writing the literal glyphs would mean
  either raw U+201E/U+201D in prose (the class `CLAUDE.md` warns about under
  the U+00A0 trap) or the contract macros, which print the current edition's
  form in both columns and say nothing, which is the trap D.1's own prose
  warns about.
- **The appendix promised a Polish reader a lookup its structure cannot
  honour.** The opening still says the appendix is for the Polish reader "who
  needs to know which English word a Polish term is standing in for", and every
  table is English-headed. A paragraph now says the heads are English, why
  (the English term is what a reader searches for, so it is the head that stays
  put), and that a Polish reader reads down the middle column. **The Polish→
  English list the review offers as its first option was refused**: it would be
  a hand-maintained second copy of a gated table, which is the class this book
  refuses — a corrected copy is the next thing to go stale. The index route was
  refused too: `\plterm`'s second argument may hold several comma-separated
  renderings, so `\index{#2}` would index "partia, wsad, batch" as one entry,
  and `make debt`'s "82 names in 926 index entries, every one printed in its
  own program" is a gate an appendix-sourced entry would have to be checked
  against first.
- **D.2's pointer column was headed "where" over cells reading F2, F3, 1, 3,
  12.** In this book a small integer overwhelmingly denotes a frame. Heading it
  **program** removes the ambiguity at no width cost. I did **not** take the
  review's first option (`Program~\ref{}` in every cell): it widens an `l`
  column by about eight characters and takes that width out of the `X` column
  beside it, which is a height change I cannot measure. Nor its parenthetical
  ("in which case the D.3 and D.4 notes should lose their 'Program' too") — a
  column headed *program* and a note running as prose are different contexts,
  and "Program~\ref{}" is right in the second.
- **D.2's F04 row withheld the word it settles.** It read "one English word
  doing two jobs" where rows P15 and P23 name theirs. **The word is *index***,
  from `programs/en/F04-sums-products-sequences.tex:341` — F01 calls the raised
  number in $a^n$ the index and F04 calls the lowered number in $x_i$ the index
  as well. The review guessed "the operation and its result", which is not what
  that box is about; opening the program is what settled it.
- **D.3 illustrated "no Polish form is in real use" with *embedding*** — the
  one term D.4 records as *mostly rendered in Polish*, so the exemplar
  contradicted the appendix two pages later. **The review's own replacement
  would have reintroduced a worse defect:** it suggests *"tokenizator,
  benchmarku, promptem"*, and `promptem` occurs **zero** times in
  `programs/pl` — which is precisely the failure `CLAUDE.md`'s Appendix D pass
  note records (§D.3's introduction once named *embeddingu*, a form the Polish
  prose uses zero times). Every exemplar was counted before it was written:
  `tokenizator` 3, `benchmarku` 22, `hiperparametr` 6 exact-word hits.
- **A math error in the argument for *krok*.** "*Krok* reads as *step*, which
  is what it multiplies" — the coefficient multiplies the **gradient** and the
  step is the product; the book calls $\eta f'$ the step
  (`programs/en/F11-derivative.tex:960`). In an appendix arguing about which
  Polish word is right, that clause is the whole case for *krok*. Now: "which
  is what the coefficient produces rather than what it multiplies: it
  multiplies the gradient, and the step is the result."
- **"Four terms in this book are rendered more than one way"** was falsified by
  a D.3 row two pages earlier — gradient descent is written both *spadek
  gradientu* and *spadek gradientowy*, which is more than one *way*. The
  distinction the appendix draws is words, not ways. The tally is gone rather
  than corrected (`CLAUDE.md`: never state a count of occurrences), the noun is
  now *word*, and the gradient-descent note says why it is filed in D.3 rather
  than D.4. **Note the Polish twin already said *słowem* — the divergence was
  in the English alone, and no check reads it.**
- **"one page where the choices are written down"** over a four-page, five-
  section appendix → "one place".
- **"Both columns are set as literal text"** over a three-column table → "The
  first two columns", in the prose **and in both file-header comments**, which
  made the same claim.

## Recorded rather than taken, with the mechanism

- **🟨 "D.4's note column is squeezed into a 12-line cell while the middle
  column is mostly empty."** Real, and the cause is one cell: *współczynnik
  uczenia, krok uczenia* is 34 characters in an `l` column, so it takes width
  the `X` note column needs. **The fix is one line** — give the two content
  columns tabularx weights, `{@{}l>{\hsize=.75\hsize}X>{\hsize=1.25\hsize}X@{}}`
  — and `array` and `tabularx` are both loaded, so it is mechanically
  available. **I wrote it, then reverted it.** There is no TeX installation in
  this container (`which pdflatex latexmk` is empty), so I could neither build
  nor put a ten-line standalone to TeX, and "standard tabularx idiom" is a
  reading of a mechanism, which this book's own rule leaves labelled as
  judgement until it is run. A `tabularx` cannot break across a page, so a
  misjudged weight moves the whole table to another leaf silently. Every other
  fix in this pass is verifiable by reading; this one is not. Whoever takes it
  needs one build of all four formats and should expect the table to get
  *shorter* (the note loses lines; the Polish cell gains one).
- **⬜ "'Program' hyphenated as 'Pro-/gram' before its number."** Book-wide.
  `Program~\ref{}` already ties the number to the word, but the word itself
  stays hyphenatable, so the class fix is `\hyphenation{Program}` in
  `preamble.tex` — a preamble change that moves line breaks at every
  "Program" in the book and that nobody has measured. `\mbox` at the Appendix D
  sites only would be fixing an instance rather than the class, which is the
  thing `CLAUDE.md` keeps recording.

## What the sync session needs

- **Frame lengths: unchanged. No frame was touched** — this pass is entirely
  inside `appendices/{en,pl}/appD-terminology.tex`, which has no frames, so
  there is no cue to walk on that account.
- **Appendix D grew by about ten lines per edition** (two new paragraphs in
  §D.1, one in the opener, one longer note in §D.4). It is back matter, so it
  moves no page boundary in the body; it can move Appendix E, F and the index,
  and therefore the page numbers the index prints.
- **Values: none emitted, none retired.** `make verify` reports all computed
  output current, `figures/values/appf.tex` included — this pass moves no
  ledger, so there was nothing to regenerate.

## Found in a neighbouring file and not fixed

- `appendices/en/appB-notation.tex:64` and `:83` write **`Program~P18`** and
  **`Program~P24`** as literal text where the rest of the book writes
  `Program~\ref{prog:P18}`. Both resolve to the right program today, so nothing
  is wrong on the page; they are simply outside the reference mechanism and
  would not follow a renumbering. Same file, `:75`, writes `Program~F3` the
  same way. Out of this unit and left alone.

## Gates

Run **before** any edit and again after, per `CLAUDE.md`'s rule that the
source gates read the source and none of them needs a PDF:

```
parity.py                    56 file pairs | 1866 frames | 0 failures, 0 warnings
  appD-terminology.tex       C4 63 tokens · C8 identical · C12 6 literals identical
check_structure.py           --frames --answers --outcomes --values --elicit
                             --scripts --terms --parts   all green, exit 0
  84 Polish renderings named in Appendix D, every one used in the prose
gen_stubs.py --check         47 programs, 2418 planned frames; current
make numbers / verify        all computed output current: values and transcripts
make debt                    unchanged; elicitation 1030/1866 (55%)
```

C12 read 7 literals while the reverted table spec was in the tree (`1.25` is a
numeric literal) and is back to 6, which is byte-for-byte what `HEAD` has. The
prose detector's two JOIN candidates — *whichever*, *czyta* — are ordinary
words that split into two words the file already contains, with the
line-length instrument at zero for both: the recorded two-instrument
false-positive pattern.
