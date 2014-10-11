import xml.etree.ElementTree as et

from .base import Object, Color

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
