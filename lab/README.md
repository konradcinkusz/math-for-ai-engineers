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
