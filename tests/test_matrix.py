from math import pi
from cambam import Matrix, quaternion

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


    def test_vector_application(self):
        m = Matrix()
        m.translate(x=10.0)
        self.assertEqual((10, 0, 0), m.apply((0, 0, 0)))


    def test_rotation(self):
        q = quaternion.rotation(pi/2, (0, 0, 1))
        m = Matrix.from_quaternion(q)

        def vector_equal(expected, actual, e=10e-14):
            if not len(expected) == len(actual):
                return False
            return all(abs(a-b) <= e for a, b in zip(expected, actual))

        self.assertTrue(
            vector_equal((0, -1, 0), m.apply((1, 0, 0)))
            )


    def test_normalization(self):
        q = quaternion.rotation(pi/2, (0, 0, 1))
        m = Matrix.from_quaternion(q).normalized()
        self.assertEqual(0, m[0][0])


    def test_outer_multiplication(self):
        a = Matrix()
        a.translate(x=10)
        b = Matrix()
        b.translate(y=20)
        c = a * b
        self.assertEqual([10.0, 0.0, 0, 1.0], a[3])
        self.assertEqual([0.0, 20.0, 0, 1.0], b[3])
        self.assertEqual([10.0, 20.0, 0, 1.0], c[3])
