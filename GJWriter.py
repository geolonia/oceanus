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
    from shapely.geometry import shape

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
                # Nullシェープは無視する
                if element['geometry']==None:
                    continue
                # 2.Property
                if 'class' in filename:
                    gjWriter.setProperty('class' ,filename['class'])
                if 'subclass' in filename:
                    gjWriter.setProperty('subclass' ,filename['subclass'])
                if 'admin_level' in filename:
                    gjWriter.setProperty('admin_level' ,filename['admin_level'])
                # 3.Tippecanoe
                gjWriter.setTippecanoe('layer' ,layer['layer'])
                if 'minzoom' in filename:
                    gjWriter.setTippecanoe('minzoom' ,filename['minzoom'])
                if 'maxzoom' in filename:
                    gjWriter.setTippecanoe('maxzoom' ,filename['maxzoom'])
                # .dbfの属性値
                if 'attr' in filename:
                    bbox = shape(element['geometry']).bounds
                    gjWriter.setProperty('name:en' ,element['properties'][filename['attr']])
                    geometry = "{\"type\":\"Point\",\"coordinates\":["
                    geometry += str(bbox[0]+(bbox[2]-bbox[0])/2) +"," + str(bbox[1]+(bbox[3]-bbox[1])/2)
                    geometry += "]}"
                    gjWriter.setGeometry(geometry)
                else:
                    # 1.Geometry
                    gjWriter.setGeometry(element['geometry'])
                # 4.GeoJSONファイルへの書き込み
                gjWriter.Write()
                
            # シェープファイルをクローズ
            elements.close()
            # デバッグ用
            print('End  :['+str(dt.datetime.now())+']'+filename['name'])

    # GeoJSONWriterを破棄
    del gjWriter
