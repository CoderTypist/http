#!/bin/bash

if [[ -z "${WEB_SERVER_PORT}" ]]; then
    echo "WEB_SERVER_PORT is undefined" >&2
    exit 1
fi

if [[ -z "${WEB_SERVER_DIR}" ]]; then
    echo "WEB_SERVER_DIR is undefined" >&2
    exit 1
fi

if [[ ! -d "${WEB_SERVER_DIR}" ]]; then
    echo "No such directory: ${WEB_SERVER_DIR}"
    exit 1
fi

python3 -m http.server -d "${WEB_SERVER_DIR}" -b "0.0.0.0" "${WEB_SERVER_PORT}"

