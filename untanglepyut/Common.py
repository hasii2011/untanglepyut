from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import NewType

from untangle import Element

from miniogl.ControlPoint import ControlPoint

from ogl.OglClass import OglClass
from ogl.OglNote import OglNote

from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import UntangledOglUseCases

OglClassDictionary    = NewType('OglClassDictionary',    Dict[int, OglClass])
OglNotesDictionary    = NewType('OglNotesDictionary',    Dict[int, OglNote])
OglUseCasesDictionary = NewType('OglUseCasesDictionary', Dict[int, OglNote])

UntangledControlPoints = NewType('UntangledControlPoints', List[ControlPoint])


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


"""
Factory methods for our dataclasses
"""


def createUntangledOglLinks() -> UntangledOglLinks:
    return UntangledOglLinks([])


def createUntangledOglUseCases() -> UntangledOglUseCases:
    return UntangledOglUseCases([])


def createUntangledOglActors() -> UntangledOglActors:
    return UntangledOglActors([])


def createOglClassDictionary() -> OglClassDictionary:
    return OglClassDictionary({})


def createOglNotesDictionary() -> OglNotesDictionary:
    return OglNotesDictionary({})


def createOglUseCasesDictionary() -> OglUseCasesDictionary:
    return OglUseCasesDictionary({})


def str2bool(strValue: str) -> bool:
    """
    Converts a known set of strings to a boolean value

    TODO: Put in common place;  Also, in UnTanglePyut

    Args:
        strValue:

    Returns:  the boolean value
    """
    return strValue.lower() in ("yes", "true", "t", "1", 'True')


def toGraphicInfo(graphicElement: Element) -> GraphicInformation:
    graphicInformation: GraphicInformation = GraphicInformation()

    graphicInformation.x = int(graphicElement['x'])
    graphicInformation.y = int(graphicElement['y'])

    graphicInformation.width  = int(graphicElement['width'])
    graphicInformation.height = int(graphicElement['height'])

    return graphicInformation
