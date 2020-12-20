# tile-builder
## 概要

[NaturalEarth](https://www.naturalearthdata.com)からダウンロードしたシェープファイルをmbtilesに変換します。

## 起動方法

```
$ git clone https://github.com/geolonia/tile-builder  
$ docker build -t geolonia/tile-builder .  
$ ./quickstart.sh "データ保存用ディレクトリ（フルパス）"  
```
## 現状のレイヤ名と元データ

## Pythonのバージョンと必要モジュール

* Pythonのバージョン:3.6.9
* 必要モジュール
  * PyYAML 5.3.1
  * fiona 1.8.18
  * Shaply 1.7.1

## 参考

### tile-builder.yamlファイルの作成

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

## 表示URL

https://labo.takamoto.biz/z7
