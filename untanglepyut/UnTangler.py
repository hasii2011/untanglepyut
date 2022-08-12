
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from untangle import parse
from untangle import Element

from ogl.OglClass import OglClass
from ogl.OglNote import OglNote
from ogl.OglText import OglText

from pyutmodel.PyutClass import PyutClass

from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutText import PyutText

from untanglepyut.Common import GraphicInformation
from untanglepyut.Common import UntangledOglLinks
from untanglepyut.Common import createUntangledOglActorsFactory
from untanglepyut.Common import createUntangledOglLinksFactory
from untanglepyut.Common import toGraphicInfo

from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglNotes
from untanglepyut.Types import UntangledOglTexts

from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.UnTangleOglLinks import UnTangleOglLinks
from untanglepyut.UnTangleUseCaseDiagram import UnTangleUseCaseDiagram


@dataclass
class ProjectInformation:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)


def createUntangledOglClassesFactory() -> UntangledOglClasses:
    """
    Factory method to create  the UntangledClasses data structure;

    Returns:  A new data structure
    """
    return UntangledOglClasses([])


def createUntangledOglNotesFactory() -> UntangledOglNotes:
    return UntangledOglNotes([])


def createUntangledOglTextsFactory() -> UntangledOglTexts:
    return UntangledOglTexts([])


@dataclass
class Document:
    documentType:    str = ''
    documentTitle:   str = ''
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      UntangledOglClasses = field(default_factory=createUntangledOglClassesFactory)
    oglLinks:        UntangledOglLinks   = field(default_factory=createUntangledOglLinksFactory)
    oglNotes:        UntangledOglNotes   = field(default_factory=createUntangledOglNotesFactory)
    oglTexts:        UntangledOglTexts   = field(default_factory=createUntangledOglTextsFactory)
    oglActors:       UntangledOglActors  = field(default_factory=createUntangledOglActorsFactory)


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

        self._untanglePyut:     UnTanglePyut     = UnTanglePyut()
        self._untangleOglLinks: UnTangleOglLinks = UnTangleOglLinks()

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
            if document.documentType == 'CLASS_DIAGRAM':
                document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)
                document.oglNotes   = self._graphicNotesToOglNotes(pyutDocument=pyutDocument)
                document.oglTexts    = self._graphicalTextToOglTexts(pyutDocument=pyutDocument)
                document.oglLinks   = self._untangleOglLinks.graphicLinksToOglLink(pyutDocument, oglClasses=document.oglClasses, oglNotes=document.oglNotes)
            elif document.documentType == 'SEQUENCE_DIAGRAM':
                self.logger.warning(f'{document.documentType} unsupported')
            elif document.documentType == 'USECASE_DIAGRAM':

                unTangleUseCaseDiagram: UnTangleUseCaseDiagram = UnTangleUseCaseDiagram()

                unTangleUseCaseDiagram.unTangle(pyutDocument=pyutDocument)
                document.oglActors = unTangleUseCaseDiagram.oglActors
            else:
                assert False, f'Unknown document type: f{document.documentType}'

    def _populateProjectInformation(self, pyutProject: Element):
        self._projectInformation.version  = pyutProject['version']
        self._projectInformation.codePath = pyutProject['CodePath']

    def _updateCurrentDocumentInformation(self, pyutDocument: Element) -> Document:

        documentInformation: Document = Document()

        documentTitle: DocumentTitle = DocumentTitle(pyutDocument['title'])

        documentInformation.documentType = pyutDocument['type']
        documentInformation.documentTitle = documentTitle

        documentInformation.scrollPositionX = int(pyutDocument['scrollPositionX'])
        documentInformation.scrollPositionY = int(pyutDocument['scrollPositionY'])
        documentInformation.pixelsPerUnitX  = int(pyutDocument['pixelsPerUnitX'])
        documentInformation.pixelsPerUnitY  = int(pyutDocument['pixelsPerUnitY'])

        self.logger.debug(f'{documentInformation=}')

        return documentInformation

    def _graphicClassesToOglClasses(self, pyutDocument: Element) -> UntangledOglClasses:

        oglClasses: UntangledOglClasses = createUntangledOglClassesFactory()
        for graphicClass in pyutDocument.GraphicClass:
            self.logger.debug(f'{graphicClass=}')

            graphicInformation: GraphicInformation = toGraphicInfo(graphicElement=graphicClass)
            oglClass: OglClass = OglClass(w=graphicInformation.width, h=graphicInformation.height)
            oglClass.SetPosition(x=graphicInformation.x, y=graphicInformation.y)

            pyutClass: PyutClass = self._untanglePyut.classToPyutClass(graphicClass=graphicClass)
            oglClass.pyutObject = pyutClass
            oglClasses.append(oglClass)

        return oglClasses

    def _graphicNotesToOglNotes(self, pyutDocument: Element) -> UntangledOglNotes:
        """

        Args:
            pyutDocument:

        Returns: untangled OglNote objects if any exist, else an empty list
        """
        oglNotes: UntangledOglNotes = createUntangledOglNotesFactory()

        graphicNotes: Element = pyutDocument.get_elements('GraphicNote')
        for graphicNote in graphicNotes:
            self.logger.debug(f'{graphicNote}')

            graphicInformation: GraphicInformation = toGraphicInfo(graphicElement=graphicNote)
            oglNote:            OglNote            = OglNote(w=graphicInformation.width, h=graphicInformation.height)
            oglNote.SetPosition(x=graphicInformation.x, y=graphicInformation.y)

            pyutNote: PyutNote = self._untanglePyut.noteToPyutNote(graphicNote=graphicNote)
            oglNote.pyutObject = pyutNote
            oglNotes.append(oglNote)

        return oglNotes

    def _graphicalTextToOglTexts(self, pyutDocument: Element) -> UntangledOglTexts:
        """
        Yeah, yeah, I know bad English;

        Args:
            pyutDocument:  The Element document

        Returns:  untangled OglText objects if any exist, else an empty list
        """
        oglTexts: UntangledOglTexts = createUntangledOglTextsFactory()

        graphicTexts: Element = pyutDocument.get_elements('GraphicText')
        for graphicText in graphicTexts:
            self.logger.debug(f'{graphicText}')

            graphicInformation: GraphicInformation = toGraphicInfo(graphicElement=graphicText)
            pyutText:           PyutText           = self._untanglePyut.textToPyutText(graphicText=graphicText)
            oglText:            OglText            = OglText(pyutText=pyutText, width=graphicInformation.width, height=graphicInformation.height)
            oglText.SetPosition(x=graphicInformation.x, y=graphicInformation.y)
            oglText.pyutText = pyutText
            oglTexts.append(oglText)

        return oglTexts

    def _getRawXml(self) -> str:

        try:
            with open(self._fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e

        return xmlString
