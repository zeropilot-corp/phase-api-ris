#!/usr/bin/env python3
"""
validate_erd.py — Reference validator for Phase API Electromagnetic Response Descriptors (ERDs).

Usage:
    python validation/validate_erd.py schema/erd_pin_28ghz.json
    python validation/validate_erd.py schema/erd_varactor_28ghz.json [more.json ...]

Validates one or more ERD JSON files against schema/erd.schema.json (JSON Schema draft-07)
and runs a set of physical-consistency sanity checks. Exits 0 if all files pass,
1 if any file fails.

Companion artifact for:
    R. D. Javor, "Electromagnetic Response Descriptors, Spatial Validity Regions,
    and the Phase API: An Antenna-Domain Interface for Reconfigurable Intelligent
    Surfaces in 6G," ZeroPilot Corporation, 2026.

Part of the Phase API companion artifacts (MIT-licensed code).
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator
    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False


def find_schema(start: Path):
    """Locate schema/erd.schema.json by walking up from the given file."""
    for base in [start.parent, *start.parents]:
        candidate = base / "schema" / "erd.schema.json"
        if candidate.is_file():
            return candidate
        candidate = base / "erd.schema.json"
        if candidate.is_file():
            return candidate
    return None


def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e.msg} at line {e.lineno}, col {e.colno})"


def schema_validate(erd: dict, schema: dict) -> list:
    """Return a list of schema violation messages (empty if valid).

    Uses Draft7Validator, consistent with the '$schema': draft-07 declaration
    in erd.schema.json.
    """
    if not HAVE_JSONSCHEMA:
        return ["[skipped] jsonschema not installed — run: pip install jsonschema"]
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(erd), key=lambda e: list(e.path))
    msgs = []
    for e in errors:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        msgs.append(f"{loc}: {e.message}")
    return msgs


def sanity_checks(erd: dict) -> list:
    """Physical-consistency warnings beyond pure schema conformance.

    All key lookups use snake_case to match the ERD schema field names.
    """
    warns = []

    # --- realized_phase_range ---
    pr = erd.get("realized_phase_range")
    if isinstance(pr, list) and len(pr) == 2:
        if pr[0] >= pr[1]:
            warns.append(
                f"realized_phase_range min ({pr[0]}) >= max ({pr[1]}): "
                "phase range must be a non-empty interval"
            )
        if (pr[1] - pr[0]) > 360.0001:
            warns.append(
                f"realized_phase_range span {pr[1] - pr[0]:.1f}° exceeds 360°: "
                "physically unrealizable for a passive unit cell"
            )

    # --- operating_frequency_grid_GHz ---
    grid = erd.get("operating_frequency_grid_GHz")
    if isinstance(grid, list) and grid:
        if any(f <= 0 for f in grid):
            warns.append(
                "operating_frequency_grid_GHz contains non-positive frequency value"
            )
        if grid != sorted(grid):
            warns.append(
                "operating_frequency_grid_GHz is not monotonically increasing: "
                "sort the frequency grid for deterministic squint interpolation"
            )

    # --- SVR core vs. marginal consistency ---
    # Core limits must be strictly tighter (smaller angles) than marginal limits.
    core = erd.get("svr_core_angular_limits") or {}
    marg = erd.get("svr_marginal_angular_limits") or {}
    for k in ("theta_incident_max_deg", "theta_scattered_max_deg"):
        c = core.get(k)
        m = marg.get(k)
        if isinstance(c, (int, float)) and isinstance(m, (int, float)):
            if c > m:
                warns.append(
                    f"svr_core_angular_limits.{k} ({c}°) exceeds "
                    f"svr_marginal_angular_limits.{k} ({m}°): "
                    "core zone must be a strict subset of the marginal zone"
                )

    # --- phase_quantization_resolution ---
    pqr = erd.get("phase_quantization_resolution")
    pr = erd.get("realized_phase_range")
    if isinstance(pqr, (int, float)) and pqr is not None and pqr < 0:
        warns.append("phase_quantization_resolution is negative; must be >= 0")
    if (
        isinstance(pqr, (int, float))
        and pqr > 0
        and isinstance(pr, list)
        and len(pr) == 2
    ):
        span = pr[1] - pr[0]
        if span > 0 and (span / pqr) < 1.0:
            warns.append(
                f"phase_quantization_resolution ({pqr}°) exceeds "
                f"realized_phase_range span ({span}°): yields fewer than one state"
            )

    # --- per_state_insertion_loss_dB ---
    pil = erd.get("per_state_insertion_loss_dB")
    if isinstance(pil, list):
        if any(v > 0 for v in pil):
            warns.append(
                "per_state_insertion_loss_dB contains positive values: "
                "insertion loss should be <= 0 dB (negative or zero)"
            )

    return warns


def validate_file(path: Path, schema: dict) -> bool:
    print(f"\n=== {path} ===")
    erd, err = load_json(path)
    if err:
        print(f"  FAIL  {err}")
        return False

    ok = True
    if schema is not None:
        viol = schema_validate(erd, schema)
        if viol and not viol[0].startswith("[skipped]"):
            ok = False
            print("  FAIL  schema violations:")
            for v in viol:
                print(f"        - {v}")
        elif viol:
            print(f"  WARN  {viol[0]}")
        else:
            print("  PASS  schema conformance (JSON Schema draft-07)")
    else:
        print("  WARN  schema not found — JSON syntax checked only")

    warnings = sanity_checks(erd)
    for w in warnings:
        print(f"  WARN  sanity: {w}")
    if not warnings:
        print("  PASS  physical sanity checks")

    hw = erd.get("hardware_class", "?")
    print(f"  INFO  hardware_class = {hw}")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Validate Phase API Electromagnetic Response Descriptor (ERD) JSON files "
            "against erd.schema.json and physical-consistency sanity checks."
        )
    )
    ap.add_argument("files", nargs="+", help="ERD JSON file(s) to validate")
    ap.add_argument("--schema", help="explicit path to erd.schema.json")
    args = ap.parse_args(argv)

    schema = None
    schema_path = (
        Path(args.schema) if args.schema else find_schema(Path(args.files[0]))
    )
    if schema_path and schema_path.is_file():
        schema_obj, serr = load_json(schema_path)
        if serr:
            print(f"WARN  could not load schema: {serr}")
        else:
            schema = schema_obj
            print(f"Using schema: {schema_path} (JSON Schema draft-07)")
    else:
        print("WARN  schema/erd.schema.json not found near input; syntax-only mode")

    results = [validate_file(Path(f), schema) for f in args.files]
    passed, total = sum(results), len(results)
    print(f"\nSummary: {passed}/{total} file(s) passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
