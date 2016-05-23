from test.test_helper import TestCase
from past.builtins import basestring

from toxiproxy.exceptions import ProxyExists


class ToxiproxyTest(TestCase):
    def test_create_proxy(self):
        """ Test if we can create proxies """

        proxy = self.toxiproxy.create(
            upstream="localhost:3306",
            name="test_mysql_master",
            enabled=False,
            listen="127.0.0.1:43215"
        )

        self.assertEqual(proxy.upstream, "localhost:3306")
        self.assertEqual(proxy.name, "test_mysql_master")
        self.assertFalse(proxy.enabled)
        self.assertEqual(proxy.listen, "127.0.0.1:43215")

        # Destroy this proxy
        proxy.destroy()

    def test_destroy_proxy(self):
        """ Test if we can destroy proxies """

        proxy = self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
        self.toxiproxy.destroy(proxy)

        self.assertNotIn(proxy, self.toxiproxy.proxies)

    def test_destroy_invalid_proxy(self):
        """ Test if we can destroy an invalid proxy """

        result = self.toxiproxy.destroy("invalid_proxy")
        self.assertFalse(result)

    def test_disable_proxy(self):
        """ Test if we can disable proxies """

        proxy = self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
        proxy.disable()

        self.assertEqual(proxy.enabled, False)
        proxy.destroy()

    def test_enable_proxy(self):
        """ Test if we can enable a proxy """

        proxy = self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
        proxy.disable()
        proxy.enable()

        self.assertEqual(proxy.enabled, True)
        proxy.destroy()

    def test_find_invalid_proxy(self):
        """ Test if that we cant fetch an invalid proxy """

        proxy = self.toxiproxy.get_proxy("invalid_proxy")
        self.assertEqual(proxy, None)

    def test_create_and_find_proxy(self):
        """ Test if we can create a proxy and retrieve it """

        self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")

        proxy = self.toxiproxy.get_proxy("test_mysql_master")

        self.assertEqual(proxy.upstream, "localhost:3306")
        self.assertEqual(proxy.name, "test_mysql_master")

        self.toxiproxy.destroy(proxy)

    def test_cant_create_proxies_same_name(self):
        """ Test that we can't create proxies with the same name """

        proxy = self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")

        with self.assertRaises(ProxyExists) as context:
            self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
            self.assertTrue("This proxy already exists." in context.exception)

        self.toxiproxy.destroy(proxy)

    def test_version_of_invalid_toxiproxy(self):
        """ Test that we cant fetch the version of an invalid toxiproxy server """

        self.toxiproxy.api_server.host = "0.0.0.0"
        self.toxiproxy.api_server.port = 12345
        self.assertEqual(self.toxiproxy.version(), None)

        self.toxiproxy.api_server.host = "127.0.0.1"
        self.toxiproxy.api_server.port = 8474

    def test_enable_and_disable_proxy_with_toxic(self):
        pass

    def test_delete_toxic(self):
        pass

    def test_reset(self):
        pass

    def test_take_endpoint_down(self):
        pass

    def test_raises_when_proxy_doesnt_exist(self):
        pass

    def test_proxies_all_returns_proxy_collection(self):
        pass

    def test_down_on_proxy_collection_disables_entire_collection(self):
        pass

    def test_disable_on_proxy_collection(self):
        pass

    def test_select_from_toxiproxy_collection(self):
        pass

    def test_grep_returns_toxiproxy_collection(self):
        pass

    def test_indexing_allows_regexp(self):
        pass

    def test_apply_upstream_toxic(self):
        pass

    def test_apply_downstream_toxic(self):
        pass

    def test_toxic_applies_a_downstream_toxic(self):
        pass

    def test_toxic_default_name_is_type_and_stream(self):
        pass

    def test_apply_prolong_toxics(self):
        pass

    def test_apply_toxics_to_collection(self):
        pass

    def test_populate_creates_proxies_array(self):
        """ Test that we can create proxies from an array of proxies """

        proxies = [
            {
                "name": "test_toxiproxy_populate1",
                "upstream": "localhost:3306",
                "listen": "localhost:22222"
            },
            {
                "name": "test_toxiproxy_populate2",
                "upstream": "localhost:3306",
                "listen": "localhost:22223",
            },
        ]

        proxies = self.toxiproxy.populate(proxies)

        for proxy in proxies:
            self.assert_proxy_available(proxy)

    def test_populate_creates_proxies_args(self):
        pass

    def test_populate_creates_proxies_update_listen(self):
        pass

    def test_populate_creates_proxies_update_upstream(self):
        pass

    def test_running_helper(self):
        """ Test if the wrapper can connect with a valid toxiproxy server """

        self.assertTrue(self.toxiproxy.running())

    def test_version(self):
        """ Test if the version is an instance of a string type """

        self.assertIsInstance(self.toxiproxy.version(), basestring)

    def test_multiple_of_same_toxic_type(self):
        pass

    def test_multiple_of_same_toxic_type_with_same_name(self):
        pass

    def test_invalid_direction(self):
        pass
