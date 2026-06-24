import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_source_authority_import_proposals import (
    DEFAULT_CHECKLIST,
    DEFAULT_MARKDOWN,
    DEFAULT_PROPOSAL,
    DEFAULT_SOURCE_AUTHORITY,
    DEFAULT_SOURCE_REGISTRY,
    ROOT,
    validate,
)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


class SourceAuthorityImportProposalTests(unittest.TestCase):
    def test_current_usage_tables_proposal_passes(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["source_authority_status"], "not_imported")

    def test_proposal_with_approved_gate_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_source_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_PROPOSAL.read_text(encoding="utf-8"))
            proposal["required_level3_gate"]["approval_record"] = "approved"
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(
                proposal_path,
                markdown_path=DEFAULT_MARKDOWN,
                checklist_path=DEFAULT_CHECKLIST,
            )

        self.assertTrue(any("approval_record" in error for error in errors))

    def test_proposal_with_direct_import_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_source_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_PROPOSAL.read_text(encoding="utf-8"))
            proposal["required_level3_gate"]["direct_import"] = True
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(
                proposal_path,
                markdown_path=DEFAULT_MARKDOWN,
                checklist_path=DEFAULT_CHECKLIST,
            )

        self.assertTrue(any("direct_import" in error for error in errors))

    def test_imported_source_authority_status_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_source_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            authority = yaml.safe_load(DEFAULT_SOURCE_AUTHORITY.read_text(encoding="utf-8"))
            for source in authority["secondary_sources"]:
                if source["id"] == "hid_usage_tables":
                    source["status"] = "active"
            authority_path = temp / "source_authority.yaml"
            _write_yaml(authority_path, authority)

            errors, _receipt = validate(
                DEFAULT_PROPOSAL,
                markdown_path=DEFAULT_MARKDOWN,
                checklist_path=DEFAULT_CHECKLIST,
                source_authority_path=authority_path,
            )

        self.assertTrue(any("status must remain not_imported" in error for error in errors))

    def test_registry_sections_present_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_source_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            registry = yaml.safe_load(DEFAULT_SOURCE_REGISTRY.read_text(encoding="utf-8"))
            for source in registry["sources"]:
                if source["source_id"] == "hid_usage_tables":
                    source["sections"] = ["1"]
            registry_path = temp / "source_registry.yaml"
            _write_yaml(registry_path, registry)

            errors, _receipt = validate(
                DEFAULT_PROPOSAL,
                markdown_path=DEFAULT_MARKDOWN,
                checklist_path=DEFAULT_CHECKLIST,
                source_registry_path=registry_path,
            )

        self.assertTrue(any("registry sections must remain empty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
