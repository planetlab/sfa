#!/usr/bin/python

from lxml import etree
from StringIO import StringIO
from sfa.util.xrn import *
from sfa.rspecs.sfa_rspec import SfaRSpec
from sfa.rspecs.pg_rspec import PGRSpec

class SfaRSpecConverter:

    @staticmethod
    def to_pg_rspec(rspec):
        if isinstance(rspec, SfaRSpec):
            sfa_rspec = rspec
        else:
            sfa_rspec = SfaRSpec(rspec=rspec)
        pg_rspec = PGRSpec()
    
        # get networks
        networks = sfa_rspec.get_networks()
        
        for network in networks:
            # get nodes
            sfa_node_elements = sfa_rspec.get_node_elements(network=network)
            for sfa_node_element in sfa_node_elements:
                # create node element
                node_attrs = {}
                node_attrs['exclusive'] = 'false'
                node_attrs['component_manager_id'] = network
                if sfa_node_element.find('hostname') != None:
                    node_attrs['component_name'] = sfa_node_element.find('hostname').text
                if sfa_node_element.find('urn') != None:    
                    node_attrs['component_id'] = sfa_node_element.find('urn').text
                node_element = pg_rspec.add_element('node', node_attrs)

                # create node_type element
                for hw_type in ['plab-pc', 'pc']:
                    hdware_type_element = pg_rspec.add_element('hardware_type', {'name': hw_type}, parent=node_element)
                # create available element
                pg_rspec.add_element('available', {'now': 'true'}, parent=node_element)
                # create locaiton element
                # We don't actually associate nodes with a country. 
                # Set country to "unknown" until we figure out how to make
                # sure this value is always accurate.
                location = sfa_node_element.find('location')
                if location != None:
                    location_attrs = {}      
                    location_attrs['country'] =  location.get('country', 'unknown')
                    location_attrs['latitude'] = location.get('latitiue', 'None')
                    location_attrs['longitude'] = location.get('longitude', 'None')
                    pg_rspec.add_element('location', location_attrs, parent=node_element)

                sliver_element = sfa_node_element.find('sliver')
                if sliver_element != None:
                    pg_rspec.add_element('sliver_type', {'name': 'planetlab-vnode'}, parent=node_element)

        return pg_rspec.toxml()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:    
        print SfaRSpecConverter.to_pg_rspec(sys.argv[1])
