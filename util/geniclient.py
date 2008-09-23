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
from geniticket import *

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

    def getparser(self): 
        unmarshaller = ExceptionUnmarshaller() 
        parser = xmlrpclib.ExpatParser(unmarshaller) 
        return parser, unmarshaller

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
       self.server = xmlrpclib.ServerProxy(self.url, self.transport, allow_none=True)

    # -------------------------------------------------------------------------
    # Registry Interface
    # -------------------------------------------------------------------------

    def create_gid(self, cred, name, uuid, pkey_string):
        gid_str = self.server.create_gid(cred.save_to_string(save_parents=True), name, uuid, pkey_string)
        return GID(string=gid_str)

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
        if cred == None:
            return self.get_self_credential(type, name)
        cred_str = self.server.get_credential(cred.save_to_string(save_parents=True), type, name)
        return Credential(string = cred_str)

    def list(self, cred):
        result_dict_list = self.server.list(cred.save_to_string(save_parents=True))
        result_rec_list = []
        for dict in result_dict_list:
             result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

    def register(self, cred, record):
        gid_str = self.server.register(cred.save_to_string(save_parents=True), record.as_dict())
        return GID(string = gid_str)

    def remove(self, cred, record):
        result = self.server.remove(cred.save_to_string(save_parents=True), record.as_dict())
        return result

    def resolve(self, cred, name):
        result_dict_list = self.server.resolve(cred.save_to_string(save_parents=True), name)
        result_rec_list = []
        for dict in result_dict_list:
             result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

    def update(self, cred, record):
        result = self.server.update(cred.save_to_string(save_parents=True), record.as_dict())
        return result

    # ------------------------------------------------------------------------
    # Slice Interface
    # ------------------------------------------------------------------------

    def start_slice(self, cred):
        result = self.server.start_slice(cred.save_to_string(save_parents=True))
        return result

    def stop_slice(self, cred):
        result = self.server.stop_slice(cred.save_to_string(save_parents=True))
        return result

    def reset_slice(self, cred):
        result = self.server.reset_slice(cred.save_to_string(save_parents=True))
        return result

    def delete_slice(self, cred):
        result = self.server.delete_slice(cred.save_to_string(save_parents=True))
        return result

    def list_slices(self, cred):
        result = self.server.list_slices(cred.save_to_string(save_parents=True))
        return result

    def get_ticket(self, cred, name, rspec):
        ticket_str = self.server.get_ticket(cred.save_to_string(save_parents=True), name, rspec)
        ticket = Ticket(string=ticket_str)
        return ticket

    def redeem_ticket(self, ticket):
        result = self.server.redeem_ticket(ticket.save_to_string(save_parents=True))
        return result


