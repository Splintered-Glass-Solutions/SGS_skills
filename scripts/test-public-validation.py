#!/usr/bin/env python3
"""Regression checks for publication leaks; uses synthetic fixture values only."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("public_validation", Path(__file__).with_name("validate-public-library.py"))
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class PublicationGateTests(unittest.TestCase):
    def rules(self, value):
        return {rule for _, rule in gate.scan_text(value, {"docs.python.org"})}

    def test_private_bindings_are_rejected(self):
        fixtures = {
            "/" + "Users/fixture-owner/project": "personal-home-path",
            "owner@" + "private-fixture.org": "non-example-email",
            "example-" + "project-42": "numbered-private-project-copy",
            "arn:aws:iam::" + "123456789012:user/fixture": "live-provider-id",
            "https://" + "private-fixture.org/path": "unreviewed-public-host",
            "AKIA" + "A" * 16: "provider-credential",
            "12345678-1234-" + "1234-1234-123456789abc": "non-example-resource-id",
        }
        for value, expected in fixtures.items():
            with self.subTest(rule=expected):
                self.assertIn(expected, self.rules(value))

    def test_safe_examples_and_documentation_are_accepted(self):
        for value in ["user@example.com", "<project-root>/src", "https://app.example.com/qa", "https://docs.python.org/3/", "GET /users/{id}", "http://localhost:3000"]:
            with self.subTest(value=value):
                self.assertEqual(set(), self.rules(value))

    def test_diagnostics_use_rule_names_not_secret_values(self):
        value = "sk-" + "a" * 40
        self.assertEqual([(1, "provider-credential")], gate.scan_text(value, set()))


class TimeTrackingPortabilityTests(unittest.TestCase):
    def test_explicit_time_and_timezone_do_not_collide_and_import_is_idempotent(self):
        helper = Path(__file__).resolve().parents[1] / "skills/local-time-tracking/scripts/log_time.py"
        with tempfile.TemporaryDirectory() as folder:
            args = ["python3", str(helper), "--project-root", folder,
                    "--project", "sample-project", "--timezone", "Pacific/Honolulu",
                    "--date", "2026-10-01", "--time", "09:15", "--minutes", "30",
                    "--description", "Synthetic validation", "--source-id", "fixture-entry"]
            for _ in range(2):
                subprocess.run(args, check=True, capture_output=True, text=True)
            lines = (Path(folder) / ".codex/time_tracking.jsonl").read_text().splitlines()
            self.assertEqual(1, len(lines))
            record = json.loads(lines[0])
            self.assertEqual(("09:15", "Pacific/Honolulu", 30),
                             (record["time"], record["timezone"], record["minutes"]))


if __name__ == "__main__":
    unittest.main()
