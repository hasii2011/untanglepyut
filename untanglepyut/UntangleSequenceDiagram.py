from typing import Dict
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage
from untangle import Element

# from pyutmodel.PyutSDInstance import PyutSDInstance
# from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from untanglepyut.Common import GraphicInformation

# from untanglepyut.Common import GraphicInformation
# from untanglepyut.Common import toGraphicInfo

OglSDInstances = NewType('OglSDInstances', List[OglSDInstance])
OglSDMessages  = NewType('OglSDMessages',  Dict[int, OglSDMessage])


def createOglSDInstances() -> OglSDInstances:
    return OglSDInstances([])


def createOglSDMessages() -> OglSDMessages:
    return OglSDMessages({})


class UntangleSequenceDiagram:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._oglSDInstances: OglSDInstances = createOglSDInstances()
        self._oglSDMessages:  OglSDMessages  = createOglSDMessages()

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:  The pyut untangle element that represents a sequence diagram
        """
        self._oglSDInstances = self._untangleSDInstances(pyutDocument=pyutDocument)

        self.logger.warning('Not yet supported')

    @property
    def oglSDInstances(self) -> OglSDInstances:
        return self._oglSDInstances

    @property
    def oglSDMessages(self) -> OglSDMessages:
        return self._oglSDMessages

    def _untangleSDMessage(self, pyutDocument: Element) -> OglSDMessages:

        oglSDMessages: OglSDMessages = createOglSDMessages()
        graphicSDMessages: List[Element] = pyutDocument.get_elements('GraphicSDMessage')

        for graphicSDMessage in graphicSDMessages:
            pyutSDMessage: PyutSDMessage = PyutSDMessage()

            srcID:   int = int(graphicSDMessage['srcID'])
            dstID:   int = int(graphicSDMessage['dstId'])
            srcTime: int = int(graphicSDMessage['srcTime'])
            dstTime: int = int(graphicSDMessage['dstTime'])
            srcOgl = self._oglSDInstances[srcID]
            dstOgl = self._oglSDInstances[dstID]

            pyutSDMessage.id = int(graphicSDMessage['id'])
            pyutSDMessage.setMessage(graphicSDMessage['message'])

        return oglSDMessages

    def _untangleSDInstances(self, pyutDocument: Element) -> OglSDInstances:

        oglSDInstances: OglSDInstances = createOglSDInstances()

        # noinspection PyUnusedLocal
        graphicSDInstances: List[Element] = pyutDocument.get_elements('GraphicSDInstance')
        #
        # for graphicSDInstance in graphicSDInstances:
        #     self.logger.info(f'{graphicSDInstance=}')
        #     pyutSDInstance: PyutSDInstance = PyutSDInstance()
        #     oglSDInstance:  OglSDInstance  = OglSDInstance(pyutSDInstance, umlFrame)
        #
        #     graphicInfo: GraphicInformation = toGraphicInfo(graphicElement=graphicSDInstance)
        #     oglSDInstance.SetSize(w, h)
        #     oglSDInstance.SetPosition(x, y)

        return oglSDInstances
