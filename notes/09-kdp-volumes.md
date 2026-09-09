# The KDP volume edition

How the book is split into paperback volumes for Amazon KDP, what was measured
to decide it, and which of the decisions are still open.

Everything here was measured on one machine, in one afternoon, at HEAD `3c9392d`.
**Ratios are the durable part; absolutes are not.** That container is a third
TeX installation — its `main-en` came out at 1455 pages against the 1435
`CLAUDE.md` records, and `CLAUDE.md`'s own ledgers were themselves stale at that
commit (57 file pairs and 1866 frames against the 56 and 1864 it printed). So
every figure below is quoted against a baseline built on the same machine, which
is the rule this repository already states for the overfull multiset.

---

## 1. What is additive, and how that is proved

`main-{en,pl}.tex`, `main-{en,pl}-a4.tex`, `body.tex`, `structure.tex`,
`preamble.tex`, `build.yml` and `release.yml` are **not modified**. The KDP
interior is `kdp/preamble-kdp.tex`, which reads `preamble.tex` and then
re-issues `\geometry` and redefines the palette.

There is deliberately no new `\bookpaper` branch: `geometry` accepts a second
`\geometry{}` before `\begin{document}`, and `preamble.tex`'s own
`\AtBeginDocument` badge assertion then validates the **new** geometry, which is
the behaviour wanted rather than a side effect.

The claim that the four existing PDFs have not moved is a claim about
artefacts, so `.github/workflows/kdp.yml`'s first job builds `main-en` on the
merge base and on `HEAD` and fails if the page count or the resolved
cross-reference list differs by one entry. It gates every other job.

### The cross-reference half compared two error messages

**Four things were wrong with that job and every one of them let it pass or
skip rather than fail**, which is the shape worth carrying rather than any of
the four: a guard is the one piece of machinery whose failure mode is silence,
so each defect in it was invisible in exactly the direction that mattered.

The first three are recorded in the commits that fixed them \dash{} it ran on
no event a pull request produces; its base worktree sat in `/tmp`, which a
Docker action does not mount, so it failed on its own scaffolding; and it fell
back to `git rev-parse HEAD~1`, which would have compared HEAD against its own
previous commit and passed.

**The fourth is the worst, and it surfaced only once the first three were
fixed and the compiles actually ran.** The step read

    ( cd "$RUNNER_TEMP/base" && python3 tools/reflist.py > /tmp/base-refs 2>/dev/null || true )

against the same command run at HEAD, and diffed the two. `tools/reflist.py`
does not answer that question. It compares the two **editions** \dash{}
English against Polish \dash{} and this job compiles `main-en` only, so on
both sides it failed on the absent `main-pl.aux` and printed one line:

    FAIL  /home/runner/work/_temp/base/main-pl.aux missing -- build both editions first
    FAIL  /home/runner/work/math-for-ai-engineers/.../main-pl.aux missing -- build both editions first

**The guard's cross-reference half had never once compared a cross-reference.**
It compared two error strings whose sole difference was the absolute path each
tree sat at \dash{} and that difference is the only reason it went red rather
than green. Two trees at one path and it would have passed, having read
nothing.

And it would not have worked even with both editions built, which is the part
that makes this a design error rather than a missing file: `reflist.py`'s
output is a **summary** \dash{} `484 labels in en, 484 in pl, 0 mismatches`
\dash{} so two builds differing by a moved `\ref` print the identical line.
The step's own comment claimed *a KDP change that moved a single `\ref` would
show up here and nowhere else*. It could not have shown up there at all.

`tools/auxrefs.py` dumps `label → number` for **one** tree and is diffed
against itself at the two commits, which is the comparison that was wanted. Two
things about it are load-bearing:

- **It takes the tree root as an argument** rather than deriving it from its
  own location. The base side is a worktree of an older commit, so it does not
  contain this script; HEAD's copy has to be able to read a tree it is not
  standing in. A flag added to `reflist.py` would have been absent exactly
  where it was needed.
- **It refuses an empty answer.** The aux tree is an `\@input{}` chain, so a
  main file whose per-program `.aux` files are missing yields zero labels and
  prints zero lines \dash{} and two empty files diff clean. That is the same
  vacuous pass in a new costume, so it exits 1 instead.

Watched firing before being believed, which is this repository's own rule and
the only reason the replacement is trusted: the same tree twice diffs clean;
one perturbed entry reports `prog:F08 F8 → F9` and fails; a hollow aux tree
and a missing one each exit 1 rather than printing nothing; and HEAD's copy
pointed at a foreign tree returns the identical 495 labels it returns in place.

---

## 2. Ten point, and why it is not a preference

Three measurements agree, and none of them is about taste.

| | trade 17×24 @11pt | 6×9 @11pt | 6×9 @10pt |
|---|---|---|---|
| characters per line | **70.0** | 64.4 | **69.3** |
| whole book, en / pl | 1455 / 1472 | 1524 / 1552 | **1345 / 1349** |
| overfull vbox, en / pl | 0 / 1 | **3 / 2**, to 241.8 pt | **0 / 0** |
| worst overfull hbox, en / pl | 6.1 / — | 31.6 / 29.6 pt | 7.3 / 19.8 pt |

Characters per line is `26 × textwidth / alphabet width`, the standard
instrument; the alphabet was measured at each size rather than assumed
(127.584 pt at 10pt, 137.389 at 11pt, 149.879 at 12pt in Latin Modern).

`preamble.tex`'s own note says both existing formats were set to about the same
measure on purpose, and that eighty-five characters is past the point where the
eye loses the line return. **10pt on 6×9 reproduces the trade measure to within
a character**; 11pt misses it by six, sets the whole book *longer*, and produces
overfull vboxes up to 241.8 pt that 10pt does not.

The ratio is also worth recording because the obvious estimate is wrong: 6×9 at
11pt is **1.05×** the trade format, not the 1.10–1.20× an area model predicts.
The frame machinery's 17 pt + 12 pt per-frame gutter is fixed and does not scale
with the measure, and there are 1866 frames.

---

## 3. The split

Four volumes, each a contiguous run of whole parts, in manifest order. Defined
in `tools/volumes.json` and nowhere else.

| Vol | Parts | Programs | en pp | pl pp |
|---|---|---|---|---|
| I | I | F1–F13 | 426 | 434 |
| II | II, III | P1–P11 | 326 | 330 |
| III | IV, V, VI | P12–P22 | 306 | 308 |
| IV | VII, VIII, IX | P23–P34 | 408 | 414 |

Every volume is inside the 24–828 window with over three hundred and ninety
pages of headroom, and the binding constraint is Polish in every volume, as
expected. **These are the counts after the back matter's tables were made
breakable** (section 9): every volume lost two to four pages, so re-measure them
from the build in front of you rather than quoting them from here.

**A three-volume split also fits** — I (426) | II–V and VI–IX both near 475 —
and saves about sixty pages of duplicated back matter and one book. Those two
figures are derived from the four-volume counts rather than built, and a
derivation is not a measurement: `make census` is what settles it. It is a
product decision rather than a technical one and the pipeline does not care:
change `tools/volumes.json` and run `make volumes`.

---

## 4. The gutter is a fixed point

KDP's minimum inside margin is a function of the page count and the page count
is a function of the inside margin, so `tools/kdpbuild.py` iterates:

| page count | minimum inside margin |
|---|---|
| ≤ 150 | 0.375 in |
| 151–300 | 0.500 in |
| 301–500 | 0.625 in |
| 501–700 | 0.750 in |
| 701–828 | 0.875 in |

It stops after four passes rather than oscillating, because a volume within a
page or two of a bracket boundary can chase itself forever. In practice every
volume converges on the first pass and the two that need a second need it for
page **parity**, not for the gutter.

Parity is settled after the gutter, one direction only: the gutter moves the
page count, and a pad leaf does not move the gutter, so the two cannot chase
each other.

**The safety margin over KDP's minimum is 2 mm, and one of those millimetres is
microtype's.** Character protrusion hangs an em dash 2.99 pt into the gutter —
deliberate optical margin alignment, and still ink a reviewer would measure. At
1 mm the protruded dash came to 0.623 in against a 0.625 in requirement.

---

## 5. Black ink, and where the colour actually was

Every colour application point in `preamble.tex` goes through one of fourteen
named colours, as do the six front-matter files that use them by name, so
redefining the names in `kdp/preamble-kdp.tex` reaches all of them.

Measured after that: **of 1524 pages, 150 still carried a non-gray mark — and
150 is exactly the diagram count.** The LaTeX interior was clean; every offender
was a diagram, carrying the Mermaid config's own palette.

`tools/kdpstage.py` converts all 300 diagrams to DeviceGray with Ghostscript.
Two properties matter and both are checked per file:

* **the page size does not change** — worst difference over all 300 is
  0.0000 pt. This book's figure sizing is a formula in the rendered width, so a
  conversion that resized a diagram would silently invalidate every node-size
  and rule-2 measurement in `CLAUDE.md`;
* **inline colours are caught**. Two `.mmd` sources hard-code their own hex
  values, which a grayscale Mermaid *theme* could not reach.

### The stager refused to do the half of its job that was still owed

`tools/kdpstage.py` does two things: it symlinks the source tree into
`build/kdp/tex`, and it converts the colour diagrams to grayscale. In CI's
per-volume job the second is already done \dash{} `diagrams-kdp` renders and
converts **once** and ships the gray set as an artifact, which `build-volume`
unpacks straight into the staging tree, so eight volume builds do not each run
ghostscript over three hundred files.

The script tested for the **colour** set and returned 1 when it found none:

    no rendered diagrams found -- run `make diagrams` first

It printed that while standing on a complete set of three hundred converted
diagrams, and it skipped the symlink half, which was the only half still owed.
So the volume build failed on the input it had rather than on the one it
lacked.

It is the milder cousin of the other four defects in this pipeline: those let a
guard pass having read nothing, and this one stopped a job that had everything
it needed. **Both come of a check that names one input when the work has two**,
and the fix is the same shape either way \dash{} decide what is actually
missing before deciding to stop.

The colour set present is still the local path and converts as before; absent
with a populated gray stage is the CI path and skips the conversion, saying
`prebuilt` in the log so a reader can tell which branch ran. **Neither present
still stops**, because that is the vacuous pass this file keeps recording.

Proved in every direction before it was believed: the old code reproduces the
CI message byte for byte in the CI state; the new one stages 576 symlinks and
finds 300 prebuilt diagrams there; with neither input it exits 1; and from a
tree shaped exactly as CI's \dash{} fresh stage, gray artifact only, no
colour source \dash{} `kdp-v3-pl` builds to 308 pages, converging on pass 1,
with `checklog` and `checkkdp` both clean. 308 is the same figure the local
build gives.

### Why a staged tree rather than a second path

`\mermaidfig` hard-codes `figures/diagrams/<lang>/<key>.pdf` in both of its
branches, and the KDP work may not edit `preamble.tex`. Two routes were tried:

1. **`figures/diagrams-kdp/`** — needs `\mermaidfig` changed. Out of bounds.
2. **A shadow directory first on `TEXINPUTS`.** `kpsewhich` confirms kpathsea
   resolves the shadowed name, and the book build ignored it: the log says
   `<./figures/diagrams/en/….pdf>`, with the leading `./` that gives it away.
   graphicx opens a name containing a slash relative to the working directory
   and never consults the search path when the file is there. **A shadow cannot
   win against a file that exists.**

So the build compiles in `build/kdp/tex`, where `figures/diagrams` *is* the gray
set and everything else is a symlink — file by file rather than directory by
directory, because `\include` writes `<program>.aux` beside its source and
through a symlinked directory those writes would land back in the real tree and
collide with the trade build's.

---

## 6. Cross-volume references

1521 `\ref{prog:…}` in `programs/en` alone, **729 of which cross a volume
boundary** under this split — 48 %, and 163 of those point forwards. Left alone
every one sets `??` and the unresolved-reference gate rejects the build.

`\ref` is the only reference command in the book — 3467 uses, and zero
`\pageref`, `\autoref`, `\nameref` or `\cref` — so there is one place to act.
**Three things were tried and the first two are recorded because they look
right:**

1. **`\renewcommand{\ref}`.** Broke immediately: hyperref's `\ref` is
   `\@ifstar`-aware and a naive redefinition consumes the wrong token. The build
   died with `Missing \endcsname inserted` and an undefined reference to
   `\reserved@d`. Do not intercept `\ref`.
2. **Supplying the label with an empty anchor.** Correct, and noisy: hyperref
   logged `Suppressing link with empty target` 257 times in one volume.
3. **What is in the tree:** supply the label, anchored at the volume's own
   series map. `\ref` resolves normally, so it *cannot* raise an unresolved
   reference — the gate stays meaningful instead of being worked around — and
   the link goes to the page that says which volume the target is in, which is
   the only honest destination when the target is in another book.

Measured: **0 unresolved references and 0 empty-target warnings across all
sixteen volume builds.**

`xr` is deliberately not used: it would make each volume read its siblings'
`.aux` files, imposing a build order and breaking the parallel matrix.

**The tag must carry a break opportunity.** Written `#2\,(\lblVolume~#3)` it is
one unbreakable run, and on the narrower measure it produced the four worst
over-budget hboxes in the prototype — 43.4, 30.5, 29.3 and 18.6 pt, every one of
them the tag itself rather than the book's prose. `\allowbreak` before the
parenthesis took three of four English volumes from failing `checklog.py` to
passing with no page count changed.

Polish inflects the noun *before* the reference across six cases —
*Program*, *Programu*, *Programie*, *Programy*, *Programem*, *Programowi* — so a
parenthetical tag after the number needs no grammatical agreement. That is the
thing that would have sunk a naive design.

---

## 7. Numbering is positional, and that is the quietest trap here

`\mainnumbering` sets the chapter counter to 0. A volume starting at Part IV
would therefore call P12 **“Program 1”** — silently, and every Summary bracket,
Quiz route and cross-reference in the series would then be wrong.
`tools/gen_volumes.py` emits `\setcounter{chapter}{11}` for that volume, which
is the whole reason the structure file is generated rather than assembled.

---

## 8. What the back matter does per volume, measured

| appendix | per volume | why |
|---|---|---|
| A answers | **scopes itself** | accumulated as programs are typeset: 22 pp in Volume III against 94 for the book |
| B notation | carried whole | four pages of reference matter |
| C formulae | **scopes itself** | same mechanism as A: 18 pp against 70 |
| D terminology | carried whole | ten pages |
| E further reading | final volume only | series back matter |
| F manifest | final volume only | series back matter |
| index | **scopes itself** | 101 entries and 2 pp in Volume III against 7 pp for the book |

Three of the seven need no configuration at all, which is worth knowing because
it is the opposite of what the plan assumed. It also means **a Volume III reader
cannot get the whole book's formula reference** — a product decision that is
still open. Accepting per-volume scoping is what is in the tree.

### Two checks that need no volume mode

* **`--terms`.** Scoped to one volume it would fail on 11–15 of the 42 glossary
  renderings, because they are used in *other volumes'* programs — `perpleksja`
  only in Volume IV. But Appendix D's claim is about **the book**, and the book
  is the series, so the existing book-wide check is the correct gate and a
  volume mode would be the wrong fix.
* **`--parts`.** It reads `frontmatter/<lang>/introduction.tex`. Carrying that
  file in every volume — which a Volume III reader wants anyway, since it is the
  series' own map — leaves the gate green with nothing to write.

The per-volume front matter that *is* new is the title page, the copyright page
(which prints an ISBN when one exists and does not claim the book comes in “two
paper formats”) and the generated series map.

---

## 9. What is still owed

1. **Nothing, on the eight interiors \dash{} and the entry that stood here said
   otherwise because it was measured with one instrument.** It read *four of the
   eight interiors still fail on a margin*, listed the four that fail
   `checkkdp.py`, and concluded that *volumes I, II and III English and Volume IV
   Polish pass every check*. The workflow runs `checklog.py` **first**, and
   against that **six of the eight failed** and **seven of the eight carried an
   overfull vbox**, the worst 207.8 pt \dash{} including two volumes the entry
   named as clean. The pull request's own smoke test is volume III, chosen
   because it is the smallest, and it was red in both languages.

   That is this repository's oldest recorded class arriving in the note about the
   thing it describes: **a claim about an artefact written from the instrument
   that was to hand rather than from the one the gate uses.** The correction is
   the finding; the numbers are below it.

   **One cause, and shrinking could not reach it.** Every `tabularx` in
   appendices D, E and F is `\linewidth` wide and cannot break across a page, and
   at 6 x 9 the text block is shorter than the trade format's \dash{} so a table
   that fits there grows past a page here. 207.8 pt out of a 540 pt block wants a
   38% reduction where `\small` buys 8%, so the recorded fix for an overfull vbox
   applies: split the table. It splits itself instead.

   **And the two reasons this entry gave for ruling that out were both wrong.**
   It said `ltablex` *turns every `tabularx` in the book into a `longtable`, and
   this book puts one inside a `tcolorbox`*. The switch does not have to be
   global: installed by `\appendix`, every `tabularx` inside a box is already
   behind it, because **all 34 appendix tables sit outside boxes** and the
   `\canyou` panel is in the body. The unstated second reason was that all 34 sit
   inside `\begin{center}`, where everybody says a `longtable` cannot go. Asked
   of pdflatex at this geometry rather than reasoned about, it sets a 60-row table
   over three pages with zero overfull vboxes. Both were readings of a mechanism,
   and both cost nothing to run.

   `kdp/preamble-kdp.tex` therefore aliases `tabularx` to `xltabular` at
   `\appendix` and sets those tables `\footnotesize`, which is swept rather than
   chosen: at the body size volume IV's English carries 12 overfull hboxes with a
   worst of 45.7 pt, at `\small` 5 with a worst of 18.8 \dash{} still over the
   15 pt budget \dash{} and at `\footnotesize` 4 with a worst of 7.6.

   **The last of those four breached the gutter, and the lever for it was in the
   wrong place three times before it was in the wrong size once.** A 7.6 pt box
   on a verso put page 276 2.2 pt inside the 0.625 in KDP requires at that page
   count. The prose was written for the trade format's 70 characters a line and
   sets at 69 here, so rewriting it would move the four existing PDFs and would
   be wrong anyway. `\emergencystretch` is the instrument \dash{} and swept at 1,
   2 and 3em in the preamble it gave **byte-identical** answers, because
   `preamble.tex` appends `\emergencystretch=0pt` after `\tableofcontents` to
   stop its own contents fix leaking into the body, so a value set in a preamble
   is wiped before the first body page. That is this book's own signal that a
   change did not REACH what was measured, and its own rule that when a fix does
   not move the number you check **where** it runs before you check how large it
   is. Appended after the contents instead, the sweep separates: none 4 boxes and
   an inner margin of 0.5953 in, 1em 1 box, **2em zero boxes and 0.6624 in**, 4em
   identical to 2em. 2em is the floor rather than a preference, and the price is
   one loose line \dash{} 9 underfull hboxes against 10.

   **It is not the `\vfuzz` objection this file records elsewhere.** `\vfuzz`
   raises the tolerance so a real defect stops being reported; this changes how
   TeX breaks the paragraph so the defect stops existing, and `checklog.py` still
   fails the volume on anything left. Both editions of all four volumes now build
   with **zero overfull vboxes, nothing over the hbox budget and no KDP
   failure**, and every change is inside `kdp/`, so the four existing PDFs
   cannot move and the regression job proves it.

   | volume | pages | overfull hbox | overfull vbox | KDP |
   |---|---|---|---|---|
   | I en | 426 | 0 | 0 | clean |
   | I pl | 434 | 0 | 0 | clean |
   | II en | 326 | 0.8 pt | 0 | clean |
   | II pl | 330 | 0.8 pt | 0 | clean |
   | III en | 306 | 0 | 0 | clean |
   | III pl | 308 | 0 | 0 | clean |
   | IV en | 408 | 0 | 0 | clean |
   | IV pl | 414 | 0 | 0 | clean |

   Zero errors and zero unresolved references in all eight. The two 0.8 pt boxes
   are inside the 15 pt budget, so `checklog.py` exits 0 on every volume.

   **And the sentence introducing that table said \enquote{zero overfull
   hboxes} until it was read against the table two lines under it.** The
   measurement was right, the summary of it was not, and it is the second
   overstatement in this one entry \dash{} which is the entry whose own lesson
   is below. A summary sentence is a claim about the table beneath it and gets
   read against it like any other.

   **What the entry above still owes is a habit rather than a fix: run the gate
   the workflow runs, over every artefact, before writing a sentence about any of
   them.** Six of eight was one loop away the whole time.

2. **The rate card.** `pricing` in `tools/volumes.json` is Amazon's figures and
   nothing in this repository can verify them. Every price the pipeline prints is
   only as good as that block.
3. **The AI disclosure, the ISBNs, the descriptions, the keywords, the
   categories and the list prices.** Ten of the twenty KDP metadata fields are
   computable and ten are decisions. `tools/kdpmeta.py` reports the second group
   as blocking rather than emitting a plausible default — and the AI declaration
   in particular is a statement about authorship with terms-of-service
   consequences, so a generator must not answer it.
4. **The covers.** `tools/kdpcover.py` computes the spine width from the built
   interior and draws a correctly-dimensioned template with trim, bleed, spine
   and safe-zone guides. It does not design anything.
