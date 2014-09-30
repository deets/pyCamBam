from cambam import BBox, grid
import unittest

class TestPlacemont(unittest.TestCase):


    def test_grid_placement_exact(self):
        bboxes = [BBox((-5.0, -5.0, 0), (5.0, 5.0, 0)) for _ in xrange(9)]
        stock, placements = grid(bboxes)
        self.assertEqual(9, len(placements))
        self.assertEqual(
            [
                (5.0, 5.0), (5.0, 15.0), (5.0, 25.0),
                (15.0, 5.0), (15.0, 15.0), (15.0, 25.0),
                (25.0, 5.0), (25.0, 15.0), (25.0, 25.0)],
            [tuple(p.apply((0, 0, 0))[:2]) for p in placements],
            )
        self.assertEqual(
            BBox((0, 0, 0), (30.0, 30.0, 0)),
            stock,
            )
