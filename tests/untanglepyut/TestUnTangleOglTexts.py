from typing import Dict
from typing import cast
from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from ogl.OglText import OglText

from untanglepyut.Types import UntangledOglTexts
from untanglepyut.UnTangleOglTexts import UnTangleOglTexts
from untanglepyut.XmlVersion import XmlVersion

from tests.TestBase import TestBase

V10_MANY_TEXTS_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="Lots Of Text" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <GraphicText width="125" height="50" x="50" y="75" textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">
        <Text id="1" content="I am text 1"/>
    </GraphicText>
    <GraphicText width="125" height="50" x="75" y="150" textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">
        <Text id="2" content="I am text 2"/>
    </GraphicText>
    <GraphicText width="125" height="50" x="275" y="75" textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">
        <Text id="3" content="I am text 3"/>
    </GraphicText>
</PyutDocument>
"""

V11_MANY_TEXTS_DOCUMENT: str = """
<PyutDocument type="CLASS_DIAGRAM" title="Class Diagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
    <OglText width="125" height="50" x="50" y="25">
        <PyutText id="1" content="I am text 1" />
    </OglText>
    <OglText width="125" height="50" x="75" y="150">
        <PyutText id="2" content="I am text 2" />
    </OglText>
    <OglText width="125" height="50" x="150" y="250">
        <PyutText id="3" content="I am text 3" />
    </OglText>
</PyutDocument>
"""


class TestUnTangleOglTexts(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testUntangleV10Texts(self):
        self._runTest(pyutDocument=V10_MANY_TEXTS_DOCUMENT, xmlVersion=XmlVersion.V10)

    def testUntangleV11Texts(self):
        """Another test"""
        pass
        self._runTest(pyutDocument=V11_MANY_TEXTS_DOCUMENT, xmlVersion=XmlVersion.V11)

    def _runTest(self, pyutDocument: str, xmlVersion: XmlVersion):

        root:              Element = parse(pyutDocument)
        manyTextsDocument: Element = root.PyutDocument

        unTangleOglTexts: UnTangleOglTexts = UnTangleOglTexts(xmlVersion=xmlVersion)
        unTangledTexts:   UntangledOglTexts = unTangleOglTexts.unTangle(pyutDocument=manyTextsDocument)

        self.assertEqual(3, len(unTangledTexts), 'Note count mismatch')

        textDict: Dict[int, OglText] = {}

        for text in unTangledTexts:
            oglText: OglText = cast(OglText, text)

            textDict[oglText.pyutObject.id] = oglText

        checkText: OglText = textDict[3]

        self.assertEqual('I am text 3', checkText.pyutObject.content)


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleOglTexts))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
