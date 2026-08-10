"""Search for sources with the Tavily REST API.

Tavily is the source-discovery tool for this programme. This module talks to the REST API directly
rather than through an MCP server, because the MCP path returned "Invalid API key" on every attempt
during the Milestone 2 research while the REST endpoint authenticated cleanly with the same
credential.

The key is read from ``TAVILY_API_KEY``. It is never written to disk, never echoed, and never
committed — the output files this writes contain results, not credentials.

What this does and does not do:

* It **finds candidates**. It does not register anything. A result here is a lead, not a source.
* Registration remains a human act: read the source, quote the passage, add the row to
  ``SOURCE-REGISTER.md``. ``STT-008`` fails the build if a control cites a source nobody has read,
  so a lead cannot leak into the model by accident.
* Nothing it retrieves is committed. Results land in ``data/leads/``, which is gitignored.

Usage::

    python scripts/tavily_search.py "Williamsburg Bridge side span length"
    python scripts/tavily_search.py --queue          # run the verification queue's open questions
    python scripts/tavily_search.py --extract URL    # pull the readable text of one page
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
LEADS = REPO / "data" / "leads"
API = "https://api.tavily.com"
TIMEOUT = 60

# The open questions that a search could plausibly answer, with the wording that has the best chance
# of surfacing a primary. Kept here rather than in GEOMETRY-CONTROL.md because these are search
# strategies, not controls -- no dimension lives in this file.
QUEUE: list[tuple[str, str]] = [
    (
        "OQ-001",
        '"Williamsburg Bridge" side span length feet tower anchorage 1903',
    ),
    (
        "OQ-001",
        '"Williamsburg Bridge" "land span" OR "side span" dimensions engineering record 1903',
    ),
    (
        "OQ-003",
        '"Williamsburg Bridge" intermediate towers side span number piers',
    ),
    (
        "OQ-002",
        '"Williamsburg Bridge" main cable sag feet midspan tower saddle elevation',
    ),
    (
        "OQ-004",
        '"Williamsburg Bridge" tower height feet above "mean high water" datum saddle',
    ),
    (
        "OQ-006",
        '"Williamsburg Bridge" approach grade percent street level Delancey Broadway elevation',
    ),
    (
        "OQ-007",
        '"Williamsburg Bridge" deck cross section width roadway footwalk transit truss',
    ),
    (
        "SRC-007",
        'Haight Patel "Reconstruction of the Williamsburg Bridge" AISC 2005 pdf',
    ),
    (
        "SRC-009",
        '"Williamsburg Bridge" contract drawings 1896 1903 "Department of Bridges" archive digitised',
    ),
    (
        "period",
        '"Engineering News" OR "Engineering Record" 1903 "Williamsburg Bridge" description dimensions',
    ),
]


def _key() -> str:
    key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not key:
        sys.exit(
            "TAVILY_API_KEY is not set.\n"
            "Set it for this shell only, so it is never written to a file:\n"
            '  $env:TAVILY_API_KEY = "tvly-..."'
        )
    return key


def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API}/{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:400]
        raise SystemExit(f"Tavily {path} failed: HTTP {exc.code}\n{detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Tavily {path} unreachable: {exc.reason}") from exc


def search(query: str, *, depth: str = "advanced", max_results: int = 8) -> dict[str, Any]:
    return _post(
        "search",
        {
            "query": query,
            "search_depth": depth,
            "max_results": max_results,
            "include_answer": False,
            "include_raw_content": False,
        },
    )


def extract(url: str) -> dict[str, Any]:
    return _post("extract", {"urls": [url], "extract_depth": "advanced"})


def _print_results(label: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    results = data.get("results", [])
    print(f"\n=== {label} — {len(results)} result(s)")
    for item in results:
        score = item.get("score", 0.0)
        print(f"  [{score:.2f}] {item.get('title', '(untitled)')}")
        print(f"        {item.get('url', '')}")
        snippet = (item.get("content") or "").replace("\n", " ").strip()
        if snippet:
            print(f"        {snippet[:220]}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="free-text query")
    parser.add_argument("--queue", action="store_true", help="run the open-question queue")
    parser.add_argument("--extract", metavar="URL", help="extract the readable text of one page")
    parser.add_argument("--max-results", type=int, default=8)
    args = parser.parse_args()

    LEADS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.extract:
        data = extract(args.extract)
        out = LEADS / f"extract-{stamp}.json"
        out.write_text(json.dumps(data, indent=2), encoding="utf-8")
        for item in data.get("results", []):
            text = item.get("raw_content") or ""
            print(f"--- {item.get('url')}  ({len(text)} chars)")
            print(text[:4000])
        failed = data.get("failed_results") or []
        for item in failed:
            print(f"FAILED {item}")
        print(f"\nwritten: {out.relative_to(REPO)}")
        return 0

    plan: list[tuple[str, str]]
    if args.queue:
        plan = QUEUE
    elif args.query:
        plan = [("adhoc", " ".join(args.query))]
    else:
        parser.print_help()
        return 2

    collected: list[dict[str, Any]] = []
    for label, query in plan:
        data = search(query, max_results=args.max_results)
        for item in _print_results(f"{label}: {query}", data):
            collected.append(
                {
                    "open_question": label,
                    "query": query,
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                    "snippet": item.get("content"),
                    "retrieved": stamp,
                    "status": "lead",
                }
            )
        if len(plan) > 1:
            time.sleep(1.0)

    out = LEADS / f"leads-{stamp}.json"
    out.write_text(
        json.dumps(
            {
                "generated": stamp,
                "note": (
                    "Leads only. Nothing here is a registered source. Read it, quote it, and add a "
                    "row to SOURCE-REGISTER.md before any control may cite it (STT-008)."
                ),
                "leads": collected,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n{len(collected)} lead(s) written to {out.relative_to(REPO)}")
    print("These are leads, not sources. Read before registering.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
