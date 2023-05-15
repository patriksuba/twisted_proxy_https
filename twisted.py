import sys

from twisted.web import http, proxy
from twisted.internet import reactor, ssl
from twisted.python import log


class ProxyClient(proxy.ProxyRequest):
	def handleHeader(self, key, value):
		# change response header here
		log.msg("Header: %s: %s" % (key, value))

		proxy.ProxyClient.handleHeader(self, key, value)

	def handleResponsePart(self, buffer):
		# change response part here
		log.msg("Content: %s" % (buffer[:50],))

		proxy.ProxyClient.handleResponsePart(self, buffer)

class ProxyClientFactory(proxy.ProxyClientFactory):
	protocol = ProxyClient

class ProxyRequest(proxy.ProxyRequest):
	protocols = dict(http=ProxyClientFactory)

	def connect(self):
		log.msg(self.uri)
		host, port = self.uri.decode("utf-8").split(":")
		proxy.ProxyRequest.process(self)


	# Request part
	def process(self):
		if self.method == b"CONNECT":
			self.connect()
		else:
			log.msg(self.method)
			for k,v in self.requestHeaders.getAllRawHeaders():
				log.msg("%s : %s" % (k,v))
			log.msg("\n \n")

			proxy.ProxyRequest.process(self)

class LoggingProxy(proxy.Proxy):
	requestFactory = ProxyRequest

class LoggingProxyFactory(http.HTTPFactory):
	protocol = LoggingProxy

log.startLogging(sys.stdout)
#reactor.listenSSL(8000, LoggingProxyFactory(), ssl.DefaultOpenSSLContextFactory('/etc/pki/consumer/key.pem', '/etc/pki/consumer/cert.pem'))
reactor.listenTCP(8000, LoggingProxyFactory())
reactor.run()