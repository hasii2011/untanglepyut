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

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers

from wx import App
from wx import Frame
from wx import ID_ANY

from tests.TestBase import TestBase
from untanglepyut.Untangler import Document
from untanglepyut.Untangler import DocumentTitle

from untanglepyut.Untangler import UnTangler
from untanglepyut.Untangler import UntangledOglClasses

DIAGRAM_NAME_1:    DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2:    DocumentTitle = DocumentTitle('Diagram-2')
TEST_XML_FILENAME: str           = 'MultiDocumentProject.xml'


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

        self._fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, TEST_XML_FILENAME)

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
        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_1)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            possibleDescriptions: List[str] = ['I am crybaby Gen Z', 'I am a righteous boomer']
            self.assertIn(pyutClass.description, possibleDescriptions, "I don't see that description")

    def testPyutClassesHaveNames(self):

        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_2)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            possibleNames: List[str] = ['File', 'Folder', 'Car', 'Wheel', 'Interface', 'Implementor', 'LollipopImplementor']
            self.assertIn(pyutClass.name, possibleNames, "I don't see that name")

    def testPyuMethodsCreated(self):

        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_2)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'Interface':
                possibleNames: List[str] = ['floatMethod', 'intMethod', 'stringMethod', 'fakeMethod']
                foundDictionary: dict = {
                    'floatMethod': False,
                    'intMethod':   False,
                    'stringMethod': False
                }
                for method in pyutClass.methods:
                    # first ensure we do not find unknown method names
                    self.assertIn(method.name, possibleNames, 'I do not see that nane')
                    foundDictionary[method.name] = True
                # Then make sure we found the all the known ones
                for methodName in foundDictionary.keys():
                    self.assertTrue(foundDictionary[methodName], f'Oops did not find an expected method: {methodName}')

    def testPyutMethodsWithParameters(self):

        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_1)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'BaseClass':
                methodWithParameters: PyutMethod = pyutClass.methods[0]
                parameters = methodWithParameters.parameters
                possibleNames: List[str] = ['intParameter', 'floatParameter', 'stringParameter']
                for parameter in parameters:
                    self.logger.info(f'{parameter.name=}')
                    self.assertIn(parameter.name, possibleNames, f'I do not see that nane')

    def testPyutMethodModifiers(self):

        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_1)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'BaseClass':
                methods: List[PyutMethod] = pyutClass.methods
                for method in methods:
                    if method.name == 'methodWithManyModifiers':
                        expectedModifiers: List[str] = ['modifier1', 'modifier2']
                        modifiers: PyutModifiers = method.modifiers
                        for modifier in modifiers:
                            self.assertIn(modifier, expectedModifiers, 'Unexpected method modifier')

    def testPyutMethodHasSourceCode(self):
        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_1)
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'SubClass':
                methods: List[PyutMethod] = pyutClass.methods
                for method in methods:
                    if method.name == 'methodWithSourceCode':
                        actualSourceCode: List[str] = method.sourceCode
                        self.assertEqual(2, len(actualSourceCode), "Source code line count mismatch")
                        expectedSource: List[str] = ['int: i = 0', 'return True']
                        self.assertEqual(expectedSource, actualSourceCode, 'Source Code Mismatch')
                        break

    def _testCreateClassesForDiagram(self, title: DocumentTitle, expectedCount: int):

        oglClasses: List[OglClass] = self._getOglClassesFromDocument(title)

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

        oglClasses: List[OglClass] = self._getOglClassesFromDocument(title)

        for oglClass in oglClasses:
            pos = oglClass.GetPosition()
            self.assertNotEqual(0, pos[0], 'x should be non-zero')
            self.assertNotEqual(0, pos[1], 'y should be non-zero')

    def _getOglClassesFromDocument(self, title: DocumentTitle) -> UntangledOglClasses:
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        document:  Document             = untangler.documents[title]
        oglClasses: UntangledOglClasses = document.oglClasses

        return oglClasses


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
