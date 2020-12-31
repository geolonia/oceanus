#!/bin/bash
DIR="/tmp"
while getopts ":d:h" OPT; do
    case "$OPT" in
        d)
            if [ "$OPTARG"="." ]; then
                DIR=$(cd "$OPTARG" && pwd)
            elif [ "$OPTARG:0:3"="../" ]; then
                DIR=$(cd "$OPTARG" && pwd)/$OPTARG
            else
                DIR="$OPTARG"
            fi
            ;;
        h)
            echo "Usage: oceanus.sh [options]"
            echo "  Specifies the directory for output."
            echo "      [-d ...]"
            exit 1
            ;;
    esac
done

cp ./shp2geojson.yaml $DIR
echo "cp ./shp2geojson.yaml ${DIR}"
docker run -it --rm --name oceanus -v $DIR:/data geolonia/oceanus /app/ne2mbtiles
echo "docker run -it --rm --name oceanus -v ${DIR}:/data geolonia/oceanus /app/ne2mbtiles"