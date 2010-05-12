from sfa.util.namespace import *
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *

from sfa.util.record import *

from sfa.plc.slices import *
from sfa.util.sfalogging import *
from sfa.util.record import SfaRecord
from lxml import etree
from StringIO import StringIO

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
    
    
    # Filter out those objects that aren't allocated
    if xrn:
        tree = etree.parse(StringIO(rspec))    
        used_nodes = [sliver.getparent() for sliver in tree.iterfind("./network/site/node/sliver")]
        used_sites = [node.getparent() for node in used_nodes]
        for node in tree.iterfind("./network/site/node"):
            if node not in used_nodes:
                parent = node.getparent()
                parent.remove(node)
        
        # Remove unused sites
        for site in tree.iterfind("./network/site"):
            if site not in used_sites:
                parent = site.getparent()
                parent.remove(site)
        rspec = etree.tostring(tree)

    return rspec


def CreateSliver(api, slice_xrn, creds, rspec):
    reg_objects = {}
    hrn, type = urn_to_hrn(slice_xrn)
    
    hrn_auth = get_authority(hrn)
    
    #site = SfaRecord(hrn=hrn_auth, type='authority')
    site = {}
    site['site_id'] = 0
    site['name'] = 'geni.%s' % slice_xrn
    site['enabled'] = True
    site['max_slices'] = 100
    site['login_base'] = get_leaf(hrn_auth)
    site['abbreviated_name'] = hrn
    site['max_slivers'] = 1000
    
    reg_objects['site'] = site
    
    manager_base = 'sfa.managers'
    mgr_type = 'pl'
    manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
    manager = __import__(manager_module, fromlist=[manager_base])

    allocated = manager.create_slice(api, slice_xrn, rspec, reg_objects)
    
    return allocated

def DeleteSliver(api, slice_xrn, creds):
    manager_base = 'sfa.managers'
    mgr_type = 'pl'
    manager_module = manager_base + ".aggregate_manager_%s" % mgr_type
    manager = __import__(manager_module, fromlist=[manager_base])

    allocated = manager.delete_slice(api, slice_xrn)
    return allocated

def SliverStatus(api, slice_xrn, creds):
    result = {}
    result['geni_urn'] = slice_xrn
    result['geni_status'] = 'unknown'
    result['geni_resources'] = {}
    return result

def RenewSliver(api, slice_xrn, creds, renew_time):
    return False

def Shutdown(api, slice_xrn, creds):
    return False

