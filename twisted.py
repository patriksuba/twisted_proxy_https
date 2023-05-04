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
        # make all content upper case
        proxy.ProxyClient.handleResponsePart(self, buffer.upper())

class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = ProxyClient

class ProxyRequest(proxy.ProxyRequest):
    protocols = dict(http=ProxyClientFactory)

    # Request part
    def process(self):
        log.msg(self.method)
        for k,v in self.requestHeaders.getAllRawHeaders():
            log.msg("%s : %s" % (k,v))
        log.msg("\n \n")

        proxy.ProxyRequest.process(self)

class LoggingProxy(proxy.Proxy):
    requestFactory = ProxyRequest

class LoggingProxyFactory(http.HTTPFactory):
    protocol = LoggingProxy
    
reactor.listenSSL(8000, LoggingProxyFactory(), ssl.DefaultOpenSSLContextFactory('/etc/pki/consumer/key.pem', '/etc/pki/consumer/cert.pem'))
#reactor.listenTCP(8080, LoggingProxyFactory())
reactor.run()