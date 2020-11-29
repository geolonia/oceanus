# tile-builder
## ズームレベル
 ズームレベル7まで対応しています。
## 現状のレイヤ名と元データ
* water:ne_110m_ocean.shp
* ocan:ne_110m_lakes.shp
* landcover:ne_110m_glaciated_areas.shp
* boundary:ne_110m_admin_0_boundary_lines_land.shp
## Pythonのバージョンと追加モジュール
* バージョン:3.9.0
* 追加モジュール
  * pyyaml
  * pyshp
  * numpy
## GeoJSONファイルのmbtiles変換
tippecanoe -zg -o z0.mbtiles --drop-densest-as-needed z0.json
## 表示URL
https://labo.takamoto.biz/z7
