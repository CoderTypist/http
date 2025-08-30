#!/usr/bin/env python3

import os
import requests
import sys


def main():
    
    if not (WEB_SERVER_IP := os.environ.get("WEB_SERVER_IP")):
        print("WEB_SERVER_IP is undefined.", file=sys.stderr)
        sys.exit(1)
    if not (WEB_SERVER_PORT := os.environ.get("WEB_SERVER_PORT")):
        print("WEB_SERVER_PORT is undefined.", file=sys.stderr)
        sys.exit(1)

    fnames = ["line.txt", "lines.txt", "nonexistent.txt"]
    for fname in fnames:
        print()
        try:
            resp = requests.get(f"http://{WEB_SERVER_IP}:{WEB_SERVER_PORT}/{fname}")

            print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

            print(f"GET /{fname} HTTP/1.1")
            for header in resp.request.headers:
                print(f"{header}: {resp.request.headers[header]}")
            
            print("\n. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n")
            
            http_version = f"{resp.raw.version/10}.{resp.raw.version%10}"
            print(f"HTTP/{http_version} {resp.status_code} {resp.reason}")
            for header in resp.headers:
                print(f"{header}: {resp.headers[header]}")
            print('\n\n', end='')
            print(resp.text, end='')

        except requests.exceptions.RequestException as e:
            print(e)
            print(f"Error in requesting {fname}", file=sys.stderr)
            sys.exit(1)
    
    print()


if __name__ == "__main__":
    main()
