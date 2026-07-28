from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-buffett-munger-company"


def _run_json(*args: str | Path) -> dict:
    result = subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["errors"] == []
    return payload


def test_crosswalk_uses_skill_relative_paths() -> None:
    crosswalk = json.loads(
        (SKILL / "references" / "methodology-implementation-crosswalk.json").read_text(
            encoding="utf-8"
        )
    )

    assert crosswalk["methodology_ledger"]["path"] == ("references/methodology-source-ledger.json")
    assert crosswalk["company_contract"]["implementation"] == (
        "scripts/company_research_validation.py"
    )


def test_installed_skill_validates_outside_repository(tmp_path: Path) -> None:
    installed_skill = tmp_path / "research-buffett-munger-company"
    shutil.copytree(SKILL, installed_skill)

    references = installed_skill / "references"
    scripts = installed_skill / "scripts"

    ledger_result = _run_json(
        scripts / "validate_methodology_source_ledger.py",
        references / "methodology-source-ledger.json",
    )
    crosswalk_result = _run_json(
        scripts / "validate_methodology_implementation_crosswalk.py",
        references / "methodology-implementation-crosswalk.json",
    )

    assert ledger_result["official_sources"] == 22
    assert ledger_result["method_claims"] == 22
    assert crosswalk_result["dimension_count"] == 25
    assert crosswalk_result["required_indicator_count"] == 50
