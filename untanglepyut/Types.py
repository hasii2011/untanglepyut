
from typing import List
from typing import NewType
from typing import Union

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglInterface2 import OglInterface2
from ogl.OglUseCase import OglUseCase

UntangledOglClasses    = NewType('UntangledOglClasses', List[OglClass])
UntangledLinks         = Union[OglLink, OglInterface2]

UntangledOglLinks      = NewType('UntangledOglLinks',  List[UntangledLinks])
UntangledOglNotes      = NewType('UntangledOglNotes',  List[OglNote])
UntangledOglTexts      = NewType('UntangledOglTexts',  List[OglText])
UntangledOglActors     = NewType('UntangledOglActors', List[OglActor])
UntangledOglUseCases   = NewType('UntangledOglUseCases',  List[OglUseCase])