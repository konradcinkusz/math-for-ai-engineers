# Blank versos carry a running head (issue #120) --- hand-off

Unit: the whole book's page style, not a program. Reviewed build: `main` at
`c9b8bb6`. The change is one wrapper in `preamble.tex`, which all four builds
read, so "both editions" needed no duplicated edit --- and no program file was
touched, so no other unit's files were either.

**This container has no TeX and no `pdftotext`.** Nothing here can compile the
book or read a PDF, so the P23 "ask TeX" instrument was not available. What
*was* available is written up under *What was verified* below, and what was
not is stated in the preamble comment itself rather than left implied.

Gates, run before any edit and again after, all green: `parity.py` 56 file
pairs / 1866 frames / 0 declared divergences / 0 failures, 0 warnings;
`check_structure.py --frames --answers --outcomes --values --elicit --scripts
--terms --parts` exit 0; `gen_stubs.py --check` current; `make numbers`
followed by `make verify`, which reports every computed output current.
**No value was emitted or retired, so `appf.tex` is NOT stale from this pass.**
`make debt`'s only FAIL is `reflist.py` wanting `main-en.aux`, which needs a
completed build --- not mine to run.

---

## The finding, verified before it was fixed

Still reproduces. `\pagestyle{fancy}` is in force from `preamble.tex:574`,
nothing anywhere redefined `\cleardoublepage` (`grep -rn cleardoublepage`
returns only the two title pages, which *call* it), and all four main files
carry `twoside,openright`, so `book.cls`'s `\chapter` reaches
`\cleardoublepage` for every program, every appendix and every part. The leaf
it inserts is blank in the body only and ships under whatever page style is
current.

CLAUDE.md has carried this since the F4 review pass as "found and deliberately
not fixed", and **the reason recorded there is scope, not risk**: *"it is one
line of preamble to fix, and it was left alone because it is nothing to do
with F4 and because it moves no page."* Issue #120 is the scope. So this is
class (a), fixed, rather than class (b).

## Why this is not the "record rather than take" bucket

The standing bucket is for a layout change that **turns pages** --- a room
test, a `\penalty` inside `\sumitem`, a swept constant --- because those have
to be measured across four paginations before anyone can choose a value. This
one changes what is *drawn* on a leaf that `\newpage` has already forced. It
is the Part~V continuation-mark case, not the Quiz room-test case, and that
pass named the distinction: *ask which half of a layout fix is being proposed
before pricing it.* There is no constant here to sweep and nothing to choose.

## The form, and why it is a wrapper

`emptypage`'s body, written out rather than required:

```latex
\let\mfa@cleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage{\pagestyle{empty}\mfa@cleardoublepage}}
```

Three decisions, each with a reason in the preamble beside it:

* **No package.** A package one of this project's two TeX installations has
  and a reader's does not is latent on every machine that exists here --- the
  trap recorded against mathtools. This is four lines that need nothing.
* **A wrapper, not a `\patchcmd`.** A patch has to match `\hbox{}\newpage`
  inside the kernel's own definition, and a failed `\patchcmd` falls into a
  `\PackageWarning`, which `checklog.py` prints and does **not** fail on
  (verified: it is not in `HARD_WARN`). The fix would go inert while the build
  stayed green --- this preamble's own recorded failure mode. A wrapper calls
  whatever `\cleardoublepage` happens to be, so there is nothing to match.
* **`\clearpage` first and outside the group**, so the page in hand ships
  under its own style; `\pagestyle{empty}` inside the group, which `\ps@empty`
  installs with local `\let`s, so the leaf ships bare and the group hands the
  fancy style straight back.

## What was verified, and what the build must still confirm

**Verified here.** `tools/checkpdf.py` needed **no code change**, which
contradicts the issue's own prediction that it would need "the same one-line
adjustment". Driven with synthetic `pdftotext -bbox` XML for the same six-page
book both ways, `head_baseline`, `text_blocks`, `foot_baseline` and
`chapter_final` answer identically. That is a measurement rather than an empty
comparison, because the probe was mutation-tested: give the leaf real body ink
and `chapter_final` moves from `[3, 6]` to `[4, 6]`. And the docstring's claim
that the head test *used to be* load-bearing was checked the same way --- with
`inked` asking for any word at all, the old head-bearing leaf gives `[4, 6]`,
so the head test was exactly what prevented it. Three of the four checks read
a body page as a word below `head + HEAD_GAP` and the fourth discards the head
by `HEAD_FRACTION`, so the leaf was already outside all four; it now carries
no words and the loop's `if not ws: continue` skips it before any of them.

**NOT verified here, and it needs the four-format build.** That the change
moves no page. It is a reading of a mechanism --- the leaf is forced by
`\newpage` either way --- and this file's rule is that such a reading stays
judgement until it is run. The one thing the mechanism cannot settle from here
is the doubled `\clearpage`: `\cleardoublepage` opens with one of its own, and
that is a no-op only because the first leaves material behind it. **If that
were wrong the failure would be loud rather than subtle** --- every one of
these leaves would become two and the page counts would jump by the number of
chapters --- so it lands squarely in the measurement the sync session takes
anyway. Expect the page table and the overfull multiset element for element.

## Frames whose length I changed

**None.** No `.tex` file under `programs/`, `appendices/` or `frontmatter/`
was touched, so no frame grew or shrank and there is no cue walk owed on my
account. Any page-level movement the sync build reports from this change is
the change itself and not a frame edit.

## Values

None emitted, none retired. `figures/values/` is untouched and `make verify`
is green, `appf.tex` included.

## Found in a neighbouring file and NOT fixed

**Both title pages say the book has forty-six programs.** It has forty-seven
--- `gen_stubs.py --check` prints "47 programs", and F1--F13 plus P1--P34 is
47.

* `frontmatter/en/titlepage.tex:8` --- `Forty-six programs, worked`
* `frontmatter/pl/titlepage.tex:8` --- `Czterdzieści sześć programów`

It is the **P7 insertion** in an eighth artefact, after the trap catalogue,
the manifest, the curriculum notes, Appendix~B, the issues' trap lists,
`notes/02` §4, the issues' contract paragraphs and both introductions --- and
this is the worst-placed of the eight, because it is page one and it is the
first sentence a reader reads. Left alone deliberately: it is not this issue,
it is the front matter rather than the page style, and the fix moves the title
page's own line breaks in a `\Large` centred block in two languages, so it
wants its own measurement. Both editions carry it identically, so C4, C8, C12
and C14 are all blind to it, exactly as they were to the introduction's nine
part ranges.

## Recorded rather than taken

Nothing else. Issue #120 named one defect and one fix, and both are here.
