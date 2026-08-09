"""Align an imported mesh to the control skeleton and report its deviation.

STATUS: not implemented. Planned for Milestone 4.

Alignment targets, per AGENT-INSTRUCTIONS.md section 9.4, are the tower centrelines, the deck
elevation, the main-span endpoints and the anchorage positions. Note that on this bridge only the
first and third of those are sourced: the anchorage stations rest on placeholder CTL-101 (OQ-001)
and the deck elevation at the anchorage on CTL-103 (OQ-006). An alignment computed against a
placeholder is not a validation of anything, and any deviation reported against one must say so.
"""

from __future__ import annotations

import sys

MILESTONE = 4
REASON = (
    "Mesh alignment is Milestone 4 work. Two of the four alignment targets named in the handoff "
    "currently rest on placeholders; retire OQ-001 first or the alignment will encode a guess."
)


def main() -> int:
    print(f"align_mesh_to_control.py is not implemented (planned for Milestone {MILESTONE}).")
    print(REASON)
    return 2


if __name__ == "__main__":
    sys.exit(main())
