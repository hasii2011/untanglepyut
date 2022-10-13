from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage

from untanglepyut.Types import OglSDInstances
from untanglepyut.Types import OglSDMessages

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from tests.TestBase import TestBase


class TestUnTangleSequenceDiagram(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestUnTangleSequenceDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        super().setUp()
        self.logger: Logger = TestUnTangleSequenceDiagram.clsLogger

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
            self.assertIn(oglSDInstance.instanceName.GetText(), expectedInstanceNames, 'Not an expected instance')

    def testSequenceMessages(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        self.assertEqual(1, len(document.oglSDMessages), 'Bad # of messages')

    def testSequenceMessageTypeIsCorrect(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        sdMessages: OglSDMessages = document.oglSDMessages
        for sdMessage in sdMessages.values():
            pyutSDMessage: PyutSDMessage = sdMessage.getPyutObject()
            self.assertEqual(PyutLinkType.SD_MESSAGE, pyutSDMessage.linkType, 'Link type not correctly set')

    def testSequenceMessagePyutSDMessageIsCorrect(self):
        document: Document = self._retrieveSequenceDiagramDocument()

        sdMessages: OglSDMessages = document.oglSDMessages
        for sdMessage in sdMessages.values():
            pyutSDMessage: PyutSDMessage = sdMessage.getPyutObject()

            pyutSrcInstance: PyutSDInstance = pyutSDMessage.getSource()
            pyutDstInstance: PyutSDInstance = pyutSDMessage.getDest()

            self.assertIsNotNone(pyutSrcInstance, 'Missing source sd instance')
            self.assertIsNotNone(pyutDstInstance, 'Missing source sd instance')

    def _retrieveSequenceDiagramDocument(self) -> Document:

        fqFileName: str       = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'SequenceDiagram.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Sequence Diagram')]

        return document


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestUnTangleSequenceDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
