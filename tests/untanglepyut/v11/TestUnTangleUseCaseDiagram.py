
from unittest import TestSuite
from unittest import main as unitTestMain

from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase
from untangle import Element
from untangle import parse

from tests.TestBase import TestBase
from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglUseCases
from untanglepyut.XmlVersion import XmlVersion
from untanglepyut.UnTangleUseCaseDiagram import UnTangleUseCaseDiagram

V11_USE_CASE_DOCUMENT: str = """
    <PyutDocument type="USECASE_DIAGRAM" title="Use-Cases" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
        <OglLink sourceAnchorX="136" sourceAnchorY="150" destinationAnchorX="475" destinationAnchorY="305" spline="False">
            <LabelCenter x="-21" y="15" />
            <LabelSource x="555" y="281" />
            <LabelDestination x="555" y="281" />
            <PyutLink name="Kicks Butt" type="ASSOCIATION" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="1" destinationId="2" />
        </OglLink>
        <OglNote width="118" height="73" x="300" y="50">
            <PyutNote id="3" content="This is the note text&amp;#xA;With Line feeds&amp;#xA;Maybe more coming" filename="" />
        </OglNote>
        <OglText width="138" height="88" x="100" y="325">
            <PyutNote id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few" />
        </OglText>
        <OglActor width="87" height="114" x="50" y="100">
            <PyutActor id="1" name="BasicActor" filename="" />
        </OglActor>
        <OglUseCase width="100" height="60" x="475" y="275">
            <PyutUseCase id="2" name="Basic Use Case" filename="" />
        </OglUseCase>
    </PyutDocument>
"""


class TestUnTangleUseCaseDiagram(TestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testUnTangleActors(self):
        unTangleUseCaseDiagram: UnTangleUseCaseDiagram = self._untangleUseCaseDocument()
        untangledOglActors:     UntangledOglActors     = unTangleUseCaseDiagram.oglActors

        self.assertEqual(1, len(untangledOglActors), 'Actor count mismatch')

        # width="87" height="114" x="50" y="100"

        oglActor: OglActor = untangledOglActors[0]

        width, height = oglActor.GetSize()
        self.assertEqual(87, width,   'Actor width mismatch')
        self.assertEqual(114, height, 'Actor height mismatch')

        x, y = oglActor.GetPosition()
        self.assertEqual(50, x,  'Actor x position mismatch')
        self.assertEqual(100, y, 'Actor y position mismatch')

    def testUnTangleUseCases(self):
        unTangleUseCaseDiagram: UnTangleUseCaseDiagram = self._untangleUseCaseDocument()
        untangledOglUseCases:   UntangledOglUseCases   = unTangleUseCaseDiagram.oglUseCases

        self.assertEqual(1, len(untangledOglUseCases), 'Use Case count mismatch')

        oglUseCase: OglUseCase = untangledOglUseCases[0]

        width, height = oglUseCase.GetSize()
        self.assertEqual(100, width,  'Use Case width mismatch')
        self.assertEqual(60,  height, 'Use Case height mismatch')

        x, y = oglUseCase.GetPosition()
        self.assertEqual(475, x,  'Use Case x position mismatch')
        self.assertEqual(275, y, 'Use Case y position mismatch')

    def _untangleUseCaseDocument(self) -> UnTangleUseCaseDiagram:

        root:            Element = parse(V11_USE_CASE_DOCUMENT)
        useCaseDocument: Element = root.PyutDocument

        unTangleUseCaseDiagram: UnTangleUseCaseDiagram = UnTangleUseCaseDiagram(xmlVersion=XmlVersion.V11)

        unTangleUseCaseDiagram.unTangle(pyutDocument=useCaseDocument)

        return unTangleUseCaseDiagram


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleUseCaseDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
