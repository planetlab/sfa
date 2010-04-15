from sfa.util.namespace import *
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *

from sfa.util.record import *

from sfa.plc.slices import *
from sfa.util.sfalogging import *
import zlib

def GetVersion():
    version = {}
    version['geni_api'] = 1
    version['geni_stitching'] = False
    return version


def ListResources(api, creds, options):
    manager_base = 'sfa.managers'
    mgr_type = 'pl'
    manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
    manager = __import__(manager_module, fromlist=[manager_base])

    xrn = None
    if options.has_key('geni_slice_urn'):
        xrn = options['geni_slice_urn']
        api.logger.info(xrn)


    rspec = manager.get_rspec(api, xrn, None)
    #outgoing_rules = SFATablesRules('OUTGOING')
    
    if options.has_key('geni_compressed') and options['geni_compressed'] == True:
        rspec = zlib.compress(rspec).encode('base64')
        
    return rspec


def CreateSliver(api, slice_xrn, creds, rspec):
    manager_base = 'sfa.managers'
    mgr_type = 'pl'
    manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
    manager = __import__(manager_module, fromlist=[manager_base])

    allocated = manager.create_slice(api, slice_xrn, rspec)
    return allocated

def DeleteSliver(api, slice_xrn, creds):
    manager_base = 'sfa.managers'
    mgr_type = 'pl'
    manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
    manager = __import__(manager_module, fromlist=[manager_base])

    allocated = manager.delete_slice(api, slice_xrn)
    return allocated
    