
from typing import Dict
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from untangle import Element
from untangle import parse

from ogl.OglNote import OglNote

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.Types import UntangledOglNotes

from untanglepyut.UnTangleOglNotes import UnTangleOglNotes


from tests.TestBase import TestBase

V11_MANY_NOTES_DOCUMENT: str = """
    <PyutDocument type="CLASS_DIAGRAM" title="Class Diagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
        <OglNote width="100" height="50" x="231" y="191">
            <PyutNote id="1" content="I am note 1" filename="" />
        </OglNote>
        <OglNote width="100" height="50" x="563" y="296">
            <PyutNote id="2" content="I am note 2" filename="" />
        </OglNote>
        <OglNote width="100" height="50" x="196" y="483">
            <PyutNote id="3" content="I am note 3" filename="/tmp/Note3.txt" />
        </OglNote>
    </PyutDocument>
"""

V10_MANY_NOTES_DOCUMENT: str = """
    <PyutDocument type="CLASS_DIAGRAM" title="Class Diagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
        <GraphicNote width="123" height="56" x="75" y="75">
            <Note id="1" content="This is note 1" filename=""/>
        </GraphicNote>
        <GraphicNote width="128" height="57" x="250" y="75">
            <Note id="2" content="This is note 2" filename=""/>
        </GraphicNote>
        <GraphicNote width="211" height="53" x="100" y="175">
            <Note id="3" content="This is the note 3;  I am fat note" filename="/tmp/Note3.txt"/>
        </GraphicNote>
    </PyutDocument>
"""


class TestUnTangleOglNotes(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testUntangleV11Notes(self):
        self._runTest(V11_MANY_NOTES_DOCUMENT, XmlVersion.V11)

    def testUntangleV10Notes(self):
        self._runTest(V10_MANY_NOTES_DOCUMENT, XmlVersion.V10)

    def _runTest(self, pyutDocument: str, xmlVersion: XmlVersion):

        root:              Element = parse(pyutDocument)
        manyNotesDocument: Element = root.PyutDocument

        unTangleOglNotes: UnTangleOglNotes = UnTangleOglNotes(xmlVersion=xmlVersion)

        unTangledNotes: UntangledOglNotes = unTangleOglNotes.unTangle(pyutDocument=manyNotesDocument)

        self.assertEqual(3, len(unTangledNotes), 'Note count mismatch')

        noteDict: Dict[int, OglNote] = {}

        for note in unTangledNotes:
            oglNote: OglNote = cast(OglNote, note)

            noteDict[oglNote.pyutObject.id] = oglNote

        noteWithFileName: OglNote = noteDict[3]

        self.assertEqual('/tmp/Note3.txt', noteWithFileName.pyutObject.fileName)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleOglNotes))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
