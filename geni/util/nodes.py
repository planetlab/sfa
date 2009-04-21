import os
import time
import datetime
import sys

from geni.util.misc import *
from geni.util.rspec import *
from geni.util.specdict import * 
from geni.util.excep import *
from geni.util.storage import *
from geni.util.debug import log
from geni.util.rspec import *
from geni.util.specdict import * 
from geni.aggregate import Aggregates 
from geni.util.policy import Policy

class Nodes(SimpleStorage):

    def __init__(self, api, ttl = 1):
        self.api = api
        self.ttl = ttl
        self.threshold = None
        self.nodes_file = os.sep.join([self.api.server_basedir, self.api.interface +'.'+ self.api.hrn + '.nodes'])
        SimpleStorage.__init__(self, self.nodes_file)
        self.policy = Policy(api)
        self.load()


    def refresh(self):
        """
        Update the cached list of nodes
        """

        # Reload components list
        now = datetime.datetime.now()
        if not self.has_key('threshold') or not self.has_key('timestamp') or \
           now > datetime.datetime.fromtimestamp(time.mktime(time.strptime(self['threshold'], self.api.time_format))): 
            if self.api.interface in ['aggregate']:
                self.refresh_nodes_aggregate()
            elif self.api.interface in ['slicemgr']:
                self.refresh_nodes_smgr()

        
    def refresh_nodes_aggregate(self):
        rspec = Rspec()
        rspec.parseString(self.get_rspec())
        
        # filter nodes according to policy
        blist = self.policy['node_blacklist']
        wlist = self.policy['node_whitelist']
        rspec.filter('NodeSpec', 'name', blacklist=blist, whitelist=wlist)

        # extract ifspecs from rspec to get ips'
        ips = []
        ifspecs = rspec.getDictsByTagName('IfSpec')
        for ifspec in ifspecs:
            if ifspec.has_key('addr') and ifspec['addr']:
                ips.append(ifspec['addr'])

        # extract nodespecs from rspec to get dns names
        hostnames = []
        nodespecs = rspec.getDictsByTagName('NodeSpec')
        for nodespec in nodespecs:
            if nodespec.has_key('name') and nodespec['name']:
                hostnames.append(nodespec['name'])

        # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.api.time_format)
        delta = datetime.timedelta(hours=self.ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.api.time_format)

        node_details = {}
        node_details['rspec'] = rspec.toxml()
        node_details['ip'] = ips
        node_details['dns'] = hostnames
        node_details['timestamp'] = hr_timestamp
        node_details['threshold'] = hr_threshold
        # save state 
        self.update(node_details)
        self.write()       
 
    def refresh_nodes_smgr(self):
        # convert and threshold to ints
        if self.has_key('timestamp') and self['timestamp']:
            hr_timestamp = self['timestamp']
            timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(hr_timestamp, self.api.time_format)))
            hr_threshold = self['threshold']
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.strptime(hr_threshold, self.api.time_format)))
        else:
            timestamp = datetime.datetime.now()
            hr_timestamp = timestamp.strftime(self.api.time_format)
            delta = datetime.timedelta(hours=self.ttl)
            threshold = timestamp + delta
            hr_threshold = threshold.strftime(self.api.time_format)

        start_time = int(timestamp.strftime("%s"))
        end_time = int(threshold.strftime("%s"))
        duration = end_time - start_time

        aggregates = Aggregates(self.api)
        rspecs = {}
        networks = []
        rspec = Rspec()
        credential = self.api.getCredential() 
        for aggregate in aggregates:
            try:
                # get the rspec from the aggregate
                agg_rspec = aggregates[aggregate].get_resources(credential)
                # extract the netspec from each aggregates rspec
                rspec.parseString(agg_rspec)
                networks.extend([{'NetSpec': rspec.getDictsByTagName('NetSpec')}])
            except:
                raise
                # XX print out to some error log
                print >> log, "Error calling list nodes at aggregate %s" % aggregate
        # create the rspec dict
        resources = {'networks': networks, 'start_time': start_time, 'duration': duration}
        resourceDict = {'Rspec': resources}
        # convert rspec dict to xml
        rspec.parseDict(resourceDict)

        # filter according to policy
        blist = self.policy['node_blacklist']
        wlist = self.policy['node_whitelist']    
        rspec.filter('NodeSpec', 'name', blacklist=blist, whitelist=wlist)

        # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.api.time_format)
        delta = datetime.timedelta(hours=self.ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.api.time_format)

        nodedict = {'rspec': rspec.toxml(),
                    'timestamp': hr_timestamp,
                    'threshold':  hr_threshold}

        self.update(nodedict)
        self.write()


    def get_rspec(self, hrn = None):
        """
        Get resource information from PLC
        """

        # Get the required nodes
        if not hrn:
            nodes = self.api.plshell.GetNodes(self.api.plauth)
            try:  linkspecs = self.api.plshell.GetLinkSpecs() # if call is supported
            except:  linkspecs = []
        else:
            slicename = hrn_to_pl_slicename(hrn)
            slices = self.api.plshell.GetSlices(self.api.plauth, [slicename])
            if not slices:
                nodes = []
            else:
                slice = slices[0]
                node_ids = slice['node_ids']
                nodes = self.api.plshell.GetNodes(self.api.plauth, node_ids)

        # Filter out whitelisted nodes
        public_nodes = lambda n: n.has_key('slice_ids_whitelist') and not n['slice_ids_whitelist']
        nodes = filter(public_nodes, nodes)

        # Get all network interfaces
        interface_ids = []
        for node in nodes:
            interface_ids.extend(node['nodenetwork_ids'])
        interfaces = self.api.plshell.GetNodeNetworks(self.api.plauth, interface_ids)
        interface_dict = {}
        for interface in interfaces:
            interface_dict[interface['nodenetwork_id']] = interface

        # join nodes with thier interfaces
        for node in nodes:
            node['interfaces'] = []
            for nodenetwork_id in node['nodenetwork_ids']:
                node['interfaces'].append(interface_dict[nodenetwork_id])

        # convert and threshold to ints
        if self.has_key('timestamp') and self['timestamp']:
            timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self['timestamp'], self.api.time_format)))
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self['threshold'], self.api.time_format)))
        else:
            timestamp = datetime.datetime.now()
            delta = datetime.timedelta(hours=self.ttl)
            threshold = timestamp + delta

        start_time = int(timestamp.strftime("%s"))
        end_time = int(threshold.strftime("%s"))
        duration = end_time - start_time

        # create the plc dict
        networks = [{'nodes': nodes,
                     'name': self.api.hrn,
                     'start_time': start_time,
                     'duration': duration}]
        if not hrn:
            networks[0]['links'] = linkspecs
        resources = {'networks': networks, 'start_time': start_time, 'duration': duration}

        # convert the plc dict to an rspec dict
        resourceDict = RspecDict(resources)
        # convert the rspec dict to xml
        rspec = Rspec()
        rspec.parseDict(resourceDict)
        return rspec.toxml()
        
