
from typing import Dict
from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.enumerations.PyutDisplayMethods import PyutDisplayMethods
from untangle import Element
from untangle import parse

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutField import PyutFields
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutType import PyutType

from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from ogl.OglClass import OglClass

from untanglepyut.Types import UntangledOglClasses

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.UnTangleOglClasses import UnTangleOglClasses

from tests.ProjectTestBase import ProjectTestBase

V11_OGL_CLASS_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="SingleClassDiagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
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
</PyutDocument>
"""

V11_OGL_CLASS_NO_DISPLAY_ATTRIBUTES_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="SingleClassDiagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <OglClass width="429" height="145" x="300" y="175">
        <PyutClass id="1" name="SingleClass" stereotype="noStereotype" displayMethods="True" displayParameters="DisplayParameters" displayFields="True" displayStereotype="True" description="">
        </PyutClass>
    </OglClass>
</PyutDocument>
"""

V11_OGL_CLASS_WITH_DISPLAY_ATTRIBUTES_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="SingleClassDiagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <OglClass width="429" height="145" x="300" y="175">
        <PyutClass id="1" name="SingleClass" stereotype="noStereotype" displayMethods="True" displayParameters="DisplayParameters" displayFields="True" displayStereotype="True" displayConstructor="Display" displayDunderMethods="Do Not Display" description=""/>
    </OglClass>
</PyutDocument>
"""

V10_OGL_CLASS_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="UnitTest" scrollPositionX="100" scrollPositionY="100" pixelsPerUnitX="1" pixelsPerUnitY="1">
    <GraphicClass width="120" height="140" x="175" y="100">
        <Class id="1" name="ClassName0" filename="/Users/humberto.a.sanchez.ii/PycharmProjects/PyUt/src/UnitTest.py" description="" showMethods="True" showFields="True" showStereotype="True" displayParameters="Unspecified">
            <Method name="OzzeeElGatoDiablo" visibility="PUBLIC">
                <Modifier name="static"/>
                <Modifier name="bogus"/>
                <Return type="str"/>
                <SourceCode>
                    <Code>weLeft:           bool = True</Code>
                    <Code>isOzzeeAGoodGato: bool = False</Code>
                    <Code>if weLeft is True:</Code>
                    <Code>    isOzzeeAGoodGato = True</Code>
                    <Code>return isOzzeeAGoodGato</Code>
                </SourceCode>
            </Method>
        </Class>
    </GraphicClass>
</PyutDocument>
"""


class TestUnTangleOglClass(ProjectTestBase):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated:  08 September 2023
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testV10OglClass(self):
        root:          Element = parse(V10_OGL_CLASS_DOCUMENT)
        classDocument: Element = root.PyutDocument

        unTangleOglClass: UnTangleOglClasses = UnTangleOglClasses(xmlVersion=XmlVersion.V10)

        unTangledOglClasses: UntangledOglClasses = unTangleOglClass.unTangle(pyutDocument=classDocument)

        self.assertEqual(1, len(unTangledOglClasses), '')

        oglClass:  OglClass  = unTangledOglClasses[0]
        #
        # TODO:  This test really belongs in a unit test for the V10 version of untangle Pyut for classes
        #
        pyutClass: PyutClass = oglClass.pyutObject

        self.assertTrue(pyutClass.displayStereoType, 'True in XML')

        width, height = oglClass.GetSize()

        self.assertEqual(120, width, '')
        self.assertEqual(140, height, '')

        x, y = oglClass.GetPosition()

        self.assertEqual(175, x, '')
        self.assertEqual(100, y, '')

    def testV11OglClassNoDisplayAttributes(self):

        root:          Element = parse(V11_OGL_CLASS_NO_DISPLAY_ATTRIBUTES_DOCUMENT)
        classDocument: Element = root.PyutDocument

        unTangleOglClass:    UnTangleOglClasses = UnTangleOglClasses(xmlVersion=XmlVersion.V11)
        unTangledOglClasses: UntangledOglClasses = unTangleOglClass.unTangle(pyutDocument=classDocument)

        oglClass:  OglClass  = unTangledOglClasses[0]
        pyutClass: PyutClass = oglClass.pyutObject
        """
        If they are not in the XML we should default them to UnSpecified
        """
        self.assertEqual(PyutDisplayMethods.UNSPECIFIED, pyutClass.displayConstructor, 'Constructor display attribute is incorrect')
        self.assertEqual(PyutDisplayMethods.UNSPECIFIED, pyutClass.displayDunderMethods, 'Dunder method display attribute is incorrect')

    def testV11OglClassWithDisplayAttributes(self):
        root:          Element = parse(V11_OGL_CLASS_WITH_DISPLAY_ATTRIBUTES_DOCUMENT)
        classDocument: Element = root.PyutDocument

        unTangleOglClass:    UnTangleOglClasses = UnTangleOglClasses(xmlVersion=XmlVersion.V11)
        unTangledOglClasses: UntangledOglClasses = unTangleOglClass.unTangle(pyutDocument=classDocument)

        oglClass:  OglClass  = unTangledOglClasses[0]
        pyutClass: PyutClass = oglClass.pyutObject

        self.assertEqual(PyutDisplayMethods.DISPLAY,        pyutClass.displayConstructor,   'Constructor display attribute is incorrect')
        self.assertEqual(PyutDisplayMethods.DO_NOT_DISPLAY, pyutClass.displayDunderMethods, 'Dunder method display attribute is incorrect')

    def testV11OglClass(self):

        root:          Element = parse(V11_OGL_CLASS_DOCUMENT)
        classDocument: Element = root.PyutDocument

        unTangleOglClass: UnTangleOglClasses = UnTangleOglClasses(xmlVersion=XmlVersion.V11)

        unTangledOglClasses: UntangledOglClasses = unTangleOglClass.unTangle(pyutDocument=classDocument)

        self.assertEqual(1, len(unTangledOglClasses), '')

        oglClass:  OglClass  = unTangledOglClasses[0]
        pyutClass: PyutClass = oglClass.pyutObject

        methods: PyutMethods = pyutClass.methods
        self.assertEqual(7, len(methods), '')
        self.assertEqual(3, len(pyutClass.fields), '')

        methodDict: Dict[str, PyutMethod] = {}
        for method in methods:
            pyutMethod: PyutMethod = cast(PyutMethod, method)

            methodDict[pyutMethod.name] = pyutMethod

        knownMethod: PyutMethod = methodDict['methodWithParameters']

        self.assertEqual(3, len(knownMethod.parameters), '')

        fields:    PyutFields           = pyutClass.fields
        fieldDict: Dict[str, PyutField] = {}
        for field in fields:
            pyutField: PyutField = cast(PyutField, field)
            fieldDict[pyutField.name] = pyutField

        self.assertEqual(3, len(fieldDict), '')

        knownField: PyutField = fieldDict['privateField']

        self.assertEqual('42.0', knownField.defaultValue, '')
        self.assertEqual(PyutType('float'), knownField.type, '')
        self.assertEqual(PyutVisibility.PRIVATE, knownField.visibility, '')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleOglClass))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
