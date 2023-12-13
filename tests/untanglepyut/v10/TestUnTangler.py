
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import cast

from importlib.abc import Traversable

from importlib.resources import files

from os import linesep as osLineSep

from unittest import TestSuite
from unittest import main as unitTestMain

from miniogl.ControlPoint import ControlPoint

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutModifiers
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutModifier import PyutModifier
from pyutmodelv2.PyutNote import PyutNote

from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from tests.ProjectTestBase import DIAGRAM_NAME_1
from tests.ProjectTestBase import DIAGRAM_NAME_2
from tests.ProjectTestBase import TEST_XML_FILENAME

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle
from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import UntangledOglNotes
from untanglepyut.Types import UntangledOglTexts

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.UnTangler import UnTangler

from tests.ProjectTestBase import TestBase

ATM_DIAGRAM_NAME:   DocumentTitle = DocumentTitle('Class Diagram')
SIMPLE_DIAGRAM_NAME: DocumentTitle = DocumentTitle('Simple')


class TestUnTangler(TestBase):
    """
    """
    def setUp(self):

        super().setUp()

        traversable: Traversable = files(TestBase.V10_TEST_FILES_PACKAGE_NAME) / TEST_XML_FILENAME
        self._fqFileName: str = str(traversable)

    def tearDown(self):
        super().tearDown()

    def testNoProjectInformation(self):
        untangler: UnTangler = UnTangler(XmlVersion.V10)

        self.assertIsNone(untangler.projectInformation, 'Should be uninitialized')

    def testProjectInformation(self):

        untangler: UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=self._fqFileName)

        self.assertEqual(self._fqFileName, untangler.projectInformation.fileName)
        self.assertEqual('',   untangler.projectInformation.codePath)
        self.assertEqual('10', untangler.projectInformation.version)

    def testCreateDocuments(self):

        untangler: UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=self._fqFileName)

        self.assertEqual(2, len(untangler.documents), 'Incorrect number of documents created')

    def testUntangleXml(self):
        untangler: UnTangler = UnTangler(XmlVersion.V10)

        rawXml: str = untangler.getRawXml(fqFileName=self._fqFileName)
        untangler.untangleXml(xmlString=rawXml, fqFileName=self._fqFileName)
        self.assertEqual(2, len(untangler.documents), 'Incorrect number of documents created')

    def testControlPointsGenerated(self):
        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(package=TestBase.V10_TEST_FILES_PACKAGE_NAME, fileName='ATM-Model.xml')
        untangler: UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        singleDocument: Document = untangler.documents[ATM_DIAGRAM_NAME]

        oglLinks: UntangledOglLinks = singleDocument.oglLinks
        for link in oglLinks:
            oglLink: OglLink = cast(OglLink, link)
            # Check a couple of the 'known' links with a single control point
            linkName: str = oglLink.pyutObject.name
            if linkName == 'has':
                # 			<ControlPoint x="207" y="469"/>
                controlPoint1: ControlPoint = cast(ControlPoint, oglLink.GetControlPoints()[0])
                self._assertPosition(expectedX=207, expectedY=469,
                                     controlPoint=controlPoint1,
                                     objectName=linkName)

            elif linkName == 'Account Transaction':
                # 			<ControlPoint x="726" y="469"/>
                controlPoint: ControlPoint = cast(ControlPoint, oglLink.GetControlPoints()[0])
                self._assertPosition(expectedX=726, expectedY=469,
                                     controlPoint=controlPoint,
                                     objectName=linkName)

    def testCreateOglClassesForDiagram1(self):

        self._testCreateClassesForDiagram(DIAGRAM_NAME_1, expectedCount=4)

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
            if len(pyutClass.description) > 0:
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

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiMethodModifier.xml')
        untangler: UnTangler = UnTangler(XmlVersion.V10)
        untangler.untangleFile(fqFileName=fqFileName)

        document:  Document             = untangler.documents[DocumentTitle('MultiMethodModifier')]
        oglClasses: UntangledOglClasses = document.oglClasses

        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'ClassWithMethods':
                methods: List[PyutMethod] = pyutClass.methods
                for method in methods:
                    if method.name == 'methodWithManyModifiers':
                        expectedModifiers: List[str] = ['Modifier1', 'Modifier2', 'Modifier3', 'Modifier4']
                        modifiers: PyutModifiers = method.modifiers
                        self.assertEqual(4, len(modifiers), 'Missing Modifiers')
                        foundCount: int = 0
                        for modifier in modifiers:
                            pyutModifier: PyutModifier = cast(PyutModifier, modifier)
                            self.assertIn(pyutModifier.name, expectedModifiers, 'Unexpected method modifier')
                            foundCount += 1
                        self.assertEqual(4, foundCount, 'Did not find all the expected modifiers')

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

    def testShowStereoType(self):
        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(DIAGRAM_NAME_1)
        foundStereoType: bool = False
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'ClassWithStereoType':
                self.assertEqual(PyutStereotype.METACLASS, pyutClass.stereotype, 'Incorrect stereotype')
                foundStereoType = True
                break
        self.assertTrue(foundStereoType, 'Did not find stereotype')

    def testStereoTypeEmpty(self):
        """
        My first indication that I understand functional programming
        """
        def emptyTest(oglClass) -> bool:
            testPassed: bool = False
            pyutClass: PyutClass = oglClass.pyutObject
            if pyutClass.name == 'ClassWithEmptyStereoType':
                self.assertEqual(PyutStereotype.NO_STEREOTYPE, pyutClass.stereotype, 'Stereotype should be empty')
                testPassed = True
            return testPassed
        self._runTest(DIAGRAM_NAME_1, emptyTest)

    def testUmlNote(self):
        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiObject.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('MultiObject')]

        self.assertEqual(1, len(document.oglNotes), 'Incorrect # of notes')

        oglNotes: UntangledOglNotes = document.oglNotes
        oglNote:  OglNote = oglNotes[0]     # Get the one and only

        expectedRepr: str = 'I am a UML Note'
        actualRepr:   str = oglNote.__repr__()      # indirectly tests pyutNote.content
        self.assertEqual(expectedRepr, actualRepr, 'Bad representation')

    def testMultiLineUmlNote(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiLineNote.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('DiagramNotes')]

        self.assertTrue(len(document.oglNotes) == 1, 'Too many notes')

        oglNote:     OglNote  = document.oglNotes.pop()
        pyutNote:    PyutNote = oglNote.pyutObject
        noteContent: str      = pyutNote.content

        lines: List[str] = noteContent.split(osLineSep)

        self.assertTrue(len(lines) == 4, 'Did not recover correct number of lines')

    def testUmlText(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiObject.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('MultiObject')]

        self.assertEqual(1, len(document.oglTexts), 'Incorrect # of text annotations')

    def testOglClassModelUpdated(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'ATM-Model.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Class Diagram')]

        oglClasses: UntangledOglClasses = document.oglClasses

        for oglClass in oglClasses:
            x, y = oglClass.GetPosition()
            self.assertNotEqual(0, x, 'There are no Ogl Classes at 0')
            self.assertNotEqual(0, y, 'There are no Ogl Classes at 0')

    def testOglTextModelUpdated(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiLinkDocument.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('MultiLink')]

        oglTexts: UntangledOglTexts = document.oglTexts

        for oglText in oglTexts:
            x, y = oglText.GetPosition()
            self.assertNotEqual(0, x, 'There are no Ogl Text objects at abscissa 0')
            self.assertNotEqual(0, y, 'There are no Ogl Text objects at ordinate 0')

    def testOglClassesWithFields(self):

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.V10_TEST_FILES_PACKAGE_NAME, 'MultiLinkDocument.xml')
        untangler:  UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('MultiLink')]
        oglClasses: UntangledOglClasses = document.oglClasses
        # ClassName -> list of field names
        classFields: Dict[str, List[str]]  = {
            'Folder':              ['permissions'],
            'File':                ['size', 'name'],
            'Car':                 ['model', 'vin', 'modelYear', 'make'],
            'Wheel':               ['size', 'width'],
            'Interface':           [],
            'Implementor':         [],
            'LollipopImplementor': []

        }
        # Class Names with found fields; classes with no fields preset to TRe
        foundFields: Dict[str, bool] = {
            'Folder':              False,
            'File':                False,
            'Car':                 False,
            'Wheel':               False,
            'Interface':           True,
            'Implementor':         True,
            'LollipopImplementor': True
        }
        for oglClass in oglClasses:
            pyutClass: PyutClass = oglClass.pyutObject
            fields: List[PyutField] = pyutClass.fields
            expectedFieldNames: List[str] = classFields[pyutClass.name]
            for field in fields:
                self.assertIn(field.name, expectedFieldNames, f'Missing field {field.name}')
                foundFields[pyutClass.name] = True
        #
        # Ensure that we found all fields
        #
        for className in foundFields.keys():
            self.assertTrue(foundFields[className], f'"{className}" is missing fields')

    def _testCreateClassesForDiagram(self, title: DocumentTitle, expectedCount: int):

        oglClasses: List[OglClass] = self._getOglClassesFromDocument(title)

        self.assertEqual(expectedCount, len(oglClasses), f'Incorrect number of classes generated for: {title}')

    def _testNonZeroSizeForClassesInDiagram(self, title: DocumentTitle):
        untangler: UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=self._fqFileName)
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
        untangler: UnTangler = UnTangler(XmlVersion.V10)

        untangler.untangleFile(fqFileName=self._fqFileName)

        document:  Document             = untangler.documents[title]
        oglClasses: UntangledOglClasses = document.oglClasses

        return oglClasses

    def _runTest(self, title: DocumentTitle, func: Callable):

        oglClasses: UntangledOglClasses = self._getOglClassesFromDocument(title)

        testPassed: bool = False
        for oglClass in oglClasses:
            testPassed = func(oglClass)

        self.assertTrue(testPassed, 'Test did not pass')

    def _assertPosition(self, expectedX: int, expectedY: int, controlPoint: ControlPoint, objectName: str):

        pos: Tuple[int, int] = controlPoint.GetPosition()

        self.assertEqual(expectedX, pos[0], f'{objectName} x position is incorrect')
        self.assertEqual(expectedY, pos[1], f'{objectName} y position is incorrect')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangler))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
