from math import cos, sin

# used to compare floats
EPSILON = 1E-15

class Matrix(object):

    @classmethod
    def _identity_rowcols(cls):
        return [[1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]]


    def __init__(self, rowcols=None):
        if rowcols is None:
            self.reset()
        else:
            self._rowcols = rowcols
            self._identity = False


    def reset(self):
        self._rowcols = self._identity_rowcols()
        self._identity = True


    def translate(self, x=0.0, y=0.0, z=0.0):
        m = Matrix()
        m._rowcols[3][:3] = [x, y, z]
        self *= m


    def __imul__(self, other):
        rc = self._identity_rowcols()
        mrc = self._rowcols
        orc = other._rowcols
        for i in xrange(4):
            for j in xrange(4):
                rc[i][j] = sum(mrc[i][k] * orc[k][j] for k in xrange(4))

        self._rowcols = rc
        self._identity = False
        return self


    def __str__(self):
        if self._identity:
            return "Identity"
        rc = self.normalized()._rowcols
        return " ".join(str(rc[i][j]) for i in xrange(4) for j in xrange(4))


    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self._rowcols)


    def __eq__(self, other):
        # TODO: needs epsilon-comparison
        return self._identity == other._identity and \
          self._rowcols == other._rowcols


    @classmethod
    def from_quaternion(cls, q):
        w, x, y, z = q
        return cls([
            [w**2+x**2-y**2-z**2, 2*x*y-2*w*z, 2*x*z+2*w*y, 0],
            [2*x*y+2*w*z, w**2-x**2+y**2-z**2, 2*y*z+2*w*x, 0],
            [2*x*z-2*w*y, 2*y*z-2*w*x, w**2-x**2-y**2+z**2, 0],
            [0.0, 0.0, 0.0, 1.0]])


    def apply(self, v):
        res = [0] * 4
        vt = (v[0], v[1], v[2], 1.0) if len(v) == 3 else v
        for i in xrange(4):
            res[i] = sum(vt[j] * self._rowcols[j][i] for j in xrange(4))
        return tuple(res[:len(v)])


    def __getitem__(self, index):
        return self._rowcols[index]


    def normalized(self):
        """
        Normalizes matrix-values to 0/1 if they are within the EPSILON range
        """
        res = self.__class__()
        for i in xrange(4):
            for j in xrange(4):
                v = self[i][j]
                if abs(v) <= EPSILON:
                    v = 0.0
                elif abs(1 - v) <= EPSILON:
                    v = 1.0
                res[i][j] = v
        return res


class quaternion(object):

    def __init__(self, w, x, y, z):
        self.w, self.x, self.y, self.z = w, x, y, z


    @classmethod
    def rotation(cls, angle, (dx, dy, dz)):
        w  = cos(angle / 2)
        x = dx * sin(angle / 2 )
        y = dy * sin(angle / 2 )
        z = dz * sin(angle / 2 )
        return cls(w, x, y, z)


    def __getitem__(self, index):
        return [self.w, self.x, self.y, self.z][index]
