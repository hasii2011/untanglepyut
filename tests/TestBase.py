
import logging
import logging.config

import json

from unittest import TestCase

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame

from wx import App
from wx import Frame
from wx import ID_ANY

from untanglepyut.UnTangler import DocumentTitle

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'

DIAGRAM_NAME_1:    DocumentTitle = DocumentTitle('Diagram-1')
DIAGRAM_NAME_2:    DocumentTitle = DocumentTitle('Diagram-2')
TEST_XML_FILENAME: str           = 'MultiDocumentProject.xml'


class DummyApp(App):
    def OnInit(self):
        return True


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                   str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    def setUp(self):
        self._app:   DummyApp = DummyApp()

        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

    def tearDown(self):
        self._app.OnExit()

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""

        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName
