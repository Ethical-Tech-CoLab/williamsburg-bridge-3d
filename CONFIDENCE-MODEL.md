# Confidence Model — Williamsburg Bridge

## 0. The one rule

> **No dimension may exist in the model without tracing to a registered source with an explicit
> confidence grade. Anything unsourced is graded `D`, labelled a placeholder, and linked to a named
> open question.**

And its corollary, which does most of the work:

> **A model that admits it does not know something is more valuable than one that guesses well.**

A plausible guess is indistinguishable from a fact once it is inside a GLB. Everything below is
machinery for keeping the rule true when it becomes inconvenient.

---

## 1. Three independent axes

There is no single "confidence" number in this repository. There are three different questions, and
collapsing them hides the one that matters most.

| Axis | Question | Where it lives |
|---|---|---|
| **Source confidence** `A` `B` `C` `D` | How good is the evidence? | `SOURCE-REGISTER.md`, and the `Confidence` column of every control row |
| **Geometry provenance** `MEASURED` `DOCUMENTED` `INFERRED` `ASSUMED` | How is the *shape and position* of this element known? | Derived per part by `scripts/build_control_skeleton.py`; never hand-declared |
| **Material** and its own grade | What is it made of, and how do we know? | The `MAT-` table in `GEOMETRY-CONTROL.md` §7 |

**Why they must stay separate.** A source can be fully read, quoted and rated Tier A and *still*
support only `ASSUMED` geometry, because a sentence establishing that an element exists says nothing
about where it is. The `manhattan-bridge-noise-dumbo` project's first implementation merged these two
axes and consequently labelled eight components "verified" on the strength of a source that located
none of them.

This bridge produces the same trap immediately. SRC-001 is a Tier A national record and its entire
dimensional content is eight clauses. It establishes that there are four main cables — and locates
not one of them.

**A material grade never drags a geometry grade down.** The Manhattan Bridge's Brooklyn anchorage is
geometry grade `B` and material grade `D`; every photograph shows stone, but a photograph is not in
the register, so it cannot grade a control. Here the anchorage material happens to be sourced
(SRC-004, "massive masonry anchorages") and so is graded `C` — but the two grades remain independent
fields, and a future correction to one must not silently move the other.

---

## 2. Source confidence grades

| Grade | Meaning | May cite sources? |
|---|---|---|
| `A` | Derived from an official dimension published by the owner, or from an archival engineering record. | **Required** |
| `B` | Derived from multiple consistent photographs or secondary records together with known control geometry. | **Required** |
| `C` | Derived from a tertiary compilation, an existing mesh, or photogrammetry aligned to controls. | **Required** |
| `D` | Inferred, decorative, or a placeholder standing in for a number nobody has yet read. | **Forbidden** |

Both directions are enforced by `scripts/control_model.py` and re-checked by tests STT-002 and
STT-003:

- **Only `D` may cite no source.** An `A`/`B`/`C` row with an empty source cell is a parse error.
- **`D` may not cite sources.** A placeholder must not appear to rest on evidence. If a placeholder
  acquires a source, it stops being a placeholder and moves table.

### What grade `A` does and does not mean here

`A` means the number was published by the structure's owner or written into the national record. It
does not mean the number is right, and it does not mean it is unambiguous. CTL-006 (tower height,
310 ft) is grade `A` from SRC-003 and its **datum is not stated by the source** — see CNF-002 and
OQ-004. Grade `A` with an open question against it is a normal and honest state.

### Inheritance: weakest link

A part's source confidence is the **lowest grade among every control it consumes**, with `D`
absorbing everything.

```
grade(part) = min over controls c in refs(part) of grade(c)      where A > B > C > D
```

A part that consumes no control at all is `D` by definition — it rests on nothing.

This is deliberately pessimistic. A tower whose height is grade `A` and whose plan rectangle is
grade `C` is a grade `C` tower, because you cannot see the `A` in it without also seeing the `C`.

---

## 3. Geometry provenance

Adopted from `VISUAL-MODEL-FRAMEWORK.md` §5.4 (Ethical Tech CoLab). **Derived in the build, never
hand-declared**, so it cannot drift from what the part actually consumes.

| State | Meaning |
|---|---|
| `MEASURED` | Derived from an instrument reading of the actual structure. Carries a Level of Accuracy. |
| `DOCUMENTED` | *This element's own* position or dimension is stated numerically in a source that was read. |
| `INFERRED` | The element's **existence** is documented, but its position or dimension is reasoned. |
| `ASSUMED` | Placed by engineering judgement, with **no source statement locating it at all**. |

**The `INFERRED`/`ASSUMED` boundary is drawn on whether anything sourced speaks to the element**, not
on how confident anyone feels about its shape. The first derivation attempted on the Manhattan Bridge
keyed off "depends on a placeholder control", which produced `INFERRED = 0` — a binary that destroyed
the distinction the framework exists to carry. The rule implemented in
`scripts/build_control_skeleton.py`:

```python
if "photogrammetry" in source_basis or "survey" in source_basis:   MEASURED
elif "control_dimension" not in source_basis or not sourced_refs:   ASSUMED
elif placeholder_refs or "inferred" in source_basis:                INFERRED
else:                                                               DOCUMENTED
```

`MEASURED` is expected to be `0` for a long time. It is **computed** rather than hardcoded, so that
the day SRC-008 or a survey lands, the number changes honestly. Test GRT-013 reports it rather than
asserting it.

---

## 4. Rendering rules — how to look good without lying

The most useful finding carried over from the Manhattan Bridge work is that the visual quality of a
provenance-tagged bridge schematic comes almost entirely from **rendering discipline**, not from
having measured drawings. No element of this model reaches `MEASURED` or `DOCUMENTED` on its
transverse position, and it can still read as a convincing bridge.

| State | Render |
|---|---|
| `MEASURED` / `DOCUMENTED` | Solid fill, solid outline, full opacity |
| `INFERRED` | Reduced opacity, **dashed** outline |
| `ASSUMED` | Low opacity, **dotted** outline, and excluded from every dimension callout |

Four interaction requirements go with them:

- **The filter must hide, not fade.** A faded outline is still a shape a reader will trace. Switching
  `INFERRED` and `ASSUMED` off must genuinely remove them, even if the honest result is a nearly
  empty frame.
- **Locus on selection.** Selecting an element shows the controls its geometry rests on and the
  grade of each, or states that there are none.
- **A standing tally, permanently on screen** — not below the fold of a scrolling list.
- **Materials drive appearance**, so masonry reads as masonry. They are assigned in
  `GEOMETRY-CONTROL.md` §7, not in the renderer, and the table has **no default rule**: an unmatched
  part is a build failure, not a silent grey.

> **No dimension may be annotated on any element whose provenance is `ASSUMED`.** If we do not know
> where it is, we do not get to say how big it is.

*three.js note:* dashed lines need `computeLineDistances()` after the geometry is built, or
`LineDashedMaterial` silently renders solid.

---

## 5. Required metadata on every part

`AGENT-INSTRUCTIONS.md` §11 requires these fields; STT-006, STT-010 and STT-011 enforce them.

```json
{
  "part_id": "tower_manhattan_leg_north",
  "system": "towers",
  "source_basis": ["control_dimension"],
  "control_refs": ["CTL-001", "CTL-019", "CTL-020"],
  "source_ids": ["SRC-003", "SRC-004"],
  "open_questions": ["OQ-004"],
  "confidence": "C",
  "provenance": "INFERRED",
  "material": "steel_structural",
  "material_confidence": "A",
  "prototype_units": "meters",
  "ho_scale_units": "millimeters",
  "last_modified_by_agent": "build_control_skeleton.py",
  "review_status": "machine_generated",
  "notes": ""
}
```

`review_status` starts at `machine_generated` for everything the build emits. It may only become
`human_reviewed` through an actual review, and nothing in the pipeline sets it.

---

## 6. Promotion and demotion

**To promote a control out of `D`:** read a source, register it in `SOURCE-REGISTER.md` §1 with
`Verified: yes`, quote the passage in §3, move the row from the placeholder table to the control
table with the source cited, and close or narrow the linked open question. The build then re-derives
every dependent part's grade and provenance automatically.

**To demote:** if a source is found not to say what it was thought to say, the control returns to the
placeholder table, loses its source citation, and a new open question is opened. This is expected.
`HOW-TO-DESIGN.md` §11 records a Manhattan Bridge tower description that was truncated mid-passage;
the full text described a materially different tower.

**Ratchets.** `tests/geometry_regression_tests.json` asserts that the placeholder count has not
regressed. Raising the expectation requires editing the number *and writing the argument for it in
the `rationale` field*.

---

## 7. Testing the guards

**Give every guard teeth, and prove it.** After writing a test that asserts a defect is fixed, run
its measure against the pre-fix arrangement and confirm it fails there. A gap test that reports `0`
both before and after a fix is worse than no test at all.

Two guards in this repository have been exercised this way:

- **GRT-010, deck longitudinal continuity.** Verified to fail when the deck chain is truncated at
  the anchorage faces — which is exactly the bug that shipped twice on the Manhattan Bridge, leaving
  the roadway and tracks terminating in mid-air. SRC-004 states the trusswork "runs continuously
  from one anchorage to the other", so this model's deck must be continuous through the anchorages
  and out along both approaches.
- **STT-012, control document hash.** Verified to fail when `GEOMETRY-CONTROL.md` is edited without
  rebuilding. Every parts manifest records the SHA-256 of the control document it was built from.

And one parsing lesson, paid for during this repository's own source research: a regular expression
written to strip `<ref>...</ref>` from wiki markup matched a self-closing `<ref name="x"/>` as an
opening tag and silently swallowed the sentences after it, deleting real content from a passage that
was about to be quoted. `HOW-TO-DESIGN.md` §11 records the same class of failure on the Manhattan
Bridge, where a "verified" column parser choked on markdown bold. **Test your tests, and read the
output of a scraper before trusting it.**
