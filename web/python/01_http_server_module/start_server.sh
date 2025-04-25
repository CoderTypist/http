#!/bin/bash

source setup.src.sh
python3 -m http.server -d "${WEB_SERVER_DIR}" -b "${WEB_SERVER_IP}" "${WEB_SERVER_PORT}"

