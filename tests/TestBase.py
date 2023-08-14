
from os import sep as osSep

from hasiihelper.UnitTestBase import UnitTestBase
from hasiicommon.ui.UnitTestBaseW import UnitTestBaseW

from untanglepyut.v10.UnTangler import DocumentTitle

DIAGRAM_NAME_1:    DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2:    DocumentTitle = DocumentTitle('Diagram-2')
TEST_XML_FILENAME: str           = 'MultiDocumentProject.xml'


class TestBase(UnitTestBaseW):

    V10_TEST_FILES_PACKAGE_NAME:  str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.v10'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        pass
