#!/bin/bash
if [ $# = 1 ]; then
    docker run -it --rm --name tile-builder -v $1:/data geolonia/tile-builder /app/tile-builder
else
    echo "引数１にデータディレクトリを指定してください。"
fi