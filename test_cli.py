import subprocess
import sys
import unittest
from pathlib import Path


class CommandTests(unittest.TestCase):
    def test_notched_fixture_reports_residual_with_equal_total_lengths(self):
        repo = Path(__file__).resolve().parent
        result = subprocess.run(
            [sys.executable, "patternfit.py", "examples/notched.json"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("start → shoulder: 40.00 / 50.00 mm, ease +10.00 mm, residual +0.00 mm (OK)", result.stdout)
        self.assertIn("shoulder → end: 60.00 / 50.00 mm, ease +0.00 mm, residual -10.00 mm (Outside tolerance)", result.stdout)

    def test_additional_notch_examples(self):
        repo = Path(__file__).resolve().parent
        cases = [
            ("notched-with-ease.json", 0, "Within tolerance"),
            ("notched-missing-counterpart.json", 2, "same notch IDs"),
        ]
        for fixture, exit_code, message in cases:
            with self.subTest(fixture=fixture):
                result = subprocess.run(
                    [sys.executable, "patternfit.py", f"examples/{fixture}"],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, exit_code, result.stderr)
                self.assertIn(message, result.stdout + result.stderr)
