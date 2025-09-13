#!/usr/bin/env python3


from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from pathlib import Path
import sqlite3
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

    def is_modified(self) -> bool:
        if self.mtime == self.fpath.stat().st_mtime:
            return False
        return True

    def update(self) -> None:
        if not self.fpath.exists():
            raise FileNotFoundError(f"No such file: {self.fpath}")
        if not self.fpath.is_file():
            raise NotARegularFileError(f"{self.fpath} is not a regular file")
        with open(self.fpath, "r") as fhandle:
            self.text = fhandle.read()
        # self.binary = self.text.encode("utf-8")
        self.mtime = self.fpath.stat().st_mtime

# get instantiated with each new request :/
class WebServerHTTPRequestHandler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"
    cached_files = {}

    def __init__(self, request, client_address, server):
        for cls_attr in ['web_server_ip', 'web_server_port', 'web_server_dir', 'database_dir', 'database_name', 'conn', 'cached_files']:
            setattr(self, cls_attr, getattr(WebServerHTTPRequestHandler, cls_attr))
        super().__init__(request, client_address, server)

    # def init_cache(self):
    #     if len(self.cached_files) == 0:
    #         for fpath in self.base_dir.rglob("*"):
    #             if fpath.is_file():
    #                 print(f" - init cache: {fpath}")
    #                 self.read_file(str(fpath).removeprefix(str(self.base_dir)))

    def read_file(self, fpath) -> FileContents:
        """
        Returns a file's contents.
        Caching is transparent to the caller.
        If a file is cached and hasn't been modified, the cached file is returned.
        If the file isn't cached or has been modified, the file contents are read from disk.
        """
        fpath = Path(f"{self.web_server_dir}{fpath}")
        
        # do not serve a non-existent file, even if cached
        if not fpath.exists():
            if self.cached_files.get(fpath):
                print(f" - removed '{fpath}' from the cache")
                del self.cached_files[fpath]
            raise FileNotFoundError(f"No such file: '{fpath}'")
        
        if not fpath.is_file():
            if self.cached_files.get(fpath):
                print(f" - removed {fpath} from the cache")
                del self.cached_files[fpath]
            raise NotARegularFileError(f"Not a regular file: '{fpath}'")

        # get file
        cached_file: FileContents = self.cached_files.get(fpath)
        if cached_file:
            print(f" - cache hit: {fpath}")
            if cached_file.is_modified():
                print(f"   - modified")
                cached_file.update()
                print(f"   - updated")
            return cached_file
        else:
            print(f" - cache miss: {fpath}")
            self.cached_files[fpath] = FileContents(fpath)
            return self.cached_files[fpath]
    
    def send_success(self, code, binary):
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(binary))
        self.end_headers()
        self.wfile.write(binary)

    def do_GET(self):
        
        # valid paths
        valid_paths = [
            "/index.html",
            "/forms/get.html",
            "/forms/post.html",
            "/forms/delete.html"
        ]

        # get path
        path = urlparse(self.path).path # query = parse_qs(urlparse(self.path).query)

        # adjust path
        if path == "/":
            path = "/index.html"
        
        # validate path
        if path not in valid_paths:
            try:
                self.log_error(f"GET request for invalid resource '{path}'")
                self.send_error(404, "Not Found")
            except Exception as e:
                self.log_error(f"Response error: 404: Failed to send '{path}': {e}")
                return

        # read file
        try:
            fcontents = self.read_file(path)
        except Exception as e:
            self.log_error(f"Failed to read '{path}': {e}")
            try:
                self.send_error(500, "Internal Server Error")
            except Exception as e:
                self.log_error(f"Response error: 500: {e}")
            return
        
        # response body
        body = fcontents.text.encode('utf-8')

        # send response
        try:
            self.send_success(200, body)
        except Exception as e:
            self.log_error(f"Failed to serve '{path}': {e}")
            return
    
    def do_POST(self):
        ...


def main():

    # get server config
    for env_name in ["WEB_SERVER_IP", "WEB_SERVER_PORT", "WEB_SERVER_DIR", "DATABASE_DIR", "DATABASE_FNAME"]:
        env_val = os.environ.get(env_name)
        if env_val:
            setattr(WebServerHTTPRequestHandler, env_name.lower(), env_val if env_name != 'WEB_SERVER_PORT' else int(env_val))
            print("{:<16} {}".format(env_name + ":", env_val))
        else:
            print(f"{env_name} is undefined.", file=sys.stderr)
            sys.exit(1)

    # validate server configs
    web_server_dir = WebServerHTTPRequestHandler.web_server_dir
    database_dir = WebServerHTTPRequestHandler.database_dir
    database_file = WebServerHTTPRequestHandler.database_file

    if not os.path.exists(web_server_dir):
        raise DirectoryNotFoundError(f"No such directory: '{web_server_dir}'")
    if not os.path.isdir(WebServerHTTPRequestHandler.web_server_dir):
        raise NotADirectoryError(f"Not a directory: '{web_server_dir}'")
    if not os.path.isdir(database_dir):
        raise NotADirectoryError(f"Not a directory: '{database_dir}'")
    
    # create database
    db_file = Path(f"{database_dir}/{database_file}")
    if not db_file.exists():
        setattr(WebServerHTTPRequestHandler, 'conn', sqlite3.connect(db_file))
    
    # start server
    addr = (WebServerHTTPRequestHandler.web_server_ip, WebServerHTTPRequestHandler.web_server_port)
    httpd = HTTPServer(addr, WebServerHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()

