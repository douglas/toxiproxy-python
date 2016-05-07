from test.test_helper import TestCase
from past.builtins import basestring


class ToxiproxyTest(TestCase):
    def test_create_proxy(self):
        """ Test if we can create proxies """

        proxy = self.toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")

        self.assertEqual(proxy.upstream, "localhost:3306")
        self.assertEqual(proxy.name, "test_mysql_master")

        # Destroy this proxy
        self.toxiproxy.destroy(proxy)

    def test_create_and_find_proxy(self):
        pass

    def test_proxy_not_running_with_bad_host(self):
        """ Test if the wrapper can't connect with an invalid toxiproxy server """

        self.toxiproxy.api_server.host = "0.0.0.0"
        self.toxiproxy.api_server.port = 12345
        self.assertFalse(self.toxiproxy.running())

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
        pass

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
