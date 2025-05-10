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

            print("\n-----------------------\n")
            
            print("REQUEST:\n")
            
            print(f"[{resp.request.url}]")
            for header in resp.request.headers:
                print(f"{header}: {resp.request.headers[header]}")
            
            print("\n- - - - - - - - - - - -\n")
            
            print("RESPONSE:\n")

            for header in resp.headers:
                print(f"{header}: {resp.headers[header]}")
            print(f"[Status Code: {resp.status_code}]")
            print(resp._content)

        except requests.exceptions.RequestException as e:
            print(e)
            print(f"Error in requesting {fname}", file=sys.stderr)
            sys.exit(1)
    
    print()

if __name__ == "__main__":
    main()

