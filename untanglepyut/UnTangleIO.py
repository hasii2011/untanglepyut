
from logging import Logger
from logging import getLogger


class UnTangleIO:
    def __init__(self):
        self.ioLogger: Logger = getLogger(__name__)

    def getRawXml(self, fqFileName: str) -> str:
        """
        method to read a file.  Assumes the file has XML.
        No check is done to verify this
        Args:
            fqFileName: The file to read

        Returns:  The contents of the file
        """
        try:
            with open(fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.ioLogger.error(f'xml open:  {e}')
            raise e

        return xmlString
