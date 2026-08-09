"""Run the geometry regression and source traceability suites.

Both suites are declarative JSON under ``tests/``. This module holds the measures; the JSON holds
what is expected and why. A test in ``assert`` mode fails the build; a test in ``report_only`` mode
surfaces a number without blocking, and is used for things that *should* change later.

Run::

    python scripts/validate_dimensions.py            # both suites
    python scripts/validate_dimensions.py --json     # machine-readable summary
"""

from __future__ import annotations

import fnmatch
import json
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from control_model import load_control_model  # noqa: E402
from normalize_units import ho_millimeters, is_linear  # noqa: E402

REPO = SCRIPT_DIR.parent
TOL = 1e-3

GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


@dataclass
class Result:
    test_id: str
    title: str
    mode: str
    passed: bool
    detail: str

    @property
    def status(self) -> str:
        if self.mode == "report_only":
            return "REPORT"
        return "PASS" if self.passed else "FAIL"


class Context:
    """Everything the measures read, loaded once."""

    def __init__(self) -> None:
        self.model = load_control_model(REPO / "GEOMETRY-CONTROL.md")
        self.control_text = (REPO / "GEOMETRY-CONTROL.md").read_text(encoding="utf-8")
        self.register_text = (REPO / "SOURCE-REGISTER.md").read_text(encoding="utf-8")
        self.parts_doc = json.loads(
            (REPO / "viewer" / "metadata" / "parts.json").read_text(encoding="utf-8")
        )
        self.report = json.loads(
            (REPO / "viewer" / "metadata" / "build_report.json").read_text(encoding="utf-8")
        )
        self.scale = json.loads(
            (REPO / "viewer" / "metadata" / "scale_ho.json").read_text(encoding="utf-8")
        )
        self.parts: list[dict[str, Any]] = self.parts_doc["parts"]
        self.stations: dict[str, float] = self.report["stations_m"]
        self.elevations: dict[str, float] = self.report["elevations_m"]

        # SOURCE-REGISTER.md section 1. The Verified column is located by reading the header rather
        # than by a hardcoded index: HOW-TO-DESIGN.md section 11 records a "verified" column parser
        # that choked on markdown bold and reported every source as unverified. An off-by-one here
        # would silently invert STT-008 and STT-009.
        self.sources: dict[str, dict[str, str]] = {}
        header = re.search(r"^\|\s*Source ID\s*\|(.+)$", self.register_text, re.M)
        if header is None:
            raise ValueError("SOURCE-REGISTER.md section 1 has no 'Source ID' header row")
        columns = [c.strip().lower() for c in header.group(1).split("|")]
        try:
            verified_col = columns.index("verified")
        except ValueError as exc:
            raise ValueError(
                "SOURCE-REGISTER.md section 1 has no 'Verified' column"
            ) from exc
        for row in re.finditer(r"^\|\s*(SRC-\d+)\s*\|(.+)$", self.register_text, re.M):
            cells = [c.strip() for c in row.group(2).split("|")]
            if len(cells) <= verified_col:
                raise ValueError(f"{row.group(1)} has fewer columns than the section 1 header")
            verified = cells[verified_col].strip().strip("*").lower()
            self.sources[row.group(1)] = {
                "title": cells[0] if cells else "",
                "verified": verified,
            }
        self.negative_controls = set(re.findall(r"^\|\s*(NEG-\d+)\s*\|", self.register_text, re.M))
        self.queue_text = self.register_text.split("## 4. Verification queue", 1)[-1].split(
            "## 5.", 1
        )[0]
        self.open_questions = set(re.findall(r"^\|\s*(OQ-\d+)\s*\|", self.control_text, re.M))

    def control(self, key: str):
        return self.model.get(key)


MEASURES: dict[str, Callable[[Context, dict[str, Any]], tuple[bool, str]]] = {}


def measure(name: str):
    def wrap(fn):
        MEASURES[name] = fn
        return fn

    return wrap


# ------------------------------------------------------------------ geometry measures


@measure("station_separation_equals_control")
def _m_station_sep(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    a, b = spec["stations"]
    measured = abs(ctx.stations[b] - ctx.stations[a])
    expected = ctx.control(spec["control"]).value_m
    ok = abs(measured - expected) <= TOL
    return ok, f"{a}..{b} = {measured:.4f} m, control {spec['control']} = {expected:.4f} m"


@measure("origin_is_main_span_midpoint")
def _m_origin(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    mid = ctx.stations["main_span_midpoint"]
    towers = (ctx.stations["manhattan_tower"], ctx.stations["brooklyn_tower"])
    centred = abs((towers[0] + towers[1]) / 2.0 - mid)
    ok = abs(mid) <= TOL and centred <= TOL
    return ok, f"midpoint at x={mid:.4f} m, tower mean offset {centred:.6f} m"


@measure("elevation_equals_control")
def _m_elev(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    measured = ctx.elevations[spec["elevation"]]
    expected = ctx.control(spec["control"]).value_m
    ok = abs(measured - expected) <= TOL
    return ok, f"{spec['elevation']} = {measured:.4f} m, control {spec['control']} = {expected:.4f} m"


@measure("part_count_equals_control")
def _m_part_count(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    n = sum(1 for p in ctx.parts if p["system"] == spec["system"])
    expected = int(ctx.control(spec["control"]).value)
    ok = n == expected
    return ok, f"system {spec['system']} has {n} parts, control {spec['control']} = {expected}"


@measure("transit_track_negative_control")
def _m_tracks(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    tracks = [p for p in ctx.parts if re.match(r"^transit_track_\d+$", p["part_id"])]
    expected = int(ctx.control(spec["control"]).value)
    offenders = [
        p["part_id"]
        for p in ctx.parts
        for pat in spec["forbidden_part_patterns"]
        if fnmatch.fnmatchcase(p["part_id"], pat)
    ]
    ok = len(tracks) == expected and not offenders
    detail = f"{len(tracks)} transit tracks, control = {expected}"
    if offenders:
        detail += f"; forbidden part IDs present: {sorted(set(offenders))}"
    return ok, detail


@measure("part_prefix_count_equals_control")
def _m_prefix_count(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    wanted = {spec["prefix"] + s for s in spec["suffixes"]}
    found = {p["part_id"] for p in ctx.parts} & wanted
    expected = int(ctx.control(spec["control"]).value)
    ok = len(found) == expected
    return ok, f"{len(found)} deck sections present, control {spec['control']} = {expected}"


@measure("suspender_spacing_matches_control")
def _m_susp(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    count = ctx.report[spec["count_key"]]
    span = ctx.control(spec["span_control"]).value_m
    spacing = ctx.control(spec["spacing_control"]).value_m
    expected = int(round(span / spacing)) - 1
    ok = count == expected
    return ok, f"{count} suspenders per cable on the main span, expected {expected} from controls"


@measure("deck_longitudinal_continuity")
def _m_continuity(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    """No gap along X in the union of deck and approach geometry.

    The intervals are measured from the vertices the build emitted, not from a declared extent.
    Verified to fail against a deck chain truncated at the anchorage faces, which is the bug
    HOW-TO-DESIGN.md section 11 records shipping twice on the Manhattan Bridge.
    """
    intervals = ctx.report["deck_chain_intervals_m"]
    ends = (ctx.stations["manhattan_approach_end"], ctx.stations["brooklyn_approach_end"])
    covered_systems = {p["system"] for p in ctx.parts} & set(spec["systems"])
    missing = set(spec["systems"]) - covered_systems
    gaps: list[str] = []
    if missing:
        gaps.append(f"no geometry for system(s) {sorted(missing)}")
    if not intervals:
        gaps.append("no deck geometry at all")
        return False, "; ".join(gaps)
    if len(intervals) > 1:
        for (_, a_hi), (b_lo, _) in zip(intervals, intervals[1:]):
            gaps.append(f"gap of {b_lo - a_hi:.3f} m between x={a_hi:.3f} and x={b_lo:.3f}")
    lo, hi = intervals[0][0], intervals[-1][1]
    if lo - min(ends) > 1.0:
        gaps.append(f"deck starts at {lo:.3f} m but the approach end is {min(ends):.3f} m")
    if max(ends) - hi > 1.0:
        gaps.append(f"deck stops at {hi:.3f} m but the approach end is {max(ends):.3f} m")
    for anchor in ("manhattan_anchorage", "brooklyn_anchorage"):
        x = ctx.stations[anchor]
        if not any(a - 1.0 <= x <= b + 1.0 for a, b in intervals):
            gaps.append(f"{anchor} at {x:.3f} m lies outside the deck chain")
    ok = not gaps
    return ok, (
        "continuous from %.3f m to %.3f m in one unbroken interval" % (lo, hi)
        if ok
        else "; ".join(gaps)
    )


@measure("control_within_deck_elevation_range")
def _m_deck_range(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    value = ctx.control(spec["control"]).value_m
    lows = [
        ctx.elevations["approach_end_derived"],
        ctx.elevations["deck_top_at_anchorage"],
    ]
    high = ctx.elevations["deck_top_at_midspan"]
    ok = min(lows) <= value <= high
    return ok, (
        f"{spec['control']} = {value:.3f} m; modelled deck top runs "
        f"{min(lows):.3f} m to {high:.3f} m"
    )


@measure("approach_end_reaches_street_level")
def _m_approach(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    z = ctx.elevations[spec["elevation"]]
    ok = z <= spec["threshold_m"]
    return ok, (
        f"derived approach end sits {z:.2f} m above mean high water; a street-level approach "
        f"would be at or below {spec['threshold_m']:.2f} m. See OQ-006."
    )


@measure("measured_census")
def _m_measured(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    census = ctx.report["provenance_census"]
    n = census.get("MEASURED", 0)
    return n > 0, (
        f"MEASURED={n}  DOCUMENTED={census.get('DOCUMENTED', 0)}  "
        f"INFERRED={census.get('INFERRED', 0)}  ASSUMED={census.get('ASSUMED', 0)}"
    )


@measure("placeholder_ratchet")
def _m_ratchet(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    n = len(ctx.model.placeholders)
    ok = n <= spec["max_placeholders"]
    return ok, f"{n} placeholders, ratchet allows at most {spec['max_placeholders']}"


@measure("placeholder_parts_not_documented")
def _m_ph_parts(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    ph = {c.control_id for c in ctx.model.placeholders}
    bad = [
        p["part_id"]
        for p in ctx.parts
        if set(p["control_refs"]) & ph and p["provenance"] in ("DOCUMENTED", "MEASURED")
    ]
    return not bad, (
        f"{len(bad)} parts overclaim on a placeholder: {bad[:6]}"
        if bad
        else "no part consuming a placeholder claims DOCUMENTED or MEASURED"
    )


@measure("no_dimension_literals_in_scripts")
def _m_literals(ctx: Context, spec: dict[str, Any]) -> tuple[bool, str]:
    floor = float(spec["min_value_checked"])
    checked = {
        c.control_id: c.value for c in ctx.model.controls.values() if abs(c.value) >= floor
    }
    offenders: list[str] = []
    for path in sorted(SCRIPT_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for cid, value in checked.items():
            literal = f"{value:g}"
            if re.search(rf"(?<![\w.]){re.escape(literal)}(?![\w.])", text):
                offenders.append(f"{path.name} contains {literal} ({cid})")
    return not offenders, (
        "; ".join(offenders)
        if offenders
        else f"{len(checked)} control values of {floor:g} or more, none present as a literal"
    )


@measure("confidence_is_weakest_link")
def _m_weakest(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    bad = []
    for p in ctx.parts:
        refs = p["control_refs"]
        if not refs:
            expected = "D"
        else:
            expected = max(
                (ctx.model.by_id[r].confidence for r in refs), key=lambda g: GRADE_ORDER[g]
            )
        if p["confidence"] != expected:
            bad.append(f"{p['part_id']} is {p['confidence']}, weakest link is {expected}")
    return not bad, "; ".join(bad) if bad else f"{len(ctx.parts)} parts graded by weakest link"


@measure("parts_have_material_rule")
def _m_material(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    known = {r.material_id for r in ctx.model.materials}
    bad = [
        p["part_id"]
        for p in ctx.parts
        if not p.get("material") or p.get("material_id") not in known
    ]
    return not bad, (
        f"{len(bad)} parts without a material rule: {bad[:6]}"
        if bad
        else f"{len(ctx.parts)} parts matched by {len(known)} rules, no default used"
    )


@measure("glb_wellformed")
def _m_glb(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    path = REPO / "mesh" / "glb" / "control_skeleton.glb"
    data = path.read_bytes()
    magic, version, length = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67 or version != 2 or length != len(data):
        return False, f"bad GLB header in {path.name}"
    chunk_len, chunk_type = struct.unpack_from("<II", data, 12)
    if chunk_type != 0x4E4F534A:
        return False, "first chunk is not JSON"
    gltf = json.loads(data[20 : 20 + chunk_len].decode("utf-8"))
    named = {n["name"] for n in gltf["nodes"] if "extras" in n}
    part_ids = {p["part_id"] for p in ctx.parts}
    missing = part_ids - named
    if missing:
        return False, f"{len(missing)} parts carry no node extras: {sorted(missing)[:5]}"
    if gltf["asset"]["version"] != "2.0":
        return False, "asset.version is not 2.0"
    return True, (
        f"glTF 2.0, {len(gltf['nodes'])} nodes, {len(gltf['meshes'])} meshes, "
        f"{len(named)} carrying metadata, {len(data)} bytes"
    )


@measure("ho_scale_roundtrip")
def _m_ho(ctx: Context, _spec: dict[str, Any]) -> tuple[bool, str]:
    bad = []
    for control in ctx.model.controls.values():
        if not is_linear(control.unit):
            continue
        reported = ctx.scale["controls"][control.key]["ho_mm"]
        expected = ho_millimeters(control.value_m)
        if abs(reported - expected) > 0.05:
            bad.append(f"{control.control_id}: {reported} vs {expected:.3f} mm")
    return not bad, "; ".join(bad) if bad else "HO conversion agrees for every linear control"


# -------------------------------------------------------------- traceability measures


@measure("cited_sources_registered")
def _t_registered(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [
        f"{c.control_id} cites {s}"
        for c in ctx.model.controls.values()
        for s in c.source_ids
        if s not in ctx.sources
    ]
    return not bad, "; ".join(bad) if bad else f"{len(ctx.sources)} sources registered"


@measure("graded_controls_have_sources")
def _t_graded(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [c.control_id for c in ctx.model.controls.values() if not c.is_placeholder and not c.source_ids]
    return not bad, "; ".join(bad) if bad else "every A/B/C control cites a source"


@measure("placeholders_have_no_sources")
def _t_ph(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [c.control_id for c in ctx.model.placeholders if c.source_ids]
    return not bad, "; ".join(bad) if bad else f"{len(ctx.model.placeholders)} placeholders, none sourced"


@measure("part_control_refs_resolve")
def _t_refs(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [
        f"{p['part_id']} -> {r}"
        for p in ctx.parts
        for r in p["control_refs"]
        if r not in ctx.model.by_id
    ]
    return not bad, "; ".join(bad) if bad else "every part control reference resolves"


@measure("open_questions_registered")
def _t_oq(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [
        f"{p['part_id']} -> {q}"
        for p in ctx.parts
        for q in p["open_questions"]
        if q not in ctx.open_questions
    ]
    return not bad, "; ".join(bad) if bad else f"{len(ctx.open_questions)} open questions registered"


@measure("parts_have_source_basis")
def _t_basis(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [p["part_id"] for p in ctx.parts if not p.get("source_basis")]
    return not bad, "; ".join(bad) if bad else "every part declares a source basis"


@measure("forbidden_source_basis")
def _t_forbidden(ctx: Context, spec) -> tuple[bool, str]:
    bad = [
        f"{p['part_id']}:{b}"
        for p in ctx.parts
        for b in p["source_basis"]
        if b in spec["forbidden"]
    ]
    return not bad, "; ".join(bad) if bad else "no part claims an external-source basis"


@measure("cited_sources_are_verified")
def _t_verified(ctx: Context, _spec) -> tuple[bool, str]:
    bad = []
    for c in ctx.model.controls.values():
        for s in c.source_ids:
            if ctx.sources.get(s, {}).get("verified") != "yes":
                bad.append(f"{c.control_id} rests on unread {s}")
    return not bad, "; ".join(bad) if bad else "every cited source is marked verified"


@measure("unverified_sources_are_queued")
def _t_queued(ctx: Context, _spec) -> tuple[bool, str]:
    unverified = [s for s, meta in ctx.sources.items() if meta["verified"] != "yes"]
    bad = [s for s in unverified if s not in ctx.queue_text]
    return not bad, (
        "; ".join(f"{s} is unread and not queued" for s in bad)
        if bad
        else f"{len(unverified)} unread source(s), all in the verification queue"
    )


@measure("parts_have_known_system")
def _t_system(ctx: Context, spec) -> tuple[bool, str]:
    known = set(spec["known"])
    bad = [f"{p['part_id']}:{p['system']}" for p in ctx.parts if p["system"] not in known]
    return not bad, "; ".join(bad) if bad else f"{len(ctx.parts)} parts in {len(known)} systems"


@measure("parts_have_review_fields")
def _t_review(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [
        p["part_id"]
        for p in ctx.parts
        if not p.get("review_status") or not p.get("last_modified_by_agent")
    ]
    return not bad, "; ".join(bad) if bad else "every part records review_status and agent"


@measure("control_document_hash_matches")
def _t_hash(ctx: Context, _spec) -> tuple[bool, str]:
    built = ctx.parts_doc["control_document_sha256"]
    current = ctx.model.document_sha256
    ok = built == current
    return ok, (
        f"parts.json built from {built[:12]}, GEOMETRY-CONTROL.md is now {current[:12]}"
        + ("" if ok else " - rebuild with scripts/build_control_skeleton.py")
    )


@measure("placeholders_cite_open_questions")
def _t_ph_oq(ctx: Context, _spec) -> tuple[bool, str]:
    bad = []
    for c in ctx.model.placeholders:
        row = re.search(rf"^\|\s*{c.control_id}\s*\|.*$", ctx.control_text, re.M)
        if not row or not re.search(r"OQ-\d+", row.group(0)):
            bad.append(c.control_id)
    return not bad, (
        "; ".join(f"{c} names no open question" for c in bad)
        if bad
        else f"all {len(ctx.model.placeholders)} placeholders name an open question"
    )


@measure("no_negative_control_citations")
def _t_neg(ctx: Context, _spec) -> tuple[bool, str]:
    bad = [
        f"{c.control_id} cites {s}"
        for c in ctx.model.controls.values()
        for s in c.source_ids
        if s in ctx.negative_controls or s.startswith("NEG-")
    ]
    return not bad, "; ".join(bad) if bad else "no control cites a negative control"


@measure("negative_controls_declared")
def _t_neg_declared(ctx: Context, spec) -> tuple[bool, str]:
    n = len(ctx.negative_controls)
    ok = n >= spec["expected_minimum"]
    return ok, f"{n} negative controls declared, at least {spec['expected_minimum']} required"


@measure("single_source_census")
def _t_single(ctx: Context, _spec) -> tuple[bool, str]:
    counts: dict[str, int] = {}
    single = 0
    for c in ctx.model.controls.values():
        if c.is_placeholder:
            continue
        if len(c.source_ids) == 1:
            single += 1
        for s in c.source_ids:
            counts[s] = counts.get(s, 0) + 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])
    spread = ", ".join(f"{s}x{n}" for s, n in top)
    return True, f"{single} controls rest on a single source; citations by source: {spread}"


# --------------------------------------------------------------------------- runner


def run_suite(ctx: Context, path: Path) -> list[Result]:
    suite = json.loads(path.read_text(encoding="utf-8"))
    results: list[Result] = []
    for spec in suite["tests"]:
        rule = spec["rule"]
        fn = MEASURES.get(rule)
        if fn is None:
            results.append(
                Result(spec["id"], spec["title"], "assert", False, f"no measure named {rule!r}")
            )
            continue
        try:
            ok, detail = fn(ctx, spec)
        except Exception as exc:  # noqa: BLE001 - a broken measure must fail loudly
            results.append(
                Result(spec["id"], spec["title"], spec["mode"], False, f"{type(exc).__name__}: {exc}")
            )
            continue
        results.append(Result(spec["id"], spec["title"], spec["mode"], ok, detail))
    return results


def main() -> int:
    ctx = Context()
    results: list[Result] = []
    for name in ("geometry_regression_tests.json", "source_traceability_tests.json"):
        results.extend(run_suite(ctx, REPO / "tests" / name))

    failed = [r for r in results if r.mode != "report_only" and not r.passed]
    reported = [r for r in results if r.mode == "report_only"]
    passed = [r for r in results if r.mode != "report_only" and r.passed]

    if "--json" in sys.argv:
        print(
            json.dumps(
                {
                    "control_document_sha256": ctx.model.document_sha256,
                    "passed": len(passed),
                    "failed": len(failed),
                    "report_only": len(reported),
                    "results": [
                        {
                            "id": r.test_id,
                            "title": r.title,
                            "mode": r.mode,
                            "status": r.status,
                            "detail": r.detail,
                        }
                        for r in results
                    ],
                },
                indent=2,
            )
        )
    else:
        for r in results:
            print(f"{r.status:<6} {r.test_id}  {r.title}")
            print(f"       {r.detail}")
        print()
        print(
            f"{len(passed)} passed, {len(failed)} failed, {len(reported)} report-only "
            f"(control document {ctx.model.document_sha256[:12]})"
        )

    (REPO / "tests" / "validation_report.json").write_text(
        json.dumps(
            {
                "control_document_sha256": ctx.model.document_sha256,
                "passed": len(passed),
                "failed": len(failed),
                "report_only": len(reported),
                "results": [
                    {
                        "id": r.test_id,
                        "title": r.title,
                        "mode": r.mode,
                        "status": r.status,
                        "detail": r.detail,
                    }
                    for r in results
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
