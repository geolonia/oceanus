#!/bin/bash
if [ $# = 1 ]; then
    cp ./shp2geojson.yaml $1
    docker run -it --rm --name oceanus -v $1:/data geolonia/oceanus /app/oceanus
else
    echo "引数１にデータディレクトリを指定してください。"
fi