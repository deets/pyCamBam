import unittest

from cambam.util import BBox


class TestUtils(unittest.TestCase):


    def test_bbox_dimensions(self):
        bbox = BBox((0, 0, 0), (10, 20, 30))
        self.assertEqual(10, bbox.width)
        self.assertEqual(20, bbox.length)
        self.assertEqual(30, bbox.height)
