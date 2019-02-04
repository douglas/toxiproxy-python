# coding: utf-8

from future.utils import raise_with_traceback, viewitems, listvalues
from .api import APIConsumer
from .proxy import Proxy
from .exceptions import ProxyExists
from .utils import can_connect_to


class Toxiproxy(object):
    """ Represents a Toxiproxy server """

    def proxies(self):
        """ Returns all the proxies registered in the server """

        proxies = APIConsumer.get("/proxies").json()
        proxies_dict = {}

        for name, values in viewitems(proxies):
            # Lets create a Proxy object to hold all its data
            proxy = Proxy(**values)

            # Add the new proxy to the toxiproxy proxies collection
            proxies_dict.update({name: proxy})

        return proxies_dict

    def destroy_all(self):
        proxies = listvalues(self.proxies())
        for proxy in proxies:
            self.destroy(proxy)

    def get_proxy(self, proxy_name):
        """ Retrive a proxy if it exists """

        proxies = self.proxies()
        if proxy_name in proxies:
            return proxies[proxy_name]
        else:
            return None

    def running(self):
        """ Test if the toxiproxy server is running """

        return can_connect_to(APIConsumer.host, APIConsumer.port)

    def version(self):
        """ Get the toxiproxy server version """

        if self.running() is True:
            return APIConsumer.get("/version").content
        else:
            return None

    def reset(self):
        """ Re-enables all proxies and disables all toxics. """

        return bool(APIConsumer.post("/reset"))

    def create(self, upstream, name, listen=None, enabled=None):
        """ Create a toxiproxy proxy """

        if name in self.proxies():
            raise_with_traceback(ProxyExists("This proxy already exists."))

        # Lets build a dictionary to send the data to the Toxiproxy server
        json = {
            "upstream": upstream,
            "name": name
        }

        if listen is not None:
            json["listen"] = listen
        else:
            json["listen"] = "127.0.0.1:0"
        if enabled is not None:
            json["enabled"] = enabled

        proxy_info = APIConsumer.post("/proxies", json=json).json()
        proxy_info["api_consumer"] = APIConsumer

        # Lets create a Proxy object to hold all its data
        proxy = Proxy(**proxy_info)

        return proxy

    def destroy(self, proxy):
        """ Delete a toxiproxy proxy """

        if isinstance(proxy, Proxy):
            return proxy.destroy()
        else:
            return False

    def populate(self, proxies):
        """ Create a list of proxies from an array """

        populated_proxies = []

        for proxy in proxies:
            existing = self.get_proxy(proxy["name"])

            if existing is not None and (existing.upstream != proxy["upstream"] or existing.listen != proxy["listen"]):
                self.destroy(existing)
                existing = None

            if existing is None:
                proxy_instance = self.create(**proxy)
                populated_proxies.append(proxy_instance)

        return populated_proxies


    def update_api_consumer(self, host, port):
        """ Update the APIConsumer host and port """

        APIConsumer.host = host
        APIConsumer.port = port
        APIConsumer.base_url = "http://%s:%s" % (host, port)
