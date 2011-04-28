#!/usr/bin/python
from sfa.util.xrn import *
from sfa.util.plxrn import *
from sfa.rspecs.sfa_rspec import SfaRSpec
from sfa.rspecs.pg_rspec  import PGRSpec

class Aggregate:

    api = None
    sites = {}
    nodes = {}
    interfaces = {}
    links = {}
    tag_types = {}
    prepared=False

    def __init__(self, api):
        self.api = api

    def prepare_sites(self, force=False):
        if not self.sites or force:  
            for site in self.api.plshell.GetSites(self.api.plauth):
                self.sites[site['site_id']] = site
    
    def prepare_nodes(self, force=False):
        if not self.nodes or force:
            for node in self.api.plshell.GetNodes(self.api.plauth):
                self.nodes[node['node_id']] = node

    def prepare_interfaces(self, force=False):
        if not self.interfaces or force:
            for interface in self.api.plshell.GetInterfaces(self.api.plauth):
                self.interfaces[interface['interface_id']] = interface

    def prepare_links(self, force=False):
        if not self.links or force:
            pass

    def prepare_tagtypes(self, force=False):
        if not self.tag_types or force:
            for tag_type in self.api.plshell.GetTagTypes(self.api.plauth):
                self.tag_types[tag_type['tag_type_id']] = tag_type

    def prepare(self, force=False):
        if not self.prepared or force:
            self.prepare_sites(force)
            self.prepare_nodes(force)
            self.prepare_interfaces(force)
            self.prepare_links(force)
            self.prepare_tagtypes(force)
            # add site/interface info to nodes
            for node in self.nodes:
                site = self.sites[node['site_id']]
                interfaces = [self.interfaces[interface_id] for interface_id in node['interface_ids']]

        self.prepared = True  

    def get_rspec(self, slice_xrn=None, format='sfa'):
        self.prepare()
        rspec = None
        if format == ['pg']:
            rspec = PGRSpec()
        else:
            rspec = SfaRSpec()

        rspec.add_nodes(self.nodes)
        rspec.add_interfaces(self.interfaces) 
        rspec.add_links(self.links)

        if slice_xrn:
            slice_hrn, _ = urn_to_hrn(slice_xrn)
            slice_name = hrn_to_pl_slicename(slice_hrn)
            slices = self.api.plshell.GetSlices(self.api.plauth, slice_name)
            if slices:
                slice = slices[0]   
                hostnames = [self.nodes[node_id]['hostname'] for node_id in slice['node_ids']]
                rspec.add_slivers(hostnames)          
