[![Circle CI](https://circleci.com/gh/douglas/toxiproxy-python.svg?style=shield)](https://circleci.com/gh/douglas/toxiproxy-python) [![Build Status](https://travis-ci.org/douglas/toxiproxy-python.svg?branch=master)](https://travis-ci.org/douglas/toxiproxy-python) [![Coverage Status](https://coveralls.io/repos/github/douglas/toxiproxy-python/badge.svg?branch=master)](https://coveralls.io/github/douglas/toxiproxy-python?branch=master) [![Code Health](https://landscape.io/github/douglas/toxiproxy-python/master/landscape.svg?style=flat)](https://landscape.io/github/douglas/toxiproxy-python/master)

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
connects to `http://127.0.0.1:8474`, but you can point to any host:

```
to be ported =(
```

For example, to simulate 1000ms latency on a database server you can use the
`latency` toxic with the `latency` argument (see the Toxiproxy project for a
list of all toxics):

```
to be ported =(
```

You can also take an endpoint down for the duration of a block at the TCP level:

```
to be ported =(
```

If you want to simulate all your Redis instances being down:

```
to be ported =(
```

If you want to simulate that your cache server is slow at incoming network
(upstream), but fast at outgoing (downstream), you can apply a toxic to just the
upstream:

```
to be ported =(
```

By default the toxic is applied to the downstream connection, you can be
explicit and chain them:

```
to be ported =(
```

See the [Toxiproxy README](https://github.com/shopify/toxiproxy#Toxics) for a
list of toxics.

## Populate

To populate Toxiproxy pass the proxy configurations to the `populate` method:

```
to be ported =(
```

This will create the proxies passed, or replace the proxies if they already exist in Toxiproxy.
It's recommended to do this early as early in boot as possible, see the
[Toxiproxy README](https://github.com/shopify/toxiproxy#Usage). If you have many
proxies, we recommend storing the Toxiproxy configs in a configuration file and
deserializing it into `populate`.
