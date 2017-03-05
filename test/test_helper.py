import socket
import threading
import socketserver
import time

from contextlib import contextmanager
from builtins import bytes as compat_bytes


class TCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.
    """

    def handle(self):
        data = self.rfile.readline().strip()
        if data:
            self.wfile.write(bytes(b"omgs\n"))


@contextmanager
def tcp_server():
    """ Simple TCPServer to help test Toxiproxy """

    server = socketserver.TCPServer(("127.0.0.1", 0), RequestHandlerClass=TCPRequestHandler)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever)

    try:
        thread.start()
        yield port
    finally:
        server.shutdown()


def connect_to_proxy(host, port):
    """ Connect to a proxy and returns how long the connection lasted """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect((host, int(port)))

    try:
        before = time.time()
        sock.sendall(compat_bytes(b"omg\n"))
        sock.recv(1024)
        passed = time.time() - before
    finally:
        sock.close()

    return passed
