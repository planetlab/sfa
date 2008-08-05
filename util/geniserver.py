# geniserver.py
#
# geniwrapper server
#
# implements a general-purpose server layer for geni. This should be usable on
# the registry, component, or other interfaces.
#
# TODO: investigate ways to combine this with existing PLC server?

import SimpleXMLRPCServer

import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import SimpleXMLRPCServer

from excep import *
from cert import *
from credential import *

import socket, os
from OpenSSL import SSL

# verify_callback
#
# verification callback for pyOpenSSL. We do our own checking of keys because
# we have our own authentication spec. Thus we disable several of the normal
# prohibitions that OpenSSL places on certificates

def verify_callback(conn, x509, err, depth, preverify):
    # if the cert has been preverified, then it is ok
    if preverify:
       #print "  preverified"
       return 1

    # we're only passing single certificates, not chains
    if depth > 0:
       #print "  depth > 0 in verify_callback"
       return 0

    # create a Certificate object and load it from the client's x509
    ctx = conn.get_context()
    server = ctx.get_app_data()
    server.peer_cert = Certificate()
    server.peer_cert.load_from_pyopenssl_x509(x509)

    # the certificate verification done by openssl checks a number of things
    # that we aren't interested in, so we look out for those error messages
    # and ignore them

    # allow self-signed certificates
    if err == 18:
       #print "  X509_V_ERR_DEPTH_ZERO_SELF_SIGNED_CERT"
       return 1

    # allow certs that don't have an issuer
    if err == 20:
       #print "  X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY"
       return 1

    # allow certs that are untrusted
    if err == 21:
       #print "  X509_V_ERR_UNABLE_TO_VERIFY_LEAF_SIGNATURE"
       return 1

    # allow certs that are untrusted
    if err == 27:
       #print "  X509_V_ERR_CERT_UNTRUSTED"
       return 1

    print "  error", err, "in verify_callback"

    return 0

# SecureXMLServer
#
# taken from the web (XXX find reference). Implements an HTTPS xmlrpc server

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, key_file, cert_file, logRequests=True):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
        """
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, None, None)
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file(key_file)
        ctx.use_certificate_file(cert_file)
        ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_callback)
        ctx.set_app_data(self)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                        self.socket_type))
        self.server_bind()
        self.server_activate()

# SecureXMLRpcRequestHandler
#
# taken from the web (XXX find reference). Implents HTTPS xmlrpc request handler

class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Secure XML-RPC request handler class.

    It it very similar to SimpleXMLRPCRequestHandler but it uses HTTPS for transporting XML data.
    """
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_POST(self):
        """Handles the HTTPS POST request.

        It was copied out from SimpleXMLRPCServer.py and modified to shutdown the socket cleanly.
        """

        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown() # Modified here!

# GeniServer
#
# Class for a general purpose geni server.
#
# Implements an HTTPS XML-RPC server. Generally it is expected that GENI
# functions will take a credential string, which is passed to
# decode_authentication. Decode_authentication() will verify the validity of
# the credential, and verify that the user is using the key that matches the
# GID supplied in the credential.

class GeniServer():
    def __init__(self, ip, port, key_file, cert_file):
        self.key = Keypair(filename = key_file)
        self.cert = Certificate(filename = cert_file)
        self.server = SecureXMLRPCServer((ip, port), SecureXMLRpcRequestHandler, key_file, cert_file)
        self.register_functions()

    def decode_authentication(self, cred_string):
        self.client_cred = Credential(string = cred_string)
        self.client_gid = self.client_cred.get_gid_caller()

        # make sure the client_gid is not blank
        if not self.client_gid:
            raise MissingCallerGID(self.client_cred.get_subject())

        # make sure the client_gid matches the certificate that the client is using
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(self.client_gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(self.client_gid.get_subject())

    # register_functions override this to add more functions
    def register_functions(self):
        self.server.register_function(self.noop)

    def noop(self, cred, anything):
        self.decode_authentication(cred)

        return anything

    def run(self):
        self.server.serve_forever()


