# XMLRPC-specific code for SFA Client

import xmlrpclib

##
# ServerException, ExceptionUnmarshaller
#
# Used to convert server exception strings back to an exception.
#    from usenet, Raghuram Devarakonda

class ServerException(Exception):
    pass

class ExceptionUnmarshaller(xmlrpclib.Unmarshaller):
    def close(self):
        try:
            return xmlrpclib.Unmarshaller.close(self)
        except xmlrpclib.Fault, e:
            raise ServerException(e.faultString)

##
# XMLRPCTransport
#
# A transport for XMLRPC that works on top of HTTPS

class XMLRPCTransport(xmlrpclib.Transport):
    key_file = None
    cert_file = None
    def make_connection(self, host):
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        import httplib
        host, extra_headers, x509 = self.get_host_info(host)
        try:
            HTTPS = httplib.HTTPS()
        except AttributeError:
            raise NotImplementedError(
                "your version of httplib doesn't support HTTPS"
                )
        else:
            return httplib.HTTPS(host, None, key_file=self.key_file, cert_file=self.cert_file) #**(x509 or {}))

    def getparser(self):
        unmarshaller = ExceptionUnmarshaller()
        parser = xmlrpclib.ExpatParser(unmarshaller)
        return parser, unmarshaller

class XMLRPCServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, url, transport, allow_none=True, options=None):
        self.options = options
        verbose = False
        if self.options and self.options.debug:
            verbose = True
        xmlrpclib.ServerProxy.__init__(self, url, transport, allow_none=allow_none, verbose=verbose)

    def __getattr__(self, attr):
        if self.options.verbose:
            print "Calling xml-rpc method:", attr
        return xmlrpclib.ServerProxy.__getattr__(self, attr)


def get_server(url, key_file, cert_file, options=None):
    transport = XMLRPCTransport()
    transport.key_file = key_file
    transport.cert_file = cert_file

    return XMLRPCServerProxy(url, transport, allow_none=True, options=options)

