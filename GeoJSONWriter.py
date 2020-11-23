# -----------------------------------------
# GeoJSON出力用クラス
# 2020.11.22 K.Takamoto(takamoto.biz)
# -----------------------------------------
import numpy as np

class GeoJSONWriter:
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
    def setGeometry(self ,inFigtype ,inXyList ,inParts):
        # 座標の変換
        if inFigtype==1:
            # FIGTYPE=1 : POINT(点)
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "Point" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":"
            # 座標文字列化
            self.Geometry+= "[" + str(str(round(inXyList[0],7))+","+str(round(inXyList[1],7))) + "]"
        elif inFigtype==3:
            # FIGTYPE=3 : POLYLINE(折れ線)
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "LineString" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"["
            # 座標文字列化
            for Xy in inXyList:
                self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
            # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
            self.Geometry = self.Geometry[:-1]
            self.Geometry+="]"
        elif inFigtype==5:
            # FIGTYPE=5 : POLYGON(ポリゴン)
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"
            self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "Polygon" + "\"" + ","
            self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"[["

            # 座標を逆転して積み込み
            XyLists = []
            if len(inParts)==1:
                XyLists.append(np.flipud(inXyList))
            else:
                startPoint = inParts
                endPoint = inParts[1:]
                endPoint.append(len(inXyList))
                for start ,end in zip(startPoint ,endPoint):
                    print("start:"+str(start)+" end:"+str(end))
                    Xy = np.flipud(inXyList[start:end])
                    XyLists.append(Xy)

            # 座標文字列化
            for XyList in XyLists:
                for Xy in XyList:
                    self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
                if len(XyLists) > 1:
                    self.Geometry = self.Geometry[:-1]
                    self.Geometry += "],["        
            if len(XyLists) > 1:
                # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
                self.Geometry = self.Geometry[:-3]
                self.Geometry+="]]"
            else:
                # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
                self.Geometry = self.Geometry[:-1]
                self.Geometry+="]]"

    # プロパティの設定
    def setProperty(self ,inName ,inValue):
        # 2つ目以降か？
        if self.Properties==None:
            # 1つ目
            self.Properties = "\t" + "\"" + "properties"+ "\"" + ":{"
        else:
            # 2つ目以降
            self.Properties+= ","
        if type(inValue) is list:
            # 文字列リスト
            self.Properties+= "\"" + inName + "\""+":" + "\"" + "".join(inValue) + "\""
        else:
            # 文字列項目
            self.Properties+= "\"" + inName + "\""+":" + "\"" + str(inValue) + "\""

    # tippecanoeプロパティの設定
    def setTippecanoe(self ,inValue):
        # とりあえずlayerのみ
        self.Tippecanoe = "\t" + "\"" + "tippecanoe" + "\"" + ":{" + "\"" + "layer" + "\"" + ":" + "\"" + str(inValue) + "\""

    # ファイルの書き込み
    def Write(self):
        # ヘッダー・行終端の書き込み
        if self._jsonfd.tell()==0 :
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            self._jsonfd.write(",\n")
        # 要素情報の書き込み
        self._jsonfd.write(self.Geometry + "}," + "\n")
        self._jsonfd.write(self.Tippecanoe + "}," + "\n")
        self._jsonfd.write(self.Properties + "}"+"}")
        # ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

if __name__ == '__main__':

    # from GeoJSONWriter import GeoJSONWriter
    import yaml
    import shapefile

    # GeoJSONWriterインスタンスの生成
    gjWriter = GeoJSONWriter("./z0.json")

    # yamlファイルのオープン
    with open('./tile-builder.yaml' ,'r') as yml:
        config = yaml.load(yml)
    # 基本情報の取得
    basedir = config['basedir']
    z0layers = config['z0']['layers']

    # z0(Zoomlevel=0)のレイヤ取得
    for layer in z0layers:
        if 'classes' in layer:
            # layer and class
            for clas in layer['classes']:
                shapes = shapefile.Reader(basedir+clas['filename'])
                for shp in shapes:
                    gjWriter.setGeometry(shp.shape.shapeType ,shp.shape.points ,shp.shape.parts)
                    gjWriter.setProperty("class" ,clas['class'])
                    gjWriter.setTippecanoe(clas['class'])
                    # GeoJSONファイルへの書き込み
                    gjWriter.Write()
                    # print(shp.shape.points)
                shapes.close()
        else:
            # layer only
            shapes = shapefile.Reader(basedir+layer['filename'])
            for shp in shapes:
                gjWriter.setGeometry(shp.shape.shapeType ,shp.shape.points ,shp.shape.parts)
                gjWriter.setProperty("class" ,layer['layer'])
                gjWriter.setTippecanoe(layer['layer'])
                # GeoJSONファイルへの書き込み
                gjWriter.Write()
            shapes.close()

    # GeoJSONWriterを破棄
    del gjWriter
