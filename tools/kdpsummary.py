#!/usr/bin/env python3
r"""What each volume costs, what it must sell for, and what is still owed.

Reads the per-volume kdp-report.json and metadata.json the build produced, and
prints one table. Written for $GITHUB_STEP_SUMMARY, and printed to the terminal
by `make kdp` for the same reason.

The money is arithmetic over Amazon's rate card, which lives in
tools/volumes.json and which nothing here can verify. The table says so.

Run:  python3 tools/kdpsummary.py build/kdp
      python3 tools/kdpsummary.py dist          (the CI artefact layout)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "build/kdp")
    cfg = json.loads((ROOT / "tools" / "volumes.json").read_text("utf8"))
    pr = cfg["pricing"]

    reports = sorted(root.rglob("kdp-report.json"))
    if not reports:
        print(f"no kdp-report.json under {root}")
        return 1

    print(f"\n## KDP volumes -- {cfg['trim']['name']} in at {cfg['body_pt']}pt, "
          f"black ink on {cfg['paper']['stock']} paper\n")
    print("| volume | pages | trim | colour | fonts | gutter | spine | "
          f"cost ({pr['currency']}) | min list | list | royalty |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")

    owed, worst, total_pages = [], 0, 0
    for rp in reports:
        r = json.loads(rp.read_text("utf8"))
        mp = rp.parent / "metadata.json"
        m = json.loads(mp.read_text("utf8")) if mp.exists() else {}
        total_pages += r["pages"]
        worst = max(worst, r["pages"])
        name = r["file"].replace("kdp-", "").replace(".pdf", "")
        price = m.get("list_price_eur")
        roy = m.get("royalty_eur")
        print(f"| {name} | {r['pages']} | "
              f"{'ok' if r['trim_ok'] else '**BAD**'} | "
              f"{r['nongray_count'] or 'none'} | "
              f"{len(r['unembedded_fonts']) or 'all embedded'} | "
              f"{r.get('inner_margin_in','?')} in | {r['spine_in']} in | "
              f"{r['printing_cost']} | {r['min_list_price']} | "
              f"{price if price is not None else '--'} | "
              f"{roy if roy is not None else '--'} |")
        for b in m.get("_blocking", []):
            owed.append((name, b))

    ceiling = cfg["limits"]["max_pages_black_regular"]
    print(f"\nLargest volume {worst} pages, {ceiling - worst} below the "
          f"{ceiling}-page black-ink ceiling. "
          f"{total_pages} pages across {len(reports)} interiors.")
    print(f"\n> The printing cost, the minimum list price and the royalty are "
          f"arithmetic over the rate card in `tools/volumes.json` "
          f"({pr['fixed_cost']} + {pr['per_page_cost']}/page, "
          f"{pr['royalty_rate']:.0%} royalty, {pr['vat_rate']:.0%} VAT). "
          f"Those are Amazon's figures, they change, and nothing in this "
          f"repository verifies them. Check them against the current KDP rate "
          f"card before believing any price here.")

    if owed:
        print(f"\n### Still owed before upload\n\n| volume | field |\n|---|---|")
        for n, b in owed:
            print(f"| {n} | {b} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
