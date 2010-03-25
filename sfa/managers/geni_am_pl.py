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
from sfa.util.record import *
from sfa.util.sfaticket import SfaTicket
from sfa.server.registry import Registries
from sfa.util.debug import log
from sfa.plc.slices import Slices
import sfa.plc.peers as peers
from sfa.plc.api import SfaAPI
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

    hrn = None
    if options.has_key('geni_slice_urn'):
        xrn = options['geni_slice_urn']
        hrn, type = urn_to_hrn(xrn)


    rspec = manager.get_rspec(api, hrn, None)
    #outgoing_rules = SFATablesRules('OUTGOING')
    
    if options.has_key('geni_compressed') and options['geni_compressed'] == True:
        rspec = zlib.compress(rspec).encode('base64')
        
    return rspec


