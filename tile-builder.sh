#!/bin/bash
if [ $# = 1 ]; then
    cp ./tile-builder.yaml $1
    docker run -it --rm --name tile-builder -v $1:/data geolonia/tile-builder /app/tile-builder
else
    echo "引数１にデータディレクトリを指定してください。"
fi