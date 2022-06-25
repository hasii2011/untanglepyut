
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from ogl.OglClass import OglClass

from untangle import parse
from untangle import Element


@dataclass
class ProjectInformation:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)


@dataclass
class Document:
    documentType:    str = ''
    documentTitle:   str = ''
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      List[OglClass] = field(default_factory=list)


DocumentTitle = NewType('DocumentTitle', str)
Documents     = NewType('Documents', dict[DocumentTitle, Document])


class UnTangler:

    def __init__(self, fqFileName: str):
        """

        Args:
            fqFileName:  Fully qualified file name
        """

        self.logger: Logger = getLogger(__name__)

        self._fqFileName:  str = fqFileName
        self._projectInformation: ProjectInformation = ProjectInformation()
        self._documents:          Documents          = Documents({})

    @property
    def projectInformation(self) -> ProjectInformation:
        """
        This property return nothing valid until you untangle the file

        Returns:  The project information of the untangled pyut file
        """
        return self._projectInformation

    @property
    def documents(self) -> Documents:
        return self._documents

    def untangle(self):

        xmlString:   str     = self._getRawXml()
        root:        Element = parse(xmlString)
        pyutProject: Element = root.PyutProject

        self._populateProjectInformation(pyutProject=pyutProject)

        for pyutDocument in pyutProject.PyutDocument:
            document: Document = self._updateCurrentDocumentInformation(pyutDocument=pyutDocument)

            self._documents[document.documentTitle] = document

            self.logger.debug(f'{document=}')
            document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)

    def _populateProjectInformation(self, pyutProject: Element):
        self._projectInformation.version  = pyutProject['version']
        self._projectInformation.codePath = pyutProject['CodePath']

    def _updateCurrentDocumentInformation(self, pyutDocument: Element) -> Document:

        documentInformation: Document = Document()

        documentTitle: DocumentTitle = DocumentTitle(pyutDocument['title'])

        documentInformation.documentType = pyutDocument['type']
        documentInformation.documentTitle = documentTitle
        documentInformation.scrollPositionX = pyutDocument['scrollPositionX']
        documentInformation.scrollPositionY = pyutDocument['scrollPositionY']
        documentInformation.pixelsPerUnitX = pyutDocument['pixelsPerUnitX']
        documentInformation.pixelsPerUnitY = pyutDocument['pixelsPerUnitY']

        self.logger.debug(f'{documentInformation=}')

        return documentInformation

    def _graphicClassesToOglClasses(self, pyutDocument: Element) -> List[OglClass]:

        oglClasses: List[OglClass] = []
        for graphicClass in pyutDocument.GraphicClass:
            self.logger.debug(f'{graphicClass=}')

            x: int = int(graphicClass['x'])
            y: int = int(graphicClass['y'])
            width:  int = int(graphicClass['width'])
            height: int = int(graphicClass['height'])
            oglClass: OglClass = OglClass(w=width, h=height)
            oglClass.SetPosition(x=x, y=y)

            oglClasses.append(oglClass)

        return oglClasses

    def _getRawXml(self) -> str:

        try:
            with open(self._fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e

        return xmlString
