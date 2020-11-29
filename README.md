# tile-builder
## ズームレベル
 ズームレベル7まで対応しています。
## 現状のレイヤ名と元データ
- layer: landuse
    - name: 50m_cultural/ne_50m_urban_areas.shp
    - name: 50m_cultural/ne_50m_urban_areas.shp
- layer: landcover
    - name: 110m_physical/ne_110m_glaciated_areas.shp
    - name: 50m_physical/ne_50m_glaciated_areas.shp
    - name: 50m_physical/ne_50m_antarctic_ice_shelves_polys.shp
    - name: 10m_physical/ne_10m_glaciated_areas.shp
    - name: 10m_physical/ne_10m_antarctic_ice_shelves_polys.shp
- layer: water
    - name: 110m_physical/ne_110m_ocean.shp
    - name: 110m_physical/ne_110m_lakes.shp
    - name: 50m_physical/ne_50m_ocean.shp
    - name: 50m_physical/ne_50m_lakes.shp
    - name: 10m_physical/ne_10m_lakes.shp
- layer: water_way
    - name: 110m_physical/ne_110m_rivers_lake_centerlines.shp
    - name: 50m_physical/ne_50m_rivers_lake_centerlines.shp
    - name: 10m_physical/ne_10m_rivers_lake_centerlines.shp
- layer: boundary
    - name: 110m_cultural/ne_110m_admin_0_boundary_lines_land.shp
    - name: 50m_cultural/ne_50m_admin_0_boundary_lines_land.shp
    - name: 10m_cultural/ne_10m_admin_0_boundary_lines_land.shp
    - name: 10m_cultural/ne_10m_admin_1_states_provinces_lines.shp
- layer: place
    - name: 10m_cultural/ne_10m_admin_1_states_provinces.shp
    - name: 10m_cultural/ne_10m_admin_0_countries.shp
## Pythonのバージョンと追加モジュール
* バージョン:3.9.0
* 追加モジュール
  * pyyaml
  * pyshp
  * numpy
## GeoJSONファイルのmbtiles変換
tippecanoe -o z7.mbtiles -z7 z7.json
## 表示URL
https://labo.takamoto.biz/z7
