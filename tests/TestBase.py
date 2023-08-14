
from hasiicommon.ui.UnitTestBaseW import UnitTestBaseW

from untanglepyut.v10.UnTangler import DocumentTitle

DIAGRAM_NAME_1:    DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2:    DocumentTitle = DocumentTitle('Diagram-2')
TEST_XML_FILENAME: str           = 'MultiDocumentProject.xml'


class TestBase(UnitTestBaseW):

    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        pass
