#
import os
import unittest

class TestBase(unittest.TestCase):


    @classmethod
    def datafilename(cls, name):
        fname = os.path.join(
            os.path.dirname(__file__),
            "data",
            name,
            )
        assert os.path.exists(fname)
        return fname
