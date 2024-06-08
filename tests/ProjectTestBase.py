
from codeallybasic.UnitTestBase import UnitTestBase
from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from untanglepyut.UnTangler import DocumentTitle

DIAGRAM_NAME_1:    DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2:    DocumentTitle = DocumentTitle('Diagram-2')
TEST_XML_FILENAME: str           = 'MultiDocumentProject.xml'


class ProjectTestBase(UnitTestBaseW):

    V10_TEST_FILES_PACKAGE_NAME:  str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.v10'
    V11_TEST_FILES_PACKAGE_NAME:  str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.v11'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        pass
