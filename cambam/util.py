# used to compare floats
EPSILON = 1E-15


def veceq(a, b):
    return all(abs(ac - bc) <= EPSILON for ac, bc in zip(a, b))


class BBox(object):

    def __init__(self, pmin, pmax):
        self.pmin, self.pmax = pmin, pmax


    @property
    def width(self):
        return self.pmax[0] - self.pmin[0]


    @property
    def length(self):
        return self.pmax[1] - self.pmin[1]


    @property
    def height(self):
        return self.pmax[2] - self.pmin[2]


    @property
    def center(self):
        return (
            (self.pmin[0] + self.pmax[0]) / 2.0,
            (self.pmin[1] + self.pmax[1]) / 2.0,
            (self.pmin[2] + self.pmax[2]) / 2.0,
            )


    def pad(self, padding=None, x=0, y=0, z=0):
        if padding is not None:
            xpadding = ypadding = zpadding = padding
        else:
            xpadding, ypadding, zpadding = x, y, z

        return BBox(
            (self.pmin[0] - xpadding, self.pmin[1] - ypadding, self.pmin[2] - zpadding),
            (self.pmax[0] + xpadding, self.pmax[1] + ypadding, self.pmax[2] + zpadding),
            )


    def __getitem__(self, index):
        return (self.pmin, self.pmax)[index]


    def __repr__(self):
        return "<%s %r %r>" % (
            self.__class__.__name__,
            self.pmin, self.pmax,
            )


    def __eq__(self, other):
        return veceq(self.pmin, other.pmin) and veceq(self.pmax, other.pmax)
