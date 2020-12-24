# tile-builder
## 概要

[NaturalEarth](https://www.naturalearthdata.com)からダウンロードしたシェープファイルをmbtilesに変換します。
具体的には、設定ファイル（tile-builder.yaml）で指定したシェープファイルをGeoJSON形式に変換し、tippecanoeを使ってmbtilesに変換します。  
変換したmbtilesを使ってlocalhost内でタイル配信できるスクリプト（runtilesv.sh）も提供します。

## 利用方法

mbtilesへの変換は以下のように行います。
```
$ git clone https://github.com/geolonia/tile-builder  
$ cd tile-builder  
$ docker build -t geolonia/tile-builder .  
$ ./tile-builder.sh "データ保存用ディレクトリ（フルパス）"  
```

変換したデータをの配信は以下のように行います。
```
$ ./runtilesv.sh "データ保存用ディレクトリ（フルパス）" "tileserver-glのポート番号"  
```
配信はlocalhostでのみ可能としています。独自のRLを指定する場合はスクリプトの修正（tileserver-glの起動引数に -u を追加）が必要です。

## 参考

## 使用する外部プロダクト

* [tippecanoe](https://github.com/mapbox/tippecanotileservewr-gl)
* [tileserver-gl](https://github.com/maptiler/tileserver-gl)

## 導入されるPythonのバージョンと拡張モジュール

* Pythonのバージョン:3.6.9
* 拡張モジュール
  * PyYAML 5.3.1
  * fiona 1.8.18
  * Shaply 1.7.1

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

## 変換結果表示URL

[https://labo.takamoto.biz/z7](https://labo.takamoto.biz/z7)
