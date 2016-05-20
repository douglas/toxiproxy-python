# coding: utf-8


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
