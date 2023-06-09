from typing import List
from typing import Tuple
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from ogl.OglDimensions import OglDimensions
from ogl.preferences.OglPreferences import OglPreferences

from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance

from untanglepyut.Types import OglSDInstances
from untanglepyut.Types import OglSDMessages

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from tests.TestBase import TestBase


class TestUnTangleSequenceDiagram(TestBase):
    """
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleSequenceDiagram(self):
        document: Document = self._retrieveSequenceDiagramDocument()
        self.assertEqual('SEQUENCE_DIAGRAM', document.documentType, 'Incorrect document type')

    def testSequenceInstances(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        oglSDInstances: OglSDInstances = document.oglSDInstances
        self.assertEqual(2, len(oglSDInstances), 'Bad # of instances')

        expectedInstanceNames: List[str] = ['Instance1', 'Instance2']
        for oglSDInstance in oglSDInstances.values():
            self.assertIn(oglSDInstance.instanceName.text, expectedInstanceNames, 'Not an expected instance')

    def testSequenceMessages(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        self.assertEqual(1, len(document.oglSDMessages), 'Bad # of messages')

    def testSequenceMessageTypeIsCorrect(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        sdMessages: OglSDMessages = document.oglSDMessages
        for sdMessage in sdMessages.values():
            pyutSDMessage: PyutSDMessage = sdMessage.pyutSDMessage
            self.assertEqual(PyutLinkType.SD_MESSAGE, pyutSDMessage.linkType, 'Link type not correctly set')

    def testSequenceMessagePyutSDMessageIsCorrect(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        sdMessages: OglSDMessages = document.oglSDMessages
        for sdMessage in sdMessages.values():
            pyutSDMessage: PyutSDMessage = sdMessage.pyutSDMessage

            pyutSrcInstance: PyutSDInstance = pyutSDMessage.getSource()
            pyutDstInstance: PyutSDInstance = pyutSDMessage.getDest()

            self.assertIsNotNone(pyutSrcInstance, 'Missing source sd instance')
            self.assertIsNotNone(pyutDstInstance, 'Missing source sd instance')

    def testSDInstanceLifeLineIsCorrect(self):
        """
        Verifies https://github.com/hasii2011/untanglepyut/issues/29
        """
        document: Document = self._retrieveSequenceDiagramDocument()

        sdInstances: OglSDInstances = document.oglSDInstances
        for sdInstance in sdInstances.values():
            oglSDInstance: OglSDInstance = cast(OglSDInstance, sdInstance)
            actualSize:   Tuple[int, int] = oglSDInstance.GetSize()
            expectedSize: OglDimensions   = OglPreferences().instanceDimensions
            self.assertEqual(expectedSize.height, actualSize[1], 'Lifeline height is incorrect')

    def _retrieveSequenceDiagramDocument(self) -> Document:

        fqFileName: str       = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, 'SequenceDiagram.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Sequence Diagram')]

        return document


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleSequenceDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
