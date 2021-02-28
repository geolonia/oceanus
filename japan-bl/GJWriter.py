"""
Writing a GeoJSON File.
Note : Depended Fiona(Python Extend Module) data model.
"""
class GJWriter:
    """
    A class for writing GeoJSON file. 
    """
    def __init__( self ,inOutFile ):
        """
        Constructor method.
        :param inOutFile: Name of the file to output
        :type inOutFile: String
        """
        self._jsonfd = open(inOutFile ,'w' ,encoding='utf-8')
        # Clear properties.
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

    def __del__(self):
        """
        Destructor method.
        """
        # Output Footer and close file.
        self._jsonfd.write( "\n" + "]}")
        self._jsonfd.close()

    def setGeometry(self ,inGeom):
        """
        Set "Geometry" member.
        :param inGeom: Geometry data to output
        :type inGeom: Objects in Fiona Geometry
        """
        self.Geometry = str(inGeom).replace("(","[").replace(")","]").replace("\'","\"")

    def setProperty(self ,inName ,inValue):
        """
        Set "Property" member.
        "Tippecanoe" is special member for the tippecanoe utility.
        :param inName: Name of the property
        :type inName: String
        :param inValue: Value of the property
        :type inValue: String or Integer
        """
        # Tabs for the first item, commas for the second and subsequent items
        if self.Properties==None:
            self.Properties= ""
        else:
            self.Properties+= ","
        # Set value
        if type(inValue) is int:
            self.Properties+= "\"" + inName + "\"" + ":" + str(inValue)
        else:
            self.Properties+= "\"" + inName + "\"" + ":" + "\"" +  str(inValue) + "\""

    def setTippecanoe(self ,inName ,inValue):
        """
        Set "Tippecanoe" member.
        "Tippecanoe" is an attribute of Feature object.
        :param inName: Name of the tippecanoe
        :type inName: String
        :param inValue: Value of the tippecanoe
        :type inValue: String or Integer
        """
        # Tabs for the first item, commas for the second and subsequent items
        if self.Tippecanoe==None:
            self.Tippecanoe= ""
        else:
            self.Tippecanoe += ","        
        # Set value
        if type(inValue) is int:
            self.Tippecanoe += "\"" + inName + "\"" + ":" + str(inValue)
        else:
            self.Tippecanoe += "\"" + inName + "\"" + ":" + "\"" + str(inValue) + "\""

    def Write(self):
        """
        Writing GeoJSON file.
        """
        # Header for the first Feature, commas and LF for the second and subsequent items
        if self._jsonfd.tell()==0 :
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            self._jsonfd.write(",\n")

        # Set "type" member(Header for the Feature)
        self._jsonfd.write("\t{\"type\":\"Feature\",")
        # Set "Geometry" member
        self._jsonfd.write("\"geometry\":" + self.Geometry + ",")
        # Set "Tippecanoe" member
        if self.Tippecanoe != None:
            self._jsonfd.write("\"tippecanoe\":{" + self.Tippecanoe + "},")
        # Set "Property" member
        if self.Properties != None:
            self._jsonfd.write("\"properties\":{" + self.Properties + "}")
        # End of Feature
        self._jsonfd.write("}")
        # Clear all properties
        self.Clear()

    def Clear(self):
        # Clear all properties
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None
