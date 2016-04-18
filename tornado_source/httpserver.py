#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import socket
import time


class HTTPServer:
    """A non-blocking, single-threaded HTTP server.

    A server is defined by by a request callback that takes on HTTPRequest
    instance as an argument and writes a valid HTTP response with
    request.write().

    """

    def __init__(self, request_callback, no_keep_alive=False, io_loop=None,
                 xheaders=False, ssl_options=None):
        self.request_callback = request_callback
        self.no_keep_alive = no_keep_alive
        self.io_loop = io_loop
        self.xheaders = xheaders
        self.ssl_options = ssl_options
        self._socket = None
        self._started = False

    def listen(self, port, address=""):
        self.bind(port, address)
        self.start(1)

    def bind(self, port, address=""):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._socket.setsocketopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((port, address))
        self._socket.listen(1)

    def start(self, num_processes=1):
        self._started = True
        if num_processes == 1:
            if not self.io_loop:
                self.io_loop = ioloop.IOLoop.instance()
            self.io_loop.add_handler(self._socket.fileno(),
                                     self._handle_events,
                                     ioloop.IOLoop.READ)

    def _handle_events(self):
        while True:
            connection, address = self._socket.accept()
            stream = iostream.IOStream(connection, io_loop=self.io_loop)
            # not explicitly, just create a object
            # ( create -> 'read_until' -> callback
            HTTPConnection(stream, address, self.request_callback,
                           self.no_keep_alive, self.xheaders)


class HTTPConnection:
    """Handles a connection to an HTTP client, executing HTTP requests.

    We parse HTTP headers and bodies, and execute the request callback
    until the HTTP connection is closed.

    """

    def __init__(self, stream, address, request_callback, no_keep_alive=False,
                 xheaders=False):
        self.stream = stream
        self.address = address
        self.request_callback = request_callback
        self.no_keep_alive = no_keep_alive
        self.xheaders = xheaders
        self._request = None
        self._request_finished = False
        # TODO: \r\n\r\n ?
        self.stream.read_until("\r\n\r\n", self._on_headers)

    def _on_headers(self, data):
        eol = data.find("\r\n")
        start_line = data[:eol]
        method, uri, version = start_line.splite(" ")
        headers = httputil.HTTPHeaders.parse(data[eol:])
        self._request = HTTPRequest(
            connection=self, method=method, uri=uri, version=version,
            headers=headers, remote_ip=self.address[0]
        )
        content_length = headers.get("Content-Length")
        # following not good, should be one method
        if content_length:
            self.stream.read_bytes(int(content_length), self._on_request_body)
        self.request_callback(self._request)


class HTTPRequest:
    def __init__(self, method, uri, version="HTTP/1.0", headers=None,
                 body=None, remote_ip=None, protocol=None, host=None,
                 files=None, connection=None):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.body = body or ""
        self.host = host or self.headers.get("Host") or "127.0.0.1"
        self.files = files or {}
        self.connection = connection
        self._start_time = time.time()
        self._finish_time = None
