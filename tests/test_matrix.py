from cambam import Matrix

from unittest import TestCase


class TestMatrix(TestCase):


    def test_identity(self):
        m = Matrix()
        self.assertEqual(
            "Identity",
            str(m),
            )


    def test_translation(self):
        m = Matrix()
        m.translate(x=10.0, y=2.0, z=3.0)
        self.assertEqual(
            Matrix([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [10.0, 2.0, 3.0, 1.0],
                    ]),
            m,
        )


    def test_multiple_translation(self):
        m = Matrix()
        m.translate(x=10.0)
        m.translate(y=2.0)
        m.translate(z=3.0)
        self.assertEqual(
            Matrix([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [10.0, 2.0, 3.0, 1.0],
                    ]),
            m,
        )


    def test_serialization(self):
        m = Matrix()
        m.translate(x=10.0)
        self.assertEquals(
            "1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 10.0 0.0 0.0 1.0",
            str(m),
            )
