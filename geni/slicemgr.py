import os
import sys
import datetime
import time

from geni.util.geniserver import *
from geni.util.geniclient import *
from geni.util.cert import *
from geni.util.credential import Credential
from geni.util.trustedroot import *
from geni.util.excep import *
from geni.util.misc import *
from geni.util.config import Config
from geni.util.rspec import Rspec
from geni.util.specdict import *
from geni.util.storage import SimpleStorage, XmlStorage

class SliceMgr(GeniServer):

    hrn = None
    nodes_ttl = None
    nodes = None
    slices = None
    policy = None
    aggregates = None
    timestamp = None
    threshold = None    
    shell = None
    registry = None
    key_file = None
    cert_file = None
    credential = None 
  
    ##
    # Create a new slice manager object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)     

    def __init__(self, ip, port, key_file, cert_file, config = "/usr/share/geniwrapper/geni/util/geni_config"):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.key_file = key_file
        self.cert_file = cert_file
        self.config = Config(config)
        self.basedir = self.config.GENI_BASE_DIR + os.sep
        self.server_basedir = self.basedir + os.sep + "geni" + os.sep
        self.hrn = self.config.GENI_INTERFACE_HRN    
        self.time_format = "%Y-%m-%d %H:%M:%S"
        
        # Get list of aggregates this sm talks to
        aggregates_file = self.server_basedir + os.sep + 'aggregates.xml'
        self.aggregate_info = XmlStorage(aggregates_file, {'aggregates': {'aggregate': []}} )
        self.aggregate_info.load()
        
        # Get cached list of nodes (rspec) 
        nodes_file = os.sep.join([self.server_basedir, 'smgr.' + self.hrn + '.components'])
        self.nodes = SimpleStorage(nodes_file)
        self.nodes.load()
        
        # Get cacheds slice states
        slices_file = os.sep.join([self.server_basedir, 'smgr.' + self.hrn + '.slices'])
        self.slices = SimpleStorage(slices_file)
        self.slices.load()

        # Get the policy
        policy_file = os.sep.join([self.server_basedir, 'smgr.' + self.hrn + '.policy'])
        self.policy = SimpleStorage(policy_file, {'whitelist': [], 'blacklist': []})
        self.policy.load()

        # How long before we refresh nodes cache  
        self.nodes_ttl = 1

        self.connectRegistry()
        self.loadCredential()
        self.connectAggregates()


    def loadCredential(self):
        """
        Attempt to load credential from file if it exists. If it doesnt get
        credential from registry.
        """
        
        # see if this file exists
        ma_cred_filename = self.server_basedir + os.sep + "smgr." + self.hrn + ".sa.cred"
        try:
            self.credential = Credential(filename = ma_cred_filename)
        except IOError:
            self.credential = self.getCrednetialFromRegistry()
            
        
    def getCredentialFromRegistry(self):
        """
        Get our current credential from the registry.
        """
        # get self credential
        self_cred_filename = self.server_basedir + os.sep + "smgr." + self.hrn + ".cred"
        self_cred = self.registry.get_credential(None, 'ma', self.hrn)
        self_cred.save_to_file(self_cred_filename, save_parents=True)

        # get ma credential
        ma_cred_filename = self.server_basedir + os.sep + "smgr." + self.hrn + ".sa.cred"
        ma_cred = self.registry.get_credential(self_cred, 'sa', self.hrn)
        ma_cred.save_to_file(ma_cred_filename, save_parents=True)
        return ma_cred        

    def connectRegistry(self):
        """
        Connect to the registry
        """
        # connect to registry using GeniClient
        address = self.config.GENI_REGISTRY_HOSTNAME
        port = self.config.GENI_REGISTRY_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        self.registry = GeniClient(url, self.key_file, self.cert_file)

    def connectAggregates(self):
        """
        Get info about the aggregates available to us from file and create 
        an xmlrpc connection to each. If any info is invalid, skip it. 
        """
        self.aggregates = {} 
        aggregates = self.aggregate_info['aggregates']['aggregate']
        if isinstance(aggregates, dict):
            aggregates = [aggregates]
        if isinstance(aggregates, list):
            for aggregate in aggregates:         
                # create xmlrpc connection using GeniClient
                hrn, address, port = aggregate['hrn'], aggregate['addr'], aggregate['port']
                url = 'http://%(address)s:%(port)s' % locals()
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
    
        # convert and threshold to ints
        if self.nodes.has_key('timestamp') and self.nodes['timestamp']:
            hr_timestamp = self.nodes['timestamp']
            timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(hr_timestamp, self.time_format)))
            hr_threshold = self.nodes['threshold']
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.strptime(hr_threshold, self.time_format)))
        else:
            timestamp = datetime.datetime.now()
            hr_timestamp = timestamp.strftime(self.time_format)
            delta = datetime.timedelta(hours=self.nodes_ttl)
            threshold = timestamp + delta
            hr_threshold = threshold.strftime(self.time_format)

        start_time = int(timestamp.strftime("%s"))
        end_time = int(threshold.strftime("%s"))
        duration = end_time - start_time

        aggregates = self.aggregates.keys()
        rspecs = {}
        networks = []
        rspec = Rspec()
        for aggregate in aggregates:
            try:
                # get the rspec from the aggregate
                agg_rspec = self.aggregates[aggregate].list_nodes(self.credential)
                # extract the netspec from each aggregates rspec
                rspec.parseString(agg_rspec)
                networks.extend([{'NetSpec': rspec.getDictsByTagName('NetSpec')}])
            except:
                # XX print out to some error log
                print "Error calling list nodes at aggregate %s" % aggregate
                raise    
  
        # create the rspec dict
        resources = {'networks': networks, 'start_time': start_time, 'duration': duration}
        resourceDict = {'Rspec': resources} 
        # convert rspec dict to xml
        rspec.parseDict(resourceDict)
       
        # filter according to policy
        rspec.filter('NodeSpec', 'name', blacklist=self.policy['blacklist'], whitelist=self.policy['whitelist'])

        # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.time_format)
        delta = datetime.timedelta(hours=self.nodes_ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.time_format)
        
        nodedict = {'rspec': rspec.toxml(),
                    'timestamp': hr_timestamp,
                    'threshold':  hr_threshold}

        self.nodes = SimpleStorage(self.nodes.db_filename, nodedict)
        self.nodes.write()

    def load_policy(self):
        """
        Read the list of blacklisted and whitelisted nodes.
        """
        self.policy.load()
 
    def load_slices(self):
        """
        Read current slice instantiation states.
        """
        self.slices.load()


    def getNodes(self, format = 'rspec'):
        """
        Return a list of components managed by this slice manager.
        """
        # Reload components list
        if not self.nodes.has_key('threshold') or not self.nodes['threshold'] or not self.nodes.has_key('timestamp') or not self.nodes['timestamp']:
            self.refresh_components()
        else:
            now = datetime.datetime.now()
            threshold = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.nodes['threshold'], self.time_format)))
            if  now > threshold:
                self.refresh_components()
        return self.nodes[format]
   
     
    def getSlices(self):
        """
        Return a list of instnatiated managed by this slice manager.
        """
        slice_hrns = []
        for aggregate in self.aggregates:
            try:
                slices = self.aggregates[aggregate].list_slices(self.credential)
                slice_hrns.extend(slices)
            except:
                raise
                # print to some error log
                pass

        return slice_hrns

    def getResources(self, slice_hrn):
        """
        Return the current rspec for the specified slice.
        """

        # request this slices state from all known aggregates
        rspec = Rspec()
        rspecdicts = []
        networks = []
        for hrn in self.aggregates.keys():
            # check if the slice has resources at this hrn
            slice_resources = self.aggregates[hrn].get_resources(self.credential, slice_hrn)
            rspec.parseString(slice_resources)
            networks.extend({'NetSpec': rspec.getDictsByTagName('NetSpec')})
            
        # merge all these rspecs into one
        start_time = int(datetime.datetime.now().strftime("%s"))
        end_time = start_time
        duration = end_time - start_time
    
        resources = {'networks': networks, 'start_time': start_time, 'duration': duration}
        resourceDict = {'Rspec': resources}
        # convert rspec dict to xml
        rspec.parseDict(resourceDict)
        # save this slices resources
        #self.slices[slice_hrn] = rspec.toxml()
        #self.slices.write()
         
        return rspec.toxml()
 
    def createSlice(self, cred, slice_hrn, rspec):
        """
        Instantiate the specified slice according to whats defined in the rspec.
        """

        # save slice state locally
        # we can assume that spec object has been validated so its safer to
        # save this instead of the unvalidated rspec the user gave us
        rspec = Rspec()
        tempspec = Rspec()
        rspec.parseString(rspec)

        self.slices[slice_hrn] = rspec.toxml()
        self.slices.write()

        # extract network list from the rspec and create a separate
        # rspec for each network
        slicename = self.hrn_to_plcslicename(slice_hrn)
        specDict = rspec.toDict()
        start_time = specDict['start_time']
        end_time = specDict['end_time']

        rspecs = {}
        # only attempt to extract information about the aggregates we know about
        for hrn in self.aggregates.keys():
            netspec = spec.getDictByTagNameValue('NetSpec', hrn)
            if netspec:
                # creat a plc dict 
                resources = {'start_time': star_time, 'end_time': end_time, 'networks': netspec}
                resourceDict = {'Rspec': resources}
                tempspec.parseDict(resourceDict)
                rspecs[hrn] = tempspec.toxml()

        # notify the aggregates
        for hrn in self.rspecs.keys():
            self.aggregates[hrn].createSlice(self.credential, rspecs[hrn])
            
        return 1

    def updateSlice(self, slice_hrn, rspec, attributes = []):
        """
        Update the specifed slice
        """
        self.create_slice(slice_hrn, rspec, attributes)
    
    def deleteSlice_(self, slice_hrn):
        """
        Remove this slice from all components it was previouly associated with and 
        free up the resources it was using.
        """
        # XX need to get the correct credential
        cred = self.credential
        
        if self.slices.has_key(slice_hrn):
            self.slices.pop(slice_hrn)
            self.slices.write()

        for hrn in self.aggregates.keys():
            self.aggregates[hrn].deleteSlice(cred, slice_hrn)

        return 1

    def startSlice(self, slice_hrn):
        """
        Stop the slice at plc.
        """
        cred = self.credential

        for hrn in self.aggregates.keys():
            self.aggregates[hrn].startSlice(cred, slice_hrn)
        return 1

    def stopSlice(self, slice_hrn):
        """
        Stop the slice at plc
        """
        cred = self.credential
        for hrn in self.aggregates.keys():
            self.aggregates[hrn].startSlice(cred, slice_hrn)
        return 1

    def resetSlice(self, slice_hrn):
        """
        Reset the slice
        """
        # XX not yet implemented
        return 1

    def getPolicy(self):
        """
        Return the policy of this slice manager.
        """
    
        return self.policy
        
    

##############################
## Server methods here for now
##############################

    def list_nodes(self, cred):
        self.decode_authentication(cred, 'listnodes')
        return self.getNodes()

    def list_slices(self, cred):
        self.decode_authentication(cred, 'listslices')
        return self.getSlices()

    def get_resources(self, cred, hrn):
        self.decode_authentication(cred, 'listnodes')
        return self.getResources(hrn)

    def get_ticket(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'getticket')
        return self.getTicket(hrn, rspec)

    def get_policy(self, cred):
        self.decode_authentication(cred, 'getpolicy')
        return self.getPolicy()

    def create_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'creatslice')
        return self.createSlice(cred, hrn, rspec)

    def delete_slice(self, cred, hrn):
        self.decode_authentication(cred, 'deleteslice')
        return self.deleteSlice(hrn)

    def start_slice(self, cred, hrn):
        self.decode_authentication(cred, 'startslice')
        return self.startSlice(hrn)

    def stop_slice(self, cred, hrn):
        self.decode_authentication(cred, 'stopslice')
        return self.stopSlice(hrn)

    def reset_slice(self, cred, hrn):
        self.decode_authentication(cred, 'resetslice')
        return self.resetSlice(hrn)

    def register_functions(self):
        GeniServer.register_functions(self)

        # Aggregate interface methods
        self.server.register_function(self.list_nodes)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.get_resources)
        self.server.register_function(self.get_policy)
        self.server.register_function(self.create_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.reset_slice)
              
