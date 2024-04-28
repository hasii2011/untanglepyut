
from typing import Dict
from typing import NewType

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutField import PyutFields
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutMethod import PyutParameters
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutUseCase import PyutUseCase

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility
from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters

from untangle import Element
from untangle import parse

from untanglepyut.XmlVersion import XmlVersion
from untanglepyut.UnTanglePyut import ConvolutedPyutSDMessageInformation
from untanglepyut.UnTanglePyut import UnTanglePyut

from tests.ProjectTestBase import TestBase


V11_PYUT_CLASS: str = """
    <OglClass width="429" height="145" x="300" y="175">
        <PyutClass id="1" name="SingleClass" stereotype="noStereotype" displayMethods="True" displayParameters="DisplayParameters" displayFields="True" displayStereotype="True" description="I am a single class">
            <PyutMethod name="publicMethod" visibility="PUBLIC" returnType="str">
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="privateMethod" visibility="PRIVATE" returnType="int">
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="protectedMethod" visibility="PROTECTED" returnType="float">
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="staticMethod" visibility="PUBLIC" returnType="">
                <Modifier name="static" />
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="methodWithModifiers" visibility="PUBLIC" returnType="">
                <Modifier name="modifier1" />
                <Modifier name="final" />
                <SourceCode />
            </PyutMethod>
            <PyutMethod name="methodWithCode" visibility="PUBLIC" returnType="">
                <SourceCode>
                    <Code>x: int = 0</Code>
                    <Code>y: int = 0</Code>
                    <Code />
                    <Code>z: int = x + y</Code>
                </SourceCode>
            </PyutMethod>
            <PyutMethod name="methodWithParameters" visibility="PUBLIC" returnType="">
                <SourceCode />
                <PyutParameter name="intParam" type="int" defaultValue="42" />
                <PyutParameter name="floatParam" type="float" defaultValue="32.0" />
                <PyutParameter name="strParam" type="str" defaultValue="Ozzee" />
            </PyutMethod>
            <PyutField name="publicField" visibility="PUBLIC" type="int" defaultValue="666" />
            <PyutField name="privateField" visibility="PRIVATE" type="float" defaultValue="42.0" />
            <PyutField name="protectedField" visibility="PROTECTED" type="str" defaultValue="Ozzee" />
        </PyutClass>
   </OglClass>
"""

V11_SOURCE_PYUT_CLASS: str = """
    <OglClass width="78" height="44" x="150" y="150">
        <PyutClass id="1" name="Folder" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="" fileName="">
            <PyutField name="permissions" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
"""

V11_DESTINATION_PYUT_CLASS: str = """
    <OglClass width="88" height="50" x="151" y="302">
        <PyutClass id="2" name="File" stereotype="noStereotype" displayMethods="True" displayParameters="Unspecified" displayFields="True" displayStereotype="True" description="" fileName="">
            <PyutField name="size" visibility="PRIVATE" type="" defaultValue="" />
            <PyutField name="name" visibility="PRIVATE" type="" defaultValue="" />
        </PyutClass>
    </OglClass>
"""

V11_PYUT_LINK: str = """
        <PyutLink name="organizes" type="COMPOSITION" cardinalitySource="1" cardinalityDestination="*" bidirectional="False" sourceId="1" destinationId="2" />
"""

V10_PYUT_TEXT: str = """
    <GraphicText width="138" height="88" x="100" y="325">
        <Text id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few" />
    </OglText>
"""

V11_PYUT_TEXT: str = """
    <OglText width="138" height="88" x="100" y="325">
        <PyutText id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few" />
    </OglText>
"""

V11_PYUT_NOTE: str = """
    <OglNote width="128" height="49" x="175" y="300">
        <PyutNote id="1" content="I am a note linked to&amp;#xA;the LinkedToClass" fileName="" />
    </OglNote>
"""

V11_PYUT_ACTOR: str = """
    <OglActor width="87" height="114" x="50" y="100">
        <PyutActor id="1" name="BasicActor" fileName="" />
    </OglActor>
"""

V11_PYUT_USE_CASE: str = """
    <OglUseCase width="100" height="60" x="475" y="275">
        <PyutUseCase id="2" name="Basic Use Case" fileName="" />
    </OglUseCase>
"""

V11_PYUT_INTERFACE: str = """
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
        </OglInterface2>"""

V11_PYUT_SD_INSTANCE: str = """
    <OglSDInstance width="100" height="400" x="803" y="50">
        <PyutSDInstance id="3" instanceName="OzzeeInstance" lifeLineLength="200" />
    </OglSDInstance>
"""

V11_PYUT_SD_MESSAGE: str = """
    <OglSDMessage>
        <PyutSDMessage id="4" message="calls()" sourceTime="148" destinationTime="150" sourceId="1" destinationId="2" />
    </OglSDMessage>
"""

MethodDictionary = NewType('MethodDictionary', Dict[str, PyutMethod])
FieldDictionary  = NewType('FieldDictionary',  Dict[str, PyutField])


class TestUnTanglePyut(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testNoteNameNone(self):

        rootElement:    Element = parse(V11_PYUT_NOTE)
        oglNoteElement: Element = rootElement.OglNote

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutNote:     PyutNote     = untanglepyut.noteToPyutNote(graphicNote=oglNoteElement)

        self.assertIsNotNone(pyutNote.name, 'Where is my update!')

    def testPyutClass(self):
        root:     Element = parse(V11_PYUT_CLASS)
        oglClass: Element = root.OglClass

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)

        pyutClass: PyutClass = untanglepyut.classToPyutClass(graphicClass=oglClass)

        self.assertEqual('SingleClass', pyutClass.name, 'Name mismatch')
        # Test changed attribute names
        self.assertEqual(PyutStereotype.NO_STEREOTYPE, pyutClass.stereotype, '')
        self.assertTrue(pyutClass.showMethods, '')
        self.assertTrue(pyutClass.showFields, '')
        self.assertTrue(pyutClass.displayStereoType, '')
        self.assertEqual(PyutDisplayParameters.WITH_PARAMETERS,  pyutClass.displayParameters)

        methods: PyutMethods = pyutClass.methods
        self.assertTrue(len(methods) == 7, '')

        methodDictionary: MethodDictionary = MethodDictionary({})
        for method in methods:
            methodDictionary[method.name] = method

        self._checkMethods(methodDictionary)
        self._checkParameters(methodDictionary)
        self._checkFields(pyutClass=pyutClass)

    def testPyutLinks(self):
        destinationPyutClass: PyutClass = self._getPyutClass(rawXml=V11_DESTINATION_PYUT_CLASS)
        sourcePyutClass:      PyutClass = self._getPyutClass(rawXml=V11_SOURCE_PYUT_CLASS)

        rootElement:     Element = parse(V11_PYUT_LINK)
        pyutLinkElement: Element = rootElement.PyutLink

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)

        pyutLink: PyutLink = untanglepyut.linkToPyutLink(singleLink=pyutLinkElement, source=sourcePyutClass, destination=destinationPyutClass)
        self.assertIsNotNone(pyutLink, '')
        self.assertEqual('organizes', pyutLink.name, '')
        self.assertEqual(PyutLinkType.COMPOSITION, pyutLink.linkType)
        self.assertFalse(pyutLink.bidirectional, 'Should not be bidirectional')
        self.assertEqual('1', pyutLink.sourceCardinality, '')
        self.assertEqual('*', pyutLink.destinationCardinality, '')

    def testTextToPyutText(self):
        rootElement:     Element = parse(V11_PYUT_TEXT)
        oglTextElement: Element = rootElement.OglText

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutText:     PyutText     = untanglepyut.textToPyutText(graphicText=oglTextElement)
        self.assertIsNotNone(pyutText, '')
        self.assertEqual('This plain text\nWith line breaks\nAt least a few', pyutText.content, '')

    def testNoteToPyutNote(self):
        rootElement:    Element = parse(V11_PYUT_NOTE)
        oglNoteElement: Element = rootElement.OglNote

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutNote:     PyutNote     = untanglepyut.noteToPyutNote(graphicNote=oglNoteElement)

        self.assertIsNotNone(pyutNote, '')
        self.assertEqual('I am a note linked to\nthe LinkedToClass', pyutNote.content, '')
        self.assertEqual('', pyutNote.fileName, '')

    def testActorToPyutActor(self):
        rootElement:     Element = parse(V11_PYUT_ACTOR)
        oglActorElement: Element = rootElement.OglActor

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutActor:    PyutActor    = untanglepyut.actorToPyutActor(graphicActor=oglActorElement)

        self.assertIsNotNone(pyutActor, '')
        self.assertEqual('BasicActor', pyutActor.name, '')
        self.assertEqual('', pyutActor.fileName, '')

    def testInterfaceToPyutInterface(self):
        rootElement:          Element = parse(V11_PYUT_INTERFACE)
        oglInterface2Element: Element = rootElement.OglInterface2

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)

        pyutInterface: PyutInterface = untanglepyut.interfaceToPyutInterface(oglInterface2=oglInterface2Element)

        self.assertIsNotNone(pyutInterface, '')
        self.assertEqual('IClassInterface', pyutInterface.name)
        self.assertTrue(len(pyutInterface.implementors) == 1, '')

    def testUseCaseToPyutUseCase(self):
        rootElement:       Element = parse(V11_PYUT_USE_CASE)
        oglUseCaseElement: Element = rootElement.OglUseCase

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutUseCase:  PyutUseCase  = untanglepyut.useCaseToPyutUseCase(graphicUseCase=oglUseCaseElement)

        self.assertIsNotNone(pyutUseCase, '')
        self.assertEqual('Basic Use Case', pyutUseCase.name, '')

    def testSdInstanceToPyutSDInstance(self):
        rootElement:          Element = parse(V11_PYUT_SD_INSTANCE)
        oglSDInstanceElement: Element = rootElement.OglSDInstance

        untanglepyut:    UnTanglePyut   = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutSdInstance:  PyutSDInstance = untanglepyut.sdInstanceToPyutSDInstance(oglSDInstanceElement=oglSDInstanceElement)

        self.assertIsNotNone(pyutSdInstance, '')
        self.assertEqual('OzzeeInstance', pyutSdInstance.instanceName, '')
        self.assertEqual(200, pyutSdInstance.instanceLifeLineLength, '')

    def testSdMessageToPyutSDMessage(self):
        rootElement:         Element = parse(V11_PYUT_SD_MESSAGE)
        oglSDMessageElement: Element = rootElement.OglSDMessage

        untanglepyut:  UnTanglePyut                        = UnTanglePyut(xmlVersion=XmlVersion.V11)
        convoluted: ConvolutedPyutSDMessageInformation = untanglepyut.sdMessageToPyutSDMessage(oglSDMessageElement=oglSDMessageElement)

        self.assertIsNotNone(convoluted, '')
        message: PyutSDMessage = convoluted.pyutSDMessage
        self.assertEqual('calls()', message.message, '')
        self.assertEqual(148, message.sourceY)
        self.assertEqual(150, message.destinationY)

    def _checkFields(self, pyutClass: PyutClass):

        fields: PyutFields = pyutClass.fields

        self.assertEqual(3, len(fields), 'There is a field number mismatch')

        fieldDictionary: FieldDictionary = FieldDictionary({})
        for field in fields:
            fieldDictionary[field.name] = field

        protectedField: PyutField = fieldDictionary['protectedField']

        self.assertIsNotNone(protectedField, '')
        self.assertEqual(PyutVisibility.PROTECTED, protectedField.visibility,  '')
        self.assertEqual('Ozzee',              protectedField.defaultValue, '')

    def _checkMethods(self, methodDictionary:  MethodDictionary):

        pyutMethod: PyutMethod = methodDictionary['publicMethod']

        self.assertEqual('publicMethod', pyutMethod.name, '')
        self.assertEqual(PyutVisibility.PUBLIC, pyutMethod.visibility, '')
        self.assertEqual(PyutType('str'), pyutMethod.returnType, '')

    def _checkParameters(self, methodDictionary: MethodDictionary):

        pyutMethod = methodDictionary['methodWithParameters']
        parameters: PyutParameters = pyutMethod.parameters
        self.assertEqual(3, len(parameters), '')

    def _getPyutClass(self, rawXml: str) -> PyutClass:

        root:           Element = parse(rawXml)
        oglSourceClass: Element = root.OglClass

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)
        pyutClass:    PyutClass    = untanglepyut.classToPyutClass(graphicClass=oglSourceClass)

        self.logger.debug(f'{pyutClass}')

        return pyutClass


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTanglePyut))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
