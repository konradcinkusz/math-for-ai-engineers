# Appendix E review hand-off — issue #172

> There is already a `notes/handoff/appE.md` in the tree, from the **#51** pass
> (the E.5 rigour route index). It is a different, unfolded hand-off and this
> file deliberately does not overwrite it.

`0 blocker · 2 major · 9 minor · 4 nit`. **Nothing was retired**: all fifteen
findings reproduce against current source, which is worth stating because the
last several batches each retired two or three. The reason they survived is
that the only change to this appendix since the reviewed build (`9402620`) was
the **addition of §E.5** under #51, and §E.5 touches none of the fifteen.

**But the page numbers in the issue are stale, and that matters for the two
layout findings.** §E.5 added three tables and a note box after the material
the review read, so the appendix is longer than the build the reviewer
measured and every PDF page number in the issue (1119–1126) now names a
different leaf. Re-locate the two layout defects on a fresh build; do not look
them up at the cited pages.

---

## THE FINDING: the suggested fix for the major layout defect names a mechanism that is not there

Finding 1 (🟧, stranded lead-in on a half-empty page) is real and I have not
taken it. Its suggested fix is *"if the float placement is what pushes it,
declare the second table `[t]` on p1124"*.

**Nothing in §E.3 floats.** The three tables are
`\begin{center}\begin{tabularx}...` — not `\begin{table}` — so there is no
float to place, `[t]` is not available, and the diagnosis that a float pushed
the lead-in down is wrong. What actually happens is the ordinary one: a
`tabularx` is a `tabular`, which is **an unbreakable box**, so when the second
table will not fit in the room left, TeX breaks the page in front of it and the
introducing paragraph stays behind on a page it has already half filled.

That is the same shape as the transcript-splitting defect the F08–F11 batch
fixed, and it has the same remedy: **a room test on the block, sized by boxing
it** — measure the table into a box, compare against `\pagegoal-\pagetotal`,
turn the page when it does not fit, excluding `\maxdimen` (a fresh page) the
way `\begin{fr}` and `\section` already do. `\needspace` will not do it, for
the reason `preamble.tex` already records: on a rigid page every candidate
break is equally awful, so TeX keeps the material and lets the block go
overleaf anyway.

**Recorded rather than taken because it is a room test and I am forbidden to
build.** A room test turns pages, and the F08–F11 batch measured exactly what
that costs: its transcript guard cleared a defect no editorial fix could reach
and put three orphaned cues and three orphan tails back doing it. That cost has
to be measured in isolation — one build with the prose and no guard, one with
the guard and nothing else — and I can measure neither.

One thing that makes it cheaper than the transcript guard was: this appendix is
**after every frame in the book**, so a guard here can strand no cue and move
no frame tail. Only the back matter's own pages move.

---

## Fixed, both editions

**Finding 2 (🟧) — the E.4 warning box's universal.** Confirmed by listing both
sections: `Strang`, `Deisenroth, Faisal and Ong`, `Goodfellow, Bengio and
Courville`, `Murphy` and `Bishop` all appear in §E.1 with a full verdict and
again in §E.4 under a box saying *"The list below was not [read and
compared]"*. Fixed in **three places, not one** — the box, the chapter's own
introduction (*"a list of names with no verdicts attached"*), and the file
header comment, which made the same claim about the file.

The fix **states the rule and never a count**, per this book's own standing
prohibition: *where a name below appears in §E.1 too, its verdict stands; the
rest were not read and compared.* Writing "five of the names below" would have
been the tally class in the paragraph correcting a universal.

**Finding 3 (🟨) — "the Fourier transform beyond a mention".**
`grep -rni fourier programs/` returns **zero**. The row now reads *"which this
book does not mention"*. I did not take the alternative fix (add the mention to
F08), because that edits a merged program from inside a back-matter pass.

**Finding 4 (🟨) — "it cites a published review for every quotation".** One of
the two quotations names MAA; the other is *"a reviewer's description"*, and
`notes/02`'s Sources section carries **only a bookstore URL** for Murphy, so
there is no named review to give. The promise is replaced by the disclosure:
*where a quotation here is not attributed to a named review, that is because
the record behind it does not name one.*

**Finding 5 (🟨) — "the most valuable sixty pages".** I could not verify
eighteen either, and I did not try: `notes/02` §1.2 states sixty with no page
count in its Sources entry, so it is **a remembered number**, and the rule is
to drop it rather than swap it for another number nobody here can check. The
sentence is now *"the most valuable chapter in this whole survey"*, which is
true under any count.

**Finding 6 (🟨) — no pointer for floating-point arithmetic.** The gap is real:
`grep -rniE "goldberg|muller|handbook of floating|overton|what every computer
scientist"` over `notes/`, `programs/`, `appendices/` and `frontmatter/`
returns **nothing**. So the issue's suggested fix — add Muller and Goldberg —
**is not available**: the repository has read neither, and inventing a pointer
is the exact move the E.4 box tells the reader to refuse.

What I did instead is what this appendix already does elsewhere: **admit the
gap**, using §E.5's own established *not surveyed* register. §E.4 now says that
no source for floating-point arithmetic itself was surveyed, and names the
neighbouring row in §E.3 without claiming it answers the question. Anyone who
reads Muller or Goldberg can turn this into a pointer in one line.

**Finding 7 (🟨) — "this book made that framing mainstream".** `notes/02` §1.3
says the same words, where "this book" means Strang's; imported into an
appendix where "this book" means *Mathematics from Zero*, it says the book made
SVD-centric linear algebra mainstream. The claim carries no source either way,
so the clause is gone and *"Putting the SVD at the centre of gravity is exactly
right"* stands alone.

**Finding 8 (🟨) — "requiring two years of mathematics … is empirically
false".** A requirement cannot be false. Now *the claim that two years of
mathematics must come before anyone may train a classifier kept people out of
the field, produced nothing, and is empirically false* — which also retires
`gatekept`, a US back-formation in a book committed to British English.

**Finding 11 (🟨) — Lee gives no pointer for category theory.** Confirmed: Lee
is a manifolds book and the row names three subjects. Fixed **without inventing
a source**: the *Where to go* cell is now `Lee, for the geometry` and the *Why
not* cell says no source here was surveyed for the category theory.

Note the geometry of that choice. `Lee, for the geometry` is 21 characters and
the column's width is already set by `Shalev-Shwartz and Ben-David` at 28, so
**the cell grows and the table does not** — which is why this fix was available
where finding 10's is not.

**Finding 12 (🟨, part) — unattributed superlatives.** I bounded the two that
are falsifiable claims about the world at large: *"the best-designed applied
linear algebra text **there is**"* → *in this survey*, and *"do something **no
book** does"* → *the books here do not*. I left *"the finest expositor of
linear algebra alive"* and *"the single best-organised map of the territory"*
as stated judgements inside a section whose heading declares it is giving
verdicts; flattening all four would cost the appendix the voice the same review
calls its best feature. Recorded here so the next pass decides rather than
rediscovers.

**Finding 13 (⬜) — the embedded question.** Now set as §E.2 already sets it:
*two questions — what already exists, and what does each do well and badly for
this reader?*

**Finding 14 (⬜) — Murphy, one volume or two.** `notes/02` §1.7 names both
volumes and the appendix had collapsed them. The heading now reads *the 2022
introduction and the 2023 advanced volume*, and the count is *over a thousand
pages across the two*. (C12 went 10 → 12 numeric literals, matched in both
editions.)

---

## Recorded rather than taken, with the mechanism

**Finding 1 (🟧) — the stranded lead-in.** A room test on an unbreakable
`tabularx`; see above. Not a float.

**Findings 9 and 10 (🟨) — the two §E.3 tables' geometry, and their bare
surnames. These are one job, and the issue's diagnosis of the first is wrong.**

The two tables carry **identical** column specifications — both are
`{@{}XXl@{}}`. What differs is the *rendered* width, because `l` is a
natural-width column and the two tables' `Where to go` cells differ in length,
which leaves the two `X` columns different widths in each. So *"give both
tables one shared column specification"* is a no-op as stated; the fix is to
replace `l` with a fixed-width column so the two agree, widen `Why not`, and
set it `\raggedright` with `\hyphenpenalty` raised (tabularx's `X` is justified
by default, which is where `mathem-atics` and `Four-ier` come from).

That is also the **precondition for finding 10**: titles cannot be added to
`Where to go` until the column can hold them, and every one of those changes
alters the height of a block that cannot break. A `tabularx` is an unbreakable
`tabular`, so a taller one is an overfull vbox rather than a page turn, and
only a build says which. Both need one measured pass, in all four formats.

**Finding 15 (⬜) — the blank verso carries a running head.** A preamble change
to `\cleardoublepage`, and this repository's longest-standing recorded item: it
was found and deliberately left in the **F04 review pass**, and every review
batch since has re-recorded it. It is not Appendix E's.

---

## Sources corrected, so the fixes are not re-seeded

Four of the defects above were imported faithfully from the two documents this
appendix is assembled from, so fixing only the page would have left the next
importer to put them back.

- `notes/01-curriculum.md` §13 — the Fourier row (`beyond a mention`, with the
  grep that settles it recorded in the row), and the Lee row.
- `notes/02-grounding-and-traps.md` §1.2 — *sixty pages*, dropped with a
  bracketed note saying why it was dropped rather than replaced.
- `notes/02-grounding-and-traps.md` §1.10 — the same *requirement … is
  empirically false* construction.

Both edits sit in sections no program pass touches (§13; §§1.2 and 1.10), so
the merge risk against parallel units is low. **`notes/02` §1.3's *"this book
made it mainstream"* was left alone**: in the source's own context it means
Strang's book and is not wrong there. Only the import was.

---

## What the sync session needs

- **No frame anywhere changed length, so no cue walk is owed for this branch.**
  Appendix E is appended after every frame in the book; the recorded reason the
  Appendix C, D and F passes each cost nothing on the cue and orphan-tail
  ledgers applies unchanged here.
- **The appendix did get longer**: typeset lines 449 → 468 (English) and
  455 → 473 (Polish), most of it §E.4's new paragraph and the widened warning
  box. Expect the back-matter page counts and Appendix F's opening page to
  move, and re-measure §20's table from the part-title pages rather than
  subtracting.
- **No values were emitted or retired.** `figures/values/` is untouched and
  `appf.tex` needs nothing from this branch.
- **Nothing was found in a neighbouring program.** Every claim §E.3 and §E.5
  make about a program was re-checked against the written program and all of
  them hold; the only cross-file defects were in the two notes documents above.

---

## Two instrument notes, both cheap and both cost me something

**`awk '{print length}'` counts bytes, and Polish diacritics are two bytes
each.** It reported the Polish file's longest line as 89 where Python reports
81, so the width cap I set from it was eight characters too loose. Measure
source-line width in Python, not in awk, on any file with non-ASCII in it.

**An assertion on the text you insert is not an assertion on the line the file
ends up with.** My substitution script asserted every line of every replacement
was within the cap and passed — and one replacement ended mid-line, so the
tail ran on and left a 96-character line that the prose detector caught. Assert
on the **resulting file**. It is one more line of code and it is the difference
between checking your input and checking your output.

The detector's remaining flags were the recorded two-instrument false-positive
pattern: `Tamta`, `dodaje`, `tamta`, `returns`, `remembered` — ordinary words in
newly added prose, each read and each correctly spaced, with the line-length
instrument reporting zero for all five. It was watched refusing on empty input
(`no files given -- refusing to report a clean tree`, exit 1) before its clean
answers were believed.

---

## Gates

Run before the edits and again after, none of them needing a build:

```
parity.py                    56 file pairs | 1866 frames | 0 failures, 0 warnings
check_structure --frames --answers --outcomes --values --elicit
               --scripts --terms --parts                        exit 0
check_structure --rigour     14 programs defer outside the book; every one answered
gen_stubs.py --check         47 programs, 2418 planned frames; current
make numbers                 exit 0
make verify                  all computed output current
```

`parity` came back clean on its **first** run after the Polish edits, C12 going
10 → 12 numeric literals with both editions matched. `make verify` reported
nothing stale, `appf.tex` included, because this branch emits and retires no
value.
