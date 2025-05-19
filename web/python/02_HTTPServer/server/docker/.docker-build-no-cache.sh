#!/bin/bash

while read -r line; do
    if ! echo "$line" | GREP_COLORS='ms=0;36' grep --color -E "^#0 .*|^#[0-9]+ \[.*] .*"; then
        echo "$line"
    fi
done < <(docker build -t web:1.1 -f ./Dockerfile-web --progress=plain --no-cache ../../ 2>&1)
