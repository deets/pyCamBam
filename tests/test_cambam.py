from math import pi
import xml.etree.ElementTree as et
from cStringIO import StringIO

from cambam import CamBam

from .base import TestBase

class TestCamBam(TestBase):


    def assertXMLEqual(self, expected, actual, path=None):

        def textcompare(expected, actual):
            expected = "" if expected is None else expected
            actual = "" if actual is None else actual
            return [part for part in expected.split() if part] == [part for part in actual.split()]

        def toxml(el_or_s):
            if isinstance(el_or_s, et.Element):
                return el_or_s
            else:
                try:
                    return et.fromstring(el_or_s)
                except et.ParseError, e:
                    self.assertTrue(
                        False,
                        "Error reading XML %r, message: %s" % (el_or_s, e))

        expected = toxml(expected)
        actual = toxml(actual)
        if path is not None:
            actual = actual.find(path)
            self.assertTrue(actual is not None, "No elements found for path %s" % path)

        if not expected.tag == actual.tag:
            self.assertTrue(False, "<%s> != <%s>" % (expected.tag, actual.tag))

        self.assertTrue(textcompare(expected.text, actual.text))
        self.assertTrue(textcompare(expected.tail, actual.tail))

        expected_attrs = set(expected.attrib.keys())
        actual_attrs = set(actual.attrib.keys())
        self.assertEqual(expected_attrs, actual_attrs)

        for name in expected_attrs:
            self.assertEqual(
                expected.attrib[name],
                actual.attrib[name],
                )

        self.assertEqual(
            len(expected), len(actual),
            "expected:%r != actual:%r" % ([c.tag for c in expected], [c.tag for c in actual]))

        for ce, ae in zip(expected, actual):
            self.assertXMLEqual(ce, ae)


    def test_empty_file(self):
        cb = CamBam("the-name")
        out = StringIO()
        cb.write(out)
        content = out.getvalue()
        self.assertXMLEqual(
            """
        <CADFile xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Version="0.9.8.0" Name="the-name">
          <layers>
            <layer name="%(layername)s" color="255,255,255"><ModifcationCount>0</ModifcationCount>
              <objects/>
            </layer>
          </layers>
         <MachiningOptions>
          <FastPlungeHeight>-1</FastPlungeHeight>
          <Stock>
            <PMin>0,0,0</PMin>
            <PMax>100,100,10</PMax>
            <Color>255,165,0</Color>
          </Stock>
          <ToolProfile>Unspecified</ToolProfile>
          <MachiningOrigin>0,0</MachiningOrigin>
         </MachiningOptions>
        </CADFile>
        """ % dict(layername=cb.current_layer.name),
            content,
            )


    def test_add_circle(self):
        cb = CamBam("circle-test")
        cb.add_circle(d=5.0, c=[10.0, 11.0, 12.0])
        self.assertXMLEqual(
        """
        <circle id="1" d="5.0" c="10.0,11.0,12.0">
          <ModifcationCount>0</ModifcationCount>
          <mat m="Identity"/>
        </circle>
        """,
        cb.tostring(),
        "layers/layer/objects/circle",
        )


    def test_add_surface_from_stl(self):
        cb = CamBam("stl-test")
        cb.add_surface(self.datafilename("ascii.stl"))
        self.assertXMLEqual(
        """
        <surface id="1">
         <ModifcationCount>0</ModifcationCount>
         <mat m="Identity"/>
         <verts>
          <v>20.0,0.0,13.0</v>
          <v>20.0,-1.3,14.0</v>
          <v>20.0,-3.0,2.0</v>
         </verts>
         <faces>
          <f>0,1,2</f>
         </faces>
        </surface>
        """,
        cb.tostring(),
        "layers/layer/objects/surface",
        )


    def test_transformable_translation(self):
        cb = CamBam("stl-test")
        surface = cb.add_surface(self.datafilename("ascii.stl"))
        surface.translate(x=10)
        self.assertXMLEqual(
        """
        <mat m="1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 10.0 0.0 0.0 1.0"/>
        """,
        cb.tostring(),
        "layers/layer/objects/surface/mat",
        )


    def test_transformable_rotation(self):
        cb = CamBam("stl-test")
        surface = cb.add_surface(self.datafilename("ascii.stl"))
        surface.rotate(pi/2, (0, 0, 1))
        self.assertXMLEqual(
        """
        <mat m="0.0 -1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0"/>
        """,
        cb.tostring(),
        "layers/layer/objects/surface/mat",
        )


    def test_transformation_chaining(self):
        cb = CamBam("stl-test")
        surface = cb.add_surface(self.datafilename("ascii.stl"))
        surface.rotate(pi/2, (0, 0, 1)).translate(x=10).translate(y=20)
        self.assertXMLEqual(
        """
        <mat m="0.0 -1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 10.0 20.0 0.0 1.0"/>
        """,
        cb.tostring(),
        "layers/layer/objects/surface/mat",
        )


    def test_surfaces_bbox(self):
        cb = CamBam("stl-test")
        surface = cb.add_surface(self.datafilename("sphere.stl"))
        bbox = surface.bbox
        self.assertEqual(
            ((36.011, 35.3559, 5.0), (74.8331, 74.6439, 44.9999)),
            bbox,
            )
