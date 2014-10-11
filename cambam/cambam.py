import xml.etree.ElementTree as et

from itertools import count

from .objects import Layer
from .machining import Stock

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
