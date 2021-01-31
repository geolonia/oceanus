#!/bin/bash
CONTAINER_NAME="tilesv"
DIR="/tmp"
PORTNO=80

while getopts ":d:p:n:h" OPT; do
    case "$OPT" in
        p) PORTNO="$OPTARG" ;;
        n) CONTAINER_NAME="$OPTARG" ;;
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
            echo "Usage: runtilesv.sh [options]"
            echo "Options:"
            echo "  -n  container name ( default "\""${CONTAINER_NAME}"\"" )"
            echo "  -p  port number ( default "\""${PORTNO}"\"" )"
            echo "  -d  directory for mbtiles ( default "\""${DIR}"\"" )"
            exit 1
            ;;
    esac
done

if [ "$(docker container ls -q -f name=${CONTAINER_NAME})" ]; then
    echo "Container ${CONTAINER_NAME} is running."
    echo "Stop and remove container ${CONTAINER_NAME}."
    docker container stop $CONTAINER_NAME
    docker container rm $CONTAINER_NAME
fi
if [ "$(docker container ls -a -q -f name=${CONTAINER_NAME})" ]; then
    echo "Container ${CONTAINER_NAME} already exist."
    echo "Remove container ${CONTAINER_NAME}."
    docker container rm $CONTAINER_NAME
fi
cp ./config.json $DIR
mkdir $DIR/styles
cp ./style.json $DIR
docker run -d -it --name $CONTAINER_NAME -v $DIR:/data -p $PORTNO:8080 maptiler/tileserver-gl -c /data/config.json
echo "docker run -d -it --name ${CONTAINER_NAME} -v ${DIR}:/data -p ${PORTNO}:8080 maptiler/tileserver-gl -c /data/config.json"
