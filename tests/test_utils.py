import unittest

from cambam.util import BBox


class TestUtils(unittest.TestCase):


    def test_bbox_dimensions(self):
        bbox = BBox((0, 0, 0), (10, 20, 30))
        self.assertEqual(10, bbox.width)
        self.assertEqual(20, bbox.length)
        self.assertEqual(30, bbox.height)


    def test_bbox_padding(self):
        bbox = BBox((0, 0, 0), (10, 20, 30))
        bbox = bbox.pad(5)
        self.assertEqual(20, bbox.width)
        self.assertEqual(30, bbox.length)
        self.assertEqual(40, bbox.height)


    def test_bbox_component_wise_padding(self):
        bbox = BBox((0, 0, 0), (10, 20, 30))
        bbox = bbox.pad(x=5, y=10, z=20)
        self.assertEqual(20, bbox.width)
        self.assertEqual(40, bbox.length)
        self.assertEqual(70, bbox.height)


    def test_bbox_tuple_like_access(self):
        bbox = BBox((0, 0, 0), (10, 20, 30))
        self.assertEqual((0, 0, 0), bbox[0])
        self.assertEqual((10, 20, 30), bbox[1])
