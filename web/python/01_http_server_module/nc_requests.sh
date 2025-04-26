#!/bin/bash

main() {
	
    local netcat_version="$(nc -h 2>&1 | grep netcat | sed -E 's/.*\((.*)\)/\1/g' | awk -F' ' '{ print $NF }')"
    local cr=$'\r'

    get_request_line="$(
		cat <<- EOF
			GET /line.txt HTTP/1.1${cr}
			Host: ${WEB_SERVER_IP}:${WEB_SERVER_PORT}${cr}
			User-Agent: netcat/${netcat_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    get_request_lines="$(
		cat <<- EOF
			GET /lines.txt HTTP/1.1${cr}
			Host: ${WEB_SERVER_IP}:${WEB_SERVER_PORT}${cr}
			User-Agent: netcat/${netcat_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    get_request_nonexistent="$(
		cat <<- EOF
			GET /nonexistent.txt HTTP/1.1${cr}
			Host: ${WEB_SERVER_IP}:${WEB_SERVER_PORT}${cr}
			User-Agent: netcat/${netcat_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    echo "${get_request_line}" | nc "${WEB_SERVER_IP}" "${WEB_SERVER_PORT}"
    echo "${get_request_lines}" | nc "${WEB_SERVER_IP}" "${WEB_SERVER_PORT}"
    echo "${get_request_nonexistent}" | nc "${WEB_SERVER_IP}" "${WEB_SERVER_PORT}"
}

source ../setup.src.sh ||
{
    echo "Failed to source setup.src.sh" >&2;
    exit 1;
}
main "$@"
