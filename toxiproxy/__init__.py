# coding: utf-8

import socket

from contextlib import closing
from future.utils import raise_with_traceback
from .api import Intoxicated
from .exceptions import ProxyExists


class Proxy(object):
    """ Represents a Proxy object """

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.upstream = kwargs["upstream"]
        self.api_server = kwargs["api_server"]
        self.enabled = kwargs["enabled"]
        self.listen = kwargs["listen"]

    def destroy(self):
        """ Destroy a Toxiproxy proxy """

        return bool(self.api_server.delete("/proxies/%s" % self.name))

    def disable(self):
        """
        Disables a Toxiproxy - this will drop all active connections and
        stop the proxy from listening.
        """

        return self.__enable_proxy(False)

    def enable(self):
        """
        Enables a Toxiproxy - this will cause the proxy to start listening again.
        """

        return self.__enable_proxy(True)

    def __enable_proxy(self, enabled=False):
        """ Enables or Disable a proxy """

        # Lets build a dictionary to send the data to the Toxiproxy server
        json = {
            "enabled": enabled,
        }

        proxy_info = self.api_server.post("/proxies/%s" % self.name, json=json).json()
        self.__update_proxy(**proxy_info)

        return True

    def __update_proxy(self, **proxy_info):
        """ Update proxy information after some action """

        self.__dict__.update(**proxy_info)


class Toxiproxy(object):
    """ Represents a Toxiproxy server """

    def __init__(self, server_host="127.0.0.1", server_port=8474):
        """ Toxiproxy constructor """

        self.api_server = Intoxicated(server_host, server_port)
        self.proxies = {}

    def get_proxy(self, proxy_name):
        """ Retrive a proxy if it exists """

        if proxy_name in self.proxies:
            return self.proxies[proxy_name]
        else:
            return None

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

        if name in self.proxies:
            raise_with_traceback(ProxyExists("This proxy already exists."))

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
        proxy_info["api_server"] = self.api_server

        # Lets create a Proxy object to hold all its data
        proxy = Proxy(**proxy_info)

        # Add the new proxy to the toxiproxy proxies collection
        self.proxies.update({proxy.name: proxy})

        return proxy

    def destroy(self, proxy):
        """ Delete a toxiproxy proxy """

        if proxy.destroy() is True:
            del self.proxies[proxy.name]
            return True
        else:
            return False
