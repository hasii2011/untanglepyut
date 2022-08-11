
from logging import Logger
from logging import getLogger
from typing import Union
from typing import cast

from untangle import Element

from pyutmodel.PyutLinkType import PyutLinkType

from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglNote import OglNote
from ogl.OglNoteLink import OglNoteLink

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2

from untanglepyut.Common import OglClassDictionary
from untanglepyut.Common import OglNotesDictionary
from untanglepyut.Common import UntangledControlPoints
from untanglepyut.Common import UntangledOglLinks
from untanglepyut.Common import createOglClassDictionaryFactory
from untanglepyut.Common import createOglNotesDictionaryFactory
from untanglepyut.Common import createUntangledOglLinksFactory
from untanglepyut.Common import str2bool

from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglNotes

from untanglepyut.UnTanglePyut import UnTanglePyut


class UnTangleOglLinks:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut:     UnTanglePyut     = UnTanglePyut()

    def graphicLinksToOglLink(self, pyutDocument: Element, oglClasses: UntangledOglClasses, oglNotes: UntangledOglNotes) -> UntangledOglLinks:

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

        spline: bool = str2bool(graphicLink['spline'])

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
