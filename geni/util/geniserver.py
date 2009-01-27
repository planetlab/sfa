##
# This module implements a general-purpose server layer for geni.
# The same basic server should be usable on the registry, component, or
# other interfaces.
#
# TODO: investigate ways to combine this with existing PLC server?
##

import SimpleXMLRPCServer

import sys
import traceback
import threading
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import SimpleXMLRPCServer

from excep import *
from cert import *
from credential import *

import socket, os
from OpenSSL import SSL

##
# Verification callback for pyOpenSSL. We do our own checking of keys because
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

    # XXX SMBAKER: I don't know what this error is, but it's being returned
    # by newer pl nodes.
    if err == 9:
       #print "  X509_V_ERR_CERT_NOT_YET_VALID"
       return 1

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

##
# Taken from the web (XXX find reference). Implements an HTTPS xmlrpc server

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, key_file, cert_file, logRequests=True):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
        """
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, True, None)
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

    # _dispatch
    #
    # Convert an exception on the server to a full stack trace and send it to
    # the client.

    def _dispatch(self, method, params):
        try:
            return SimpleXMLRPCServer.SimpleXMLRPCDispatcher._dispatch(self, method, params)
        except:
            # can't use format_exc() as it is not available in jython yet
            # (evein in trunk).
            type, value, tb = sys.exc_info()
            raise xmlrpclib.Fault(1,''.join(traceback.format_exception(type, value, tb)))

##
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

##
# Implements an HTTPS XML-RPC server. Generally it is expected that GENI
# functions will take a credential string, which is passed to
# decode_authentication. Decode_authentication() will verify the validity of
# the credential, and verify that the user is using the key that matches the
# GID supplied in the credential.

class GeniServer(threading.Thread):

    ##
    # Create a new GeniServer object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key 
    #   (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        threading.Thread.__init__(self)
        self.key = Keypair(filename = key_file)
        self.cert = Certificate(filename = cert_file)
        self.server = SecureXMLRPCServer((ip, port), SecureXMLRpcRequestHandler, key_file, cert_file)
        self.trusted_cert_list = None
        self.register_functions()

    ##
    # Decode the credential string that was submitted by the caller. Several
    # checks are performed to ensure that the credential is valid, and that the
    # callerGID included in the credential matches the caller that is
    # connected to the HTTPS connection.

    def decode_authentication(self, cred_string, operation):
        self.client_cred = Credential(string = cred_string)
        self.client_gid = self.client_cred.get_gid_caller()
        self.object_gid = self.client_cred.get_gid_object()

        # make sure the client_gid is not blank
        if not self.client_gid:
            raise MissingCallerGID(self.client_cred.get_subject())

        # make sure the client_gid matches client's certificate
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(self.client_gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(self.client_gid.get_subject())

        # make sure the client is allowed to perform the operation
        if operation:
            if not self.client_cred.can_perform(operation):
                raise InsufficientRights(operation)

        if self.trusted_cert_list:
            self.client_cred.verify_chain(self.trusted_cert_list)
            if self.client_gid:
                self.client_gid.verify_chain(self.trusted_cert_list)
            if self.object_gid:
                self.object_gid.verify_chain(self.trusted_cert_list)

    ##
    # Register functions that will be served by the XMLRPC server. This
    # function should be overrided by each descendant class.

    def register_functions(self):
        self.server.register_function(self.noop)

    ##
    # Sample no-op server function. The no-op function decodes the credential
    # that was passed to it.

    def noop(self, cred, anything):
        self.decode_authentication(cred)

        return anything

    ##
    # Execute the server, serving requests forever. 

    def run(self):
        self.server.serve_forever()


