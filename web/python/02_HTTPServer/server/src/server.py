#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os
from pathlib import Path
import sys


class DirectoryNotFoundError(FileNotFoundError):
    def __init__(self, message=None):
        super().__init__(message)


class WebServerHTTPRequestHandler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"

    def __init__(self, request, client_address, server):
        self.base_dir = os.environ.get("WEB_SERVER_DIR")
        super().__init__(request, client_address, server)

    def do_GET(self):

        path = urlparse(self.path).path
        # query = parse_qs(urlparse(self.path).query)

        match path:

            case "/" | "/index.html":
                try:
                    with open(f"{self.base_dir}/index.html", "rb") as f_html:
                        b_html = f_html.read()
                except Exception as e:
                    print(e)
                    self.send_error(500, "Internal Server Error")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(b_html))
                self.end_headers()
                self.wfile.write(b_html)

            case "/forms/get.html":
                try:
                    with open(f"{self.base_dir}/forms/get.html", "rb") as f_html:
                        b_html = f_html.read()
                except Exception as e:
                    print(e)
                    self.send_error(500, "Internet Server Error")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(b_html))
                self.end_headers()
                self.wfile.write(b_html)

            case "/forms/post.html":
                try:
                    with open(f"{self.base_dir}/forms/post.html", "rb") as f_html:
                        b_html = f_html.read()
                except Exception as e:
                    print(e)
                    self.send_error(500, "Internet Server Error")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(b_html))
                self.end_headers()
                self.wfile.write(b_html)

            case "/forms/delete.html":
                try:
                    with open(f"{self.base_dir}/forms/delete.html", "rb") as f_html:
                        b_html = f_html.read()
                except Exception as e:
                    print(e)
                    self.send_error(500, "Internet Server Error")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", len(b_html))
                self.end_headers()
                self.wfile.write(b_html)
            
            case _:
                self.send_error(404, "Not found")
    
    def do_POST(self):
        ...

    def do_DELETE(self):
        ...


def main():

    # get server config
    if not (WEB_SERVER_IP := os.environ.get("WEB_SERVER_IP")):
        print("WEB_SERVER_IP is undefined.", file=sys.stderr)
        sys.exit(1)

    if not (WEB_SERVER_PORT := os.environ.get("WEB_SERVER_PORT")):
        print("WEB_SERVER_PORT is undefined.", file=sys.stderr)
        sys.exit(1)
    WEB_SERVER_PORT = int(WEB_SERVER_PORT)
    
    if not (WEB_SERVER_DIR := os.environ.get("WEB_SERVER_DIR")):
        print("WEB_SERVER_PORT is undefined.", file=sys.stderr)
        sys.exit(1)

    # validate server config
    if not os.path.exists(WEB_SERVER_DIR):
        print("ERROR: Tried to serve a non-existent directory", file=sys.stderr)
        raise DirectoryNotFoundError(f"No such directory: {WEB_SERVER_DIR}")
    
    if not os.path.isdir(WEB_SERVER_DIR):
        print(f"ERROR: {WEB_SERVER_DIR} is not a directory", file=sys.stderr)
        raise NotADirectoryError(f"Not a directory: {WEB_SERVER_DIR}")
    
    # print config
    print(f"WEB_SERVER_IP:   {WEB_SERVER_IP}")
    print(f"WEB_SERVER_PORT: {WEB_SERVER_PORT}")
    print(f"WEB_SERVER_DIR:  {WEB_SERVER_DIR}")

    # start server
    httpd = HTTPServer((WEB_SERVER_IP, WEB_SERVER_PORT), WebServerHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()

