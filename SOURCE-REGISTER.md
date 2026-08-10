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
| SRC-002 | Historic American Engineering Record, *Williamsburg Bridge*, HAER No. NY-128, index to photographs | https://tile.loc.gov/storage-services/master/pnp/habshaer/ny/ny1200/ny1263/data/ny1263cap.pdf — local copy `sources/drawings/ny1263cap.pdf`; the photographs themselves in `viewer/public/photos/` | Archival photo index and photographs | B | Public domain (US Government work) | yes | B, **visual only** | 9 photographs: NY-128-1..4 by Jack Boucher 1978, NY-128-5..9 by Jet Lowe October 1991. Captions are viewpoint descriptions and carry no dimensions. All nine are retrieved and shown in the viewer as reference imagery; the captions there are transcribed from this index rather than paraphrased. |
| SRC-003 | New York City Department of Transportation, *Williamsburg Bridge — About the Bridge* (Bridge Facts) | https://www.nyc.gov/html/dot/html/infrastructure/williamsburg-bridge.shtml — retrieved 2026-08-09, quoted in section 3, page not redistributed | Official owner facts | A | © City of New York, quoted as fact under fair use | yes | A | The bridge owner's own published figures. Eight facts plus a deck description. Quoted in section 3. |
| SRC-004 | Wikipedia, *Williamsburg Bridge* (revision read 2026-08-09), sections Description, Deck, Caissons and towers, Cables, Anchorages | https://en.wikipedia.org/wiki/Williamsburg_Bridge | Tertiary encyclopaedia | C | CC BY-SA 4.0 | yes | C | Read directly via the MediaWiki API, not via a search snippet. Densely cited to works this repository has **not** opened; those underlying works are therefore *not* registered and this source may grade no higher than `C`. |
| SRC-005 | Library of Congress item record for HAER survey `ny1263` (JSON API) | https://www.loc.gov/item/ny1263/?fo=json | Archival catalogue metadata | A | Public domain | yes | A | Establishes the survey identity: call number `HAER NY,31-NEYO,165-`, survey number **HAER NY-128**, 9 photographs, 3 data pages, 2 caption pages, **0 measured drawings**. |
| SRC-006 | NYCDOT, *Bridges and Tunnels Annual Condition Report 2015* | https://www.nyc.gov/html/dot/downloads/pdf/dot_bridgereport15.pdf — retrieved 2026-08-09, not committed (28 MB; re-fetch from the URL) | Official condition report | A | © City of New York | yes | — | 307 pages, retrieved and searched. **Grades nothing.** It carries rehabilitation history and condition ratings but no span geometry. Registered so that the negative result is on the record and nobody re-fetches it. |
| SRC-007 | Haight, R. and Patel, J., *Reconstruction of New York City's Williamsburg Bridge*, AISC / World Steel Bridge Symposium, 2005 | https://www.aisc.org/media/nvvl5nm3/haight-2005-wsbs-final.pdf — found via Tavily 2026-08-10, full text extracted and read | Engineering paper | A | © AISC; quoted for scholarly commentary | **yes** | A | **Co-authored by Jay Patel, Director of East River Bridges at NYCDOT** — the owner's own engineer — with Roger Haight of Parsons, the reconstruction designer. This is the single most valuable source yet found for this bridge, and it states in one paragraph the side-span length, the intermediate tower count, the anchorage length and both approach lengths. Quoted in section 3. Earlier attempts to reach it by guessing AISC URLs failed; a Tavily search found it in one query. |
| SRC-008 | 2017 NYC Topobathymetric LiDAR (1 ft DEM/DSM and classified point cloud) | NYC Open Data / NYS GIS clearinghouse / NOAA S3 `noaa-nos-coastal-lidar-pds` / OpenTopography | Remote sensing | A (potential) | Public domain | **no** | none yet | Aerial, so it sees the top of the deck only. The right tool for approach grade and ground profile; useless for anything underneath. See section 4. |
| SRC-009 | NYCDOT record, shop and rehabilitation drawings | Not public — obtainable only by FOIL request to NYCDOT | Archival drawings | A (potential) | Unknown | **no** | none yet | The single highest-value outstanding action on this bridge. Long lead time. See section 4. |
| SRC-010 | *The Historic Williamsburg Bridge in NYC Was the Longest Suspension Bridge in the World When It Opened* | https://www.historic-structures.com/ny/new_york/historic-williamsburg-bridge/ — read 2026-08-09, quoted in section 3 | Secondary compilation | C | © historic-structures.com, quoted for commentary | yes | B/C | A narrative history with a dense specification paragraph and a detailed construction account. Corroborates several figures previously resting on SRC-004 alone, which is what lets CTL-010 and two material rules reach grade `B`. It also states a **side-span length**, the first source read to do so — but see CNF-009 before using it. Uncited and unfootnoted, so it may not exceed `C`. |
| SRC-011 | *Aerial view of the Williamsburg Bridge in New York*, Alex Kane — watermarked preview, 960x540, 11.9 s, 30 fps | Envato Elements stock item 24580550. Local preview file only; **not committed, not redistributable** | Aerial video | B | © Alex Kane / Envato. Watermarked preview, licence not held | yes | B, **visual only** | Low, sweeping aerial passes of the Manhattan tower and the main span. **Grades no dimension and cannot** — no camera metadata, no scale control points, and a watermarked 960x540 preview. Registered for what it legitimately settles: arrangement and material. See section 3. |
| SRC-012 | HistoricBridges.org, *Williamsburg Bridge photo gallery* (gallery 2) | https://historicbridges.org/bridges/browser/photosviewer.php?bridgebrowser=newyork/williamsburg/&gallerynum=2&gallerysize=2 | Modern detail photographs | B | © HistoricBridges.org, all rights reserved | yes | B, **visual only** | 684 photographs, systematically shot, at up to 6000x4000. Reviewed in full by contact sheet on 2026-08-09; six examined at full size. **Not redistributed and not committed** — retrieved to a temporary directory outside the repository, read, and deleted. The gallery is almost entirely uncaptioned, so it makes no textual claim at all: it is pure visual detail. Observations in section 3. |
| SRC-013 | Bridge commission dedication tablet, mounted on the structure | The bridge itself. Read from SRC-012 photographs `7699` and `7702` at 6000x4000 | Period primary, on-structure inscription | A | The inscription is a public monument text; the photographs of it are © HistoricBridges.org | yes | A for chronology, **none for geometry** | The bridge's own bronze tablet, naming both bridge commissions and their dates. A genuine period primary that has been read directly rather than through a citation — and it carries **no dimensions whatsoever**. Transcribed in section 3. |

### Sources that may not grade a dimension

`SRC-002` and `SRC-011` are **visual-only**. They show what exists and how it is arranged; they do not
state a number, and nothing in this repository may take a length from them. `AGENT-INSTRUCTIONS.md`
§8 puts it exactly: extracted video frames "help with continuity and detail orientation, but they
should not override measured geometry unless scale control points exist." There are none here.

Test **STT-017** enforces this: a `CTL-` row citing a visual-only source is a build failure. Material
rules (`MAT-`) may cite them, because "that pier is masonry" is a claim a photograph can actually
support.

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

### SRC-007 — Haight and Patel, AISC 2005, the dimensional paragraph

> The main suspended span is 1,600 feet long, **with side spans each 596.5 feet**. The main span is
> suspended [...] while **the side spans are each supported by three intermediate towers** as well as
> at the anchorages and main towers. **The anchorages are each 114.25 feet long. The Manhattan
> Approach viaduct is the longer of the two approach viaducts at 2,090.25 feet; the Brooklyn Approach
> viaduct is approximately 1,557 feet long.** Four cables suspend the stiffening truss approximately
> 135 feet above mean high water level in the East River. **The stiffening truss is 67 feet wide and
> approximately 40 feet deep and is pinned at each main tower.**

One paragraph, written by the bridge's owner-engineer and its reconstruction designer, that closes
three open questions and settles two conflicts. It retires the largest placeholder in the model.

**It also refuses to close the total length.** Adding the figures it states:

```
main span                    1600.00
+ two side spans (2 x 596.5) 2793.00   suspended structure
+ two anchorages (2 x 114.25) 3021.50
+ Manhattan approach 2090.25
+ Brooklyn approach  1557.00
                             6668.75 ft
```

That is **639.25 ft short of the 7,308 ft** published by NYCDOT itself (CTL-002, grade `A`). The gap
is too large to be rounding and too small to be a missing approach. Something is measured between
different points in the two statements — which is exactly what CNF-014 suspects and what OQ-006
asks. The model keeps both numbers and records the discrepancy rather than adjusting either.

**A caution on the extraction.** This text was pulled from a PDF, and the extraction visibly
interleaves column fragments — "The main span is suspended, REVIOUS WORK e Williamsburg Bridge began
in the early 1990s, and the major construction tion contract involved..." is two columns run
together. The quoted sentences above are each internally coherent and were checked to read cleanly,
but `HOW-TO-DESIGN.md` §10 warns specifically that PDF extraction does not preserve spatial order.
The figures are used; the *figure captions* and section arrangement in that paper are not, and the
labelled transverse section it contains has not been read.

### SRC-010 — historic-structures.com

The specification paragraph:

> When it opened, the Williamsburg Bridge was the longest suspension bridge in the world, with a
> span of 1,600 ft and a total length between approaches of 7,308 ft. Its two all-steel towers reach
> a height of 310 ft, supporting four steel 18-in.-diameter main cables. **Steel arches, not the
> cables, support the side spans. Massive 40-ft-deep steel stiffening trusses carry the decks.**

And, on cost and the side spans:

> Its final cost came to $24.2 million, including land and approaches. Despite the increased costs,
> economics guided much of the design. **Since the main cables don't support the relatively short
> (300 ft) side spans, they were made to be shorter and lighter.** The towers, made from less
> expensive and lighter steel rather than masonry, required smaller foundations.

On the towers and cables:

> Each of the bridge's two steel towers sit on two separate masonry piers. [...] Saddles atop the
> towers support each of the four 4,344-ton main cables. Each cable consists of 37 strands of 208
> wires, and nearly 17,500 miles of wire in the cables suspend the bridge 135 ft above the river.

What this source does for the model: it independently corroborates the 1,600 ft span, the 7,308 ft
length, the 310 ft tower height, the 18 in cable diameter, the 135 ft clearance, the 37×208 strand
construction, and — the only one that changes a grade — the **40 ft stiffening truss depth**, which
until now rested on SRC-004 alone. It also introduces five conflicts, CNF-009 to CNF-013.

### SRC-011 — aerial video, what was actually observed

Twelve frames were extracted at 1 fps and read. **No measurement was taken from them and none can
be.** The observations are arrangement and material only:

- **Each tower stands on two separate masonry piers**, one under each leg, rising independently out
  of the water. This is visible unambiguously and is stated in words by SRC-010. It is the reason
  the tower parts' transverse arrangement is no longer purely an inference from a caisson figure —
  though the *spacing* remains one. See the note on CTL-021.
- The piers are **dressed stone masonry**; the towers, the stiffening trusses and the deck framing
  are **steel latticework**. This is what raises MAT-003 and MAT-010 to grade `B`.
- The stiffening trusses are **painted a dark red**, in contrast to the grey towers and deck framing.
  Recorded as an observation about livery, not material: the closed material vocabulary describes
  what a thing is made of, not what colour it has been painted.
- The deck reads, outboard to inboard, as an **upper walkway above an outer roadway**, then the deep
  red truss enclosing the centre. Vehicles are visible on the outer roadway, below the walkway.
- **The Manhattan tower stands at or very near the shoreline**, with parkland and streets beginning
  immediately inland of its piers. Qualitative, but it bears directly on CNF-009: if the towers are
  effectively at the shore, then a tower-to-anchorage distance ought to be close to the anchorage's
  570–590 ft inland set-back, not 300 ft.

That last point is an observation, not a measurement, and it is used only to keep a conflict open —
never to settle one. Eyeballing a frame is exactly the move `HOW-TO-DESIGN.md` §11 warns about.

### SRC-012 — HistoricBridges.org gallery, what 684 photographs actually settled

All 684 were reviewed by contact sheet; six were pulled at 6000x4000. The set is systematic and
close-range — the underside of the side spans, the intermediate bents, truss connections, rivet
patterns, railings, the transit bay with trains in it, ornamental ironwork. It is the best available
material on **how this bridge is put together**. It is also uncaptioned, so it asserts nothing in
words, and it carries no scale. Under STT-017 it grades no dimension.

What it settles, and what it does not:

- **The side spans are carried on multi-column steel lattice bents** standing on masonry footings,
  with a deep riveted truss at deck level. Photographs `7051`, `7057` (from beneath, showing several
  bents in a row) and `7066` (the deck truss in elevation) are unambiguous on this.
- **This narrows CNF-013 but does not close it.** The deck-level structure is a truss, not an arch;
  SRC-004 is right about that and SRC-010's "steel arches" is at best loose. There *is* arched portal
  bracing within the bents, which may be what SRC-010's author had in mind. Recorded as a narrowing,
  not a resolution.
- **It does not answer OQ-003.** No single frame covers a side span end to end, so the number of
  intermediate towers per side span still cannot be counted. Counting bents across several
  photographs taken from different positions would be inventing a result.
- **Material evidence is strong**: riveted steel latticework throughout, masonry footings under the
  bents, and the approach viaduct visibly of the same construction. This is what raises MAT-013.
- The stiffening truss is confirmed as painted dark red and the tower steel grey, matching SRC-011.

### SRC-013 — the bridge's own dedication tablet, transcribed

Read from SRC-012 photographs `7699` and `7702`, which between them cover the whole tablet. Square
brackets mark text obscured by graffiti or falling outside the frame.

> **FIRST COMMISSION**
> APPOINTED JUNE 1895 ·
> ANDREW D· BAIRD · PRES · SALEM H· WALES · VICE-PRES · LEWIS [NIXON]
> FRANCIS B· THURBER · SEC'Y · RICHARD DEEVES · TREAS · SMITH E· [LANE]
> JAMES A· SPERRY · HENRY BATTERMAN
> W· L· STRONG · EX-OFFICIO
> C· A· SCHIEREN · EX-OFFICIO · F· W· WURSTER · EX-OFFICIO
>
> **SECOND COMMISSION**
> APPOINTED JAN· 19· 1898 ·
> LEWIS NIXON · PRES · JAMES W· BOYLE · VICE-PRES ·
> SMITH E· LANE · SEC'Y 1899 · JAMES D· BELL · SEC'Y 1901
> JULIAN D· FAIRCHILD · TREASURER ·
> JOHN W· WEBER · THOS· S· MOORE
> R· A· VAN WYCK · EX-OFFICIO
>
> SECOND COMMISSION SUCCEEDED BY
> DEPARTMENT OF BRIDGES OF NEW YORK JANUARY 1· 1902 ·

**This is a period primary source read directly, and it grades nothing in this model.** It fixes
three dates — the first commission June 1895, the second 19 January 1898, and the transfer to the
Department of Bridges on 1 January 1902 — and names the men responsible. It states no dimension, no
material and no arrangement. It is registered because it is the only primary this repository has
read *on the structure itself*, and because it is a clean illustration of the rule: a Tier A source
is not a dimension. Worth knowing for a future milestone: bridges of this period often carry a
second tablet giving lengths and costs, and this one is mounted on the walkway trusswork where such
a companion would be.

---

## 4. Verification queue

In priority order. Nothing here may grade a control until it moves to section 1 with `Verified: yes`.

| # | Source | Action | Why it matters |
|---|---|---|---|
| 1 | SRC-009 | **File the NYCDOT FOIL request for record, shop and rehabilitation drawings.** | Longest lead time, largest payoff. It is the only route to `A`-grade transverse geometry and would retire OQ-001, OQ-003, OQ-005 and OQ-007 at once. This is a request, not a research problem. |
| 2 | SRC-007 | Obtain the AISC 2005 paper through a library or AISC membership. | `HOW-TO-DESIGN.md` reports it gives the stiffening truss as *"67 feet wide and approximately 40 feet deep and is pinned at each main tower"* and a labelled transverse section. SRC-004 independently states 67 ft / 40 ft, so reading SRC-007 would raise CTL-008 and CTL-009 from `C` toward `A`, and the "pinned at each main tower" clause bears directly on OQ-011. |
| 3 | — | Settle **CNF-009**: does SRC-010's "300 ft side spans" describe the whole tower-to-anchorage span, or one panel between a main tower and an intermediate tower? | OQ-001 and OQ-003 together. This is now a sharper question than "find the side-span length", and answering it retires the largest placeholder in the model. |
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
| CNF-009 | **Side-span length, tower to anchorage** | **300 ft** — SRC-010 | **Not stated.** SRC-004 instead places the anchorages "570 ft or 590 ft inland of the shore" | **Open — and the 300 ft figure is deliberately NOT adopted** | This is the first source read to give a side-span length, and it is the answer to OQ-001 if it is right. It is not adopted, for three reasons. **First, arithmetic:** SRC-011 shows the towers standing at or very near the shoreline, so a tower-to-anchorage distance should be close to the anchorage's own 570–590 ft inland set-back. 300 ft is roughly half that, and the two cannot both describe the same distance. **Second, wording:** SRC-010 says "the relatively short (300 ft) side spans" in a sentence about cable economics, and SRC-004 states that *intermediate towers* stand within each side span. 300 ft may well be the length of one arch or truss panel between a main tower and an intermediate tower, not the whole tower-to-anchorage run — which would make both sources right and neither a side-span length. **Third, cost of being wrong:** adopting it moves both anchorages, both side spans and both approach lengths on the authority of one uncited compilation. CTL-101 therefore stays a grade `D` placeholder and OQ-001 stays open, now narrowed to a specific question: does 300 ft describe the whole side span or one panel of it? |
| CNF-010 | Total construction cost | **$8 million** — SRC-001 | **$24.2 million "including land and approaches"** — SRC-010 | **Open** | Not used by any control. The qualifier probably explains most of the gap, and SRC-010 separately reports a $7 million initial estimate. Registered because a cost figure is the kind of number that gets quoted without its qualifier. |
| CNF-011 | Main cable weight | **4,344 tons for the cables** — SRC-003 | **"each of the four 4,344-ton main cables"** — SRC-010 | **Open** | A factor of four apart, from the same number. SRC-003 lists it under "Weight of cables" for the bridge; SRC-010 attaches it to each cable. Not used by any control, but it is a clean example of why a figure is registered with its wording rather than as a bare quantity. |
| CNF-012 | Total length of wire | **17,500 miles** — SRC-003, SRC-010 | **"Almost 19,000 mi of steel wire strands were manufactured"** — SRC-004 | **Settled by reading** | Not a contradiction: SRC-004 says *manufactured*, the others say installed in the cables. Registered so the difference is not later "corrected". |
| CNF-013 | What supports the side spans | **"Steel arches, not the cables"** — SRC-010 | **Trusswork, carried on intermediate towers** — SRC-004 | **Open, but narrowed toward SRC-004** | SRC-012 photographs `7051`, `7057` and `7066` show multi-column steel lattice bents on masonry footings carrying a deep riveted truss at deck level. The deck-level structure is a truss, not an arch. There is arched portal bracing *within* the bents, which may be what SRC-010's author meant, so the conflict is narrowed rather than closed. This matters because it governs what the side-span geometry should be modelled as, and it is bound up with OQ-003. Nothing in the model depends on the answer yet: no side-span structure is modelled beyond the deck chain. |
| CNF-014 | What the 7,308 ft is measured between | **"including approaches"** — SRC-004; "Total length" — SRC-003 | **"total length between approaches"** — SRC-010 | **Open** | Two words, and they invert the meaning of a grade `A` control. CTL-002 keeps the "including approaches" reading, which two sources support against one, but this is direct evidence on OQ-006 and may be part of why the approach grade fails to reach street level. |

---

## 7. Licences and provenance of retrieved material

| Path | Source | Licence | Redistribution |
|---|---|---|---|
| `sources/drawings/ny1263data.pdf` | SRC-001 | Public domain (US Government work) | Yes |
| `sources/drawings/ny1263cap.pdf` | SRC-002 | Public domain (US Government work) | Yes |
| `viewer/public/photos/*.jpg` | SRC-002 | Public domain (US Government work) | Yes. The nine HAER photographs, retrieved from the Library of Congress originals at 1024 px and served by the viewer as reference imagery. They were **surfaced by** the historic-structures.com page registered as SRC-010, which the viewer credits and links to, but they were **not copied from it** — taking them from the archival original gives better resolution and unambiguous rights. |
| *(not committed)* | SRC-003 | © City of New York | Retrieved 2026-08-09 and read. The passages relied on are quoted verbatim in section 3; the page itself is not redistributed. |
| *(not committed)* | SRC-010 | © historic-structures.com | Read 2026-08-09. Passages quoted in section 3 for commentary; the page is not redistributed. |
| *(not committed)* | SRC-011 | © Alex Kane / Envato | **A watermarked stock preview for which no licence is held.** Neither the video nor any frame extracted from it is committed to this repository, and `.gitignore` excludes `sources/videos/`. Only the written observations in section 3 are retained. If this material is ever to be used beyond arrangement and material observations, licence it first. |
| *(not committed)* | SRC-012 | © HistoricBridges.org, all rights reserved | 684 photographs retrieved on 2026-08-09 to a temporary directory **outside this repository**, reviewed by contact sheet, six examined at full size, and then deleted. Nothing from this source is committed, served or republished. Only the written observations in section 3 are retained. `.gitignore` excludes `sources/photos/` and `sources/videos/` so a copy cannot be added by accident. |
| *(not committed)* | SRC-013 | Inscription text transcribed here; the photographs read from are © HistoricBridges.org | The transcription in section 3 is this repository's own work from those photographs. No photograph of the tablet is committed. |
| *(not committed)* | SRC-006 | © City of New York | 28 MB. Retrieved, searched, and found to carry no span geometry. Re-fetch from the URL rather than committing it. |

No mesh, photogrammetry, video or marketplace asset has been ingested. `sources/existing-meshes/`,
`sources/photos/`, `sources/videos/` and `photogrammetry/` are empty by design at Milestone 1:
nothing may be imported before there is a control skeleton to align it against.
