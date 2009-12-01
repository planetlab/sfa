import os
import xmlrpclib
from sfa.util.faults import *
from sfa.util.sfaticket import SfaTicket

def start_slice(api, slicename):
    api.nodemanger.Start(slicename)

def stop_slice(api, slicename):
    api.nodemanager.Stop(slicename)

def delete_slice(api, slicename):
    api.nodemanager.Destroy(slicename)

def reset_slice(api, slicename):
    if not api.sliver_exists(slicename):
        raise SliverDoesNotExist(slicename)
    api.nodemanager.ReCreate(slicename)
 
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
    

