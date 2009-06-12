import os
import sys
import datetime
import time
import xmlrpclib

from geni.util.geniserver import GeniServer
from geni.util.geniclient import *
from geni.util.cert import Keypair, Certificate
from geni.util.credential import Credential
from geni.util.trustedroot import TrustedRootList
from geni.util.excep import *
from geni.util.misc import *
from geni.util.config import Config
from geni.util.rspec import Rspec
from geni.util.specdict import *
from geni.util.storage import SimpleStorage

class AltAggregate(GeniServer):

    hrn = None
    nodes_ttl = None
    nodes = None
    slices = None 
    policy = None
    timestamp = None
    threshold = None    
    shell = None
    registry = None
    key_file = None
    cert_file = None
    credential = None
  
    ##
    # Create a new aggregate object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     

    def __init__(self, ip, port, key_file, cert_file, config = "/usr/share/geniwrapper/geni/util/geni_config"):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        self.config = Config(config)
        self.basedir = self.config.GENI_BASE_DIR + os.sep
        self.server_basedir = self.basedir + os.sep + "geni" + os.sep
        self.hrn = self.config.GENI_INTERFACE_HRN
        
        nodes_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.components'])
        self.nodes = SimpleStorage(nodes_file)
        self.nodes.load()
       
        slices_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.slices'])
        self.slices = SimpleStorage(slices_file)
        self.slices.load()
 
        policy_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.policy'])
        self.policy = SimpleStorage(policy_file, {'whitelist': [], 'blacklist': []})
        self.policy.load()
        
        timestamp_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.timestamp']) 
        self.timestamp = SimpleStorage(timestamp_file)

        self.nodes_ttl = 1

        self.connectRegistry()
        #self.loadCredential()

    def connectRegistry(self):
        """
        Connect to the registry
        """
        # connect to registry using GeniClient
        address = self.config.GENI_REGISTRY_HOST
        port = self.config.GENI_REGISTRY_PORT
        url = 'https://%(address)s:%(port)s' % locals()
        self.registry = GeniClient(url, self.key_file, self.cert_file)

    def loadCredential(self):
        """
        Attempt to load credential from file if it exists. If it doesnt get 
        credential from registry.
        """ 

        self_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".cred"
        ma_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".ma.cred"
        
        # see if this file exists
        try:
            cred = Credential(filename = ma_cred_filename, subject=self.hrn)
            self.credential = cred.save_to_string()
        except IOError:
            # get self credential
            self_cred = self.registry.get_credential(None, 'ma', self.hrn)
            self_credential = Credential(string = self_cred)
            self_credential.save_to_file(self_cred_filename)

            # get ma credential
            ma_cred = self.registry.get_credential(self_cred)
            ma_credential = Credential(string = ma_cred)
            ma_credential.save_to_file(ma_cred_filename)
            self.credential = ma_cred

    def load_policy(self):
        """
        Read the list of blacklisted and whitelisted nodes.
        """
        self.policy.load()

    def getNodes(self, format = 'rspec'):
        """
        Return a list of components at this aggregate.
        """
    
    def getSlices(self):
        """
        Return a list of instnatiated managed by this slice manager.
        """
 
    def getResources(self, slice_hrn):
        """
        Return the current rspec for the specified slice.
        """
    
    def getTicket(self, hrn, rspec):
        """
        Retrieve a ticket
        """

    def createSlice(self, slice_hrn, rspec, attributes = []):
        """
        Instantiate/update slice according rspec
        """

    def updateSlice(self, slice_hrn, rspec, attributes = []):
        return self.create_slice(slice_hrn, rspec, attributes)
         
    def deleteSlice(self, slice_hrn):
        """
        Remove this slice
        """

    def startSlice(self, slice_hrn):
        """
        Stop the slice
        """

    def stopSlice(self, slice_hrn):
        """
        Stop the slice at the aggregate level
        """

    def resetSlice(self, slice_hrn):
        """
        Reset the slice
        """

    def getPolicy(self):
        """
        Return this aggregates policy.
        """
    

##############################
## Server methods here for now
##############################

    def list_nodes(self, cred, format):
        self.decode_authentication(cred, 'listnodes')
        return self.getNodes(format)

    def list_slices(self, cred):
        self.decode_authentication(cred, 'listslices')
        return self.getSlices()

    def get_resources(self, cred, hrn):
        self.decode_authentication(cred, 'listnodes')
        return self.getResources(hrn)

    def get_ticket(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'getticket')
        return self.getTicket(hrn, rspec)
 
    def get_policy(self, cred):
        self.decode_authentication(cred, 'getpolicy')
        return self.getPolicy()

    def create_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'createslice')
        return self.createSlice(hrn, rspec)

    def update_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'updateslice')
        return self.updateSlice(hrn)    

    def delete_slice(self, cred, hrn):
        self.decode_authentication(cred, 'deleteslice')
        return self.deleteSlice(hrn)

    def start_slice(self, cred, hrn):
        self.decode_authentication(cred, 'startslice')
        return self.startSlice(hrn)

    def stop_slice(self, cred, hrn):
        self.decode_authentication(cred, 'stopslice')
        return self.stopSlice(hrn)

    def reset_slice(self, cred, hrn):
        self.decode_authentication(cred, 'resetslice')
        return self.resetSlice(hrn)

    def register_functions(self):
        GeniServer.register_functions(self)

        # Aggregate interface methods
        self.server.register_function(self.list_nodes)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.get_resources)
        self.server.register_function(self.get_ticket)
        self.server.register_function(self.get_policy)
        self.server.register_function(self.create_slice)
        self.server.register_function(self.update_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.reset_slice)
              
