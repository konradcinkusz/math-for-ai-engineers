# Issue #117 — one kind of answer, two boxes

*[Review][UX] One-sentence answers are boxed two different ways, so the edge
the reader covers with a hand keeps moving.*

Book-wide UX finding rather than a program's. Verified in full, measured
book-wide, **one deliverable shipped and both of the issue's proposed fixes
recorded with their mechanism**. No frame was lengthened or shortened, no
`\val{}` was emitted or retired, and no page can have moved: everything in the
diff is a Python check, a Makefile target, and comments.

---

## Every finding, and what happened to it

### Confirmed, exactly as reported

**F08 frames 2, 3, 4.** `ansblock` / `\ans` / `ansblock`, three consecutive
frames, three answers of the same kind, at `F08-trigonometry.tex:141`, `:151`,
`:179`. This is the strongest instance in the book and it is what the issue
leads with.

**F08 frames 23 / 25, 26 and 27 / 28.** Confirmed as alternations in source
order — 23 `ansblock`, 25 and 26 `\ans`, 27 `\ans`, 28 `ansblock`.

**P04.** Every frame number in the issue is right: frames 2, 3, 25, 31, 33 are
`ansblock` and frames 7, 11, 13, 17, 20, 22, 29 are `\ans`.

**P20.** `\ans{Adam}` at `:493` is the **only** `\ans` in the program, against
19 `ansblock`s — including `$\val{p20.sched.after}$.` at `:787`, a bare value
(`1e-6`) set across the measure, and *The expression it appears in, not the
number.* at `:430`. A single word narrow and centred; a single number full
width and left-aligned, in one program.

### Confirmed but understated — the corpus is much larger than the sample

The issue judged 19 of 55 units and found it in three. Measured over all 47
programs, in both editions:

| | count |
|---|---|
| `\ans{}` | 543 |
| `ansblock`, one paragraph and no display — *the class the issue names* | **378** |
| `ansblock` carrying a display, list, table or listing, or >1 paragraph | 112 |
| programs that set a plain one-sentence answer **both** ways | **43 of 47** |

The two treatments overlap across the whole range where one-sentence answers
live: between 40 and 80 characters there are 138 `\ans` and 137 plain
`ansblock`s — a dead heat.

And the poles say what the variable really is. **P19 has 0 `\ans` and 17 plain
`ansblock`s; P29 has 19 `\ans` and 0.** Each is internally consistent, and
each is consistent with the *opposite* convention. The treatment is a property
of which pass wrote the program, not of the answer. (P18 and P30 are the other
two non-mixers, one each way.)

### Corrected: two of F08's eight are not instances

The issue says *"Eight `ansblock`s in `F08-trigonometry.tex`, all one-liners."*
Eight is right; **all one-liners is not**. Frames 6 and 9 (`:226`, `:302`)
carry a displayed equation — `\[ \cos^{2}\theta + \sin^{2}\theta = 1 \]` and
`\[ \cos\theta = \sin(\theta + \frac{\pi}{2}) \]` — which is precisely what
the preamble reserves `ansblock` for. **Six of the eight are actionable, not
eight.** It is the difference between counting by eye and counting by the
preamble's own predicate, and it is why the ledger's column is
plain-against-worked.

### Could not be checked: the page-level claims

*"the same alternation on p226 (frames 9, 10)"* — frames 9 and 10 are **both**
`ansblock`, so there is no alternation between those two in source. Whichever
`\ans` shares p226 with them (frame 5 or frame 12) I cannot determine, because
**there is no TeX installation in this container at all** — not `pdflatex`,
not `tex`, no `/usr/local/texlive`. Every page number in the issue is
therefore unverified here, and every source-level claim behind them is
verified. Nothing was changed on the strength of a page number.

### Stale: the P04 source line numbers

The issue attaches *"(source lines 109, 129, 488, 592, 636)"* to the list of
**centred** boxes. In the current file 109, 129 and 636 are blank lines, 488
is a question and 592 is a `\label`; the `\ans` in those frames are at 202,
265, 294, 358, 424, 459, 609, and 109/129 sit two lines above the *`ansblock`*
frames 2 and 3. So the numbers are attached to the wrong half of the sentence
or come from an earlier revision. **The frame numbers in the same sentence are
all correct**, so the finding is untouched and only its line references are.

### Checked and clean — the reverse defect does not exist

No `\ans{}` anywhere in the book carries a display, a list or a second
paragraph. The longest is 226 characters (`P08:436`), which is a matter of
taste and runs in the issue's own direction. And **no `ansblock` anywhere
contains a `\blank` or a `\dotline`** — CLAUDE.md records that a `\blank`
inside an `ansblock` is a defect, and the rule holds book-wide today.

---

## What was shipped (a)

**`make answerbox` / `check_structure.py --answerbox`**, reported per program
and for the book, wired into `make debt` — so it prints in the CI `ledgers`
job's step summary beside the orphan tail and the elicitation rate.

**Reported and never fatal**, on their reasoning: the count is 378, none of it
can be cleared without a book-wide pagination pass, and a gate red on
something nobody can responsibly clear teaches the next person to stop reading
the output.

**No length threshold.** The issue proposed *"no display and under about 120
characters"*; the 40–80 band is 138 against 137, so any cut would be a number
chosen to make a sentence come out — the failure mode this book has paid for
five times. The predicate is structural (a display, a list, a table, a
listing, or a second paragraph) and needs no constant. **It was checked for
sensitivity rather than assumed**: adding `array`, `cases`, every matrix
environment, `\dotline` and `\blank` to the marker list moves neither figure by
one, because not one of them occurs in an `ansblock` body anywhere in the book.

**Watched producing known answers before being believed**, in both directions:

| mutation | result |
|---|---|
| one plain `ansblock` → `\ans`, both editions | 543/378/112 → 544/377/112 |
| a plain `ansblock` gains a `\[` display | 543/378/112 → 543/377/113 |
| restored | 543/378/112 |

A second, independently written survey script agreed with the ledger to the
unit on all three figures before either was trusted.

---

## What was recorded rather than taken (b), and the mechanism

**Both of the issue's proposed fixes are book-wide layout changes nobody has
measured**, and neither can be measured here.

- *Convert the 378 plain `ansblock`s to `\ans`* — 756 edits across both
  editions, each changing a box from full-measure/left/**breakable** to
  0.86-measure/centred/**unbreakable**.
- *Give both treatments the same width and alignment* — two `tcolorbox` keys,
  changing the geometry of 490 or 543 boxes at a stroke.

**Read out of `preamble.tex` (not measured — there is no TeX here):** both
inherit `mfa answer`, so `before skip=4pt` and `after skip=10pt` are the same
and only the geometry differs. `\ans` is `left/right=8pt, top/bottom=5pt,
width=0.86\linewidth, center, halign=flush center, unbreakable`; `ansblock` is
`left/right=10pt, top/bottom=6pt`, full measure, `breakable`. So **every
conversion changes the box height** — by 2pt of padding even for a one-liner,
and by a line for every six on anything that wraps. Hundreds of height changes
move every page break in the book, which is why this needs the four-format
build, the overfull multiset, the orphan-tail ledger and a cue walk, and why
it is a pass of its own. A measurement taken here would in any case be void on
the next merge, with several sessions running in parallel.

**Which way it resolves is not open, and that is the pass's own finding.**
`notes/07` §3 records the original's answer box as *narrower than the measure,
centred… a thing you put your hand over*, and `notes/07` records `ansblock`'s
full width as a **departure**, with its reason stated: *a multi-paragraph
worked answer with displayed maths at `0.86\linewidth` is where the overfull
hboxes would come from*. **That reason reaches the 112 worked answers and not
the other 378**, which carry no display and no second paragraph and so cannot
produce the box the departure was taken to avoid. So the issue's first option
is what the book's own notes already prescribe; the second would spend the one
property `notes/07` §3 records the box for. Recorded in `notes/07` beside the
departure and in `preamble.tex` beside the macro, so whoever takes the pass
meets it rather than rediscovering it.

**Not shipped as a hard lint**, deliberately. The issue asks for one; at 378
instances it would be permanently red on day one.

---

## For the sync session

- **No frame was lengthened or shortened. No cue walk is owed by this branch.**
  The diff is `tools/check_structure.py`, `Makefile`, `notes/07`, and a comment
  block in `preamble.tex`. Nothing in it can move a page.
- No value emitted or retired, so `figures/values/appf.tex` is untouched by
  this branch and `make verify` reported everything current.
- **One durable fact, proved by mutation and worth keeping:** turning a single
  English `ansblock` into an `\ans` fails **C4** (`diverge at token 109 --
  en:141 ANS != pl:142 BEGIN(ansblock)`) **and C14** (`\ans: en=13 pl=12`). So
  the two editions cannot drift apart on treatment, and any conversion pass
  must be done in both editions together or parity stops it. What no check can
  see is both editions being wrong *together* — 378 times, in perfect
  agreement — which is this repository's oldest recorded class and is what the
  new ledger is for.
- Suggested ledger line, if this is folded into CLAUDE.md's list: **543 `\ans`
  against 490 `ansblock`, of which 378 carry no display and no second
  paragraph; 43 of 47 programs set a plain one-sentence answer both ways.**
  Reported by `make debt`, never fatal, on the orphan tail's reasoning.
