# coding: utf-8

import requests

from future.utils import raise_with_traceback
from .exceptions import ProxyExists, NotFound, InvalidToxic


class APIConsumer(object):
    """ Toxiproxy API Consumer """

    host = "127.0.0.1"
    port = 8474
    base_url = "http://%s:%s" % (host, port)

    @classmethod
    def get(cls, url, params=None, **kwargs):
        """ Use the GET method to fetch data from the API """

        endpoint = cls.base_url + url
        return validate_response(requests.get(url=endpoint, params=params, **kwargs))

    @classmethod
    def delete(cls, url, **kwargs):
        """ Use the DELETE method to delete data from the API """

        endpoint = cls.base_url + url
        return validate_response(requests.delete(url=endpoint, **kwargs))

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        """ Use the POST method to post data to the API """

        endpoint = cls.base_url + url
        return validate_response(requests.post(url=endpoint, data=data, json=json, **kwargs))


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

    return response
