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
from sfa.util.record import GeniRecord
from sfa.util.policy import Policy
from sfa.util.prefixTree import prefixTree
from sfa.util.rspec import *
from sfa.util.sfaticket import *
from sfa.util.debug import log
from sfa.server.registry import Registries
from sfa.server.aggregate import Aggregates
import sfa.plc.peers as peers

def delete_slice(api, hrn, origin_hrn=None):
    credential = api.getCredential()
    aggregates = Aggregates(api)
    for aggregate in aggregates:
        success = False
        # request hash is optional so lets try the call without it
        try:
            request_hash=None
            aggregates[aggregate].delete_slice(credential, hrn, request_hash, origin_hrn)
            success = True
        except:
            print >> log, "%s" % (traceback.format_exc())
            print >> log, "Error calling delete slice at aggregate %s" % aggregate

        # try sending the request hash if the previous call failed
        if not success:
            try:
                arg_list = [credential, hrn]
                request_hash = api.key.compute_hash(arg_list)
                aggregates[aggregate].delete_slice(credential, hrn, request_hash, origin_hrn)
                success = True
            except:
                print >> log, "%s" % (traceback.format_exc())
                print >> log, "Error calling list nodes at aggregate %s" % aggregate
    return 1

def create_slice(api, hrn, rspec, origin_hrn=None):
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
    aggregates = Aggregates(api)
    credential = api.getCredential()

    # split the netspecs into individual rspecs
    netspecs = spec.getDictsByTagName('NetSpec')
    for netspec in netspecs:
        net_hrn = netspec['name']
        resources = {'start_time': start_time, 'end_time': end_time, 'networks': netspec}
        resourceDict = {'RSpec': resources}
        tempspec.parseDict(resourceDict)
        rspecs[net_hrn] = tempspec.toxml()

    #print "rspecs:", rspecs.keys()
    #print "aggregates:", aggregates.keys() 
    # send each rspec to the appropriate aggregate/sm
    for net_hrn in rspecs:
        try:
            # if we are directly connected to the aggregate then we can just 
            # send them the rspec. if not, then we may be connected to an sm 
            # thats connected to the aggregate
            if net_hrn in aggregates:
                # send the whloe rspec to the local aggregate
                if net_hrn in [api.hrn]:
                    try:
                        request_hash = None
                        aggregates[net_hrn].create_slice(credential, hrn, \
                                        rspec, request_hash, origin_hrn)
                    except:
                        arg_list = [credential,hrn,rspec]
                        request_hash = api.key.compute_hash(arg_list)
                        aggregates[net_hrn].create_slice(credential, hrn, \
                                        rspec, request_hash, origin_hrn)
                else:
                    try:
                        request_hash = None
                        aggregates[net_hrn].create_slice(credential, hrn, \
                                rspecs[net_hrn], request_hash, origin_hrn)
                    except:
                        arg_list = [credential,hrn,rspecs[net_hrn]]
                        request_hash = api.key.compute_hash(arg_list)
                        aggregates[net_hrn].create_slice(credential, hrn, \
                                rspecs[net_hrn], request_hash, origin_hrn)
            else:
                # lets forward this rspec to a sm that knows about the network
                arg_list = [credential, net_hrn]
                request_hash = api.key.compute_hash(arg_list)
                for aggregate in aggregates:
                    try:
                        network_found = aggregates[aggregate].get_aggregates(credential, net_hrn)
                    except:
                        network_found = aggregates[aggregate].get_aggregates(credential, net_hrn, request_hash)
                    if network_found:
                        try:
                            request_hash = None
                            aggregates[aggregate].create_slice(credential, hrn, \
                                    rspecs[net_hrn], request_hash, origin_hrn)
                        except:
                            arg_list = [credential, hrn, rspecs[net_hrn]]
                            request_hash = api.key.compute_hash(arg_list)
                            aggregates[aggregate].create_slice(credential, hrn, \
                                    rspecs[net_hrn], request_hash, origin_hrn)

        except:
            print >> log, "Error creating slice %(hrn)s at aggregate %(net_hrn)s" % \
                           locals()
            traceback.print_exc()
    return 1

def get_ticket(api, slice_hrn, rspec, origin_hrn=None):
    
    # get the netspecs contained within the clients rspec
    client_rspec = RSpec(xml=rspec)
    netspecs = client_rspec.getDictsByTagName('NetSpec')
    
    # create an rspec for each individual rspec 
    rspecs = {}
    temp_rspec = RSpec()
    for netspec in netspecs:
        net_hrn = netspec['name']
        resources = {'start_time': 0, 'end_time': 0 , 
                     'network': netspec}
        resourceDict = {'RSpec': resources}
        temp_rspec.parseDict(resourceDict)
        rspecs[net_hrn] = temp_rspec.toxml() 
    
    # send the rspec to the appropiate aggregate/sm
    aggregates = Aggregates(api)
    credential = api.getCredential()
    tickets = {}
    for net_hrn in rspecs:    
        try:
            # if we are directly connected to the aggregate then we can just
            # send them the request. if not, then we may be connected to an sm
            # thats connected to the aggregate
            if net_hrn in aggregates:
                try:
                    ticket = aggregates[net_hrn].get_ticket(credential, slice_hrn, \
                                rspecs[net_hrn], None, origin_hrn)
                    tickets[net_hrn] = ticket
                except:
                    arg_list = [credential,hrn,rspecs[net_hrn]]
                    request_hash = api.key.compute_hash(arg_list)
                    ticket = aggregates[net_hrn].get_ticket(credential, slice_hrn, \
                                rspecs[net_hrn], request_hash, origin_hrn)
                    tickets[net_hrn] = ticket 
            else:
                # lets forward this rspec to a sm that knows about the network
                arg_list = [credential, net_hrn]
                request_hash = api.key.compute_hash(arg_list)
                for agg in aggregates:
                    try:
                        network_found = aggregates[agg].get_aggregates(credential, \
                                                        net_hrn)
                    except:
                        network_found = aggregates[agg].get_aggregates(credential, \
                                                        net_hrn, request_hash)
                    if network_found:
                        try:
                            ticket = aggregates[aggregate].get_ticket(credential, \
                                        slice_hrn, rspecs[net_hrn], None, origin_hrn)
                            tickets[aggregate] = ticket
                        except:
                            arg_list = [credential, hrn, rspecs[net_hrn]]
                            request_hash = api.key.compute_hash(arg_list)
                            aggregates[aggregate].get_ticket(credential, slice_hrn, \
                                    rspecs[net_hrn], request_hash, origin_hrn)
                            tickets[aggregate] = ticket
        except:
            print >> log, "Error getting ticket for %(slice_hrn)s at aggregate %(net_hrn)s" % \
                           locals()
            
    # create a new ticket
    new_ticket = SfaTicket(subject = slice_hrn)
    new_ticket.set_gid_caller(api.auth.client_gid)
   
    tmp_rspec = RSpec()
    networks = []
    valid_data = {} 
    # merge data from aggregate ticket into new ticket 
    for agg_ticket in tickets.values():
        agg_ticket = SfaTicket(string=agg_ticket)
        object_gid = agg_ticket.get_gid_object()
        new_ticket.set_gid_object(object_gid)
        new_ticket.set_issuer(key=api.key, subject=api.hrn)
        new_ticket.set_pubkey(object_gid.get_pubkey())
        
        
        #new_ticket.set_attributes(data)
        tmp_rspec.parseString(agg_ticket.get_rspec)
        newtworks.extend([{'NetSpec': rspec.getDictsByTagName('NetSpec')}])
    
    #new_ticket.set_parent(api.auth.hierarchy.get_auth_ticket(auth_hrn))
    resources = {'networks': networks, 'start_time': 0, 'duration': 0}
    resourceDict = {'RSpec': resources}
    tmp_rspec.parseDict(resourceDict)
    new_ticket.set_rspec(tmp_rspec.toxml())
        
    new_ticket.encode()
    new_ticket.sign()          

def start_slice(api, hrn, origin_hrn=None):
    slicename = hrn_to_pl_slicename(hrn)
    slices = api.plshell.GetSlices(api.plauth, {'name': slicename}, ['slice_id'])
    if not slices:
        raise RecordNotFound(hrn)
    slice_id = slices[0]
    attributes = api.plshell.GetSliceTags(api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
    attribute_id = attreibutes[0]['slice_attribute_id']
    api.plshell.UpdateSliceTag(api.plauth, attribute_id, "1" )

    return 1
 
def stop_slice(api, hrn, origin_hrn):
    slicename = hrn_to_pl_slicename(hrn)
    slices = api.plshell.GetSlices(api.plauth, {'name': slicename}, ['slice_id'])
    if not slices:
        raise RecordNotFound(hrn)
    slice_id = slices[0]['slice_id']
    attributes = api.plshell.GetSliceTags(api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
    attribute_id = attributes[0]['slice_attribute_id']
    api.plshell.UpdateSliceTag(api.plauth, attribute_id, "0")
    return 1

def reset_slice(api, hrn, origin_hrn):
    # XX not implemented at this interface
    return 1

def get_slices(api):
    # XX just import the legacy module and excute that until
    # we transition the code to this module
    from sfa.plc.slices import Slices
    slices = Slices(api)
    slices.refresh()
    return slices['hrn']
     
def get_rspec(api, hrn=None, origin_hrn=None):
    from sfa.plc.nodes import Nodes
    nodes = Nodes(api, origin_hrn=origin_hrn)
    if hrn:
        rspec = nodes.get_rspec(hrn)
    else:
        nodes.refresh()
        rspec = nodes['rspec']

    return rspec

"""
Returns the request context required by sfatables. At some point, this mechanism should be changed
to refer to "contexts", which is the information that sfatables is requesting. But for now, we just
return the basic information needed in a dict.
"""
def fetch_context(slice_hrn, user_hrn, contexts):
    base_context = {'sfa':{'user':{'hrn':user_hrn}}}
    return base_context

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc.princeton.tmacktestslice',rspec)

if __name__ == "__main__":
    main()
    
