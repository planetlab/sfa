# XMLRPC-specific code for SFA Client

import xmlrpclib

from sfa.util.sfalogging import sfa_logger

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
            HTTPS = httplib.HTTPSConnection()
        except AttributeError:
            raise NotImplementedError(
                "your version of httplib doesn't support HTTPS"
                )
        else:
            return httplib.HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file) #**(x509 or {}))

    def getparser(self):
        unmarshaller = ExceptionUnmarshaller()
        parser = xmlrpclib.ExpatParser(unmarshaller)
        return parser, unmarshaller

class XMLRPCServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, url, transport, allow_none=True, options=None):
        verbose = False
        if options and options.debug:
            verbose = True
        sfa_logger().info ("Connecting to xmlrpcserver at %s (with verbose=%s)"%(url,verbose))
        xmlrpclib.ServerProxy.__init__(self, url, transport, allow_none=allow_none, verbose=verbose)

    def __getattr__(self, attr):
        sfa_logger().info ("Calling xml-rpc method:%s"%attr)
        return xmlrpclib.ServerProxy.__getattr__(self, attr)


def get_server(url, key_file, cert_file, options=None):
    transport = XMLRPCTransport()
    transport.key_file = key_file
    transport.cert_file = cert_file

    return XMLRPCServerProxy(url, transport, allow_none=True, options=options)

