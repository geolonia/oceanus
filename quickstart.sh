#!/bin/bash
if [ $# = 2 ]; then
    docker run -it --rm --name tile-builder -v $1:/data geolonia/tile-builder /app/tile-builder
    cp /app/tileservr-env.zip /data
    unzip /data/tileservr-env.zip
    docker run -d -it --name tb-server -v $1:/data klokantech/tileserver-gl -c $1/config.json -p $2
else
    echo "引数１にデータディレクトリ、引数２にtileserverのポートを指定してください。"
fi