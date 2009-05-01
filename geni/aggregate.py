import os
import sys
import datetime
import time
import xmlrpclib

from types import StringTypes, ListType
from geni.util.geniserver import GeniServer
from geni.util.geniclient import GeniClient
# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None
from geni.util.storage import *
from geni.util.excep import *

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
        self.server.interface = 'aggregate'

##
# Aggregates is a dictionary of geniclient aggregate connections keyed on the aggregate hrn

class Aggregates(dict):

    required_fields = ['hrn', 'addr', 'port']
     
    def __init__(self, api):
        dict.__init__(self, {})
        self.api = api
        aggregates_file = self.api.server_basedir + os.sep + 'aggregates.xml'
        connection_dict = {}
        for field in self.required_fields:
            connection_dict[field] = ''
        self.aggregate_info = XmlStorage(aggregates_file, {'aggregates': {'aggregate': [connection_dict]}})
        self.aggregate_info.load()
        self.connectAggregates()


    def connectAggregates(self):
        """
        Get connection details for the trusted peer aggregates from file and 
        create an GeniClient connection to each. 
        """
        aggregates = self.aggregate_info['aggregates']['aggregate']
        if isinstance(aggregates, dict):
            aggregates = [aggregates]
        if isinstance(aggregates, list):
            for aggregate in aggregates:
                # make sure the required fields are present
                if not set(self.required_fields).issubset(aggregate.keys()):
                    continue
                hrn, address, port = aggregate['hrn'], aggregate['addr'], aggregate['port']
                if not hrn or not address or not port:
                    continue
                # check which client we should use
                # geniclient is default
                client_type = 'geniclient'
                if aggregate.has_key('client') and aggregate['client'] in ['geniclientlight']:
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
        address = self.api.config.GENI_AGGREGATE_HOSTNAME
        port = self.api.config.GENI_AGGREGATE_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        self[self.api.hrn] = GeniClient(url, self.api.key_file, self.api.cert_file)
                   
