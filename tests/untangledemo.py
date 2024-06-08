
from pkg_resources import resource_filename

import untangle

from tests.ProjectTestBase import ProjectTestBase

fqFileName = resource_filename(ProjectTestBase.RESOURCES_PACKAGE_NAME, 'MultiDocumentProject.xml')

with open(fqFileName, "r") as xmlFile:
    xmlString: str = xmlFile.read()

root = untangle.parse(xmlString)
pyutProject = root.PyutProject

for pyutDocument in pyutProject.PyutDocument:
    print(f"{pyutDocument['type']=} {pyutDocument['title']=} {pyutDocument['scrollPositionX']=} {pyutDocument['scrollPositionY']=} {pyutDocument['pixelsPerUnitX']=} {pyutDocument['pixelsPerUnitY']=}")

    for graphicClass in pyutDocument.GraphicClass:
        print(f"{graphicClass['x']=} {graphicClass['y']=} {graphicClass['width']=} {graphicClass['height']=}")
