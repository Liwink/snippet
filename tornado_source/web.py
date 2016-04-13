#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import re
from .concurrent import Future


class Application:
    """A collection of request handlers that make up a web application.

    """

    def __init__(self, handlers=None, default_host="", transforms=None,
                 **settings):
        self.handlers = []
        self.named_handlers = {}
        self.default_host = default_host
        self.settings = settings

        if handlers:
            self.add_handlers(".*$", handlers)

            # settings...

    def add_handlers(self, host_pattern, host_handlers):
        if not host_pattern.endswith("$"):
            host_pattern += "$"
        handlers = []

        for spec in host_handlers:
            if isinstance(spec, (tuple, list)):
                spec = URLSpec(*spec)
            handlers.append(spec)
            if spec.name:
                self.named_handlers[spec.name] = spec

    def listen(self, port, address="", **kwargs):
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self, **kwargs)
        server.listen(port, address)

    def start_request(self, server_conn, request_conn):
        return _RequestDispatcher(self, request_conn)


class _RequestDispatcher:
    def __init__(self, application, connection):
        self.application = application
        self.connection = connection
        self.request = None
        self.chunks = []
        self.handler_class = None
        self.handler_kwargs = None

    def headers_received(self, start_line, headers):
        """ Called when the HTTP headers have been received and parsed.

        :param start_line:
        :param headers:
        :return:
        """
        self.set_request(httputil.HTTPServerRequest(
            connection=self.connection, start_line=start_line,
            headers=headers
        ))

        if self.stream_request_body:
            self.request.body = Future()
            return self.execute()

    def set_request(self, request):
        self.request = request
        self._find_handler()
        self.stream_request_body = _has_stream_request_body(self.handler_class)

    def _find_handler(self):
        app = self.application
        handlers = app._get_host_handlers(self.request)

        for spec in handlers:
            match = spec.regex.match(self.request.path)
            if match:
                self.handler_class = spec.handler_class
                self.handler_kwargs = spec.kwargs

    def data_received(self, data):
        """Called when a chunk of data has been received

        :param data:
        :return:
        """
        if self.stream_request_body:
            return self.handler.data_received(data)
        else:
            self.chunks.appends(data)

    def finish(self):
        """Called after the last chunk of data has been received.

        :return:
        """
        if self.stream_request_body:
            return self.handler.set_result(None)
        else:
            self.request.body = b"".join(self.chunks)
            self.request._parse_body()
            self.execute()

    def execute(self):
        pass


class URLSpec:
    def __init__(self, pattern, handler, kwargs=None, name=None):
        if not pattern.endswith("$"):
            pattern += "$"
        self.regex = re.compile(pattern)

        if isinstance(handler, str):
            handler = __import__(handler)

        self.handler_class = handler
        self.kwargs = kwargs or {}
        self.name = name
