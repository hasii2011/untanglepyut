
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutParameter import PyutParameter
from untangle import Element

from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutModifiers
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutStereotype import PyutStereotype

UntangledPyutMethods   = NewType('UntangledPyutMethods',   List[PyutMethod])


class UnTanglePyut:
    """
    Converts PyutModel XML to Pyut Objects
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def classToPyutClass(self, graphicClass: Element) -> PyutClass:
        classElement: Element = graphicClass.Class

        pyutClass: PyutClass = PyutClass(name=classElement['name'])

        displayParameters: PyutDisplayParameters = PyutDisplayParameters.toEnum(classElement['displayParameters'])

        showStereotype:    bool = bool(classElement['showStereotype'])
        showFields:        bool = bool(classElement['showFields'])
        showMethods:       bool = bool(classElement['showMethods'])
        stereotypeStr:     str  = classElement['stereotype']

        pyutClass.displayParameters = displayParameters

        pyutClass.displayStereoType = showStereotype
        pyutClass.showFields     = showFields
        pyutClass.showMethods    = showMethods

        pyutClass.description = classElement['description']
        pyutClass.fileName    = classElement['fileName']
        pyutClass.id          = int(classElement['id'])      # TODO revisit this when we start using UUIDs
        pyutClass.stereotype = PyutStereotype(name=stereotypeStr)

        pyutClass.methods = self._methodToPyutMethods(classElement=classElement)
        return pyutClass

    def textToPyutText(self, graphicText: Element) -> PyutText:
        """
        Parses Text elements
        Args:
            graphicText:   Of the form:   <Text id="3" content="I am stand alone text"/>

        Returns: A PyutText Object
        """
        textElement: Element  = graphicText.Text
        pyutText:    PyutText = PyutText()

        pyutText.id = textElement['id']
        pyutText.content = textElement['content']

        return pyutText

    def noteToPyutNote(self, graphicNote: Element) -> PyutNote:
        """
        Parse Note elements
        Args:
            graphicNote: of the form:  <Note id="2" content="I am a UML Note" filename=""/>

        Returns: A PyutNote Object
        """
        noteElement: Element = graphicNote.Note
        pyutNote: PyutNote = PyutNote()

        pyutNote.id       = int(noteElement['id'])
        pyutNote.content  = noteElement['content']
        pyutNote.fileName = noteElement['filename']

        return pyutNote

    def interfaceToPyutInterface(self, interface: Element) -> PyutInterface:

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

    def linkToPyutLink(self, singleLink: Element, source: PyutClass, destination: PyutClass) -> PyutLink:
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

    def _modifierToPyutMethodModifiers(self, methodElement: Element) -> PyutModifiers:
        """
        Should be in this form:

        <Modifier name="modifier1,modifier2,modifier3"/>

        Args:
            methodElement:

        Returns:  PyutModifiers if not exist returns an empty
        """

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

    def _interfaceMethodsToPyutMethods(self, interface: Element) -> List[PyutMethod]:

        pyutMethods: List[PyutMethod] = self._methodToPyutMethods(interface)

        return pyutMethods

    def _str2bool(self, strValue: str) -> bool:
        """
        Converts a know set of strings to a boolean value

        TODO: Put in common place;  Also, in UnTangler

        Args:
            strValue:

        Returns:  the boolean value
        """
        return strValue.lower() in ("yes", "true", "t", "1", 'True')
