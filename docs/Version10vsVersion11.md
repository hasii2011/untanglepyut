Pyut Xml Version 10 vs. Version 11
===================

PyutProject version="11"

# Class Diagrams

## GraphicClass → OglClass

 ```xml
 <GraphicClass width="429" height="145" x="300" y="175">
 ```
is now
```xml
<OglClass width="429" height="145" x="300" y="175">
```



## Class → PyutClass

```xml
<Class id="1" name="SingleClass" stereotype="noStereotype" filename="" description="I am a single class" showMethods="True" showFields="True" showStereotype="True" displayParameters="Display">
```

is now

```xml
<PyutClass id="1" name="SingleClass" stereotype="noStereotype" displayMethods="True" displayParameters="Display" displayFields="True" displayStereotype="True" description="I am a single class">
```

## GraphicLink → OglLink

```xml
<GraphicLink srcX="125" srcY="146" dstX="553" dstY="147" spline="False">
```
is now
```xml
<OglLink sourceAnchorX="125" sourceAnchorY="146" destinationAnchorX="553" destinationAnchorY="147" spline="False">
```



```xml
<Class id="3" name="Car" stereotype="noStereotype" filename="" description="" showMethods="True" showFields="True"    showStereotype="True" displayParameters="Unspecified">
```

is now

```xml
<PyutClass id="3" name="Car" stereotype="noStereotype"  description="" displayMethods="True" displayFields="True" displayStereotype="True" displayParameters="Unspecified" >
```


## Method → PyutMethod

```xml
<Method name="protectedMethod" visibility="PROTECTED">
    <Return type="float"/>
</Method>
```

is renamed and has a new attribute

```xml
<PyutMethod name="protectedMethod" visibility="PROTECTED" returnType="float">
```

## Param → PyutParameter

```xml
<Param name="intParam" type="int" defaultValue="42"/>
```

is now

```xml
<PyutParameter name="intParam" type="int" defaultValue="42" />
```

## Field → PyutField

```xml
<Field visibility="PRIVATE">
 <Param name="privateField" type="float" defaultValue="42.0"/>
</Field>
```

is now

```xml
<PyutField name="privateField" visibility="PRIVATE" type="float" defaultValue="42.0" />
```

## Link → PyutLink

```xml
<Link name="" type="INTERFACE" cardSrc="" cardDestination="" bidir="False" sourceId="6" destId="5"/>
```

is now

```xml
<PyutLink name="organizes" type="COMPOSITION" cardinalitySource="1" cardinalityDestination="*" bidirectional="False" sourceId="1" destinationId="2" />
```



## GraphicLollipop → OglInterface2

```xml
<GraphicLollipop attachmentPoint="EAST" x="465" y="649"/>
```

is now

```xml
<OglInterface2 attachmentPoint="EAST" x="465" y="649"/>
```
## Interface → PyutInterface

```xml
<Interface id="10" name="IClassInterface" description="">
```

is now

```xml
<PyutInterface id="10" name="IClassInterface" description="">
```


# Sequence Diagrams

## GraphicSDInstance → OglSDInstance
```xml
<GraphicSDInstance width="100" height="400" x="129" y="50">
```

is now

```xml
<OglSDInstance width="100" height="400" x="129" y="50">
```

## SDInstance → PyutSDInstance
```xml
<SDInstance id="1" instanceName="hasiiInstance" lifeLineLength="200"/>
```

is now

```xml
PyutSDInstance id="1" instanceName="hasiiInstance" lifeLineLength="200" />
```

## GraphicSDMessage  → OglSDMessage

## SDMessage → PyutSDMessage

```xml
<SDMessage id="6" message="bites()" srcTime="328" dstTime="338" srcID="3" dstID="2"/>
```

is now 

```xml
<PyutSDMessage id="6" message="bites()" sourceX="328" destinationY="338" sourceID="3" destinationID="2" />
```

Attribute renames

srcTime → sourceX
dstTime → destinationY
srcID → sourceID
dstId → destinationID`

# Notes and Text
## GraphicNote  →  OglNote

```xml
GraphicNote width="128" height="49" x="175" y="300">
```

is now

```xml
<OglNote width="128" height="49" x="175" y="300">
```

## Text  → PyutText

```xml
<Text id="1" content="Donec eleifend luctus enim vel mollis"/>
```

is now

```xml
<PyutText id="1" content="Donec eleifend luctus enim vel mollis"/>
```

## GraphicText → OglText

```xml
GraphicText width="138" height="88" x="100" y="325" textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">
```

is now

```xml
<OglText width="138" height="88" x="100" y="325"  textSize="14" isBold="False" isItalicized="False" fontFamily="Swiss">
```

## Text → PyutText
```xml
<Text id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few"/>
```

is now

```xml
<PyutText id="4" content="This plain text&amp;#xA;With line breaks&amp;#xA;At least a few"/>
```

# Use Case Diagrams

## GraphicUseCase → OglUseCase

```xml
<GraphicUseCase width="100" height="60" x="475" y="275"/>
```

is now

```xml
<OglUseCase width="100" height="60" x="475" y="275"/>
```

## GraphicActor → OglActor

```xml
<GraphicActor width="87" height="114" x="293" y="236"/>
```
is now
```xml
<OglActor width="87" height="114" x="293" y="236"/>
```

## Actor → PyutActor

```xml
<Actor id="1" name="BasicActor" filename=""/>
```

is now

```xml
<PyutActor id="1" name="BasicActor" filename="" />
```

## UseCase → PyutUseCase
```xml
<UseCase id="3" name="Basic Use Case" filename=""/>
```

is now

```xml
<PyutUseCase id="3 " name="Basic Use Case" filename="" />
```