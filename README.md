[![Circle CI](https://circleci.com/gh/douglas/toxiproxy-python.svg?style=shield)](https://circleci.com/gh/douglas/toxiproxy-python) [![Build Status](https://travis-ci.org/douglas/toxiproxy-python.svg?branch=master)](https://travis-ci.org/douglas/toxiproxy-python) [![Coverage Status](https://coveralls.io/repos/github/douglas/toxiproxy-python/badge.svg?branch=master)](https://coveralls.io/github/douglas/toxiproxy-python?branch=master)

# toxiproxy-python (Work in Progress)

`toxiproxy-python` `0.x` (latest) is compatible with the Toxiproxy `2.x` series.

[Toxiproxy](https://github.com/shopify/toxiproxy) is a proxy to simulate network
and system conditions. The Python API aims to make it simple to write tests that
ensure your application behaves appropriately under harsh conditions. Before you
can use the Python library, you need to read the [Usage section of the Toxiproxy
README](https://github.com/shopify/toxiproxy#usage).

```
pip install git+https://github.com/douglas/toxiproxy-python.git
```

Make sure the Toxiproxy server is already running.

For more information about Toxiproxy and the available toxics, see the [Toxiproxy
documentation](https://github.com/shopify/toxiproxy)

## Usage (what we want to achieve when this library is ready)

The Python client communicates with the Toxiproxy daemon via HTTP. By default it
connects to `http://127.0.0.1:8474`. you can create multiple proxies:

```python
import toxiproxy

server = toxiproxy.Toxiproxy()
# To populate Toxiproxy pass the proxy configurations to
# the populate method. This will create the proxies passed,
# or replace the proxies if they already exist in
# Toxiproxy. It's recommended to do this early as early
# in boot as possible, see the Toxiproxy README. If you
# have many proxies, we recommend storing the Toxiproxy
# configs in a configuration file and deserializing it
# into populate.
proxies = server.populate([{
    "name": "proxy1",
    "listen": f"127.0.0.1:5000",
    "upstream": f"127.0.0.1:50001"
}, {
    "name": "proxy2",
    "listen": f"127.0.0.1:6000",
    "upstream": f"127.0.0.1:60001"
}])
```

For example:
```python
import toxiproxy

server = toxiproxy.Toxiproxy()
proxies = server.populate([{
    "name": "proxy1",
    "listen": f"127.0.0.1:5000",
    "upstream": f"127.0.0.1:50001"
}, {
    "name": "proxy2",
    "listen": f"127.0.0.1:6000",
    "upstream": f"127.0.0.1:60001"
}])

# You can use the latency toxic with the latency argument
proxies[0].add_toxic(name="latency_toxics",
                     type="latency",
                     attributes={
                         "latency": 1000,  # 1000ms
                         "jitter": 0
                     })

# You can also take an endpoint down for the duration of
# a block at the TCP level:
proxies[1].disable()  # down
# do something
proxies[1].enable()  # up

# Remove a toxic
proxies[0].destroy_toxic("latency_toxics")

# Destroy a proxy
proxies[0].destroy()
proxies[1].destroy()
# or destroy all proxies
server.destroy_all()

# Get all proxies
proxies = server.proxies()
# Get a proxy by name
proxy1 = server.get_proxy("proxy1")
```

See the [Toxiproxy README](https://github.com/shopify/toxiproxy#Toxics) for a
list of toxics.
