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
                node_attrs['component_manager_id'] = network
                if sfa_node_element.find('hostname') != None:
                    node_attrs['component_name'] = sfa_node_element.find('hostname').text
                if sfa_node_element.find('urn') != None:    
                    node_attrs['component_id'] = sfa_node_element.find('urn').text
                node_element = pg_rspec.add_element('node', node_attrs)

                # create node_type element
                node_type_attrs = {'type_name': 'pcvm', 'type_slots': '100'}    
                node_type_element = pg_rspec.add_element('node_type', node_type_attrs, parent=node_element)
                # create available element
                pg_rspec.add_element('available', parent=node_element, text='true')
                # create exclusive element
                pg_rspec.add_element('exclusive', parent=node_element, text='false')
                # create locaiton element
                # We don't actually associate nodes with a country. 
                # Set country to "unknown" until we figure out how to make
                # sure this value is always accurate.
                location = sfa_node_element.find('location')
                if location != None:
                    location_attrs = {}      
                    location_attrs['country'] = locatiton.get('country', 'unknown')
                    location_attrs['latitude'] = location.get('latitiue', 'None')
                    location_attrs['longitude'] = location.get('longitude', 'None')
                    pg_rspec.add_element('location', location_attrs, parent=node_element)
                # TODO: convert sliver element

        return pg_rspec.toxml()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:    
        print SfaRSpecConverter.to_pg_rspec(sys.argv[1])
