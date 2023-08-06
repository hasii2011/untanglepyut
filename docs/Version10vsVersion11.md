Pyut Xml Version 10 vs. Version 11
===================

PyutProject version="11"

# Class Diagrams

## GraphicClass → OglClass

 `<GraphicClass width="429" height="145" x="300" y="175">`
is now
`<OglClass width="429" height="145" x="300" y="175">`

## GraphicLink → OglLink

`<GraphicLink srcX="125" srcY="146" dstX="553" dstY="147" spline="False">`
is now
`<OglLink sourceAnchorX="125" sourceAnchorY="146" destinationAnchorX="553" destinationAnchorY="147" spline="False">`



`<Class id="3" name="Car" stereotype="noStereotype" filename="" description="" showMethods="True" showFields="True"    showStereotype="True" displayParameters="Unspecified">`

is now

`<PyutClass id="3" name="Car" stereotype="noStereotype"  description="" displayMethods="True" displayFields="True" displayStereotype="True" displayParameters="Unspecified" >`


## Method → PyutMethod

`<Method name="protectedMethod" visibility="PROTECTED">
    <Return type="float"/>
</Method>`

is renamed and has a new attribute

`<PyutMethod name="protectedMethod" visibility="PROTECTED" returnType="float">`

## Param → PyutParameter

`<Param name="intParam" type="int" defaultValue="42"/>`

is now

`<PyutParameter name="intParam" type="int" defaultValue="42" />`

## Field → PyutField

`<Field visibility="PRIVATE">
 <Param name="privateField" type="float" defaultValue="42.0"/>
</Field>`

is now

`<PyutField name="privateField" visibility="PRIVATE" type="float" defaultValue="42.0" />`

# Sequence Diagrams
## GraphicSDInstance → OglSDInstance
`<GraphicSDInstance width="100" height="400" x="129" y="50">`

is now

`<OglSDInstance width="100" height="400" x="129" y="50">`

## SDInstance → PyutSDInstance
`<SDInstance id="1" instanceName="hasiiInstance" lifeLineLength="200"/>`

is now

`PyutSDInstance id="1" instanceName="hasiiInstance" lifeLineLength="200" />`

## GraphicSDMessage  → OglSDMessage

## SDMessage → PyutSDMessage

`<SDMessage id="6" message="bites()" srcTime="328" dstTime="338" srcID="3" dstID="2"/>`

is now 

`<PyutSDMessage id="6" message="bites()" sourceX="328" destinationY="338" sourceID="3" destinationID="2" />`

Attribute renames

srcTime → sourceX
dstTime → destinationY
srcID → sourceID
dstId → destinationID`

# Notes and Text
## GraphicNote  →  OglNote

`GraphicNote width="128" height="49" x="175" y="300">`

is now

`<OglNote width="128" height="49" x="175" y="300">`

## Note  → PyutNote

`<Note id="4" content="I am a note linked to&amp;#xA;the LinkedToClass" filename=""/>`

is now

`<PyutNote id="1" content="I am a note linked to&amp;#xA;the LinkedToClass" filename="" />`

## GraphicText → OglText

`GraphicText width="138" height="88" x="100" y="325" textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">`

is now

`<OglText width="138" height="88" x="100" y="325">`

## Text → PyutText
`<Text id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few"/>`

is now

`<PyutText id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few"/>`

# Use Case Diagrams

## GraphicUseCase → OglUseCase

`<GraphicUseCase width="100" height="60" x="475" y="275">`

is now

`<OglUseCase width="100" height="60" x="475" y="275">`


## UseCase → PyutUseCase
`<UseCase id="3" name="Basic Use Case" filename=""/>`

is now

`<PyutUseCase id="3 " name="Basic Use Case" filename="" />`