from math import sqrt, ceil
from cambam import BBox, Matrix
import unittest


def grid(bboxes):
    max_width = max(bbox.width for bbox in bboxes)
    max_length = max(bbox.length for bbox in bboxes)
    max_height = max(bbox.height for bbox in bboxes)
    xcount = int(ceil(sqrt(len(bboxes))))
    ycount, rest = divmod(len(bboxes), xcount)
    if rest:
        ycount += 1

    centers = [((x + .5) * max_width, (y + .5) * max_length)
               for x in xrange(xcount)
               for y in xrange(ycount)]

    res = []
    for center, bbox in zip(centers, bboxes):
        m = Matrix()
        old = bbox.center
        m.translate(x=center[0] - old[0], y=center[1] - old[1])
        res.append(m)
    stock = BBox(
        (0, 0, 0),
        (xcount * max_width, ycount * max_length, max_height),
        )
    return stock, res


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
