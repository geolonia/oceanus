"""
Convert ESRI Shapefile to GeoJSON.
"""
import yaml
import csv
import fiona
import datetime as dt
from shapely.geometry import shape,Polygon,MultiPolygon
from shapely.ops import polylabel
from GJWriter import GJWriter

# Open setting file.
with open('./shp2geojson.yaml' ,'r') as yml:
    # with open('./shp2geojson.yaml' ,'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)

# Create instance of GJWriter
gjWriter = GJWriter(config['outputfile'])
# Get basic information from yaml
basedir = config['basedir']
layers = config['layers']

# Get Japan area( only 1 polygon )
with fiona.open(basedir+config['japanarea']) as shapes:
    japanarea = shape(next(shapes)['geometry'])

# Get layer information
for layer in layers:
    # Get file information
    for filename in layer['file']:

        # Print start message
        print('Start:['+str(dt.datetime.now())+']'+filename['fname'])

        # Create replace dictionary
        if 'replacecsv' in filename:
            with open(basedir+filename['replacecsv'], encoding='utf-8-sig') as fd:
                dr = csv.reader(fd)
                citydict={}
                for r in dr:
                    citydict.update({r[0]:r[1]})
            replacecsv = True
        else:
            replacecsv = False

        # Open the shapefile
        elements = fiona.open(basedir+filename['fname'])

        # Get property filter condition
        if 'condition' in filename:
            condition = filename['condition'].split('=')
            keylist = condition[1].split('/')
            conddic = {key: '' for key in keylist}

        # Get elements
        for element in elements:
            # Create CSV to Geometry
            if 'filetype' in filename:
                csvelement={"type":"Point"}
                csvelement.update({"coordinates":(float(element['properties']['x']) , float(element['properties']['y']))})
                element['geometry']=csvelement

            # property filter( equal condition only )
            if 'condition' in filename:
                if element['properties'][condition[0]] not in conddic:
                    # Skip output GeoJSON
                    gjWriter.Clear()
                    continue

            # Ignore Null Shapes
            if element['geometry']==None:
                gjWriter.Clear()
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
                    if replacecsv:
                        # Check Japan pref-capital list
                        if element['properties'][filename['name']] in citydict:
                            if citydict[element['properties'][filename['name']]]=='':
                                # Skip output GeoJSON
                                gjWriter.Clear()
                                continue
                            else:
                                # Replace pref-capital name
                                gjWriter.setProperty('name' ,citydict[element['properties'][filename['name']]])
                        else:
                            # Set name to property
                            gjWriter.setProperty('name' ,element['properties'][filename['name']])
                    else:
                        # Set name to property
                        gjWriter.setProperty('name' ,element['properties'][filename['name']])
                else:
                    # Skip output GeoJSON
                    gjWriter.Clear()
                    continue
                    
            # Set Scalerank
            if 'scalerank' in filename:
                if element['properties']['scalerank'] > filename['scalerank']:
                    gjWriter.Clear()
                    continue

            # Set Japan territory
            if 'jflag' in filename:
                if japanarea.intersection(shape(element['geometry'])):
                    gjWriter.setProperty('jflag' ,'japan')
                elif filename['jflag']=='erase':
                    # Issue#17
                    gjWriter.Clear()
                    continue

            # Set pref-capital property
            if 'pref-capital' in filename:
                gjWriter.setProperty('pref-capital' ,'true')

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
                # Simplify Geometry
                if 'simplify' in filename:
                    if element['geometry']['type']=='Polygon':
                        polygon = Polygon(shape(element['geometry']))
                        geometry = "{\"type\":\"Polygon\",\"coordinates\":["
                        geometry += str(polygon.simplify(config['simplifyparam'])).replace("(","[").replace(")","]").replace("\'","\"").replace("POLYGON " ,"").replace(", " ,"],[").replace(" " ,",")
                        geometry += "]}"
                    else:
                        polygon = MultiPolygon(list(shape(element['geometry'])))
                        geometry = "{\"type\":\"MultiPolygon\",\"coordinates\":["
                        geometry += str(polygon.simplify(config['simplifyparam'])).replace("(","[").replace(")","]").replace("\'","\"").replace("MULTIPOLYGON " ,"").replace(", " ,"],[").replace(" " ,",")
                        geometry += "]}"
                    # Set "Geometry" member
                    gjWriter.setGeometry(geometry)
                else:
                    gjWriter.setGeometry(element['geometry'])
            # Write "Geometry" member
            gjWriter.Write()
            
        # Close Shapefile
        elements.close()
        # Print end message
        print('End  :['+str(dt.datetime.now())+']'+filename['fname'])

# Dispose GJWriter instance
del gjWriter
