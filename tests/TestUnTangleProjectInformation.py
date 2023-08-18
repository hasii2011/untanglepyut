
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from untanglepyut.Types import ProjectInformation
from untanglepyut.UnTangleProjectInformation import UnTangleProjectInformation
from untanglepyut.UnsupportedFileTypeException import UnsupportedFileTypeException


class TestUnTangleProjectInformation(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testIncorrectExtension(self):
        with self.assertRaises(UnsupportedFileTypeException):
            # noinspection PyUnusedLocal
            unTangleProjectInformation: UnTangleProjectInformation = UnTangleProjectInformation(fqFileName='HokeyXmlFileName.opie')

    def testV10ProjectInformation(self):
        self._testProjectInformation(package=TestBase.V10_TEST_FILES_PACKAGE_NAME, fileName='EmptyDiagram.xml', expectedVersion='10')

    def testV11ProjectInformation(self):
        self._testProjectInformation(package=TestBase.V11_TEST_FILES_PACKAGE_NAME, fileName='EmptyDiagram.xml', expectedVersion='11')

    def _testProjectInformation(self, package: str, fileName: str, expectedVersion: str):

        fqFileName:                 str                         = TestBase.getFullyQualifiedResourceFileName(package=package, fileName=fileName)
        unTangleProjectInformation: UnTangleProjectInformation  = UnTangleProjectInformation(fqFileName=fqFileName)
        projectInformation:         ProjectInformation          = unTangleProjectInformation.projectInformation

        expectedFileName: str = fqFileName

        self.assertEqual(expectedFileName, projectInformation.fileName, 'Mismatched project information file name')
        self.assertEqual(expectedVersion,  projectInformation.version, 'Mismatched XML version')


def suite() -> TestSuite:
    """"""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleProjectInformation))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
