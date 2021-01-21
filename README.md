# Oceanus

このプロジェクトでは、簡単なコマンドを数回実行するだけで、Natural Earth のデータをベースとしたベクトルタイルを生成することができます。

Oceanus（オケアノス）とは、ギリシャ神話に登場する天空の神ウラノスと大地の女神ガイアの子として生まれた水の神です。世界中に3,000もの河川を作り出し、英語の「海（ocean）」の語源でもあります。

世界中の川や湖の創造主であり、地球をデジタル世界上に創造するという願いをこめて、この名前をつけました。ギリシャの詩人ホメロスはオケアノスを「万物の始まり」と評しています。

このプロジェクトが地球のデータをデジタルの世界に創造する「万物の始まり」の手助けとなりたい、という願いを込めて、ギリシャ神話にあやかってオケアノスという名前をつけてみました。

なお、映画「ローマの休日」で、オードリー・ヘプバーンが手を入れる「真実の口」は、オケアノスがモデルではないかと言われているそうです。
## 概要

[NaturalEarth](https://www.naturalearthdata.com)からシェープファイルをダウンロードしmbtilesに変換します。
具体的には、設定ファイル（shp2geojson.yaml）で指定したシェープファイルをGeoJSON形式に変換し、tippecanoeを使ってmbtilesに変換します。  
変換したmbtilesは、runtilesv.shスクリプト（TileserverGLのDockerコンテナを作成）を使って配信できます。

## 利用方法
Oceanusによる地図表示までの流れを以降に示します。
### mbtilesの作成
mbtilesの作成は以下のように行います。
```
$ git clone https://github.com/geolonia/oceanus  
$ cd oceanus  
$ ./oceanus.sh
```
`oceanus.sh`は、Oceanus用のDockerイメージをビルドしNatural Earthデータをダウンロードして`oceanus.mbtiles`を作成します。  
以下のオプションを指定できます。  
* `-d`：`oceanus.mbtiles` を作成するディレクトリを指定します。（未指定時は`/tmp`）  

### HTTPによる配信
HTTPによる配信は以下のように行います。
```
$ ./runtilesv.sh  
```
`runtilesv.sh`は、TileserverGLのDockerコンテナを作成し mbtiles を配信します。  
以下のオプションを指定できます。  
* `-d`：`oceanus.mbtiles`が存在するディレクトリを指定します。（未指定時は`/tmp`）
* `-p`：配信ポート番号を指定します。（未指定時は`80`）
* `-n`：TileserverGLのコンテナ名を指定します。（未指定時は`tilesv`）

### 地図の表示
`runtilesv.sh`実行後、ブラウザからURL `http://localhost:ポート番号` を指定するとTileserverGLの初期画面が表示されます。スタイル"basic"を指定することで地図を表示できます。  

## 参考

### NaturalEarthからダウンロードするデータ

 * 110m_physical(3.4MB)
 * 110m_cultural(1.3MB)
 * 50m_physical(7.1MB)
 * 50m_cultural(7.9MB)
 * 10m_physical(4.7MB)
 * 10m_cultural(206.7MB)

### shp2geojson.yamlの設定項目

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

### 使用プロダクト

* [tippecanoe](https://github.com/mapbox/tippecanotileservewr-gl)
* [tileserver-gl](https://github.com/maptiler/tileserver-gl)
* [Google Font:Noto Sans JP](https://fonts.google.com/specimen/Noto+Sans+JP?subset=japanese)
* Python3.6.9
* Python拡張モジュール
  * PyYAML 5.3.1
  * fiona 1.8.18
  * Shaply 1.7.1
  
### タイルのメタデータ（サンプル）

```
{
  "vector_layers": [
    {
      "id": "boundary",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "admin_level": "Number"
      }
    },
    {
      "id": "landcover",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String",
        "subclass": "String"
      }
    },
    {
      "id": "landuse",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String"
      }
    },
    {
      "id": "place",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String",
        "name:en": "String"
      }
    },
    {
      "id": "water",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String"
      }
    },
    {
      "id": "water_name",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String"
      }
    },
    {
      "id": "water_way",
      "description": "",
      "minzoom": 0,
      "maxzoom": 7,
      "fields": {
        "class": "String"
      }
    }
  ],
  "tilestats": {
    "layerCount": 7,
    "layers": [
      {
        "layer": "boundary",
        "count": 11123,
        "geometry": "LineString",
        "attributeCount": 1,
        "attributes": [
          {
            "attribute": "admin_level",
            "count": 2,
            "type": "number",
            "values": [
              2,
              4
            ],
            "min": 2,
            "max": 4
          }
        ]
      },
      {
        "layer": "landcover",
        "count": 2497,
        "geometry": "Polygon",
        "attributeCount": 2,
        "attributes": [
          {
            "attribute": "class",
            "count": 1,
            "type": "string",
            "values": [
              "ice"
            ]
          },
          {
            "attribute": "subclass",
            "count": 2,
            "type": "string",
            "values": [
              "glacier",
              "ice_shelf"
            ]
          }
        ]
      },
      {
        "layer": "landuse",
        "count": 4286,
        "geometry": "Polygon",
        "attributeCount": 1,
        "attributes": [
          {
            "attribute": "class",
            "count": 1,
            "type": "string",
            "values": [
              "residential"
            ]
          }
        ]
      },
      {
        "layer": "place",
        "count": 4771,
        "geometry": "Point",
        "attributeCount": 2,
        "attributes": [
          {
            "attribute": "class",
            "count": 2,
            "type": "string",
            "values": [
              "city",
              "country"
            ]
          },
          {
            "attribute": "name:en",
            "count": 1000,
            "type": "string",
            "values": [
              "None",
              "­キャンギャルリ県",
              "­ボグダンツィ",
              "­ボシロヴォ",
              "­ヴァシレヴォ",
              "­ヴァランドヴォ",
              "アアーナ",
              "アイウォ地区",
              "アイウン＝ブジュール＝サキア・エル・ハムラ地方",
              "アイオワ州",
              "アイガイレタイ",
              "アイスランド",
              "アイズクラウクレ",
              "アイズプテ",
              "アイセン・デル・ヘネラル・カルロス・イバニェス・デル・カンポ州",
              "アイダホ州",
              "アイツタキ島",
              "アイドゥン県",
              "アイドフシュチナ",
              "アイナロ県",
              "アイメリーク州",
              "アイライ州",
              "アイルランド",
              "アイレウ県",
              "アインシーレム",
              "アインデフラ県",
              "アイン・ティムシェント県",
              "アウスト・アグデル県",
              "アウター・ヘブリディーズ",
              "アウツェ",
              "アウロラ州",
              "アウ・カップ",
              "アオスタ",
              "アカバ県",
              "アガゴ県",
              "アガデス州",
              "アガレガ諸島",
              "アクサライ県",
              "アクトベ州",
              "アクニーステ",
              "アクモラ州",
              "アクラン州",
              "アクリンズ",
              "アクレ州",
              "アクワ・イボム州",
              "アグアスカリエンテス州",
              "アグジャバディ県",
              "アグスタファ県",
              "アグス県",
              "アグダシュ県",
              "アグダム県",
              "アグリジェント県",
              "アグルァナ",
              "アサバ州",
              "アザド・カシミール",
              "アシャンティ州",
              "アシュート県",
              "アジャリア自治共和国",
              "アジュダービヤー",
              "アジュマニ県",
              "アジュマーン",
              "アジュルン県",
              "アスアイ県",
              "アスア州",
              "アスィール州",
              "アスコリ・ピチェーノ県",
              "アスタナ",
              "アスタラ県",
              "アスティ県",
              "アストゥリアス州",
              "アストラハン州",
              "アスワン県",
              "アスンシオン",
              "アセンション島",
              "アゼルバイジャン",
              "アゾレス諸島",
              "アタカマ州",
              "アタコラ県",
              "アタード",
              "アダナ県",
              "アダマワ州",
              "アチェ州",
              "アックアヴィーヴァ",
              "アッサム州",
              "アッタプー県",
              "アッティキ",
              "アッドゥ環礁",
              "アッバ",
              "アッパー・イースト州",
              "アッパー・ウエスト州",
              "アッパー・タクトゥ＝アッパー・エセキボ州",
              "アッパー・デメララ＝ベルビセ州",
              "アッペンツェル・アウサーローデン準州",
              "アッペンツェル・インナーローデン準州",
              "アッ＝ザアーイン",
              "アッ＝シャマール",
              "アティラウ州",
              "アディゲ共和国",
              "アディスアベバ",
              "アデン県"
            ]
          }
        ]
      },
      {
        "layer": "water",
        "count": 1658,
        "geometry": "Polygon",
        "attributeCount": 1,
        "attributes": [
          {
            "attribute": "class",
            "count": 2,
            "type": "string",
            "values": [
              "lakes",
              "ocean"
            ]
          }
        ]
      },
      {
        "layer": "water_name",
        "count": 307,
        "geometry": "Polygon",
        "attributeCount": 1,
        "attributes": [
          {
            "attribute": "class",
            "count": 1,
            "type": "string",
            "values": [
              "ocean"
            ]
          }
        ]
      },
      {
        "layer": "water_way",
        "count": 1928,
        "geometry": "LineString",
        "attributeCount": 1,
        "attributes": [
          {
            "attribute": "class",
            "count": 1,
            "type": "string",
            "values": [
              "ocean"
            ]
          }
        ]
      }
    ]
  }
}
```

### 変換結果表示URL

[https://labo.takamoto.biz/oceanus](https://labo.takamoto.biz/oceanus)
