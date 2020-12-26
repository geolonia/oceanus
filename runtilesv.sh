#!/bin/bash
if [ $# = 2 ]; then
    docker run -it --rm --name tile-builder -v $1:/data geolonia/tile-builder /app/settilesvenv
    docker container stop tilesv
    docker container rm tilesv
    docker run -d -it --name tilesv -v $1:/data -p $2:80 klokantech/tileserver-gl -c /data/config.json
else
    echo "引数１にデータディレクトリ、引数２にtileserverのポート番号を指定してください。"
fi