from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from miniogl.DiagramFrame import DiagramFrame
from ogl.OglClass import OglClass
from pkg_resources import resource_filename

from wx import App
from wx import Frame
from wx import ID_ANY

from tests.TestBase import TestBase
from untanglepyut.Untangler import Document
from untanglepyut.Untangler import DocumentTitle

from untanglepyut.Untangler import UnTangler


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

        self._testCreateClassesForDiagram(DocumentTitle('Diagram-1'), expectedCount=2)

    def testCreateOglClassesForDiagram2(self):

        self._testCreateClassesForDiagram(DocumentTitle('Diagram-2'), expectedCount=7)

    def testNonZeroSizeForClasses(self):
        pass
    
    def _testCreateClassesForDiagram(self, title: DocumentTitle, expectedCount: int):

        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()
        document: Document = untangler.documents[title]
        oglClasses: List[OglClass] = document.oglClasses

        self.assertEqual(expectedCount, len(oglClasses), f'Incorrect number of classes generated for: {title}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
