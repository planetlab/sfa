import os
import sys
import datetime
import time

from util.geniserver import *
from util.geniclient import *
from util.cert import *
from util.trustedroot import *
from util.excep import *
from util.misc import *
from util.config import Config

class SliceMgr(GeniServer):

    hrn = None
    key_file = None
    cert_file = None
    components_file = None
    slices_file = None	
    components_ttl = None
    components = []
    slices = []	
    policy = {}
    timestamp = None
    threshold = None	
    shell = None
    aggregates = {}
	
  
    ##
    # Create a new slice manager object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     

    def __init__(self, ip, port, key_file, cert_file, config = "/usr/share/geniwrapper/util/geni_config"):
        GeniServer.__init__(ip, port, key_file, cert_file)
	self.key_file = key_file
	self.cert_file = cert_file
	self.conf = Config(config)
        basedir = self.conf.GENI_BASE_DIR + os.sep
        server_basedir = basedir + os.sep + "plc" + os.sep
	self.hrn = conf.GENI_INTERFACE_HRN
	
	# Get list of aggregates this sm talks to
	aggregates_file = server_basedir + os.sep + 'aggregates'
	self.load_aggregates(aggregates_file) 
	self.components_file = os.sep.join([server_basedir, 'components', 'slicemgr.' + hrn + '.comp'])
	self.slices_file = os.sep.join([server_basedir, 'components', 'slicemgr' + hrn + '.slices'])
	self.timestamp_file = os.sep.join([server_basedir, 'components', 'slicemgr' + hrn + '.timestamp']) 
	self.components_ttl = components_ttl
	self.policy['whitelist'] = []
        self.policy['blacklist'] = []
	self.connect()

    def load_aggregates(self, aggregates_file):
	"""
	Get info about the aggregates available to us from file and create 
        an xmlrpc connection to each. If any info is invalid, skip it. 
	"""
	lines = []
        try:
	    f = open(aggregates_file, 'r')
	    lines = f.readlines()
	    f.close()
	except: raise 
	
	for line in lines:
	    # Skip comments
	    if line.strip.startswith("#"):
		continue
	    agg_info = line.split("\t").split(" ")
	    
	    # skip invalid info
	    if len(agg_info) != 3:
		continue

	    # create xmlrpc connection using GeniClient
	    hrn, address, port = agg_info[0], agg_info[1], agg_info[2]
	    url = 'https://%(address)s:%(port)s' % locals()
	    self.aggregates[hrn] = GeniClient(url, self.key_file, self.cert_file)


    def item_hrns(self, items):
	"""
	Take a list of items (components or slices) and return a dictionary where
	the key is the authoritative hrn and the value is a list of items at that 
	hrn.
	"""
	item_hrns = {}
	agg_hrns = self.aggregates.keys()
	for agg_hrn in agg_hrns:
	    item_hrns[agg_hrn] = []
	for item in items:
	    for agg_hrn in agg_hrns:
		if item.startswith(agg_hrn):
		   item_hrns[agg_hrn] = item

	return item_hrns	
		 	

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
	Update the cached list of nodes.
	"""
	print "refreshing"
	
	aggregates = self.aggregates.keys()
	all_nodes = []
	all_slices = []
	for aggregate in aggregates:
	    try:
		# resolve components hostnames
	        nodes = self.aggregates[aggregate].get_components()
		all_nodes.extend(nodes)	
		# update timestamp and threshold
		self.timestamp = datetime.datetime.now()
		delta = datetime.timedelta(hours=self.components_ttl)
		self.threshold = self.timestamp + delta 
	    except:
		# XX print out to some error log
		pass	
   
	self.components = all_nodes
	f = open(self.components_file, 'w')
	f.write(str(self.components))
	f.close()
	f = open(self.timestamp_file, 'w')
	f.write(str(self.threshold))
	f.close()
 
    def load_components(self):
	"""
	Read cached list of nodes and slices.
	"""
	print "loading nodes"
	# Read component list from cached file 
	if os.path.exists(self.components_file):
	    f = open(self.components_file, 'r')
	    self.components = eval(f.read())
	    f.close()
	
	time_format = "%Y-%m-%d %H:%M:%S"
	if os.path.exists(self.timestamp_file):
	    f = open(self.timestamp_file, 'r')
	    timestamp = str(f.read()).split(".")[0]
	    self.timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestamp, time_format)))
	    delta = datetime.timedelta(hours=self.components_ttl)
            self.threshold = self.timestamp + delta
	    f.close()

    def load_policy(self):
        """
        Read the list of blacklisted and whitelisted nodes.
        """
        whitelist = []
        blacklist = []
        if os.path.exists(self.whitelist_file):
            f = open(self.whitelist_file, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                line = line.strip().replace(" ", "").replace("\n", "")
                whitelist.extend(line.split(","))


        if os.path.exists(self.blacklist_file):
            f = open(self.blacklist_file, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                line = line.strip().replace(" ", "").replace("\n", "")
                blacklist.extend(line.split(","))

        self.policy['whitelist'] = whitelist
        self.policy['blacklist'] = blacklist
 
    def load_slices(self):
	"""
 	Read current slice instantiation states.
	"""
	print "loading slices"
	if os.path.exists(self.slices_file):
            f = open(self.components_file, 'r')
            self.slices = eval(f.read())
            f.close()	

    def write_slices(self):
        """
        Write current slice instantiations to file.
        """
        print "writing slices"
        f = open(self.slices_file, 'w')
        f.write(str(self.slices))
        f.close()


    def get_components(self):
	"""
	Return a list of components managed by this slice manager.
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
	Return a list of instnatiated managed by this slice manager.
	"""
	now = datetime.datetime.now()
	#self.load_components()
	if not self.threshold or not self.timestamp or now > self.threshold:
	    self.refresh_components()
	elif now < self.threshold and not self.slices:
	    self.load_components()
	return self.slices

    def get_slivers(self, hrn):
	"""
	Return the list of slices instantiated at the specified component.
	"""

	# hrn is assumed to be a component hrn
	if hrn not in self.slices:
	    raise RecordNotFound(hrn)
	
	return self.slices[hrn]

    def get_rspec(self, hrn, type):
	#rspec = Rspec()
	if type in ['node']:
	    nodes = self.shell.GetNodes(self.auth)
	elif type in ['slice']:
	    slices = self.shell.GetSlices(self.auth)
	elif type in ['aggregate']:
	    pass

    def get_resources(self, slice_hrn):
	"""
	Return the current rspec for the specified slice.
	"""
	slicename = hrn_to_plcslicename(slice_hrn)
	rspec = self.get_rspec(slicenamem, 'slice' )
        
	return rspec
 
    def create_slice(self, slice_hrn, rspec, attributes):
	"""
	Instantiate the specified slice according to whats defined in the rspec.
	"""
	slicename = self.hrn_to_plcslicename(slice_hrn)
	#spec = Rspec(rspec)
	node_hrns = []
	#for netspec in spec['networks]:
	#    networkname = netspec['name']
	#    nodespec = spec['networks']['nodes']
	#    nodes = [nspec['name'] for nspec in nodespec]
	#    node_hrns = [networkname + node for node in nodes]
	#    
	self.db.AddSliceToNodes(slice_hrn, node_hrns)
	return 1
	
    def delete_slice_(self, slice_hrn):
	"""
	Remove this slice from all components it was previouly associated with and 
	free up the resources it was using.
	"""
	self.db.DeleteSliceFromNodes(self.auth, slicename, self.components)
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
	self.shell.UpdateSliceAttribute(self.auth, attribute_id, "1" )
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
	self.shell.UpdateSliceAttribute(self.auth, attribute_id, "0")
	return 1

    def reset_slice(self, slice_hrn):
	"""
	Reset the slice
	"""
	slicename = self.hrn_to_plcslicename(slice_hrn)
	return 1

    def get_policy(self):
	"""
	Return the policy of this slice manager.
	"""
	
	return self.policy
    	
	

##############################
## Server methods here for now
##############################

    def nodes(self):
        return self..get_components()

    def slices(self):
        return self.get_slices()

    def resources(self, cred, hrn):
        self.decode_authentication(cred, 'info')
        self.verify_object_belongs_to_me(hrn)

        return self.get_resources(hrn)

    def create(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'embed')
        self.verify_object_belongs_to_me(hrn, rspec)
        return self.create(hrn)

    def delete(self, cred, hrn):
        self.decode_authentication(cred, 'embed')
        self.verify_object_belongs_to_me(hrn)
        return self.delete_slice(hrn)

    def start(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.start(hrn)

    def stop(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.stop(hrn)

    def reset(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.reset(hrn)

    def policy(self, cred):
        self.decode_authentication(cred, 'info')
        return self.get_policy()

    def register_functions(self):
        GeniServer.register_functions(self)

        # Aggregate interface methods
        self.server.register_function(self.components)
        self.server.register_function(self.slices)
        self.server.register_function(self.resources)
        self.server.register_function(self.create)
        self.server.register_function(self.delete)
        self.server.register_function(self.start)
        self.server.register_function(self.stop)
        self.server.register_function(self.reset)
        self.server.register_function(self.policy)
      		
