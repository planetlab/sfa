import os
import sys
import datetime
import time
import xmlrpclib

from geni.util.geniserver import GeniServer
from geni.util.geniclient import *
from geni.util.cert import Keypair, Certificate
from geni.util.credential import Credential
from geni.util.trustedroot import TrustedRootList
from geni.util.excep import *
from geni.util.misc import *
from geni.util.config import Config
from geni.util.rspec import Rspec
from geni.util.specdict import *
from geni.util.storage import SimpleStorage

class Aggregate(GeniServer):

    hrn = None
    nodes_ttl = None
    nodes = None
    slices = None 
    policy = None
    timestamp = None
    threshold = None    
    shell = None
    registry = None
    key_file = None
    cert_file = None
    credential = None
  
    ##
    # Create a new aggregate object.
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
        
        nodes_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.components'])
        self.nodes = SimpleStorage(nodes_file)
        self.nodes.load()
       
        slices_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.slices'])
        self.slices = SimpleStorage(slices_file)
        self.slices.load()
 
        policy_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.policy'])
        self.policy = SimpleStorage(policy_file, {'whitelist': [], 'blacklist': []})
        self.policy.load()
        
        timestamp_file = os.sep.join([self.server_basedir, 'agg.' + self.hrn + '.timestamp']) 
        self.timestamp = SimpleStorage(timestamp_file)

        self.nodes_ttl = 1

        self.connectPLC()
        self.connectRegistry()
        self.loadCredential()

    def connectRegistry(self):
        """
        Connect to the registry
        """
        # connect to registry using GeniClient
        address = self.config.GENI_REGISTRY_HOSTNAME
        port = self.config.GENI_REGISTRY_PORT
        url = 'https://%(address)s:%(port)s' % locals()
        self.registry = GeniClient(url, self.key_file, self.cert_file)

    
    def connectPLC(self):
        """
        Connect to the plc api interface. First attempt to impor thte shell, if that fails
        try to connect to the xmlrpc server.
        """
        self.auth = {'Username': self.config.GENI_PLC_USER,
                     'AuthMethod': 'password',
                     'AuthString': self.config.GENI_PLC_PASSWORD}

        try:
           # try to import PLC.Shell directly
            sys.path.append(self.config.GENI_PLC_SHELL_PATH) 
            import PLC.Shell
            self.shell = PLC.Shell.Shell(globals())
            self.shell.AuthCheck()
        except ImportError:
            # connect to plc api via xmlrpc
            plc_host = self.config.GENI_PLC_HOST
            plc_port = self.config.GENI_PLC_PORT
            plc_api_path = self.config.GENI_PLC_API_PATH                 
            url = "https://%(plc_host)s:%(plc_port)s/%(plc_api_path)s/" % locals()
            self.auth = {'Username': self.config.GENI_PLC_USER,
                 'AuthMethod': 'password',
                 'AuthString': self.config.GENI_PLC_PASSWORD} 

            self.shell = xmlrpclib.Server(url, verbose = 0, allow_none = True) 
            self.shell.AuthCheck(self.auth)

    def loadCredential(self):
        """
        Attempt to load credential from file if it exists. If it doesnt get 
        credential from registry.
        """ 

        self_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".cred"
        ma_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".ma.cred"
        
        # see if this file exists
        try:
            cred = Credential(filename = ma_cred_filename)
            self.credential = cred.save_to_string()
        except IOError:
            # get self credential
            #self_cred = self.registry.get_credential(None, 'ma', self.hrn)
            #self_credential = Credential(string = self_cred)
            #self_credential.save_to_file(self_cred_filename)

            # get ma credential
            #ma_cred = self.registry.get_gredential(self_cred)
            #ma_credential = Credential(string = ma_cred)
            #ma_credential.save_to_file(ma_cred_filename)

            ma_cred = Certificate(filename = self.cert_file)
            
            self.credential = ma_cred.save_to_string()

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
        Update the cached list of nodes and save in 4 differnt formats
        (rspec, dns, ip, hrn)
        """

        node_details = {}
        # get node list in rspec format
        rspec = Rspec()
        rspec.parseString(self.get_rspec(self.hrn, 'aggregate'))
        # filter nodes according to policy
        rspec.filter('NodeSpec', 'name', blacklist=self.policy['blacklist'], whitelist=self.policy['whitelist'])
        # extract ifspec info to get ip's
        ips = []
        ifspecs = rspec.getDictsByTagName('IfSpec')
        for ifspec in ifspecs:
            if ifspec.has_key('addr') and ifspec['addr']:
                ips.append(ifspec['addr']) 

        # resolve component hostnames 
        nodes = self.shell.GetNodes(self.auth, {}, ['hostname', 'site_id'])
    
        # resolve site login_bases
        site_ids = [node['site_id'] for node in nodes]
        sites = self.shell.GetSites(self.auth, site_ids, ['site_id', 'login_base'])
        site_dict = {}
        for site in sites:
            site_dict[site['site_id']] = site['login_base']

        # filter nodes according to policy
        # convert plc names to geni hrn
        nodedict = {}
        for node in nodes:
            node_hrn = self.hostname_to_hrn(site_dict[node['site_id']], node['hostname'])
            # apply policy. 
            # Do not allow nodes found in blacklist, only allow nodes found in whitelist
            if self.policy['whitelist'] and node_hrn not in self.polciy['whitelist']:
                continue
            if self.policy['blacklist'] and node_hrn in self.policy['blacklist']:
                continue
            nodedict[node_hrn] = node['hostname']

        
        node_details['rspec'] = rspec.toxml()
        node_details['hrn'] = nodedict.keys()
        node_details['dns'] = nodedict.values()
        node_details['ip'] = ips
        # save state 
        self.nodes = SimpleStorage(self.nodes.db_filename, node_details)
        self.nodes.write()

        
        # update timestamp and threshold
        self.timestamp['timestamp'] =  datetime.datetime.now()
        delta = datetime.timedelta(hours=self.nodes_ttl)
        self.threshold = self.timestamp['timestamp'] + delta 
        self.timestamp.write()        
 
    def load_components(self):
        """
        Read cached list of nodes.
        """
        # Read component list from cached file 
        self.nodes.load()
        self.timestamp.load() 
        time_format = "%Y-%m-%d %H:%M:%S"
        timestamp = self.timestamp['timestamp']
        self.timestamp['timestamp'] = datetime.datetime.fromtimestamp(time.mktime(time.strptime(timestamp, time_format)))
        delta = datetime.timedelta(hours=self.nodes_ttl)
        self.threshold = self.timestamp['timestamp'] + delta

    def load_policy(self):
        """
        Read the list of blacklisted and whitelisted nodes.
        """
        self.policy.load()


    def getComponents(self, type = 'rspec'):
        """
        Return a list of components at this aggregate.
        """
        valid_types = ['rspec', 'hrn', 'dns', 'ip']
        if type not in valid_types:
            raise Exception, "Invalid type specified, must be one of the following: %s" \
                             % ", ".join(valid_types)
        
        # Reload components list
        now = datetime.datetime.now()
        #self.load_components()
        if not self.threshold or not self.timestamp['timestamp'] or now > self.threshold:
            self.refresh_components()
        elif now < self.threshold and not self.nodes.keys(): 
            self.load_components()
        return self.nodes.keys()
    
    def getSlices(self, hrn):
        """
        Return a list of instnatiated managed by this slice manager.
        """

        # XX list only the slices at the specfied hrn
        return dict(self.slices)
 
    def get_rspec(self, hrn, type):
        """
        Get resource information from PLC
        """
        
        # Get the required nodes
        if type in ['aggregate']:
            nodes = self.shell.GetNodes(self.auth)
        elif type in ['slice']:
            slicename = hrn_to_pl_slicename(hrn)
            slices = self.shell.GetSlices(self.auth, [slicename])
            node_ids = slices[0]['node_ids']
            nodes = self.shell.GetNodes(self.auth, node_ids) 
        
        # Get all network interfaces
        interface_ids = []
        for node in nodes:
            interface_ids.extend(node['nodenetwork_ids'])
        interfaces = self.shell.GetNodeNetworks(self.auth, interface_ids)
        interface_dict = {}
        for interface in interfaces:
            interface_dict[interface['nodenetwork_id']] = interface
        
        # join nodes with thier interfaces
        for node in nodes:
            node['interfaces'] = []
            for nodenetwork_id in node['nodenetwork_ids']:
                node['interfaces'].append(interface_dict[nodenetwork_id])

        # convert and threshold to ints
        if self.timestamp.has_key('timestamp') and self.timestamp['timestamp']:
            timestamp = self.timestamp['timestamp']
            threshold = self.threshold
        else:
            timestamp = datetime.datetime.now()
            delta = datetime.timedelta(hours=self.nodes_ttl)
            threshold = timestamp + delta        

    
        start_time = int(timestamp.strftime("%s"))
        end_time = int(threshold.strftime("%s"))
        duration = end_time - start_time

        # create the plc dict
        networks = {'nodes': nodes, 'name': self.hrn, 'start_time': start_time, 'duration': duration} 
        #networks = [{'name': self.hrn, 'start_time': start_time, 'duration': duration}] 
        resources = {'networks': networks, 'start_time': start_time, 'duration': duration}

        # convert the plc dict to an rspec dict
        resourceDict = RspecDict(resources)
        # convert the rspec dict to xml
        rspec = Rspec()
        rspec.parseDict(resourceDict)
        return rspec.toxml()

    def getResources(self, slice_hrn):
        """
        Return the current rspec for the specified slice.
        """
        slicename = self.hrn_to_plcslicename(slice_hrn)
        rspec = self.get_rspec(slicenamem, 'slice')
        
        return rspec
 

    def createSlice(self, slice_hrn, rspec, attributes = []):
        """
        Instantiate the specified slice according to whats defined in the rspec.
        """
        
        # save slice state locally
        # we can assume that spec object has been validated so its safer to
        # save this instead of the unvalidated rspec the user gave us
        self.slices[slice_hrn] = spec.toxml()
        self.slices.write()
        
        # Get slice info
        slicename = self.hrn_to_plcslicename(slice_hrn)
        slices = self.shell.GetSlices(self.auth, [slicename], ['node_ids'])
        if not slice:
            raise RecordNotFound(slice_hrn)
        slice = slices[0]

        # find out where this slice is currently running
        nodes = self.shell.GetNodes(self.auth, slice['node_ids'], ['hostname'])
        hostnames = [node['hostname'] for node in nodes]

        # get netspec details
        spec = Rspec(rspec)
        nodespecs = spec.getDictsByTagName('NodeSpec')
        nodes = [nodespec['name'] for nodespec in nodespecs]    
       
        # save slice state locally
        # we can assume that spec object has been validated so its safer to 
        # save this instead of the unvalidated rspec the user gave us
        self.slices[slice_hrn] = spec.toxml()
        self.slices.write()

        # remove nodes not in rspec
        delete_nodes = set(hostnames).difference(nodes)
        # add nodes from rspec
        added_nodes = set(nodes).difference(hostnames)
    
        shell.AddSliceToNodes(self.auth, slicename, added_nodes)
        shell.DeleteSliceFromNodes(self.auth, slicename, deleted_nodes)

        for attribute in attributes:
            type, value, node, nodegroup = attribute['type'], attribute['value'], attribute['node'], attribute['nodegroup']
            shell.AddSliceAttribute(self.auth, slicename, type, value, node, nodegroup)
    
        # contact registry to get slice users and add them to the slice
        slice_record = self.registry.resolve(self.credential, slice_hrn)
        # persons = slice_record['users']
        
        #for person in persons:
        #    shell.AddPersonToSlice(person['email'], slice_name)
        return 1

    def update_slice(self, slice_hrn, rspec, attributes = []):
        return self.create_slice(slice_hrn, rspec, attributes)
         
    def deleteSlice_(self, slice_hrn):
        """
        Remove this slice from all components it was previouly associated with and 
        free up the resources it was using.
        """
        if self.slices.has_key(slice_hrn):
            self.slices.pop(slice_hrn)
            self.slices.write()

        slicename = self.hrn_to_plcslicename(slice_hrn)
        slices = shell.GetSlices(self.auth, [slicename])
        if not slice:
            return 1  
        slice = slices[0]
      
        shell.DeleteSliceFromNodes(self.auth, slicename, slice['node_ids'])
        return 1

    def startSlice(self, slice_hrn):
        """
        Stop the slice at plc.
        """
        slicename = self.hrn_to_plcslicename(slice_hrn)
        slices = self.shell.GetSlices(self.auth, {'name': slicename}, ['slice_id'])
        if not slices:
            #raise RecordNotFound(slice_hrn)
            return 1 
        slice_id = slices[0]
        atrribtes = self.shell.GetSliceAttributes({'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attreibutes[0] 
        self.shell.UpdateSliceAttribute(self.auth, attribute_id, "1" )
        return 1

    def stopSlice(self, slice_hrn):
        """
        Stop the slice at plc
        """
        slicename = self.hrn_to_plcslicename(slice_hrn)
        slices = self.shell.GetSlices(self.auth, {'name': slicename}, ['slice_id'])
        if not slices:
            #raise RecordNotFound(slice_hrn)
            return 1
        slice_id = slices[0]
        atrribtes = self.shell.GetSliceAttributes({'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attreibutes[0]
        self.shell.UpdateSliceAttribute(self.auth, attribute_id, "0")
        return 1


    def resetSlice(self, slice_hrn):
        """
        Reset the slice
        """
        # XX not yet implemented
        return 1

    def getPolicy(self):
        """
        Return this aggregates policy.
        """
    
        return self.policy
        
    

##############################
## Server methods here for now
##############################

    def list_components(self):
        return self.getComponents()

    def list_slices(self, cred, hrn):
        self.decode_authentication(cred, 'list')
        return self.getSlices(hrn)

    def get_resources(self, cred, hrn):
        self.decode_authentication(cred, 'info')
        return self.getResources(hrn)

    def get_policy(self, cred):
        self.decode_authentication(cred, 'info')
        return self.getPolicy()

    def create_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'embed')
        return self.createSlice(hrn)

    def update_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'embed')
        return self.updateSlice(hrn)    

    def delete_slice(self, cred, hrn):
        self.decode_authentication(cred, 'embed')
        return self.deleteSlice(hrn)

    def start_slice(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.startSlice(hrn)

    def stop_slice(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.stopSlice(hrn)

    def reset_slice(self, cred, hrn):
        self.decode_authentication(cred, 'control')
        return self.resetSlice(hrn)

    def register_functions(self):
        GeniServer.register_functions(self)

        # Aggregate interface methods
        self.server.register_function(self.list_components)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.get_resources)
        self.server.register_function(self.get_policy)
        self.server.register_function(self.create_slice)
        self.server.register_function(self.update_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.reset_slice)
              
