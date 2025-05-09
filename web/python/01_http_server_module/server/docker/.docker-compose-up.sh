#!/bin/bash

# alternative to exporting is to have a .env file
set -a
source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}
set +a

docker-compose up --build
