import os
import xmlrpclib
from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.sfaticket import SfaTicket

def init_server():
    from server import sfa_component_setup
    # get current trusted gids
    try:
        sfa_component_setup.get_trusted_certs()
    except:
        # our keypair may be old, try refreshing
        sfa_component_setup.get_node_key()
        sfa_component_setup.get_credential(force=True)
        sfa_component_sertup.get_trusted_certs()
           
    

def start_slice(api, slicename):
    record = api.nmdb.get(hrn_to_pl_slicename(slicename))
    api.nodemanger.Start(record)

def stop_slice(api, slicename):
    record = api.nmdb.get(hrn_to_pl_slicename(slicename))
    api.nodemanager.Stop(record)

def delete_slice(api, slicename):
    record = api.nmdb.get(hrn_to_pl_slicename(slicename))
    api.nodemanager.Destroy(record)

def reset_slice(api, slicename):
    record = api.nmdb.get(hrn_to_pl_slicename(slicename))
    if not api.sliver_exists(slicename):
        raise SliverDoesNotExist(slicename)
    api.nodemanager.ReCreate(record)
 
def get_slices(api):
    slicenames = api.nodemanager.GetXIDs().keys()
    return slicenames

def roboot():
    os.system("/sbin/reboot")        

def redeem_ticket(api, ticket_string):
    ticket = SfaTicket(string=ticket_string)
    ticket.decode()
    hrn = ticket.attributes['slivers'][0]['hrn']
    slicename = hrn_to_pl_slicename(hrn)
    if not api.sliver_exists(slicename):
        raise SliverDoesNotExist(slicename)

    # convert ticket to format nm is used to
    nm_ticket = xmlrpclib.dumps((ticket.attributes,), methodresponse=True)
    self.api.nodemanager.AdminTicket(nm_ticket)
    

