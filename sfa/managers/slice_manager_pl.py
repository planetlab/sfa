### $Id: slices.py 15842 2009-11-22 09:56:13Z anil $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/slices.py $

import sys
import time,datetime
from StringIO import StringIO
from types import StringTypes
from copy import deepcopy
from copy import copy
from lxml import etree

from sfa.util.sfalogging import sfa_logger
from sfa.util.rspecHelper import merge_rspecs
from sfa.util.xrn import urn_to_hrn, hrn_to_urn
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *
from sfa.util.record import SfaRecord
from sfa.util.policy import Policy
from sfa.util.prefixTree import prefixTree
from sfa.util.sfaticket import *
from sfa.trust.credential import Credential
from sfa.util.threadmanager import ThreadManager
import sfa.util.xmlrpcprotocol as xmlrpcprotocol     
import sfa.plc.peers as peers

def get_version():
    version = {}
    version['geni_api'] = 1
    version['sfa'] = 1
    return version

def slice_status(api, slice_xrn, creds ):
    hrn, type = urn_to_hrn(slice_xrn)
    # find out where this slice is currently running
    api.logger.info(hrn)
    slicename = hrn_to_pl_slicename(hrn)
    api.logger.info("Checking status for %s" % slicename)
    slices = api.plshell.GetSlices(api.plauth, [slicename], ['node_ids','person_ids','name','expires'])
    if len(slices) == 0:        
        raise Exception("Slice %s not found (used %s as slicename internally)" % (slice_xrn, slicename))
    slice = slices[0]
    
    nodes = api.plshell.GetNodes(api.plauth, slice['node_ids'],
                                    ['hostname', 'boot_state', 'last_contact'])
    api.logger.info(slice)
    api.logger.info(nodes)
    
    result = {}
    result['geni_urn'] = slice_xrn
    result['geni_status'] = 'unknown'
    result['pl_login'] = slice['name']
    result['pl_expires'] = slice['expires']
    
    resources = []
    
    for node in nodes:
        res = {}
        res['pl_hostname'] = node['hostname']
        res['pl_boot_state'] = node['boot_state']
        res['pl_last_contact'] = node['last_contact']
        res['geni_urn'] = ''
        res['geni_status'] = 'unknown'
        res['geni_error'] = ''

        resources.append(res)
        
    result['geni_resources'] = resources
    return result

def create_slice(api, xrn, creds, rspec, users):
    hrn, type = urn_to_hrn(xrn)

    # Validate the RSpec against PlanetLab's schema --disabled for now
    # The schema used here needs to aggregate the PL and VINI schemas
    # schema = "/var/www/html/schemas/pl.rng"
    schema = None
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

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'createsliver', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:     
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM 
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
            
        # Just send entire RSpec to each aggregate
        server = api.aggregates[aggregate]
        threads.run(server.CreateSliver, xrn, credential, rspec, users)
            
    results = threads.get_results() 
    merged_rspec = merge_rspecs(results)
    return merged_rspec

def renew_slice(api, xrn, creds, expiration_time):
    hrn, type = urn_to_hrn(xrn)

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'renewesliver', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue

        server = api.aggregates[aggregate]
        threads.run(server.RenewSliver, xrn, credential, expiration_time)
    threads.get_results()
    return 1

def get_ticket(api, xrn, creds, rspec, users):
    slice_hrn, type = urn_to_hrn(xrn)
    # get the netspecs contained within the clients rspec
    aggregate_rspecs = {}
    tree= etree.parse(StringIO(rspec))
    elements = tree.findall('./network')
    for element in elements:
        aggregate_hrn = element.values()[0]
        aggregate_rspecs[aggregate_hrn] = rspec 

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'getticket', slice_hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential() 
    threads = ThreadManager()
    for aggregate, aggregate_rspec in aggregate_rspecs.items():
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        server = None
        if aggregate in api.aggregates:
            server = api.aggregates[aggregate]
        else:
            net_urn = hrn_to_urn(aggregate, 'authority')     
            # we may have a peer that knows about this aggregate
            for agg in api.aggregates:
                target_aggs = api.aggregates[agg].get_aggregates(credential, net_urn)
                if not target_aggs or not 'hrn' in target_aggs[0]:
                    continue
                # send the request to this address 
                url = target_aggs[0]['url']
                server = xmlrpcprotocol.get_server(url, api.key_file, api.cert_file)
                # aggregate found, no need to keep looping
                break   
        if server is None:
            continue 
        threads.run(server.GetTicket, xrn, credential, aggregate_rspec, users)

    results = threads.get_results()
    
    # gather information from each ticket 
    rspecs = []
    initscripts = []
    slivers = [] 
    object_gid = None  
    for result in results:
        agg_ticket = SfaTicket(string=result)
        attrs = agg_ticket.get_attributes()
        if not object_gid:
            object_gid = agg_ticket.get_gid_object()
        rspecs.append(agg_ticket.get_rspec())
        initscripts.extend(attrs.get('initscripts', [])) 
        slivers.extend(attrs.get('slivers', [])) 
    
    # merge info
    attributes = {'initscripts': initscripts,
                 'slivers': slivers}
    merged_rspec = merge_rspecs(rspecs) 

    # create a new ticket
    ticket = SfaTicket(subject = slice_hrn)
    ticket.set_gid_caller(api.auth.client_gid)
    ticket.set_issuer(key=api.key, subject=api.hrn)
    ticket.set_gid_object(object_gid)
    ticket.set_pubkey(object_gid.get_pubkey())
    #new_ticket.set_parent(api.auth.hierarchy.get_auth_ticket(auth_hrn))
    ticket.set_attributes(attributes)
    ticket.set_rspec(merged_rspec)
    ticket.encode()
    ticket.sign()          
    return ticket.save_to_string(save_parents=True)


def delete_slice(api, xrn, creds):
    hrn, type = urn_to_hrn(xrn)

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'deletesliver', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        server = api.aggregates[aggregate]
        threads.run(server.DeleteSliver, xrn, credential)
    threads.get_results()
    return 1

def start_slice(api, xrn, creds):
    hrn, type = urn_to_hrn(xrn)

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'startslice', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        server = api.aggregates[aggregate]
        threads.run(server.Start, xrn, credential)
    threads.get_results()    
    return 1
 
def stop_slice(api, xrn, creds):
    hrn, type = urn_to_hrn(xrn)

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'stopslice', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        server = api.aggregates[aggregate]
        threads.run(server.Stop, xrn, credential)
    threads.get_results()    
    return 1

def reset_slice(api, xrn):
    """
    Not implemented
    """
    return 1

def shutdown(api, xrn, creds):
    """
    Not implemented   
    """
    return 1

def status(api, xrn, creds):
    """
    Not implemented 
    """
    return 1

def get_slices(api, creds):

    # look in cache first
    if api.cache:
        slices = api.cache.get('slices')
        if slices:
            return slices    

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'listslices', None)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    # fetch from aggregates
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        server = api.aggregates[aggregate]
        threads.run(server.ListSlices, credential)

    # combime results
    results = threads.get_results()
    slices = []
    for result in results:
        slices.extend(result)
    
    # cache the result
    if api.cache:
        api.cache.add('slices', slices)

    return slices
 
def get_rspec(api, creds, options):
    
    # get slice's hrn from options
    xrn = options.get('geni_slice_urn', '')
    hrn, type = urn_to_hrn(xrn)

    # get hrn of the original caller
    origin_hrn = options.get('origin_hrn', None)
    if not origin_hrn:
        origin_hrn = Credential(string=creds[0]).get_gid_caller().get_hrn()
    
    # look in cache first 
    if api.cache and not xrn:
        rspec =  api.cache.get('nodes')
        if rspec:
            return rspec

    hrn, type = urn_to_hrn(xrn)
    rspec = None

    # get the callers hrn
    valid_cred = api.auth.checkCredentials(creds, 'listnodes', hrn)[0]
    caller_hrn = Credential(string=valid_cred).get_gid_caller().get_hrn()

    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        # prevent infinite loop. Dont send request back to caller
        # unless the caller is the aggregate's SM
        if caller_hrn == aggregate and aggregate != api.hrn:
            continue
        # get the rspec from the aggregate
        server = api.aggregates[aggregate]
        my_opts = copy(options)
        my_opts['geni_compressed'] = False
        threads.run(server.ListResources, credential, my_opts)
        #threads.run(server.get_resources, cred, xrn, origin_hrn)
                    
    results = threads.get_results()
    # combine the rspecs into a single rspec 
    for agg_rspec in results:
        try:
            tree = etree.parse(StringIO(agg_rspec))
        except etree.XMLSyntaxError:
            message = str(agg_rspec) + ": " + str(sys.exc_info()[1])
            raise InvalidRSpec(message)

        root = tree.getroot()
        if root.get("type") in ["SFA"]:
            if rspec == None:
                rspec = root
            else:
                for network in root.iterfind("./network"):
                    rspec.append(deepcopy(network))
                for request in root.iterfind("./request"):
                    rspec.append(deepcopy(request))
    
    sfa_logger().debug('get_rspec: rspec=%r'%rspec)
    rspec =  etree.tostring(rspec, xml_declaration=True, pretty_print=True)
    # cache the result
    if api.cache and not xrn:
        api.cache.add('nodes', rspec)
 
    return rspec

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc.princeton.tmacktestslice',rspec)

if __name__ == "__main__":
    main()
    
