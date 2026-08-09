"""Build the Williamsburg Bridge control skeleton from GEOMETRY-CONTROL.md.

This script contains **no dimensions**. Every number it uses is read from GEOMETRY-CONTROL.md
through ``control_model.py``. If a literal length ever appears below, it is a bug.

Outputs:

* ``mesh/glb/control_skeleton.glb``            prototype scale, meters
* ``mesh/glb/control_skeleton_ho.glb``         1:87.1, for physical-scale study
* ``viewer/public/control_skeleton.glb``       the copy the browser viewer loads
* ``viewer/metadata/parts.json``               every part with its provenance
* ``viewer/metadata/build_report.json``        stations, elevations, census, control hash
* ``viewer/metadata/scale_ho.json``            HO conversion of every linear control

Run::

    python scripts/build_control_skeleton.py
"""

from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from control_model import ControlModel, load_control_model  # noqa: E402
from export_gltf import (  # noqa: E402
    GltfBuilder,
    box_mesh_data,
    prism_mesh_data,
    tube_mesh_data,
)
from normalize_units import HO_SCALE_DENOMINATOR, ho_report, is_linear  # noqa: E402

REPO = SCRIPT_DIR.parent
AGENT = "build_control_skeleton.py"

# Closed taxonomy from AGENT-INSTRUCTIONS.md section 6, plus "reference" for drawing furniture.
KNOWN_SYSTEMS = (
    "reference",
    "anchorages",
    "towers",
    "cables",
    "suspenders",
    "deck_system",
    "approaches",
    "details",
)

GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}

# Appearance is driven by the material assigned in GEOMETRY-CONTROL.md section 7, never by the
# renderer's own judgement. There is no default: an unmatched part fails the build in
# control_model.material_for().
MATERIAL_COLOR = {
    "masonry": (0.62, 0.57, 0.50),
    "concrete": (0.70, 0.70, 0.68),
    "steel_structural": (0.42, 0.47, 0.53),
    "steel_wire": (0.80, 0.78, 0.72),
    "roadway_surface": (0.28, 0.28, 0.30),
    "reference": (0.35, 0.65, 0.85),
}


# --------------------------------------------------------------------------- parts


@dataclass
class Part:
    """One addressable component, with everything CONFIDENCE-MODEL.md section 5 requires."""

    part_id: str
    system: str
    control_refs: tuple[str, ...]
    notes: str = ""
    source_basis: tuple[str, ...] = ("control_dimension",)
    open_questions: tuple[str, ...] = ()
    primitives: list[dict[str, Any]] = field(default_factory=list)
    confidence: str = "D"
    provenance: str = "ASSUMED"
    source_ids: tuple[str, ...] = ()
    material: str = ""
    material_confidence: str = "D"
    material_id: str = ""

    def metadata(self) -> dict[str, Any]:
        return {
            "part_id": self.part_id,
            "system": self.system,
            "source_basis": list(self.source_basis),
            "control_refs": list(self.control_refs),
            "source_ids": list(self.source_ids),
            "open_questions": list(self.open_questions),
            "confidence": self.confidence,
            "provenance": self.provenance,
            "material": self.material,
            "material_id": self.material_id,
            "material_confidence": self.material_confidence,
            "prototype_units": "meters",
            "ho_scale_units": "millimeters",
            "last_modified_by_agent": AGENT,
            "review_status": "machine_generated",
            "notes": self.notes,
        }


class SkeletonBuilder:
    def __init__(self, model: ControlModel) -> None:
        self.m = model
        self.parts: list[Part] = []

    # ----------------------------------------------------------------- grading

    def _grade(self, refs: Sequence[str]) -> tuple[str, tuple[str, ...], bool, bool]:
        """Weakest-link grade over the controls a part consumes.

        Returns (grade, source_ids, has_sourced_ref, has_placeholder_ref). A part consuming no
        control at all is grade D and has no sourced reference, which makes it ASSUMED.
        """
        if not refs:
            return "D", (), False, False
        worst = "A"
        sources: list[str] = []
        has_sourced = False
        has_placeholder = False
        for ref in refs:
            control = self.m.by_id.get(ref)
            if control is None:
                raise KeyError(f"part references unknown control {ref!r}")
            if GRADE_ORDER[control.confidence] > GRADE_ORDER[worst]:
                worst = control.confidence
            if control.is_placeholder:
                has_placeholder = True
            else:
                has_sourced = True
                sources.extend(control.source_ids)
        return worst, tuple(dict.fromkeys(sources)), has_sourced, has_placeholder

    @staticmethod
    def _provenance(
        source_basis: Sequence[str], has_sourced: bool, has_placeholder: bool
    ) -> str:
        """GEOMETRY-CONTROL.md section 8. Derived, never declared.

        The INFERRED/ASSUMED boundary is drawn on whether anything sourced speaks to the element,
        not on how confident anyone feels about its shape.
        """
        if "photogrammetry" in source_basis or "survey" in source_basis:
            return "MEASURED"
        if "control_dimension" not in source_basis or not has_sourced:
            return "ASSUMED"
        if has_placeholder or "inferred" in source_basis:
            return "INFERRED"
        return "DOCUMENTED"

    def add(self, part: Part) -> Part:
        grade, sources, has_sourced, has_placeholder = self._grade(part.control_refs)
        part.confidence = grade
        part.source_ids = sources
        part.provenance = self._provenance(part.source_basis, has_sourced, has_placeholder)
        rule = self.m.material_for(part.part_id)
        part.material = rule.material
        part.material_id = rule.material_id
        part.material_confidence = rule.confidence
        self.parts.append(part)
        return part


# --------------------------------------------------------------------- geometry helpers


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _sample(points: Sequence[tuple[float, float]], x: float) -> float:
    """Piecewise-linear lookup over (x, value) knots sorted by x."""
    if x <= points[0][0]:
        return points[0][1]
    if x >= points[-1][0]:
        return points[-1][1]
    for (x0, v0), (x1, v1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            span = x1 - x0
            return v0 if span == 0 else _lerp(v0, v1, (x - x0) / span)
    return points[-1][1]


def _frange(start: float, stop: float, step: float) -> Iterable[float]:
    n = 1
    x = start + step
    while x < stop - 1e-9:
        yield x
        n += 1
        x = start + step * n


def _primitive_vertices(prim: tuple) -> Iterable[tuple[float, float, float]]:
    kind = prim[0]
    if kind == "line":
        for seg in prim[1]:
            yield from seg
    elif kind in ("box", "box_span"):
        yield prim[1]
        yield prim[2]
    elif kind == "prism":
        yield from prim[1]
        yield from prim[2]
    elif kind == "tube":
        yield from prim[1]
    else:  # pragma: no cover - guarded by the closed set in write_glb
        raise ValueError(f"unknown primitive kind {kind!r}")


def merge_x_intervals(
    parts: Sequence["Part"], systems: Sequence[str], tolerance: float
) -> list[list[float]]:
    """Longitudinal extent actually occupied by the emitted geometry of the given systems.

    Measured from the vertices the build emits, not from a declared constant, so GRT-010 tests the
    model rather than a promise about it. Intervals closer together than ``tolerance`` meters are
    treated as joined; anything wider is a real gap in the deck chain.
    """
    wanted = set(systems)
    spans: list[tuple[float, float]] = []
    for part in parts:
        if part.system not in wanted:
            continue
        xs = [v[0] for prim in part.primitives for v in _primitive_vertices(prim)]
        if xs:
            spans.append((min(xs), max(xs)))
    if not spans:
        return []
    spans.sort()
    merged = [list(spans[0])]
    for lo, hi in spans[1:]:
        if lo <= merged[-1][1] + tolerance:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return [[round(a, 4), round(b, 4)] for a, b in merged]


# ------------------------------------------------------------------------- the build


def build(model: ControlModel) -> tuple[SkeletonBuilder, dict[str, Any]]:
    b = SkeletonBuilder(model)
    m = model

    m.require(
        "main_span_tower_to_tower",
        "total_length_including_approaches",
        "navigation_clearance_at_center",
        "tower_height",
        "deck_width",
        "stiffening_truss_spacing",
        "stiffening_truss_depth",
        "side_span_tower_to_anchorage",
    )

    # --- stations (DRV-001..DRV-006) --------------------------------------------------
    half_main = m.m("main_span_tower_to_tower") / 2.0
    side = m.m("side_span_tower_to_anchorage")
    half_total = m.m("total_length_including_approaches") / 2.0
    x_tower = half_main
    x_anchor = half_main + side
    x_end = half_total

    stations = {
        "manhattan_approach_end": -x_end,
        "manhattan_anchorage": -x_anchor,
        "manhattan_tower": -x_tower,
        "main_span_midpoint": 0.0,
        "brooklyn_tower": x_tower,
        "brooklyn_anchorage": x_anchor,
        "brooklyn_approach_end": x_end,
    }
    station_grade = {
        "manhattan_approach_end": ("DRV-006", ["CTL-002"]),
        "manhattan_anchorage": ("DRV-004", ["CTL-001", "CTL-101"]),
        "manhattan_tower": ("DRV-002", ["CTL-001"]),
        "main_span_midpoint": ("DRV-001", ["CTL-001"]),
        "brooklyn_tower": ("DRV-003", ["CTL-001"]),
        "brooklyn_anchorage": ("DRV-005", ["CTL-001", "CTL-101"]),
        "brooklyn_approach_end": ("DRV-006", ["CTL-002"]),
    }

    # --- elevations (DRV-007..DRV-009, DRV-014, DRV-015) ------------------------------
    z_deck_under_mid = m.m("navigation_clearance_at_center")
    z_deck_top_mid = z_deck_under_mid + m.m("stiffening_truss_depth")
    z_deck_anchor = m.m("deck_elevation_at_anchorage")
    z_tower_top = m.m("tower_height")
    z_pier_top = m.m("tower_pier_top_elevation")
    z_cable_mid = m.m("main_cable_elevation_at_midspan")
    z_anchor_top = m.m("anchorage_top_elevation")
    approach_run = x_end - x_anchor
    z_approach_end = z_deck_anchor - m.raw("approach_grade") * approach_run

    deck_profile = [
        (-x_end, z_approach_end),
        (-x_anchor, z_deck_anchor),
        (0.0, z_deck_top_mid),
        (x_anchor, z_deck_anchor),
        (x_end, z_approach_end),
    ]
    truss_depth = m.m("stiffening_truss_depth")

    def deck_top(x: float) -> float:
        return _sample(deck_profile, x)

    def deck_under(x: float) -> float:
        return deck_top(x) - truss_depth

    # Main cable profile: over the saddles at the tower tops, down to a placeholder mid-span
    # elevation, and down to the anchorage tops. Z here is ASSUMED; the cables' existence is A.
    cable_profile = [
        (-x_anchor, z_anchor_top),
        (-x_tower, z_tower_top),
        (0.0, z_cable_mid),
        (x_tower, z_tower_top),
        (x_anchor, z_anchor_top),
    ]

    def cable_z(x: float) -> float:
        return _sample(cable_profile, x)

    # --- transverse layout (DRV-010..DRV-012, DRV-016, DRV-017) -----------------------
    y_truss = m.m("stiffening_truss_spacing") / 2.0
    y_deck = m.m("deck_width") / 2.0
    y_leg = m.m("tower_leg_center_spacing") / 2.0
    y_track = m.m("transit_track_center_spacing") / 2.0

    pair_spacing = [
        (-x_anchor, m.m("cable_pair_spacing_at_anchorage")),
        (-x_tower, m.m("cable_pair_spacing_at_tower_top")),
        (0.0, m.m("cable_pair_spacing_at_midspan")),
        (x_tower, m.m("cable_pair_spacing_at_tower_top")),
        (x_anchor, m.m("cable_pair_spacing_at_anchorage")),
    ]

    def cable_y(x: float, side_sign: float, inner: bool) -> float:
        """Four cables: two pairs centred on the truss lines, cradling together at mid-span."""
        half = _sample(pair_spacing, x) / 2.0
        return side_sign * y_truss + (-half if inner else half) * side_sign

    cable_defs = [
        ("north_main_cable_inner", 1.0, True),
        ("north_main_cable_outer", 1.0, False),
        ("south_main_cable_inner", -1.0, True),
        ("south_main_cable_outer", -1.0, False),
    ]
    assert len(cable_defs) == int(m.raw("main_cable_count"))

    cable_radius = m.m("main_cable_diameter") / 2.0

    # ================================================================= reference frame
    ref_refs = ("CTL-001", "CTL-002")
    b.add(
        Part(
            "reference_axis_longitudinal",
            "reference",
            ref_refs,
            notes="Bridge centreline from approach end to approach end. Z=0 is mean high water.",
            primitives=[("line", [[(-x_end, 0.0, 0.0), (x_end, 0.0, 0.0)]])],
        )
    )
    b.add(
        Part(
            "reference_axis_transverse",
            "reference",
            ("CTL-008",),
            notes="Deck width axis at the origin.",
            primitives=[("line", [[(0.0, -y_deck, 0.0), (0.0, y_deck, 0.0)]])],
        )
    )
    b.add(
        Part(
            "reference_axis_vertical",
            "reference",
            ("CTL-006",),
            notes="Vertical axis at the origin, from mean high water to the tower top elevation.",
            primitives=[("line", [[(0.0, 0.0, 0.0), (0.0, 0.0, z_tower_top)]])],
        )
    )
    for name, x in stations.items():
        rule, refs = station_grade[name]
        b.add(
            Part(
                f"reference_station_{name}",
                "reference",
                tuple(refs),
                notes=f"Station marker, {rule}.",
                open_questions=("OQ-001",) if "CTL-101" in refs else (),
                primitives=[
                    ("line", [[(x, -y_deck, 0.0), (x, y_deck, 0.0)]]),
                    ("line", [[(x, 0.0, 0.0), (x, 0.0, z_tower_top)]]),
                ],
            )
        )
    b.add(
        Part(
            "reference_water_plane",
            "reference",
            ("CTL-002", "CTL-008"),
            notes="Mean high water plane, the vertical datum of this model.",
            primitives=[
                (
                    "line",
                    [
                        [(-x_end, -y_deck, 0.0), (x_end, -y_deck, 0.0)],
                        [(-x_end, y_deck, 0.0), (x_end, y_deck, 0.0)],
                    ],
                )
            ],
        )
    )

    # ========================================================================= towers
    leg_we = m.m("tower_leg_plan_length_we") / 2.0
    leg_ns = m.m("tower_leg_plan_width_ns") / 2.0
    col = m.m("tower_column_base_side") / 2.0
    narrowing = m.m("tower_top_narrowing") / 2.0
    saddle_h = m.m("tower_saddle_height")

    for end, sign in (("manhattan", -1.0), ("brooklyn", 1.0)):
        xt = sign * x_tower
        # CTL-021 is stated of the caisson pair centres, not of the legs. Taking it as the leg
        # spacing is a reasoned step, so every part that uses it declares an "inferred" basis and
        # is derived as INFERRED rather than DOCUMENTED. Their longitudinal station remains grade A.
        leg_basis = ("control_dimension", "inferred")
        for side_name, ysign in (("north", 1.0), ("south", -1.0)):
            yl = ysign * y_leg
            b.add(
                Part(
                    f"tower_{end}_pier_{side_name}",
                    "towers",
                    ("CTL-001", "CTL-021", "CTL-022", "CTL-023", "CTL-024"),
                    source_basis=leg_basis,
                    open_questions=("OQ-003",),
                    notes=(
                        "Masonry pier rising to 23 ft above mean high water (CTL-024). Its "
                        "transverse position is taken from the caisson pair spacing (CTL-021), "
                        "which is an inference, not a statement about the pier."
                    ),
                    primitives=[
                        (
                            "box",
                            (xt - leg_we, yl - leg_ns, 0.0),
                            (xt + leg_we, yl + leg_ns, z_pier_top),
                        )
                    ],
                )
            )
            # Lower legs: from the pier top to deck level, columns vertical.
            z_deck_at_tower = deck_top(xt)
            b.add(
                Part(
                    f"tower_{end}_leg_{side_name}_lower",
                    "towers",
                    ("CTL-001", "CTL-021", "CTL-022", "CTL-023", "CTL-025"),
                    source_basis=leg_basis,
                    notes=(
                        "Four diagonally braced columns per leg; modelled here as the leg envelope "
                        "from the pier top to deck level. Transverse position inferred from "
                        "CTL-021."
                    ),
                    primitives=[
                        (
                            "box",
                            (xt - leg_we, yl - leg_ns, z_pier_top),
                            (xt + leg_we, yl + leg_ns, z_deck_at_tower),
                        )
                    ],
                )
            )
            # Upper legs slant inward and narrow toward the top (CTL-027).
            b.add(
                Part(
                    f"tower_{end}_leg_{side_name}_upper",
                    "towers",
                    ("CTL-001", "CTL-006", "CTL-021", "CTL-022", "CTL-023", "CTL-027"),
                    source_basis=leg_basis,
                    open_questions=("OQ-004",),
                    notes=(
                        "Upper leg, slanted inward and narrowing by CTL-027 at the top. The tower "
                        "top elevation rests on CTL-006, whose datum is unstated (OQ-004)."
                    ),
                    primitives=[
                        (
                            "prism",
                            [
                                (xt - leg_we, yl - leg_ns, z_deck_at_tower),
                                (xt + leg_we, yl - leg_ns, z_deck_at_tower),
                                (xt + leg_we, yl + leg_ns, z_deck_at_tower),
                                (xt - leg_we, yl + leg_ns, z_deck_at_tower),
                            ],
                            [
                                (xt - leg_we + narrowing, yl - leg_ns + narrowing, z_tower_top),
                                (xt + leg_we - narrowing, yl - leg_ns + narrowing, z_tower_top),
                                (xt + leg_we - narrowing, yl + leg_ns - narrowing, z_tower_top),
                                (xt - leg_we + narrowing, yl + leg_ns - narrowing, z_tower_top),
                            ],
                        )
                    ],
                )
            )
        # Portal bracing between the two legs, above the deck.
        b.add(
            Part(
                f"tower_{end}_portal_truss",
                "towers",
                ("CTL-001", "CTL-006", "CTL-021", "CTL-026"),
                source_basis=leg_basis,
                open_questions=("OQ-004",),
                notes="Pair of trusses stiffening the upper legs, CTL-026 high.",
                primitives=[
                    (
                        "box",
                        (xt - col, -y_leg, z_tower_top - m.m("tower_upper_truss_height")),
                        (xt + col, y_leg, z_tower_top),
                    )
                ],
            )
        )
        # One saddle per cable.
        for cname, ysign, inner in cable_defs:
            yc = cable_y(xt, ysign, inner)
            b.add(
                Part(
                    f"tower_{end}_saddle_{cname}",
                    "towers",
                    ("CTL-001", "CTL-006", "CTL-019", "CTL-106"),
                    open_questions=("OQ-009",),
                    notes="Cable saddle at the tower top. Installed height is a placeholder.",
                    primitives=[
                        (
                            "box",
                            (xt - saddle_h / 2, yc - saddle_h / 2, z_tower_top),
                            (xt + saddle_h / 2, yc + saddle_h / 2, z_tower_top + saddle_h),
                        )
                    ],
                )
            )

    # ===================================================================== anchorages
    for end, sign, lkey, wkey in (
        ("manhattan", -1.0, "manhattan_anchorage_base_length", "manhattan_anchorage_base_width"),
        ("brooklyn", 1.0, "brooklyn_anchorage_base_length", "brooklyn_anchorage_base_width"),
    ):
        xa = sign * x_anchor
        half_l = m.m(lkey) / 2.0
        half_w = m.m(wkey) / 2.0
        refs = ("CTL-001", "CTL-101", "CTL-104") + (
            ("CTL-030", "CTL-031") if end == "manhattan" else ("CTL-032", "CTL-033")
        )
        b.add(
            Part(
                f"{end}_anchorage",
                "anchorages",
                refs,
                open_questions=("OQ-001", "OQ-005", "OQ-008"),
                notes=(
                    "Masonry anchorage. Base rectangle is sourced; which axis runs along the "
                    "bridge is not (OQ-008), and its station rests on the side-span placeholder "
                    "(OQ-001)."
                ),
                primitives=[
                    ("box", (xa - half_l, -half_w, 0.0), (xa + half_l, half_w, z_anchor_top))
                ],
            )
        )

    # ========================================================================= cables
    cable_xs = [-x_anchor + (x_anchor * 2) * i / 240.0 for i in range(241)]
    for cname, ysign, inner in cable_defs:
        points = [(x, cable_y(x, ysign, inner), cable_z(x)) for x in cable_xs]
        b.add(
            Part(
                cname,
                "cables",
                ("CTL-004", "CTL-005", "CTL-018", "CTL-019", "CTL-020", "CTL-102", "CTL-104"),
                open_questions=("OQ-002", "OQ-001"),
                notes=(
                    "One of four main cables. Count and diameter are grade A and the transverse "
                    "cradling is sourced; the vertical profile rests on a placeholder sag "
                    "(CTL-102), so this part is not DOCUMENTED."
                ),
                primitives=[("tube", points, cable_radius)],
            )
        )

    # ===================================================================== suspenders
    susp_spacing = m.m("suspender_spacing_main_span")
    susp_radius = m.m("suspender_rope_diameter") / 2.0
    susp_stations = list(_frange(-x_tower, x_tower, susp_spacing))
    for cname, ysign, inner in cable_defs:
        segments = []
        for x in susp_stations:
            yc = cable_y(x, ysign, inner)
            top = cable_z(x)
            bottom = deck_top(x)
            if top > bottom:
                segments.append([(x, yc, bottom), (x, yc, top)])
        b.add(
            Part(
                f"suspender_set_{cname}",
                "suspenders",
                ("CTL-001", "CTL-013", "CTL-014", "CTL-102"),
                open_questions=("OQ-002",),
                notes=(
                    f"{len(segments)} suspenders at CTL-013 spacing on the main span. Lengths "
                    "follow the placeholder cable profile and are not dimensions."
                ),
                primitives=[("line", segments)],
            )
        )

    # ==================================================================== deck system
    # SRC-004: "The trusswork runs continuously from one anchorage to the other." The deck chain
    # here runs further still, unbroken from approach end to approach end, because the roadway and
    # the tracks do not stop at the anchorage face. GRT-010 asserts there is no gap.
    deck_xs = sorted(
        {-x_end, -x_anchor, -x_tower, 0.0, x_tower, x_anchor, x_end}
        | {-x_anchor + (2 * x_anchor) * i / 80.0 for i in range(81)}
    )

    def ribbon(y0: float, y1: float, ztop_fn, thickness: float) -> list[dict[str, Any]]:
        prims = []
        for xa_, xb_ in zip(deck_xs, deck_xs[1:]):
            za_, zb_ = ztop_fn(xa_), ztop_fn(xb_)
            prims.append(
                (
                    "prism",
                    [
                        (xa_, y0, za_ - thickness),
                        (xb_, y0, zb_ - thickness),
                        (xb_, y1, zb_ - thickness),
                        (xa_, y1, za_ - thickness),
                    ],
                    [(xa_, y0, za_), (xb_, y0, zb_), (xb_, y1, zb_), (xa_, y1, za_)],
                )
            )
        return prims

    deck_refs = (
        "CTL-002",
        "CTL-003",
        "CTL-008",
        "CTL-010",
        "CTL-036",
        "CTL-101",
        "CTL-103",
    )
    deck_thickness = m.m("floor_beam_depth")

    # Five sections of roughly equal width (CTL-016), with only the outermost width sourced
    # (CTL-015). The interior split is an open question (OQ-007).
    outer_w = m.m("outer_roadway_width")
    inner_edge = y_deck - outer_w
    centre_w = (2 * inner_edge) / 3.0
    band_edges = [
        (-y_deck, -inner_edge, "outer_roadway_south"),
        (-inner_edge, -centre_w / 2, "inner_roadway_south"),
        (-centre_w / 2, centre_w / 2, "transit_bay"),
        (centre_w / 2, inner_edge, "inner_roadway_north"),
        (inner_edge, y_deck, "outer_roadway_north"),
    ]
    assert len(band_edges) == int(m.raw("deck_section_count"))

    for y0, y1, name in band_edges:
        b.add(
            Part(
                f"deck_{name}",
                "deck_system",
                deck_refs + ("CTL-015", "CTL-016"),
                open_questions=("OQ-006", "OQ-007", "OQ-001"),
                notes=(
                    "One of the five deck sections. Only the outermost width is sourced; the "
                    "interior division is reasoned (OQ-007). Runs unbroken from approach end to "
                    "approach end."
                ),
                primitives=ribbon(y0, y1, deck_top, deck_thickness),
            )
        )

    # Two transit tracks. Not four: see CNF-003 and NEG-003 in SOURCE-REGISTER.md.
    track_count = int(m.raw("transit_track_count"))
    track_ys = [(-1.0) ** i * y_track for i in range(track_count)]
    for i, yt in enumerate(sorted(track_ys), start=1):
        b.add(
            Part(
                f"transit_track_{i}",
                "deck_system",
                ("CTL-007", "CTL-017") + deck_refs,
                open_questions=("OQ-006", "OQ-001"),
                notes=(
                    "Rapid transit track, J/M/Z services. The bridge carries two tracks, not the "
                    "four in the inherited taxonomy of AGENT-INSTRUCTIONS.md section 6 (CNF-003)."
                ),
                primitives=ribbon(
                    yt - m.m("transit_track_center_spacing") / 6.0,
                    yt + m.m("transit_track_center_spacing") / 6.0,
                    lambda x: deck_top(x) + deck_thickness * 0.25,
                    deck_thickness * 0.2,
                ),
            )
        )

    # Stiffening trusses, continuous anchorage to anchorage (SRC-004).
    truss_chord = m.m("floor_beam_depth") / 2.0
    for side_name, ysign in (("north", 1.0), ("south", -1.0)):
        yt = ysign * y_truss
        prims = []
        for xa_, xb_ in zip(deck_xs, deck_xs[1:]):
            if xa_ < -x_anchor - 1e-6 or xb_ > x_anchor + 1e-6:
                continue
            for which in ("top", "bottom"):
                za_ = deck_top(xa_) if which == "top" else deck_under(xa_)
                zb_ = deck_top(xb_) if which == "top" else deck_under(xb_)
                prims.append(
                    (
                        "box_span",
                        (xa_, yt - truss_chord, za_ - truss_chord),
                        (xb_, yt + truss_chord, zb_ + truss_chord),
                    )
                )
        b.add(
            Part(
                f"stiffening_truss_{side_name}",
                "deck_system",
                ("CTL-009", "CTL-010", "CTL-003", "CTL-101", "CTL-103", "CTL-001"),
                open_questions=("OQ-001", "OQ-011"),
                notes=(
                    "Top and bottom chords of one stiffening truss, 67 ft from its partner and 40 "
                    "ft deep. Runs continuously from one anchorage to the other and is not rigidly "
                    "connected to the towers or anchorages (SRC-004). Web members are not modelled "
                    "at this milestone."
                ),
                primitives=prims,
            )
        )

    # Transverse floor beams at CTL-012 spacing, across the suspended structure.
    fb_depth = m.m("floor_beam_depth")
    fb_segments = []
    for x in _frange(-x_anchor, x_anchor, m.m("floor_beam_spacing")):
        z = deck_under(x) + fb_depth / 2.0
        fb_segments.append([(x, -y_deck, z), (x, y_deck, z)])
    b.add(
        Part(
            "deck_floor_beam_set",
            "deck_system",
            ("CTL-008", "CTL-011", "CTL-012", "CTL-003", "CTL-101", "CTL-103"),
            open_questions=("OQ-001",),
            notes=(
                f"{len(fb_segments)} transverse floor beams, CTL-011 deep and CTL-008 long, at "
                "CTL-012 spacing. The deck sits above them and they hang from the suspenders."
            ),
            primitives=[("line", fb_segments)],
        )
    )

    # ===================================================================== approaches
    for end, sign in (("manhattan", -1.0), ("brooklyn", 1.0)):
        xs = sorted([sign * x_anchor, sign * x_end])
        prims = []
        for xa_, xb_ in zip(deck_xs, deck_xs[1:]):
            if xa_ < xs[0] - 1e-6 or xb_ > xs[1] + 1e-6:
                continue
            prims.append(
                (
                    "prism",
                    [
                        (xa_, -y_deck, deck_top(xa_) - deck_thickness * 2),
                        (xb_, -y_deck, deck_top(xb_) - deck_thickness * 2),
                        (xb_, y_deck, deck_top(xb_) - deck_thickness * 2),
                        (xa_, y_deck, deck_top(xa_) - deck_thickness * 2),
                    ],
                    [
                        (xa_, -y_deck, deck_top(xa_) - deck_thickness),
                        (xb_, -y_deck, deck_top(xb_) - deck_thickness),
                        (xb_, y_deck, deck_top(xb_) - deck_thickness),
                        (xa_, y_deck, deck_top(xa_) - deck_thickness),
                    ],
                )
            )
        b.add(
            Part(
                f"{end}_approach",
                "approaches",
                ("CTL-002", "CTL-036", "CTL-008", "CTL-101", "CTL-103"),
                open_questions=("OQ-006", "OQ-001"),
                notes=(
                    "Approach viaduct at CTL-036 grade. DRV-015 puts its far end well above street "
                    "level, which the model does not believe: see OQ-006."
                ),
                primitives=prims,
            )
        )

    # ======================================================================== details
    for side_name, ysign in (("north", 1.0), ("south", -1.0)):
        yr = ysign * y_deck
        segs = []
        for xa_, xb_ in zip(deck_xs, deck_xs[1:]):
            segs.append(
                [
                    (xa_, yr, deck_top(xa_) + truss_chord),
                    (xb_, yr, deck_top(xb_) + truss_chord),
                ]
            )
        b.add(
            Part(
                f"deck_railing_{side_name}",
                "details",
                ("CTL-008", "CTL-002", "CTL-103", "CTL-101"),
                open_questions=("OQ-006",),
                notes=(
                    "Heavy lattice railing on the deck edge (SRC-004). Height is not sourced, so "
                    "this is a line, not a dimensioned member."
                ),
                primitives=segs and [("line", segs)] or [],
            )
        )

    report_extra = {
        "stations_m": {k: round(v, 4) for k, v in stations.items()},
        "elevations_m": {
            "mean_high_water": 0.0,
            "tower_pier_top": round(z_pier_top, 4),
            "deck_top_at_anchorage": round(z_deck_anchor, 4),
            "deck_underside_at_midspan": round(z_deck_under_mid, 4),
            "deck_top_at_midspan": round(z_deck_top_mid, 4),
            "main_cable_at_midspan": round(z_cable_mid, 4),
            "tower_top": round(z_tower_top, 4),
            "approach_end_derived": round(z_approach_end, 4),
        },
        "deck_chain_intervals_m": merge_x_intervals(
            b.parts, ("deck_system", "approaches"), tolerance=1.0
        ),
        "suspender_count_per_cable": len(susp_stations),
    }
    return b, report_extra


# ------------------------------------------------------------------------- gltf output


def write_glb(builder: SkeletonBuilder, path: Path, scale: float, model: ControlModel) -> Path:
    g = GltfBuilder(
        generator=f"williamsburg-bridge-3d {AGENT}",
        scale=scale,
        copyright_text="Ethical Tech CoLab - source-governed digital twin",
    )
    g.set_root_name("williamsburg_bridge_control_skeleton")
    g.set_root_extras(
        {
            "control_document_sha256": model.document_sha256,
            "scale_denominator": 1.0 / scale if scale else 1.0,
            "vertical_datum": "mean high water",
            "units": "meters",
        }
    )
    system_nodes: dict[str, int] = {}
    for part in builder.parts:
        color = MATERIAL_COLOR[part.material]
        # Provenance drives opacity here as well as in the viewer, so an exported GLB opened in any
        # third-party tool still shows which geometry is reasoned rather than sourced.
        alpha = {"MEASURED": 1.0, "DOCUMENTED": 1.0, "INFERRED": 0.65, "ASSUMED": 0.35}[
            part.provenance
        ]
        mat = g.add_material(
            f"{part.material}_{part.provenance.lower()}",
            (*color, alpha),
            unlit=part.material == "reference",
        )
        prims = []
        for prim in part.primitives:
            kind = prim[0]
            if kind == "line":
                segs = [tuple(map(tuple, s)) for s in prim[1]]
                if segs:
                    prims.append(g.line_primitive(segs, mat))
            elif kind == "box":
                pos, nor, idx = box_mesh_data(prim[1], prim[2])
                prims.append(g.triangle_primitive(pos, nor, idx, mat))
            elif kind == "box_span":
                lo = tuple(min(a, b) for a, b in zip(prim[1], prim[2]))
                hi = tuple(max(a, b) for a, b in zip(prim[1], prim[2]))
                hi = tuple(h + 1e-4 if h - l < 1e-6 else h for l, h in zip(lo, hi))
                pos, nor, idx = box_mesh_data(lo, hi)
                prims.append(g.triangle_primitive(pos, nor, idx, mat))
            elif kind == "prism":
                pos, nor, idx = prism_mesh_data(prim[1], prim[2])
                prims.append(g.triangle_primitive(pos, nor, idx, mat))
            elif kind == "tube":
                pos, nor, idx = tube_mesh_data(prim[1], prim[2], sides=8)
                prims.append(g.triangle_primitive(pos, nor, idx, mat))
            else:  # pragma: no cover - guarded by the closed set above
                raise ValueError(f"unknown primitive kind {kind!r}")
        if not prims:
            continue
        mesh = g.add_mesh(part.part_id, prims)
        node = g.add_node(part.part_id, mesh=mesh, extras=part.metadata())
        if part.system not in system_nodes:
            system_nodes[part.system] = g.add_node(part.system)
            g.add_to_root(system_nodes[part.system])
        g.add_child(system_nodes[part.system], node)
    return g.save_glb(path)


# ------------------------------------------------------------------------------- main


def main() -> int:
    model = load_control_model(REPO / "GEOMETRY-CONTROL.md")
    builder, extra = build(model)
    parts = builder.parts

    (REPO / "mesh" / "glb").mkdir(parents=True, exist_ok=True)
    (REPO / "viewer" / "metadata").mkdir(parents=True, exist_ok=True)
    (REPO / "viewer" / "public").mkdir(parents=True, exist_ok=True)

    glb = write_glb(builder, REPO / "mesh" / "glb" / "control_skeleton.glb", 1.0, model)
    write_glb(
        builder,
        REPO / "mesh" / "glb" / "control_skeleton_ho.glb",
        1.0 / HO_SCALE_DENOMINATOR,
        model,
    )
    shutil.copyfile(glb, REPO / "viewer" / "public" / "control_skeleton.glb")

    census: dict[str, int] = {}
    for part in parts:
        census[part.provenance] = census.get(part.provenance, 0) + 1
    grades: dict[str, int] = {}
    for part in parts:
        grades[part.confidence] = grades.get(part.confidence, 0) + 1
    systems: dict[str, int] = {}
    for part in parts:
        systems[part.system] = systems.get(part.system, 0) + 1

    parts_doc = {
        "schema_version": "1.0",
        "model": "control_skeleton",
        "milestone": 1,
        "bridge": "Williamsburg Bridge",
        "generated_by": AGENT,
        "control_document": "GEOMETRY-CONTROL.md",
        "control_document_sha256": model.document_sha256,
        "units": "meters",
        "vertical_datum": "mean high water",
        "ho_scale_denominator": HO_SCALE_DENOMINATOR,
        "taxonomy": list(KNOWN_SYSTEMS),
        "controls": [
            {
                "control_id": c.control_id,
                "key": c.key,
                "value": c.value,
                "unit": c.unit,
                "value_m": round(c.value_m, 6),
                "source_ids": list(c.source_ids),
                "confidence": c.confidence,
                "is_placeholder": c.is_placeholder,
                "notes": c.notes,
            }
            for c in model.controls.values()
        ],
        "parts": [p.metadata() for p in parts],
    }
    (REPO / "viewer" / "metadata" / "parts.json").write_text(
        json.dumps(parts_doc, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(
        REPO / "viewer" / "metadata" / "parts.json", REPO / "viewer" / "public" / "parts.json"
    )

    report = {
        "schema_version": "1.0",
        "generated_by": AGENT,
        "control_document_sha256": model.document_sha256,
        "controls_total": len(model.controls),
        "controls_sourced": len(model.controls) - len(model.placeholders),
        "placeholders": sorted(c.control_id for c in model.placeholders),
        "parts_total": len(parts),
        "provenance_census": census,
        "confidence_census": grades,
        "system_census": systems,
        **extra,
    }
    (REPO / "viewer" / "metadata" / "build_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    scale_doc = {
        "schema_version": "1.0",
        "ho_scale_denominator": HO_SCALE_DENOMINATOR,
        "control_document_sha256": model.document_sha256,
        "controls": {
            c.key: ho_report(c.value_m) for c in model.controls.values() if is_linear(c.unit)
        },
    }
    (REPO / "viewer" / "metadata" / "scale_ho.json").write_text(
        json.dumps(scale_doc, indent=2) + "\n", encoding="utf-8"
    )

    print(f"control document sha256 : {model.document_sha256[:12]}")
    print(f"controls                : {len(model.controls)} "
          f"({report['controls_sourced']} sourced, {len(model.placeholders)} placeholder)")
    print(f"parts                   : {len(parts)}")
    print(f"provenance              : " + "  ".join(
        f"{k.lower()}={census.get(k, 0)}"
        for k in ("MEASURED", "DOCUMENTED", "INFERRED", "ASSUMED")
    ))
    print(f"confidence              : " + "  ".join(
        f"{k}={grades.get(k, 0)}" for k in ("A", "B", "C", "D")
    ))
    print(f"glb                     : {glb.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
