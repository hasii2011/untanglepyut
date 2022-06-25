
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from tests.TestBase import TestBase

from untanglepyut.Untangler import UnTangler


class TestTemplate(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestTemplate.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestTemplate.clsLogger

        self._fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'MultiDocumentProject.xml')

    def tearDown(self):
        pass

    def testNoProjectInformation(self):
        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        self.assertIsNone(untangler.projectInformation.version, 'Should be uninitialized')
        self.assertIsNone(untangler.projectInformation.codePath, 'Should be uninitialized')

    def testProjectInformation(self):

        untangler: UnTangler = UnTangler(fqFileName=self._fqFileName)

        untangler.untangle()

        self.assertEqual('',   untangler.projectInformation.codePath)
        self.assertEqual('10', untangler.projectInformation.version)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestTemplate))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
