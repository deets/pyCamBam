

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
