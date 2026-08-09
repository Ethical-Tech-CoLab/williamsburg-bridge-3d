"""Ingest external source material into ``sources/`` with a licence manifest.

STATUS: not implemented. Planned for Milestone 2.

Nothing may be ingested before it is registered. The order is: read the source, add a row to
``SOURCE-REGISTER.md`` section 1 with its licence and verification state, quote the passage relied
on in section 3, and only then retrieve the file. Registration is not verification, and retrieval
is not either — test STT-008 fails the build if a control cites a source that has not been read.

The two HAER PDFs already under ``sources/drawings/`` were retrieved by hand and registered as
SRC-001 and SRC-002 before any control cited them.
"""

from __future__ import annotations

import sys

MILESTONE = 2
REASON = (
    "Source ingestion is Milestone 2 work. Register and read a source first; see "
    "SOURCE-REGISTER.md section 4 for the verification queue in priority order."
)


def main() -> int:
    print(f"ingest_sources.py is not implemented (planned for Milestone {MILESTONE}).")
    print(REASON)
    return 2


if __name__ == "__main__":
    sys.exit(main())
