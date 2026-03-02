#!/usr/bin/env python3
"""Read an rwcheck JSON report and emit counts + a Markdown table of retracted entries.

Usage:
    python3 action_bib_table.py <path/to/stem_rwcheck.json>

Exit codes:
    0 — success (may have found retractions)
    1 — file not found or JSON parse error

Stdout (tab-separated on first line, then markdown table rows):
    COUNTS\t<total>\t<retracted>\t<unchecked>
    ROW\t| `key` | title | nature | date | journal | reason |
    ...
"""

from __future__ import annotations

import json
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: action_bib_table.py <json_file>", file=sys.stderr)
        sys.exit(1)

    json_file = sys.argv[1]
    try:
        with open(json_file) as f:
            d = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {json_file}: {e}", file=sys.stderr)
        sys.exit(1)

    total = d.get("total", 0)
    retracted = d.get("retracted", 0)
    unchecked = d.get("unchecked", 0)

    print(f"COUNTS\t{total}\t{retracted}\t{unchecked}")

    for entry in d.get("results", []):
        if not entry.get("matched"):
            continue
        for m in entry.get("matches", []):
            key = entry.get("key", "?")
            title = (m.get("title") or entry.get("title") or "Unknown")[:60]
            nature = m.get("retraction_nature") or "Retraction"
            date = m.get("retraction_date") or "unknown date"
            journal = (m.get("journal") or "unknown journal")[:40]
            reason = (m.get("reason") or "")[:50]
            print(f"ROW\t{key}\t{title}\t{nature}\t{date}\t{journal}\t{reason}")


if __name__ == "__main__":
    main()
