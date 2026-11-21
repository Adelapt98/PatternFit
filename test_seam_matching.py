import unittest

from seam_matching import seam_boundaries


class BoundaryTests(unittest.TestCase):
    def test_reversed_seam_uses_sewing_order_and_distances(self):
        notches = [{"id": "A", "distance_mm": 20}, {"id": "B", "distance_mm": 70}]
        self.assertEqual(
            seam_boundaries(notches, 100, reverse=True),
            [("start", 0), ("B", 30), ("A", 80), ("end", 100)],
        )

    def test_rejects_duplicate_and_out_of_order_notches(self):
        first = {"id": "A", "distance_mm": 20}
        for second in ({"id": "A", "distance_mm": 30}, {"id": "B", "distance_mm": 10}):
            with self.subTest(second=second), self.assertRaises(ValueError):
                seam_boundaries([first, second], 100)
