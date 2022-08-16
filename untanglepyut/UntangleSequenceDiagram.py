
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from untangle import Element

# from pyutmodel.PyutSDInstance import PyutSDInstance
# from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

# from untanglepyut.Common import GraphicInformation
# from untanglepyut.Common import toGraphicInfo

OglSDInstances = NewType('OglSDInstances', List[OglSDInstance])
OGLSDMessages  = NewType('OGLSDMessages',  List[OglSDMessage])


def createOglSDInstances() -> OglSDInstances:
    return OglSDInstances([])


def createOGLSDMessages() -> OGLSDMessages:
    return OGLSDMessages([])


class UntangleSequenceDiagram:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._oglSDInstances: OglSDInstances = createOglSDInstances()
        self._oglSDMessages:  OGLSDMessages  = createOGLSDMessages()

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:  The pyut untangle element that represents a sequence diagram
        """
        self._oglSDInstances = self._untangleSDInstances(pyutDocument=pyutDocument)

        self.logger.error('Not yet supported')

    @property
    def oglSDInstances(self) -> OglSDInstances:
        return self._oglSDInstances

    @property
    def oglSDMessages(self) -> OGLSDMessages:
        return self._oglSDMessages

    def _untangleSDInstances(self, pyutDocument: Element) -> OglSDInstances:

        oglSDInstances: OglSDInstances = createOglSDInstances()

        # noinspection PyUnusedLocal
        graphicSDInstances: Element = pyutDocument.get_elements('GraphicSDInstance')
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
