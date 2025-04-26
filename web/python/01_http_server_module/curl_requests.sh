#!/bin/bash

main() {

    curl --trace - "http://${WEB_SERVER_IP}:${WEB_SERVER_PORT}/line.txt" ||
    {
        echo "Error in requesting /line.txt" >&2;
        exit 1;
    }

    curl --trace - "http://${WEB_SERVER_IP}:${WEB_SERVER_PORT}/lines.txt" ||
    {
        echo "Error in requesting /lines.txt" >&2;
        exit 1;
    }

    curl --trace - "http://${WEB_SERVER_IP}:${WEB_SERVER_PORT}/nonexistent.txt" ||
    {
        echo "Error in requesting /nonexistent.txt" >&2;
        exit 1;
    }
}

source ../setup.src.sh ||
{
    echo "Failed to source setup.src.sh" >&2;
    exit 1;
}
main "$@"

