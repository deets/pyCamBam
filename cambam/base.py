from itertools import count
import xml.etree.ElementTree as et

from .matrix import Matrix

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


class Circle(Transformable, Modifiable):

    TAG = "circle"

    CIRCLE_ID_GEN = count(1)

    def __init__(self, d, c, *a, **k):
        super(Circle, self).__init__(*a, **k)
        self.d, self.c = d, Point(c)
        self.id = self.CIRCLE_ID_GEN.next()


    def add_details(self, tag):
        super(Circle, self).add_details(tag)
        tag.attrib["c"] = str(self.c)
        tag.attrib["d"] = str(self.d)
        tag.attrib["id"] = str(self.id)


class Layer(Modifiable):

    TAG = "layer"

    LAYER_COUNT = count()

    def __init__(self, name=None, *a, **k):
        super(Layer, self).__init__(*a, **k)
        if name is None:
            name = "layer_%i" % self.LAYER_COUNT.next()
        self.name = name
        self.color = Color(255, 255, 255)
        self._objects = []


    def add_details(self, tag):
        super(Layer, self).add_details(tag)
        tag.attrib["name"] = self.name
        tag.attrib["color"] = str(self.color)

        objects = et.Element("objects")
        for obj in self._objects:
            obj.serialize(objects)

        tag.append(objects)


    def add_circle(self, d, c):
        self._objects.append(Circle(d=d, c=c))


class CamBam(object):

    VERSION = "0.9.8.0"

    def __init__(self, name):
        self.name = name
        self.current_layer = Layer()
        self._layers = [self.current_layer]


    def write(self, file_):
        file_.write(self.tostring())


    def tostring(self):
        cadfile = et.Element('CADFile')
        cadfile.attrib["Name"] = self.name
        cadfile.attrib["Version"] = self.VERSION
        layers = et.Element("layers")
        for layer in self._layers:
            layer.serialize(layers)
        cadfile.append(layers)
        return et.tostring(cadfile)


    def add_circle(self, d, c):
        self.current_layer.add_circle(d=d, c=c)
