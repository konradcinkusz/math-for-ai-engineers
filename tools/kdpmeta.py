#!/usr/bin/env python3
r"""The KDP upload form, as JSON, per volume and language.

Half of what KDP asks for is computable from the built interior and the
manifest; the other half is a decision. This emits both, and NEVER guesses the
second kind: a field a human has not set is null AND is listed as blocking, so
the job summary says what is still owed rather than shipping a plausible
default.

THE AI DISCLOSURE IS THE SHARPEST CASE. KDP requires a declaration about
AI-generated text, translation and images, and an AI-produced translation
counts. That is a statement about authorship with terms-of-service
consequences, so it is read from tools/volumes.json and is null until a human
sets it -- a generator must not answer it.

Run:  python3 tools/kdpmeta.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / "build" / "kdp" / "tex"
OUT = ROOT / "build" / "kdp"

# Fields KDP requires that no script can derive. Reported, not invented.
HUMAN_FIELDS = ["description_html", "keywords", "categories", "isbn",
                "list_price_eur", "ai_content_disclosure"]


def pages_of(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(out.split("Pages:")[1].split()[0])


def build(cfg: dict, vol: dict, lang: str, pdf: Path) -> tuple[dict, list[str]]:
    pages = pages_of(pdf)
    pr = cfg["pricing"]
    cost = pr["fixed_cost"] + pr["per_page_cost"] * pages
    min_list = cost / pr["royalty_rate"] * (1 + pr["vat_rate"])
    price = (vol.get("list_price") or {}).get(lang)
    disc = cfg.get("ai_content_disclosure", {})
    disc = {k: v for k, v in disc.items() if not k.startswith("_")}

    m = {
        "language": lang,
        "title": vol["title"][lang],
        "subtitle": (vol.get("subtitle") or {}).get(lang),
        "series_name": cfg["series"][lang],
        "volume_number": vol["n"],
        "author": cfg["author"],
        "description_html": (vol.get("description_html") or {}).get(lang),
        "keywords": vol.get("keywords") or [],
        "categories": vol.get("categories") or [],
        "isbn": (vol.get("isbn") or {}).get(lang),
        "ai_content_disclosure": disc,
        "territories": "all",
        "trim": cfg["trim"]["name"],
        "ink": "black_and_white",
        "paper": cfg["paper"]["stock"],
        "page_count": pages,
        "printing_cost_eur": round(cost, 2),
        "min_list_price_eur": round(min_list, 2),
        "list_price_eur": price,
        "royalty_eur": (round(price / (1 + pr["vat_rate"]) * pr["royalty_rate"]
                              - cost, 2) if price else None),
        "_pricing_source": ("tools/volumes.json `pricing'. These are Amazon's "
                            "figures and they change; nothing here verifies "
                            "them."),
    }

    blocking = []
    if not m["description_html"]:
        blocking.append("description_html")
    if len(m["keywords"]) == 0:
        blocking.append("keywords (KDP takes up to 7)")
    if len(m["categories"]) == 0:
        blocking.append("categories (KDP takes 2)")
    if m["isbn"] is None:
        blocking.append("isbn (or choose a free KDP-assigned one)")
    if m["list_price_eur"] is None:
        blocking.append(f"list_price_eur (must be at least "
                        f"{m['min_list_price_eur']} to earn a royalty)")
    elif m["list_price_eur"] < m["min_list_price_eur"]:
        blocking.append(f"list_price_eur {m['list_price_eur']} is below the "
                        f"{m['min_list_price_eur']} minimum")
    unset = [k for k, v in disc.items() if v is None]
    if unset:
        blocking.append("ai_content_disclosure: " + ", ".join(unset)
                        + " -- a declaration about authorship, not a default")
    m["_blocking"] = blocking
    return m, blocking


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--summary", metavar="FILE")
    a = ap.parse_args()

    cfg = json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))
    byn = {v["n"]: v for v in cfg["volumes"]}
    pdfs = ([STAGE / f"kdp-v{v['n']}-{l}.pdf" for v in cfg["volumes"]
             for l in ("en", "pl")] if a.all else [Path(p) for p in a.pdfs])
    if not pdfs:
        ap.error("give an interior PDF, or --all")

    lines, rc = [], 0
    for pdf in pdfs:
        if not pdf.exists():
            print(f"  {pdf.name}: not built")
            rc = 1
            continue
        mm = re.match(r"kdp-v(\d+)-(en|pl)", pdf.stem)
        if not mm:
            continue
        n, lang = int(mm.group(1)), mm.group(2)
        m, blocking = build(cfg, byn[n], lang, pdf)
        d = OUT / pdf.stem
        d.mkdir(parents=True, exist_ok=True)
        (d / "metadata.json").write_text(json.dumps(m, indent=1,
                                                    ensure_ascii=False), "utf8")
        print(f"  v{n}-{lang}: {m['page_count']} pp, cost "
              f"{m['printing_cost_eur']} EUR, min list "
              f"{m['min_list_price_eur']} EUR"
              + (f", {len(blocking)} field(s) still owed" if blocking else
                 ", complete"))
        for b in blocking:
            print(f"      needs a human: {b}")
            lines.append(f"| v{n}-{lang} | {b} |")

    if a.summary and lines:
        with open(a.summary, "a", encoding="utf8") as fh:
            fh.write("\n### KDP metadata still owed\n\n| volume | field |\n"
                     "|---|---|\n" + "\n".join(lines) + "\n")
    # Missing metadata is not a build failure: the interior is correct and the
    # form is a separate act. It is reported loudly and exits 0 so it cannot
    # block a pipeline that has produced a good book.
    return rc


if __name__ == "__main__":
    sys.exit(main())
