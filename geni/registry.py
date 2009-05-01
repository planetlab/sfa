##
# Registry is a GeniServer that implements the Registry interface

import tempfile
import os
import time
import sys

from geni.util.geniserver import GeniServer
from geni.util.geniclient import GeniClient
# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None            
from geni.util.genitable import GeniTable
from geni.util.excep import *
from geni.util.storage import *


#


##
# Registry is a GeniServer that serves registry and slice operations at PLC.

class Registry(GeniServer):
    ##
    # Create a new registry object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'registry' 


##
# Registries is a dictionary of geniclient registry connections keyed on the registry
# hrn

class Registries(dict):

    required_fields = ['hrn', 'addr', 'port']

    def __init__(self, api):
        dict.__init__(self, {})
        self.api = api
        registries_file = self.api.server_basedir + os.sep + 'registries.xml'
        connection_dict = {}
        for field in self.required_fields:
            connection_dict[field] = ''  
        self.registry_info = XmlStorage(registries_file, {'registries': {'registry': [connection_dict]}})
        self.registry_info.load()
        self.connectRegistries()
        
    def connectRegistries(self):
        """
        Get connection details for the trusted peer registries from file and 
        create an GeniClient connection to each. 
        """
        registries = self.registry_info['registries']['registry']
        if isinstance(registries, dict):
            registries = [registries]
        if isinstance(registries, list):
            for registry in registries:
                # make sure the required fields are present
                if not set(self.required_fields).issubset(registry.keys()):
                    continue
                hrn, address, port = registry['hrn'], registry['addr'], registry['port']
                if not hrn or not address or not port:
                    continue

                # check which client we should use
                # geniclient is default
                client_type = 'geniclient'
                if registry.has_key('client') and registry['client'] in ['geniclientlight']:
                    client_type = 'geniclientlight'
                
                # create url
                url = 'http://%(address)s:%(port)s' % locals()

                # create the client connection
                # make sure module exists before trying to instantiate it
                if client_type in ['geniclientlight'] and GeniClientLight:
                    self[hrn] = GeniClientLight(url, self.api.key_file, self.api.cert_file) 
                else:    
                    self[hrn] = GeniClient(url, self.api.key_file, self.api.cert_file)

        # set up a connection to the local registry
        # connect to registry using GeniClient
        address = self.api.config.GENI_REGISTRY_HOSTNAME
        port = self.api.config.GENI_REGISTRY_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        self[self.api.hrn] = GeniClient(url, self.api.key_file, self.api.cert_file)            
    
