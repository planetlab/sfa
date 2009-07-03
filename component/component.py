##
# Sfa Component Wrapper
#
# This wrapper implements the SFA Slice and Mgmt Interfaces on a node.
#
##

import tempfile
import os
import sys
from xmlrpclib import ServerProxy

from sfa.trust.certificate import Certificate, Keypair
from sfa.trust.gid import *
from sfa.trust.trustedroot import *

from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.record import *
from sfa.util.geniticket import *
from sfa.util.geniserver import *

##
# ComponentManager is a GeniServer that serves slice and
# management operations at a node.

class ComponentManager(GeniServer):

    ##
    # Create a new ComponentManager object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.nodemanager = ServerProxy('http://127.0.0.1:812/')

    ##
    # Register the server RPCs for the component

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.reset_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.redeem_ticket)
        self.server.register_function(self.reboot)

    def sliver_exists(self, slicename):
        dict = self.nodemanager.GetXIDs()
        if slicename in dict.keys():
            return True
        else:
            return False

    # ------------------------------------------------------------------------
    # Slice Interface

    ##
    # Stop a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def stop_slice(self, cred_str):
        self.decode_authentication(cred_str, "stopslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "stopslice:", slicename
        self.nodemanager.Stop(slicename)

    ##
    # Start a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def start_slice(self, cred_str):
        self.decode_authentication(cred_str, "startslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "startslice:", slicename
        self.nodemanager.Start(slicename)

    ##
    # Reset a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def reset_slice(self, cred_str):
        self.decode_authentication(cred_str, "resetslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "resetslice:", slicename

        # find the existing record for the slice
        if not self.sliver_exists(slicename):
            raise SliverDoesNotExist(slicename)

        self.nodemanager.ReCreate(slicename)

    ##
    # Delete a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def delete_slice(self, cred_str):
        self.decode_authentication(cred_str, "deleteslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "deleteslice:", slicename
        self.nodemanager.Destroy(slicename)

    ##
    # Examine the ticket that was provided by the caller, check that it is
    # signed and verified correctly. Throw an exception if something is
    # wrong with the ticket.
    #
    # This is similar to geniserver.decode_authentication
    #
    # @param ticket_string the string representation of the ticket

    def decode_ticket(self, ticket_string):
        self.client_ticket = Ticket(string = ticket_string)
        self.client_gid = self.client_ticket.get_gid_caller()
        self.object_gid = self.client_ticket.get_gid_object()

        # make sure the client_gid is not blank
        if not self.client_gid:
            raise MissingCallerGID(self.client_ticket.get_subject())

        # make sure the client_gid matches the certificate that the client is using
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(self.client_gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(self.client_gid.get_subject())

        if self.trusted_cert_list:
            self.client_ticket.verify_chain(self.trusted_cert_list)
            if self.client_gid:
                self.client_gid.verify_chain(self.trusted_cert_list)
            if self.object_gid:
                self.object_gid.verify_chain(self.trusted_cert_list)

    def geni_ticket_to_plc_ticket(self, ticket):
        ticket_attrs = ticket.get_attributes()
        ticket_rspec = ticket.get_rspec()

        data = {}
        rec = {}
        attr_list = []

        # sort out the initscript... The NM expects to receive an initscript name
        # and a dictionary of initscripts. NM ends up discarding the initscript
        # name and sticking the contents in the slice record. (technically, this
        # is what we started with, but we have to provide the data in the format
        # that the NM expects)
        if ticket_attrs.get("initscript", None):
            initscript_name = ticket_attrs.get("name") + "_initscript"
            initscript_body = ticket_attrs.get("initscript")
            data["initscripts"] = {"name": initscript_name, "script": initscript_body}
            attr_dict["initscript"] = initscript_name
        else:
            data["initscripts"] = {}

        # copy the rspec attributes from the geniticket into the plticket
        # attributes. The NM will later copy them back out and put them into
        # the rspec field of the slice record
        for itemname in ticket_rspec.keys():
            attr = {"name": itemname, "value": ticket_rspec[itemname]}
            attr_list.append(attr)

        # NM expects to receive a list of key dictionaries containing the
        # keys.
        keys = []
        for key in ticket_attrs.get("keys", []):
            keys.append({"key": key})
        rec["keys"] = keys

        rec["name"] = ticket_attrs.get("name")

        rec["attributes"] = attr_list
        rec["instantiation"] = ticket_attrs["instantiation"]
        rec["slice_id"] = ticket_attrs["slice_id"]

        # XXX - this shouldn't be hardcoded; use the actual slice name
        rec["delegations"] = "pl_genicw"

        data["timestamp"] = ticket_attrs.get("timestamp")
        data["slivers"] = [rec]

        return data

    ##
    # Redeem a ticket.
    #
    # The ticket is submitted to the node manager, and the slice is instantiated
    # or updated as appropriate.
    #
    # TODO: This operation should return a sliver credential and indicate
    # whether or not the component will accept only sliver credentials, or
    # will accept both sliver and slice credentials.
    #
    # @param ticket_str the string representation of a ticket object

    def redeem_ticket(self, ticket_str):
        self.decode_ticket(ticket_str)
        ticket = self.client_ticket

        print "ticket received for", self.object_gid.get_hrn()

        pt = self.geni_ticket_to_plc_ticket(ticket)

        print "plticket", pt

        str = xmlrpclib.dumps((pt,), allow_none=True)
        self.nodemanager.AdminTicket(str)

        # TODO: should return a sliver credential

    # ------------------------------------------------------------------------
    # Slice Interface

    ##
    # List the slices on a component.
    #
    # @param cred_str string representation of a credential object that
    #     authorizes the caller
    #
    # @return a list of slice names

    def list_slices(self, cred_str):
        self.decode_authentication(cred_str, "listslices")
        slice_names = self.nodemanager.GetXIDs().keys()
        return slice_names

    # ------------------------------------------------------------------------
    # Management Interface

    ##
    # Reboot the component.
    #
    # @param cred_str string representation of a credential object that
    #     authorizes the caller

    def reboot(self, cred_str):
        self.decode_authentication(cred_str, "reboot")
        system("/sbin/reboot")


if __name__ == "__main__":
    global TrustedRoots

    key_file = "component.key"
    cert_file = "component.cert"

    # if no key is specified, then make one up
    if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        key = Keypair(create=True)
        key.save_to_file(key_file)

        cert = Certificate(subject="component")
        cert.set_issuer(key=key, subject="component")
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    TrustedRoots = TrustedRootList()

    s = ComponentManager("", 12345, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

