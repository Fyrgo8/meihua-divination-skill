#!/usr/bin/env python3
"""Normalize a structured Meihua Yishu case file.

Usage:
    python normalize_case_input.py --input case.json --format json
    python normalize_case_input.py --input case.json --format markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TRIGRAM_ALIASES = {
    "乾": "乾",
    "qian": "乾",
    "兑": "兑",
    "dui": "兑",
    "离": "离",
    "li": "离",
    "震": "震",
    "zhen": "震",
    "巽": "巽",
    "xun": "巽",
    "坎": "坎",
    "kan": "坎",
    "艮": "艮",
    "gen": "艮",
    "坤": "坤",
    "kun": "坤",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize a Meihua divination case file.")
    parser.add_argument("--input", required=True, help="Path to input JSON.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    return parser.parse_args()


def normalize_trigram(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")
    key = value.strip().lower()
    normalized = TRIGRAM_ALIASES.get(key)
    if normalized is None:
        allowed = " / ".join(sorted(set(TRIGRAM_ALIASES.values())))
        raise ValueError(f"{field_name} must be one of: {allowed}")
    return normalized


def normalize_moving_lines(payload: dict) -> list[int]:
    if "moving_lines" in payload:
        raw = payload["moving_lines"]
    elif "moving_line" in payload:
        raw = [payload["moving_line"]]
    else:
        return []

    if not isinstance(raw, list):
        raise ValueError("moving_lines must be a list, or use moving_line as a single integer.")

    normalized: list[int] = []
    for item in raw:
        if not isinstance(item, int):
            raise ValueError("Each moving line must be an integer.")
        if item < 1 or item > 6:
            raise ValueError("Moving lines must be between 1 and 6.")
        normalized.append(item)

    return sorted(set(normalized))


def normalize_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object.")

    question_context = payload.get("question_context")
    if not isinstance(question_context, str) or not question_context.strip():
        raise ValueError("question_context is required and must be a non-empty string.")

    result = {
        "question_context": question_context.strip(),
        "upper_trigram": normalize_trigram(payload.get("upper_trigram"), "upper_trigram"),
        "lower_trigram": normalize_trigram(payload.get("lower_trigram"), "lower_trigram"),
        "moving_lines": normalize_moving_lines(payload),
        "month_branch": str(payload.get("month_branch", "")).strip(),
        "day_branch": str(payload.get("day_branch", "")).strip(),
        "external_signs": payload.get("external_signs", []),
        "notes": str(payload.get("notes", "")).strip(),
    }

    if result["external_signs"] and not isinstance(result["external_signs"], list):
        raise ValueError("external_signs must be a list of strings.")

    for item in result["external_signs"]:
        if not isinstance(item, str):
            raise ValueError("Each external sign must be a string.")

    return result


def to_markdown(payload: dict) -> str:
    signs = payload["external_signs"] or ["(none)"]
    moving_lines = ", ".join(str(x) for x in payload["moving_lines"]) or "(none)"
    return "\n".join(
        [
            "# Normalized Meihua Case",
            "",
            "## Question",
            payload["question_context"],
            "",
            "## Core Hexagram Fields",
            f"- upper_trigram: {payload['upper_trigram']}",
            f"- lower_trigram: {payload['lower_trigram']}",
            f"- moving_lines: {moving_lines}",
            "",
            "## Time Context",
            f"- month_branch: {payload['month_branch'] or '(empty)'}",
            f"- day_branch: {payload['day_branch'] or '(empty)'}",
            "",
            "## External Signs",
            *[f"- {item}" for item in signs],
            "",
            "## Notes",
            payload["notes"] or "(empty)",
        ]
    )


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"Input file not found: {path}", file=sys.stderr)
        return 1

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        normalized = normalize_payload(payload)
    except Exception as exc:  # noqa: BLE001
        print(f"Normalization failed: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(normalized))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
