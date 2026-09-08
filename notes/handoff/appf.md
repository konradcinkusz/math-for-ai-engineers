# Appendix F review pass (issue #176) --- hand-off

Unit: Appendix~F, the manifest. Reviewed build: `main` at `9402620`, which is
the commit that *wrote* Appendix~F. Both editions edited; no other unit's
files touched.

Gates, all run before any edit and again after, all green: `parity.py` 56 file
pairs / 1864 frames / 0 failures and 0 warnings; `check_structure.py --frames
--answers --outcomes --values --elicit --scripts --terms --parts`;
`gen_stubs.py --check`; `make numbers`; `make verify` reports every computed
output current, `appf.tex` included --- **no value was emitted or retired, so
`appf.tex` is NOT stale from this pass.**

---

## THE FINDING: the false claim has four more homes, and one of them is a ledger

The review's second major is that F.4's warning box says *the Quiz runs on the
Foundation programs only*. Verified false: `grep -l 'begin{quiz}'
programs/en/*.tex` returns **47 of 47**. Deleted from both editions.

Grepping for the claim rather than for the file --- which is this repository's
own rule after the MiB unit defect --- finds it alive in four more places, and
the chain between them is the useful part:

| where | text | what it is |
|---|---|---|
| `notes/01-curriculum.md:325` | \S14, "**Quiz** --- Foundation programs only." | the premise |
| `notes/01-curriculum.md:790--791` | \S16, "\S14 puts the Quiz on Foundation programs only, so the standard could not be measured on 34 of the 47" | cites \S14 |
| `Makefile:310--314` | the `make debt` 80/80 block: "The Quiz runs on the thirteen Foundation programs only, so a standard defined against it would be unmeasurable on thirty-four of the forty-seven -- and contaminated on the other thirteen" | the ledger, printed on **every build** and into CI's step summary |
| `README.md:56` | "**Quiz** \| Foundation programs only." | contributor-facing |

**Appendix~F's sentence was written from the Makefile's ledger**, near enough
word for word, so this is one false premise with four dependents rather than
four independent slips. The P04 pass corrected the front matter's copy and the
Foundation batch corrected the Quiz heading in `lang/*.tex`; neither swept the
premise, which is this repository's recorded finding that *a sweep is as wide
as the artefact somebody thought to open*.

**All four recorded, none fixed**, because the Makefile block and
`notes/01-curriculum.md` are ledger prose the sync session owns and `README.md`
is outside this unit. The ledger copy is the one worth fixing first: it is the
only one a build prints.

**And one apparent copy is NOT one, on evidence.**
`frontmatter/en/how-to-use.tex:99` reads "**Work the thirteen Foundation
Quizzes and nothing else.**" That is advice to a reader with a degree ---
skip Part~I except where a Quiz goes badly --- and it makes no claim about
which programs carry a Quiz. It is correct as it stands. Do not "fix" it.

---

## Fixed, in both editions

1. **The false Quiz clause**, above. The rest of the sentence carries the
   argument on its own and matches `\lblCanYouFooter`, which says the Quiz
   "answered a second time \dots is the same questions asked of a reader who
   now remembers the answers." Checked against that string rather than assumed.

2. **The bare-numeral \enquote{Where} column** (the review's first major).
   `\ref{prog:P20}` renders as **20**, because `preamble.tex:286` sets
   `\thechapter` to `\arabic{chapter}` for the main programs --- so a cell read
   as a folio, four pages after the diagram manifest has trained the reader
   that a right-hand numeral is one. Now `Program~\ref{prog:P20}`, which is the
   book's own form (1432 uses in `programs/en` alone). The not-run table's
   header is now \enquote{Where it would go}, because an experiment that has
   not run has no *where*.

3. **F.2's middle table was staler than the review found, and \S17 settles all
   three of its rows.** The review flagged E5 only. `notes/01-curriculum.md`
   \S17's Status column was filled in at `fd802d1`, **one day after Appendix~F
   was written**, and it settles the middle table's whole membership --- "one
   yes, one half and one no". Verified against the scripts rather than taken
   on trust:

   - **E3 is met, line by line** --- `code/p05_inner_product_norms.py:134` has
     `DIMS = (2, 3, 10, 100, 768, 4096)`, the specification's range verbatim;
     line 167 measures the angle in degrees; line 186 asserts the spread tracks
     `1/sqrt(d)`. **Moved to \enquote{Run}.**
   - **E1 is half met** --- P02 has the cliff per format
     (`code/p02_numerical_stability.py:176`) and sweeps *pivots* on one fixed
     row rather than sweeping the magnitude. **Its own table, \enquote{Half
     run}**, with a sentence saying which clause is met and which is not.
   - **E5 is not met** --- P16 counted operations and derived the checkpointing
     peak; the specification asks for time and peak memory on a machine.
     **Moved to \enquote{Not run}**, with a sentence saying what P16 did
     instead and why that is a different instrument.

   The middle category's old prose --- "no pass ever claimed the experiment"
   --- was false for E3 and E1 by then, and is gone. The three groups are now
   three parallel bold labels, which also settles the nit about their being
   labelled in three different shapes.

   **E1's cell described the program, not the specification**, which is
   probably why it looked met: it read "what a non-maximal pivot costs", which
   is what P02 *did*. It now states what E1 *specifies*, under a column headed
   "What it specifies".

4. **\enquote{Two of those describe one edition} --- there are three.}**
   Confirmed against the values: transcripts 44/88, diagrams 150/300,
   **Polish renderings 27 per edition and 54 across both** (`make debt` prints
   54; `figures/values/appf.tex` has 27). The third row was missing and its
   both-editions figure was never given, which broke the note box's own promise
   on p1127. Now "Three of those", with the renderings given as *twice*
   `\val{appf.terms.rend}` --- **a doubling rather than a hand-typed 54**, so
   no new value was needed and the appendix's no-typed-counts design holds.
   The stated reason is now "because each edition carries its own", which is
   true of all three rows where "produced separately in each language" was true
   only of two.

5. **\enquote{Claims marked as unverified --- 0} misdescribed what it counts.}**
   The row counts `verifybox` blocks; read as written it says no claim in the
   book is marked unverified, which the facing page contradicts. Renamed to
   **Boxes headed \enquote{\lblVerify}** --- the language macro, not the
   literal string, so it cannot drift if the label is reworded. That is the
   mechanism `checkpdf.py` already uses for `\lblNextFrame`.

6. **2418 against 1864, with nothing reconciling them.** One paragraph added
   under the ledger table saying the planned figure is a sum of per-program
   estimates each made before its neighbours existed, so the estimates ran
   high, and that every program is written. **No tally**: the review's
   suggested clause said "all but one came in under it", which is wrong ---
   P24 came in over and P25 landed exactly --- so the sentence states the
   mechanism and no count.

7. **\enquote{Four claims} need a trained model --- there are five.} The
   optimiser comparison (whether an adaptive method beats momentum on a real
   surface, which P20 declines to claim) was missing. Count dropped, fifth
   clause added, and the paragraph now says no count is given and why.

8. **Repository jargon, three phrases.** "in the file the next author reads
   first" is gone --- **and note that the review's suggested replacement,
   "survived on this page", would have been false**, since the sentence was
   never on this page. It now reads "survived five programs after one had been
   run", which is true and needs no artefact. "no pass ever claimed" and "a
   written program" went with the F.2 restructure.

9. **Two rows carrying prose in a numeric column.** The renderings row's "in
   24 rows" moved into the Ledger column; the elicitation row's percentage was
   dropped from the table --- see below.

---

## Retired --- no longer reproduces

**\enquote{968, or 51 per cent} does not reproduce from its own operands.**
True of the reviewed build: 968/1863 = 51.96, and
`code/appf_ledgers.py:148` floors (`100 * elicit // frames`), deliberately, to
match `check_structure.py`'s arithmetic. On current `main` the figures are
**1028/1864 = 55.15**, which floors *and* rounds to 55, so the printed 55
reproduces. The defect as reported is gone.

**It is arithmetic luck, not a fix**, so the structure that produced it was
removed anyway: the percentage no longer sits in the ledger row beside its two
operands. It survives once, in F.4's prose, where the operands are not
adjacent --- so `\val{appf.elicit.pct}` is **still referenced** and C7 stays
green (checked). This is the review's own third option for that row, and it
retires the recurrence: the defect returns for any future rate whose decimal
part exceeds .5.

---

## Recorded rather than taken --- mechanism named

**All four of the manifest's layout findings have ONE cause, and it is one
line.** `\mermaidfig` writes its manifest entry with
`\addcontentsline{dgm}{subsection}{...}` (`preamble.tex:2441`), so the entry is
set by book.cls's `\l@subsection`, which is `\@dottedtocline{2}{3.8em}{3.2em}`
--- **a level-2 contents indent applied to a flat list.** Nothing is nested
under anything, so the 3.8em buys no information and costs about a ninth of the
measure. That lost measure is what makes long entries wrap, hyphenate and lose
their dot leaders. Fixing the indent alone (redefine `\l@subsection` inside
`\listofdiagrams`'s group, or write the entry at `section` level) retires the
review's indent, leader and hyphenation findings together and shortens the list
by about a page.

**Not taken** because it is a preamble constant nobody has measured, and this
column has a documented history of eight overfull-hbox recurrences and a
*falsified* character budget (the P32 pass: 153 of 284 manifest lines are at or
over the recorded 48-character budget and none of them overflows, because the
column wraps). Widening it is very likely strictly safer --- and "very likely"
is a reading of a mechanism, which this book's own rule keeps as judgement
until it is run.

**The `\listofdiagrams` heading level.** `preamble.tex:2434` sets
`\section*{\lblDiagramManifest}`, the same size, weight and colour as the
numbered `\section` above it, so \enquote{Diagram manifest} could be a new
section or a caption --- ambiguous across four and a half pages. One level down
fixes it; same preamble/pagination reason as above.

**The manifest copy's style split, and two wrong descriptions --- neighbouring
files.** Measured with a brace-matching parser over all 150 English entries:
**12 end in a full stop and they are the early ones.** F01--F04 entries are
capitalised full sentences (`programs/en/F01-numbers-powers-roots.tex` writes "Nested number
sets, with the machine's floating-point set shown as a finite subset of the
rationals.", ~100 characters); everything from f05 on is a lower-case fragment
("what saturation costs", 21). The long early ones are also the entries most
likely to wrap and lose their leaders, so this compounds with the indent.
15 edits per edition, all in F01--F04's `\mermaidfig` third argument.

**And one is not a style problem but a wrong description**, confirmed exactly:

- `programs/en/F13-accumulation.tex:526` and
  `programs/pl/F13-accumulation.tex:520` give
  `f13-weighted-average` the manifest copy **"from a sum to an integral"** /
  **"od sumy do całki"** --- which is `f13-sum-to-integral`'s subject (line 184,
  and line 180 in the Polish). The figure's own caption says "An average, weighted, with
  the weighting done by a density", so the manifest line names the one thing
  the figure is not about, and the two entries are duplicates.

F13's review issue is already merged, so nobody may be holding that file ---
but it is another unit's file and this pass did not touch it.

**Later manifest copy that only re-spells its own stem** --- same files, same
mechanism, a reading job over the third arguments.

**A blank verso carries a running head** (p1134). Book-wide preamble
(`\cleardoublepage` issuing `\thispagestyle{empty}`), found and deliberately
left in the F04 review pass for the reason recorded there; nothing about this
unit changes that.

---

## For the sync session

- **No frame length changed anywhere.** Appendix~F has no frames, and no
  program file was touched --- so **there is no cue walk owed by this pass.**
- **The appendix's own length grew**: F.2 gained a fourth table and two
  explanatory sentences, F.3 gained one paragraph. An appendix is appended, so
  this moves no page boundary in the body; expect the four page counts to move
  by the appendix's own growth and nothing else.
- **Three table columns widened**: the \enquote{Where} columns now carry
  "Program 20" rather than "20", so the `X` column beside each narrows. Widest
  new cell is "Programs 25 and 32", ~18 characters, in an `l` column; no
  unbreakable run was added and no `\code{}` or maths span went near a margin.
- **Values: none emitted, none retired.** `appf.tex` is not stale from this
  pass.
- The elicitation-rate ledger is unmoved at 1028/1864; the pass converted
  nothing and added no frame.
