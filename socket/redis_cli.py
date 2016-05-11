#!/usr/bin/env python
# encoding: utf-8

import socket

class Redis():
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

        sock.connect(("localhost", 6379))
        self.sock = sock

    def get(self, key):
        command = "*2\r\n$3\r\nGET\r\n$5\r\n{0}\r\n".format(key).encode()
        self.sock.sendall(command)
        response = self.sock.recv(1024).decode()
        i = int(response[1])
        return response[4:4+i]


