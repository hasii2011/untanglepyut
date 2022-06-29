
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from ogl.OglClass import OglClass
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from untangle import parse
from untangle import Element


@dataclass
class ProjectInformation:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)


UntangledOglClasses  = NewType('UntangledOglClasses', List[OglClass])

UntangledPyutMethods          = NewType('UntangledPyutMethods', List[PyutMethod])


def createUntangledOglClassesFactory() -> UntangledOglClasses:
    """
    Factory method to create  the UntangledClasses data structure;

    Returns:  A new data structure
    """
    return UntangledOglClasses([])


@dataclass
class Document:
    documentType:    str = ''
    documentTitle:   str = ''
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses: UntangledOglClasses = field(default_factory=createUntangledOglClassesFactory)

    def __post_init__(self):
        self.oglClasses = UntangledOglClasses([])


DocumentTitle = NewType('DocumentTitle', str)
Documents     = NewType('Documents', dict[DocumentTitle, Document])


class UnTangler:

    def __init__(self, fqFileName: str):
        """

        Args:
            fqFileName:  Fully qualified file name
        """

        self.logger: Logger = getLogger(__name__)

        self._fqFileName:  str = fqFileName
        self._projectInformation: ProjectInformation = ProjectInformation()
        self._documents:          Documents          = Documents({})

    @property
    def projectInformation(self) -> ProjectInformation:
        """
        This property return nothing valid until you untangle the file

        Returns:  The project information of the untangled pyut file
        """
        return self._projectInformation

    @property
    def documents(self) -> Documents:
        return self._documents

    def untangle(self):

        xmlString:   str     = self._getRawXml()
        root:        Element = parse(xmlString)
        pyutProject: Element = root.PyutProject

        self._populateProjectInformation(pyutProject=pyutProject)

        for pyutDocument in pyutProject.PyutDocument:
            document: Document = self._updateCurrentDocumentInformation(pyutDocument=pyutDocument)

            self._documents[document.documentTitle] = document

            self.logger.debug(f'{document=}')
            document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)

    def _populateProjectInformation(self, pyutProject: Element):
        self._projectInformation.version  = pyutProject['version']
        self._projectInformation.codePath = pyutProject['CodePath']

    def _updateCurrentDocumentInformation(self, pyutDocument: Element) -> Document:

        documentInformation: Document = Document()

        documentTitle: DocumentTitle = DocumentTitle(pyutDocument['title'])

        documentInformation.documentType = pyutDocument['type']
        documentInformation.documentTitle = documentTitle
        documentInformation.scrollPositionX = pyutDocument['scrollPositionX']
        documentInformation.scrollPositionY = pyutDocument['scrollPositionY']
        documentInformation.pixelsPerUnitX = pyutDocument['pixelsPerUnitX']
        documentInformation.pixelsPerUnitY = pyutDocument['pixelsPerUnitY']

        self.logger.debug(f'{documentInformation=}')

        return documentInformation

    def _graphicClassesToOglClasses(self, pyutDocument: Element) -> UntangledOglClasses:

        oglClasses: UntangledOglClasses = createUntangledOglClassesFactory()
        for graphicClass in pyutDocument.GraphicClass:
            self.logger.debug(f'{graphicClass=}')

            x: int = int(graphicClass['x'])
            y: int = int(graphicClass['y'])
            width:  int = int(graphicClass['width'])
            height: int = int(graphicClass['height'])
            oglClass: OglClass = OglClass(w=width, h=height)
            oglClass.SetPosition(x=x, y=y)

            pyutClass: PyutClass = self._classToPyutClass(graphicClass=graphicClass)
            oglClass.pyutObject = pyutClass
            oglClasses.append(oglClass)

        return oglClasses

    def _classToPyutClass(self, graphicClass: Element) -> PyutClass:
        classElement: Element = graphicClass.Class

        pyutClass: PyutClass = PyutClass(name=classElement['name'])

        displayParameters: PyutDisplayParameters = PyutDisplayParameters.toEnum(classElement['displayParameters'])

        showStereotype:    bool = bool(classElement['showStereotype'])
        showFields:        bool = bool(classElement['showFields'])
        showMethods:       bool = bool(classElement['showMethods'])
        pyutClass.displayParameters = displayParameters

        pyutClass.setStereotype(showStereotype)     # This is bogus;  How did I forget this
        pyutClass.showFields     = showFields
        pyutClass.showMethods    = showMethods

        pyutClass.description = classElement['description']
        pyutClass.fileName    = classElement['fileName']
        pyutClass.id          = int(classElement['id'])      # TODO revisit this when we start using UUIDs

        pyutClass.methods = self._methodToPyutMethods(classElement=classElement)
        return pyutClass

    def _methodToPyutMethods(self, classElement: Element) -> UntangledPyutMethods:
        """
        The pyutClass may not have methods;
        Args:
            classElement:  The pyutClassElement

        Returns:  May return an empty list
        """

        untangledPyutMethods: UntangledPyutMethods = UntangledPyutMethods([])

        methodElements = classElement.get_elements('Method')
        for methodElement in methodElements:
            methodName: str                = methodElement['name']
            visibility: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(methodElement['visibility'])
            self.logger.info(f"{methodName=} - {visibility=}")

            pyutMethod: PyutMethod = PyutMethod(name=methodName, visibility=visibility)

            returnElement = methodElement.get_elements('Return')
            if len(returnElement) > 0:
                pyutType: PyutType = PyutType(value=returnElement[0]['type'])
                pyutMethod.returnType = pyutType

            # <Modifier name="static"/>
            parameters = self._paramToPyutParameters(methodElement)
            pyutMethod.parameters = parameters
            untangledPyutMethods.append(pyutMethod)

        return untangledPyutMethods

    def _paramToPyutParameters(self, methodElement: Element) -> PyutParameters:

        parameterElements = methodElement.get_elements('Param')     # TODO:  https://github.com/hasii2011/PyUt/issues/326
        untangledPyutMethodParameters: PyutParameters = PyutParameters([])
        for parameterElement in parameterElements:
            name:           str = parameterElement['name']
            defaultValue:   str = parameterElement['defaultValue']
            parameterType:  PyutType = PyutType(parameterElement['type'])

            parameter: PyutParameter = PyutParameter(name=name, parameterType=parameterType, defaultValue=defaultValue)
            # <Param name="intParameter" type="int" defaultValue="0"/>
            # <Param name="floatParameter" type="float" defaultValue="0.0"/>
            # <Param name="stringParameter" type="str" defaultValue="''"/>
            untangledPyutMethodParameters.append(parameter)

        return untangledPyutMethodParameters

    def _getRawXml(self) -> str:

        try:
            with open(self._fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e

        return xmlString
