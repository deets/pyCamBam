from cambam import Matrix

from unittest import TestCase


class TestMatrix(TestCase):


    def test_identity(self):
        m = Matrix()
        self.assertEqual(
            "Identity",
            str(m),
            )
