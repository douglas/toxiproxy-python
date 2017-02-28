from past.builtins import basestring

import pytest

from toxiproxy.exceptions import ProxyExists
from toxiproxy import Toxiproxy
from toxiproxy.utils import can_connect_to

from .test_utils import tcp_server


# The toxiproxy server we will use for the tests
toxiproxy = Toxiproxy()


def teardown_function(function):
    """ Lets cler all the created proxies during the tests """

    toxiproxy.destroy_all()


def test_create_proxy():
    """ Test if we can create proxies """

    proxy = toxiproxy.create(
        upstream="localhost:3306",
        name="test_mysql_master",
        enabled=False,
        listen="127.0.0.1:43215"
    )

    assert proxy.upstream == "localhost:3306"
    assert proxy.name == "test_mysql_master"
    assert proxy.enabled is False
    assert proxy.listen == "127.0.0.1:43215"


def test_destroy_proxy():
    """ Test if we can destroy proxies """

    proxy = toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
    toxiproxy.destroy("test_mysql_master")
    assert proxy not in toxiproxy.proxies()


def test_destroy_invalid_proxy():
    """ Test if we can destroy an invalid proxy """

    result = toxiproxy.destroy("invalid_proxy")
    assert result is False


def test_disable_proxy():
    """ Test if we can disable proxies """

    proxy = toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
    proxy.disable()

    assert proxy.enabled is False


def test_enable_proxy():
    """ Test if we can enable a proxy """

    proxy = toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
    proxy.disable()
    proxy.enable()

    assert proxy.enabled is True


def test_find_invalid_proxy():
    """ Test if that we cant fetch an invalid proxy """

    proxy = toxiproxy.get_proxy("invalid_proxy")
    assert proxy is None


def test_create_and_find_proxy():
    """ Test if we can create a proxy and retrieve it """

    toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
    proxy = toxiproxy.get_proxy("test_mysql_master")

    assert proxy.upstream == "localhost:3306"
    assert proxy.name == "test_mysql_master"


def test_cant_create_proxies_same_name():
    """ Test that we can't create proxies with the same name """

    toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")

    with pytest.raises(ProxyExists) as context:
        toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
        assert "This proxy already exists." in context.exception


def test_version_of_invalid_toxiproxy():
    """ Test that we cant fetch the version of an invalid toxiproxy server """

    toxiproxy.update_api_consumer("0.0.0.0", 12345)
    assert toxiproxy.version() is None

    # Restoring the defaults
    toxiproxy.update_api_consumer("127.0.0.1", 8474)


def test_proxy_not_running_with_bad_host():
    toxiproxy.update_api_consumer("0.0.0.0", 12345)
    assert toxiproxy.running() is False

    # Restoring the defaults
    toxiproxy.update_api_consumer("127.0.0.1", 8474)


def test_populate_creates_proxies_array():
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

    proxies = toxiproxy.populate(proxies)

    for proxy in proxies:
        host, port = proxy.listen.split(":")
        assert can_connect_to(host, int(port)) is True


def test_running_helper():
    """ Test if the wrapper can connect with a valid toxiproxy server """

    assert toxiproxy.running() is True


def test_version():
    """ Test if the version is an instance of a string type """

    assert isinstance(toxiproxy.version(), basestring)


def test_enable_and_disable_proxy_with_toxic():
    """ Test if we can enable and disable a proxy with toxic """

    with tcp_server() as server:
        port = server.server_address[1]

        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")
        listen_addr = proxy.listen

        proxy.add_toxic(type="latency", attributes={"latency": 123})

        proxy.disable()
        assert proxy.enabled is False

        proxy.enable()
        assert proxy.enabled is True

        latency_toxic = proxy.get_toxic("latency_downstream")
        assert latency_toxic.attributes['latency'] == 123

        assert listen_addr == proxy.listen


#     def test_delete_toxic(self):
#         pass

#     def test_reset(self):
#         pass

#     def test_take_endpoint_down(self):
#         pass

#     def test_raises_when_proxy_doesnt_exist(self):
#         pass

#     def test_proxies_all_returns_proxy_collection(self):
#         pass

#     def test_down_on_proxy_collection_disables_entire_collection(self):
#         pass

#     def test_disable_on_proxy_collection(self):
#         pass

#     def test_select_from_toxiproxy_collection(self):
#         pass

#     def test_grep_returns_toxiproxy_collection(self):
#         pass

#     def test_indexing_allows_regexp(self):
#         pass

#     def test_apply_upstream_toxic(self):
#         pass

#     def test_apply_downstream_toxic(self):
#         pass

#     def test_toxic_applies_a_downstream_toxic(self):
#         pass

#     def test_toxic_default_name_is_type_and_stream(self):
#         pass

#     def test_apply_prolong_toxics(self):
#         pass

#     def test_apply_toxics_to_collection(self):
#         pass

def test_populate_creates_proxies_update_listen():
    """ Create proxies and tests if they are available """

    proxies = [{
        "name": "test_toxiproxy_populate1",
        "upstream": "localhost:3306",
        "listen": "localhost:22222",
    }]

    proxies = toxiproxy.populate(proxies)

    proxies = [{
        "name": "test_toxiproxy_populate1",
        "upstream": "localhost:3306",
        "listen": "localhost:22223",
    }]

    proxies = toxiproxy.populate(proxies)

    for proxy in proxies:
        host, port = proxy.listen.split(":")
        assert can_connect_to(host, int(port)) is True

#     def test_populate_creates_proxies_update_upstream(self):
#         pass

#     def test_multiple_of_same_toxic_type(self):
#         pass

#     def test_multiple_of_same_toxic_type_with_same_name(self):
#         pass

#     def test_invalid_direction(self):
#         pass
