#!/bin/bash

source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}

docker build \
    -t web:1.0 \
    -f ./Dockerfile-web \
    --build-arg WEB_SERVER_IP="${WEB_SERVER_IP}" \
    --build-arg WEB_SERVER_PORT="${WEB_SERVER_PORT}" \
    --build-arg WEB_SERVER_DIR="/src/files" \
    ../../

