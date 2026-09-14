#!/usr/bin/env python3
"""Run a lab's checks with nothing installed beyond Python.

    python3 lab/check.py p01            # every check of Lab P1
    python3 lab/check.py p01 -k gap     # only the checks whose name has `gap`

The checks are the same plain functions pytest runs; this runner exists so
that the loop -- read, predict, implement, check -- costs a reader no
installation at all. Three outcomes, printed one per line:

    ok    the check passed
    todo  the function still raises NotImplementedError
    FAIL  the check failed, with the message that names the frames to re-read

Exit 0 only when everything is `ok`. The last line is machine-readable
(`SUMMARY ok=.. fail=.. todo=..`) so that lab/tools/labcheck.py can prove the
reference solutions pass and the untouched stubs do not.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESTS = HERE / "tests"


def run(lab: str, keyword: str | None = None) -> tuple[int, int, int]:
    if str(TESTS) not in sys.path:
        sys.path.insert(0, str(TESTS))
    path = TESTS / f"test_{lab}.py"
    if not path.exists():
        sys.exit(f"no such lab: {lab!r} (expected {path})")
    spec = importlib.util.spec_from_file_location(f"test_{lab}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)   # a syntax error in the reader's file
                                      # surfaces here, with Python's own message
    tests = [(name, fn) for name, fn in vars(module).items()
             if name.startswith("test_") and callable(fn)]
    if keyword:
        tests = [(n, f) for n, f in tests if keyword in n]
        if not tests:
            sys.exit(f"no check of lab {lab!r} has {keyword!r} in its name")
    ok = fail = todo = 0
    for name, fn in tests:
        try:
            fn()
        except NotImplementedError as exc:
            todo += 1
            print(f"  todo  {name}: not implemented yet ({exc})")
        except AssertionError as exc:
            fail += 1
            print(f"  FAIL  {name}: {exc or 'assertion failed'}")
        except Exception as exc:  # noqa: BLE001 -- a reader's bug, reported
            fail += 1
            print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")
        else:
            ok += 1
            print(f"  ok    {name}")
    print(f"SUMMARY ok={ok} fail={fail} todo={todo}")
    return ok, fail, todo


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("lab", help="the lab's id, e.g. p01")
    ap.add_argument("-k", dest="keyword", default=None,
                    help="run only the checks whose name contains this")
    args = ap.parse_args()
    ok, fail, todo = run(args.lab, args.keyword)
    return 0 if (fail == 0 and todo == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
