# tile-builder
##Pythonのバージョンと追加モジュール
*バージョン:3.9.0
*追加モジュール
  *pyyaml
  *pyshp
  *numpy
##GeoJSONファイルのmbtiles変換
tippecanoeにて、以下のように実施しました。
tippecanoe -zg -o z0.mbtiles --drop-densest-as-needed z0.json
