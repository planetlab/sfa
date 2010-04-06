#
# Registry is a SfaServer that implements the Registry interface
#
### $Id$
### $URL$
#

from sfa.util.server import SfaServer
from sfa.util.faults import *
from sfa.server.interface import Interfaces
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.soapprotocol as soapprotocol
 

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

class Registries(Interfaces):
    
    default_dict = {'registries': {'registry': [default_fields]}}

    def __init__(self, api, conf_file = "/etc/sfa/registries.xml"):
        Interfaces.__init__(self, conf_file, 'sa') 

    def get_connections(self, interfaces):
        """
        read connection details for the trusted peer registries from file return 
        a dictionary of connections keyed on interface hrn. 
        """
        connections = Interfaces.get_connections(self, interfaces)

        # set up a connection to the local registry
        address = self.api.config.SFA_REGISTRY_HOST
        port = self.api.config.SFA_REGISTRY_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        local_registry = {'hrn': self.api.hrn, 'addr': address, 'port': port}
        connections[self.api.hrn] = xmlrpcprotocol.get_server(url, self.api.key_file, self.api.cert_file)            
        return connections 
