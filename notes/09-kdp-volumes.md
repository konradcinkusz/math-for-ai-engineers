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
| I | I | F1–F13 | 428 | 436 |
| II | II, III | P1–P11 | 328 | 332 |
| III | IV, V, VI | P12–P22 | 308 | 310 |
| IV | VII, VIII, IX | P23–P34 | 412 | 418 |

Every volume is inside the 24–828 window with over four hundred pages of
headroom, spread is −18 % to +16 % about the mean, and the binding constraint is
Polish in every volume, as expected.

**A three-volume split also fits** — I (428) | II–V (~476) | VI–IX (~477) — and
saves about sixty pages of duplicated back matter and one book. It is a product
decision rather than a technical one and the pipeline does not care: change
`tools/volumes.json` and run `make volumes`.

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

1. **Four of the eight interiors still fail on a margin, and every one is a
   `tabularx` in an appendix that cannot break across a page.** All eight are
   even, colour-free and fully embedded; these are the remainder.

   | volume | failure | what is there |
   |---|---|---|
   | I pl | bottom 0.203 in, p428 | Appendix D, vbox 39.8 pt |
   | II pl | bottom 0.203 in, p326 | Appendix D, vbox 39.8 pt |
   | III pl | bottom 0.037 in, p304 | Appendix D, vbox 51.8 pt |
   | IV en | inner 0.595 in, p276 | an overfull hbox of 45.7 pt |
   | IV en | bottom 0.037 in, p396 | Appendix E, vbox 207.8 pt |

   Volumes I, II and III English and Volume IV Polish pass every check.

   **They are not fixable from inside this pipeline, and that is the point worth
   recording.** `tabularx` cannot break across a page at all; Appendices D and E
   fit in the trade format because their chunks were split to fit *that* measure,
   and at 6 × 9 those chunks are three or four lines too tall. The two available
   fixes are both out of bounds here:

   * **edit the appendix** — which moves the four existing PDFs, and the
     regression job exists to forbid exactly that;
   * **make `tabularx` breakable in the KDP build** with `ltablex` — which turns
     every `tabularx` in the book into a `longtable`, and this book puts one
     inside a `tcolorbox` (the *Can you?* panel), where a `longtable` cannot go.

   So it needs a pass of its own: either split those two tables at rows that fit
   both measures, and re-measure all four existing PDFs, or move the glossary to
   a breakable environment book-wide. `tools/checkkdp.py` fails on them so they
   stay visible.
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
