import sys
import zlib

from sfa.util.faults import *
from sfa.util.xrn import urn_to_hrn
from sfa.util.method import Method
from sfa.util.parameter import Parameter, Mixed
from sfa.trust.credential import Credential
from sfa.util.sfatablesRuntime import run_sfatables

class ListResources(Method):
    """
    Returns information about available resources or resources allocated to this slice
    @param credential list
    @param options dictionary
    @return string
    """
    interfaces = ['aggregate', 'slicemgr']
    accepts = [
        Mixed(Parameter(str, "Credential string"), 
              Parameter(type([str]), "List of credentials")),
        Parameter(dict, "Options"),
        Parameter(str, "call_id"),
        ]
    returns = Parameter(str, "List of resources")

    def call(self, creds, options, call_id=""):
        self.api.logger.info("interface: %s\tmethod-name: %s" % (self.api.interface, self.name))
        
        # get slice's hrn from options    
        xrn = options.get('geni_slice_urn', '')
        (hrn, _) = urn_to_hrn(xrn)

        # Find the valid credentials
        valid_creds = self.api.auth.checkCredentials(creds, 'listnodes', hrn)

        # get hrn of the original caller 
        origin_hrn = options.get('origin_hrn', None)
        if not origin_hrn:
            origin_hrn = Credential(string=valid_creds[0]).get_gid_caller().get_hrn()
        # get manager for this interface    
        manager = self.api.get_interface_manager()
        rspec = manager.ListResources(self.api, creds, options, call_id)

        # filter rspec through sfatables 
        if self.api.interface in ['aggregate']:
            chain_name = 'OUTGOING'
        elif self.api.interface in ['slicemgr']: 
            chain_name = 'FORWARD-OUTGOING'
        self.api.logger.debug("ListResources: sfatables on chain %s"%chain_name)
        filtered_rspec = run_sfatables(chain_name, hrn, origin_hrn, rspec) 
 
        if options.has_key('geni_compressed') and options['geni_compressed'] == True:
            filtered_rspec = zlib.compress(filtered_rspec).encode('base64')

        return filtered_rspec  
    
    
