# tile-builder
## 概要

[NaturalEarth](https://www.naturalearthdata.com)からダウンロードしたシェープファイルをGeoJSON形式に変換します。
変換したGeoJSONを[Tippecanoe](https://github.com/mapbox/tippecanoe)を使ってmbtilesに変換し、ベクトルタイル配信に利用するとこを最終的な目的としています。

## 現状のレイヤ名と元データ

tile-builder.yamlの設定によりGeoJSONのレイヤと対応するシェープファイルや属性値を指定します。
現在の設定を以下に示します。

  - layer: landuse
    - name: 50m_cultural/ne_50m_urban_areas.shp
      class: residential
      minzoom: 4
      maxzoom: 4
    - name: 50m_cultural/ne_50m_urban_areas.shp
      class: residential
      minzoom: 5
      maxzoom: 7
  - layer: landcover
    - name: 110m_physical/ne_110m_glaciated_areas.shp
      class: ice
      subclass: glacier
      minzoom: 0
      maxzoom: 1
    - name: 50m_physical/ne_50m_glaciated_areas.shp
      class: ice
      subclass: glacier
      minzoom: 2
      maxzoom: 4
    - name: 50m_physical/ne_50m_antarctic_ice_shelves_polys.shp
      class: ice
      subclass: ice_shelf
      minzoom: 2
      maxzoom: 4
    - name: 10m_physical/ne_10m_glaciated_areas.shp
      class: ice
      subclass: glacier
      minzoom: 5
      maxzoom: 7
    - name: 10m_physical/ne_10m_antarctic_ice_shelves_polys.shp
      class: ice
      subclass: ice_shelf
      minzoom: 5
      maxzoom: 7
  - layer: water
    - name: 110m_physical/ne_110m_ocean.shp
      class: ocean
      minzoom: 0
      maxzoom: 1
    - name: 50m_physical/ne_50m_ocean.shp
      class: ocean
      minzoom: 2
      maxzoom: 4
    - name: 10m_physical/ne_10m_ocean.shp
      class: ocean
      minzoom: 5
      maxzoom: 7
    - name: 110m_physical/ne_110m_lakes.shp
      class: lakes
      minzoom: 0
      maxzoom: 1
    - name: 50m_physical/ne_50m_lakes.shp
      class: lakes
      minzoom: 2
      maxzoom: 4
    - name: 10m_physical/ne_10m_lakes.shp
      class: lakes
      minzoom: 5
      maxzoom: 7
  - layer: water_name
    - name: 10m_physical/ne_10m_geography_marine_polys.shp
      class: ocean
      minzoom: 0
      maxzoom: 7
  - layer: water_way
    - name: 110m_physical/ne_110m_rivers_lake_centerlines.shp
      class: ocean
      minzoom: 3
      maxzoom: 3
    - name: 50m_physical/ne_50m_rivers_lake_centerlines.shp
      class: ocean
      minzoom: 4
      maxzoom: 5
    - name: 10m_physical/ne_10m_rivers_lake_centerlines.shp
      class: ocean
      minzoom: 6
      maxzoom: 7
  - layer: boundary
    - name: 110m_cultural/ne_110m_admin_0_boundary_lines_land.shp
      admin_level: 2
      minzoom: 0
      maxzoom: 0
    - name: 50m_cultural/ne_50m_admin_0_boundary_lines_land.shp
      admin_level: 4
      minzoom: 0
      maxzoom: 7
    - name: 10m_cultural/ne_10m_admin_0_boundary_lines_land.shp
      admin_level: 2
      minzoom: 3
      maxzoom: 7
    - name: 10m_cultural/ne_10m_admin_1_states_provinces_lines.shp
      admin_level: 4
      minzoom: 5
      maxzoom: 7
  - layer: place
    - name: 110m_cultural/ne_110m_admin_0_countries.shp
      class: country
      attr: NAME_JA
      minzoom: 0
      maxzoom: 5
    - name: 10m_cultural/ne_10m_admin_1_states_provinces.shp
      class: city
      attr: name_ja
      minzoom: 6
      maxzoom: 7

## Pythonのバージョンと必要モジュール

* Pythonのバージョン:3.9.0
* 必要モジュール
  * PyYAML 5.3.1
  * Shaply 1.7.1

## 使用方法

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

### GeoJSONファイルの作成

tile-builder.yamlの作成後、以下のように実行します。

```sh
$ python GJWriter.py
```

### GeoJSONファイルのmbtiles変換

```sh
$ tippecanoe -o z7.mbtiles -z7 z7.json
```

### mbtilesのメタデータ書き換え（任意）

Tileserver-GLのデフォルト設定を使って配信を行う場合は、以下のコマンド（SQLite3）を実行します。

```sh
$ sqlite3 < update.sql
```

## 表示URL

https://labo.takamoto.biz/z7
