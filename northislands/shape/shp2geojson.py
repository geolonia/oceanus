"""
Convert ESRI Shapefile to GeoJSON.
"""
import yaml
import fiona
import datetime as dt
from shapely.geometry import shape,Polygon
from shapely.ops import polylabel
import json
from GJWriter import GJWriter

# Open setting file.
with open('/app/shp2geojson.yaml' ,'r') as yml:
# with open('./shp2geojson.yaml' ,'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)

# Create instance of GJWriter
gjWriter = GJWriter(config['outputfile'])
# Get basic information from yaml
basedir = config['basedir']
layers = config['layers']

# Get layer information
for layer in layers:
    # Get file information
    for filename in layer['file']:
        # Print start message
        print('Start:['+str(dt.datetime.now())+']'+filename['fname'])
        # Open the shapefile
        elements = fiona.open(basedir+filename['fname'])
        # Get elements
        for element in elements:
            # Ignore Null Shapes
            if element['geometry']==None:
                continue
            # Set "Property" member
            if 'class' in filename:
                gjWriter.setProperty('class' ,filename['class'])
            if 'subclass' in filename:
                gjWriter.setProperty('subclass' ,filename['subclass'])
            if 'admin_level' in filename:
                gjWriter.setProperty('admin_level' ,filename['admin_level'])
            if 'name' in filename:
                if element['properties'][filename['name']]!=None:
                    # Set river name to property
                    gjWriter.setProperty('name' ,element['properties'][filename['name']])
            # Set "Tippecanoe" member
            gjWriter.setTippecanoe('layer' ,layer['layer'])
            if 'minzoom' in filename:
                gjWriter.setTippecanoe('minzoom' ,filename['minzoom'])
            if 'maxzoom' in filename:
                gjWriter.setTippecanoe('maxzoom' ,filename['maxzoom'])
            # Issue#47(Disputed border)
            if 'ne_10m_admin_1_states_provinces_lines' in filename['fname']:
                if element['properties']['note']=='Russa_1000':
                    print('Disputed border:[' + element['properties']['note'] + ']')
                    gjWriter.Clear()
                    continue
            # Set "Geometry" member
            if 'attr' in filename:
                # Issue#21(Do not mark "None" on the map)
                if element['properties'][filename['attr']]==None or element['properties'][filename['attr']]=='スコットランド海':
                    gjWriter.Clear()
                    continue
                # Attribute label (only polygon and multipolygon are supported)
                if element['geometry']['type']=='MultiPolygon' or element['geometry']['type']=='Polygon':
                    # Get attribute name and set "Property" member
                    gjWriter.setProperty('name' ,element['properties'][filename['attr']])
                    area=0.0
                    # Get polygon
                    for parts in element['geometry']['coordinates']:
                        if element['geometry']['type']=='MultiPolygon':
                            pgn = Polygon(parts[0])
                        else:
                            pgn = Polygon(parts)
                        if area < pgn.area:
                            # Save the polygon with the largest area
                            area = pgn.area
                            maxpgn=pgn
                    try:
                        # The label position is determined by the polylabel
                        geometry = "{\"type\":\"Point\",\"coordinates\":"
                        geometry += str(polylabel(maxpgn ,tolerance=10)).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                        geometry += "}"
                    except:
                        # In case of InvalidPolygon, use centroid
                        geometry = "{\"type\":\"Point\",\"coordinates\":"
                        geometry += str(maxpgn.centroid).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                        geometry += "}"
                    # Set "Geometry" member
                    gjWriter.setGeometry(geometry)
            else:
                # Write "Geometry" member(Other than attribute label)
                gjWriter.setGeometry(element['geometry'])
            # Write "Geometry" member
            gjWriter.Write()
            
        # Close Shapefile
        elements.close()
        # Print end message
        print('End  :['+str(dt.datetime.now())+']'+filename['fname'])

# Dispose GJWriter instance
del gjWriter
