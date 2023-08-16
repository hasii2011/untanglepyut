
from logging import Logger
from logging import getLogger
from typing import cast

from untangle import Element
from untangle import parse

from untanglepyut.Types import ProjectInformation
from untanglepyut.UnTangleIO import UnTangleIO
from untanglepyut.UnsupportedFileTypeException import UnsupportedFileTypeException


class UnTangleProjectInformation(UnTangleIO):
    
    def __init__(self, fqFileName: str):
        super().__init__()

        self.infoLogger: Logger = getLogger(__name__)

        self._fqFileName:         str                = fqFileName
        self._projectInformation: ProjectInformation = cast(ProjectInformation, None)

    @property
    def projectInformation(self) -> ProjectInformation:
        """
        This property return nothing valid until you untangle the file

        Returns:  The project information of the untangled pyut file
        """
        if self._projectInformation is None:
            self._projectInformation = self._extractProjectInformationForFile(fqFileName=self._fqFileName)

        return self._projectInformation

    def _extractProjectInformationForFile(self, fqFileName: str) -> ProjectInformation:
        """
        Allows callers to inspect the project information.  For example the XML version

        Args:
            fqFileName: The fully qualified file for a .xml or .put file

        Returns:  A project information data class`
        """
        if fqFileName.endswith('.put') is False and fqFileName.endswith('.xml') is False:
            raise UnsupportedFileTypeException(message='File must end with .xml or .put extension')

        projectInformation: ProjectInformation = ProjectInformation()

        if fqFileName.endswith('.xml'):
            xmlString:   str = self.getRawXml(fqFileName=fqFileName)
            root:        Element = parse(xmlString)
            pyutProject: Element = root.PyutProject

            projectInformation = self._populateProjectInformation(pyutProject=pyutProject)
            projectInformation.fileName = fqFileName

        return projectInformation

    def _populateProjectInformation(self, pyutProject: Element) -> ProjectInformation:

        projectInformation: ProjectInformation = ProjectInformation()

        projectInformation.version  = pyutProject['version']
        projectInformation.codePath = pyutProject['CodePath']

        return projectInformation
