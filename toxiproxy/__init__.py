# coding: utf-8

import socket

from contextlib import closing
from .api import Intoxicated


class Toxiproxy(object):
    """ Represents a Toxiproxy server """

    def __init__(self, host="127.0.0.1", port=8474):
        """ Toxiproxy constructor """

        self.host = host
        self.port = port
        self.api = Intoxicated(host, port)

    def running(self):
        """ Test if the toxiproxy server is running """

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            is_running = True if sock.connect_ex((self.host, self.port)) == 0 else False

        return is_running

    def version(self):
        if self.running() is True:
            return self.api.get("/version")
        else:
            return False
