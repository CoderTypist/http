#/bin/bash

source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}

docker run -ti --rm \
    -v "$(realpath ../../files)":/src/files \
    --entrypoint=/bin/bash \
    -p "${WEB_SERVER_PORT}":"${WEB_SERVER_PORT}" \
    web:1.0
