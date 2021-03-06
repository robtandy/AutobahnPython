# Autobahn|Python

[![Build Status](https://travis-ci.org/tavendo/AutobahnPython.png?branch=master)](https://travis-ci.org/tavendo/AutobahnPython)
&nbsp; ![Version](https://pypip.in/v/autobahn/badge.png)
&nbsp; ![Downloads](https://pypip.in/d/autobahn/badge.png)

**Autobahn**|Python is a subproject of [Autobahn](http://autobahn.ws/) and provides open-source implementations of

* **[The WebSocket Protocol](http://tools.ietf.org/html/rfc6455)**
* **[The Web Application Messaging Protocol (WAMP)](http://wamp.ws/)**

in Python running on [**Twisted**](http://twistedmatrix.com/) and [**asyncio**](http://docs.python.org/3.4/library/asyncio.html).

WebSocket allows [bidirectional real-time messaging on the Web](http://tavendo.com/blog/post/websocket-why-what-can-i-use-it/) and WAMP adds asynchronous *Remote Procedure Calls* and *Publish & Subscribe* on top of WebSocket. 

You can use **Autobahn**|Python to create clients and servers in Python speaking just plain WebSocket or WAMP:

* framework for [WebSocket](http://tools.ietf.org/html/rfc6455) / [WAMP](http://wamp.ws/) clients and servers
* compatible with Python 2.6, 2.7, 3.3 and 3.4
* runs on [CPython](http://python.org/), [PyPy](http://pypy.org/) and [Jython](http://jython.org/)
* runs under [Twisted](http://twistedmatrix.com/) and [asyncio](http://docs.python.org/3.4/library/asyncio.html)
* implements WebSocket [RFC6455](http://tools.ietf.org/html/rfc6455), Draft Hybi-10+, Hixie-76
* implements [WebSocket compression](http://tools.ietf.org/html/draft-ietf-hybi-permessage-compression)
* implements [WAMPv1](http://wamp.ws/spec/) and [WAMPv2](https://github.com/tavendo/WAMP/blob/master/spec/README.md) (*upcoming*)
* high-performance, fully asynchronous implementation
* best-in-class standards conformance (100% strict passes with [Autobahn Testsuite](http://autobahn.ws/testsuite))
* message-, frame- and streaming-APIs for WebSocket
* supports TLS (secure WebSocket) and proxies
* Open-source (Apache 2 [license](https://github.com/tavendo/AutobahnPython/blob/master/LICENSE))


## Python support

Support for **Autobahn**|Python on Twisted and asyncio is as follows:

| Python        | Twisted   | asyncio | Notes |
|---------------|-----------|---------|-------|
| CPython 2.6	| yes       | yes     | asyncio support via [trollius](https://pypi.python.org/pypi/trollius/) |
| CPython 2.7	| yes       | yes     | asyncio support via [trollius](https://pypi.python.org/pypi/trollius/) |
| CPython 3.3	| yes       | yes     | asyncio support via [tulip](https://pypi.python.org/pypi/asyncio/) |
| CPython 3.4+	| yes       | yes     | asyncio in the standard library |
| PyPy 2.2+	    | yes       | yes     | asyncio support via [trollius](https://pypi.python.org/pypi/trollius/) |
| Jython 2.7+   | yes       | ?       | Issues: [1](http://twistedmatrix.com/trac/ticket/3413), [2](http://twistedmatrix.com/trac/ticket/6746) |


## Installation

You will need at least one of Twisted or Asyncio as your networking framework.

> Asyncio comes bundled with Python 3.4. For Python 3.3, install it from [here](https://pypi.python.org/pypi/asyncio). For Twisted, please see [here](http://twistedmatrix.com/).

Install from the [Python Package Index](http://pypi.python.org/pypi/autobahn) using [Pip](http://www.pip-installer.org/en/latest/installing.html):

	pip install autobahn

You can also specify install variants

	pip install autobahn[twisted,accelerate]

The latter will automatically install Twisted and native acceleration packages when running on CPython.

	pip install autobahn[asyncio,accelerate]

The latter will automatically install asyncio backports when required and native acceleration packages when running on CPython.

To install from sources, clone the repo

	git clone git@github.com:tavendo/AutobahnPython.git

checkout a tagged release

	cd AutobahnPython
	git checkout v0.7.2

and install

	cd autobahn
	python setup.py install

You can also use Pip for the last step, which allows to specify install variants

	pip install -e .[twisted]

**Autobahn**|Python has the following install variants:

 1. `twisted`: Install Twisted as a dependency
 2. `asyncio`: Install asyncio backports when required
 3. `accelerate`: Install native acceleration packages on CPython
 4. `compress`: Install packages for non-standard WebSocket compression methods
 5. `serialization`: Install packages for additional WAMP serialization formats (currently [MsgPack](http://msgpack.org/))


## Getting Started

The *"Hello, world!"* of WebSocket is probably an echo server:

```python
class MyServerProtocol(WebSocketServerProtocol):

   def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {} bytes".format(len(payload)))
      else:
         print("Text message received: {}".format(payload.decode('utf8')))

      ## echo back message verbatim
      self.sendMessage(payload, isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))
```

Complete examples are here:

 * [WebSocket Echo (Twisted-based)](https://github.com/tavendo/AutobahnPython/tree/master/examples/twisted/websocket/echo)
 * [WebSocket Echo (Asyncio-based)](https://github.com/tavendo/AutobahnPython/tree/master/examples/asyncio/websocket/echo)

Autobahn comes with lots of [examples](https://github.com/tavendo/AutobahnPython/tree/master/examples) with ready-to-run code.

For complete API documentation, please consult the [reference documentation](http://autobahn.ws/python/reference/).

For more information, including some tutorials, please visit the project's [homepage](http://autobahn.ws/python).


## Depending on Autobahn

To require **Autobahn**|Python as a dependency of your package, include the following in your `setup.py`:

	install_requires = ["autobahn>=0.7.2"]

You can also depend on an install variant which automatically installs respective packages:

	install_requires = ["autobahn[twisted,accelerate]>=0.7.2"]


## Upgrading from Autobahn < 0.7.0

Starting with release 0.7.0, **Autobahn**|Python now supports both Twisted and asyncio as the underlying network library. This required changing module naming, e.g.

Autobahn|Python **< 0.7.0**:

     from autobahn.websocket import WebSocketServerProtocol

Autobahn|Python **>= 0.7.0**:

     from autobahn.twisted.websocket import WebSocketServerProtocol

or

     from autobahn.asyncio.websocket import WebSocketServerProtocol 

Two more small changes (also see the [interface definition](https://github.com/tavendo/AutobahnPython/blob/master/autobahn/autobahn/websocket/interfaces.py) now available):

 1. `WebSocketProtocol.sendMessage`: renaming of parameter `binary` to `isBinary` (for consistency with `onMessage`)
 2. `ConnectionRequest` no longer provides `peerstr`, but only `peer`, and the latter is a plain, descriptive string (this was needed since we now support both Twisted and asyncio, and also non-TCP transports)

## Upgrading from Autobahn < 0.8.0

Starting with release 0.8.0, **Autobahn**|Python now supports WAMPv2. This required changing module naming for WAMPv1 (Twisted), e.g.

Autobahn|Python **< 0.8.0**:

     from autobahn.wamp import WampServerFactory

Autobahn|Python **>= 0.8.0**:

     from autobahn.wamp1.protocol import WampServerFactory

> Note that WAMPv1 will be deprecated with the 0.9.0 release.

## Performance

**Autobahn**|Python is portable, well tuned code. You can further accelerate performance by

* Running under [PyPy](http://pypy.org/) or
* on CPython, install the native accelerators [wsaccel](https://pypi.python.org/pypi/wsaccel/) and [ujson](https://pypi.python.org/pypi/ujson/) (you can use the install variant `acceleration` for that)


## Get in touch

Get in touch on IRC `#autobahn` on `chat.freenode.net`, follow us on [Twitter](https://twitter.com/autobahnws) or join the [mailing list](http://groups.google.com/group/autobahnws).
