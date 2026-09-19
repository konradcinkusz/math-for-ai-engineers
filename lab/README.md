# The lab — the book's exercise engine

Computer exercises for *Mathematics from Zero for the AI Engineer*, built so
that **every number a reader's code has to reproduce is one the book prints**.
The checks read `figures/values/<program>.tex` — the same files the book's
pages are set from and `make verify` gates — and compare against nothing
else. The lab therefore has no numbers of its own to drift, and the book
cannot move without the lab noticing.

It is deliberately **presentation-independent**: the same stubs and the same
checks serve a terminal today, and are the exercise layer of the learning
application proposed in `notes/10-learning-app.md`, where they run in the
browser under Pyodide. Nothing here is LaTeX and nothing here is read by the
book's build; `lab/tools/labcheck.py --guard` proves the lab touches nothing
the book reads.

## For a reader

Open `lab/exercises/p01_floating_point.py` on one side of the screen and
Program P1 on the other. Every function is one exercise; its docstring names
the frames it rests on. The loop, in this order:

1. **Read** the frames the exercise names — the frames, not the program.
2. **Predict, on paper**, what the exercise tells you to predict. This is the
   book's covered answer box, and it is the step you will be tempted to skip.
3. **Implement** the function. Keep its name and signature.
4. **Check**:

```sh
python3 lab/check.py p01            # every exercise of Lab P1
python3 lab/check.py p01 -k gap     # one of them
python3 -m pytest lab/tests/test_p01.py   # the same checks, under pytest
```

Nothing beyond Python 3.11 is needed. A failed check names the frames to
re-read; go there, not to `lab/solutions/`, which exists so that the build can
prove the exercises are solvable and is for after your own check passes.

## For a maintainer

```
lab/
├─ exercises/<id>_<name>.py    the reader's file: stubs raising NotImplementedError
├─ solutions/<id>_<name>.py    the reference; same public names, same region markers
├─ tests/test_<id>.py          plain functions and plain asserts, pytest-compatible
├─ tests/labkit.py             load() the reader's or the reference file; values() of a program
├─ check.py                    the stdlib runner: ok / todo / FAIL, and a SUMMARY line
└─ tools/labcheck.py           the gates below
```

```sh
python3 lab/tools/labcheck.py --files          exercise and solution files agree; every
                                               region has a check; lines fit a half-screen pane
python3 lab/tools/labcheck.py --tests          the solutions pass every check and the untouched
                                               stubs pass none -- the instrument is watched
                                               producing a known answer in both directions
python3 lab/tools/labcheck.py --guard origin/main   nothing the book's build reads changed
python3 lab/tools/labcheck.py --all            --files and --tests
```

`# region: <key>` / `# endregion: <key>` markers delimit each exercise in
both files. They are what a presentation layer prints — a PDF listing, a web
editor pane — so the page and the file cannot disagree.

## Adding a lab

Pick a program whose `code/<program>.py` is the experiment a reader could
run: the lab's exercises are that script's measurements asked of the reader
before they read them. Write the stubs, the solution and the checks; every
expected value comes from `figures/values/`, never from a literal; then run
`--all`. The first lab is P1 because its own method is *a claim about what
the machine stores is settled by asking it*.

## The content compiler

`lab/tools/content_compile.py` is the other half of issue #239 §1: it reads
the two editions with the book's own tokeniser and emits **one data bundle**
that the learning application consumes, so that the application never sees
LaTeX. Every exercise id the compiler attaches to a step is declared by the
lab that owns it — `# --- exercise 4: orders ---` in `tests/test_p01.py` —
because a name a reader types at `lab/check.py -k` is a name, not something
to derive from a test's spelling.

```sh
python3 lab/tools/content_compile.py --tag v0 --cross-check \
        -o build/content/bundle.json --pack build/content/content-v0.tar
python3 lab/tools/content_compile.py --only P01 --stdout   # one program
python3 lab/tools/content_compile.py --survey              # every refusal at once
python3 lab/tools/content_compile.py --macros              # the KaTeX table

npm install --no-save katex
node lab/tools/content_katex.js build/content/bundle.json  # the render test
```

Measured on the whole book: **47 units, 275 sections, 1866 steps, 1030
answers, 1030 cues, 1408 routes**, and **21 714 of 21 714 maths spans render
under KaTeX in strict mode**. Every one of the first five figures agrees with
`lab/tools/content_probe.py`, which was written separately and reads the same
source — `--cross-check` makes that agreement a gate, and it earned its place
by catching a `\section` the compiler had silently dropped.

**It refuses rather than degrades.** A macro outside the declared vocabulary,
a `\val` with no computed value, a cue whose successor does not answer, two
editions whose frames do not pair: each stops the build and names the
program, the frame and the token. What schema v1 has no field for — figures,
transcripts, and the ten steps whose whole content is an answer — is
**counted and printed on every run** rather than dropped in silence, which is
the treatment this book already gives the orphan-tail ledger and for the same
reason.
