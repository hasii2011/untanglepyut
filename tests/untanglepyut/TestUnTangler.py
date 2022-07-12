from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers

from wx import App
from wx import Frame
from wx import ID_ANY

from tests.TestBase import TestBase
from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle

from untanglepyut.UnTangler import UnTangler
from untanglepyut.UnTangler import UntangledOglClasses
from untanglepyut.UnTangler import UntangledOglLinks

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

    def testGraphicSimpleLinks(self):

        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_1)

        self.assertTrue(len(oglLinks) == 1, 'A minimal link was not created')

    def testClassicInterfaceCreated(self):

        oglLinks:  UntangledOglLinks = self._getOglLinksFromDocument(DIAGRAM_NAME_2)
        for oglLink in oglLinks:
            pyutLink: PyutLink = oglLink.pyutObject
            if pyutLink.linkType == PyutLinkType.INTERFACE:
                srcShape:     OglClass  = oglLink.getSourceShape()
                srcPyutClass: PyutClass = srcShape.pyutObject
                self.assertEquals(8, srcPyutClass.id)

                dstShape:     OglClass  = oglLink.getDestinationShape()
                dstPyutClass: PyutClass = dstShape.pyutObject
                self.assertEquals(7, dstPyutClass.id)
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
                pyutInterface: PyutInterface = cast(PyutInterface, oglLink.pyutObject)
                self.logger.debug(f'{pyutInterface=}')
                self.assertEqual('IClassInterface', pyutInterface.name, 'Mismatched interface name')
                self.assertEqual(1, len(pyutInterface.implementors), 'Should only have 1 implementor')
                implementorName: str = pyutInterface.implementors[0]
                self.assertEqual('LollipopImplementor', implementorName, 'Mismatched implementor name')

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

    def _getOglLinksFromDocument(self, title: DocumentTitle) -> UntangledOglLinks:
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        document:  Document             = untangler.documents[title]
        oglLinks:  UntangledOglLinks = document.oglLinks
        return oglLinks


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
