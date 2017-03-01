# coding: utf-8


class Toxic(object):
    """ Represents a Proxy object """

    def __init__(self, **kwargs):
        """ Initializing the Toxic object """

        self.type = kwargs["type"]
        self.stream = kwargs["stream"] if "stream" in kwargs else "downstream"
        self.name = kwargs["name"] if "name" in kwargs else "%s_%s" % (self.type, self.stream)
        self.toxicity = kwargs["toxicity"] if "toxicity" in kwargs else 1.0
        self.attributes = kwargs["attributes"] if "attributes" in kwargs else {}
