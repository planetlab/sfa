# 
import sys
import time,datetime
from StringIO import StringIO
from types import StringTypes
from copy import deepcopy
from copy import copy
from lxml import etree

from sfa.util.sfalogging import sfa_logger
from sfa.util.rspecHelper import merge_rspecs
from sfa.util.xrn import Xrn, urn_to_hrn, hrn_to_urn
from sfa.util.plxrn import hrn_to_pl_slicename
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
from sfa.util.version import version_core

# XX FIX ME:  should merge result from multiple aggregates instead of 
# calling aggregate implementation
from sfa.managers.aggregate_manager_pl import slice_status

# we have specialized xmlrpclib.ServerProxy to remember the input url
# OTOH it's not clear if we're only dealing with XMLRPCServerProxy instances
def get_serverproxy_url (server):
    try:
        return server.url
    except:
        sfa_logger().warning("GetVersion, falling back to xmlrpclib.ServerProxy internals")
        return server._ServerProxy__host + server._ServerProxy__handler 

def GetVersion(api):
    # peers explicitly in aggregates.xml
    peers =dict ([ (peername,get_serverproxy_url(v)) for (peername,v) in api.aggregates.iteritems() 
                   if peername != api.hrn])
    xrn=Xrn (api.hrn)
    sm_version=version_core({'interface':'slicemgr',
                             'hrn' : xrn.get_hrn(),
                             'urn' : xrn.get_urn(),
                             'peers': peers,
                             })
    # local aggregate if present needs to have localhost resolved
    if api.hrn in api.aggregates:
        local_am_url=get_serverproxy_url(api.aggregates[api.hrn])
        sm_version['peers'][api.hrn]=local_am_url.replace('localhost',sm_version['hostname'])
    return sm_version

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
    valid_cred = api.auth.checkCredentials(creds, 'renewsliver', hrn)[0]
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
        threads.run(server.RenewSliver, xrn, [credential], expiration_time)
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
    for (aggregate, aggregate_rspec) in aggregate_rspecs.iteritems():
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
        if isinstance(creds, list):
            origin_hrn = Credential(string=creds[0]).get_gid_caller().get_hrn()
        else:
            origin_hrn = Credential(string=creds).get_gid_caller().get_hrn()
    
    # look in cache first 
    if api.cache and not xrn:
        rspec =  api.cache.get('nodes')
        if rspec:
            return rspec

    hrn, type = urn_to_hrn(xrn)

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
    merged_rspec = merge_rspecs(results)

    # cache the result
    if api.cache and not xrn:
        api.cache.add('nodes', merged_rspec)
 
    return merged_rspec

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc.princeton.tmacktestslice',rspec)

if __name__ == "__main__":
    main()
    
