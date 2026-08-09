# Williamsburg Bridge — source-governed digital twin

A browser-renderable, part-addressable 3D model of the Williamsburg Bridge in which **every part
carries its provenance**, so a reader can ask of any surface — *how do you know that?* — and get a
real answer, including "we do not".

**Milestone 1: control skeleton and viewer.** 57 parts, 43 controls, 9 sources, 11 open questions,
8 registered conflicts, 32 tests passing.

```
python scripts/build_control_skeleton.py     # read the control document, emit GLB + metadata
python scripts/validate_dimensions.py        # run both test suites
cd viewer && npm install && npm run dev      # browser viewer on http://localhost:5174
```

---

## The one rule

> **No dimension may exist in the model without tracing to a registered source with an explicit
> confidence grade. Anything unsourced is graded `D`, labelled a placeholder, and linked to a named
> open question.**

And its corollary:

> **A model that admits it does not know something is more valuable than one that guesses well.**

`GEOMETRY-CONTROL.md` holds every number. Scripts hold none — a literal dimension in Python is a
bug, and test GRT-016 fails the build if one appears.

---

## What the sources actually support

This is the honest state of the model, and it is the most useful thing in this README.

| | Count |
|---|---:|
| Parts | 57 |
| Controls | 43 (37 sourced, 6 placeholders) |
| Geometry provenance | **0 measured · 9 documented · 48 inferred · 0 assumed** |
| Source confidence | 7 `A` · 0 `B` · 16 `C` · 34 `D` |
| Open questions | 11 |
| Registered conflicts | 8 |

**Turn off `INFERRED` in the viewer and the bridge disappears**, leaving the reference frame: the
centreline, the station markers and the mean-high-water plane. That emptiness is published rather
than hidden, and it is a stronger emptiness than the Manhattan Bridge model's — which at least keeps
its towers. The reason is specific and worth stating: on this bridge, every structural element
depends either on a placeholder or on one reasoned step, and the model says so rather than papering
over it.

The dimensional content of the **entire national record** for this bridge is one sentence:

> SPECIFICATIONS: Suspension bridge; steel towers; spans 1,600 feet between towers; total length,
> 7,200 feet; clearance for ships, 135 feet; double decked; 4 main cables 18 inches in diameter;
> cost $8 million
>
> — Historic American Engineering Record, HAER No. NY-128 (SRC-001)

HAER NY-128 contains **no measured drawings**, confirmed by direct Library of Congress API query.
Nine photographs, three data pages, two caption pages. That is the whole survey.

### The highest-value unknown

**Nobody has read a source that states the side-span length** — the distance from each tower to its
anchorage (OQ-001). `CTL-101` stands in for it at a deliberately round 600 ft so that it cannot be
mistaken for a measurement. That one number places both anchorages, both side spans, the ends of the
suspended structure, and the lengths of both approaches. Finding it is item 3 in the verification
queue.

The single highest-value *action*, though, is item 1: **file the NYCDOT FOIL request** for record,
shop and rehabilitation drawings. It is a request, not a research problem, it has a long lead time,
and it would retire four open questions at once.

---

## Three things this repository found

**1. The build brief is wrong about the tracks, and the model follows the sources.**
`AGENT-INSTRUCTIONS.md` §6 and §13 specify four subway tracks. That is inherited from the Manhattan
Bridge, which this brief was adapted from. NYCDOT and the descriptive record both say the
Williamsburg Bridge carries **two** rapid transit tracks (J, M, Z), flanked by inner roadways that
were originally streetcar tracks. The model carries two, the disagreement is registered as CNF-003,
the four-track taxonomy is registered as negative control NEG-003, and **test GRT-007 fails the
build if a `track_3` ever appears**. That test was verified to fail against a four-track model.

**2. The survey number in the method guide is wrong.** `HOW-TO-DESIGN.md` §10 cites "HAER NY-165".
The survey is **HAER NY-128**; 165 is the NYC index number inside the call number
`HAER NY,31-NEYO,165-`. Registered as CNF-007 and NEG-004.

**3. The sources do not close.** Carried through honestly, the approaches descend at their sourced
3% grade and end about 22 m above mean high water — nowhere near street level. At least one of the
deck elevation at the anchorage, the grade, or the approach length implied by the total length is
wrong. This is reported by GRT-012 and registered as OQ-006 rather than tuned away, because tuning
it would mean choosing a number to make a picture look right.

---

## The three independent axes

There is no single "confidence" number here. Collapsing these hides the one that matters most.

| Axis | Question | Values |
|---|---|---|
| **Source confidence** | How good is the evidence? | `A` `B` `C` `D` |
| **Geometry provenance** | How is the *shape and position* known? | `MEASURED` `DOCUMENTED` `INFERRED` `ASSUMED` |
| **Material** | What is it made of, and how do we know? | closed vocabulary, separately graded |

A Tier A source can support `ASSUMED` geometry, because a sentence establishing that an element
exists says nothing about where it is. Provenance is **derived in the build**, never hand-declared.
See `CONFIDENCE-MODEL.md`.

## Rendering discipline

The viewer implements the rules that stop a schematic from lying:

- `DOCUMENTED` renders solid; `INFERRED` reduced opacity with a **dashed** outline; `ASSUMED` low
  opacity with a **dotted** outline.
- **The provenance filter hides. It does not fade.** A faded outline is still a shape a reader will
  trace.
- **No dimension is annotated on any part whose provenance is not documented.** The metadata panel
  shows `withheld` instead of a number. If we do not know where it is, we do not get to say how big
  it is.
- **A standing tally, permanently on screen.**
- Selecting a part shows the controls it rests on, their grades, their sources, and the open
  questions against it — or states plainly that there are none.
- Materials are assigned in the control document, not the renderer, and the table has **no default
  rule**: an unmatched part fails the build rather than rendering as a silent grey.

---

## Repository layout

```
GEOMETRY-CONTROL.md      every dimension, machine-parsed, the single source of truth
SOURCE-REGISTER.md       every source with verification state, conflicts, and negative controls
CONFIDENCE-MODEL.md      what A/B/C/D mean and how a part inherits its grade
SCALE-HO.md              1:87.1 reporting scale
AGENT-INSTRUCTIONS.md    the build brief for this bridge
HOW-TO-DESIGN.md         the transferable method, copied in from manhattan-bridge-3d
scripts/                 build and validation pipeline, no third-party dependencies
tests/                   geometry regression (GRT-) and source traceability (STT-) suites
viewer/                  browser viewer; viewer/public is the published contract surface
mesh/ cad/               generated artifacts
sources/                 retrieved source material and licences
photogrammetry/          capture inputs, when they exist
```

### Pipeline

```
GEOMETRY-CONTROL.md
   └── control_model.py               parses controls, placeholders, materials; enforces the contract
        └── build_control_skeleton.py derives stations and elevations, emits parts + GLB
             ├── export_gltf.py       hand-written glTF 2.0 / GLB writer, no dependencies
             ├── normalize_units.py   the ONLY unit conversion in the repository
             └── validate_dimensions.py runs both suites
```

`control_model.py`, `normalize_units.py` and `export_gltf.py` are bridge-agnostic and were ported
unchanged from [manhattan-bridge-3d](https://github.com/Ethical-Tech-CoLab/manhattan-bridge-3d).

---

## The validation harness

Two suites, three modes: `assert` fails the build, `report_only` surfaces a number without blocking,
and ratchets guard against regression.

**Every guard has been proven to have teeth.** After writing a test that asserts a defect is absent,
its measure was run against the defective arrangement and confirmed to fail there — a guard that
reports success both before and after a fix is worse than no guard at all.

| Guard | Proven by |
|---|---|
| **GRT-010** no longitudinal gap in the deck chain | Truncating the deck at the anchorage faces — the bug that shipped twice on the Manhattan Bridge, leaving the roadway and every track terminating in mid-air. Fails with the exact gap reported. |
| **GRT-007** two transit tracks, no third or fourth | Setting the track count to four. Fails naming `transit_track_3` and `transit_track_4`. |
| **STT-012** the manifest matches the control document | Editing `GEOMETRY-CONTROL.md` without rebuilding. Fails with both hashes. |

The deck-continuity test measures the longitudinal extent of the **geometry the build actually
emitted**, not a declared constant, so it tests the model rather than a promise about it.

One bug of the same family was found and fixed during this work: the source-register parser located
its `Verified` column by a hardcoded index and was off by one, marking every read source as unread.
It now reads the table header. `HOW-TO-DESIGN.md` §11 records the same class of failure on the
Manhattan Bridge. **Test your tests.**

---

## Negative controls

Cross-contamination between three similar East River suspension bridges is the most likely way this
programme produces a confident wrong number. `SOURCE-REGISTER.md` §5 registers, as material that
must never enter this model:

- every dimension of the **Manhattan Bridge**, which sits in a sibling directory on the same disk;
- every dimension of the **Brooklyn Bridge**, whose span this bridge's own HAER record invites you
  to compare;
- the **four-track deck taxonomy** in this repository's own build brief;
- `HOW-TO-DESIGN.md`'s incorrect survey number;
- **any figure produced by this repository's own scripts or agents, used as external corroboration.**

Tests STT-014 and STT-015 keep the negative controls declared and uncited.

---

## Next milestone

Milestone 2 is source verification: retire placeholders by reading sources, not by guessing. In
priority order — file the FOIL request, obtain the AISC 2005 reconstruction paper, find any source
stating the side-span length, and retrieve the 2017 NYC topobathymetric LiDAR for the approach
ground profile.

Lowering the placeholder ratchet in `tests/geometry_regression_tests.json` from 6 is the measure of
that milestone's success.

---

## Licence

Repository content: see `LICENSE.md`. Retrieved source material keeps its own licence, recorded in
`SOURCE-REGISTER.md` §7.
