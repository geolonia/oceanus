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
                # Ignore Null Shapes
                if filename['pofname']=="WA":
                    if element['properties']['ftCode']=="5100":
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
