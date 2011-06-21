# XMLRPC-specific code for SFA Client

import httplib
import xmlrpclib

from sfa.util.sfalogging import logger
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

# python 2.7 xmlrpclib has changed its internal code
# it now calls 'getresponse' on the obj returned by make_connection
# while it used to call 'getreply'
# regardless of the version, httplib.HTTPS does implement getreply, 
# while httplib.HTTPSConnection has getresponse
# so we create a dummy instance to check what's expected
need_HTTPSConnection=hasattr(xmlrpclib.Transport().make_connection('localhost'),'getresponse')

class XMLRPCTransport(xmlrpclib.Transport):
    key_file = None
    cert_file = None
    def make_connection(self, host):
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        host, extra_headers, x509 = self.get_host_info(host)
        if need_HTTPSConnection:
            return httplib.HTTPSConnection(host, None, key_file=self.key_file, cert_file=self.cert_file) #**(x509 or {}))
        else:
            return httplib.HTTPS(host, None, key_file=self.key_file, cert_file=self.cert_file) #**(x509 or {}))

    def getparser(self):
        unmarshaller = ExceptionUnmarshaller()
        parser = xmlrpclib.ExpatParser(unmarshaller)
        return parser, unmarshaller

class XMLRPCServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, url, transport, allow_none=True, options=None):
        # remember url for GetVersion
        self.url=url
        verbose = False
        if options and options.debug:
            verbose = True
        xmlrpclib.ServerProxy.__init__(self, url, transport, allow_none=allow_none, verbose=verbose)

    def __getattr__(self, attr):
        logger.debug ("xml-rpc %s method:%s"%(self.url,attr))
        return xmlrpclib.ServerProxy.__getattr__(self, attr)


def get_server(url, key_file, cert_file, options=None):
    transport = XMLRPCTransport()
    transport.key_file = key_file
    transport.cert_file = cert_file

    return XMLRPCServerProxy(url, transport, allow_none=True, options=options)

