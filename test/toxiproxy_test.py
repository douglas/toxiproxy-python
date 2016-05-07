from test.test_helper import TestCase
from past.builtins import basestring


class ToxiproxyTest(TestCase):
    def test_create_proxy(self):
        pass

    def test_create_and_find_proxy(self):
        pass

    def test_proxy_not_running_with_bad_host(self):
        pass

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
        """ Test if the helper is running """

        self.assertTrue(self.proxy.running())

    def test_version(self):
        """ Test if the version is an instance of a string type """

        self.assertIsInstance(self.proxy.version(), basestring)

    def test_multiple_of_same_toxic_type(self):
        pass

    def test_multiple_of_same_toxic_type_with_same_name(self):
        pass

    def test_invalid_direction(self):
        pass
