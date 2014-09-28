

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
