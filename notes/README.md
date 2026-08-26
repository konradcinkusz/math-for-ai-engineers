# Design notes

The research this book was built from, committed rather than summarised away.
None of it is the book; all of it is why the book is shaped as it is.

| | |
|---|---|
| `01-curriculum.md` | The reasoned program list: each program's argument, its concrete AI payoff, its frame estimate, the dependency graph, the ten specified measurements, and §21's addendum recording what the adversarial review changed. |
| `02-grounding-and-traps.md` | What already exists (Deisenroth, Goodfellow, Strang, Boyd, Bishop, Murphy, 3Blue1Brown, fast.ai) and what each does badly; the thesis and what would falsify it; and **the catalogue of 38 misconceptions AI engineers actually hold**, each phrased in the reader's own voice with its correction and its owning program. That catalogue is the source for every `trapbox` in the book. |
| `03-bilingual-and-notation.md` | The bilingual architecture, the CI parity checks and why each exists, and the Polish notation contract — governed by the keyboard test, with the four genuine splits settled so nobody re-litigates them from a search result. |
| `04-macro-design.md` | The programmed-learning machinery in LaTeX, and the traps in implementing it. |
| `05-floating-point-plan.md` | The frame-by-frame plan for **P1**. Written when the floating-point material was proposed as F1; the curriculum moved it to P1, and the plan is unchanged and still correct for its new home. |
| `06-numeric-verification.py` | An independent re-derivation of every numeric claim in that plan, and in F1. Its output is `06-numeric-verification.out.txt`: **152 claims checked, 152 confirmed**, plus two consistency defects it found that were not about arithmetic — one quantity emitted at two precisions, and a device count rounded to nearest where it should take a ceiling. Both are fixed. |

Note that `06-numeric-verification.py` is not part of the build. The book's own
numbers come from `code/`, which writes `figures/values/` and is gated by
`make verify`. This is a second, independent computation of the same quantities,
kept because agreeing with yourself is not evidence.
