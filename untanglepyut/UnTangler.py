
from typing import Dict
from typing import List
from typing import NewType

from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation

from ogl.OglClass import OglClass
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglNoteLink import OglNoteLink
from ogl.OglText import OglText

from pyutmodel.PyutClass import PyutClass

from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutText import PyutText

from untangle import parse
from untangle import Element

from untanglepyut.UnTanglePyut import UnTanglePyut


@dataclass
class ProjectInformation:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)


UntangledLinks         = Union[OglLink, OglInterface2]
UntangledOglClasses    = NewType('UntangledOglClasses',    List[OglClass])
UntangledOglLinks      = NewType('UntangledOglLinks',      List[UntangledLinks])
UntangledControlPoints = NewType('UntangledControlPoints', List[ControlPoint])
UntangledOglNotes      = NewType('UntangledOglNotes',      List[OglNote])
UntangledOglTexts      = NewType('UntangledOglTexts',      List[OglText])

OglClassDictionary = NewType('OglClassDictionary', Dict[int, OglClass])
OglNotesDictionary = NewType('OglNotesDictionary', Dict[int, OglNote])


def createUntangledOglClassesFactory() -> UntangledOglClasses:
    """
    Factory method to create  the UntangledClasses data structure;

    Returns:  A new data structure
    """
    return UntangledOglClasses([])


def createUntangledOglLinksFactory() -> UntangledOglLinks:
    return UntangledOglLinks([])


def createUntangledOglNotesFactory() -> UntangledOglNotes:
    return UntangledOglNotes([])


def createUntangledOglTextsFactory() -> UntangledOglTexts:
    return UntangledOglTexts([])


def createOglClassDictionaryFactory() -> OglClassDictionary:
    return OglClassDictionary({})


def createOglNotesDictionaryFactory() -> OglNotesDictionary:
    return OglNotesDictionary({})


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
    oglTexts:        UntangledOglTexts    = field(default_factory=createUntangledOglTextsFactory)


DocumentTitle = NewType('DocumentTitle', str)
Documents     = NewType('Documents', dict[DocumentTitle, Document])


@dataclass
class GraphicInformation:
    """
    Internal Class use to move information from a Graphic XML element
    into Python
    """
    x: int = -1
    y: int = -1
    width:  int = -1
    height: int = -1


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

        self._untanglePyut: UnTanglePyut = UnTanglePyut()

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
                document.oglLinks   = self._graphicLinksToOglLink(pyutDocument, oglClasses=document.oglClasses, oglNotes=document.oglNotes)
            elif document.documentType == 'SEQUENCE_DIAGRAM':
                self.logger.warning(f'{document.documentType} unsupported')
            elif document.documentType == 'USECASE_DIAGRAM':
                self.logger.warning(f'{document.documentType} unsupported')
            else:
                assert False, f'Unknown document type: {document.documentType}'

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

            graphicInformation: GraphicInformation = self._toGraphicInfo(graphicElement=graphicClass)
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

            graphicInformation: GraphicInformation = self._toGraphicInfo(graphicElement=graphicNote)
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

            graphicInformation: GraphicInformation = self._toGraphicInfo(graphicElement=graphicText)
            pyutText:           PyutText           = self._untanglePyut.textToPyutText(graphicText=graphicText)
            oglText:            OglText            = OglText(pyutText=pyutText, width=graphicInformation.width, height=graphicInformation.height)
            oglText.SetPosition(x=graphicInformation.x, y=graphicInformation.y)
            oglText.pyutText = pyutText
            oglTexts.append(oglText)

        return oglTexts

    def _graphicLinksToOglLink(self, pyutDocument: Element, oglClasses: UntangledOglClasses, oglNotes: UntangledOglNotes) -> UntangledOglLinks:

        oglClassDictionary: OglClassDictionary = self._buildOglClassDictionary(oglClasses)
        oglNotesDictionary: OglNotesDictionary = self._buildOglNotesDictionary(oglNotes)

        oglLinks: UntangledOglLinks = createUntangledOglLinksFactory()

        graphicLinks: Element = pyutDocument.get_elements('GraphicLink')
        for graphicLink in graphicLinks:
            oglLink: OglLink = self._graphicLinkToOglLink(graphicLink, oglClassDictionary=oglClassDictionary, oglNotesDictionary=oglNotesDictionary)
            oglLinks.append(oglLink)

        graphicLollipops: Element = pyutDocument.get_elements('GraphicLollipop')
        for graphicLollipop in graphicLollipops:
            oglInterface2: OglInterface2 = self._graphicLollipopToOglInterface(graphicLollipop, oglClassDictionary)
            oglLinks.append(oglInterface2)

        return oglLinks

    def _graphicLinkToOglLink(self, graphicLink: Element, oglClassDictionary: OglClassDictionary, oglNotesDictionary: OglNotesDictionary) -> OglLink:
        """
        This code is way too convoluted.  Failing to do any of these step in this code leads to BAD
        visual representations.
        TODO:  Figure out how to simplify this code and/or make it more readable and obvious on how to create
        links (of whatever kind) between 2 OglClass'es

        Args:
            graphicLink:        The XML `GraphicClass` element
            oglClassDictionary: A dictionary indexed by an ID that returns an appropriate OglClass instance

        Returns:  A fully formed OglLink including control points

        """

        assert len(oglClassDictionary) != 0, 'Developer forgot to create dictionary'
        srcX: int = int(graphicLink['srcX'])
        srcY: int = int(graphicLink['srcY'])
        dstX: int = int(graphicLink['dstX'])
        dstY: int = int(graphicLink['dstY'])

        spline: bool = self._str2bool(graphicLink['spline'])

        links: Element = graphicLink.get_elements('Link')
        assert len(links) == 1, 'Should only ever one'

        singleLink:  Element = links[0]
        sourceId:    int = int(singleLink['sourceId'])
        dstId:       int = int(singleLink['destId'])
        self.logger.debug(f'graphicLink= {srcX=} {srcY=} {dstX=} {dstY=}')

        try:
            if singleLink['type'] == 'NOTELINK':
                dstShape: OglClass = oglClassDictionary[dstId]
                srcShape: Union[OglClass, OglNote] = oglNotesDictionary[sourceId]
            else:
                srcShape = oglClassDictionary[sourceId]
                dstShape = oglClassDictionary[dstId]
        except KeyError as ke:
            self.logger.error(f'Developer Error -- srcId: {sourceId} - dstId: {dstId}  KeyError index: {ke}')
            return cast(OglLink, None)

        pyutLink: PyutLink = self._untanglePyut.linkToPyutLink(singleLink, source=srcShape.pyutObject, destination=dstShape.pyutObject)
        oglLink:  OglLink  = self._createOglLink(srcShape=srcShape, pyutLink=pyutLink, destShape=dstShape,
                                                 linkType=pyutLink.linkType,
                                                 srcPos=(srcX, srcY),
                                                 dstPos=(dstX, dstY)
                                                 )
        srcShape.addLink(oglLink)
        dstShape.addLink(oglLink)
        oglLink.SetSpline(spline)
        controlPoints: UntangledControlPoints = self._generateControlPoints(graphicLink=graphicLink)

        # put the anchors at the right position
        srcAnchor = oglLink.GetSource()
        dstAnchor = oglLink.GetDestination()
        srcAnchor.SetPosition(srcX, srcY)
        dstAnchor.SetPosition(dstX, dstY)

        # add the control points to the line
        line   = srcAnchor.GetLines()[0]     # only 1 line per anchor in Pyut
        parent = line.GetSource().GetParent()
        selfLink: bool = parent is oglLink.GetDestination().GetParent()

        for controlPoint in controlPoints:
            oglLink.AddControl(controlPoint)
            if selfLink:
                x, y = controlPoint.GetPosition()
                controlPoint.SetParent(parent)
                controlPoint.SetPosition(x, y)
        return oglLink

    def _graphicLollipopToOglInterface(self, graphicLollipop: Element, oglClassDictionary: OglClassDictionary) -> OglInterface2:
        assert len(oglClassDictionary) != 0, 'Developer forgot to create dictionary'

        x: int = int(graphicLollipop['x'])
        y: int = int(graphicLollipop['y'])
        attachmentLocationStr: str                = graphicLollipop['attachmentPoint']
        attachmentLocation:    AttachmentLocation = AttachmentLocation.toEnum(attachmentLocationStr)
        self.logger.debug(f'{x=},{y=}')

        elements: Element = graphicLollipop.get_elements('Interface')
        assert len(elements) == 1, 'If more than one interface tag the XML is invalid'
        interfaceElement: Element           = elements[0]
        pyutInterface:    PyutInterface     = self._untanglePyut.interfaceToPyutInterface(interface=interfaceElement)
        oglClass:         OglClass          = self._getOglClassFromName(pyutInterface.implementors[0], oglClassDictionary)
        anchorPoint:      SelectAnchorPoint = SelectAnchorPoint(x=x, y=y, attachmentPoint=attachmentLocation, parent=oglClass)
        oglInterface2:    OglInterface2     = OglInterface2(pyutInterface=pyutInterface, destinationAnchor=anchorPoint)

        return oglInterface2

    def _getOglClassFromName(self, className: str, oglClassDictionary: OglClassDictionary) -> OglClass:

        foundClass: OglClass = cast(OglClass, None)
        for oglClass in oglClassDictionary.values():
            if oglClass.pyutObject.name == className:
                foundClass = oglClass
                break
        assert foundClass is not None, 'XML must be in error'
        return foundClass

    def _generateControlPoints(self, graphicLink: Element) -> UntangledControlPoints:

        controlPoints: UntangledControlPoints = UntangledControlPoints([])

        controlPointElements: Element = graphicLink.get_elements('ControlPoint')
        for controlPointElement in controlPointElements:
            x: int = int(controlPointElement['x'])
            y: int = int(controlPointElement['y'])
            controlPoint: ControlPoint = ControlPoint(x=x, y=y)
            controlPoints.append(controlPoint)

        return controlPoints

    def _buildOglClassDictionary(self, oglClasses: UntangledOglClasses) -> OglClassDictionary:
        """
        Map class id to OglClass
        Args:
            oglClasses:

        Returns:  The dictionary
        """
        oglClassDictionary: OglClassDictionary = createOglClassDictionaryFactory()

        for oglClass in oglClasses:
            classId: int = oglClass.pyutObject.id
            oglClassDictionary[classId] = oglClass

        return oglClassDictionary

    def _buildOglNotesDictionary(self, oglNotes: UntangledOglNotes) -> OglNotesDictionary:
        """
        Map note ID to OglNote
        Args:
            oglNotes:

        Returns:  The dictionary
        """
        oglNotesDictionary: OglNotesDictionary = createOglNotesDictionaryFactory()

        for oglNote in oglNotes:
            noteId: int = oglNote.pyutObject.id
            oglNotesDictionary[noteId] = oglNote

        return oglNotesDictionary

    def _createOglLink(self, srcShape, pyutLink, destShape, linkType: PyutLinkType, srcPos=None, dstPos=None):
        """
        Used to get a OglLink of the given linkType.

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            destShape:  Destination shape
            linkType:   The linkType of the link (OGL_INHERITANCE, ...)
            srcPos:     source position
            dstPos:     destination position

        Returns:  The requested link
        """
        if linkType == PyutLinkType.AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.SD_MESSAGE:
            assert False, 'Sequence Diagram Messages not supported'
            # return OglSDMessage(srcShape=srcShape, pyutSDMessage=pyutLink, dstShape=destShape)
        else:
            self.logger.error(f"Unknown OglLinkType: {linkType}")
            return None

    def _str2bool(self, strValue: str) -> bool:
        """
        Converts a know set of strings to a boolean value

        TODO: Put in common place;  Also, in UnTanglePyut

        Args:
            strValue:

        Returns:  the boolean value
        """
        return strValue.lower() in ("yes", "true", "t", "1", 'True')

    def _toGraphicInfo(self, graphicElement: Element) -> GraphicInformation:
        graphicInformation: GraphicInformation = GraphicInformation()

        graphicInformation.x = int(graphicElement['x'])
        graphicInformation.y = int(graphicElement['y'])

        graphicInformation.width  = int(graphicElement['width'])
        graphicInformation.height = int(graphicElement['height'])

        return graphicInformation

    def _getRawXml(self) -> str:

        try:
            with open(self._fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e

        return xmlString
