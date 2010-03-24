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

def GetVersion():
    version = {}
    version['geni_api'] = 1
    version['geni_stitching'] = False
    return version

def ListResources(creds, options):
    return "Hello World"
