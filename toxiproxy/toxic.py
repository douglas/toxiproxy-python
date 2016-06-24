# coding: utf-8


class Toxic(object):
    """ Represents a Toxic object """

    def __init__(self, **kwargs):
        self.type = kwargs["type"]
        self.stream = kwargs["stream"] if "stream" in kwargs else "downstream"
        self.name = kwargs["name"] if "name" in kwargs else "%s_%s" % (self.type, self.stream)
        self.proxy = kwargs["proxy"]
        self.toxicity = kwargs["toxicity"] if "toxicity" in kwargs else 1.0
        self.attributes = kwargs["attributes"] if "attributes" in kwargs else {}
        self.api_server = kwargs["api_server"]

    def destroy(self):
        """ Destroy this toxic """

        delete_url = "/proxies/%s/toxics/%s" % (self.proxy.name, self.name)
        return bool(self.api_server.delete(delete_url))

    def save(self):
        """ Saves this toxic """

        # Lets build a dictionary to send the data to create the Toxic
        json = {
            "name": self.name,
            "type": self.type,
            "stream": self.stream,
            "toxicity": self.toxicity,
            "attributes": self.attributes,
        }

        self.api_server.post("/proxies/%s/toxics" % self.proxy.name, json=json).json()

        return True
