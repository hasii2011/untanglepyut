from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from miniogl.DiagramFrame import DiagramFrame
from ogl.OglClass import OglClass
from pkg_resources import resource_filename
from pyutmodel.PyutClass import PyutClass

from wx import App
from wx import Frame
from wx import ID_ANY

from tests.TestBase import TestBase
from untanglepyut.Untangler import Document
from untanglepyut.Untangler import DocumentTitle

from untanglepyut.Untangler import UnTangler
from untanglepyut.Untangler import UntangledOglClasses

DIAGRAM_NAME_1: DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2: DocumentTitle = DocumentTitle('Diagram-2')


class DummyApp(App):
    def OnInit(self):
        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

        return True


class TestUnTangler(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestUnTangler.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestUnTangler.clsLogger
        self.app:    App    = DummyApp(redirect=True)

        self._fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'MultiDocumentProject.xml')

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testNoProjectInformation(self):
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        self.assertIsNone(untangler.projectInformation.version, 'Should be uninitialized')
        self.assertIsNone(untangler.projectInformation.codePath, 'Should be uninitialized')

    def testProjectInformation(self):

        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        self.assertEqual('',   untangler.projectInformation.codePath)
        self.assertEqual('10', untangler.projectInformation.version)

    def testCreateDocuments(self):

        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        self.assertEqual(2, len(untangler.documents), 'Incorrect number of documents created')

    def testCreateOglClassesForDiagram1(self):

        self._testCreateClassesForDiagram(DIAGRAM_NAME_1, expectedCount=2)

    def testCreateOglClassesForDiagram2(self):

        self._testCreateClassesForDiagram(DIAGRAM_NAME_2, expectedCount=7)

    def testNonZeroSizeForClassesInDiagram1(self):
        self._testNonZeroSizeForClassesInDiagram(DIAGRAM_NAME_1)

    def testNonZeroSizeForClassesInDiagram2(self):
        self._testNonZeroSizeForClassesInDiagram(DIAGRAM_NAME_2)

    def testNonZeroPositionsForClassesInDiagram1(self):
        self._testNonZeroPositionsForClassesInDiagram(DIAGRAM_NAME_1)

    def testNonZeroPositionsForClassesInDiagram2(self):
        self._testNonZeroPositionsForClassesInDiagram(DIAGRAM_NAME_2)

    def testPyutClassesDescription(self):
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        title: DocumentTitle = DIAGRAM_NAME_1
        document: Document = untangler.documents[title]
        oglClasses: UntangledOglClasses = document.oglClasses
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            possibleDescriptions: List[str] = ['I am crybaby Gen Z', 'I am a righteous boomer']
            self.assertIn(pyutClass.description, possibleDescriptions, "I don't see any of those")

    def _testCreateClassesForDiagram(self, title: DocumentTitle, expectedCount: int):

        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()
        document: Document = untangler.documents[title]
        oglClasses: List[OglClass] = document.oglClasses

        self.assertEqual(expectedCount, len(oglClasses), f'Incorrect number of classes generated for: {title}')

    def _testNonZeroSizeForClassesInDiagram(self, title: DocumentTitle):
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()
        document: Document = untangler.documents[title]
        oglClasses: List[OglClass] = document.oglClasses

        for oglClass in oglClasses:
            size = oglClass.GetSize()
            self.assertNotEqual(0, size[0], 'Width should be non-zero')
            self.assertNotEqual(0, size[1], 'Height should be non-zero')

    def _testNonZeroPositionsForClassesInDiagram(self, title: DocumentTitle):
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()
        document: Document = untangler.documents[title]
        oglClasses: List[OglClass] = document.oglClasses

        for oglClass in oglClasses:
            pos = oglClass.GetPosition()
            self.assertNotEqual(0, pos[0], 'x should be non-zero')
            self.assertNotEqual(0, pos[1], 'y should be non-zero')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
