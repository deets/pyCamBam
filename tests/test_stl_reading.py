#
from cambam.stl import StlReader

from .base import TestBase


class TestStlReading(TestBase):


    def test_ascii_stl_reading(self):
        self.assertEqual(
            [[[20.0, 0.0, 13.0], [20.0, -1.3, 14.], [20.0, -3.0, 2.0]]],
            StlReader.read(self.datafilename("ascii.stl")),
            )
