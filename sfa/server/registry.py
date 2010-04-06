#
# Registry is a SfaServer that implements the Registry interface
#
### $Id$
### $URL$
#

import tempfile
import os
import time
import sys

from sfa.util.server import SfaServer
from sfa.util.faults import *
from sfa.util.storage import *
from sfa.trust.gid import GID
from sfa.util.table import SfaTable
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.soapprotocol as soapprotocol
 
# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None            

##
# Registry is a SfaServer that serves registry and slice operations at PLC.
class Registry(SfaServer):
    ##
    # Create a new registry object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)
    
    def __init__(self, ip, port, key_file, cert_file):
        SfaServer.__init__(self, ip, port, key_file, cert_file)
        self.server.interface = 'registry' 


##
# Registries is a dictionary of registry connections keyed on the registry
# hrn

class Registries(dict):

    default_fields = {
        'hrn': '',
        'addr': '', 
        'port': '', 
    }

    def __init__(self, api, file = "/etc/sfa/registries.xml"):
        dict.__init__(self, {})
        self.api = api
        
        # create default connection dict
        registries_dict = {'registries': {'registry': [default_fields]}}

        # load config file
        self.registry_info = XmlStorage(file, registries_dict)
        self.registry_info.load()
        self.interfaces = self.registry_info['registries']['registry']
        if not isinstance(self.interfaces, list):
            self.interfaces = [self.interfaces]
        
        # Attempt to get any missing peer gids
        # There should be a gid file in /etc/sfa/trusted_roots for every
        # peer registry found in in the registries.xml config file. If there
        # are any missing gids, request a new one from the peer registry.
        gids_current = self.api.auth.trusted_cert_list.get_list()
        hrns_current = [gid.get_hrn() for gid in gids_found] 
        hrns_expected = [interface['hrn'] for interfaces in self.interfaces] 
        new_hrns = set(hrns_current).difference(hrns_expected)
        
        self.get_peer_gids(new_hrns)

        # update the local db records for these registries
        self.update_db_records('sa')
        
        # create connections to the registries
        self.update(self.get_connections(interfaces))

    def get_peer_gids(self, new_hrns):
        """
        Install trusted gids from the specified interfaces.  
        """
        if not new_hrns:
            return

        trusted_certs_dir = self.api.config.get_trustedroots_dir()
        for new_hrn in new_hrns:
            try:
                # get gid from the registry
                registry = self.get_connections(self.interfaces[new_hrn])[new_hrn]
                trusted_gids = registry.get_trusted_certs()
                # default message
                message = "interface: registry\tunable to retrieve and install trusted gid for %s" % new_hrn 
                if trusted_gids:
                    # the gid we want shoudl be the first one in the list, but lets 
                    # make sure
                    for trusted_gid in trusted_gids:
                        gid = GID(string=trusted_gids[0])
                        if gid.get_hrn() == new_hrn:
                            gid_filename = os.path.join(trusted_certs_dir, '%s.gid' % new_hrn)
                            gid.save_to_file(gid_filename, save_parents=True)
                            message = "interface: registry\tinstalled trusted gid for %s" % \
                                (new_hrn)
                # log the message
                self.api.logger.info(message)
            except:
                message = "interface: registry\tunable to retrieve and install trusted gid for %s" % new_hrn 
                self.api.logger.info(message)
        
        # reload the trusted certs list
        self.api.auth.load_trusted_certs()

    def update_db_records(self, type):
        """
        Make sure there is a record in the local db for allowed registries
        defined in the config file (registries.xml). Removes old records from
        the db.         
        """
        # get hrns we expect to find
        hrns_expected = self.interfaces.keys()

        # get hrns that actually exist in the db
        table = SfaTable()
        records = table.find({'type': 'sa'})
        hrns_found = [record['hrn'] for record in records]
        
        # remove old records
        for record in records:
            if record['hrn'] not in hrns_expected:
                table.remove(record)

        # add new records
        for hrn in hrns_expected:
            if hrn not in hrns_found:
                record = {
                    'hrn': hrn,
                    'type': 'sa',
                }
            table.insert(record)
                        
 
    def get_connections(self, registries):
        """
        read connection details for the trusted peer registries from file return 
        a dictionary of connections keyed on interface hrn. 
        """
        connections = {}
        required_fields = self.default_fields.keys()
        if not isinstance(registries, []):
            registries = [registries]
        for registry in registries:
            # make sure the required fields are present and not null
            for key in required_fields
                if not registry.get(key):
                    continue 
            hrn, address, port = registry['hrn'], registry['addr'], registry['port']
            url = 'http://%(address)s:%(port)s' % locals()
            # check which client we should use
            # sfa.util.xmlrpcprotocol is default
            client_type = 'xmlrpcprotocol'
            if registry.has_key('client') and \
               registry['client'] in ['geniclientlight'] and \
               GeniClientLight:
                client_type = 'geniclientlight'
                connections[hrn] = GeniClientLight(url, self.api.key_file, self.api.cert_file) 
            else:
                connections[hrn] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file)

        # set up a connection to the local registry
        address = self.api.config.SFA_REGISTRY_HOST
        port = self.api.config.SFA_REGISTRY_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        local_registry = {'hrn': self.api.hrn, 'addr': address, 'port': port}
        connections[self.api.hrn] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file)            
        return connections 
