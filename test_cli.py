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
