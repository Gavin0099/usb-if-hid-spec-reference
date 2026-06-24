import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_usage_tables_matrix_proposals import (
    DEFAULT_MARKDOWN,
    DEFAULT_USAGE_ID_MARKDOWN,
    DEFAULT_USAGE_ID_PROPOSAL,
    DEFAULT_PROPOSAL,
    DEFAULT_SOURCE_AUTHORITY,
    ROOT,
    validate,
)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


class UsageTablesMatrixProposalTests(unittest.TestCase):
    def test_current_usage_page_identity_proposal_passes(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertFalse(receipt["future_matrix_exists"])

    def test_current_usage_id_identity_proposal_passes(self) -> None:
        errors, receipt = validate(
            proposal_path=DEFAULT_USAGE_ID_PROPOSAL,
            markdown_path=DEFAULT_USAGE_ID_MARKDOWN,
        )
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertFalse(receipt["future_matrix_exists"])

    def test_matrix_created_flag_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_usage_matrix_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_PROPOSAL.read_text(encoding="utf-8"))
            proposal["matrix_created"] = True
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(proposal_path, markdown_path=DEFAULT_MARKDOWN)

        self.assertTrue(any("matrix_created must be false" in error for error in errors))

    def test_verified_uplift_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_usage_matrix_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_PROPOSAL.read_text(encoding="utf-8"))
            proposal["verified_uplift"] = True
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(proposal_path, markdown_path=DEFAULT_MARKDOWN)

        self.assertTrue(any("verified_uplift must be false" in error for error in errors))

    def test_missing_schema_field_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_usage_matrix_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_PROPOSAL.read_text(encoding="utf-8"))
            proposal["proposed_schema_fields"].remove("source_section")
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(proposal_path, markdown_path=DEFAULT_MARKDOWN)

        self.assertTrue(any("source_section" in error for error in errors))

    def test_missing_usage_id_field_in_usage_id_matrix_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_usage_matrix_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            proposal = json.loads(DEFAULT_USAGE_ID_PROPOSAL.read_text(encoding="utf-8"))
            proposal["proposed_schema_fields"].remove("usage_id_name")
            proposal_path = temp / "proposal.json"
            _write_json(proposal_path, proposal)

            errors, _receipt = validate(
                proposal_path,
                markdown_path=DEFAULT_USAGE_ID_MARKDOWN,
            )

        self.assertTrue(any("usage_id_name" in error for error in errors))

    def test_imported_source_authority_status_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tmp_usage_matrix_proposal_", dir=ROOT) as tempdir:
            temp = Path(tempdir)
            authority = yaml.safe_load(DEFAULT_SOURCE_AUTHORITY.read_text(encoding="utf-8"))
            for source in authority["secondary_sources"]:
                if source["id"] == "hid_usage_tables":
                    source["status"] = "active"
            authority_path = temp / "source_authority.yaml"
            _write_yaml(authority_path, authority)

            errors, _receipt = validate(DEFAULT_PROPOSAL, markdown_path=DEFAULT_MARKDOWN, source_authority_path=authority_path)

        self.assertTrue(any("status must remain not_imported" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
