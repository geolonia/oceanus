while getopts ":d:p:h" OPT; do
    case "$OPT" in
        p) PORTNO="$OPTARG" ;;
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
            echo "  Specifies the port number."
            echo "      [-p ...]"
            echo "  Specifies the directory for input data."
            echo "      [-d ...]"
            exit 1
            ;;
    esac
done
echo ${DIR}