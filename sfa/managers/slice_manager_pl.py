### $Id: slices.py 15842 2009-11-22 09:56:13Z anil $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/slices.py $

import datetime
import time
import traceback
import sys

from types import StringTypes
from sfa.util.namespace import *
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *
from sfa.util.record import SfaRecord
from sfa.util.policy import Policy
from sfa.util.prefixTree import prefixTree
from sfa.util.rspec import *
from sfa.util.sfaticket import *
from sfa.util.debug import log
from sfa.server.registry import Registries
from sfa.server.aggregate import Aggregates
import sfa.plc.peers as peers

def delete_slice(api, xrn, origin_hrn=None):
    credential = api.getCredential()
    aggregates = Aggregates(api)
    for aggregate in aggregates:
        success = False
        # request hash is optional so lets try the call without it
        try:
            aggregates[aggregate].delete_slice(credential, xrn, origin_hrn)
            success = True
        except:
            print >> log, "%s" % (traceback.format_exc())
            print >> log, "Error calling delete slice at aggregate %s" % aggregate
    return 1

def create_slice(api, xrn, rspec, origin_hrn=None):
    hrn, type = urn_to_hrn(xrn)
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
        resources = {'start_time': start_time, 'end_time': end_time, 'networks': {'NetSpec' : netspec}}
        resourceDict = {'RSpec': resources}
        tempspec.parseDict(resourceDict)
        rspecs[net_hrn] = tempspec.toxml()
    
    #print "rspecs:", rspecs.keys()
    #print "aggregates:", aggregates.keys() 
    # send each rspec to the appropriate aggregate/sm
    for net_hrn in rspecs:
        net_urn = hrn_to_urn(net_hrn, 'authority')
        try:
            # if we are directly connected to the aggregate then we can just 
            # send them the rspec. if not, then we may be connected to an sm 
            # thats connected to the aggregate
            if net_hrn in aggregates:
                # send the whloe rspec to the local aggregate
                if net_hrn in [api.hrn]:
                    aggregates[net_hrn].create_slice(credential, xrn, rspec, \
                                origin_hrn)
                else:
                    aggregates[net_hrn].create_slice(credential, xrn, \
                                rspecs[net_hrn], origin_hrn)
            else:
                # lets forward this rspec to a sm that knows about the network
                for aggregate in aggregates:
                    network_found = aggregates[aggregate].get_aggregates(credential, net_hrn)
                    if network_found:
                        aggregates[aggregate].create_slice(credential, xrn, \
                                    rspecs[net_hrn], origin_hrn)

        except:
            print >> log, "Error creating slice %(hrn)s at aggregate %(net_hrn)s" % \
                           locals()
            traceback.print_exc()
    return 1

def get_ticket(api, xrn, rspec, origin_hrn=None):
    slice_hrn, type = urn_to_hrn(xrn)
    # get the netspecs contained within the clients rspec
    client_rspec = RSpec(xml=rspec)
    netspecs = client_rspec.getDictsByTagName('NetSpec')
    
    # create an rspec for each individual rspec 
    rspecs = {}
    temp_rspec = RSpec()
    for netspec in netspecs:
        net_hrn = netspec['name']
        resources = {'start_time': 0, 'end_time': 0 , 
                     'network': {'NetSpec' : netspec}}
        resourceDict = {'RSpec': resources}
        temp_rspec.parseDict(resourceDict)
        rspecs[net_hrn] = temp_rspec.toxml() 
    
    # send the rspec to the appropiate aggregate/sm
    aggregates = Aggregates(api)
    credential = api.getCredential()
    tickets = {}
    for net_hrn in rspecs:
        net_urn = urn_to_hrn(net_hrn)     
        try:
            # if we are directly connected to the aggregate then we can just
            # send them the request. if not, then we may be connected to an sm
            # thats connected to the aggregate
            if net_hrn in aggregates:
                ticket = aggregates[net_hrn].get_ticket(credential, xrn, \
                            rspecs[net_hrn], origin_hrn)
                tickets[net_hrn] = ticket
            else:
                # lets forward this rspec to a sm that knows about the network
                for agg in aggregates:
                    network_found = aggregates[agg].get_aggregates(credential, net_urn)
                    if network_found:
                        ticket = aggregates[aggregate].get_ticket(credential, \
                                        slice_hrn, rspecs[net_hrn], origin_hrn)
                        tickets[aggregate] = ticket
        except:
            print >> log, "Error getting ticket for %(slice_hrn)s at aggregate %(net_hrn)s" % \
                           locals()
            
    # create a new ticket
    new_ticket = SfaTicket(subject = slice_hrn)
    new_ticket.set_gid_caller(api.auth.client_gid)
    new_ticket.set_issuer(key=api.key, subject=api.hrn)
   
    tmp_rspec = RSpec()
    networks = []
    valid_data = {
        'timestamp': int(time.time()),
        'initscripts': [],
        'slivers': [] 
    } 
    # merge data from aggregate ticket into new ticket 
    for agg_ticket in tickets.values():
        # get data from this ticket
        agg_ticket = SfaTicket(string=agg_ticket)
        attributes = agg_ticket.get_attributes()
        valid_data['initscripts'].extend(attributes.get('initscripts', []))
        valid_data['slivers'].extend(attributes.get('slivers', []))
 
        # set the object gid
        object_gid = agg_ticket.get_gid_object()
        new_ticket.set_gid_object(object_gid)
        new_ticket.set_pubkey(object_gid.get_pubkey())

        # build the rspec
        tmp_rspec.parseString(agg_ticket.get_rspec())
        networks.extend([{'NetSpec': tmp_rspec.getDictsByTagName('NetSpec')}])
    
    #new_ticket.set_parent(api.auth.hierarchy.get_auth_ticket(auth_hrn))
    new_ticket.set_attributes(valid_data)
    resources = {'networks': networks, 'start_time': 0, 'duration': 0}
    resourceDict = {'RSpec': resources}
    tmp_rspec.parseDict(resourceDict)
    new_ticket.set_rspec(tmp_rspec.toxml())
    new_ticket.encode()
    new_ticket.sign()          
    return new_ticket.save_to_string(save_parents=True)

def start_slice(api, xrn):
    hrn, type = urn_to_hrn(xrn)
    slicename = hrn_to_pl_slicename(hrn)
    slices = api.plshell.GetSlices(api.plauth, {'name': slicename}, ['slice_id'])
    if not slices:
        raise RecordNotFound(hrn)
    slice_id = slices[0]
    attributes = api.plshell.GetSliceTags(api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
    attribute_id = attreibutes[0]['slice_attribute_id']
    api.plshell.UpdateSliceTag(api.plauth, attribute_id, "1" )

    return 1
 
def stop_slice(api, xrn):
    hrn, type = urn_to_hrn(xrn)
    slicename = hrn_to_pl_slicename(hrn)
    slices = api.plshell.GetSlices(api.plauth, {'name': slicename}, ['slice_id'])
    if not slices:
        raise RecordNotFound(hrn)
    slice_id = slices[0]['slice_id']
    attributes = api.plshell.GetSliceTags(api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
    attribute_id = attributes[0]['slice_attribute_id']
    api.plshell.UpdateSliceTag(api.plauth, attribute_id, "0")
    return 1

def reset_slice(api, xrn):
    # XX not implemented at this interface
    return 1

def get_slices(api):
    # XX just import the legacy module and excute that until
    # we transition the code to this module
    from sfa.plc.slices import Slices
    slices = Slices(api)
    slices.refresh()
    return [hrn_to_urn(slice_hrn, 'slice') for slice_hrn in slices['hrn']]
     
def get_rspec(api, xrn=None, origin_hrn=None):
    
    from sfa.plc.nodes import Nodes
    nodes = Nodes(api, origin_hrn=origin_hrn)
    if xrn:
        rspec = nodes.get_rspec(xrn)
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
    #slice_hrn = urn_to_hrn(slice_xrn)[0]
    #user_hrn = urn_to_hrn(user_xrn)[0]
    base_context = {'sfa':{'user':{'hrn':user_hrn}}}
    return base_context

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc.princeton.tmacktestslice',rspec)

if __name__ == "__main__":
    main()
    
