
from typing import Tuple
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglAssociation import OglAssociation
from ogl.OglAssociationLabel import OglAssociationLabel

from ogl.OglClass import OglClass
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType

from tests.TestBase import DIAGRAM_NAME_1
from tests.TestBase import DIAGRAM_NAME_2
from tests.TestBase import TEST_XML_FILENAME
from tests.TestBase import TestBase

from untanglepyut.Types import UntangledOglLinks
from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler


class TestUnTangleOglLinks(TestBase):
    """
    """
    SIMPLE_DIAGRAM_NAME: DocumentTitle = DocumentTitle('Simple')

    def setUp(self):

        super().setUp()
        self._fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, TEST_XML_FILENAME)

        self._mockDC: MagicMock = MagicMock()

    def tearDown(self):
        super().tearDown()

    def testNoGraphicLinks(self):
        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'ScaffoldDiagram.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName)

        self.assertEqual(1, len(untangler.documents), 'Should be a small document')
        singleDocument: Document = untangler.documents[DocumentTitle('UnitTest')]
        self.assertEqual(0, len(singleDocument.oglLinks))

    def testGraphicSimpleLinks(self):

        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_1)

        self.assertTrue(len(oglLinks) == 1, 'A minimal link was not created')

    def testSimpleInheritance(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'SimpleInheritance.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document          = untangler.documents[TestUnTangleOglLinks.SIMPLE_DIAGRAM_NAME]
        oglLinks:       UntangledOglLinks = singleDocument.oglLinks
        self.assertEqual(1, len(oglLinks), 'There can be only one.')
        self.assertTrue(isinstance(oglLinks[0], OglInheritance), 'Must be inheritance')
        for oglLink in oglLinks:
            self.logger.debug(f'{oglLink}')
            pyutLink: PyutLink = cast(PyutLink, oglLink.pyutObject)
            self.assertEqual(PyutLinkType.INHERITANCE, pyutLink.linkType)

    def testClassicInterfaceCreated(self):

        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        for link in oglLinks:

            oglLink: OglLink = cast(OglLink, link)

            pyutLink: PyutLink = oglLink.pyutObject
            if pyutLink.linkType == PyutLinkType.INTERFACE:
                srcShape:     OglClass  = oglLink.sourceShape
                srcPyutClass: PyutClass = srcShape.pyutObject
                self.assertEqual(8, srcPyutClass.id)

                dstShape:     OglClass  = oglLink.destinationShape
                dstPyutClass: PyutClass = dstShape.pyutObject
                self.assertEqual(7, dstPyutClass.id)
                break

    def testAggregationCreated(self):
        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        for oglLink in oglLinks:

            if isinstance(oglLink.pyutObject, PyutLink):
                pyutLink: PyutLink = oglLink.pyutObject
                if pyutLink.linkType == PyutLinkType.AGGREGATION:
                    self.assertEqual('1', pyutLink.sourceCardinality, 'Aggregation source cardinality not correctly retrieved')
                    self.assertEqual('4', pyutLink.destinationCardinality, 'Aggregation destination cardinality not correctly retrieved')

    def testCompositionCreated(self):
        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        for oglLink in oglLinks:
            if isinstance(oglLink.pyutObject, PyutLink):
                pyutLink: PyutLink = oglLink.pyutObject
                if pyutLink.linkType == PyutLinkType.COMPOSITION:
                    self.assertEqual('1', pyutLink.sourceCardinality, 'Composition source cardinality not correctly retrieved')
                    self.assertEqual('*', pyutLink.destinationCardinality, 'Aggregation destination cardinality not correctly retrieved')

    def testLollipopInterfaceCreated(self):
        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        foundKnownLollipop: bool = False
        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):

                oglInterface2: OglInterface2 = cast(OglInterface2, oglLink)

                pyutInterface: PyutInterface = cast(PyutInterface, oglInterface2.pyutObject)
                self.logger.debug(f'{pyutInterface=}')
                self.assertEqual('IClassInterface', pyutInterface.name, 'Mismatched interface name')
                self.assertEqual(1, len(pyutInterface.implementors), 'Should only have 1 implementor')
                implementorName: str = pyutInterface.implementors[0]
                self.assertEqual('LollipopImplementor', implementorName, 'Mismatched implementor name')

                destAnchor:      SelectAnchorPoint  = oglInterface2.destinationAnchor

                x, y = destAnchor.GetPosition()

                self.assertEqual(465, x, 'X location incorrect')
                self.assertEqual(649, y, 'Y location incorrect')

                foundKnownLollipop = True
                break
        self.assertTrue(foundKnownLollipop, 'Did not untangle the expected lollipop interface')

    def testLollipopInterfaceMethodsCreated(self):

        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        foundMethods: bool = False
        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):
                pyutInterface: PyutInterface = cast(PyutInterface, oglLink.pyutObject)
                self.assertEqual(1, len(pyutInterface.methods), "Where is single method")
                self.assertEqual(3, len(pyutInterface.methods[0].parameters), 'Not enough parameters')

                foundMethods = True

        self.assertTrue(foundMethods, 'Did not untangle the expected lollipop interface')

    def testGetAssociationLabelPositions(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'SimpleGraphicLinkTest.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName)

        document: Document = untangler.documents[DocumentTitle('SimpleLink')]

        oglLinks: UntangledOglLinks = document.oglLinks
        for oglLink in oglLinks:
            self.logger.info(f'{oglLink}')
            oglAssociation: OglAssociation = cast(OglAssociation, oglLink)
            oglAssociation.Draw(dc=self._mockDC, withChildren=False)
            center: OglAssociationLabel = oglAssociation.centerLabel
            src:    OglAssociationLabel = oglAssociation.sourceCardinality
            dest:   OglAssociationLabel = oglAssociation.destinationCardinality

            dumbPosition: Tuple[int, int] = center.GetPosition()
            self.assertEqual(669, dumbPosition[0], 'Bad center x')
            self.assertEqual(249, dumbPosition[1], 'Bad center y')

            dumbPosition = src.GetPosition()
            self.assertEqual(669, dumbPosition[0], 'Bad source x')
            self.assertEqual(249, dumbPosition[1], 'Bad source y')

            dumbPosition = dest.GetPosition()
            self.assertEqual(669, dumbPosition[0], 'Bad destination x')
            self.assertEqual(249, dumbPosition[1], 'Bad destination y')

    def _getOglLinksFromDocument(self, title: DocumentTitle) -> UntangledOglLinks:
        untangler: UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=self._fqFileName)

        document:  Document             = untangler.documents[title]
        oglLinks:  UntangledOglLinks = document.oglLinks
        return oglLinks


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleOglLinks))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
