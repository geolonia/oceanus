#!/bin/bash
if [ $# = 2 ]; then
    docker run -it --rm --name tile-builder -v $1:/data geolonia/tile-builder /app/tile-builder
    docker run -d -it --name tb-server -v $1:/data -p $2:80 klokantech/tileserver-gl -c $1/config.json
else
    echo "引数１にデータディレクトリ、引数２にtileserverのポートを指定してください。"
fi