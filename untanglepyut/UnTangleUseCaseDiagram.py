
from logging import Logger
from logging import getLogger

from ogl.OglActor import OglActor
from pyutmodel.PyutActor import PyutActor
from untangle import Element

from untanglepyut.Common import GraphicInformation
from untanglepyut.Common import createUntangledOglActorsFactory
from untanglepyut.Common import toGraphicInfo

from untanglepyut.Types import UntangledOglActors
from untanglepyut.UnTanglePyut import UnTanglePyut


class UnTangleUseCaseDiagram:
    """
        <PyutDocument type="USECASE_DIAGRAM" title="Use-Cases" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
            <GraphicActor width="87" height="114" x="293" y="236">
                <Actor id="1" name="BasicActor" filename=""/>
            </GraphicActor>
            <GraphicUseCase width="100" height="60" x="575" y="250">
                <UseCase id="2" name="Basic Use Case" filename=""/>
            </GraphicUseCase>
            <GraphicLink srcX="379" srcY="286" dstX="575" dstY="280" spline="False">
                <LabelCenter x="555" y="281"/>
                <LabelSrc x="555" y="281"/>
                <LabelDst x="555" y="281"/>
                <Link name="Kicks Butt" type="ASSOCIATION" cardSrc="" cardDestination="" bidir="False" sourceId="1" destId="2"/>
            </GraphicLink>
        </PyutDocument>
    """

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._untangledOglActors: UntangledOglActors = createUntangledOglActorsFactory()
        self._untanglePyut:       UnTanglePyut       = UnTanglePyut()

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:

        Returns:
        """

        self._untangledOglActors = self._unTangleOglActors(pyutDocument=pyutDocument)

    @property
    def oglActors(self) -> UntangledOglActors:
        return self._untangledOglActors

    def _unTangleOglActors(self, pyutDocument: Element) -> UntangledOglActors:
        untangledOglActors: UntangledOglActors = createUntangledOglActorsFactory()

        graphicActors: Element = pyutDocument.get_elements('GraphicActor')
        for graphicActor in graphicActors:
            graphicInfo: GraphicInformation = toGraphicInfo(graphicActor)
            oglActor:    OglActor           = OglActor(w=graphicInfo.width, h=graphicInfo.height)
            oglActor.SetPosition(x=graphicInfo.x, y=graphicInfo.y)

            pyutActor: PyutActor = self._untanglePyut.actorToPyutActor(graphicActor=graphicActor)

            oglActor.pyutObject = pyutActor

            untangledOglActors.append(oglActor)

        return untangledOglActors
