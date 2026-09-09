# Hand-off: issue #119, the console transcripts

Book-wide, filed once, so the unit is the transcript mechanism rather than a
program. Nothing in `programs/` changed. Six scripts under `code/`, one
generated transcript and three comment blocks in `preamble.tex` did.

---

## What the issue asks for, and what happened to each half

**The type size reproduces and is recorded rather than taken.** `\transcript`
sets `basicstyle=\ttfamily\scriptsize`, one step below `mfacode`'s own
`\footnotesize`, so a transcript is the smallest type on its page and it is the
one thing the reader was told to check character by character. That is real and
the issue is right about it. Raising it is a book-wide layout change nobody has
measured, which is the standing reason to record: 88 references, every box a
point or two taller, which makes `\mfa@transcriptroom` fire more often; each
firing turns a page, and every orphaned cue and orphan tail after it is
re-rolled. When that guard was introduced its cost was measured in isolation and
it put three cues and three tails back. This is larger. The full mechanism, the
arithmetic and the measurement it wants are written into `preamble.tex` beside
the `basicstyle` line, so the next person meets it there rather than here.

**Two things about that arithmetic are worth carrying out of this note.** The
issue justifies the raise with *the book's 64-character line guard still fits
the A4 measure at that size* — and **A4 is the slacker of the two formats.** The
trade build has the narrower measure, 13.0 cm against 14.8, and never the larger
type, so it binds first and it is the one the issue did not check. And **nobody
has measured what a listing line can be in either format**: the typewriter
advance is a property of the font, this container has Latin Modern Mono and CI
has inconsolata, and the container that builds the published PDF has no TeX at
all to ask. A clean build is not evidence either way, for the reason under
*breaklines* below.

**The precondition was false, in two ways, and both are fixed here.** The guard
the issue rests its case on was asserted by most of the scripts and not by
`f03_logarithms.py`, `f04_sums.py`, `f11_derivative.py`, `p15_gradient.py`,
`p16_autodiff.py` or `p17_hessian_taylor.py` — and `f04-empty.txt` broke it, at
76 and 73 characters, the only two lines in the book over 64. So the sentence
the issue reasons from was not true of the book when it was written. It is now.

**The box is recorded, and where it comes from changes the size of the job.**
The fill is white — `\transcript` sets `backgroundcolor=\color{white}` — so
what is light grey is the *rule*: `frame=single` with `rulecolor=codeframe`,
and both of those are inherited from `mfacode` rather than set here. That means
the box the issue objects to is **every listing in the book and not transcripts
alone**, so a fix belongs in `mfacode` and reaches further than the issue's
own scope suggests. Whether the frame overhangs `\linewidth`, and by how much, is a
question for TeX and is **not** settled here: the mechanism reading is that
`framesep=6pt` with `framerule`, `xleftmargin` and `framexleftmargin` at their
listings defaults puts the rule outside a body that is `\linewidth` wide, but
this book has twice had a confident, specific, right-class reading of a
mechanism turn out to be simply wrong, and there is no TeX in this container to
ask. It also does **not** compose with the type size: pulling the rule inside
`\linewidth` means narrowing the body, which tightens the same measure the
`\footnotesize` question is about. Do not take the two fixes as independent.

**The measurement behind the motivation is true, and only just.** 44 transcript
files, 350 lines: median 34 characters, 59% under 40, 78% under 50. So "most
transcript lines are under 40 characters" holds, and the box really is mostly
white. After the fixes below, **every line in the book is at or under 64** and
the widest is exactly 64.

**One of the issue's four illustrative values has moved, and it moved the way
that strengthens the case.** It cites *`0.0997` against `0.1` (P20 p687)*;
`figures/transcripts/p20-unit-step.txt` now prints `[0.099668, 0.099857]`
against `[0.1, 0.1]`, rounded to six decimals rather than four by a later
review batch. The other three — P12's `0.0` against `1.4693664691599209e-27`,
P14's `True`, P4's rank list — are all still there. So the finding reproduces,
and the one figure that changed got longer and finer, which is more of the
thing the issue objects to rather than less.

**The `upquote`-style check on the finished page cannot be done here** — it
needs a build, and this pass is forbidden one. It belongs to whichever pass
takes the type size, and it is the only instrument for that class.

**Both of the related content defects the issue mentions have been retired
because they no longer reproduce.** `figures/transcripts/p12-collision-zero.txt`
opens `>>> import math` — fixed in the second review batch. And P05's transcript
computes its row rather than carrying a typed literal, printing the four figures
the frame quotes — fixed in the P05 review pass. Each cost one `cat` to retire.

---

## THE FINDING: `breaklines=true` means the build cannot see this class at all

`mfacode` sets `breaklines=true`, and `\transcript` inherits it. **An over-wide
listing line does not overfull.** It wraps, prints the `postbreak` arrow into
the middle of what the reader is meant to paste back into a REPL, and leaves no
error, no warning and no overfull box anywhere in the log.

So `f04-empty.txt`'s 76-character line produced nothing for any gate to catch
and read like the book's own convention. It is the graceful-degradation shape
this repository already records for `\transcript`'s own file-is-absent marker,
for `\mermaidfig`'s fallback and for `gen_stubs`' `escape()` outside backticks:
the mechanism returned something plausible instead of failing. The 64-character
source guard is the **only** instrument there is, which is why six scripts not
running it was worth more than a tidy-up.

It also means the type-size question cannot be settled by a green build. Zero
overfull boxes is what `breaklines` guarantees, not evidence that 64 characters
fit.

---

## What was fixed

`figures/transcripts/f04-empty.txt` had its two trailing comments shortened, from
76 and 73 characters to 40 and 59. Nothing was lost: both said what the paragraph
four lines under the listing already says — *the loop body never executes, so
what comes back is whatever the accumulator was set to, and the reason it was set
to that is the same in both cases.* The listing was replayed through
`code.InteractiveConsole` afterwards and prints `0` and `1`, which is what the
page prints.

Every script that writes a transcript now asserts **ASCII** and **width ≤ 64**.
`f03` and `f04` gained the width assertion beside the two they already had;
`f11`, `p15`, `p16` and `p17` had none of any kind and gained both, the latter
three through a three-line `_write_transcript` helper so that the *next*
transcript in those files is guarded without anybody remembering.

**The height guard was deliberately not generalised, and that is the one
judgement in this pass worth arguing with.** `f03`, `f04` and `p01` cap a
transcript at 14 lines, "too tall for one frame". `f11-shrinking-h.txt` is
**18** and every row is load-bearing — the error falls, bottoms out and climbs
again, and that curve is the section's whole argument. Generalising the height
guard would have failed on the one listing in the book that is long on purpose.
A tall listing is `\mfa@transcriptroom`'s business now, not the scripts'. The
reasoning is in `code/f11_derivative.py` at the assertion.

**Every new guard was watched failing before it was believed**, by injecting an
over-wide line and a non-ASCII one into each of the seven sites and checking the
message. Worth recording that the *first* probe was a shell one-liner and it
reported three of the guards silent when all three were fine — a `printf`
expansion that produced nothing and, for one case, an "ASCII" injection I had
written in ASCII. The tool accepted the input and returned a plausible answer,
which is this repository's most-recorded instrument defect; the probe was rebuilt
in Python, where the mutation is asserted to have landed before the script runs.
One of those bad shell probes also left a mutated line in
`figures/transcripts/p17-too-big.txt`, caught by `git status` and regenerated.

**Two claims in my own comment had to be corrected before it was committed,
and both are the class this pass is about.** The first gave a reason why
`\lstnewenvironment{console}` is still defined — which is recorded nowhere, so
I had invented it from the feel of the code; the comment now says the reason is
not recorded and does not guess. The second stated the point sizes
(`\scriptsize` 8 pt in both formats, `\footnotesize` 9 and 10) as fact when I
had them from memory and there is no TeX here to ask. That one is worth the
detail, because the fix improved the argument: the *conclusion* — that the
trade format binds and the issue checked the slacker of the two — does not
depend on the exact sizes at all, since the trade build has the narrower measure
and never the larger type. So the comment now carries the conclusion
unconditionally and the arithmetic with its input labelled unverified.

`preamble.tex` gained three comment blocks and no code: the `basicstyle` note
described above; a correction to the `\transcript` comment, which claimed *the
ASCII rule is asserted by the script that writes it* when four scripts asserted
nothing; and a note on `\lstnewenvironment{console}`, which is **defined and
used zero times in the book** while carrying the same `\scriptsize` — so a pass
that raises the type size and leaves it ships a book with two transcript sizes.
Raise both or delete it.

---

## For the sync session

**A frame may have shortened, and it is worth walking the cues for it.**
Nothing in `programs/` changed, but `figures/transcripts/f04-empty.txt` did, and
two of its lines went from over the measure to well under it. If they were
wrapping, the box loses up to two lines and F04's frame at
`programs/en/F04-sums-products-sequences.tex:466` and
`programs/pl/F04-sums-products-sequences.tex:469` shortens, which moves every
break after it in both editions. If they were not wrapping, nothing moves at
all. **Which of those is the case is exactly the thing no gate in this
repository can see**, per the *breaklines* finding above, so it needs the build
this pass was not allowed to run.

**One correction for `CLAUDE.md`, which I was not to edit.** Its P01 pass note
says the width guard is *64 characters, taken from the widest listing line
already in the book*. That basis was false when it was written: `f04-empty.txt`
carried a 76-character line and was already in the book. 64 is a house figure
that has never been a page measurement — which is the whole reason the issue's
"the guard still fits" cannot be taken on trust. It is worth saying in the pass
note, because the same sentence is what a later pass would reason from.

**The widest listing in the book is now `f03-underflow.txt`, and it sits ON 64
rather than under it.** It is the one to measure first if anybody takes the type
size.

**Nothing was found in a neighbouring program that needed fixing and was left.**

**No values were emitted or retired.** `figures/values/` is byte-identical;
`make verify` reports everything current except `appf.tex`, which is yours.
