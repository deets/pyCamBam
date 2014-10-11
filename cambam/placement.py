from math import sqrt, ceil
from .util import BBox
from .base import Matrix


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
