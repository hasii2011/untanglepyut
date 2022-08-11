
from typing import Dict
from typing import List
from typing import NewType

from miniogl.ControlPoint import ControlPoint

from ogl.OglClass import OglClass
from ogl.OglNote import OglNote

from untanglepyut.Types import UntangledOglLinks

OglClassDictionary = NewType('OglClassDictionary', Dict[int, OglClass])
OglNotesDictionary = NewType('OglNotesDictionary', Dict[int, OglNote])

UntangledControlPoints = NewType('UntangledControlPoints', List[ControlPoint])


def createUntangledOglLinksFactory() -> UntangledOglLinks:
    return UntangledOglLinks([])


def createOglNotesDictionaryFactory() -> OglNotesDictionary:
    return OglNotesDictionary({})


def createOglClassDictionaryFactory() -> OglClassDictionary:
    return OglClassDictionary({})


def str2bool(strValue: str) -> bool:
    """
    Converts a known set of strings to a boolean value

    TODO: Put in common place;  Also, in UnTanglePyut

    Args:
        strValue:

    Returns:  the boolean value
    """
    return strValue.lower() in ("yes", "true", "t", "1", 'True')
