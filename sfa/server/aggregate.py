### $Id$
### $URL$

import os
import sys
import datetime
import time

from sfa.util.server import SfaServer
from sfa.util.storage import *
from sfa.util.faults import *
from sfa.trust.gid import GID
from sfa.util.table import SfaTable
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.soapprotocol as soapprotocol

# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None


class Aggregate(SfaServer):

    ##
    # Create a new aggregate object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     
    def __init__(self, ip, port, key_file, cert_file):
        SfaServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'aggregate'

##
# Aggregates is a dictionary of aggregate connections keyed on the aggregate hrn

class Aggregates(dict):

    default_fields = {
        'hrn': '',
        'addr': '',
        'port': '',
    }    
 
    def __init__(self, api, file = "/etc/sfa/aggregates.xml"):
        dict.__init__(self, {})
        self.api = api
        
        # create default connection dict
        aggregates_dict = {'aggregates': {'aggregate': [default_fields]}}
        
        # load config file
        self.aggregate_info = XmlStorage(file, aggregates_dict)
        self.aggregate_info.load()
        self.interfaces = self.registry_info['aggregates']['aggregate']
        if not isinstance(self.interfaces, list):
            self.interfaces = [self.interfaces]

        # Attempt to get any missing peer gids
        # There should be a gid file in /etc/sfa/trusted_roots for every
        # peer registry found in in the aggregates.xml config file. If there
        # are any missing gids, request a new one from the peer registry.
        gids_current = self.api.auth.trusted_cert_list.get_list()
        hrns_current = [gid.get_hrn() for gid in gids_found]
        hrns_expected = [interface['hrn'] for interfaces in self.interfaces]
        new_hrns = set(hrns_current).difference(hrns_expected)

        self.get_peer_gids(new_hrns)
        self.connectAggregates()

    def connectAggregates(self):
        """
        Get connection details for the trusted peer aggregates from file and 
        create an connection to each. 
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
                self.interfaces.append(aggregate)
                # check which client we should use
                # sfa.util.xmlrpcprotocol is default
                client_type = 'xmlrpcprotocol'
                if aggregate.has_key('client') and aggregate['client'] in ['geniclientlight']:
                    client_type = 'geniclientlight'
                
                # create url
                url = 'http://%(address)s:%(port)s' % locals()

                # create the client connection
                # make sure module exists before trying to instantiate it
                if client_type in ['geniclientlight'] and GeniClientLight:
                    self[hrn] = GeniClientLight(url, self.api.key_file, self.api.cert_file)
                else:
                    self[hrn] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file)

        # set up a connection to the local registry
        address = self.api.config.SFA_AGGREGATE_HOST
        port = self.api.config.SFA_AGGREGATE_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        local_aggregate = {'hrn': self.api.hrn, 'addr': address, 'port': port}
        self.interfaces.append(local_aggregate) 
        self[self.api.hrn] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file)


