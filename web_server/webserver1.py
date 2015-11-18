#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import socket

HOST, PORT = '', 8888

# Server creates a TCP/IP socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Server sets some socket options
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Server binds the address
listen_socket.bind((HOST, PORT))
# Server makes the socket a listening socket
listen_socket.listen(1)

print("Serving HTTP on port {}".format(PORT))

while True:
    client_connection, client_address = listen_socket.accept()
    # 当 telnet 建立连接时打印
    print(1)
    # 1024 表示接收的字节数
    request = client_connection.recv(1024)
    # 当 telnet 发送消息时打印
    print(request)

    http_response = """\
    HTTP/1.1 200 OK

    Hello, World!
    """

    client_connection.sendall(http_response)
    client_connection.close()


