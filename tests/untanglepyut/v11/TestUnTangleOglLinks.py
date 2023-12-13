from typing import Dict
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutClass import PyutClass

from ogl.OglLink import OglLink

from untangle import Element
from untangle import parse

from miniogl.AnchorPoint import AnchorPoint
from miniogl.AttachmentSide import AttachmentSide
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglClass import OglClass

from untanglepyut.Types import LinkableOglObjects
from untanglepyut.Types import UntangledLink
from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglLinks

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.UnTangleOglClasses import UnTangleOglClasses
from untanglepyut.UnTangleOglLinks import UnTangleOglLinks

from tests.ProjectTestBase import TestBase

V11_OGL_INTERFACE2_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="Simple Interface Diagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <OglClass width="150" height="75" x="100" y="75">
        <PyutClass id="1" name="Implementor" stereotype="noStereotype" filename="" description="" displayMethods="True" displayStereotype="True" displayFields="True" displayParameters="Unspecified"/>
    </OglClass>
    <OglInterface2 attachmentPoint="EAST" x="250" y="112">
        <PyutInterface id="2" name="IClassInterface" description="">
            <PyutMethod name="MethodWithParameters" visibility="PUBLIC" returnType="">
                <PyutParameter name="strParam"  type="str"  defaultValue=""/>
                <PyutParameter name="intParam"  type="int"  defaultValue="1"/>
                <PyutParameter name="floatParam" type="float" defaultValue="1.0"/>
                <SourceCode/>
            </PyutMethod>
            <Implementor implementingClassName="Implementor"/>
        </PyutInterface>
    </OglInterface2>
</PyutDocument>
"""

V11_OGL_LINKS: str = """
<PyutDocument type="CLASS_DIAGRAM" title="MultiLink" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <OglClass width="78" height="44" x="150" y="150">
        <PyutClass id="1" name="Folder" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="">
            <PyutField name="permissions" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
    <OglClass width="88" height="50" x="151" y="302">
        <PyutClass id="2" name="File" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="">
            <PyutField name="size" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="name" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
    <OglClass width="129" height="70" x="517" y="125">
        <PyutClass id="3" name="Car" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="">
            <PyutField name="make" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="model" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="vin" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="modelYear" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
    <OglClass width="81" height="50" x="525" y="300">
        <PyutClass id="4" name="Wheel" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="">
            <PyutField name="size" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="width" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
    <OglClass width="172" height="75" x="850" y="175">
        <PyutClass id="5" name="Interface" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="">
            <PyutMethod name="floatMethod" visibility="PUBLIC" returnType="float">
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="intMethod" visibility="PUBLIC" returnType="int">
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="stringMethod" visibility="PUBLIC" returnType="str">
                <SourceCode />
            </PyutMethod>
        </PyutClass>
    </OglClass>
    <OglClass width="99" height="44" x="875" y="350">
        <PyutClass id="6" name="Implementor" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="" />
    </OglClass>
    <OglClass width="140" height="48" x="325" y="625">
        <PyutClass id="7" name="LollipopImplementor" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="" />
    </OglClass>
    <OglLink sourceAnchorX="186" sourceAnchorY="193" destinationAnchorX="187" destinationAnchorY="302" spline="False">
        <LabelCenter x="401" y="-8" />
        <LabelSource x="0" y="-53" />
        <LabelDestination x="0" y="-53" />
        <PyutLink name="organizes" type="COMPOSITION" cardinalitySource="1" cardinalityDestination="*" bidirectional="False" sourceId="1" destinationId="2" />
    </OglLink>
    <OglLink sourceAnchorX="573" sourceAnchorY="194" destinationAnchorX="573" destinationAnchorY="300" spline="False">
        <LabelCenter x="-371" y="-8" />
        <LabelSource x="0" y="-53" />
        <LabelDestination x="0" y="-53" />
        <PyutLink name="has" type="AGGREGATION" cardinalitySource="1" cardinalityDestination="4" bidirectional="False" sourceId="3" destinationId="4" />
    </OglLink>
    <OglLink sourceAnchorX="924" sourceAnchorY="350" destinationAnchorX="924" destinationAnchorY="249" spline="False">
        <PyutLink name="" type="INTERFACE" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="5" destinationId="6" />
    </OglLink>
    <OglInterface2 attachmentPoint="EAST" x="465" y="649">
        <PyutInterface id="7" name="IClassInterface" description="">
            <PyutMethod name="methodWithParameters" visibility="PUBLIC" returnType="">
                <SourceCode />
                <PyutParameter name="strParam" type="str" defaultValue="''" />
                <PyutParameter name="intParam" type="int" defaultValue="1" />
                <PyutParameter name="floatParam" type="float" defaultValue="1.0" />
            </PyutMethod>
            <Implementor implementingClassName="LollipopImplementor" />
        </PyutInterface>
    </OglInterface2>
    <OglText width="221" height="73" x="500" y="400">
        <PyutNote id="8" content="Aggregation associates two objects describes the 'have a' relationship." />
    </OglText>
    <OglText width="206" height="74" x="125" y="400">
        <PyutNote id="9" content="Composition is a specific type of Aggregation which implies ownership." />
    </OglText>
</PyutDocument>
"""

TEST_LINK_NAME: str = 'has'


class TestUnTangleOglLinks(TestBase):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated:  05 September 2023
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testStandardLinks(self):
        root:             Element = parse(V11_OGL_LINKS)
        oglLinksDocument: Element = root.PyutDocument

        linkableOglObjects: LinkableOglObjects = self._createLinkableObjects(pyutDocument=oglLinksDocument)

        unTangleOglLinks: UnTangleOglLinks  = UnTangleOglLinks(xmlVersion=XmlVersion.V11)
        untangledLinks:   UntangledOglLinks = unTangleOglLinks.unTangle(pyutDocument=oglLinksDocument, linkableOglObjects=linkableOglObjects)

        self.assertEqual(4, len(untangledLinks), '')

        hasLink: OglLink = self._getTestLink(untangledLinks=untangledLinks)

        self._checkAnchor(anchorPoint=hasLink.sourceAnchor, expectedX=573, expectedY=194)
        self._checkAnchor(anchorPoint=hasLink.destinationAnchor, expectedX=573, expectedY=300)

    def testUnTangleOglInterface2(self):
        root:               Element = parse(V11_OGL_INTERFACE2_DOCUMENT)
        interface2Document: Element = root.PyutDocument

        linkableOglObjects:        LinkableOglObjects = self._createLinkableObjects(pyutDocument=interface2Document)
        unTangleInterface2Diagram: UnTangleOglLinks   = UnTangleOglLinks(xmlVersion=XmlVersion.V11)

        untangledOglLinks: UntangledOglLinks = unTangleInterface2Diagram.unTangle(pyutDocument=interface2Document, linkableOglObjects=linkableOglObjects)

        self.assertEqual(1, len(untangledOglLinks), '')

        oglInterface2: UntangledLink = untangledOglLinks[0]

        destinationAnchor: SelectAnchorPoint = cast(SelectAnchorPoint, oglInterface2.destinationAnchor)

        x, y = destinationAnchor.GetPosition()
        self.assertEqual(250, x, '')
        self.assertEqual(112, y, '')

        self.assertEqual(AttachmentSide.EAST, destinationAnchor.attachmentPoint, '')

    def _createLinkableObjects(self, pyutDocument: Element) -> LinkableOglObjects:

        unTangleOglClass:    UnTangleOglClasses  = UnTangleOglClasses(xmlVersion=XmlVersion.V11)
        unTangledOglClasses: UntangledOglClasses = unTangleOglClass.unTangle(pyutDocument=pyutDocument)

        linkableOglObjects: LinkableOglObjects = LinkableOglObjects({})
        for aClass in unTangledOglClasses:
            oglClass:  OglClass  = cast(OglClass, aClass)
            pyutClass: PyutClass = oglClass.pyutObject
            linkableOglObjects[pyutClass.id] = oglClass
            self.logger.warning(f'{oglClass.id=}')

        return linkableOglObjects

    def _getTestLink(self, untangledLinks: UntangledOglLinks) -> OglLink:
        """

        Args:
            untangledLinks:

        Returns:  The link that has the TEST_LINK_NAME relationship
        """

        linkDict: Dict[str, UntangledLink] = {}

        for link in untangledLinks:
            untangledLink: UntangledLink = cast(UntangledLink, link)
            if isinstance(untangledLink, OglLink):
                linkDict[untangledLink.pyutObject.name] = untangledLink

        hasLink: OglLink = cast(OglLink, linkDict[TEST_LINK_NAME])

        return hasLink

    def _checkAnchor(self, anchorPoint: AnchorPoint, expectedX: int, expectedY: int):

        x, y = anchorPoint.GetModel().GetPosition()
        self.assertEqual(expectedX, x, '')
        self.assertEqual(expectedY, y, '')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleOglLinks))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
