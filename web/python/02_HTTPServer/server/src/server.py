#!/usr/bin/env python3


from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import sys
from urllib.parse import urlparse, parse_qs


class DirectoryNotFoundError(FileNotFoundError):
    def __init__(self, message=None):
        super().__init__(message)


class NotARegularFileError(OSError):
    def __init__(self, message=None):
        super().__init__(message)


class FileContents:

    def __init__(self, fpath):
        self.fpath = fpath
        self.text = ""
        self.binary = b''
        self.mtime = 0
        self.update()

    def is_modified(self):
        if self.mtime == self.fpath.stat().st_mtime:
            return False
        return True

    def update(self):
        if not self.fpath.exists():
            raise FileNotFoundError(f"No such file: {self.fpath}")
        if not self.fpath.is_file():
            raise NotARegularFileError(f"{self.fpath} is not a regular file")
        with open(self.fpath, "r") as fhandle:
            self.text = fhandle.read()
        self.binary = self.text.encode("utf-8")
        self.mtime = self.fpath.stat().st_mtime

# get instantiated with each new request :/
class WebServerHTTPRequestHandler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"
    cached_files = {}

    def __init__(self, request, client_address, server):
        self.base_dir = Path(os.environ.get("WEB_SERVER_DIR"))
        self._cached_files = WebServerHTTPRequestHandler.cached_files
        self.init_cache()
        super().__init__(request, client_address, server)

    def init_cache(self):
        if len(self._cached_files) == 0:
            for fpath in self.base_dir.rglob("*"):
                if fpath.is_file():
                    print(f" - init cache: {fpath}")
                    self.read_file(str(fpath).removeprefix(str(self.base_dir)))

    def read_file(self, fpath) -> FileContents:

        fpath = Path(f"{self.base_dir}{fpath}")
        
        # do not serve a non-existent file, even if cached
        if not fpath.exists():
            if self._cached_files.get(fpath):
                print(f" - removed {fpath} from the cache")
                del self._cached_files[fpath]
            raise FileNotFoundError(f"No such file: {fpath}")
        
        if not fpath.is_file():
            if self._cached_files.get(fpath):
                print(f" - removed {fpath} from the cache")
                del self._cached_files[fpath]
            raise NotARegularFileError(f"{fpath} is not a regular file")

        # get file
        cached_file: FileContents = self._cached_files.get(fpath)
        if cached_file:
            print(f" - cache hit: {fpath}")
            if cached_file.is_modified():
                print(f"   - modified")
                cached_file.update()
                print(f"   - updated")
            return cached_file
        else:
            print(f" - cache miss: {fpath}")
            self._cached_files[fpath] = FileContents(fpath)
            return self._cached_files[fpath]
    
    def send_success(self, code, binary):
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(binary))
        self.end_headers()
        self.wfile.write(binary)

    def do_GET(self):
        
        # validate path
        valid_paths = [
            "/index.html",
            "/forms/get.html",
            "/forms/post.html",
            "/forms/delete.html"
        ]

        path = urlparse(self.path).path # query = parse_qs(urlparse(self.path).query)

        if path == "/":
            path = "/index.html"
        
        if path not in valid_paths:
            try:
                self.log_error(f"GET request for non-existent resource: {path}")
                self.send_error(404, "Not Found")
            except Exception as e:
                self.log_error(f"Response error: 404: {path}: {e}")
                return

        # read file
        try:
            fcontents = self.read_file(path)
        except Exception as e:
            self.log_error(f"Failed to read {path}: {e}")
            try:
                self.send_error(500, "Internal Server Error")
            except Exception as e:
                self.log_error(f"Response error: 500: {e}")
            return
        
        # create response
        response = fcontents.binary

        # send response
        try:
            self.send_success(200, response)
        except Exception as e:
            self.log_error(f"Failed to serve {path}: {e}")
            return
    
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

