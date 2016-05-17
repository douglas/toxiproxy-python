from unittest import TestCase
from toxiproxy.api import validate_response
from toxiproxy.exceptions import NotFound, ProxyExists

import requests


class IntoxicatedTest(TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8474"

    def test_not_found(self):
        """ Test an invalid url """

        url_to_test = "%s/%s" % (self.base_url, "not_found")

        with self.assertRaises(NotFound) as context:
            validate_response(requests.get(url_to_test))
            self.assertTrue("404 page not found\n" in context.exception)

    def test_proxy_exists(self):
        """ Test that a proxy already exists """

        url_to_test = "%s/%s" % (self.base_url, "proxies")

        json = {
            "upstream": "localhost:3306",
            "name": "test_mysql_service"
        }

        # Lets create the first proxy
        validate_response(requests.post(url_to_test, json=json))

        with self.assertRaises(ProxyExists) as context:
            # Lets create another one to see it breaks
            validate_response(requests.post(url_to_test, json=json))
            self.assertTrue("proxy already exists" in context.exception)

        # Delete the created proxy
        requests.delete("%s/%s" % (url_to_test, "test_mysql_service"))
