
from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.BaseUnTangle import BaseUnTangle

from untanglepyut.Types import ProjectInformation

from untanglepyut.UnsupportedFileTypeException import UnsupportedFileTypeException

from tests.TestBase import TestBase


class TestBaseUnTangle(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testComing(self):
        pass


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestBaseUnTangle))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
