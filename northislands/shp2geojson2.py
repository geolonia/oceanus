"""
Convert ESRI Shapefile to GeoJSON.
"""
import yaml
import fiona
import datetime as dt
from shapely.geometry import shape ,Point ,Polygon
from shapely.ops import polylabel
import json
from GJWriter import GJWriter
import pathlib
import glob

# Open setting file.
with open('./shp2geojson2.yaml' ,'r') as yml:
# with open('./shp2geojson.yaml' ,'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)

# Create instance of GJWriter
gjWriter = GJWriter(config['outputfile'])
# Get basic information from yaml
shapedir = config['shapedir']
layers = config['layers']

# Open the niarea shapefile and get a polygon
niarea = fiona.open(config['niarea'])
for element in niarea:
    niareapgn = Polygon(element['geometry']['coordinates'][0])
niarea.close()

# Get layer information
for layer in layers:
    # Get file information
    for filename in layer['file']:
        # Print start message
        print('Start:['+str(dt.datetime.now())+']'+filename['pofname'])

        # Get Shapefiles(specify part of file name)
        shapefiles = glob.glob(shapedir + "/*/*/*" + filename['pofname'] +"*.shp")
        # Get elements
        for shapefile in shapefiles:
            # Open the shapefile
            elements = fiona.open(shapefile)
            # Get elements
            for element in elements:
                # Ignore Null Shapes
                if element['geometry']==None:
                    continue
                # 
                if not niareapgn.contains(Point(element['geometry']['coordinates'])):
                    continue
                # Ignore Ocean(ftCode=5100)
                if filename['pofname']=="WA":
                    if element['properties']['ftCode']=="5100":
                        continue
                # Ignore YOMIGANA(Fixed #54)
                if element['properties']['annoCtg'].startswith("その他"):
                    continue

                # print( element['properties']['ftCode'] + "," + element['properties']['annoCtg'])

                # Set "Property" member
                if element['properties']['annoCtg'].startswith("海域"):
                    # Set "Property" member
                    gjWriter.setProperty('class' ,'ocean')
                    # Set "Tippecanoe" member
                    gjWriter.setTippecanoe('layer' ,'water_name')
                    gjWriter.setTippecanoe('minzoom' ,0)
                    gjWriter.setTippecanoe('maxzoom' ,9)
                elif element['properties']['annoCtg'].startswith("山地") or element['properties']['annoCtg'].startswith("行政") or element['properties']['annoCtg'].startswith("土地"):
                    # Set "Property" member
                    gjWriter.setProperty('class' ,'town')
                    # Set "Tippecanoe" member
                    gjWriter.setTippecanoe('layer' ,'place')
                    gjWriter.setTippecanoe('minzoom' ,3)
                    gjWriter.setTippecanoe('maxzoom' ,9)
                elif element['properties']['annoCtg'].startswith("居住") or element['properties']['annoCtg'].startswith("建物"):
                    # Set "Property" member
                    gjWriter.setProperty('class' ,'city')
                    # Set "Tippecanoe" member
                    gjWriter.setTippecanoe('layer' ,'place')
                    gjWriter.setTippecanoe('minzoom' ,7)
                    gjWriter.setTippecanoe('maxzoom' ,9)
                elif element['properties']['annoCtg'].startswith("河川"):
                    # Set "Property" member
                    gjWriter.setTippecanoe('layer' ,'water_name')
                    # Set "Tippecanoe" member
                    gjWriter.setProperty('class' ,'other')
                    gjWriter.setTippecanoe('minzoom' ,2)
                    gjWriter.setTippecanoe('maxzoom' ,9)
                else:
                    # Set "Property" member(Fixed #55)
                    gjWriter.setTippecanoe('layer' ,'place')
                    # Set "Tippecanoe" member
                    gjWriter.setProperty('class' ,'village')
                    gjWriter.setTippecanoe('minzoom' ,3)
                    gjWriter.setTippecanoe('maxzoom' ,9)
                # Set "Geometry" member
                if 'attr' in filename:
                    # Attribute 
                    if element['geometry']['type']=='Point':
                        # Get attribute name and set "Property" member
                        gjWriter.setProperty('name' ,element['properties'][filename['attr']])
                # Write "Geometry" member(Other than attribute label)
                gjWriter.setGeometry(element['geometry'])
                # Write "Geometry" member
                gjWriter.Write()            
            # Close Shapefile
            elements.close()
        # Print end message
        print('End  :['+str(dt.datetime.now())+']'+filename['pofname'])

# Dispose GJWriter instance
del gjWriter
