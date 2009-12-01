### $Id: slices.py 15842 2009-11-22 09:56:13Z anil $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/slices.py $

import datetime
import time
import traceback
import sys

from types import StringTypes
from sfa.util.misc import *
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *
from sfa.util.storage import *
from sfa.util.record import GeniRecord
from sfa.util.policy import Policy
from sfa.util.prefixTree import prefixTree
from sfa.util.debug import log
from sfa.server.aggregate import Aggregates
from sfa.server.registry import Registries

MAXINT =  2L**31-1

class Slices(SimpleStorage):

    rspec_to_slice_tag = {'max_rate':'net_max_rate'}

    def __init__(self, api, ttl = .5, caller_cred=None):
        self.api = api
        self.ttl = ttl
        self.threshold = None
        path = self.api.config.SFA_DATA_DIR
        filename = ".".join([self.api.interface, self.api.hrn, "slices"])
        filepath = path + os.sep + filename
        self.slices_file = filepath
        SimpleStorage.__init__(self, self.slices_file)
        self.policy = Policy(self.api)    
        self.load()
        self.caller_cred=caller_cred
        self.aggregates = Aggregates(self.api)
        
    def get_slivers(self, hrn, node=None):
        """
        Get the slivers at each aggregate
        """
        slivers = []
        for aggregate in self.aggregates:
            slivers += aggregate.get_slivers()
        return slivers
 
    def refresh(self):
        """
        Update the cached list of slices
        """
        # Reload components list
        now = datetime.datetime.now()
        if not self.has_key('threshold') or not self.has_key('timestamp') or \
           now > datetime.datetime.fromtimestamp(time.mktime(time.strptime(self['threshold'], self.api.time_format))):
            self.refresh_slices_smgr()

    def refresh_slices_smgr(self):
        slice_hrns = []
        aggregates = Aggregates(self.api)
        credential = self.api.getCredential()
        for aggregate in aggregates:
            success = False
            # request hash is optional so lets try the call without it 
            try:
                request_hash=None
                slices = aggregates[aggregate].get_slices(credential, request_hash, self.caller_cred)
                slice_hrns.extend(slices)
                success = True
            except:
                print >> log, "%s" % (traceback.format_exc())
                print >> log, "Error calling slices at aggregate %(aggregate)s" % locals()

            # try sending the request hash if the previous call failed 
            if not success:
                arg_list = [credential]
                request_hash = self.api.key.compute_hash(arg_list)
                try:
                    slices = aggregates[aggregate].get_slices(credential, request_hash, self.caller_cred)
                    slice_hrns.extend(slices)
                    success = True
                except:
                    print >> log, "%s" % (traceback.format_exc())
                    print >> log, "Error calling slices at aggregate %(aggregate)s" % locals()

        # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.api.time_format)
        delta = datetime.timedelta(hours=self.ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.api.time_format)

        slice_details = {'hrn': slice_hrns,
                         'timestamp': hr_timestamp,
                         'threshold': hr_threshold
                        }
        self.update(slice_details)
        self.write()


    def delete_slice(self, hrn):
        self.delete_slice_smgr(hrn)
        
    def delete_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        caller_cred = self.caller_cred
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            success = False
            # request hash is optional so lets try the call without it
            try:
                request_hash=None	
                aggregates[aggregate].delete_slice(credential, hrn, request_hash, caller_cred)
                success = True
            except:
                print >> log, "%s" % (traceback.format_exc())
                print >> log, "Error calling list nodes at aggregate %s" % aggregate
            
            # try sending the request hash if the previous call failed 
            if not success:
                try:
                    arg_list = [credential, hrn]
                    request_hash = self.api.key.compute_hash(arg_list)
                    aggregates[aggregate].delete_slice(credential, hrn, request_hash, caller_cred)
                    success = True
                except:
                    print >> log, "%s" % (traceback.format_exc())
                    print >> log, "Error calling list nodes at aggregate %s" % aggregate
                        
    def create_slice(self, hrn, rspec):
        
	# check our slice policy before we procede
        whitelist = self.policy['slice_whitelist']     
        blacklist = self.policy['slice_blacklist']
       
        if whitelist and hrn not in whitelist or \
           blacklist and hrn in blacklist:
            policy_file = self.policy.policy_file
            print >> log, "Slice %(hrn)s not allowed by policy %(policy_file)s" % locals()
            return 1

        self.create_slice_smgr(hrn, rspec)

    def create_slice_smgr(self, hrn, rspec):
        spec = RSpec()
        tempspec = RSpec()
        spec.parseString(rspec)
        slicename = hrn_to_pl_slicename(hrn)
        specDict = spec.toDict()
        if specDict.has_key('RSpec'): specDict = specDict['RSpec']
        if specDict.has_key('start_time'): start_time = specDict['start_time']
        else: start_time = 0
        if specDict.has_key('end_time'): end_time = specDict['end_time']
        else: end_time = 0

        rspecs = {}
        aggregates = Aggregates(self.api)
        credential = self.api.getCredential()

        # split the netspecs into individual rspecs
        netspecs = spec.getDictsByTagName('NetSpec')
        for netspec in netspecs:
            net_hrn = netspec['name']
            resources = {'start_time': start_time, 'end_time': end_time, 'networks': netspec}
            resourceDict = {'RSpec': resources}
            tempspec.parseDict(resourceDict)
            rspecs[net_hrn] = tempspec.toxml()

        # send each rspec to the appropriate aggregate/sm
        caller_cred = self.caller_cred 
        for net_hrn in rspecs:
            try:
                # if we are directly connected to the aggregate then we can just send them the rspec
                # if not, then we may be connected to an sm thats connected to the aggregate
                if net_hrn in aggregates:
                    # send the whloe rspec to the local aggregate
                    if net_hrn in [self.api.hrn]:
                        try:
			    request_hash = None
                            aggregates[net_hrn].create_slice(credential, hrn, rspec, request_hash, caller_cred)
                        except:
                            arg_list = [credential,hrn,rspec]
                            request_hash = self.api.key.compute_hash(arg_list)
                            aggregates[net_hrn].create_slice(credential, hrn, rspec, request_hash, caller_cred)
                    else:
                        try:
			    request_hash = None
                            aggregates[net_hrn].create_slice(credential, hrn, rspecs[net_hrn], request_hash, caller_cred)
                        except:
                            arg_list = [credential,hrn,rspecs[net_hrn]]
                            request_hash = self.api.key.compute_hash(arg_list)
                            aggregates[net_hrn].create_slice(credential, hrn, rspecs[net_hrn], request_hash, caller_cred)
                else:
                    # lets forward this rspec to a sm that knows about the network
                    arg_list = [credential, net_hrn]
                    request_hash = self.api.compute_hash(arg_list)    
                    for aggregate in aggregates:
                        try:
                            network_found = aggregates[aggregate].get_aggregates(credential, net_hrn)
                        except:
                            network_found = aggregates[aggregate].get_aggregates(credential, net_hrn, request_hash)
                        if network_networks:
                            try:
				request_hash = None
                                aggregates[aggregate].create_slice(credential, hrn, rspecs[net_hrn], request_hash, caller_cred)
                            except:
                                arg_list = [credential, hrn, rspecs[net_hrn]]
                                request_hash = self.api.key.compute_hash(arg_list) 
                                aggregates[aggregate].create_slice(credential, hrn, rspecs[net_hrn], request_hash, caller_cred)
                     
            except:
                print >> log, "Error creating slice %(hrn)s at aggregate %(net_hrn)s" % locals()
                traceback.print_exc()
        return 1


    def start_slice(self, hrn):
        self.start_slice_smgr(hrn)

    def start_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            aggregates[aggregate].start_slice(credential, hrn)
        return 1


    def stop_slice(self, hrn):
        self.stop_slice_smgr(hrn)

    def stop_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        arg_list = [credential, hrn]
        request_hash = self.api.key.compute_hash(arg_list)
        for aggregate in aggregates:
            try:
                aggregates[aggregate].stop_slice(credential, hrn)
            except:  
                aggregates[aggregate].stop_slice(credential, hrn, request_hash)

