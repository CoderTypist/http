#/bin/bash

source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}

docker run -ti --rm \
    -v "$(realpath ../../files)":/src/files \
    --entrypoint=/bin/bash \
    -e WEB_SERVER_IP="${WEB_SERVER_IP}" \
    -e WEB_SERVER_PORT="${WEB_SERVER_PORT}" \
    -e WEB_SERVER_DIR="${WEB_SERVER_DIR}" \
    -p "${WEB_SERVER_PORT}":"${WEB_SERVER_PORT}" \
    web:1.0

