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
from sfa.util.callids import Callids

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

def CreateSliver(api, xrn, creds, rspec, users, call_id):

    if Callids().already_handled(call_id): return ""

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
        threads.run(server.CreateSliver, xrn, credential, rspec, users, call_id)
            
    results = threads.get_results() 
    merged_rspec = merge_rspecs(results)
    return merged_rspec

def RenewSliver(api, xrn, creds, expiration_time, call_id):
    if Callids().already_handled(call_id): return True

    (hrn, type) = urn_to_hrn(xrn)
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
        threads.run(server.RenewSliver, xrn, [credential], expiration_time, call_id)
    # 'and' the results
    return reduce (lambda x,y: x and y, threads.get_results() , True)

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


def DeleteSliver(api, xrn, creds, call_id):
    if Callids().already_handled(call_id): return ""
    (hrn, type) = urn_to_hrn(xrn)
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
        threads.run(server.DeleteSliver, xrn, credential, call_id)
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

# Thierry : caching at the slicemgr level makes sense to some extent
caching=True
#caching=False
def ListSlices(api, creds, call_id):

    if Callids().already_handled(call_id): return []

    # look in cache first
    if caching and api.cache:
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
        threads.run(server.ListSlices, credential, call_id)

    # combime results
    results = threads.get_results()
    slices = []
    for result in results:
        slices.extend(result)
    
    # cache the result
    if caching and api.cache:
        api.cache.add('slices', slices)

    return slices


def ListResources(api, creds, options, call_id):

    if Callids().already_handled(call_id): return ""

    # get slice's hrn from options
    xrn = options.get('geni_slice_urn', '')
    (hrn, type) = urn_to_hrn(xrn)

    # get hrn of the original caller
    origin_hrn = options.get('origin_hrn', None)
    if not origin_hrn:
        if isinstance(creds, list):
            origin_hrn = Credential(string=creds[0]).get_gid_caller().get_hrn()
        else:
            origin_hrn = Credential(string=creds).get_gid_caller().get_hrn()
    
    # look in cache first 
    if caching and api.cache and not xrn:
        rspec =  api.cache.get('nodes')
        if rspec:
            return rspec

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
        threads.run(server.ListResources, credential, my_opts, call_id)
        #threads.run(server.get_resources, cred, xrn, origin_hrn)
                    
    results = threads.get_results()
    merged_rspec = merge_rspecs(results)

    # cache the result
    if caching and api.cache and not xrn:
        api.cache.add('nodes', merged_rspec)
 
    return merged_rspec

# first draft at a merging SliverStatus
def SliverStatus(api, slice_xrn, creds, call_id):
    if Callids().already_handled(call_id): return {}
    # attempt to use delegated credential first
    credential = api.getDelegatedCredential(creds)
    if not credential:
        credential = api.getCredential()
    threads = ThreadManager()
    for aggregate in api.aggregates:
        server = api.aggregates[aggregate]
        threads.run (server.SliverStatus, slice_xrn, credential, call_id)
    results = threads.get_results()

    # get rid of any void result - e.g. when call_id was hit where by convention we return {}
    results = [ result for result in results if result and result['geni_resources']]

    # do not try to combine if there's no result
    if not results : return {}

    # otherwise let's merge stuff
    overall = {}

    # mmh, it is expected that all results carry the same urn
    overall['geni_urn'] = results[0]['geni_urn']

    # consolidate geni_status - simple model using max on a total order
    states = [ 'ready', 'configuring', 'failed', 'unknown' ]
    # hash name to index
    shash = dict ( zip ( states, range(len(states)) ) )
    def combine_status (x,y):
        return shash [ max (shash(x),shash(y)) ]
    overall['geni_status'] = reduce (combine_status, [ result['geni_status'] for result in results], 'ready' )

    # {'ready':0,'configuring':1,'failed':2,'unknown':3}
    # append all geni_resources
    overall['geni_resources'] = \
        reduce (lambda x,y: x+y, [ result['geni_resources'] for result in results] , [])

    return overall

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    CreateSliver(None,'plc.princeton.tmacktestslice',rspec,'create-slice-tmacktestslice')

if __name__ == "__main__":
    main()
    
