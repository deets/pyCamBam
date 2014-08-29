#
import os
import unittest
from cambam.stl import StlReader

class TestStlReading(unittest.TestCase):


    @classmethod
    def datafilename(cls, name):
        fname = os.path.join(
            os.path.dirname(__file__),
            "data",
            name,
            )
        assert os.path.exists(fname)
        return fname


    def test_ascii_stl_reading(self):
        self.assertEqual(
            [[[20.0, 0.0, 13.0], [20.0, -1.3, 14.], [20.0, -3.0, 2.0]]],
            StlReader.read(self.datafilename("ascii.stl")),
            )
