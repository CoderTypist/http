#/bin/bash

source "../../web.env" ||
{
    echo "Failed to source ../../web.env";
    exit 1;
}

docker run -ti --rm \
    -v "$(realpath ../../files/)":/app/files/ \
    -v "$(realpath ../../data/):/app/data/" \
    -v "$(realpath ../src/)":/app/server/src/ \
    --entrypoint=/bin/bash \
    -e WEB_SERVER_IP="${WEB_SERVER_IP}" \
    -e WEB_SERVER_PORT="${WEB_SERVER_PORT}" \
    -e WEB_SERVER_DIR="${WEB_SERVER_DIR}" \
    -e DATABASE_DIR="${DATABASE_DIR}" \
    -e DATABASE_FNAME="${DATABASE_FNAME}" \
    -p "${WEB_SERVER_PORT}":"${WEB_SERVER_PORT}" \
    web:1.1

