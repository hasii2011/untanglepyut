
from typing import Dict
from typing import NewType

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutField import PyutFields
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutMethods
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from untangle import Element

from tests.TestBase import TestBase

from untangle import parse

from untanglepyut.XmlVersion import XmlVersion
from untanglepyut.v11.UnTanglePyut import UnTanglePyut

V11_PYUT_CLASS: str = """
    <OglClass width="429" height="145" x="300" y="175">
        <PyutClass id="1" name="SingleClass" stereotype="noStereotype" displayMethods="True" displayParameters="Display" displayFields="True" displayStereotype="True" description="I am a single class">
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

    def testPyutClass(self):
        root:        Element = parse(V11_PYUT_CLASS)
        oglClass: Element = root.OglClass

        untanglepyut: UnTanglePyut = UnTanglePyut(xmlVersion=XmlVersion.V11)

        pyutClass: PyutClass = untanglepyut.classToPyutClass(graphicClass=oglClass)

        self.assertEqual('SingleClass', pyutClass.name, 'Name mismatch')
        # Test changed attribute names
        self.assertEqual(PyutStereotype.NO_STEREOTYPE, pyutClass.stereotype, '')
        self.assertTrue(pyutClass.showMethods, '')
        self.assertTrue(pyutClass.showFields, '')
        self.assertTrue(pyutClass.displayStereoType, '')
        self.assertEqual(PyutDisplayParameters.DISPLAY,  pyutClass.displayParameters)

        methods: PyutMethods = pyutClass.methods
        self.assertTrue(len(methods) == 7, '')

        methodDictionary: MethodDictionary = MethodDictionary({})
        for method in methods:
            methodDictionary[method.name] = method

        self._checkMethods(methodDictionary)
        self._checkParameters(methodDictionary)
        self._checkFields(pyutClass=pyutClass)

    def _checkFields(self, pyutClass: PyutClass):

        fields: PyutFields = pyutClass.fields

        self.assertEqual(3, len(fields), 'There is a field number mismatch')

        fieldDictionary: FieldDictionary = FieldDictionary({})
        for field in fields:
            fieldDictionary[field.name] = field

        protectedField: PyutField = fieldDictionary['protectedField']

        self.assertIsNotNone(protectedField, '')
        self.assertEqual(PyutVisibilityEnum.PROTECTED, protectedField.visibility,  '')
        self.assertEqual('Ozzee',              protectedField.defaultValue, '')

    def _checkMethods(self, methodDictionary:  MethodDictionary):

        pyutMethod: PyutMethod = methodDictionary['publicMethod']

        self.assertEqual('publicMethod', pyutMethod.name, '')
        self.assertEqual(PyutVisibilityEnum.PUBLIC, pyutMethod.visibility, '')
        self.assertEqual(PyutType('str'), pyutMethod.returnType, '')

    def _checkParameters(self, methodDictionary: MethodDictionary):

        pyutMethod = methodDictionary['methodWithParameters']
        parameters: PyutParameters = pyutMethod.parameters
        self.assertEqual(3, len(parameters), '')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTanglePyut))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
