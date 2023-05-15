
from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutActor import PyutActor

from ogl.OglActor import OglActor

from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import UntangledOglUseCases

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from tests.TestBase import TestBase

# import the class you want to test here
# from org.pyut.template import template


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
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'UseCasesTextNotes.xml')
        untangler:  UnTangler = UnTangler()

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

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'UseCaseDiagram.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Use-Cases')]

        return document


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangleUseCase))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
