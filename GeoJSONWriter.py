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
            if len(inParts)==1:
                # 単一ライン（Lines4tring）
                self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "LineString" + "\"" + ","
                self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"["
                # 座標文字列化
                for Xy in inXyList:
                    self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
                # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
                self.Geometry = self.Geometry[:-1]
                self.Geometry+="]"
            else:
                # 複数ライン（MultiLineString）
                self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "MultiLineString" + "\"" + ","
                self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"[["
                # 座標文字列化
                XyLists = []
                startPoint = inParts
                endPoint = inParts[1:]
                endPoint.append(len(inXyList))
                for start ,end in zip(startPoint ,endPoint):
                    XyLists.append(inXyList[start:end])
                for XyList in XyLists:
                    for Xy in XyList:
                        self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
                    self.Geometry = self.Geometry[:-1]
                    self.Geometry+= "],["
                # 最後の1文字をカンマから]に置き換え（イテレータのhasNextがないため）
                self.Geometry = self.Geometry[:-3]
                self.Geometry+="]]"
        elif inFigtype==5:
            # FIGTYPE=5 : POLYGON、MULTIPOLYGON
            self.Geometry = "\t" + "{" + "\"" + "type"+ "\"" + ":" +"\"" + "Feature" +"\"" + "," + "\n"
            self.Geometry+= "\t" + "\"" + "geometry"+ "\"" + ":{"

            # 座標を逆転して積み込み
            XyLists = []
            uclockwise=[]
            if len(inParts)==1:
                XyLists.append(np.flipud(inXyList))
                uclockwise.append(True)
            else:
                startPoint = inParts
                endPoint = inParts[1:]
                endPoint.append(len(inXyList))
                for start ,end in zip(startPoint ,endPoint):
                    Xy = np.flipud(inXyList[start:end])
                    XyLists.append(Xy)
                    # 時計回り判定
                    if self.isClockwise(Xy):
                        uclockwise.append(False)
                    else:
                        uclockwise.append(True)

            if uclockwise.count(True) > 1:
                # マルチポリゴン（外周（反時計回り）が2つ以上）
                self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "MultiPolygon" + "\"" + ","
                self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"[[["
            else:
                # 単一ポリゴン
                self.Geometry+= "\"" + "type"+ "\"" + ":" + "\"" + "Polygon" + "\"" + ","
                self.Geometry+= "\"" + "coordinates"+ "\"" + ":" +"[["

            # 座標文字列化
            for XyList ,uclockw in zip(XyLists ,uclockwise):
                if uclockw==False:
                    # 穴あき部分の処理
                    if uclockwise.count(True) > 1:
                        # マルチポリゴン
                        self.Geometry = self.Geometry[:-5]
                        self.Geometry+="],["
                    else:
                        # 単一ポリゴン
                        self.Geometry = self.Geometry[:-2]
                        self.Geometry+="],["
                # 座標の積み込み
                for Xy in XyList:
                    self.Geometry+= "[" + str(str(round(Xy[0],7))+","+str(round(Xy[1],7))) + "],"
                # 構成要素ごとに閉じる
                self.Geometry = self.Geometry[:-1]
                if uclockwise.count(True) > 1:
                    # マルチポリゴン
                    self.Geometry+= "]],[["

                else:
                    # 単一ポリゴン
                    self.Geometry+= "],"
            
            # 図形要素として閉じる
            self.Geometry = self.Geometry[:-1]
            if uclockwise.count(True) > 1:
                # マルチポリゴン
                self.Geometry+= "]]"
            else:
                # 単一ポリゴン
                self.Geometry+= "]"

    # プロパティの設定
    def setProperty(self ,inName ,inValue):
        # 2つ目以降か？
        if self.Properties==None:
            # 1つ目
            self.Properties = "\t" + "\"" + "properties"+ "\"" + ":{"
        else:
            # 2つ目以降
            self.Properties+= ","
        if type(inValue) is int:
            # 数値項目
            self.Properties+= "\"" + inName + "\"" + ":" + str(inValue)
        else:
            # 文字列項目
            self.Properties+= "\"" + inName + "\"" + ":" + "\"" +  str(inValue) + "\""

    # tippecanoeプロパティの設定
    def setTippecanoe(self ,inTag ,inValue):
        # とりあえずlayerのみ
        if self.Tippecanoe==None:
            self.Tippecanoe = "\t" + "\"" + "tippecanoe" + "\"" + ":{"
        else:
            self.Tippecanoe += ","
        
        if type(inValue) is int:
            # 数値項目
            self.Tippecanoe += "\"" + inTag + "\"" + ":" + str(inValue)
        else:
            # 文字列項目
            self.Tippecanoe += "\"" + inTag + "\"" + ":" + "\"" + str(inValue) + "\""

    # ファイルの書き込み
    def Write(self):
        # ヘッダー・行終端の書き込み
        if self._jsonfd.tell()==0 :
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            self._jsonfd.write(",\n")
        # 要素情報の書き込み
        self._jsonfd.write(self.Geometry + "}," + "\n")
        self._jsonfd.write(self.Tippecanoe + "}")
        if self.Properties != None:
            self._jsonfd.write(",\n" + self.Properties + "}")
        # 最後の終端
        self._jsonfd.write("}")
        # ジオメトリとプロパティをクリア
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

    # 座標点列の時計回り判定
    # https://gis.stackexchange.com/questions/298290/checking-if-vertices-of-polygon-are-in-clockwise-or-anti-clockwise-direction-in
    # 
    def isClockwise(self ,pr2):
        xs, ys = map(list, zip(*pr2))
        xs.append(xs[1])
        ys.append(ys[1])
        if (sum(xs[i]*(ys[i+1]-ys[i-1]) for i in range(1, len(pr2)))/2.0) < 0:
            # 時計回り
            return True
        else:
            # 反時計回り
            return False

if __name__ == '__main__':

    # from GeoJSONWriter import GeoJSONWriter
    import yaml
    import shapefile
    import datetime as dt

    # GeoJSONWriterインスタンスの生成
    gjWriter = GeoJSONWriter("./z7.json")

    # yamlファイルのオープン
    with open('./tile-builder.yaml' ,'r') as yml:
        config = yaml.load(yml)
    # 基本情報の取得
    basedir = config['basedir']
    layers = config['layers']

    # z0(Zoomlevel=0)のレイヤ取得
    for layer in layers:
        for filename in layer['file']:
            print('Start:['+str(dt.datetime.now())+']'+filename['name'])
            shapes = shapefile.Reader(basedir+filename['name'])
            for shp in shapes:
                if shp.shape.shapeType!=0:
                    # Null Shape以外ならGeoJSON化
                    gjWriter.setGeometry(shp.shape.shapeType ,shp.shape.points ,shp.shape.parts)
                    if 'class' in filename:
                        gjWriter.setProperty('class' ,filename['class'])
                    if 'subclass' in filename:
                        gjWriter.setProperty('subclass' ,filename['subclass'])
                    if 'admin_level' in filename:
                        gjWriter.setProperty('admin_level' ,filename['admin_level'])
                    gjWriter.setTippecanoe('layer' ,layer['layer'])
                    if 'minzoom' in filename:
                        gjWriter.setTippecanoe('minzoom' ,filename['minzoom'])
                    if 'maxzoom' in filename:
                        gjWriter.setTippecanoe('maxzoom' ,filename['maxzoom'])
                    # GeoJSONファイルへの書き込み
                    gjWriter.Write()
            shapes.close()
            print('End  :['+str(dt.datetime.now())+']'+filename['name'])

    # GeoJSONWriterを破棄
    del gjWriter
