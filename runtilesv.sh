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
            echo "  -n  container name ( default "\""tilesv"\"" )"
            echo "  -p  port number ( default 80 )"
            echo "  -d  directory for mbtiles ( default "\""/tmp"\"" )"
            exit 1
            ;;
    esac
done

if [ ! -e /data/config.json ]; then
    echo "Deploy the files required for TileserverGL."
    tar xvf ./tilesvenv.tar.gz -C $DIR
fi
if [ "$(docker container ls -q -f name=${CONTAINER_NAME})" ]; then
    echo "Container ${CONTAINER_NAME} is running."
    echo "Stop container ${CONTAINER_NAME}."
    docker container stop $CONTAINER_NAME
fi
if [ "$(docker container ls -a -q -f name=${CONTAINER_NAME})" ]; then
    echo "Container ${CONTAINER_NAME} already exist."
    echo "Remove container ${CONTAINER_NAME}."
    docker container rm $CONTAINER_NAME
fi
docker container rm $CONTAINER_NAME
if [ $PORTNO -ge 1 ]; then
    docker run -d -it --name $CONTAINER_NAME -v $DIR:/data -p $PORTNO:80 klokantech/tileserver-gl
    echo "docker run -d -it --name ${CONTAINER_NAME} -v ${DIR}:/data -p ${PORTNO}:80 klokantech/tileserver-gl"
else
    docker run -d -it --name $CONTAINER_NAME -v $DIR:/data klokantech/tileserver-gl
    echo "docker run -d -it --name ${CONTAINER_NAME} -v ${DIR}:/data -p ${PORTNO}:80 klokantech/tileserver-gl"
fi
