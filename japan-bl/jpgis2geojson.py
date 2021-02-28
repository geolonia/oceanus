"""
Convert JPGIS2.0 to GeoJSON.
"""
import xml.sax,xml.sax.handler
from GJWriter import GJWriter
import subprocess

class SaxHandler(xml.sax.handler.ContentHandler):
    """
    A class for sax(xml parser) event handler. 
    """
    def __init__( self ):
        """
        Constructor method.
        """
        # Initialize internal status
        self._nb = False
        self._controlPoint = False
        self._coordinate = False
        self._geombuff = None
        # Create GeoJSON
        self._gjWriter = GJWriter('./jpgis2geojson.json')

    def startElement(self ,name ,attrs):
        """
        Start element(xml start tag detection).
        :param name: tag name
        :type name: string
        :param attrs: tag attributes
        :type name: array
        """
        if(name=='controlPoint'):
            self._controlPoint = True
            self._geombuff = None
        if(name=='coordinate'):
            self._coordinate = True

    def endElement(self ,name):
        """
        End element(xml end tag detection).
        :param name: tag name
        :type name: string
        """
        if(self._nb==True and name=='controlPoint'):
            # Generate GeoJSON string
            elembuff = "{\"type\":\"LineString\",\"coordinates\":"
            elembuff += str(self._geombuff).replace('\'','')
            elembuff += "}"
            # Set Geometry
            self._gjWriter.setGeometry(elembuff)
            # Set Property( admin_level=3 ,boundary )
            self._gjWriter.setProperty('admin_level' ,3)
            self._gjWriter.setTippecanoe('layer' ,'boundary')
            # Set zoom level range
            self._gjWriter.setTippecanoe('minzoom' ,0)
            self._gjWriter.setTippecanoe('maxzoom' ,7)

            # Write "Geometry" member and clear buffer
            self._gjWriter.Write()
            self._geombuff = None

        # Set status
        if(name=='controlPoint'):
            self._controlPoint = False
        if(name=='境界'):
            self._nb = False
        if(name=='coordinate'):
            self._coordinate = False

    def characters(self ,content):
        """
        Get element value(xml data detection).
        :param content: set value
        :type content: string
        """
        if(content.startswith('国界(海上)')):
            self._nb = True
        if(self._nb and self._controlPoint and self._coordinate):
            # Set coordinate(BL -> XY)
            buff = content.lstrip(' ').split(' ')
            buff.reverse()
            if(self._geombuff==None):
                self._geombuff = [buff]
            else:
                self._geombuff.append(buff)
            
    def __del__(self):
        # Dispose GJWriter instance
        del self._gjWriter
        # execute tippecanoe
        command = ['tippecanoe' ,'-z7' ,'-f','-o japanborder.mbtiles' ,'jpgis2geojson.json']
        commandstr = ' '.join(command)
        subprocess.check_output(commandstr ,shell=True)

if __name__=='__main__':

    # Create sax parser and regist event handler
    parser = xml.sax.make_parser()
    parser.setContentHandler(SaxHandler())
    # Parse GSI digitalmap 5M(border line layer)
    parser.parse('./5M_BL.xml')
