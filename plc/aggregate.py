##
# Aggregate is a GeniServer that implements the Slice interface at PLC

import tempfile
import os
import time
import sys

from util.hierarchy import Hierarchy
from util.trustedroot import TrustedRootList
from util.cert import Keypair, Certificate
from util.gid import GID
from util.geniserver import GeniServer
from util.record import GeniRecord
from util.genitable import GeniTable
from util.geniticket import Ticket
from util.excep import *
from util.misc import *

##
# Aggregate class extends GeniServer class

class Aggregate(GeniServer):
    ##
    # Create a new aggregate object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

        # get PL account settings from config module
        self.pl_auth = get_pl_auth()

        # connect to planetlab
        if "Url" in self.pl_auth:
            self.connect_remote_shell()
        else:
            self.connect_local_shell()

    ##
    # Connect to a remote shell via XMLRPC

    def connect_remote_shell(self):
        import remoteshell
        self.shell = remoteshell.RemoteShell()

    ##
    # Connect to a local shell via local API functions

    def connect_local_shell(self):
        import PLC.Shell
        self.shell = PLC.Shell.Shell(globals = globals())

    ##
    # Register the server RPCs for the slice interface

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.create_slice)
        self.server.register_function(self.get_ticket)
        self.server.register_function(self.redeem_ticket)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.reset_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.get_slice_resources)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.list_nodes)

    ##
    # Given an authority name, return the information for that authority. This
    # is basically a stub that calls the hierarchy module.
    #
    # @param auth_hrn human readable name of authority

    def get_auth_info(self, auth_hrn):
        return AuthHierarchy.get_auth_info(auth_hrn)

    ##
    # Given an authority name, return the database table for that authority. If
    # the database table does not exist, then one will be automatically
    # created.
    #
    # @param auth_name human readable name of authority

    def get_auth_table(self, auth_name):
        auth_info = self.get_auth_info(auth_name)

        table = GeniTable(hrn=auth_name,
                          cninfo=auth_info.get_dbinfo())

        # if the table doesn't exist, then it means we haven't put any records
        # into this authority yet.

        if not table.exists():
            report.trace("Registry: creating table for authority " + auth_name)
            table.create()

        return table

    ##
    # Verify that an authority belongs to this registry. This is basically left
    # up to the implementation of the hierarchy module. If the specified name
    # does not belong to this registry, an exception is thrown indicating the
    # caller should contact someone else.
    #
    # @param auth_name human readable name of authority

    def verify_auth_belongs_to_me(self, name):
        # get_auth_info will throw an exception if the authority does not
        # exist
        self.get_auth_info(name)

    ##
    # Verify that an object belongs to this registry. By extension, this implies
    # that the authority that owns the object belongs to this registry. If the
    # object does not belong to this registry, then an exception is thrown.
    #
    # @param name human readable name of object

    def verify_object_belongs_to_me(self, name):
        auth_name = get_authority(name)
        if not auth_name:
            # the root authority belongs to the registry by default?
            # TODO: is this true?
            return
        self.verify_auth_belongs_to_me(auth_name)

    ##
    # Verify that the object_gid that was specified in the credential allows
    # permission to the object 'name'. This is done by a simple prefix test.
    # For example, an object_gid for planetlab.us.arizona would match the
    # objects planetlab.us.arizona.slice1 and planetlab.us.arizona.
    #
    # @param name human readable name to test

    def verify_object_permission(self, name):
        object_hrn = self.object_gid.get_hrn()
        if object_hrn == name:
            return
        if name.startswith(object_hrn + "."):
            return
        raise PermissionError(name)

    ##
    # Convert a PLC record into the slice information that will be stored in
    # a ticket. There are two parts to this information: attributes and
    # rspec.
    #
    # Attributes are non-resource items, such as keys and the initscript
    # Rspec is a set of resource specifications
    #
    # @param record a record object
    #
    # @return a tuple (attrs, rspec) of dictionaries

    def record_to_slice_info(self, record):

        # get the user keys from the slice
        keys = []
        persons = self.shell.GetPersons(self.pl_auth, record.pl_info['person_ids'])
        for person in persons:
            person_keys = self.shell.GetKeys(self.pl_auth, person["key_ids"])
            for person_key in person_keys:
                keys = keys + [person_key['key']]

        attributes={}
        attributes['name'] = record.pl_info['name']
        attributes['keys'] = keys
        attributes['instantiation'] = record.pl_info['instantiation']
        attributes['vref'] = 'default'
        attributes['timestamp'] = time.time()
        attributes['slice_id'] = record.pl_info['slice_id']

        rspec = {}

        # get the PLC attributes and separate them into slice attributes and
        # rspec attributes
        filter = {}
        filter['slice_id'] = record.pl_info['slice_id']
        plc_attrs = self.shell.GetSliceAttributes(self.pl_auth, filter)
        for attr in plc_attrs:
            name = attr['name']

            # initscripts: lookup the contents of the initscript and store it
            # in the ticket attributes
            if (name == "initscript"):
                filter={'name': attr['value']}
                initscripts = self.shell.GetInitScripts(self.pl_auth, filter)
                if initscripts:
                    attributes['initscript'] = initscripts[0]['script']
            else:
                rspec[name] = attr['value']

        return (attributes, rspec)

    ##
    # create_slice: Create (instantiate) a slice. 
    #
    # @param cred credential string
    # @param name name of the slice to retrieve a ticket for
    # @param rspec resource specification dictionary
    #
    # @return the string representation of a ticket object

    def create_slice(self, cred, name, rspec):
        self.decode_authentication(cred, "createslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: create a slice

    ##
    # get_ticket: Retrieve a ticket. 
    #
    # This operation is currently implemented on PLC only (see SFA,
    # engineering decisions); it is not implemented on components.
    #
    # The ticket is filled in with information from the PLC database. This
    # information includes resources, and attributes such as user keys and
    # initscripts.
    #
    # @param cred credential string
    # @param name name of the slice to retrieve a ticket for
    # @param rspec resource specification dictionary
    #
    # @return the string representation of a ticket object

    def get_ticket(self, cred, name, rspec):
        self.decode_authentication(cred, "getticket")

        self.verify_object_belongs_to_me(name)

        self.verify_object_permission(name)

        auth_hrn = get_authority(name)
        auth_info = self.get_auth_info(auth_hrn)

        records = self.resolve_raw("slice", name, must_exist=True)
        record = records[0]

        object_gid = record.get_gid_object()
        new_ticket = Ticket(subject = object_gid.get_subject())
        new_ticket.set_gid_caller(self.client_gid)
        new_ticket.set_gid_object(object_gid)
        new_ticket.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_ticket.set_pubkey(object_gid.get_pubkey())

        self.fill_record_info(record)

        (attributes, rspec) = self.record_to_slice_info(record)

        new_ticket.set_attributes(attributes)
        new_ticket.set_rspec(rspec)

        new_ticket.set_parent(AuthHierarchy.get_auth_ticket(auth_hrn))

        new_ticket.encode()
        new_ticket.sign()

        return new_ticket.save_to_string(save_parents=True)

    ##
    # redeem_ticket: Redeem a ticket.
    #
    # Not supported at a PLC aggregate.
    #
    # @param ...not sure...

    def redeem_ticket(self, whatever):
        return anything

    ##
    # stop_slice: Stop a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def stop_slice(self, cred_str):
        self.decode_authentication(cred_str, "stopslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: stop the slice

    ##
    # start_slice: Start a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def start_slice(self, cred_str):
        self.decode_authentication(cred_str, "startslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: start the slice

    ##
    # reset_slice: Reset a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def reset_slice(self, cred_str):
        self.decode_authentication(cred_str, "resetslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: reset the slice

    ##
    # delete_slice: Delete a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def delete_slice(self, cred_str):
        self.decode_authentication(cred_str, "deleteslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: delete the slice

    ##
    # get_resources: Get resources allocated to slice
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def get_slice_resources(self, cred_str):
        self.decode_authentication(cred_str, "getsliceresources")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # TODO: get resources allocated to slice

    ##
    # list_slices: List hosted slices.
    #
    # @param cred a credential identifying the caller (callerGID)

    def list_slices(self, cred_str):
        self.decode_authentication(cred_str, "listslices")
        # TODO: list hosted slices

    ##
    # list_nodes: List available nodes.
    #
    # @param cred a credential identifying the caller (callerGID)

    def list_nodes(self, cred_str):
        self.decode_authentication(cred_str, "listnodes")
        # TODO: list available nodes


