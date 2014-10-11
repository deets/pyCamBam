import xml.etree.ElementTree as et

from .stl import StlReader
from .util import BBox

from .base import (
    Identifiable,
    Transformable,
    Modifiable,
    Point,
    Color,
    )

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
