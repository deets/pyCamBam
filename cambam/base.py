import xml.etree.ElementTree as et

from .matrix import Matrix, quaternion


class Color(object):

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b


    def __str__(self):
        return "%i,%i,%i" % (self.r, self.g, self.b)


    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self))


class Point(object):

    def __init__(self, coords):
        self.coords = coords


    def __str__(self):
        return ",".join(str(c) for c in self.coords)


class Object(object):

    TAG = None

    def serialize(self, parent):
        assert self.TAG, "<%s> needs a TAG definition" % self.__class__.__name__
        tag = et.Element(self.TAG)
        self.add_details(tag)
        parent.append(tag)
        return tag


    def add_details(self, tag):
        pass


class Identifiable(Object):


    def __init__(self, id_gen, *a, **k):
        super(Identifiable, self).__init__(*a, **k)
        self.id = id_gen.next()


    def add_details(self, tag):
        super(Identifiable, self).add_details(tag)
        tag.attrib["id"] = str(self.id)


class Modifiable(Object):

    def __init__(self, *a, **k):
        super(Modifiable, self).__init__(*a, **k)
        self.mod_count = 0


    def add_details(self, tag):
        super(Modifiable, self).add_details(tag)
        mc = et.Element("ModifcationCount")
        mc.text = str(self.mod_count)
        tag.append(mc)


class Transformable(Object):

    def __init__(self, *a, **k):
        super(Transformable, self).__init__(*a, **k)
        self.matrix = Matrix()


    def add_details(self, tag):
        super(Transformable, self).add_details(tag)
        mat = et.Element("mat")
        mat.attrib["m"] = str(self.matrix)
        tag.append(mat)


    def translate(self, x=0, y=0, z=0):
        m = Matrix()
        m.translate(x=x, y=y, z=z)
        self.matrix *= m
        return self


    def rotate(self, angle, axis):
        q = quaternion.rotation(angle, axis)
        m = Matrix.from_quaternion(q)
        self.matrix *= m
        return self
