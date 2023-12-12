
from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutActor import PyutActor

from ogl.OglActor import OglActor

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle
from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import UntangledOglUseCases

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.UnTangler import UnTangler

from tests.TestBase import TestBase


class TestUnTangleUseCase(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testUseCaseDiagramNotesTexts(self):
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'UseCasesTextNotes.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Use-Cases')]

        self.assertEqual(1, len(document.oglTexts), 'Mismatch # of OglText instances ')
        self.assertEqual(1, len(document.oglNotes), 'Mismatch # of OglNote instances')

    def testUseCaseDiagramActors(self):

        document:  Document           = self._retrieveUseCaseDocument()
        oglActors: UntangledOglActors = document.oglActors

        self.assertEqual(1, len(oglActors), 'Mismatch # of OglActors ')

        oglActor: OglActor = oglActors[0]
        pyutActor: PyutActor = oglActor.pyutObject
        actualName: str = pyutActor.name
        expectedName: str = 'BasicActor'

        self.assertEqual(expectedName, actualName, 'Did we get the wrong actor !!')

    def testUseCaseDiagramUseCases(self):
        document:    Document             = self._retrieveUseCaseDocument()
        oglUseCases: UntangledOglUseCases = document.oglUseCases

        self.assertEqual(1, len(oglUseCases), 'Mismatch # of OglUseCases ')

    def testUseCaseDiagramLinks(self):
        document: Document             = self._retrieveUseCaseDocument()
        oglLinks: UntangledOglLinks = document.oglLinks

        self.assertEqual(1, len(oglLinks), 'Mismatch # of links ')      # TODO TEMP UNTIL I REFACTOR DIRTY CODE

    def _retrieveUseCaseDocument(self) -> Document:

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'UseCaseDiagram.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Use-Cases')]

        return document


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleUseCase))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
