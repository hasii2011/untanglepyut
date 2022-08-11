
from typing import List
from typing import NewType
from typing import Union

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglInterface2 import OglInterface2

UntangledOglClasses    = NewType('UntangledOglClasses', List[OglClass])
UntangledLinks         = Union[OglLink, OglInterface2]

UntangledOglLinks      = NewType('UntangledOglLinks', List[UntangledLinks])
UntangledOglNotes      = NewType('UntangledOglNotes', List[OglNote])
UntangledOglTexts      = NewType('UntangledOglTexts', List[OglText])
