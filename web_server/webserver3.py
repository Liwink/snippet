#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import os
import errno
import signal
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = "", 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    # set up a SIGCHLD event handler but instead of wait use a waitpid system call with a WNOHANG option in a
    # loop to make sure that all terminated child processes are taken care of.
    while True:
        try:
            pid, status = os.waitpid(
                -1,  # Wait for any child process
                os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return

        if pid == 0:    # no more zombies
            return
    # pid, status = os.wait()
    # print(
    #     "Child {pid} terminated with status {status}"
    #     "\n".format(pid=pid, status=status)
    # )


def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(
        "Child PID: {pid}. Parent PID {ppid}".format(
            pid=os.getpid(),
            ppid=os.getppid(),
        )
    )
    print(request.decode())
    http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
    client_connection.sendall(http_response)
    time.sleep(3)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print("Serving HTTP on port {port} ...".format(port=PORT))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        try:
            print(1)
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            print(2)
            code, msg = e.args
            # restart "accept" if interrupted
            if code == errno.EINTR:
                continue
            else:
                raise
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)
        else:
            client_connection.close()

if __name__ == "__main__":
    serve_forever()


