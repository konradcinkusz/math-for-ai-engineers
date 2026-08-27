# The original's layout, observed

Taken from photographs of the Polish edition of Stroud's *Engineering
Mathematics* — Program F.4 *Wykresy*, pages 123, 124, 131, 132 and 151. That
is one program's opener, its Quiz, two mid-program spreads and one late
spread, which between them show every structural element the format uses.

This file is the reference. **Where this book departs from the original, the
departure is recorded here with its reason** — otherwise a later pass will
"fix" a deliberate decision back to the source, or drift away from it by
accident.

---

## 1. The program opener (p. 123)

| Element | Original |
|---|---|
| Frame range | `Ramki 1 do 54` in a thin-ruled box, **top right**, above everything |
| Program label | `Program F. 4`, bold, medium, above the title |
| Title | `Wykresy` — very large, bold, **black** |
| Outcomes heading | `Czego się nauczę z tego programu?` — a *question*, bold |
| Lead-in | `Po ukończeniu tego programu będziesz potrafił:` — **italic**, indented |
| Outcomes | **Empty checkboxes** `☐`, not bullets. The reader ticks them. |
| Panel | The whole outcomes block sits on a light grey tint |
| Standing instruction | A paragraph *outside* the panel: if you already feel confident in any of these, try the quiz overleaf |
| Page number | Bottom centre (the opener uses a plain page style) |

**The frame range is the reader's contract.** It says how long the commitment
is before they start, and it is the first thing on the page.

**The checkbox is not decoration.** It is the same affordance as the *Can you?*
checklist at the end — the outcomes list is a thing you come back and tick.
Bullets cannot be ticked.

## 2. The Quiz (p. 124)

- The whole quiz sits inside **one thin-ruled rectangle**, questions and all.
- A column heading `Ramki` sits at the **top right inside** the box.
- Each question group's route is **two small ruled boxes with `do` between
  them**, right-aligned: `1 do 8`, `9 do 16`, `17 do 29`, `30 do 35`,
  `36 do 53`. Not parenthesised prose.
- Questions are `1`–`5` with `(a)`, `(b)`, `(c)` sub-parts.
- A marginal note at the top explains an icon used on some questions.

The route boxes are the entire point of the Quiz: **a wrong answer sends the
reader to a specific span of frames**, and the boxed pair reads as a coordinate
rather than as a footnote.

## 3. The frame (pp. 131, 132, 151)

This is the part the current book had most wrong.

- **The frame number lives in the OUTER margin**, in a grey rounded box, set
  large. p. 131 (recto) has `13`, `14` on the right; p. 132 (verso) has `15`,
  `16` on the left; p. 151 (recto) has `50`, `51` on the right. It follows the
  spread, so a reader thumbing for frame 37 runs a finger down the edge of the
  block and never crosses the text.
- **A horizontal rule** spans the measure at the frame boundary.
- **`Kolejna ramka.`** — *Next frame.* — set **italic and right-aligned** at
  the end of a frame that has asked for a response. It is the instruction to
  cover the page and turn over, and it appears at every such boundary.
- **The answer to the previous frame is in a thin-ruled box**, white inside,
  narrower than the measure, centred. Not a tint, not a bar. It is a thing you
  put your hand over.
- Figures sit on a light grey tint.

## 4. Summary, revision, and the end of a program

- **`Podsumowanie` is itself a numbered frame** — 14 on p. 131, 51 on p. 151 —
  with a small list icon beside the number.
- Its items are **numbered**, and each ends with the frame it came from in
  square brackets: `[4]`, `[5]`, `[7]`, `[36]`, `[40]`, `[41]`.
- The panel is grey-tinted, and where it breaks across a page it carries a
  **`▶` at the bottom right** to say so.
- **`Ćwiczenia na powtórzenie`** (revision exercises) is the next numbered
  frame — 15 on p. 132 — and **its answers are the frame after it**, 16.

**Stroud summarises mid-program, not only at the end.** Frame 14 of a 54-frame
program says, in bold: *W tym miejscu przerwiemy i podsumujemy najważniejsze
fakty, które zostały dotychczas przedstawione w tym programie* — we will pause
here and summarise what has been covered so far. Summary, revision exercise
and answers form a three-frame checkpoint, and the program then continues.

## 5. Running heads

Mirrored, with the page number **outer** and the running title **inner**:

| | Left of head | Right of head |
|---|---|---|
| recto (131, 151) | `Wykresy` — the program title, italic | `131` |
| verso (132) | `132` | `Program F. 4` |

Note what is **not** there: no frame number in the running head. The margin
badge does that job, and does it better — it names the frame you are looking
at rather than the last one to start on the page.

---

## What this book does differently, and why

Every element in sections 1 to 5 above is implemented **except the two named at
the bottom of this section**, which are recorded as departures rather than left
to be rediscovered. What follows is the list of places where the implementation
departs from the photograph, each with its reason. **Do not "fix" one of these back to the
source without reading why it is here** — that is what this section exists to
prevent.

Two departures of principle:

**Colour.** The original is monochrome. This book keeps its palette, which it
shares with the two companion volumes; a reader who owns one should recognise
the second. So the answer box is ruled in the book's green rather than black,
and the program title is set in the book's blue. The *structure* is the
original's; the ink is this series'.

**`Can you?` keeps its five-point scale.** The original's checklist is a tick.
A self-assessment with a midpoint is one people actually use; a yes/no one is
one they lie to. The outcomes list gained the original's checkbox, which is
where the tick belongs.

### The departures the implementation added

**The outcomes heading stays in the box's blue title bar.** The original sets
the bold question as black text *on* the grey tint. Two reasons, both this
repository's own rules. CLAUDE.md: *two box treatments, and that is the whole
visual grammar* — a bold coloured heading inside the body of a tinted box is a
third treatment used by exactly one box in the book, where the blue bar is what
`note`, `warning`, `aibox` and `notationbox` already do. And the panel is
`breakable`: a tcolorbox title is bound to the start of the box and cannot be
orphaned from the list, where a heading set as body text can be.

**The answer box is ruled at 0.6 pt where the admonitions are 0.8 pt.** The
page then carries exactly two rule weights — 0.6 pt for frame furniture
(`\framerule` and the answer box) and 0.8 pt for content the author flagged.
The answer box appears about thirty times per program against an admonition's
four or five, so it is the one that has to be quiet. A later pass will want to
"unify" it to 0.8 pt; that is the wrong direction.

**`ansblock` is set full width**, where section 3 above records the answer box
as *narrower than the measure, centred*. `\ans` does obey the original; a
multi-paragraph worked answer with displayed maths at `0.86\linewidth` is
where the overfull hboxes would come from, so the block form gives up the
narrowness and keeps the white ground and the hairline.

**The revision exercise's answers are not the following frame.** The original's
frame 15 is a revision exercise and its frame 16 is the answers to it. This
book carries every answer to Appendix A, keyed by program and item, so the
original's frame 16 has no counterpart here.

**`Can you?` and `Further problems` are deliberately not frames.** Summary and
Test exercises are — the original frames both — but `Can you?` is an instrument
rather than content, and `Further problems` is optional consolidation outside
the 80/80 instrument. The consequence is visible and was accepted rather than
overlooked: the frame stream is interrupted once, by `Can you?` sitting
unnumbered between frames 46 and 47.

**The continuation marker is drawn in the book's blue** rather than set as a
black glyph, consistent with the colour departure above; and it sits **wholly
inside the panel's padding** rather than optically on the text edge. The
original's marker sits closer to the measure. Here the triangle spans 5 pt
horizontally and 5.2 pt vertically from its apex against 8 pt of right padding
and 6 pt of bottom padding, so the apex is at `xshift=-3pt, yshift=3pt` — the
largest offset that keeps the whole mark off the text column, where the
descender of a justified last line lives.

**The frame-range box counts the named frames.** `Frames 1 to 47`, not `1 to
45`: the Summary is frame 46 and the Test exercises frame 47, so a range
stopping at the last teaching frame would contradict two frames the reader can
see. This matches the original, whose F.4 says `Ramki 1 do 54` over a program
whose Summary is frame 51. Note that the debt ledgers count *teaching* frames
and therefore report 45 — that divergence is deliberate and is recorded in
CLAUDE.md.

**The Summary's list icon sits on the rule, not beside the number.** The
original puts a small list mark next to the frame number. Here the number lives
in the outer margin, so the icon takes over the position the number vacated on
the rule. It does not follow the badge into the margin: `\marginparwidth` is
34.14 pt in the trade format and a two-digit badge plus the icon is about
48 pt, so a badge-and-icon margin note would overfull its own hbox.

**The badge is body size, not large.** Section 3 records the original's frame
number as set large. Ours is `\bfseries\normalsize`. At this measure a larger
badge starts competing with the section headings for the eye, and the badge is
a locator rather than a heading. Revisit if a reader reports missing it.

Two elements of the original are **not** implemented, deliberately:

**Figures do not sit on a tint** (section 3, last line). The rendered
`\mermaidfig` is a bare `\includegraphics` on white; what tint appears comes
from the Mermaid theme's own node fills, not from a panel behind the figure.
A panel would put a third box treatment on the page, and the book's visual
grammar is two. Reconsider only if figures start reading as part of the prose.

**There is no mid-program checkpoint** (section 4). Stroud pauses a 54-frame
program at frame 14 for a Summary, a revision exercise and its answers, and
then continues. F1 has one Summary, at the end. The machinery is already there
— `summarybox` and `testexercises` are numbered frames and work anywhere in a
program — so this is a *content* decision, not a missing feature, and it is the
author's: inserting three frames mid-program renumbers every frame after them,
and with it every outcome, every Quiz route and every Summary bracket above the
insertion point. That is the renumbering CLAUDE.md says is a decision and not a
side effect. For a program of F1's length one checkpoint is arguable; for the
70-frame programs later in the book it is not optional.
