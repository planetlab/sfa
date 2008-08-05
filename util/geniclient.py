# geniclient.py
#
# geni client
#
# implements the client-side of the GENI API.
#
# TODO: Investigate ways to combine this with existing PLC API?

import xmlrpclib

from gid import *
from credential import *
from record import *

# GeniTransport
#
# A transport for XMLRPC that works on top of HTTPS

class GeniTransport(xmlrpclib.Transport):
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

# GeniClient:
#
# Class for performing GeniClient operations.

class GeniClient():
    # url = url of server
    # key_file = private key file of client
    # cert_file = x.509 cert of client
    def __init__(self, url, key_file, cert_file):
       self.url = url
       self.key_file = key_file
       self.cert_file = cert_file
       self.transport = GeniTransport()
       self.transport.key_file = self.key_file
       self.transport.cert_file = self.cert_file
       self.server = xmlrpclib.ServerProxy(self.url, self.transport)

    def get_gid(self, name):
       gid_str_list = self.server.get_gid(name)
       gid_list = []
       for str in gid_str_list:
           gid_list.append(GID(string=str))
       return gid_list

    # get_self_credential
    #
    # a degenerate version of get_credential used by a client to get his
    # initial credential when he doesn't have one. The same as calling
    # get_credential(..., cred=None,...)

    def get_self_credential(self, type, name):
       cred_str = self.server.get_self_credential(type, name)
       return Credential(string = cred_str)

    def get_credential(self, cred, type, name):
       cred_str = self.server.get_credential(cred.save_to_string(), type, name)
       return Credential(string = cred_str)

    def resolve(self, cred, name):
       result_dict_list = self.server.resolve(cred.save_to_string(), name)
       result_rec_list = []
       for dict in result_dict_list:
            result_rec_list.append(GeniRecord(dict=dict))
       return result_rec_list

