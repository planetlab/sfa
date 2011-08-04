import traceback
import os.path

from sfa.util.faults import *
from sfa.util.storage import XmlStorage
from sfa.util.xrn import get_authority, hrn_to_urn
from sfa.util.record import SfaRecord
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.soapprotocol as soapprotocol
from sfa.trust.gid import GID

# GeniLight client support is optional
try:
    from egeni.geniLight_client import *
except ImportError:
    GeniClientLight = None            


##
# In is a dictionary of registry connections keyed on the registry
# hrn

class Interfaces(dict):
    """
    Interfaces is a base class for managing information on the
    peers we are federated with. It is responsible for the following:

    1) Makes sure a record exist in the local registry for the each 
       fedeated peer   
    2) Attempts to fetch and install trusted gids   
    3) Provides connections (xmlrpc or soap) to federated peers
    """

    # fields that must be specified in the config file
    default_fields = {
        'hrn': '',
        'addr': '', 
        'port': '', 
    }

    # defined by the class 
    default_dict = {}

    types = ['authority']

    def __init__(self, api, conf_file, type='authority'):
        if type not in self.types:
            raise SfaInfaildArgument('Invalid type %s: must be in %s' % (type, self.types))    
        dict.__init__(self, {})
        self.api = api
        self.type = type  
        # load config file
        self.interface_info = XmlStorage(conf_file, self.default_dict)
        self.interface_info.load()
        interfaces = self.interface_info.values()[0].values()[0]
        if not isinstance(interfaces, list):
            interfaces = [self.interfaces]
        # set the url and urn 
        for interface in interfaces:
            # port is appended onto the domain, before the path. Should look like:
            # http://domain:port/path
            hrn, address, port = interface['hrn'], interface['addr'], interface['port']
            address_parts = address.split('/')
            address_parts[0] = address_parts[0] + ":" + str(port)
            url =  "http://%s" %  "/".join(address_parts)
            interface['url'] = url
            interface['urn'] = hrn_to_urn(hrn, 'authority')
    
        self.interfaces = {}
        required_fields = self.default_fields.keys()
        for interface in interfaces:
            valid = True
            # skp any interface definition that has a null hrn, 
            # address or port
            for field in required_fields:
                if field not in interface or not interface[field]:
                    valid = False
                    break
            if valid:     
                self.interfaces[interface['hrn']] = interface


    def get_connections(self):
        """
        read connection details for the trusted peer registries from file return 
        a dictionary of connections keyed on interface hrn. 
        """
        connections = {}
        required_fields = self.default_fields.keys()
        for interface in self.interfaces.values():
            url = interface['url']
#            sfa_logger().debug("Interfaces.get_connections - looping on neighbour %s"%url)
            # check which client we should use
            # sfa.util.xmlrpcprotocol is default
            client_type = 'xmlrpcprotocol'
            if interface.has_key('client') and \
               interface['client'] in ['geniclientlight'] and \
               GeniClientLight:
                client_type = 'geniclientlight'
                connections[hrn] = GeniClientLight(url, self.api.key_file, self.api.cert_file) 
            else:
                connections[interface['hrn']] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file, timeout=30)

        return connections 
