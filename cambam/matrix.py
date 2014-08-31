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
        rc = self._rowcols
        return " ".join(str(rc[i][j]) for i in xrange(4) for j in xrange(4))


    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self._rowcols)


    def __eq__(self, other):
        return self._identity == other._identity and \
          self._rowcols == other._rowcols
