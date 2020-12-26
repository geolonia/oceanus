# tile-builder
## 概要

[NaturalEarth](https://www.naturalearthdata.com)からシェープファイルをダウンロードしmbtilesに変換します。
具体的には、設定ファイル（tile-builder.yaml）で指定したシェープファイルをGeoJSON形式に変換し、tippecanoeを使ってmbtilesに変換します。  
変換したmbtilesは、runtilesv.shスクリプト（tileserver-glのDockerコンテナを作成）を使って配信できます。

## 利用方法

mbtilesへの変換は以下のように行います。
```
$ git clone https://github.com/geolonia/tile-builder  
$ cd tile-builder  
$ docker build -t geolonia/tile-builder .
$ ./tile-builder.sh <データ保存用ディレクトリ（フルパス）>
```

変換したタイルの配信は以下のように行います。
```
$ ./runtilesv.sh <データ保存用ディレクトリ（フルパス）> <配信サーバーのポート番号>  
```

ブラウザから以下のようにURLを指定するとtileserver-glの初期画面が表示されますので、スタイル"basic"を指定することで、地図を表示できます。  
http://localhost:ポート番号

## 参考

## NaturalEarthからダウンロードするデータ

 * 110m_physical(3.4MB)
 * 110m_cultural(1.3MB)
 * 50m_physical(7.1MB)
 * 50m_cultural(7.9MB)
 * 10m_physical(4.7MB)
 * 10m_cultural(206.7MB)

### tile-builder.yamlの設定項目

|項目|設定内容|
|----|----|
|basedir|シェープファイル の存在するディレクトリ|
|outputfile|出力するGeoJSONファイル名|
|layer|レイヤ名|
|file.name|シェープファイル名|
|file.class|style用の属性値|
|file.subclass|style用の属性値|
|file.minzoom|タイルを作成する最小ズーム値|
|file.maxzoom|タイルを作成する最大ズーム値|

## 使用ているプロダクト

* [tippecanoe](https://github.com/mapbox/tippecanotileservewr-gl)
* [tileserver-gl](https://github.com/maptiler/tileserver-gl)
* [Google Font:Noto Sans JP](https://fonts.google.com/specimen/Noto+Sans+JP?subset=japanese)
* Python3.6.9
* Python拡張モジュール
  * PyYAML 5.3.1
  * fiona 1.8.18
  * Shaply 1.7.1

## 変換結果表示URL

[https://labo.takamoto.biz/tile-builder](https://labo.takamoto.biz/tile-builder)
