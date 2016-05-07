# coding: utf-8

import socket

from collections import namedtuple
from contextlib import closing
from .api import Intoxicated


class Toxiproxy(object):
    """ Represents a Toxiproxy server """

    def __init__(self, server_host="127.0.0.1", server_port=8474):
        """ Toxiproxy constructor """

        self.api_server = Intoxicated(server_host, server_port)
        self.proxies = []

    def running(self):
        """ Test if the toxiproxy server is running """

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            is_running = True if sock.connect_ex((self.api_server.host, self.api_server.port)) == 0 else False

        return is_running

    def version(self):
        """ Get the toxiproxy server version """

        if self.running() is True:
            return self.api_server.get("/version").content
        else:
            return False

    def reset(self):
        """ Re-enables all proxies and disables all toxics. """

        return bool(self.api_server.post("/reset"))

    def create(self, upstream, name, listen=None, enabled=None):
        """ Create a toxiproxy proxy """

        # Lets build a dictionary to send the data to the Toxiproxy server
        json = {
            "upstream": upstream,
            "name": name
        }

        if listen is not None:
            json["listen"] = listen
        if enabled is not None:
            json["enabled"] = enabled

        proxy_info = self.api_server.post("/proxies", json=json).json()

        # Lets create a Proxy object to hold all its data
        Proxy = namedtuple("Proxy", ["upstream", "name", "listen", "enabled", "toxics"])
        proxy = Proxy(**proxy_info)

        # Add the new proxy to the toxiproxy proxies collection
        self.proxies.append(proxy)

        return proxy

    def destroy(self, proxy):
        """ Destroy a Toxiproxy proxy """

        return bool(self.api_server.delete("/proxies/%s" % proxy.name))
