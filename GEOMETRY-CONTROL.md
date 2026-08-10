# Geometry Control — Williamsburg Bridge

**This document is the single source of truth for every dimension in this repository.** Scripts carry
no numbers of their own; if a dimension appears in Python, it is a bug. `scripts/control_model.py`
parses the tables below and enforces their contract at load time.

Parsing contract, enforced rather than reviewed:

- Any markdown row whose first cell matches `CTL-<digits>` is a control row and must have exactly
  seven columns. Any row matching `MAT-<digits>` is a material rule and must have exactly six.
- **Only confidence `D` may cite no source. Confidence `D` may not cite sources.**
- Values are **bare decimals**. No thousands separators, no ranges, no "approx", no units in the
  value cell.
- Units come from the closed set `ft`, `in`, `m`, `mm`, `count`, `ratio` and are converted in exactly
  one place, `scripts/normalize_units.py`.

---

## 1. Coordinate system and datum

| Property | Value | Basis |
|---|---|---|
| World units | meters | `AGENT-INSTRUCTIONS.md` §5.1 |
| Authoring units | as published by the source, converted once | §5.1 and `normalize_units.py` |
| Origin | midpoint of the main span | `AGENT-INSTRUCTIONS.md` §5.3 |
| `+X` | along the bridge, Manhattan (west) negative, Brooklyn (east) positive | §5.4 |
| `+Y` | across the bridge, north positive | §5.5 |
| `+Z` | vertical, up | §5.6 |
| Up axis on export | Z-up authoring, rotated to glTF Y-up at the scene root only | `scripts/export_gltf.py` |
| **Vertical datum** | **mean high water (MHW), `Z = 0`** | Declared, not converted — see below |
| HO reporting scale | 1:87.1 | `SCALE-HO.md` |

**The vertical datum is declared and not silently converted.** Every elevation this repository has a
source for is published relative to mean high water: SRC-001's "clearance for ships, 135 feet",
SRC-003's "Clearance at center: 135 feet", and SRC-004's "23 ft above mean high water", "122 ft above
mean high water", "333 ft or 335 ft above mean high water". Authoring against MHW keeps every stored
number directly comparable to its source. Converting to NAVD88 or to any district frame belongs at
placement time, in the consumer, with a stated offset — not here.

**The origin is not geolocated.** No latitude or longitude for any part of this bridge is in
`SOURCE-REGISTER.md`, so this model has no georeference and cannot be placed in a district frame yet.
`HOW-TO-DESIGN.md` §11 records what happened on the Manhattan Bridge when invented tower coordinates
were nearly used as ground truth: they implied 823 m between towers against a sourced main span of
about 448 m. An unregistered coordinate verifies nothing, including our own work.

---

## 2. Control dimensions

Sourced values only. Every row cites a registered, verified source.

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-001 | main_span_tower_to_tower | 1600 | ft | SRC-001, SRC-003, SRC-004, SRC-010 | A | "spans 1,600 feet between towers" (SRC-001); "Main span: 1,600 feet" (SRC-003). Four sources agree. The strongest number this bridge has. |
| CTL-002 | total_length_including_approaches | 7308 | ft | SRC-003, SRC-004, SRC-010 | A | Owner's published figure. Conflicts with SRC-001's 7,200 ft — see CNF-001. SRC-010 gives the same number but says "between approaches" rather than including them, which inverts the meaning: CNF-014, and direct evidence on OQ-006. |
| CTL-003 | navigation_clearance_at_center | 135 | ft | SRC-001, SRC-003, SRC-004, SRC-010 | A | Clearance beneath the span at mid-river, above MHW. Fixes the underside of the structure at the origin. |
| CTL-004 | main_cable_count | 4 | count | SRC-001, SRC-003, SRC-004, SRC-010 | A | "4 main cables" (SRC-001). Grouped in two pairs, north and south (SRC-004). |
| CTL-005 | main_cable_diameter | 18 | in | SRC-001, SRC-003, SRC-010 | A | Nominal. SRC-004 gives 18 to 18.75 in; see CNF-004. |
| CTL-006 | tower_height | 310 | ft | SRC-003, SRC-010 | A | Owner's figure, now independently corroborated by SRC-010 ("two all-steel towers reach a height of 310 ft"). **Neither source states a datum** — see CNF-002 and OQ-004. SRC-004 says 333 or 335 ft above MHW. Two sources now favour 310, but a second statement of the same undatumed number does not supply the datum. |
| CTL-007 | transit_track_count | 2 | count | SRC-003, SRC-004 | A | "two rapid transit tracks (J, M, and Z subway lines) sandwiched in between" (SRC-003). **Not four** — see CNF-003 and NEG-003. |
| CTL-008 | deck_width | 118 | ft | SRC-004 | C | Also the length of the transverse floor beams, which is a useful internal consistency check on the figure. |
| CTL-009 | stiffening_truss_spacing | 67 | ft | SRC-004 | C | "The trusses are placed 67 ft apart". Independently reported by SRC-007 per `HOW-TO-DESIGN.md` §10, but this repository has not read SRC-007, so the grade stays `C`. |
| CTL-010 | stiffening_truss_depth | 40 | ft | SRC-004, SRC-010 | B | "and measure 40 ft deep" (SRC-004); "Massive 40-ft-deep steel stiffening trusses carry the decks" (SRC-010). **The first grade B control in this model** — two independent secondary records agreeing, which is exactly what B means. |
| CTL-011 | floor_beam_depth | 5 | ft | SRC-004 | C | Transverse floor beams. |
| CTL-012 | floor_beam_spacing | 20 | ft | SRC-004 | C | Equal to the suspender spacing, which is what one would expect and is stated separately. |
| CTL-013 | suspender_spacing_main_span | 20 | ft | SRC-004 | C | "suspender castings on the main cables, placed at intervals of 20 ft". Stated for the main span only. |
| CTL-014 | suspender_rope_diameter | 1.75 | in | SRC-004 | C | Seven strands of rope per suspender. |
| CTL-015 | outer_roadway_width | 20 | ft | SRC-004 | C | The outermost of the five deck sections, each side. |
| CTL-016 | deck_section_count | 5 | count | SRC-004 | C | "divided into five sections of roughly equal width". "Roughly" is doing real work here — see OQ-007. |
| CTL-017 | transit_track_center_spacing | 11 | ft | SRC-004 | C | Standard gauge, centres 11 ft apart. |
| CTL-018 | cable_pair_spacing_at_anchorage | 34 | ft | SRC-004 | C | Spacing *within* a pair, at the anchorage. |
| CTL-019 | cable_pair_spacing_at_tower_top | 22 | ft | SRC-004 | C | Spacing within a pair, at the saddles. |
| CTL-020 | cable_pair_spacing_at_midspan | 4 | ft | SRC-004 | C | The cables are "cradled" together at mid-span to resist wind. This is the transverse geometry that makes this bridge look like itself. |
| CTL-021 | tower_leg_center_spacing | 97.5 | ft | SRC-004 | C | Stated of the caisson pair centres. SRC-010 states that each tower "sit[s] on two separate masonry piers" and SRC-011 shows exactly that, so the two-legs-on-two-piers *arrangement* is now well supported. The *spacing* is still taken from a caisson figure, which remains an inference: the legs are known to stand on those foundations, not known to stand on their centres. Parts using this row stay `INFERRED` for that reason. |
| CTL-022 | tower_leg_plan_length_we | 40 | ft | SRC-004 | C | "each leg forms a rectangle measuring 40 ft west–east". |
| CTL-023 | tower_leg_plan_width_ns | 24 | ft | SRC-004 | C | "and 24 ft north–south". |
| CTL-024 | tower_pier_top_elevation | 23 | ft | SRC-004 | C | Masonry pier top, above MHW. The one solidly-datumed elevation in the whole document. |
| CTL-025 | tower_column_base_side | 4 | ft | SRC-004 | C | Square cross-section at the foot of each column. |
| CTL-026 | tower_upper_truss_height | 45 | ft | SRC-004 | C | Trusses stiffening the inward-slanted upper legs above deck level. |
| CTL-027 | tower_top_narrowing | 14 | ft | SRC-004 | C | Tower tops are about 14 ft narrower than at deck level. |
| CTL-028 | deck_elevation_at_shoreline | 122 | ft | SRC-004 | C | Above MHW. **Not consumed as a vertex** — the shoreline station is unknown (OQ-001). Used by GRT-011 as a report-only sanity check on the modelled deck profile. |
| CTL-029 | main_span_cantilever_from_tower | 100 | ft | SRC-004 | C | A 100 ft section of the centre span is cantilevered outward from either tower. |
| CTL-030 | manhattan_anchorage_base_length | 178 | ft | SRC-004 | C | At the base. Which axis is which is not stated: OQ-008. |
| CTL-031 | manhattan_anchorage_base_width | 152 | ft | SRC-004 | C | As above. |
| CTL-032 | brooklyn_anchorage_base_length | 182 | ft | SRC-004 | C | As above. |
| CTL-033 | brooklyn_anchorage_base_width | 158 | ft | SRC-004 | C | As above. |
| CTL-034 | anchorage_height_above_street | 80 | ft | SRC-004 | C | Above *street level*, which is not an elevation this model knows: OQ-005. |
| CTL-035 | anchorage_foundation_depth | 40 | ft | SRC-004 | C | Below street level. Not modelled; recorded for a later foundation milestone. |
| CTL-036 | approach_grade | 0.03 | ratio | SRC-004 | C | "The approach spans, between the anchorages and either end of the bridge, have a 3 percent grade." |
| CTL-037 | main_cable_strand_diameter | 3 | in | SRC-004 | C | 37 hexagonal strands per cable. Not modelled at Milestone 1. |

## 3. Placeholders

**Every row here is grade `D`, cites no source, and is linked to an open question.** These numbers
are engineering judgement standing in for numbers nobody has read. They are deliberately given round
values so that they cannot be mistaken for measurements, and every part that consumes one is derived
as `ASSUMED` and excluded from dimension callouts.

| Control ID | Key | Value | Unit | Source IDs | Confidence | Notes |
|---|---|---:|---|---|---|---|
| CTL-101 | side_span_tower_to_anchorage | 600 | ft | | D | **OQ-001, and now CNF-009.** SRC-010 states "the relatively short (300 ft) side spans" — the first side-span length any source read here has given. It is **not adopted**: it is roughly half the 570–590 ft the anchorages are said to sit inland of the shore, and SRC-011 shows the towers standing essentially at the shoreline. It may describe one panel between a main tower and an intermediate tower rather than the whole span. This row therefore stays a deliberately round placeholder. Do not quote it, and do not quietly replace it with 300 either. |
| CTL-102 | main_cable_elevation_at_midspan | 190 | ft | | D | **OQ-002.** No source read states the cable sag. Chosen only to clear the deck: it must sit above the deck top, which derivation DRV-007 puts at 175 ft. The main cable profile is therefore `ASSUMED` in Z even though the cable's existence and count are grade `A`. |
| CTL-103 | deck_elevation_at_anchorage | 140 | ft | | D | **OQ-006.** No source read gives the deck elevation where the suspended structure meets the anchorage. |
| CTL-104 | anchorage_top_elevation | 90 | ft | | D | **OQ-005.** CTL-034 gives 80 ft above *street level*, and this model does not know street level at either anchorage. Deliberately round. |
| CTL-105 | intermediate_towers_per_side_span | 1 | count | | D | **OQ-003.** SRC-004 states intermediate towers support both side spans and describes their form, but states neither how many there are nor where they stand. |
| CTL-106 | tower_saddle_height | 8 | ft | | D | **OQ-009.** SRC-004 gives saddle plan dimensions (7.67 by 19 by 4 ft) but this repository has not established which figure is the height as installed. |

## 4. Derivation rules

Derivations are computed by `scripts/build_control_skeleton.py` from the controls above. They are
listed here so that a reader can reproduce every coordinate in the model by hand.

| Rule ID | Derived quantity | Rule | Inputs | Resulting grade |
|---|---|---|---|---|
| DRV-001 | `station_main_span_midpoint` | `x = 0` | origin definition | A |
| DRV-002 | `station_manhattan_tower` | `x = -CTL-001 / 2` | CTL-001 | A |
| DRV-003 | `station_brooklyn_tower` | `x = +CTL-001 / 2` | CTL-001 | A |
| DRV-004 | `station_manhattan_anchorage` | `x = -(CTL-001 / 2 + CTL-101)` | CTL-001, CTL-101 | D |
| DRV-005 | `station_brooklyn_anchorage` | `x = +(CTL-001 / 2 + CTL-101)` | CTL-001, CTL-101 | D |
| DRV-006 | `station_approach_end` | `x = ±CTL-002 / 2` | CTL-002 | A |
| DRV-007 | `deck_top_elevation_at_midspan` | `z = CTL-003 + CTL-010` | CTL-003, CTL-010 | C |
| DRV-008 | `deck_underside_elevation_at_midspan` | `z = CTL-003` | CTL-003 | A |
| DRV-009 | `tower_top_elevation` | `z = CTL-006`, treating the owner's tower height as an elevation above MHW | CTL-006 | A, with OQ-004 open |
| DRV-010 | `truss_half_spacing` | `y = ±CTL-009 / 2` | CTL-009 | C |
| DRV-011 | `deck_half_width` | `y = ±CTL-008 / 2` | CTL-008 | C |
| DRV-012 | `cable_y_positions` | Four cables at `y = ±(CTL-021 / 2 ± s / 2)` is **not** used. The pair centres are taken as the truss lines (DRV-010) and `s` interpolates linearly along `x` between CTL-018 at the anchorage, CTL-019 at the tower and CTL-020 at mid-span. | CTL-009, CTL-018, CTL-019, CTL-020 | C |
| DRV-013 | `suspender_stations` | Every `CTL-013` along `x` strictly between the two towers | CTL-001, CTL-013 | C |
| DRV-014 | `deck_profile` | Linear from `DRV-007` at mid-span to `CTL-103` at each anchorage, then `CTL-036` downgrade outward to each approach end | CTL-003, CTL-010, CTL-103, CTL-036, CTL-002, CTL-101 | D |
| DRV-015 | `approach_end_elevation` | `z = CTL-103 - CTL-036 x (CTL-002 / 2 - (CTL-001 / 2 + CTL-101))` | CTL-103, CTL-036, CTL-002, CTL-001, CTL-101 | D |
| DRV-016 | `tower_leg_y` | `y = ±CTL-021 / 2` | CTL-021 | C |
| DRV-017 | `transit_track_y` | `y = ±CTL-017 / 2` | CTL-017 | C |
| DRV-018 | `suspended_structure_length` | `CTL-001 + 2 x CTL-101` | CTL-001, CTL-101 | D |

**DRV-015 produces a result the model does not believe.** Carried through, the approaches descend
only about 68 ft over their length and end roughly 72 ft above MHW, nowhere near street level. At
least one of CTL-103, CTL-036 and the approach length implied by CTL-002 and CTL-101 is wrong. This
is recorded as OQ-006 and reported by GRT-012 rather than being tuned away, because tuning it would
mean choosing a number to make a picture look right.

## 5. Open questions

| ID | Question | Blocks | Retired by |
|---|---|---|---|
| OQ-001 | Does SRC-010's "300 ft side spans" describe the whole tower-to-anchorage span, or one panel of it? | CTL-101, and through it both anchorages, both side spans, the suspended structure length, and the approach lengths | SRC-009 (FOIL), or any source stating the span arrangement panel by panel |
| OQ-002 | What is the main cable sag, or the cable elevation at mid-span? | CTL-102, the whole main cable profile, every suspender length | SRC-007, SRC-009, or a period engineering description |
| OQ-003 | How many intermediate towers support each side span, and where do they stand? | CTL-105, all side-span support geometry, and the reading of CNF-009 | SRC-009. SRC-011 shows side-span structure but no frame covers a full side span end to end, so it cannot supply the count |
| OQ-004 | Is SRC-003's 310 ft tower height measured above mean high water, above the deck, or above the pier top? | The datum of CTL-006, and CNF-002 | A statement of datum from NYCDOT, or SRC-007 |
| OQ-005 | What is street level at each anchorage, in MHW terms? | CTL-104; makes CTL-034's 80 ft usable | SRC-008 (LiDAR) |
| OQ-006 | Between which two points is the 7,308 ft total length measured, and can it be reconciled with a 3% approach grade reaching street level? | CTL-002, CTL-103, DRV-015 | SRC-008, SRC-009. Sharpened by CNF-014: SRC-010 reads the same figure as "between approaches" rather than including them |
| OQ-007 | What is the transverse width and position of each of the five deck sections? | The deck cross-section; currently only the outermost width (CTL-015) and the track spacing (CTL-017) are sourced | SRC-007's labelled section, SRC-009 |
| OQ-008 | Which axis of each anchorage's base rectangle runs along the bridge? | The plan orientation of CTL-030 to CTL-033 | SRC-009, or a georeferenced aerial |
| OQ-009 | What is the installed height of a main cable saddle? | CTL-106 | SRC-007, SRC-009 |
| OQ-010 | Where is this bridge, in any published coordinate frame, from a registered source? | Any georeference; district integration under `HOW-TO-DESIGN.md` §12 | A surveyed coordinate in the register |
| OQ-011 | SRC-007 is reported to say the stiffening truss is "pinned at each main tower". What does that pinning imply for the truss geometry at the towers? | The truss-to-tower connection detail | SRC-007, read directly |

## 6. Stations and elevations

Computed by the build from §4 and reported into `viewer/metadata/build_report.json`. Reproduced here
for reading, not for parsing — the build does not read this table.

| Station | Rule | x (ft) | Grade |
|---|---|---:|---|
| `manhattan_approach_end` | DRV-006 | -3654 | A |
| `manhattan_anchorage` | DRV-004 | -1400 | D |
| `manhattan_tower` | DRV-002 | -800 | A |
| `main_span_midpoint` | DRV-001 | 0 | A |
| `brooklyn_tower` | DRV-003 | +800 | A |
| `brooklyn_anchorage` | DRV-005 | +1400 | D |
| `brooklyn_approach_end` | DRV-006 | +3654 | A |

| Elevation | Rule | z (ft) | Grade |
|---|---|---:|---|
| mean high water | datum | 0 | — |
| tower pier top | CTL-024 | 23 | C |
| deck top at anchorage | CTL-103 | 140 | D |
| deck underside at mid-span | DRV-008 | 135 | A |
| deck top at mid-span | DRV-007 | 175 | C |
| main cable at mid-span | CTL-102 | 190 | D |
| tower top | DRV-009 | 310 | A |

## 7. Materials

Matched **in document order, first glob wins**. There is deliberately **no default rule**: a part
that matches nothing is a build failure, because silently painting it grey would be an unsourced
claim about what the bridge is made of. The material vocabulary is closed and is enforced by
`scripts/control_model.py`.

| Material ID | Applies to | Material | Source IDs | Confidence | Notes |
|---|---|---|---|---|---|
| MAT-001 | `reference_*` | reference | | D | Datum planes, axes and station markers. Not part of the bridge; graded `D` because they are drawing furniture, not structure. |
| MAT-002 | `*anchorage*` | masonry | SRC-004 | C | "massive masonry anchorages"; "The above-ground sections of the anchorages were clad with masonry." |
| MAT-003 | `tower_*_pier_*` | masonry | SRC-004, SRC-010, SRC-011 | B | "Each foundation supports a masonry pier" (SRC-004); "two separate masonry piers" (SRC-010); dressed stone piers plainly visible in SRC-011. A photograph cannot give a dimension, but it can settle what a thing is made of. |
| MAT-004 | `*main_cable*` | steel_wire | SRC-001, SRC-004 | A | "4 main cables 18 inches in diameter" (SRC-001); steel wire strands (SRC-004). |
| MAT-005 | `*suspender*` | steel_wire | SRC-004 | C | Seven strands of rope per suspender. |
| MAT-006 | `tower_*` | steel_structural | SRC-001, SRC-004, SRC-010 | A | "steel towers" (SRC-001). Buck chose steel over stone deliberately; see SRC-004. Confirmed visually in SRC-011. |
| MAT-007 | `*roadway*` | roadway_surface | SRC-003, SRC-004 | C | Four two-lane roadways (SRC-003). Originally wooden blocks, now orthotropic decks from Contracts 5 and 7. |
| MAT-008 | `*walkway*` | roadway_surface | SRC-003 | C | "A walkway and a bikeway also run across the bridge." |
| MAT-009 | `*track*` | steel_structural | SRC-003, SRC-004 | A | Two rapid transit tracks, standard gauge. |
| MAT-010 | `*truss*` | steel_structural | SRC-004, SRC-010, SRC-011 | B | Stiffening trusses, 67 ft apart and 40 ft deep. "Massive 40-ft-deep steel stiffening trusses" (SRC-010), and steel latticework in SRC-011. Note from SRC-011: they are painted a dark red, unlike the grey towers. That is livery, not material, and the vocabulary here describes what a thing is made of. |
| MAT-011 | `*floor_beam*` | steel_structural | SRC-004 | C | Transverse floor beams, 5 ft deep and 118 ft long. |
| MAT-012 | `*railing*` | steel_structural | SRC-004 | C | "heavy lattice railings on the north and south edges of the deck". |
| MAT-013 | `*approach*` | steel_structural | SRC-004, SRC-012 | B | "viaducts with braced columns and masonry foundations" (SRC-004), and riveted steel lattice bents on masonry footings throughout SRC-012. The extreme ends were masonry, so the mixed construction is still unresolved at this milestone; the steel is what the geometry currently represents. |
| MAT-014 | `deck_*` | steel_structural | SRC-004 | C | Any remaining deck-system envelope geometry. |

## 8. Provenance derivation

Stated here so the rule lives with the data. Implemented in `scripts/build_control_skeleton.py`,
never hand-declared per part, and defined in `CONFIDENCE-MODEL.md` §3.

```python
if "photogrammetry" in source_basis or "survey" in source_basis:   MEASURED
elif "control_dimension" not in source_basis or not sourced_refs:   ASSUMED
elif placeholder_refs or "inferred" in source_basis:                INFERRED
else:                                                               DOCUMENTED
```

`MEASURED` is expected to be zero until SRC-008 or a survey is ingested. It is computed rather than
hardcoded so that the number changes honestly on the day that happens.
