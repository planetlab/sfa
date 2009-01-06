##
# SliceMgr is a GeniServer that implements the Slice interface at PLC

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

from util.config import *

##
# SliceMgr class extends GeniServer class

class SliceMgr(GeniServer):
    ##
    # Create a new slice manager object.
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
        # slice interface
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
        # extract per-aggregate netspec from rspec
        # call create_slice on each aggregate

    ##
    # get_ticket: Retrieve a ticket. 
    #
    # This operation is not supported as part of a slice manager
    #
    # @param cred credential string
    # @param name name of the slice to retrieve a ticket for
    # @param rspec resource specification dictionary
    #

    def get_ticket(self, cred, name, rspec):
        return anything

    ##
    # redeem_ticket: Redeem a ticket. 
    #
    # This operation is not supported as part of a slice manager
    #
    # @param cred credential string
    # @param name name of the slice to retrieve a ticket for
    # @param rspec resource specification dictionary
    #

    def redeem_ticket(self, cred, name, rspec):
        return anything

    ##
    # stop_slice: Stop a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def stop_slice(self, cred_str):
        self.decode_authentication(cred_str, "stopslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # call stop_slice on each aggregate that hosts the slice

    ##
    # start_slice: Start a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def start_slice(self, cred_str):
        self.decode_authentication(cred_str, "startslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # call start_slice on each aggregate that hosts the slice

    ##
    # reset_slice: Reset a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def reset_slice(self, cred_str):
        self.decode_authentication(cred_str, "resetslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # call reset_slice on each aggregate that hosts the slice

    ##
    # delete_slice: Delete a slice.
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def delete_slice(self, cred_str):
        self.decode_authentication(cred_str, "deleteslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # call delete_slice on each aggregate that hosts the slice

    ##
    # get_slice_resources: Get resources allocated to slice
    #
    # @param cred a credential identifying the caller (callerGID) and the slice
    #     (objectGID)

    def get_slice_resources(self, cred_str):
        self.decode_authentication(cred_str, "getsliceresources")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        # call get_resources on each aggregate that hosts the slice
        # merge returned netspecs into one big rspec

    ##
    # list_slices: List hosted slices.
    #
    # @param cred a credential identifying the caller (callerGID)

    def list_slices(self, cred_str):
        self.decode_authentication(cred_str, "listslices")
        # probably have this information cached, so return that
        # otherwise, call list_slices on all peer aggregates

    ##
    # list_nodes: List available nodes.
    #
    # @param cred a credential identifying the caller (callerGID)

    def list_nodes(self, cred_str):
        self.decode_authentication(cred_str, "listslices")
        # probably have this information cached, so return that
        # otherwise, call list_nodes on all peer aggregates
