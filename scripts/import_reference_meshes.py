"""Import an external reference mesh into ``mesh/raw/`` without letting it become authoritative.

STATUS: not implemented. Planned for Milestone 4.

AGENT-INSTRUCTIONS.md section 9 sets the workflow: preserve the original file and its licence,
convert to a neutral working format, align to the control skeleton, record the deviation, and only
then split into named components. AGENT-INSTRUCTIONS.md section 15.7 is the rule that matters most —
never merge a raw mesh directly into the authoritative model.

Test STT-007 currently fails the build if any part claims a ``mesh_reference`` basis, which is
correct at Milestone 1: there is nothing to align against yet beyond the control skeleton itself.
"""

from __future__ import annotations

import sys

MILESTONE = 4
REASON = (
    "Reference mesh import is Milestone 4 work, and only after the control skeleton is stable "
    "enough to align against. Import one mesh at a time and produce an alignment report for each."
)


def main() -> int:
    print(f"import_reference_meshes.py is not implemented (planned for Milestone {MILESTONE}).")
    print(REASON)
    return 2


if __name__ == "__main__":
    sys.exit(main())
