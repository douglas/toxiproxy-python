# coding: utf-8

import requests

from future.utils import raise_with_traceback
from .exceptions import ProxyExists, NotFound, InvalidToxic


class Intoxicated(object):
    """ Toxiproxy API Consumer """

    def __init__(self, host, port):
        """ """

        self.base_url = "http://%s:%s" % (host, port)

    def get(self, url):
        """ Use the GET method to fetch data from the API """

        endpoint = self.base_url + url
        return validate_response(requests.get(endpoint))


def validate_response(response):
    """
    Handle the received response to make sure that we
    will only process valid requests.
    """

    content = response.content

    if response.status_code == 409:
        raise_with_traceback(ProxyExists(content))
    elif response.status_code == 404:
        raise_with_traceback(NotFound(content))
    elif response.status_code == 400:
        raise_with_traceback(InvalidToxic(content))
    return content
