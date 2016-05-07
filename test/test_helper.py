import unittest

from toxiproxy import Toxiproxy


class TestCase(unittest.TestCase):
    def setUp(self):
        self.proxy = Toxiproxy()

    def tearDown(self):
        pass

    def assert_proxy_available(self, proxy):
        pass

    def assert_proxy_unavailable(self, proxy):
        pass

    def connect_to_proxy(self, proxy):
        pass

    def with_tcpserver(self, block, receive=False):
        pass
