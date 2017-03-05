# coding: utf-8

import pytest

from past.builtins import basestring

from toxiproxy.exceptions import ProxyExists, InvalidToxic
from toxiproxy import Toxiproxy
from toxiproxy.utils import can_connect_to

from .test_helper import tcp_server, connect_to_proxy

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

    with pytest.raises(ProxyExists) as excinfo:
        toxiproxy.create(upstream="localhost:3306", name="test_mysql_master")
    assert excinfo.typename == "ProxyExists"


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

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")
        proxy_host, proxy_port = proxy.listen.split(":")
        listen_addr = proxy.listen

        proxy.add_toxic(type="latency", attributes={"latency": 123})

        proxy.disable()
        assert can_connect_to(proxy_host, int(proxy_port)) is False

        proxy.enable()
        assert can_connect_to(proxy_host, int(proxy_port)) is True

        latency_toxic = proxy.get_toxic("latency_downstream")
        assert latency_toxic.attributes['latency'] == 123

        assert listen_addr == proxy.listen


def test_delete_toxic():
    """ Test if we can delete a toxic """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")
        proxy_host, proxy_port = proxy.listen.split(":")
        listen_addr = proxy.listen

        proxy.add_toxic(type="latency", attributes={"latency": 123})

        assert can_connect_to(proxy_host, int(proxy_port)) is True

        latency_toxic = proxy.get_toxic("latency_downstream")
        assert latency_toxic.attributes['latency'] == 123

        proxy.destroy_toxic("latency_downstream")
        assert proxy.toxics() == {}

        assert listen_addr == proxy.listen


def test_reset():
    """ Test the reset Toxiproxy feature """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")
        proxy_host, proxy_port = proxy.listen.split(":")
        listen_addr = proxy.listen

        proxy.disable()
        assert can_connect_to(proxy_host, int(proxy_port)) is False

        proxy.add_toxic(type="latency", attributes={"latency": 123})

        toxiproxy.reset()
        assert can_connect_to(proxy_host, int(proxy_port)) is True
        assert proxy.toxics() == {}
        assert listen_addr == proxy.listen


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


def test_apply_upstream_toxic():
    """ Test that is possible to create upstream toxics """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_proxy")
        proxy_host, proxy_port = proxy.listen.split(":")
        proxy.add_toxic(stream="upstream", type="latency", attributes={"latency": 100})

        passed = connect_to_proxy(proxy_host, proxy_port)
        assert passed, pytest.approx(0.100, 0.01)


def test_apply_downstream_toxic():
    """ Test that is possible to create downstream toxics """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_proxy")
        proxy_host, proxy_port = proxy.listen.split(":")
        proxy.add_toxic(type="latency", attributes={"latency": 100})

        passed = connect_to_proxy(proxy_host, proxy_port)
        assert passed, pytest.approx(0.100, 0.01)


def test_invalid_direction():
    """ Test that is not possible to create toxics with invalid direction """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")

        with pytest.raises(InvalidToxic) as excinfo:
            proxy.add_toxic(type="latency", attributes={"latency": 123}, stream="lolstream")
        assert excinfo.typename == "InvalidToxic"


def test_multiple_of_same_toxic_type():
    """ Test that is possible to create various toxics with the same type """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_proxy")
        proxy_host, proxy_port = proxy.listen.split(":")
        proxy.add_toxic(type="latency", attributes={"latency": 100})
        proxy.add_toxic(type="latency", attributes={"latency": 100}, name="second_latency_downstream")

        passed = connect_to_proxy(proxy_host, proxy_port)
        assert passed, pytest.approx(0.200, 0.01)


def test_take_endpoint_down():
    """ Test that is possible to take the endpoint down inside a context """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_rubby_server")
        proxy_host, proxy_port = proxy.listen.split(":")
        listen_addr = proxy.listen

        with proxy.down():
            assert can_connect_to(proxy_host, int(proxy_port)) is False

        assert can_connect_to(proxy_host, int(proxy_port)) is True
        assert listen_addr == proxy.listen


def test_apply_prolong_toxics():
    """ Test that is possible to prolong toxics """

    with tcp_server() as port:
        proxy = toxiproxy.create(upstream="localhost:%s" % port, name="test_proxy")
        proxy_host, proxy_port = proxy.listen.split(":")
        proxy.add_toxic(stream="upstream", type="latency", attributes={"latency": 100})
        proxy.add_toxic(type="latency", attributes={"latency": 100})

        passed = connect_to_proxy(proxy_host, proxy_port)
        assert passed, pytest.approx(0.200, 0.01)

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

#     def test_toxic_applies_a_downstream_toxic(self):
#         pass

#     def test_toxic_default_name_is_type_and_stream(self):
#         pass

#     def test_apply_prolong_toxics(self):
#         pass

#     def test_apply_toxics_to_collection(self):
#         pass

#     def test_populate_creates_proxies_update_upstream(self):
#         pass

#     def test_multiple_of_same_toxic_type_with_same_name(self):
#         pass
