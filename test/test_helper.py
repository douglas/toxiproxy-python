# coding: utf-8

import socket
from contextlib import contextmanager

@contextmanager
def tcpserver():
    """ Create a simple TCPServer to allows us to test our wrapper """

    # Create a TCP/IP socket and bind it
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 0)
    server.bind(server_address)
    server.listen(1)

    try:
        yield server
    finally:
        server.close()


#   def assert_proxy_unavailable(proxy)
#     assert_raises Errno::ECONNREFUSED do
#       connect_to_proxy proxy
#     end
#   end

