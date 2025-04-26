#!/bin/bash

source ../setup.src.sh ||
{
    echo "Failed to source setup.src.sh" >&2;
    exit 1;
}
python3 -m http.server -d "${WEB_SERVER_DIR}" -b "${WEB_SERVER_IP}" "${WEB_SERVER_PORT}"

