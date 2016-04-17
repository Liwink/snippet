#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import socket


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
            HTTPConnection(stream, address, self.request_callback,
                           self.no_keep_alive, self.xheaders)



