import os
import sys
import datetime
import time
import xmlrpclib

from geniserver import *
from excep import *
from misc import *
from config import Config

conf = Config()
basedir = conf.GENI_BASE_DIR + os.sep 
server_basedir = basedir + os.sep + "plc" + os.sep 
agg_hrn = conf.GENI_INTERFACE_HRN

class Aggregate:

    hrn = None
    aggregate_file = None
    components_file = None
    slices_file = None	
    components_ttl = None
    components = []
    slices = []	
    policies = {}
    timestamp = None
    threshold = None	
    server = None
     

    def __init__(self, hrn = agg_hrn, components_ttl = 1):
        self.hrn = hrn
	self.components_file = os.sep.join([server_basedir, 'components', hrn + '.comp'])
	self.slices_file = os.sep.join([server_basedir, 'components', hrn + '.slices'])
	self.timestamp_file = os.sep.join([server_basedir, 'components', hrn + '.timestamp']) 
	self.components_ttl = components_ttl

    def connect(self):
	"""
	Connect to the plc api interface. First attempt to impor thte shell, if that fails
	try to connect to the xmlrpc server.
	"""
	self.auth = {'Username': conf.GENI_PLC_USER,
                     'AuthMethod': 'password',
                     'AuthString': conf.GENI_PLC_PASSWORD}

	try:
	    # try to import PLC.Shell directly
	    sys.path.append(conf.GENI_PLC_SHELL_PATH) 
	    import PLC.Shell
	    self.shell = PLC.Shell.Shell(globals())
	    self.shell.AuthCheck()
	except ImportError:
            # connect to plc api via xmlrpc
	    plc_host = conf.GENI_PLC_HOST
 	    plc_port = conf.GENI_PLC_PORT
	    plc_api_path = conf.GENI_PLC_API_PATH    		     
	    url = "https://%(plc_host)s:%(plc_port)s/%(plc_api_path)s/" % locals()
            self.auth = {'Username': conf.GENI_PLC_USER,
		         'AuthMethod': 'password',
		         'AuthString': conf.GENI_PLC_PASSWORD} 

	    self.shell = xmlrpclib.Server(url, verbose = 0, allow_none = True) 
	    self.shell.AuthCheck(self.auth) 

    def hostname_to_hrn(self, login_base, hostname):
	"""
	Convert hrn to plantelab name.
	"""
        genihostname = "_".join(hostname.split("."))
        return ".".join([self.hrn, login_base, genihostname])

    def slicename_to_hrn(self, slicename):
	"""
	Convert hrn to planetlab name.
	"""
        slicename = slicename.replace("_", ".")
        return ".".join([self.hrn, slicename])

    def refresh_components(self):
	"""
	Update the cached list of nodes and slices.
	"""
	print "refreshing"	
	# resolve component hostnames 
	nodes = self.shell.GetNodes(self.auth, {}, ['hostname', 'site_id'])
	
	# resolve slices
	slices = self.shell.GetSlices(self.auth, {}, ['name', 'site_id'])
   
	# resolve site login_bases
	site_ids = [node['site_id'] for node in nodes]
	sites = self.shell.GetSites(self.auth, site_ids, ['site_id', 'login_base'])
	site_dict = {}
	for site in sites:
	    site_dict[site['site_id']] = site['login_base']

	# convert plc names to geni hrn
	self.components = [self.hostname_to_hrn(site_dict[node['site_id']], node['hostname']) for node in nodes]
	self.slices = [self.slicename_to_hrn(slice['name']) for slice in slices]
		
	# update timestamp and threshold
	self.timestamp = datetime.datetime.now()
	delta = datetime.timedelta(hours=self.components_ttl)
	self.threshold = self.timestamp + delta 
	
	f = open(self.components_file, 'w')
	f.write(str(self.components))
	f.close()
	f = open(self.slices_file, 'w')
	f.write(str(self.slices))
	f.close()
	f = open(self.timestamp_file, 'w')
	f.write(str(self.threshold))
	f.close()
 
    def load_components(self):
	"""
	Read cached list of nodes and slices.
	"""
	print "loading"
	# Read component list from cached file 
	if os.path.exists(self.components_file):
	    f = open(self.components_file, 'r')
	    self.components = eval(f.read())
	    f.close()
	
	if os.path.exists(self.slices_file):
            f = open(self.components_file, 'r')
            self.slices = eval(f.read())
            f.close()

	time_format = "%Y-%m-%d %H:%M:%S"
	if os.path.exists(self.timestamp_file):
	    f = open(self.timestamp_file, 'r')
	    timestamp = str(f.read()).split(".")[0]
	    self.timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestamp, time_format)))
	    delta = datetime.timedelta(hours=self.components_ttl)
            self.threshold = self.timestamp + delta
	    f.close()	

    def get_components(self):
	"""
	Return a list of components at this aggregate.
	"""
	# Reload components list
	now = datetime.datetime.now()
	#self.load_components()
	if not self.threshold or not self.timestamp or now > self.threshold:
	    self.refresh_components()
	elif now < self.threshold and not self.components: 
	    self.load_components()
	return self.components
   
     
    def get_slices(self):
	"""
	Return a list of instnatiated slices at this aggregate.
	"""
	now = datetime.datetime.now()
	#self.load_components()
	if not self.threshold or not self.timestamp or now > self.threshold:
	    self.refresh_components()
	elif now < self.threshold and not self.slices:
	    self.load_components()
	return self.slices

    def get_rspec(self, hrn, type):
	#rspec = Rspec()
	if type in ['node']:
	    nodes = self.shell.GetNodes(self.auth)
	elif type in ['slice']:
	    slices = self.shell.GetSlices(self.auth)
	elif type in ['aggregate']:
	    pass

    get_slice_rspec = get_rspec(hrn, 'slice')
    get_node_rspec = get_rspec(hrn, 'node')
    get_aggregate_rspec = get_rpsec(hrn, 'aggregate')		

    def get_resources(self, slice_hrn):
	"""
	Return the current rspec for the specified slice.
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	rspec = self.get_slice_rspec(slicename)
        
	return rspec
 
    def create_slice(self, slice_hrn, rspec):
	"""
	Instantiate the specified slice according to whats defined in the rspec.
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	#spec = Rspec(rspec)
	#components = spec.components()
	#shell.AddSliceToNodes(self.auth, slicename, components)
	return 1
	
    def delete_slice_(self, slice_hrn):
	"""
	Remove this slice from all components it was previouly associated with and 
	free up the resources it was using.
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	rspec = self.get_resources(slice_hrn)
	components = rspec.components()
	shell.DeleteSliceFromNodes(self.auth, slicename, components)
	return 1

    def start_slice(self, slice_hrn):
	"""
	Stop the slice at plc.
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	slices = self.shell.GetSlices(self.auth, {'name': slicename}, ['slice_id'])
	if not slices:
	    raise RecordNotFound(slice_hrn)
	slice_id = slices[0]
	atrribtes = self.shell.GetSliceAttributes({'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
	attribute_id = attreibutes[0] 
	self.shell.UpdateSliceAttribute(self.auth, attribute_id, "1" })
	return 1

    def stop_slice(self, slice_hrn):
	"""
	Stop the slice at plc
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	slices = self.shell.GetSlices(self.auth, {'name': slicename}, ['slice_id'])
        if not slices:
            raise RecordNotFound(slice_hrn)
        slice_id = slices[0]
        atrribtes = self.shell.GetSliceAttributes({'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attreibutes[0]
	self.shell.UpdateSliceAttribute(self.auth, attribute_id, "0"})
	return 1

    def reset_slice(self, slice_hrn):
	"""
	Reset the slice
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	return 1

    def get_policy(self):
	"""
	Return this aggregates policy as an rspec
	"""
	rspec = get_aggregate_rspec(self.hrn):
	return rspec
    	
	 		
