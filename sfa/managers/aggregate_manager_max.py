from sfa.util.xrn import urn_to_hrn, hrn_to_urn, get_authority
from sfa.util.plxrn import hrn_to_pl_slicename
from sfa.util.plxrn import hrn_to_pl_slicename
from sfa.util.rspec import RSpec
from sfa.util.sfalogging import sfa_logger
from sfa.util.config import Config
from sfa.managers.aggregate_manager_pl import GetVersion, __get_registry_objects
from sfa.plc.slices import Slices
import os
import time

RSPEC_TMP_FILE_PREFIX = "/tmp/max_rspec"

# execute shell command and return both exit code and text output
def shell_execute(cmd, timeout):
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    pipe = os.popen(cmd + ' 2>&1', 'r')
    text = ''
    while timeout:
        line = pipe.read()
        text += line
        time.sleep(1)
        timeout = timeout-1
    code = pipe.close()
    if code is None: code = 0
    if text[-1:] == '\n': text = text[:-1]
    return code, text

"""
 call AM API client with command like in the following example:
 cd aggregate_client; java -classpath AggregateWS-client-api.jar:lib/* \
      net.geni.aggregate.client.examples.CreateSliceNetworkClient \
      ./repo https://geni:8443/axis2/services/AggregateGENI \
      ... params ...
"""

def call_am_apiclient(client_app, params, timeout):
    (client_path, am_url) = Config().get_max_aggrMgr_info()
    sys_cmd = "cd " + client_path + "; java -classpath AggregateWS-client-api.jar:lib/* net.geni.aggregate.client.examples." + client_app + " ./repo " + am_url + " " + ' '.join(params)
    ret = shell_execute(sys_cmd, timeout)
    sfa_logger().debug("shell_execute cmd: %s returns %s" % (sys_cmd, ret))
# save request RSpec xml content to a tmp file
def save_rspec_to_file(rspec):
    path = RSPEC_TMP_FILE_PREFIX + "_" + time.strftime('%Y%m%dT%H:%M:%S', time.gmtime(time.time())) +".xml"
    file = open(path, "w")
    file.write(rspec)
    file.close()
    return path

# get stripped down slice id/name plc:maxpl:xi_slice1 --> xi_slice1
def get_short_slice_id(cred, hrn):
    if hrn == None:
        return None
    slice_id = hrn[hrn.rfind('+')+1:]
    if slice_id == None:
        slice_id = hrn[hrn.rfind(':')+1:]
    if slice_id == None:
       return hrn
       pass
    return str(slice_id)

# extract xml 
def get_xml_by_tag(text, tag):
    indx1 = text.find('<'+tag)
    indx2 = text.find('/'+tag+'>')
    xml = None
    if indx1!=-1 and indx2>indx1:
        xml = text[indx1:indx2+len(tag)+2]
    return xml

def prepare_slice(api, xrn, users):
    reg_objects = __get_registry_objects(slice_xrn, creds, users)
    (hrn, type) = urn_to_hrn(slice_xrn)
    slices = Slices(api)
    peer = slices.get_peer(hrn)
    sfa_peer = slices.get_sfa_peer(hrn)
    registry = api.registries[api.hrn]
    credential = api.getCredential()
    (site_id, remote_site_id) = slices.verify_site(registry, credential, hrn, peer, sfa_peer, reg_objects)
    slices.verify_slice(registry, credential, hrn, site_id, remote_site_id, peer, sfa_peer, reg_objects)

def create_slice(api, xrn, cred, rspec, users):
    indx1 = rspec.find("<RSpec")
    indx2 = rspec.find("</RSpec>")
    if indx1 > -1 and indx2 > indx1:
        rspec = rspec[indx1+len("<RSpec type=\"SFA\">"):indx2-1]
    rspec_path = save_rspec_to_file(rspec)
    prepare_slice(api, xrn, users)
    (ret, output) = call_am_apiclient("CreateSliceNetworkClient", [rspec_path,], 3)
    # parse output ?
    rspec = "<RSpec type=\"SFA\"> Done! </RSpec>"
def delete_slice(api, xrn, cred):
    slice_id = get_short_slice_id(cred, xrn)
    (ret, output) = call_am_apiclient("DeleteSliceNetworkClient", [slice_id,], 3)
    # parse output ?
def get_rspec(api, cred, options):
    #geni_slice_urn: urn:publicid:IDN+plc:maxpl+slice+xi_rspec_test1
    urn = options.get('geni_slice_urn')
    slice_id = get_short_slice_id(cred, urn)
    if slice_id == None:
        (ret, output) = call_am_apiclient("GetResourceTopology", ['all', '\"\"'], 5)
        (ret, output) = call_am_apiclient("GetResourceTopology", ['all', slice_id,], 5)
    # parse output into rspec XML
    if output.find("No resouce found") > 0:
        rspec = "<RSpec type=\"SFA\"> <Fault>No resource found</Fault> </RSpec>"
    else:
        comp_rspec = get_xml_by_tag(output, 'computeResource')
        sfa_logger().debug("#### computeResource %s" % comp_rspec)
        topo_rspec = get_xml_by_tag(output, 'topology')
        sfa_logger().debug("#### topology %s" % topo_rspec)
        rspec = "<RSpec type=\"SFA\"> <network name=\"" + Config().get_interface_hrn() + "\">";
        if comp_rspec != None:
            rspec = rspec + get_xml_by_tag(output, 'computeResource')
        if topo_rspec != None:
            rspec = rspec + get_xml_by_tag(output, 'topology')
        rspec = rspec + "</network> </RSpec>"

    return (rspec)

def start_slice(api, xrn, cred):
    # service not supported
    return None

def stop_slice(api, xrn, cred):
    # service not supported
    return None

def reset_slices(api, xrn):
    # service not supported
    return None

"""
Returns the request context required by sfatables. At some point, this mechanism should be changed
to refer to "contexts", which is the information that sfatables is requesting. But for now, we just
return the basic information needed in a dict.
"""
def fetch_context(slice_hrn, user_hrn, contexts):
    base_context = {'sfa':{'user':{'hrn':user_hrn}}}
    return base_context
    api = SfaAPI()
    create_slice(api, "plc.maxpl.test000", None, rspec_xml, None)

