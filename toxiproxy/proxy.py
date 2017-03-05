# coding: utf-8

from contextlib import contextmanager

from .api import APIConsumer
from .toxic import Toxic


class Proxy(object):
    """ Represents a Proxy object """

    def __init__(self, **kwargs):

        self.name = kwargs["name"]
        self.upstream = kwargs["upstream"]
        self.enabled = kwargs["enabled"]
        self.listen = kwargs["listen"]

    @contextmanager
    def down(self):
        """ Takes the proxy down while in the context """

        try:
            self.disable()
            yield self
        finally:
            self.enable()

    def toxics(self):
        """ Returns all toxics tied to the proxy """

        toxics = APIConsumer.get("/proxies/%s/toxics" % self.name).json()
        toxics_dict = {}

        for toxic in toxics:
            toxic_name = toxic["name"]
            toxic.update({'proxy': self.name})

            # Add the new toxic to the proxy toxics collection
            toxics_dict.update({toxic_name: Toxic(**toxic)})

        return toxics_dict

    def get_toxic(self, toxic_name):
        """ Retrive a toxic if it exists """

        toxics = self.toxics()
        if toxic_name in toxics:
            return toxics[toxic_name]
        else:
            return None

    def add_toxic(self, **kwargs):
        """ Add a toxic to the proxy """

        toxic_type = kwargs["type"]
        stream = kwargs["stream"] if "stream" in kwargs else "downstream"
        name = kwargs["name"] if "name" in kwargs else "%s_%s" % (toxic_type, stream)
        toxicity = kwargs["toxicity"] if "toxicity" in kwargs else 1.0
        attributes = kwargs["attributes"] if "attributes" in kwargs else {}

        # Lets build a dictionary to send the data to create the Toxic
        json = {
            "name": name,
            "type": toxic_type,
            "stream": stream,
            "toxicity": toxicity,
            "attributes": attributes
        }

        APIConsumer.post("/proxies/%s/toxics" % self.name, json=json).json()

    def destroy_toxic(self, toxic_name):
        """ Destroy the given toxic """

        delete_url = "/proxies/%s/toxics/%s" % (self.name, toxic_name)
        return bool(APIConsumer.delete(delete_url))

    def destroy(self):
        """ Destroy a Toxiproxy proxy """

        return bool(APIConsumer.delete("/proxies/%s" % self.name))

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

        APIConsumer.post("/proxies/%s" % self.name, json=json).json()
        self.enabled = enabled
