#!/usr/bin/env python
# encoding: utf-8

import socket

sock = socket.socket(socket.AF_INET, socket.SOCKET_STREAM, 0)
sock.setsockopt(socket.TCP, socket.TCP_NODELAY, 1)

sock.connect(("localhost", 6379))

sock.sendall(b'*2\r\n$3\r\nGET\r\n$5\r\nbaidu\r\n')
sock.recv(1024)
