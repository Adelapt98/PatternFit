import math
import unittest

from patternfit import seam_length


class SeamLengthTests(unittest.TestCase):
    def test_original_fixture_format(self):
        self.assertEqual(seam_length({"start": [0, 0], "end": [3, 4]}), 5)

    def test_curve_plus_line_matches_analytic_length_in_either_direction(self):
        # The curve has x(t) = 100t and y(t) = 100t² for 0 <= t <= 1.
        expected = 25 * (2 * math.sqrt(5) + math.asinh(2)) + 20
        curve = {"kind": "quadratic", "control": [50, 0], "end": [100, 100]}
        forward = {
            "start": [0, 0],
            "segments": [curve, {"kind": "line", "end": [100, 120]}],
        }
        reverse = {
            "start": [100, 120],
            "segments": [
                {"kind": "line", "end": [100, 100]},
                {**curve, "end": [0, 0]},
            ],
        }
        for path in (forward, reverse):
            with self.subTest(path=path):
                self.assertAlmostEqual(seam_length(path), expected, delta=0.0001)

    def test_invalid_segment_kind(self):
        with self.assertRaisesRegex(ValueError, "unknown segment kind"):
            seam_length({
                "start": [0, 0],
                "segments": [{"kind": "arc", "end": [10, 10]}],
            })


if __name__ == "__main__":
    unittest.main()
