#!/bin/bash

# export for yaml interpolation
set -a
source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}
set +a

docker-compose up --build

