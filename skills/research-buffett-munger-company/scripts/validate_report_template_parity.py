#!/usr/bin/env python3
"""Validate the fixed reader-facing contract for a public company report."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

TEMPLATE_VERSION = "company-research-publication-v1"
MIN_SECTIONS = 15
MIN_TABLES = 8
MIN_SVGS = 2
MIN_DETAILS = 8
CROSSWALK_PATH = (
    Path(__file__).resolve().parents[1]
    / "references"
    / "methodology-implementation-crosswalk.json"
)


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.section_ids: list[str] = []
        self.fragment_targets: list[str] = []
        self.template_version: str | None = None
        self.stylesheets: list[str] = []
        self.counts = {"section": 0, "table": 0, "svg": 0, "details": 0}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "body":
            self.template_version = values.get("data-template")
        if tag == "section":
            self.counts["section"] += 1
            if element_id:
                self.section_ids.append(element_id)
        elif tag in self.counts:
            self.counts[tag] += 1
        if tag == "a":
            href = values.get("href") or ""
            if href.startswith("#") and len(href) > 1:
                self.fragment_targets.append(href[1:])
        if (
            tag == "link"
            and (values.get("rel") or "").lower() == "stylesheet"
            and values.get("href")
        ):
            self.stylesheets.append(values["href"])


def _first_index(items: list[str], candidates: tuple[str, ...]) -> int | None:
    indexes = [items.index(candidate) for candidate in candidates if candidate in items]
    return min(indexes) if indexes else None


def validate_report_html(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        html = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "schema_version": "seed.public-report-template-parity.v1",
            "generated_at": datetime.now(UTC).isoformat(),
            "path": path.name,
            "valid": False,
            "errors": [f"cannot read report HTML: {exc}"],
            "warnings": [],
        }

    parser = ReportParser()
    parser.feed(html)

    if parser.template_version != TEMPLATE_VERSION:
        errors.append(
            f"body data-template must be {TEMPLATE_VERSION!r}; "
            f"found {parser.template_version!r}"
        )

    has_shared_theme = any(
        href.endswith("/company-report-theme.css")
        or href == "../company-report-theme.css"
        for href in parser.stylesheets
    )
    is_canonical_inline_theme = all(
        token in html for token in ("--paper:", "--green:", "--amber:", "--shadow:")
    )
    if not (has_shared_theme or is_canonical_inline_theme):
        errors.append(
            "report must use ../company-report-theme.css or the canonical inline theme"
        )

    groups: dict[str, tuple[str, ...]] = {
        "status legend": ("status-legend",),
        "long-term dossier": ("long-term",),
        "near-term event monitor": ("event-monitor",),
        "snapshot": ("snapshot", "summary"),
        "five-year financials": ("financials",),
        "latest quarter/interim": (
            "quarter",
            "quarterly",
            "business-kpis",
            "financials",
        ),
        "capital/per-share bridge": ("capital",),
        "market pricing": ("market-pricing",),
        "Buffett–Munger interpretation": ("buffett",),
        "methodology": ("methodology",),
        "timeline": ("timeline",),
        "next validation": ("monitor",),
        "evidence/sources": ("evidence", "sources"),
    }
    resolved_groups: dict[str, str] = {}
    for label, candidates in groups.items():
        resolved = next((item for item in candidates if item in parser.ids), None)
        if resolved is None:
            errors.append(f"missing required reader job: {label} ({' / '.join(candidates)})")
        else:
            resolved_groups[label] = resolved

    contract_anchor = next(
        (
            item
            for item in ("research-contract", "audit-matrix", "dimensions", "methodology")
            if item in parser.ids
        ),
        None,
    )
    if contract_anchor is None:
        errors.append("missing 25×50×9 research-contract section")

    status_index = _first_index(parser.section_ids, ("status-legend",))
    entry_index = _first_index(parser.section_ids, ("report-doors", "long-term"))
    snapshot_index = _first_index(parser.section_ids, ("snapshot", "summary"))
    if None in (status_index, entry_index, snapshot_index):
        errors.append("cannot resolve status → entries → snapshot reading order")
    elif not status_index < entry_index < snapshot_index:
        errors.append(
            "first reader order must be status legend → report entries → snapshot"
        )

    missing_targets = sorted(
        {
            target
            for target in parser.fragment_targets
            if target not in parser.ids and target not in {"main-content", "home"}
        }
    )
    if missing_targets:
        errors.append(f"fragment links do not resolve: {missing_targets}")

    if parser.counts["section"] < MIN_SECTIONS:
        errors.append(
            f"full report requires at least {MIN_SECTIONS} sections; "
            f"found {parser.counts['section']}"
        )
    if parser.counts["table"] < MIN_TABLES:
        errors.append(
            f"full report requires at least {MIN_TABLES} auditable tables; "
            f"found {parser.counts['table']}"
        )
    if parser.counts["svg"] < MIN_SVGS:
        errors.append(
            f"full report requires at least {MIN_SVGS} inline charts; "
            f"found {parser.counts['svg']}"
        )
    if parser.counts["details"] < MIN_DETAILS:
        errors.append(
            f"full report requires at least {MIN_DETAILS} evidence drawers; "
            f"found {parser.counts['details']}"
        )

    required_terms = (
        "applicable",
        "unknown",
        "observed",
        "not_disclosed",
        "provisional",
        "needs_human_review",
    )
    missing_terms = [term for term in required_terms if term not in html]
    if missing_terms:
        errors.append(f"status legend is missing required terms: {missing_terms}")

    has_25_50_9 = (
        bool(re.search(r"25\s*(?:个|/|×|x)", html, flags=re.IGNORECASE))
        and bool(re.search(r"50\s*(?:个|/|×|x)", html, flags=re.IGNORECASE))
        and (
            "九道" in html
            or "9 / 9" in html
            or bool(re.search(r"25\s*[×x]\s*50\s*[×x]\s*9", html, flags=re.IGNORECASE))
        )
    )
    if not has_25_50_9:
        errors.append("HTML must visibly summarize 25 dimensions, 50 indicators and nine gates")

    try:
        crosswalk = json.loads(CROSSWALK_PATH.read_text(encoding="utf-8"))
        dimensions = crosswalk["dimensions"]
        required_indicator_ids = [
            indicator_id
            for dimension in dimensions
            for indicator_id in dimension["required_indicator_ids"]
        ]
        visible_dimension_results = sum(
            all(indicator_id in html for indicator_id in dimension["required_indicator_ids"])
            for dimension in dimensions
        )
        required_gate_ids = sorted(
            {
                gate_id
                for dimension in dimensions
                for gate_id in dimension["gate_ids"]
            }
        )
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load 25×50×9 implementation crosswalk: {exc}")
        required_indicator_ids = []
        required_gate_ids = []
        dimensions = []
        visible_dimension_results = 0

    missing_indicator_ids = [
        indicator_id for indicator_id in required_indicator_ids if indicator_id not in html
    ]
    if missing_indicator_ids:
        errors.append(
            "HTML does not expose all 50 required indicator-family results; "
            f"missing {missing_indicator_ids}"
        )
    missing_gate_ids = [gate_id for gate_id in required_gate_ids if gate_id not in html]
    if missing_gate_ids:
        errors.append(
            "HTML does not expose all nine gate results; "
            f"missing {missing_gate_ids}"
        )

    if "<!-- template-parity: viewport-qa-required -->" not in html:
        warnings.append(
            "rendered desktop and 390px viewport QA remains required before publication"
        )

    return {
        "schema_version": "seed.public-report-template-parity.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "path": path.name,
        "template_version": parser.template_version,
        "valid": not errors,
        "counts": parser.counts,
        "contract_counts": {
            "required_dimensions": len(dimensions),
            "visible_dimension_results": visible_dimension_results,
            "required_indicator_ids": len(required_indicator_ids),
            "visible_indicator_ids": len(required_indicator_ids)
            - len(missing_indicator_ids),
            "required_gate_ids": len(required_gate_ids),
            "visible_gate_ids": len(required_gate_ids) - len(missing_gate_ids),
        },
        "resolved_reader_jobs": resolved_groups,
        "missing_fragment_targets": missing_targets,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_html", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = validate_report_html(args.report_html)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
