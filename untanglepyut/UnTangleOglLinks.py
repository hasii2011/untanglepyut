from dataclasses import dataclass
from logging import Logger
from logging import getLogger
from typing import Dict
from typing import NewType
from typing import Union
from typing import cast

from untangle import Element

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink

from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglNoteLink import OglNoteLink
from ogl.OglNote import OglNote
from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2

from untanglepyut.Common import OglClassDictionary
from untanglepyut.Common import OglNotesDictionary
from untanglepyut.Common import UntangledControlPoints
from untanglepyut.Common import UntangledOglLinks
from untanglepyut.Common import createOglClassDictionary
from untanglepyut.Common import createOglNotesDictionary
from untanglepyut.Common import createUntangledOglLinks
from untanglepyut.Common import str2bool
from untanglepyut.Types import UntangledOglActors

from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglNotes
from untanglepyut.Types import UntangledOglUseCases

from untanglepyut.UnTanglePyut import UnTanglePyut


OglUseCasesDictionary = NewType('OglUseCasesDictionary', Dict[int, OglUseCase])
OglActorsDictionary   = NewType('OglActorsDictionary',   Dict[int, OglActor])


def createOgActorsDictionary() -> OglActorsDictionary:
    return OglActorsDictionary({})


def createOglUseCasesDictionary() -> OglUseCasesDictionary:
    return OglUseCasesDictionary({})


@dataclass
class GraphicLinkAttributes:

    srcX:   int = -1
    srcY:   int = -1
    dstX:   int = -1
    dstY:   int = -1
    spline: bool = False


def fromGraphicLink(graphicLink: Element) -> GraphicLinkAttributes:

    gla: GraphicLinkAttributes = GraphicLinkAttributes()
    gla.srcX = int(graphicLink['srcX'])
    gla.srcY = int(graphicLink['srcY'])
    gla.dstX = int(graphicLink['dstX'])
    gla.dstY = int(graphicLink['dstY'])

    gla.spline = str2bool(graphicLink['spline'])

    return gla


class UnTangleOglLinks:
    """
    Currently, unsupported:

    ```html
      <LabelCenter x="579" y="300"/>
      <LabelSrc x="579" y="300"/>
      <LabelDst x="579" y="300"/>
    ```
    See:
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut:     UnTanglePyut     = UnTanglePyut()

    def graphicLinksToOglLinks(self, pyutDocument: Element, oglClasses: UntangledOglClasses, oglNotes: UntangledOglNotes) -> UntangledOglLinks:
        """
        Convert from XML to Ogl Links

        Args:
            pyutDocument:  The Element that represents the Class Diagram XML
            oglClasses:    The current list of OGL classes
            oglNotes:      The current list of OGL Notes

        Returns:  The links between any of the above objects.  Also returns the graphic lollipop links
        """

        oglClassDictionary: OglClassDictionary = self._buildOglClassDictionary(oglClasses)
        oglNotesDictionary: OglNotesDictionary = self._buildOglNotesDictionary(oglNotes)

        oglLinks: UntangledOglLinks = createUntangledOglLinks()

        graphicLinks: Element = pyutDocument.get_elements('GraphicLink')
        for graphicLink in graphicLinks:
            oglLink: OglLink = self._graphicLinkToOglLink(graphicLink, oglClassDictionary=oglClassDictionary, oglNotesDictionary=oglNotesDictionary)
            oglLinks.append(oglLink)

        graphicLollipops: Element = pyutDocument.get_elements('GraphicLollipop')
        for graphicLollipop in graphicLollipops:
            oglInterface2: OglInterface2 = self._graphicLollipopToOglInterface(graphicLollipop, oglClassDictionary)
            oglLinks.append(oglInterface2)

        return oglLinks

    def graphicUseCaseLinksToOglLinks(self, pyutDocument: Element, oglActors: UntangledOglActors, oglUseCases: UntangledOglUseCases) -> UntangledOglLinks:
        """
        Convert from XML to Ogl Links

        Args:
            pyutDocument:  The Element that represents the Use Case Diagram XML
            oglActors:     The current list of OGL Actors
            oglUseCases:   The current list of OGL Use Cases

        Returns:  The links between the OGL Actors and the OGL Uses Cases
        """
        # noinspection PyUnusedLocal
        oglActorsDictionary:   OglActorsDictionary   = self._buildOglActorsDictionary(oglActors=oglActors)
        # noinspection PyUnusedLocal
        oglUseCasesDictionary: OglUseCasesDictionary = self._buildOglUseCasesDictionary(oglUseCases=oglUseCases)

        oglLinks: UntangledOglLinks = createUntangledOglLinks()

        graphicLinks: Element = pyutDocument.get_elements('GraphicLink')
        for graphicLink in graphicLinks:
            self.logger.info(f'{graphicLink}')

        return oglLinks

    def _buildOglClassDictionary(self, oglClasses: UntangledOglClasses) -> OglClassDictionary:
        """
        Map class id to OglClass
        Args:
            oglClasses:

        Returns:  The dictionary
        """
        oglClassDictionary: OglClassDictionary = createOglClassDictionary()

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
        oglNotesDictionary: OglNotesDictionary = createOglNotesDictionary()

        for oglNote in oglNotes:
            noteId: int = oglNote.pyutObject.id
            oglNotesDictionary[noteId] = oglNote

        return oglNotesDictionary

    def _buildOglActorsDictionary(self, oglActors: UntangledOglActors) -> OglActorsDictionary:
        """
        Map Actor ID to OglActor
        Args:
            oglActors:

        Returns:  The dictionary
        """
        oglActorsDictionary: OglActorsDictionary = createOgActorsDictionary()
        for oglActor in oglActors:
            actorId: int = oglActor.pyutObject.id
            oglActorsDictionary[actorId] = oglActor

        return oglActorsDictionary

    def _buildOglUseCasesDictionary(self, oglUseCases: UntangledOglUseCases) -> OglUseCasesDictionary:
        """
        Maps UseCase ID to OglUseCase
        Args:
            oglUseCases:

        Returns:  The dictionary
        """
        oglUseCasesDictionary: OglUseCasesDictionary = createOglUseCasesDictionary()

        for oglUseCase in oglUseCases:
            useCaseId: int = oglUseCase.pyutObject.id
            oglUseCasesDictionary[useCaseId] = oglUseCase

        return oglUseCasesDictionary

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
        gla: GraphicLinkAttributes = fromGraphicLink(graphicLink=graphicLink)

        links: Element = graphicLink.get_elements('Link')
        assert len(links) == 1, 'Should only ever be one'

        singleLink:  Element = links[0]
        sourceId:    int = int(singleLink['sourceId'])
        dstId:       int = int(singleLink['destId'])
        self.logger.debug(f'graphicLink= {gla.srcX=} {gla.srcY=} {gla.dstX=} {gla.dstY=} {gla.spline=}')

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
        oglLink:  OglLink  = self._oglLinkFactory(srcShape=srcShape, pyutLink=pyutLink, destShape=dstShape,
                                                  linkType=pyutLink.linkType,
                                                  srcPos=(gla.srcX, gla.srcY),
                                                  dstPos=(gla.dstX, gla.dstY)
                                                  )
        oglLink.SetSpline(gla.spline)
        srcShape.addLink(oglLink)
        dstShape.addLink(oglLink)

        # put the anchors at the right position
        srcAnchor = oglLink.GetSource()
        dstAnchor = oglLink.GetDestination()
        srcAnchor.SetPosition(gla.srcX, gla.srcY)
        dstAnchor.SetPosition(gla.dstX, gla.dstY)

        # add the control points to the line
        line   = srcAnchor.GetLines()[0]     # only 1 line per anchor in Pyut
        parent = line.GetSource().GetParent()
        selfLink: bool = parent is oglLink.GetDestination().GetParent()

        controlPoints: UntangledControlPoints = self._generateControlPoints(graphicLink=graphicLink)
        for controlPoint in controlPoints:
            oglLink.AddControl(controlPoint)
            if selfLink:
                x, y = controlPoint.GetPosition()
                controlPoint.SetParent(parent)
                controlPoint.SetPosition(x, y)
        return oglLink

    def _oglLinkFactory(self, srcShape, pyutLink, destShape, linkType: PyutLinkType, srcPos=None, dstPos=None):
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
        """
        Looks up a name in the class dictionary and return the associated class
        TODO: Make a simple lookup and catch any Key errors
        Args:
            className:
            oglClassDictionary:

        Returns:
        """

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
