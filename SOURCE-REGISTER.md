# Source Register — Williamsburg Bridge

Every dimension in this repository traces to a row in this file. A source that is not registered
here cannot grade anything, **including a source held locally in a sibling repository**.

## Rules

1. **Only confidence `D` may cite no source.** Anything `A`, `B` or `C` without a source ID is a
   parse error in `scripts/control_model.py`, not a review comment.
2. **A source may only grade a control once it has been read.** Registration is not verification.
   The `Verified` column below records whether *this repository's agent opened the source and read
   the passage it relies on*. An unverified source may sit in the register and in the queue; it may
   not appear in a control row.
3. **Quote, do not summarise.** Section 3 holds the exact passage each control rests on. A control
   whose supporting passage cannot be quoted is not documented, it is inferred.
4. **Negative controls are sources too.** Section 5 registers material that must never enter this
   model. Cross-contamination between three similar East River suspension bridges is the most
   likely way this programme produces a confident wrong number.

---

## 1. Registered sources

| Source ID | Title | URL or archive reference | Type | Tier | Licence | Verified | Confidence impact | Notes |
|---|---|---|---|---|---|---|---|---|
| SRC-001 | Historic American Engineering Record, *Williamsburg Bridge*, HAER No. NY-128, written historical and descriptive data | https://tile.loc.gov/storage-services/master/pnp/habshaer/ny/ny1200/ny1263/data/ny1263data.pdf — local copy `sources/drawings/ny1263data.pdf` | Archival engineering record | A | Public domain (US Government work) | yes | A | 3 data pages. Transmitted by Monica E. Hawley, Historian, 1983. Carries a single `SPECIFICATIONS` paragraph, quoted in section 3. No measured drawings exist in this survey. |
| SRC-002 | Historic American Engineering Record, *Williamsburg Bridge*, HAER No. NY-128, index to photographs | https://tile.loc.gov/storage-services/master/pnp/habshaer/ny/ny1200/ny1263/data/ny1263cap.pdf — local copy `sources/drawings/ny1263cap.pdf` | Archival photo index | B | Public domain (US Government work) | yes | B | 9 photographs: NY-128-1..4 by Jack Boucher 1978, NY-128-5..9 by Jet Lowe October 1991. Captions are viewpoint descriptions only; they carry no dimensions. |
| SRC-003 | New York City Department of Transportation, *Williamsburg Bridge — About the Bridge* (Bridge Facts) | https://www.nyc.gov/html/dot/html/infrastructure/williamsburg-bridge.shtml — retrieved 2026-08-09, quoted in section 3, page not redistributed | Official owner facts | A | © City of New York, quoted as fact under fair use | yes | A | The bridge owner's own published figures. Eight facts plus a deck description. Quoted in section 3. |
| SRC-004 | Wikipedia, *Williamsburg Bridge* (revision read 2026-08-09), sections Description, Deck, Caissons and towers, Cables, Anchorages | https://en.wikipedia.org/wiki/Williamsburg_Bridge | Tertiary encyclopaedia | C | CC BY-SA 4.0 | yes | C | Read directly via the MediaWiki API, not via a search snippet. Densely cited to works this repository has **not** opened; those underlying works are therefore *not* registered and this source may grade no higher than `C`. |
| SRC-005 | Library of Congress item record for HAER survey `ny1263` (JSON API) | https://www.loc.gov/item/ny1263/?fo=json | Archival catalogue metadata | A | Public domain | yes | A | Establishes the survey identity: call number `HAER NY,31-NEYO,165-`, survey number **HAER NY-128**, 9 photographs, 3 data pages, 2 caption pages, **0 measured drawings**. |
| SRC-006 | NYCDOT, *Bridges and Tunnels Annual Condition Report 2015* | https://www.nyc.gov/html/dot/downloads/pdf/dot_bridgereport15.pdf — retrieved 2026-08-09, not committed (28 MB; re-fetch from the URL) | Official condition report | A | © City of New York | yes | — | 307 pages, retrieved and searched. **Grades nothing.** It carries rehabilitation history and condition ratings but no span geometry. Registered so that the negative result is on the record and nobody re-fetches it. |
| SRC-007 | Haight, R. and Patel, N., *Reconstruction of the Williamsburg Bridge*, AISC, 2005 | Not obtained; not reachable from `aisc.org` at the paths tried on 2026-08-09 | Engineering paper | A (potential) | Unknown | **no** | none yet | Named by `HOW-TO-DESIGN.md` §10 as the one real transverse source for this bridge, co-authored by the NYCDOT Director of East River Bridges. **Nothing in this model is graded on it**, because this repository has not read it. See section 4. |
| SRC-008 | 2017 NYC Topobathymetric LiDAR (1 ft DEM/DSM and classified point cloud) | NYC Open Data / NYS GIS clearinghouse / NOAA S3 `noaa-nos-coastal-lidar-pds` / OpenTopography | Remote sensing | A (potential) | Public domain | **no** | none yet | Aerial, so it sees the top of the deck only. The right tool for approach grade and ground profile; useless for anything underneath. See section 4. |
| SRC-009 | NYCDOT record, shop and rehabilitation drawings | Not public — obtainable only by FOIL request to NYCDOT | Archival drawings | A (potential) | Unknown | **no** | none yet | The single highest-value outstanding action on this bridge. Long lead time. See section 4. |

## 2. Tier definitions

| Tier | Role |
|---|---|
| A | Control geometry. Establishes the bridge coordinate system and its dimensions. |
| B | Detail geometry. Secondary validation and part-level detail. |
| C | Existing meshes, photogrammetry and tertiary compilations. Reference overlays only. |

Tier is a property of the *source*. Confidence is a property of the *claim*. A Tier A source can
still support only a `D`-grade claim if the passage relied on does not actually state the number —
see `CONFIDENCE-MODEL.md`.

---

## 3. Quoted passages

Every control in `GEOMETRY-CONTROL.md` graded `A`, `B` or `C` rests on one of these passages. They
are reproduced verbatim, including the original's errors.

### SRC-001 — HAER No. NY-128, data page 2

> DATE: ca. 1903
> LOCATION: Spanning East River at South 6th, New York, New York
> DESIGNED BY: Leffert Lefferts Buck
> OWNER: New York Department of Public Works
> **SPECIFICATIONS: Suspension bridge; steel towers; spans 1,600 feet between towers; total
> length, 7,200 feet; clearance for ships, 135 feet; double decked; 4 main cables 18 inches in
> diameter; cost $8 million**
> SIGNIFICANCE: The Williamsburg Bridge is the longest span suspension bridge over the East River,
> it's span exceeding that of the Brooklyn Bridge by 4.5 feet.

This is the *entire* dimensional content of the national record for this bridge. Note what it does
not contain: no side-span length, no tower height, no deck width, no anchorage dimension, and no
statement locating anything transversely.

### SRC-003 — NYCDOT, Bridge Facts

> Total length: 7,308 feet
> Main span: 1,600 feet
> Clearance at center: 135 feet
> Height of towers: 310 feet
> Number of cables: 4 cables
> Diameter of each cable: 18 inches
> Weight of cables: 4,344 tons
> Total length of wires: 17,500 miles

And, on the deck arrangement:

> Currently, the bridge carries four two-lane vehicular roadways, a south roadway (inner and outer)
> and north roadway (inner and outer), with two rapid transit tracks (J, M, and Z subway lines)
> sandwiched in between. A walkway and a bikeway also run across the bridge.

### SRC-004 — Wikipedia, *Williamsburg Bridge*

Deck and stiffening trusses:

> The deck measures 118 ft wide. The center suspension span measures 1,600 ft long and mostly hangs
> from cables, as in similar suspension bridges. A 100 ft-long section of the center span is
> cantilevered outward from either tower.
>
> The main deck is divided into five sections of roughly equal width. The center section contains
> two rapid transit tracks. These were flanked originally by two pairs of streetcar tracks, which
> are now the inner roadways. The outermost sections of the deck were used as vehicular roadways
> from the outset, measuring 20 ft wide.
>
> The side spans (also known as the end spans), between the tower and the corresponding anchorage on
> either side, are supported by their trusswork. This was done to reduce the size, cost, and length
> of the main cables. Intermediate towers support both of the side spans, in contrast to the
> Brooklyn Bridge, where the side spans were supported by cables.
>
> The deck is placed above transverse floor beams measuring 5 ft deep and 118 ft long and spaced at
> intervals of 20 ft. [...] **The trusses are placed 67 ft apart and measure 40 ft deep.** [...]
> **The trusswork runs continuously from one anchorage to the other and is not rigidly connected to
> either the towers or the anchorages.**
>
> The approach spans, between the anchorages and either end of the bridge, have a 3 percent grade.
>
> The subway tracks are laid to standard gauge, and their centers are spaced 11 ft apart.

Towers:

> Each foundation supports a masonry pier that rises to 23 ft above mean high water. [...] There are
> legs on the south and north sides of both suspension towers; each leg comprises four columns that
> are diagonally braced together. Viewed from above, each leg forms a rectangle measuring 40 ft
> west–east and 24 ft north–south. The lowest portion of each column tapers to a square cross-section
> measuring 4 by 4 ft [...] Above the bridge's deck, the upper sections of the towers' legs are
> slanted inward and are stiffened by a pair of trusses measuring 45 ft high. The tops of each tower
> are about 14 ft narrower than at the deck level, and they measure about 333 ft or 335 ft above mean
> high water.
>
> The centers of each pair of caissons are placed 97.5 ft apart.

Cables:

> The main cables are grouped in two pairs, one each on the north and south sides of the bridge. At
> the anchorages on either end, each pair of cables is spaced 34 ft apart; they narrow to 22 ft apart
> at the top of the towers and 4 ft apart at the middle of the span. The main cables are "cradled"
> together at the center of the span [...] The main cables each measure between 18 in and 18.75 in
> across.
>
> On the main span, there are suspender castings on the main cables, placed at intervals of 20 ft.
> The suspension cables, which hang from the suspension castings, are each composed of seven strands
> of rope measuring 1.75 in in diameter.

Anchorages, and the overall envelope:

> At either end of the main span are massive masonry anchorages placed 570 ft or 590 ft inland of the
> shore. [...] At its base, the Manhattan anchorage measures 178 by 152 ft across, while the Brooklyn
> anchorage measures 182 by 158 ft across. Each anchorage rises 80 ft above street level and has a
> foundation 40 ft deep. [...] The above-ground sections of the anchorages were clad with masonry.
>
> The bridge, including approaches, is 7,308 ft long and 118 ft wide. The bridge reaches a maximum
> height of 135 ft above mean high water at the middle of the river, and the deck is around 122 ft
> above mean high water at either shoreline.

**Read this passage carefully before using it.** "The bridge reaches a maximum height of 135 ft
above mean high water at the middle of the river" cannot mean the top of the structure, because the
same article puts the tower tops at 333–335 ft. Read against SRC-001 ("clearance for ships, 135
feet") and SRC-003 ("Clearance at center: 135 feet"), the 135 ft figure is the **navigation
clearance beneath the span**, and this repository uses it only in that sense.

---

## 4. Verification queue

In priority order. Nothing here may grade a control until it moves to section 1 with `Verified: yes`.

| # | Source | Action | Why it matters |
|---|---|---|---|
| 1 | SRC-009 | **File the NYCDOT FOIL request for record, shop and rehabilitation drawings.** | Longest lead time, largest payoff. It is the only route to `A`-grade transverse geometry and would retire OQ-001, OQ-003, OQ-005 and OQ-007 at once. This is a request, not a research problem. |
| 2 | SRC-007 | Obtain the AISC 2005 paper through a library or AISC membership. | `HOW-TO-DESIGN.md` reports it gives the stiffening truss as *"67 feet wide and approximately 40 feet deep and is pinned at each main tower"* and a labelled transverse section. SRC-004 independently states 67 ft / 40 ft, so reading SRC-007 would raise CTL-008 and CTL-009 from `C` toward `A`, and the "pinned at each main tower" clause bears directly on OQ-011. |
| 3 | — | Identify a source that states the **side-span length** (tower to anchorage). | OQ-001. Every station outboard of the towers currently rests on a placeholder. This one number unlocks more geometry than any other. |
| 4 | SRC-008 | Retrieve the LiDAR tile covering the bridge corridor. | Would give a `MEASURED` deck-top profile and an approach ground profile, and would settle OQ-006. |
| 5 | — | The works cited by SRC-004 behind the 67 ft / 40 ft / 97.5 ft / anchorage figures. | Reading them directly would let those controls cite a primary instead of an encyclopaedia. `HOW-TO-DESIGN.md` §11 records what trusting a secondary's gloss cost on the Manhattan Bridge. |

---

## 5. Negative controls — sources that must never enter this model

Registered so that cross-contamination becomes a test failure rather than a silent error.

| ID | Prohibited material | Where it lives | Why it is dangerous here |
|---|---|---|---|
| NEG-001 | Every dimension of the **Manhattan Bridge** | `manhattan-bridge-3d/GEOMETRY-CONTROL.md` and its `SOURCE-REGISTER.md`, present on the same filesystem as this repository | A three-tower-type, four-track, 1,470 ft-span East River suspension bridge a mile away. Its figures are *not* approximations of Williamsburg figures; they are a different structure's measurements. |
| NEG-002 | Every dimension of the **Brooklyn Bridge** | HAER survey `ny1234`, including the one measured drawing sheet in the national record | The nearest neighbour and the most-written-about. SRC-001 itself invites the error by comparing the two spans, and SRC-004 compares truss depths and side-span support. |
| NEG-003 | **The four-track deck taxonomy in `AGENT-INSTRUCTIONS.md` §6** (`track_1`..`track_4`) | This repository's own build brief | The brief was adapted from the Manhattan Bridge, which carries four tracks. The Williamsburg Bridge carries **two** rapid transit tracks (SRC-003, SRC-004). The brief is wrong on this point and the model follows the sources. See CNF-003. |
| NEG-004 | **`HOW-TO-DESIGN.md`'s survey number "HAER NY-165"** | `HOW-TO-DESIGN.md` §10 | The survey number is **NY-128** (SRC-001, SRC-005). 165 is the NYC index number inside the call number `HAER NY,31-NEYO,165-`. Citing NY-165 would send a future reader to the wrong record. See CNF-007. |
| NEG-005 | Any figure produced by this repository's own scripts, tables or agents, when used as *external corroboration* | This repository | Recorded in `HOW-TO-DESIGN.md` §11: an exploration agent with filesystem access read the local repository and reported its own `CTL-` and `SRC-` values back as independent confirmation. Always ask where a fact came from. |

---

## 6. Registered conflicts

Conflicts are kept, not smoothed away. A model that hides source disagreement is lying by omission.

| ID | Subject | Position A | Position B | State | Resolution and reasoning |
|---|---|---|---|---|---|
| CNF-001 | Total length including approaches | **7,308 ft** — SRC-003, SRC-004 | **7,200 ft** — SRC-001 | **Settled by weight of evidence** | CTL-002 adopts 7,308 ft. The owner's current published figure (SRC-003) agrees with SRC-004, and 7,200 ft has the shape of a round number in a one-line 1983 summary. The disagreement is 108 ft — 1.5% — and is carried as an uncertainty on every approach-end station. |
| CNF-002 | Tower height | **310 ft** — SRC-003 | **"about 333 ft or 335 ft above mean high water"** — SRC-004 | **Open** | CTL-006 adopts the owner's 310 ft because SRC-003 outranks SRC-004, but SRC-003 does not state a datum, so the 25 ft gap may be a datum difference (deck level vs mean high water) rather than a factual disagreement. SRC-004 is internally uncertain too, offering two values. See OQ-004. Nothing in the model may treat the tower top elevation as settled. |
| CNF-003 | Number of rapid transit tracks | **2** — SRC-003, SRC-004 | **4** — `AGENT-INSTRUCTIONS.md` §6 and §13 | **Settled against the brief** | The model carries two tracks. The four-track taxonomy is an artifact of adaptation from the Manhattan Bridge; see NEG-003. `AGENT-INSTRUCTIONS.md` has been annotated rather than silently obeyed. |
| CNF-004 | Main cable diameter | **18 in** — SRC-001, SRC-003 | **"between 18 in and 18.75 in"** — SRC-004 | **Settled by weight of evidence** | CTL-005 adopts 18 in as the nominal diameter. SRC-004 does not contradict it; it reports a range whose lower bound is the nominal value. The 0.75 in variation is below any tolerance this model can resolve. |
| CNF-005 | Anchorage set-back from the shore | **570 ft** — SRC-004 | **590 ft** — SRC-004 | **Open** | A single source offering two values. Neither is used: the shoreline station is itself unknown (OQ-001), so this cannot place the anchorages. Registered so the next reader does not mistake it for a side-span length — it is not one. |
| CNF-006 | Wires per main cable strand | **208** — SRC-004 | **"280, 281, or 282"** — SRC-004, explanatory note | **Open** | Not used by any control. Registered because a future cable-detail milestone will hit it. |
| CNF-007 | HAER survey number | **NY-128** — SRC-001, SRC-005 | **NY-165** — `HOW-TO-DESIGN.md` §10 | **Settled** | NY-128. The document that carried the error is a method guide copied in from a sibling repository, not a source; it is registered as NEG-004. |
| CNF-008 | Tower saddle weight | **32.5 short tons** — SRC-004 | **36 short tons** — SRC-004 | **Open** | Not used by any control. |

---

## 7. Licences and provenance of retrieved material

| Path | Source | Licence | Redistribution |
|---|---|---|---|
| `sources/drawings/ny1263data.pdf` | SRC-001 | Public domain (US Government work) | Yes |
| `sources/drawings/ny1263cap.pdf` | SRC-002 | Public domain (US Government work) | Yes |
| *(not committed)* | SRC-003 | © City of New York | Retrieved 2026-08-09 and read. The passages relied on are quoted verbatim in section 3; the page itself is not redistributed. |
| *(not committed)* | SRC-006 | © City of New York | 28 MB. Retrieved, searched, and found to carry no span geometry. Re-fetch from the URL rather than committing it. |

No mesh, photogrammetry, video or marketplace asset has been ingested. `sources/existing-meshes/`,
`sources/photos/`, `sources/videos/` and `photogrammetry/` are empty by design at Milestone 1:
nothing may be imported before there is a control skeleton to align it against.
