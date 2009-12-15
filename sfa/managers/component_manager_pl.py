import os
import xmlrpclib
from sfa.util.faults import *
from sfa.util.misc import *
from sfa.util.sfaticket import SfaTicket

def start_slice(api, slicename):
    record = {'name': hrn_to_pl_slicename(slicename)}
    api.nodemanger.Start(record)

def stop_slice(api, slicename):
    record = {'name': hrn_to_pl_slicename(slicename)}
    api.nodemanager.Stop(record)

def delete_slice(api, slicename):
    record = {'name': hrn_to_pl_slicename(slicename)}
    api.nodemanager.Destroy(record)

def reset_slice(api, slicename):
    record = {'name': hrn_to_pl_slicename(slicename)}
    if not api.sliver_exists(slicename):
        raise SliverDoesNotExist(slicename)
    api.nodemanager.ReCreate(record)
 
def get_slices(api):
    slicenames = api.nodemanager.GetXiDs().keys()
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
    

