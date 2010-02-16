### $Id: slices.py 15842 2009-11-22 09:56:13Z anil $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/slices.py $

import datetime
import time
import traceback
import sys
from copy import deepcopy
from lxml import etree
from StringIO import StringIO
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

    # Validate the RSpec against PlanetLab's schema
    schema = "/var/www/html/schemas/pl.rng"
    if schema:
        try:
            tree = etree.parse(StringIO(rspec))
        except etree.XMLSyntaxError:
            message = str(sys.exc_info()[1])
            raise InvalidRSpec(message)

        relaxng_doc = etree.parse(schema)
        relaxng = etree.RelaxNG(relaxng_doc)
        
        if not relaxng(tree):
            error = relaxng.error_log.last_error
            message = "%s (line %s)" % (error.message, error.line)
            raise InvalidRSpec(message)

    aggs = Aggregates(api)
    cred = api.getCredential()                                                 
    for agg in aggs:
        if agg not in [api.auth.client_cred.get_gid_caller().get_hrn()]:      
            try:
                # Just send entire RSpec to each aggregate
                aggs[agg].create_slice(cred, xrn, rspec, origin_hrn)
            except:
                print >> log, "Error creating slice %s at %s" % (hrn, agg)
                traceback.print_exc()

    return True

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
	if attributes.get('initscripts', []) != None:
            valid_data['initscripts'].extend(attributes.get('initscripts', []))
	if attributes.get('slivers', []) != None:
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
    hrn, type = urn_to_hrn(xrn)
    rspec = None

    aggs = Aggregates(api)
    cred = api.getCredential()                                                 
    for agg in aggs:
        if agg not in [api.auth.client_cred.get_gid_caller().get_hrn()]:      
            try:
                # get the rspec from the aggregate
                agg_rspec = aggs[agg].get_resources(cred, xrn, origin_hrn)
            except:
                # XX print out to some error log
                print >> log, "Error getting resources at aggregate %s" % agg
                traceback.print_exc(log)
                print >> log, "%s" % (traceback.format_exc())

                
            try:
                tree = etree.parse(StringIO(agg_rspec))
            except etree.XMLSyntaxError:
                message = agg + ": " + str(sys.exc_info()[1])
                raise InvalidRSpec(message)

            root = tree.getroot()
            if root.get("type") in ["Planetlab", "VINI"]:
                if rspec == None:
                    rspec = root
                else:
                    for network in root.iterfind("./network"):
                        rspec.append(deepcopy(network))

    return etree.tostring(rspec, xml_declaration=True, pretty_print=True)

"""
Returns the request context required by sfatables. At some point, this
mechanism should be changed to refer to "contexts", which is the
information that sfatables is requesting. But for now, we just return
the basic information needed in a dict.
"""
def fetch_context(slice_hrn, user_hrn, contexts):
    #slice_hrn = urn_to_hrn(slice_xrn)[0]
    #user_hrn = urn_to_hrn(user_xrn)[0]
    base_context = {'sfa':{'user':{'hrn':user_hrn}, 'slice':{'hrn':slice_hrn}}}
    return base_context

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc.princeton.tmacktestslice',rspec)

if __name__ == "__main__":
    main()
    
