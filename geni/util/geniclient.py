##
# This module implements the client-side of the Geni API. Stubs are provided
# that convert the supplied parameters to the necessary format and send them
# via XMLRPC to a Geni Server.
#
# TODO: Investigate ways to combine this with existing PLC API?
##

import xmlrpclib

from gid import *
from credential import *
from record import *
from geniticket import *

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

##
# The GeniClient class provides stubs for executing Geni operations. A given
# client object connects to one server. To connect to multiple servers, create
# multiple GeniClient objects.
#
# The Geni protocol uses an HTTPS connection, and the client's side of the
# connection uses his private key. Generally, this private key must match the
# public key that is containing in the GID that the client is providing for
# those functions that take a GID.

class GeniClient():
    ##
    # Create a new GeniClient object.
    #
    # @param url is the url of the server
    # @param key_file = private key file of client
    # @param cert_file = x.509 cert containing the client's public key. This
    #      could be a GID certificate, or any x.509 cert.

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

    ##
    # Create a new GID. For MAs and SAs that are physically located on the
    # registry, this allows a owner/operator/PI to create a new GID and have it
    # signed by his respective authority.
    #
    # @param cred credential of caller
    # @param name hrn for new GID
    # @param uuid unique identifier for new GID
    # @param pkey_string public-key string (TODO: why is this a string and not a keypair object?)
    #
    # @return a GID object

    def create_gid(self, cred, name, uuid, pkey_string):
        gid_str = self.server.create_gid(cred.save_to_string(save_parents=True), name, uuid, pkey_string)
        return GID(string=gid_str)

    ##
    # Retrieve the GID for an object. This function looks up a record in the
    # registry and returns the GID of the record if it exists.
    # TODO: Is this function needed? It's a shortcut for Resolve()
    #
    # @param name hrn to look up
    #
    # @return a GID object

    def get_gid(self, name):
       gid_str_list = self.server.get_gid(name)
       gid_list = []
       for str in gid_str_list:
           gid_list.append(GID(string=str))
       return gid_list

    ##
    # Get_self_credential a degenerate version of get_credential used by a
    # client to get his initial credential when he doesn't have one. This is
    # the same as get_credential(..., cred=None,...).
    #
    # The registry ensures that the client is the principal that is named by
    # (type, name) by comparing the public key in the record's GID to the
    # private key used to encrypt the client-side of the HTTPS connection. Thus
    # it is impossible for one principal to retrieve another principal's
    # credential without having the appropriate private key.
    #
    # @param type type of object (user | slice | sa | ma | node
    # @param name human readable name of object
    #
    # @return a credential object

    def get_self_credential(self, type, name):
        cred_str = self.server.get_self_credential(type, name)
        return Credential(string = cred_str)

    ##
    # Retrieve a credential for an object.
    #
    # If cred==None, then the behavior reverts to get_self_credential()
    #
    # @param cred credential object specifying rights of the caller
    # @param type type of object (user | slice | sa | ma | node)
    # @param name human readable name of object
    #
    # @return a credental object

    def get_credential(self, cred, type, name):
        if cred == None:
            return self.get_self_credential(type, name)
        cred_str = self.server.get_credential(cred.save_to_string(save_parents=True), type, name)
        return Credential(string = cred_str)

    ##
    # List the records in an authority. The objectGID in the supplied credential
    # should name the authority that will be listed.
    #
    # @param cred credential object specifying rights of the caller
    #
    # @return list of record objects

    def list(self, cred, auth_hrn):
        result_dict_list = self.server.list(cred.save_to_string(save_parents=True), auth_hrn)
        result_rec_list = []
        for dict in result_dict_list:
             result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

    ##
    # Register an object with the registry. In addition to being stored in the
    # Geni database, the appropriate records will also be created in the
    # PLC databases.
    #
    # The geni_info and/or pl_info fields must in the record must be filled
    # out correctly depending on the type of record that is being registered.
    #
    # TODO: The geni_info member of the record should be parsed and the pl_info
    # adjusted as necessary (add/remove users from a slice, etc)
    #
    # @param cred credential object specifying rights of the caller
    # @return record to register
    #
    # @return GID object for the newly-registered record

    def register(self, cred, record):
        gid_str = self.server.register(cred.save_to_string(save_parents=True), record.as_dict())
        return GID(string = gid_str)

    ##
    # Remove an object from the registry. If the object represents a PLC object,
    # then the PLC records will also be removed.
    #
    # @param cred credential object specifying rights of the caller
    # @param type
    # @param hrn

    def remove(self, cred, type, hrn):
        result = self.server.remove(cred.save_to_string(save_parents=True), type, hrn)
        return result

    ##
    # Resolve an object in the registry. A given HRN may have multiple records
    # associated with it, and therefore multiple records may be returned. The
    # caller should check the type fields of the records to find the one that
    # he is interested in.
    #
    # @param cred credential object specifying rights of the caller
    # @param name human readable name of object

    def resolve(self, cred, name):
        result_dict_list = self.server.resolve(cred.save_to_string(save_parents=True), name)
        result_rec_list = []
        for dict in result_dict_list:
             result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

    ##
    # Update an object in the registry. Currently, this only updates the
    # PLC information associated with the record. The Geni fields (name, type,
    # GID) are fixed.
    #
    # The record is expected to have the pl_info field filled in with the data
    # that should be updated.
    #
    # TODO: The geni_info member of the record should be parsed and the pl_info
    # adjusted as necessary (add/remove users from a slice, etc)
    #
    # @param cred credential object specifying rights of the caller
    # @param record a record object to be updated

    def update(self, cred, record):
        result = self.server.update(cred.save_to_string(save_parents=True), record.as_dict())
        return result


    #-------------------------------------------------------------------------
    # Aggregate Interface
    #-------------------------------------------------------------------------
    
    ## Get components
    #
    # 
    def list_components(self):
        result = self.server.list_components()
        return result

    def list_resources(self, cred, hrn):
        result = self.server.get_resources(cred.save_to_string(save_parents=True), hrn)
        return result

    def get_policy(self, cred):
        result = self.server.get_policy(cred.save_to_string(save_parents=True))
        return result


    # ------------------------------------------------------------------------
    # Slice Interface
    # ------------------------------------------------------------------------

    ##
    # Start a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def start_slice(self, cred):
        result = self.server.start_slice(cred.save_to_string(save_parents=True))
        return result

    ##
    # Stop a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def stop_slice(self, cred):
        result = self.server.stop_slice(cred.save_to_string(save_parents=True))
        return result

    ##
    # Reset a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def reset_slice(self, cred):
        result = self.server.reset_slice(cred.save_to_string(save_parents=True))
        return result

    ##
    # Delete a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def delete_slice(self, cred):
        result = self.server.delete_slice(cred.save_to_string(save_parents=True))
        return result

    ##
    # List the slices on a component.
    #
    # @param cred credential object that authorizes the caller
    #
    # @return a list of slice names

    def list_slices(self, cred):
        result = self.server.list_slices(cred.save_to_string(save_parents=True))
        return result

    ##
    # Retrieve a ticket. This operation is currently implemented on the
    # registry (see SFA, engineering decisions), and is not implemented on
    # components.
    #
    # The ticket is filled in with information from the PLC database. This
    # information includes resources, and attributes such as user keys and
    # initscripts.
    #
    # @param cred credential object
    # @param name name of the slice to retrieve a ticket for
    # @param rspec resource specification dictionary
    #
    # @return a ticket object

    def get_ticket(self, cred, name, rspec):
        ticket_str = self.server.get_ticket(cred.save_to_string(save_parents=True), name, rspec)
        ticket = Ticket(string=ticket_str)
        return ticket

    ##
    # Redeem a ticket. This operation is currently implemented on the
    # component.
    #
    # The ticket is submitted to the node manager, and the slice is instantiated
    # or updated as appropriate.
    #
    # TODO: This operation should return a sliver credential and indicate
    # whether or not the component will accept only sliver credentials, or
    # will accept both sliver and slice credentials.
    #
    # @param ticket a ticket object containing the ticket

    def redeem_ticket(self, ticket):
        result = self.server.redeem_ticket(ticket.save_to_string(save_parents=True))
        return result


