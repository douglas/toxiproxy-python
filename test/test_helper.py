import socket
import threading
import socketserver

from contextlib import closing, contextmanager
from builtins import bytes


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print("%s wrote: %s" % (self.client_address[0], self.data))
        if self.data == bytes(b"omg"):
            self.request.sendall(bytes(b"omgs"))


@contextmanager
def tcp_server():
    server = socketserver.TCPServer(("127.0.0.1", 0), RequestHandlerClass=TCPHandler)

    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
    thread.daemon = True

    try:
        thread.start()
        yield server
    finally:
        server.shutdown()


def connect_to_proxy(proxy):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        host, port = proxy.listen.split(":")
        sock.connect((host, int(port)))
        sock.sendall(bytes(b"omg"))
        response = sock.recv(1024)
        #print("Received: {}".format(response))
