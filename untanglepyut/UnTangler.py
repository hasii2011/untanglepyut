
from typing import Dict
from typing import List
from typing import NewType

from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from miniogl.AttachmentLocation import AttachmentLocation
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation

from ogl.OglClass import OglClass
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglNoteLink import OglNoteLink

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from untangle import parse
from untangle import Element


@dataclass
class ProjectInformation:
    version:  str = cast(str, None)
    codePath: str = cast(str, None)


UntangledLinks         = Union[OglLink, OglInterface2]
UntangledOglClasses    = NewType('UntangledOglClasses', List[OglClass])
UntangledPyutMethods   = NewType('UntangledPyutMethods', List[PyutMethod])
UntangledOglLinks      = NewType('UntangledOglLinks', List[UntangledLinks])
UntangledControlPoints = NewType('UntangledControlPoints', List[ControlPoint])

OglClassDictionary   = NewType('OglClassDictionary', Dict[int, OglClass])


def createUntangledOglClassesFactory() -> UntangledOglClasses:
    """
    Factory method to create  the UntangledClasses data structure;

    Returns:  A new data structure
    """
    return UntangledOglClasses([])


def createUntangledOglLinksFactory() -> UntangledOglLinks:
    return UntangledOglLinks([])


def createOglClassDictionaryFactory() -> OglClassDictionary:
    return OglClassDictionary({})


@dataclass
class Document:
    documentType:    str = ''
    documentTitle:   str = ''
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:         UntangledOglClasses = field(default_factory=createUntangledOglClassesFactory)
    oglLinks:           UntangledOglLinks   = field(default_factory=createUntangledOglLinksFactory)

    # def __post_init__(self):
    #     self.oglClasses = UntangledOglClasses([])


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
            document.oglLinks = self._graphicLinksToOglLink(pyutDocument, document.oglClasses)

    def _populateProjectInformation(self, pyutProject: Element):
        self._projectInformation.version  = pyutProject['version']
        self._projectInformation.codePath = pyutProject['CodePath']

    def _updateCurrentDocumentInformation(self, pyutDocument: Element) -> Document:

        documentInformation: Document = Document()

        documentTitle: DocumentTitle = DocumentTitle(pyutDocument['title'])

        documentInformation.documentType = pyutDocument['type']
        documentInformation.documentTitle = documentTitle

        documentInformation.scrollPositionX = int(pyutDocument['scrollPositionX'])
        documentInformation.scrollPositionY = int(pyutDocument['scrollPositionY'])
        documentInformation.pixelsPerUnitX  = int(pyutDocument['pixelsPerUnitX'])
        documentInformation.pixelsPerUnitY  = int(pyutDocument['pixelsPerUnitY'])

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

    def _graphicLinksToOglLink(self, pyutDocument: Element, oglClasses: UntangledOglClasses) -> UntangledOglLinks:

        oglClassDictionary: OglClassDictionary = self._buildOglClassDictionary(oglClasses)

        oglLinks: UntangledOglLinks = createUntangledOglLinksFactory()

        graphicLinks: Element = pyutDocument.get_elements('GraphicLink')
        for graphicLink in graphicLinks:
            oglLink: OglLink = self._graphicLinkToOglLink(graphicLink, oglClassDictionary)
            oglLinks.append(oglLink)

        graphicLollipops: Element = pyutDocument.get_elements('GraphicLollipop')
        for graphicLollipop in graphicLollipops:
            oglInterface2: OglInterface2 = self._graphicLollipopToOglInterface(graphicLollipop, oglClassDictionary)
            oglLinks.append(oglInterface2)

        return oglLinks

    def _classToPyutClass(self, graphicClass: Element) -> PyutClass:
        classElement: Element = graphicClass.Class

        pyutClass: PyutClass = PyutClass(name=classElement['name'])

        displayParameters: PyutDisplayParameters = PyutDisplayParameters.toEnum(classElement['displayParameters'])

        showStereotype:    bool = bool(classElement['showStereotype'])
        showFields:        bool = bool(classElement['showFields'])
        showMethods:       bool = bool(classElement['showMethods'])
        stereotypeStr:     str  = classElement['stereotype']

        pyutClass.displayParameters = displayParameters

        pyutClass.setShowStereotype(showStereotype)
        pyutClass.showFields     = showFields
        pyutClass.showMethods    = showMethods

        pyutClass.description = classElement['description']
        pyutClass.fileName    = classElement['fileName']
        pyutClass.id          = int(classElement['id'])      # TODO revisit this when we start using UUIDs
        pyutClass.setStereotype(PyutStereotype(name=stereotypeStr))

        pyutClass.methods = self._methodToPyutMethods(classElement=classElement)
        return pyutClass

    def _modifierToPyutMethodModifiers(self, methodElement: Element) -> PyutModifiers:
        # <Modifier name="modifier1,modifier2,modifier3"/>
        modifierElements = methodElement.get_elements('Modifier')

        pyutModifiers: PyutModifiers = PyutModifiers([])
        if len(modifierElements) > 0:
            modifierElement: Element   = modifierElements[0]
            names:           str       = modifierElement['name']    # comma delimited string
            nameList:        List[str] = names.split(',')
            for modifierName in nameList:
                pyutModifier: PyutModifier = PyutModifier(modifierTypeName=modifierName)
                pyutModifiers.append(pyutModifier)

        return pyutModifiers

    def _paramToPyutParameters(self, methodElement: Element) -> PyutParameters:

        parameterElements = methodElement.get_elements('Param')     # TODO:  https://github.com/hasii2011/PyUt/issues/326
        untangledPyutMethodParameters: PyutParameters = PyutParameters([])
        for parameterElement in parameterElements:
            name:           str = parameterElement['name']
            defaultValue:   str = parameterElement['defaultValue']
            parameterType:  PyutType = PyutType(parameterElement['type'])

            pyutParameter: PyutParameter = PyutParameter(name=name, parameterType=parameterType, defaultValue=defaultValue)
            # <Param name="intParameter" type="int" defaultValue="0"/>
            # <Param name="floatParameter" type="float" defaultValue="0.0"/>
            # <Param name="stringParameter" type="str" defaultValue="''"/>
            untangledPyutMethodParameters.append(pyutParameter)

        return untangledPyutMethodParameters

    def _sourceCodeToPyutSourceCode(self, methodElement: Element) -> SourceCode:
        sourceCodeElements = methodElement.get_elements('SourceCode')
        codeElements = sourceCodeElements[0].get_elements('Code')
        sourceCode: SourceCode = SourceCode([])
        for codeElement in codeElements:
            self.logger.debug(f'{codeElement.cdata=}')
            codeLine: str = codeElement.cdata
            sourceCode.append(codeLine)
        return sourceCode

    def _graphicLinkToOglLink(self, graphicLink: Element, oglClassDictionary: OglClassDictionary) -> OglLink:
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

        spline: bool = self._str2bool(graphicLink['spline'])

        links: Element = graphicLink.get_elements('Link')
        assert len(links) == 1, 'Should only ever one'

        singleLink:  Element = links[0]
        sourceId:    int = int(singleLink['sourceId'])
        dstId:       int = int(singleLink['destId'])
        self.logger.debug(f'graphicLink= {srcX=} {srcY=} {dstX=} {dstY=}')
        try:
            srcShape = oglClassDictionary[sourceId]
            dstShape = oglClassDictionary[dstId]
        except KeyError as ke:
            self.logger.error(f'Developer Error -- srcId: {sourceId} - dstId: {dstId}  error: {ke}')
            return cast(OglLink, None)

        pyutLink: PyutLink = self._linkToPyutLink(singleLink, source=srcShape.pyutObject, destination=dstShape.pyutObject)
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
        pyutInterface:    PyutInterface     = self._interfaceToPyutInterface(interface=interfaceElement)
        oglClass:         OglClass          = self._getOglClassFromName(pyutInterface.implementors[0], oglClassDictionary)
        anchorPoint:      SelectAnchorPoint = SelectAnchorPoint(x=x, y=y, attachmentPoint=attachmentLocation, parent=oglClass)
        oglInterface2:    OglInterface2     = OglInterface2(pyutInterface=pyutInterface, destinationAnchor=anchorPoint)

        return oglInterface2

    def _linkToPyutLink(self, singleLink: Element, source: PyutClass, destination: PyutClass) -> PyutLink:
        linkTypeStr:     str          = singleLink['type']
        linkType:        PyutLinkType = PyutLinkType.toEnum(linkTypeStr)
        cardSrc:         str          = singleLink['cardSrc']
        cardDest:        str          = singleLink['cardDestination']
        bidir:           bool         = self._str2bool(singleLink['bidir'])
        linkDescription: str          = singleLink['name']

        pyutLink: PyutLink = PyutLink(name=linkDescription,
                                      linkType=linkType,
                                      cardSrc=cardSrc, cardDest=cardDest,
                                      bidir=bidir,
                                      source=source,
                                      destination=destination)

        return pyutLink

    def _interfaceToPyutInterface(self, interface: Element) -> PyutInterface:

        interfaceId: int = int(interface['id'])
        name:        str = interface['name']
        description: str = interface['description']

        pyutInterface: PyutInterface = PyutInterface(name=name)
        pyutInterface.id          = interfaceId
        pyutInterface.description = description

        implementors: Element = interface.get_elements('Implementor')
        for implementor in implementors:
            pyutInterface.addImplementor(implementor['implementingClassName'])

        pyutInterface.methods = self._interfaceMethodsToPyutMethods(interface=interface)
        return pyutInterface

    def _interfaceMethodsToPyutMethods(self, interface: Element) -> List[PyutMethod]:

        pyutMethods: List[PyutMethod] = self._methodToPyutMethods(interface)

        return pyutMethods

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
            self.logger.debug(f"{methodName=} - {visibility=}")

            pyutMethod: PyutMethod = PyutMethod(name=methodName, visibility=visibility)

            pyutMethod.modifiers = self._modifierToPyutMethodModifiers(methodElement=methodElement)

            returnElement = methodElement.get_elements('Return')

            if len(returnElement) > 0:
                pyutType: PyutType = PyutType(value=returnElement[0]['type'])
                pyutMethod.returnType = pyutType

            parameters = self._paramToPyutParameters(methodElement)
            pyutMethod.parameters = parameters
            pyutMethod.sourceCode = self._sourceCodeToPyutSourceCode(methodElement=methodElement)

            untangledPyutMethods.append(pyutMethod)

        return untangledPyutMethods

    def _getOglClassFromName(self, className: str, oglClassDictionary: OglClassDictionary) -> OglClass:

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

    def _buildOglClassDictionary(self, oglClasses: UntangledOglClasses):
        """
        """
        oglClassDictionary: OglClassDictionary = createOglClassDictionaryFactory()

        for oglClass in oglClasses:
            classId: int = oglClass.pyutObject.id
            oglClassDictionary[classId] = oglClass

        return oglClassDictionary

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

    def _str2bool(self, strValue: str) -> bool:
        return strValue.lower() in ("yes", "true", "t", "1", 'True')

    def _getRawXml(self) -> str:

        try:
            with open(self._fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e

        return xmlString
