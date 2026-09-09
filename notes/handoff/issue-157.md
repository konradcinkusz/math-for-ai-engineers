# Issue #157 --- 114 elicitations answered on the facing recto

Reviewed against `main` at `c9b8bb6`. The issue was filed against `9402620`,
and `git merge-base --is-ancestor 9402620 c9b8bb6` confirms it, so every
finding was read against current source before anything was touched.

**The mechanism survives in full and every number in the issue is stale.**
Those are two different statements and the pass turns on keeping them apart.

## What could not be measured here, and why that is not fatal to the finding

This container has **no TeX and no poppler** --- `pdflatex`, `latexmk`,
`pdftotext` and `pdfinfo` are all absent --- so no page-level reading of the
book was available at any point, and the sync session owns pagination anyway.
Nothing below is a claim about where a page breaks.

It does not need to be. The issue's own argument is structural and it holds:

- **C16 makes the cue an iff.** `tools/parity.py:639` states the rule in as
  many words --- a frame carries `\nextframe` exactly when the next frame
  opens with `\ans` or `ansblock` --- and it is green on all 56 file pairs. So
  *a page whose last line is the cue is followed by an answer* is a property
  of the source, not an observation about one build.
- **`check_structure.py --frames` makes the cue the last thing in its frame**,
  and `\nextframe` sets it as its own `\raggedleft` paragraph
  (`preamble.tex`). So "the last line of the block is the cue" is exactly
  "this page ends by asking".
- **The margins are mirrored**, so a verso's answer opens the facing recto.
  `tools/checkpdf.py:text_blocks` already measures the two block edges
  separately and its docstring records 51 pt against 62 pt in the trade
  format.

What is stale is every count. The issue read 968 cues in a 1140-page A4
build; `--elicit` now reports **1030** in 1866 frames, and CLAUDE.md's page
table has `main-en-a4` at 1200. The 220 / 114 split, the per-program table and
the thirteen verbatim folios are all measurements of a book that has since
grown, and none of them was re-taken. **Do not quote them.**

## Fixed --- an instruction whose extent was wrong (both editions)

Six frames printed, immediately above a question, a `\dotline` and a cue:

> Cover the rest of the page. / Zasłoń resztę strony.

The thing that has to be covered is **the next frame**, and on a verso the
next frame is the facing page. So the instruction names the right hand and the
wrong extent, and it is wrong exactly in the case this issue is about: a
reader who does what the page says, on a verso, has the answer in view.

The correct wording was already in the book, in both languages, in the front
matter's own non-negotiable rule --- `frontmatter/en/how-to-use.tex:18`
*Cover the next frame before you read the current one to the end*, and
`frontmatter/pl/how-to-use.tex:19` *Zasłoń następną ramkę*. The body now says
what the front matter says, rather than inventing a second phrasing.

Twelve sites, six per edition, one for one:

| | English | Polish |
|---|---|---|
| F02 | 565, 845, 998 | 572, 853, 1008 |
| F03 | 263, 529, 1003 | 276, 542, 1021 |

A sweep of every `.tex` in the tree (`programs/`, `appendices/`,
`frontmatter/`) finds no thirteenth site and no other reader-facing
instruction that depends on the leaf.

## Fixed --- the ledger nobody could see

The issue's second remedy, taken. `tools/checkpdf.py` gains **defect 5: the
cue at the foot of a verso**, reported and never fatal.

It answers the issue's sharpest point, which was verified by reading the tool
rather than taken on trust: a full verso ending on the cue is **healthy by all
four existing checks**. It is not a cue alone (defect 2 requires the cue to be
the only thing below the running head), its ink reaches the foot of the block
(defect 4 requires fill below `FILL_FLOOR`), and nothing is stranded (1, 3).
It was the one defect of the five that nothing in the repository could see.

Three decisions worth knowing about:

- **Parity is measured, not assumed.** Page 1 of the file is a recto, so even
  PDF pages are versos, and that is true of every book this repository has
  built --- but the tool's habit is to learn from the artefact rather than
  assume, which is why `text_blocks` survived the day A4 was added. The new
  `verso_parity()` reads it off the mirrored block edges, which `text_blocks`
  has already taken. When the two parities are indistinguishable it returns
  `None` and the tool **refuses and fails**, on the same reasoning as the
  empty-cue-set and zero-heading refusals: reporting no verso cues would be a
  false reading rather than a clean one.
- **Defect 2 and defect 5 are kept disjoint.** On a cue-alone page the
  question is not on the page at all --- it is on the leaf before, which the
  reader has already turned --- so the answer opposite is not in view beside
  its question. That is a different reader's complaint, it is what makes
  defect 2 a hard gate, and naming one page under two diagnoses would make
  both ledgers harder to read.
- **Pages are not listed; the count and the rate are.** Unlike the orphan
  tail, there is nothing an author can do page by page, so a list is not
  actionable. Both numbers are printed because they say different things: the
  count is elicitations spent and grows with the book, and **the rate is near
  a half by construction** --- page parity is independent of where a frame's
  tail lands --- so a rate near a half is the null result and only a
  structural change moves it.

### It was watched producing answers already known

No poppler, so it could not be run on the book. It was driven instead through
its own code path on synthesised `pdftotext -bbox` output --- ten pages with
mirrored margins, running heads, a calibrating section heading, two versos and
one recto ending on the cue, and one verso carrying the cue alone:

| probe | expected | got |
|---|---|---|
| as built | verso = even; ends 2, 3, 6; versos 2, 6 | as expected |
| margins mirrored the other way | verso = odd; versos 3 | as expected |
| margins not mirrored | refuses, `verso = None` | as expected |
| page 2 stops ending on the cue | ends 3, 6; versos 6 | as expected |
| the cue-alone verso gains a question | it becomes a defect 5 and stops being a defect 2 | as expected |

The second row is the one that matters: it proves the parity is read off the
page rather than inferred from the file's first leaf. `main()`'s reporting and
its refusal branch were exercised too, and the refusal exits 1.

**The probe is disposable and is not in the tree**, on this repository's own
habit. What it establishes is that the instrument looks at something and can
tell a verso from a recto; **it establishes nothing whatever about the book.**

### And then CI took the first real reading

The four builds on this PR ran it on the book. `main-en-a4`:

> `121 of 230 pages that END ON THE CUE are versos (53%), reported not fatal`

Three things follow, and only the first two are worth anything. The check
**runs on the real artefact without crashing**, and its fatal refusal branch
**did not fire** --- so verso and recto were told apart in every build, as the
geometry says they must be (A4's `inner`/`outer` differ by 17.0 pt and the
trade format's by 11.4 pt, against a 2 pt slack). And the reading is
**plausible rather than degenerate**: 53%, which is the null half, and not the
0% or 100% a broken parity test would give.

**The third thing is the count, and it is not a finding.** It is a pagination
measurement, so it is void on the next merge --- which is exactly why the sync
session owns it and why it is quoted here as an instrument reading rather than
entered in a ledger. What is worth noticing is only that it lands where the
issue said it would: 121/230 against the issue's 114/220 on a book that has
since grown by 62 cues.

### One pre-existing wart, fixed because this PR made it noise

CI printed `checkpdf.py:291: SyntaxWarning: invalid escape sequence '\c'`
above the check's own output. It is **pre-existing on `main`** (line 238
there), one docstring carrying `\cleardoublepage` where every other backslash
in the file is escaped, and it was invisible locally because Python emits that
warning at compile time only and `__pycache__` was hiding it --- an instrument
returning a plausible clean answer, which is the theme of this pass. One
character, and it is in scope because the warning now prints directly above
defect 5's ledger.

The probe's first run failed, and the failure was mine rather than the tool's:
my synthetic body lines were not justified, so the mode of the words' `xMax`
was the end of the commonest first word instead of the block's right edge, and
the right-aligned cue fell outside the block. Worth knowing for anyone
synthesising a page for this tool --- `text_blocks` assumes justified prose.

## Recorded rather than taken --- the parity-aware room test

The issue's first remedy, and the one that would actually fix the defect
rather than count it. Recorded in `preamble.tex` beside `\nextframe`, where
this repository already keeps the four failed attempts on the neighbouring
defect, so the next person meets it with the reasoning rather than
rediscovering it.

**The mechanism.** Give `\dotline` the room test `\begin{fr}` and
`\mfa@sectionroom` already have --- measure `\pagegoal - \pagetotal`, turn the
page when the cue will not fit --- but **arm it only on an even page**, so the
cue that would have ended a verso starts a recto instead and the paper does
the covering.

**Why it is not taken here.** It turns pages. Page counts, orphaned cues and
orphan tails all move with it, and it has to be swept against all four builds
and then against CI, which paginates differently. That is a book-wide layout
change nobody has measured, and this container cannot build the book at all.

**What whoever measures it must not do**, and it is the reason this is
recorded rather than merely deferred: the table already in `preamble.tex`
prices the **unconditional** version of the same guard --- two cues became
eight tails and six pages --- and it is tempting to read that table as a
verdict on this one. It is not. The parity-aware version fires on about half
as many pages, and it buys something the unconditional version did not: a page
turned here moves the answer **behind the leaf** rather than merely lower on
it. That is a different trade, and the tails it costs have to be weighed
against elicitations it saves rather than against cues it silences.
`checkpdf.py` now prints the number that would move.

## For CLAUDE.md --- a rule this falsifies, and two quotations it makes stale

I may not edit CLAUDE.md; these are for whoever writes the pass note.

**1. The rule at CLAUDE.md:380 is falsified.** *Non-negotiable conventions*
ends its pagination paragraph:

> *Cover the rest of the page* is fine; it names the hand, not the leaf.

It names the hand correctly and the **extent** wrongly, and the extent is a
statement about the leaf. This is the F02 review pass's own finding one step
further out: that pass fixed *before you turn over* and left this, on the
reasoning that only the first mentioned a leaf. Both do. The replacement is
already in the front matter and is now in the body: **name the frame, not the
page** --- *cover the next frame* is true under every pagination, and *cover
the rest of the page* is true under half of them.

**2. Two passages now quote wording that no longer exists.** CLAUDE.md:354 and
CLAUDE.md:1375 both paraphrase F02's frame as *cover the rest of the page and
write down the expansion of (a+b)^2 as fast as you can*. Both are narrative
prose inside pass notes about figure placement, and the point each makes is
untouched --- 1375's *covering the page does nothing when the spoiler is above
the covering hand* is this issue's own mechanism from the other direction.

## Neighbouring things found and deliberately not fixed

- **`preamble.tex:1031` and `:1055`** describe `\nextframe` as *the
  instruction to cover the page and turn over*. That is the mental model this
  issue falsifies, and it is right on a recto and empty on a verso. Left as
  written and **answered immediately below them** by the new block, rather
  than rewritten, because both sentences trace the wording to notes/07.
- **`notes/07-stroud-original-layout.md` §3** records the same phrase. Left
  alone: it is a faithful description of the photographed original, not a
  claim about this book. Whether Stroud's own editions carried the same verso
  exposure is **unknown here** --- there are no photographs in the tree --- and
  it is worth an hour of somebody's time, because the answer decides whether
  this is an inherited defect or one this book introduced.
- **`appendices/en/appE-further-reading.tex:219`** lists *the frame, the answer
  overleaf, the Quiz...* among the devices borrowed from Stroud. Considered and
  left: it names a device, it is not an instruction to the reader, and *the
  answer overleaf* is the right name for the thing.

## For the sync session

**Frames whose length changed: six, three in F02 and three in F03, in both
editions.** English loses six characters at each site (18 per program) and
Polish gains one (3 per program). That is far less than a line in either
direction and it is still not nothing: a few characters move a break when the
line was nearly full, and the break carries the rest of the program with it.
**Walk the cues.** No frame was lengthened or shortened deliberately and
nothing was trimmed to move a page --- which would be the wrong move here in
any case, for the reason in the recorded section above.

**No value was emitted or retired**, no transcript was touched, no figure was
moved or reworded, and no frame, outcome, Quiz route or Summary bracket
changed. The elicitation ledger is unmoved at 1030/1866.

`figures/values/appf.tex` was **not** stale on this tree: `make numbers`
regenerated `figures/values/` byte-identically, so there is nothing there for
you to reconcile from this branch.

## Gates

Run before anything was touched and again after. All green, all on the first
run afterwards:

- `parity.py` --- 56 file pairs, 1866 frames, 0 declared divergences, 0
  failures, 0 warnings. C4, C8, C12, C14 and C16 all clean on F02 and F03 in
  both editions: the edit is prose only, and it carries no maths span, no
  numeric literal and no macro, so there was nothing for the ordered checks to
  diverge on.
- `check_structure.py --frames --answers --outcomes --values --elicit
  --scripts --terms --parts` --- clean. 88 transcript references, 84 Polish
  renderings, 9 part ranges, 1030/1866 frames elicit.
- `gen_stubs.py --check` --- 47 programs, 2418 planned frames, current.
- `make numbers`, `make verify`, `make debt` --- clean, nothing stale.
- `reflist.py` needs a build's `.aux` files and was not run.
- **No PDF was built and no page-level ledger was read**, by instruction and
  by the absence of a toolchain. The overfull multiset, the page counts, the
  orphaned-cue walk, the orphan-tail ledger and the first real reading of
  defect 5 are all the sync session's.

## One instrument note

`grep -n "names the hand, not the leaf" CLAUDE.md` returns **nothing**, and
the sentence is there: it wraps across lines 380 and 381. A line-oriented
search cannot find a phrase that wraps, which is the same instrument defect
the P25 pass recorded for *zanim pójdziesz dalej* and the P14 batch recorded
for the `polsko-` hyphen. The rule is cheap and it is not yet written down
anywhere it would be read: **a phrase-level claim about this book's prose
needs a phrase-level search**, over the file rather than over its lines.
