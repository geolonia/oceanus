# -----------------------------------------
# GeoJSON出力用クラス　Fiona版
# 2020.12.12 K.Takamoto(takamoto.biz)
# Fionaに依存
# -----------------------------------------

class GJWriter:
    # コンストラクタ
    def __init__( self ,inOutFile ):
        # 出力ファイルのオープン（とりあえず失敗・例外を考慮しない）
        self._jsonfd = open(inOutFile ,'w' ,encoding='utf-8')
        # ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

    # デストラクタ
    def __del__(self):
        # フッターを書き込み
        self._jsonfd.write( "\n" + "]}")
        # ファイルのクローズ
        self._jsonfd.close()

    # ジオメトリの設定
    def setGeometry(self ,inGeom):
        self.Geometry = str(inGeom).replace("(","[").replace(")","]").replace("\'","\"")

    # プロパティの設定
    def setProperty(self ,inName ,inValue):
        # 1.先頭文字（1項目目はタブ、2項目目以降は継続のカンマ）
        if self.Properties==None:
            self.Properties = "\t"
        else:
            self.Properties+= ","
        # 2.値（文字列の場合は”で囲む）
        if type(inValue) is int:
            self.Properties+= "\"" + inName + "\"" + ":" + str(inValue)
        else:
            self.Properties+= "\"" + inName + "\"" + ":" + "\"" +  str(inValue) + "\""

    # tippecanoeプロパティの設定
    def setTippecanoe(self ,inTag ,inValue):
        # 1.先頭文字（1項目目はタブ、2項目目以降は継続のカンマ）
        if self.Tippecanoe==None:
            self.Tippecanoe = "\t"
        else:
            self.Tippecanoe += ","        
        # 2.値（文字列の場合は”で囲む）
        if type(inValue) is int:
            self.Tippecanoe += "\"" + inTag + "\"" + ":" + str(inValue)
        else:
            self.Tippecanoe += "\"" + inTag + "\"" + ":" + "\"" + str(inValue) + "\""

    # ファイルの書き込み
    def Write(self):
        # 0.ヘッダー・行終端（2つ目以降はカンマ＋改行）
        if self._jsonfd.tell()==0 :
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            self._jsonfd.write(",\n")

        # 1.図形要素ヘッダー
        self._jsonfd.write("\t{\"type\":\"Feature\",\n")
        # 2.Geometry
        self._jsonfd.write("\"geometry\":" + self.Geometry + ",\n")
        # 3.Tippecanoe
        self._jsonfd.write("\"tippecanoe\":{" + self.Tippecanoe + "}")
        # 4.Property
        if self.Properties != None:
            # Propertyタグは存在しない場合を想定
            self._jsonfd.write(",\n")
            self._jsonfd.write("\"properties\":{" + self.Properties + "}")

        # 5.要素の終端（ファイルの終端はデストラクタにて書き込み）
        self._jsonfd.write("}")

        # 6.ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

if __name__ == '__main__':

    # from GeoJSONWriter import GeoJSONWriter
    import yaml
    import fiona
    import datetime as dt
    from shapely.geometry import shape,Polygon
    from shapely.ops import polylabel
    import json

    # yamlファイルのオープン
    with open('/app/tile-builder.yaml' ,'r') as yml:
        config = yaml.load(yml)

    # GeoJSONWriterインスタンスの生成
    gjWriter = GJWriter(config['outputfile'])
    # 基本情報の取得
    basedir = config['basedir']
    layers = config['layers']

    # yaml.layerタグを取得
    for layer in layers:
        # yaml.layer.layerタグを取得
        for filename in layer['file']:
            # デバッグ用
            print('Start:['+str(dt.datetime.now())+']'+filename['name'])
            # シェープファイルをオープン
            elements = fiona.open(basedir+filename['name'])
            # 図形要素を順次取得
            for element in elements:
                # Nullシェープは無視
                if element['geometry']==None:
                    continue
                # 1.Property
                if 'class' in filename:
                    gjWriter.setProperty('class' ,filename['class'])
                if 'subclass' in filename:
                    gjWriter.setProperty('subclass' ,filename['subclass'])
                if 'admin_level' in filename:
                    gjWriter.setProperty('admin_level' ,filename['admin_level'])
                # 2.Tippecanoe
                gjWriter.setTippecanoe('layer' ,layer['layer'])
                if 'minzoom' in filename:
                    gjWriter.setTippecanoe('minzoom' ,filename['minzoom'])
                if 'maxzoom' in filename:
                    gjWriter.setTippecanoe('maxzoom' ,filename['maxzoom'])
                # 3.ジオメトリ
                if 'attr' in filename:
                    # 属性ラベル（ポリゴン、マルチポルゴンのみ対応）
                    if element['geometry']['type']=='MultiPolygon' or element['geometry']['type']=='Polygon':
                        # プロパティ（名称）を設定：yamlにて項目名を設定できる方がよさそう
                        gjWriter.setProperty('name:en' ,element['properties'][filename['attr']])
                        area=0.0
                        # ポリゴン取得Loop
                        for parts in element['geometry']['coordinates']:
                            if element['geometry']['type']=='MultiPolygon':
                                pgn = Polygon(parts[0])
                            else:
                                pgn = Polygon(parts)
                            if area < pgn.area:
                                # 最大面積のポリゴンを記録
                                area = pgn.area
                                maxpgn=pgn
                        try:
                            # ラベル表示位置を最大ポリゴンのpolylabelにて決定
                            geometry = "{\"type\":\"Point\",\"coordinates\":"
                            geometry += str(polylabel(maxpgn ,tolerance=10)).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                            geometry += "}"
                        except:
                            # InvalidPolygonとなる場合は矩形中心とする
                            geometry = "{\"type\":\"Point\",\"coordinates\":"
                            geometry += str(maxpgn.centroid).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                            geometry += "}"
                        # ジオメトリの設定
                        gjWriter.setGeometry(geometry)
                else:
                    # 属性ラベル以外
                    gjWriter.setGeometry(element['geometry'])
                # 4.GeoJSONファイルへの書き込み
                gjWriter.Write()
                
            # シェープファイルをクローズ
            elements.close()
            # デバッグ用
            print('End  :['+str(dt.datetime.now())+']'+filename['name'])

    # GeoJSONWriterを破棄
    del gjWriter
