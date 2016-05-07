# coding: utf-8

import unittest
import socket

from contextlib import contextmanager
from toxiproxy import Toxiproxy


class TestCase(unittest.TestCase):
    def setUp(self):
        self.toxiproxy = Toxiproxy()

    def tearDown(self):
        pass

    def assert_proxy_available(self, proxy):
        pass

    def assert_proxy_unavailable(self, proxy):
        pass

    def connect_to_proxy(self, proxy):
        pass


@contextmanager
def tcpserver(receive=False):
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
