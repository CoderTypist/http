#!/bin/bash

main() {
	
    local nc_version="$(nc -h 2>&1 | grep netcat | sed -E 's/.*\((.*)\)/\1/g' | awk -F' ' '{ print $NF }')"
    local cr=$'\r'

    get_request_line="$(
		cat <<- EOF
			GET /line.txt HTTP/1.1${cr}
			Host: 127.0.0.1:8888${cr}
			User-Agent: telnet/${nc_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    get_request_lines="$(
		cat <<- EOF
			GET /lines.txt HTTP/1.1${cr}
			Host: 127.0.0.1:8888${cr}
			User-Agent: telnet/${nc_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    get_request_nonexistent="$(
		cat <<- EOF
			GET /nonexistent.txt HTTP/1.1${cr}
			Host: 127.0.0.1:8888${cr}
			User-Agent: telnet/${nc_version}${cr}
			Accept: */*${cr}
			${cr}
		EOF
    )"

    echo "${get_request_line}" | nc 127.0.0.1 8888
    echo "${get_request_lines}" | nc 127.0.0.1 8888
    echo "${get_request_nonexistent}" | nc 127.0.0.1 8888
}

main "$@"
