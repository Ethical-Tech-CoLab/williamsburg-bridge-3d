# HO Scale Reference — Williamsburg Bridge

Reporting scale: **1:87.1** (HO).

## 1. Scale is a reporting layer, never an authoring layer

Every dimension in this repository is authored at prototype scale, in the unit its source published,
and converted to meters exactly once by `scripts/normalize_units.py`. HO figures are **derived at
report time** and stored only in `viewer/metadata/scale_ho.json`, which the build regenerates.

Nothing in `GEOMETRY-CONTROL.md` is ever expressed in HO. If a scaled number were authored, a later
change to the scale denominator would silently corrupt it.

## 2. Conversions

```
1 prototype meter  = 1000 / 87.1  = 11.4811 mm HO
1 prototype foot   = 304.8 / 87.1 = 3.4995 mm HO
1 HO millimeter    = 87.1 mm      = 0.0871 m prototype
```

`scripts/build_control_skeleton.py` also writes `mesh/glb/control_skeleton_ho.glb`, which is the
same geometry with a uniform 1/87.1 scale applied at export. Vertex data in the prototype GLB stays
in bridge coordinates so that it remains directly comparable to the control tables.

## 3. What this bridge looks like in HO

Derived from the controls; regenerate with `python scripts/normalize_units.py`.

| Control | Prototype | HO |
|---|---:|---:|
| CTL-001 main span, tower to tower | 1600 ft (487.68 m) | 5599 mm — **5.6 metres** |
| CTL-002 total length with approaches | 7308 ft (2227.48 m) | 25574 mm — **25.6 metres** |
| CTL-006 tower height | 310 ft (94.49 m) | 1085 mm |
| CTL-008 deck width | 118 ft (35.97 m) | 413 mm |
| CTL-003 navigation clearance at centre | 135 ft (41.15 m) | 472 mm |
| CTL-005 main cable diameter | 18 in (0.457 m) | 5.25 mm |
| CTL-014 suspender rope diameter | 1.75 in (0.044 m) | 0.51 mm |

## 4. The consequence, stated plainly

**A complete HO Williamsburg Bridge is over 25 metres long.** That is not a layout element; it is a
building. `AGENT-INSTRUCTIONS.md` §2 anticipates this: treat the full bridge as a digital twin
first, and extract modular study pieces later.

Natural study modules, in rough order of usefulness:

| Module | Prototype extent | HO length |
|---|---|---:|
| One tower, pier to saddle | CTL-006 | 1085 mm tall |
| Main span between towers | CTL-001 | 5599 mm |
| One side span, tower to anchorage | CTL-101 *(placeholder)* | about 2100 mm |
| One anchorage | CTL-030 to CTL-033 | 620 x 530 mm |
| One deck bay between floor beams | CTL-012 | 70 mm |

The deck bay is the honest starting point for physical work: it is 70 mm long, it exercises the full
transverse section, and it is the smallest piece that would expose whether the five-section deck
division is right — which OQ-007 says it is not yet known to be.

## 5. Rounding

Rounding is applied at report time only, by `normalize_units.ho_report()`:

- HO millimetres: two decimals below 10 mm, one decimal above.
- HO inches: three decimals below 1 in, two above.

Prototype values are never rounded in the stored data.

## 6. Printing is out of scope here

`AGENT-INSTRUCTIONS.md` is explicit that this programme does not optimise for slicer settings,
infill or supports. A part measured at 0.51 mm in HO — the suspender ropes — is below what most
processes resolve, and the answer to that is a print-preparation decision recorded in a
print-preparation document, not a change to a sourced dimension.
