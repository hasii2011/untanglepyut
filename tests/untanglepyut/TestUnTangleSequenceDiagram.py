
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from tests.TestBase import TestBase
from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler


# import the class you want to test here
# from org.pyut.template import template


class TestUnTangleSequenceDiagram(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestUnTangleSequenceDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestUnTangleSequenceDiagram.clsLogger

    def tearDown(self):
        pass

    def testSimpleSequenceDiagram(self):
        document: Document = self._retrieveSequenceDiagramDocument()
        self.assertEqual('SEQUENCE_DIAGRAM', document.documentType, 'Incorrect document type')

    # def testSequenceInstances(self):
    #     document: Document = self._retrieveSequenceDiagramDocument()
    #
    #     self.assertEqual(2, len(document.oglSDInstances), 'Bad # of instances')

    # def testSequenceMessages(self):
    #     document: Document = self._retrieveSequenceDiagramDocument()
    #
    #     self.assertEqual(1, len(document.oglSDMessages), 'Bad # of messages')
    #
    def _retrieveSequenceDiagramDocument(self) -> Document:

        fqFileName: str       = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'SequenceDiagram.xml')
        untangler:  UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

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
