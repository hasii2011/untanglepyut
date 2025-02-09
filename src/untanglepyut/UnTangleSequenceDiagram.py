
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglActor import OglActor
from pyutmodelv2.PyutLink import PyutLink
from untangle import Element

from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from ogl.OglAssociation import OglAssociation

from untanglepyut import XmlConstants
from untanglepyut.Types import Elements

from untanglepyut.Types import GraphicInformation
from untanglepyut.Types import GraphicLinkAttributes
from untanglepyut.Types import LinkableOglObject
from untanglepyut.Types import LinkableOglObjects
from untanglepyut.Types import OglSDInstances
from untanglepyut.Types import OglSDMessages
from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import createLinkableOglObjects
from untanglepyut.Types import createOglSDInstances
from untanglepyut.Types import createOglSDMessages
from untanglepyut.Types import createUntangledOglActors
from untanglepyut.Types import createUntangledOglLinks
from untanglepyut.UnTangleOglLinks import UnTangleOglLinks

from untanglepyut.UnTanglePyut import ConvolutedPyutSDMessageInformation
from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.UnTangleUseCaseDiagram import UnTangleUseCaseDiagram

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.BaseUnTangle import BaseUnTangle


class UnTangleSequenceDiagram(BaseUnTangle):

    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion)

        self.logger: Logger = getLogger(__name__)

        self._oglSDInstances: OglSDInstances     = createOglSDInstances()
        self._oglSDMessages:  OglSDMessages      = createOglSDMessages()
        self._oglActors:      UntangledOglActors = createUntangledOglActors()
        self._oglLinks:       UntangledOglLinks  = createUntangledOglLinks()

        self._untanglePyut: UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)
        #
        # Need some help
        #
        self._untangleUseCaseStuff: UnTangleUseCaseDiagram = UnTangleUseCaseDiagram(xmlVersion=xmlVersion)
        self._untangleLinks:        UnTangleOglLinks       = UnTangleOglLinks(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementInstance:   str = XmlConstants.V10_ELEMENT_INSTANCE
            self._elementMessage:    str = XmlConstants.V10_ELEMENT_MESSAGE
            self._elementOglLink:    str = XmlConstants.V10_ELEMENT_OGL_LINK
            self._elementLink:       str = XmlConstants.V10_ELEMENT_LINK
            self._attrSourceId:      str = XmlConstants.V10_ATTR_SOURCE_ID
            self._attrDestinationId: str = XmlConstants.V10_ATTR_DESTINATION_ID

        else:
            self._elementInstance   = XmlConstants.V11_ELEMENT_INSTANCE
            self._elementMessage    = XmlConstants.V11_ELEMENT_MESSAGE
            self._elementOglLink    = XmlConstants.V11_ELEMENT_OGL_LINK
            self._elementLink       = XmlConstants.V11_ELEMENT_LINK
            self._attrSourceId      = XmlConstants.V11_ATTR_SOURCE_ID
            self._attrDestinationId = XmlConstants.V11_ATTR_DESTINATION_ID

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:  The pyut untangle element that represents a sequence diagram
        """
        self._oglSDInstances = self._untangleSDInstances(pyutDocument=pyutDocument)
        self._oglSDMessages  = self._untangleSDMessages(pyutDocument=pyutDocument)

        self._untangleUseCaseStuff.unTangle(pyutDocument=pyutDocument)

        self._oglActors = self._untangleUseCaseStuff.oglActors

        linkableOglObjects: LinkableOglObjects = self._buildLinkableObjects()
        # self._oglLinks       = self._untangleLinks.unTangle(pyutDocument=pyutDocument, linkableOglObjects=linkableOglObjects)
        self._oglLinks       = self._connectActorsToSDInstances(pyutDocument=pyutDocument, linkableOglObjects=linkableOglObjects)

    @property
    def oglSDInstances(self) -> OglSDInstances:
        return self._oglSDInstances

    @property
    def oglSDMessages(self) -> OglSDMessages:
        return self._oglSDMessages

    @property
    def oglActors(self) -> UntangledOglActors:
        return self._oglActors

    @property
    def oglLinks(self) -> UntangledOglLinks:
        return self._oglLinks

    def _untangleSDInstances(self, pyutDocument: Element) -> OglSDInstances:

        oglSDInstances:     OglSDInstances = createOglSDInstances()
        graphicSDInstances: List[Element]  = pyutDocument.get_elements(self._elementInstance)

        for graphicSDInstance in graphicSDInstances:
            self.logger.debug(f'{graphicSDInstance=}')
            pyutSDInstance: PyutSDInstance     = self._untanglePyut.sdInstanceToPyutSDInstance(oglSDInstanceElement=graphicSDInstance)

            oglSDInstance:  OglSDInstance      = OglSDInstance(pyutSDInstance)
            graphicInfo:    GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicSDInstance)

            oglSDInstance.SetSize(width=graphicInfo.width, height=graphicInfo.height)
            oglSDInstance.SetPosition(x=graphicInfo.x, y=graphicInfo.y)

            self._updateModel(oglObject=oglSDInstance, graphicInformation=graphicInfo)

            oglSDInstances[pyutSDInstance.id] = oglSDInstance
        return oglSDInstances

    def _untangleSDMessages(self, pyutDocument: Element) -> OglSDMessages:

        oglSDMessages:     OglSDMessages = createOglSDMessages()
        graphicSDMessages: List[Element] = pyutDocument.get_elements(self._elementMessage)

        for graphicSDMessage in graphicSDMessages:
            bogus: ConvolutedPyutSDMessageInformation = self._untanglePyut.sdMessageToPyutSDMessage(oglSDMessageElement=graphicSDMessage)

            pyutSDMessage: PyutSDMessage = bogus.pyutSDMessage

            srcInstance: OglSDInstance = self._oglSDInstances[bogus.sourceId]
            dstInstance: OglSDInstance = self._oglSDInstances[bogus.destinationId]

            pyutSDMessage.source      = srcInstance.pyutSDInstance         # Ugh, time was set by sdMessageToPyutSDMessage
            pyutSDMessage.destination = dstInstance.pyutSDInstance         # This "split" functionality must be fixed

            oglSDMessage: OglSDMessage = OglSDMessage(srcSDInstance=srcInstance, pyutSDMessage=pyutSDMessage, dstSDInstance=dstInstance)

            oglSDMessages[pyutSDMessage.id] = oglSDMessage

        return oglSDMessages

    def _connectActorsToSDInstances(self, pyutDocument: Element, linkableOglObjects: LinkableOglObjects) -> UntangledOglLinks:

        oglLinks: UntangledOglLinks = createUntangledOglLinks()

        # US Agency for International Development must go away

        graphicLinks: Elements = cast(Elements, pyutDocument.get_elements(self._elementOglLink))
        for graphicLink in graphicLinks:
            oglAssociation: OglAssociation = self._createActorLink(graphicLink=graphicLink, linkableOglObjects=linkableOglObjects)
            oglLinks.append(oglAssociation)

        return oglLinks

    def _createActorLink(self, graphicLink: Element, linkableOglObjects: LinkableOglObjects) -> OglAssociation:
        """

        Args:
            graphicLink:
            linkableOglObjects:

        Returns:
        """

        links: Elements = cast(Elements, graphicLink.get_elements(self._elementLink))
        assert len(links) == 1, 'Should only ever be one'

        singleLink: Element = links[0]
        sourceId, dstId     = self._linkIDs(singleLink=singleLink)
        try:
            srcShape: LinkableOglObject = linkableOglObjects[sourceId]
            dstShape: OglSDInstance     = linkableOglObjects[dstId]        # type: ignore
        except KeyError as ke:
            self.logger.error(f'{linkableOglObjects=}')
            self.logger.error(f'Developer Error -- {singleLink=}')
            self.logger.error(f'Developer Error -- {sourceId=} {dstId=}  KeyError index: {ke}')
            return cast(OglAssociation, None)

        assert isinstance(srcShape, OglActor),      'Developer Error'
        assert isinstance(dstShape, OglSDInstance), 'Developer Error'

        pyutLink: PyutLink              = self._untanglePyut.linkToPyutLink(singleLink, source=srcShape.pyutObject, destination=dstShape.pyutSDInstance)
        gla:      GraphicLinkAttributes = GraphicLinkAttributes.fromGraphicLink(xmlVersion=self._xmlVersion, graphicLink=graphicLink)

        self.logger.debug(f'graphicLink= {gla.srcX=} {gla.srcY=} {gla.dstX=} {gla.dstY=} {gla.spline=}')

        oglAssociation: OglAssociation = OglAssociation(srcShape=srcShape,
                                                        pyutLink=pyutLink,
                                                        dstShape=dstShape,
                                                        srcPos=(gla.srcX, gla.srcY),
                                                        dstPos=(gla.dstX, gla.dstY)
                                                        )
        # put the anchors at the right position
        srcAnchor = oglAssociation.sourceAnchor
        dstAnchor = oglAssociation.destinationAnchor
        srcAnchor.SetPosition(gla.srcX, gla.srcY)
        dstAnchor.SetPosition(gla.dstX, gla.dstY)

        srcModel = srcAnchor.model
        srcModel.SetPosition(x=gla.srcX, y=gla.srcY)
        dstModel = dstAnchor.model
        dstModel.SetPosition(x=gla.dstX, y=gla.dstY)
        #
        # Do not create association labels
        #
        return oglAssociation

    def _linkIDs(self, singleLink: Element) -> Tuple[int, int]:
        """
        Extracts the source and destination IDs
        Args:
            singleLink:

        Returns:  A tuple of sourceId,destinationId
        """

        sourceId:    int = int(singleLink[self._attrSourceId])
        dstId:       int = int(singleLink[self._attrDestinationId])

        return sourceId, dstId

    def _buildLinkableObjects(self) -> LinkableOglObjects:
        """

        Returns:  Linkable Objects Dictionary
        """

        linkableOglObjects: LinkableOglObjects = createLinkableOglObjects()

        for oglActor in self.oglActors:
            linkableOglObjects[oglActor.pyutObject.id] = oglActor

        for pyutID, oglSDInstance in self.oglSDInstances.items():
            linkableOglObjects[pyutID] = oglSDInstance              # type: ignore

        return linkableOglObjects
