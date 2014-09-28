from itertools import count
import xml.etree.ElementTree as et

from .matrix import Matrix, quaternion
from .stl import StlReader
from .util import BBox


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


class Circle(Identifiable, Transformable, Modifiable):

    TAG = "circle"

    def __init__(self, d, c, *a, **k):
        super(Circle, self).__init__(*a, **k)
        self.d, self.c = d, Point(c)


    def add_details(self, tag):
        super(Circle, self).add_details(tag)
        tag.attrib["c"] = str(self.c)
        tag.attrib["d"] = str(self.d)


class Surface(Identifiable, Transformable, Modifiable):

    TAG = "surface"

    def __init__(self, filename, *a, **k):
        super(Surface, self).__init__(*a, **k)
        self._faces = StlReader.read(filename)
        self._bbox = None


    def add_details(self, tag):
        super(Surface, self).add_details(tag)
        vertices = []
        faces = []
        for i, stl_face in enumerate(self._faces):
            vertices.extend(stl_face)
            faces.append((i*3, i*3 + 1, i*3 + 2))

        verts = et.Element("verts")
        tag.append(verts)

        for vertex in vertices:
            v = et.Element("v")
            v.text = ",".join(str(c) for c in vertex)
            verts.append(v)

        faces_tag = et.Element("faces")
        tag.append(faces_tag)
        for face in faces:
            f = et.Element("f")
            f.text = ",".join(str(c) for c in face)
            faces_tag.append(f)


    @property
    def bbox(self):
        if self._bbox is None:
            minx = min(vertex[0]
                       for face in self._faces
                       for vertex in face)
            miny = min(vertex[1]
                       for face in self._faces
                       for vertex in face)
            minz = min(vertex[2]
                       for face in self._faces
                       for vertex in face)
            maxx = max(vertex[0]
                       for face in self._faces
                       for vertex in face)
            maxy = max(vertex[1]
                       for face in self._faces
                       for vertex in face)
            maxz = max(vertex[2]
                       for face in self._faces
                       for vertex in face)
            self._bbox = BBox((minx, miny, minz), (maxx, maxy, maxz))
        return self._bbox


class Layer(Modifiable):

    TAG = "layer"

    def __init__(self, name=None, layer_count=None, id_gen=None, *a, **k):
        super(Layer, self).__init__(*a, **k)
        if name is None:
            name = "layer_%i" % layer_count.next()
        self.name = name
        self.color = Color(255, 255, 255)
        self._objects = []
        self._id_gen = id_gen


    def add_details(self, tag):
        super(Layer, self).add_details(tag)
        tag.attrib["name"] = self.name
        tag.attrib["color"] = str(self.color)

        objects = et.Element("objects")
        for obj in self._objects:
            obj.serialize(objects)

        tag.append(objects)


    def add_circle(self, d, c):
        self._objects.append(Circle(d=d, c=c, id_gen=self._id_gen))


    def add_surface(self, filename):
        surface = Surface(filename, id_gen=self._id_gen)
        self._objects.append(surface)
        return surface


class Stock(Object):

    TAG = "Stock"

    def __init__(self):
        self.pmin = (0, 0, 0)
        self.pmax = (100, 100, 10)
        self.color = Color(255, 165, 0)


    def add_details(self, tag):
        pminel = et.Element("PMin")
        pminel.text = ",".join(str(p) for p in self.pmin)
        pmaxel = et.Element("PMax")
        pmaxel.text = ",".join(str(p) for p in self.pmax)
        colorel = et.Element("Color")
        colorel.text = str(self.color)
        tag.append(pminel)
        tag.append(pmaxel)
        tag.append(colorel)


class CamBam(object):

    VERSION = "0.9.8.0"

    def __init__(self, name, fast_plunge_height=-1):
        self.name = name
        self.fast_plunge_height = fast_plunge_height
        self.stock = Stock()
        self._layer_count = count()
        self._object_count = count(1)
        self.current_layer = Layer(layer_count=self._layer_count, id_gen=self._object_count)
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
        cadfile.append(self._machining_options())
        return et.tostring(cadfile)


    def add_circle(self, d, c):
        self.current_layer.add_circle(d=d, c=c)


    def add_surface(self, filename):
        return self.current_layer.add_surface(filename)


    def _machining_options(self):
        moel = et.Element("MachiningOptions")
        fph = et.Element("FastPlungeHeight")
        fph.text = str(self.fast_plunge_height)
        tph = et.Element("ToolProfile")
        tph.text = "Unspecified"
        mo = et.Element("MachiningOrigin")
        mo.text = "0,0"

        moel.append(fph)
        self.stock.serialize(moel)
        moel.append(tph)
        moel.append(mo)

        return moel
