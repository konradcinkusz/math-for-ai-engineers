"""The lab's test kit: load the reader's file, and read the book's values.

The lab has no numbers of its own. Every value a check compares against is
read out of figures/values/<program>.tex, which is the file the program's own
pages are set from and the one `make verify` gates -- so the lab cannot drift
from the book, and the book cannot move without the lab noticing.

The exercise engine is presentation-independent on purpose: a PDF, a terminal
runner and a web application all call the same two functions here.
"""
from __future__ import annotations

import importlib.util
import os
import re
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
RE_VAL = re.compile(r"\\mfaval(?:text)?\{([^}]+)\}\{([^}]*)\}")


def values(program: str) -> dict[str, str]:
    """Every \\mfaval{key}{value} the program's script committed, as strings.

    Strings, not floats: a check compares what the reader's code PRINTS with
    what the page prints, because two numbers on one page are the same number
    only if they are the same string (CLAUDE.md, the P05 review pass).
    """
    path = ROOT / "figures" / "values" / f"{program}.tex"
    if not path.exists():
        raise FileNotFoundError(
            f"{path.relative_to(ROOT)} is missing -- run `make numbers` first")
    return dict(RE_VAL.findall(path.read_text(encoding="utf8")))


def load(stem: str) -> ModuleType:
    """The reader's exercise file, or the reference solution under
    LAB_SOLUTIONS=1, imported by path so neither needs to be a package."""
    where = "solutions" if os.environ.get("LAB_SOLUTIONS") else "exercises"
    path = ROOT / "lab" / where / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"lab_{where}_{stem}", path)
    assert spec is not None and spec.loader is not None, path
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
