import os
import sys
import datetime
import time
import xmlrpclib

from types import StringTypes, ListType
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

        # How long before we refresh nodes cache
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
        url = 'http://%(address)s:%(port)s' % locals()
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

        ma_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".ma.cred"
        
        # see if this file exists
        try:
            self.credential = Credential(filename = ma_cred_filename)
        except IOError:
            self.credential = self.getCredentialFromRegistry()

    def getCredentialFromRegistry(self):
        """
        Get our current credential from the registry
        """
        # get self credential
        self_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".cred"
        self_cred = self.registry.get_credential(None, 'ma', self.hrn)
        self_cred.save_to_file(self_cred_filename, save_parents = True)

        
        # get ma credential
        ma_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".ma.cred"
        ma_cred = self.registry.get_credential(self_cred, 'ma', self.hrn)
        ma_cred.save_to_file(ma_cred_filename, save_parents=True)
        return ma_cred        


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
        parts = slicename.split("_")
        slice_hrn = ".".join([self.hrn, parts[0]]) + "." + "_".join(parts[1:])
          
        return slice_hrn

    def refresh_components(self):
        """
        Update the cached list of nodes and save in 4 differnt formats
        (rspec, dns, ip)
        """

        # get node list in rspec format
        rspec = Rspec()
        rspec.parseString(self.get_rspec(self.hrn, 'aggregate'))
        
        # filter nodes according to policy
        rspec.filter('NodeSpec', 'name', blacklist=self.policy['blacklist'], whitelist=self.policy['whitelist'])
        
        # extract ifspecs from rspec to get ip's
        ips = []
        ifspecs = rspec.getDictsByTagName('IfSpec')
        for ifspec in ifspecs:
            if ifspec.has_key('addr') and ifspec['addr']:
                ips.append(ifspec['addr']) 

        # extract nodespecs from rspec to get dns names
        hostnames = []
        nodespecs = rspec.getDictsByTagName('NodeSpec')
        for nodespec in nodespecs:
            if nodespec.has_key('name') and nodespec['name']:
                hostnames.append(nodespec['name'])

        
        node_details = {}
        node_details['rspec'] = rspec.toxml()
        node_details['ip'] = ips
        node_details['dns'] = hostnames
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


    def getNodes(self, format = 'rspec'):
        """
        Return a list of components at this aggregate.
        """
        valid_formats = ['rspec', 'hrn', 'dns', 'ip']
        if not format:
            format = 'rspec'
        if format not in valid_formats:
            raise Exception, "Invalid format specified, must be one of the following: %s" \
                             % ", ".join(valid_formats)
        
        # Reload components list
        now = datetime.datetime.now()
        #self.load_components()
        if not self.threshold or not self.timestamp['timestamp'] or now > self.threshold:
            self.refresh_components()
        elif now < self.threshold and not self.nodes.keys(): 
            self.load_components()
        return self.nodes[format]
    
    def getSlices(self):
        """
        Return a list of instnatiated managed by this slice manager.
        """

        slices = self.shell.GetSlices(self.auth, {}, ['name'])
        slice_hrns = [self.slicename_to_hrn(slice['name']) for slice in slices]  
        
        return slice_hrns
 
    def get_rspec(self, hrn, type):
        """
        Get resource information from PLC
        """
        
        # Get the required nodes
        if type in ['aggregate']:
            nodes = self.shell.GetNodes(self.auth)
            try:  linkspecs = self.shell.GetLinkSpecs() # if call is supported
            except:  linkspecs = []
        elif type in ['slice']:
            slicename = hrn_to_pl_slicename(hrn)
            slices = self.shell.GetSlices(self.auth, [slicename])
            node_ids = slices[0]['node_ids']
            nodes = self.shell.GetNodes(self.auth, node_ids) 
        
        # Filter out whitelisted nodes
        public_nodes = lambda n: n.has_key('slice_ids_whitelist') and not n['slice_ids_whitelist']
        nodes = filter(public_nodes, nodes)
 
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
        networks = [{'nodes': nodes,
                     'name': self.hrn, 
                     'start_time': start_time, 
                     'duration': duration}]
        if type in ['aggregate']:
            networks[0]['links'] = linkspecs 
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
        rspec = self.get_rspec(slice_hrn, 'slice')
        
        return rspec
 
    
    def getTicket(self, hrn, rspec):
        """
        Retrieve a ticket. This operation is currently implemented on PLC
        only (see SFA, engineering decisions); it is not implemented on
        components.

        @param name name of the slice to retrieve a ticket for
        @param rspec resource specification dictionary
        @return the string representation of a ticket object
        """
        #self.registry.get_ticket(name, rspec)

        return         


    def createSlice(self, slice_hrn, rspec, attributes = []):
        """
        Instantiate the specified slice according to whats defined in the rspec.
        """
        
        spec = Rspec(rspec)
        # save slice state locally
        # we can assume that spec object has been validated so its safer to
        # save this instead of the unvalidated rspec the user gave us
        self.slices[slice_hrn] = spec.toxml()
        self.slices.write()
       
        # Get the slice record from geni
        slice = {}
        records = self.registry.resolve(self.credential, slice_hrn)
            
        for record in records:
            if record.get_type() in ['slice']:
                slice_info = record.as_dict()
                slice = slice_info['pl_info']
        if not slice:
            raise RecordNotFound(slice_hrn)
                    
 
        # Make sure slice exists at plc, if it doesnt add it
        slicename = hrn_to_pl_slicename(slice_hrn)
        slices = self.shell.GetSlices(self.auth, [slicename], ['node_ids'])
        if not slices:
            parts = slicename.split("_")
            login_base = parts[0]
            # if site doesnt exist add it
            sites = self.shell.GetSites(self.auth, [login_base]) 
            if not sites:
                authority = get_authority(slice_hrn)
                site_record = self.registry.reolve(self.cred, authority)
                site_info = site_record.as_dict()
                site = site_info['pl_info'] 
                
                # add the site
                site.pop('site_id') 
                site_id = self.shell.AddSite(self.auth, site)
            else:
                site = sites[0]
                
            self.shell.AddSlice(self.auth, slice_info)
        
        # get the list of valid slice users from the registry and make 
        # they are added to the slice 
        geni_info = slice_info['geni_info']
        researchers = geni_info['researcher']
        for researcher in researchers:
            person_record = {}
            person_records = self.registry.resolve(self.credential, researcher)
            for record in person_records:
                if record.get_type() in ['user']:
                    person_record = record
            if not person_record:
                pass
            person_dict = person_record.as_dict()['pl_info']
            persons = self.shell.GetPersons(self.auth, [person_dict['email']], ['person_id', 'key_ids'])
            
            # Create the person record 
            if not persons:
                self.shell.AddPerson(self.auth, person_dict)
            self.shell.AddPersonToSlice(self.auth, person_dict['email'], slicename)
            # Add this person's public keys
            for personkey in person_dict['keys']:
                key = {'key_type': 'ssh', 'key': personkey}      
                self.shell.AddPersonKey(self.auth, person_dict['email'], key)
 
        # find out where this slice is currently running
        nodelist = self.shell.GetNodes(self.auth, slice['node_ids'], ['hostname'])
        hostnames = [node['hostname'] for node in nodelist]

        # get netspec details
        nodespecs = spec.getDictsByTagName('NodeSpec')
        nodes = []
        for nodespec in nodespecs:
            if isinstance(nodespec['name'], list):
                nodes.extend(nodespec['name'])
            elif isinstance(nodespec['name'], StringTypes):
                nodes.append(nodespec['name'])
                
        # save slice state locally
        # we can assume that spec object has been validated so its safer to 
        # save this instead of the unvalidated rspec the user gave us
        self.slices[slice_hrn] = spec.toxml()
        self.slices.write()

        # remove nodes not in rspec
        deleted_nodes = list(set(hostnames).difference(nodes))
        # add nodes from rspec
        added_nodes = list(set(nodes).difference(hostnames))
    
        self.shell.AddSliceToNodes(self.auth, slicename, added_nodes)
        self.shell.DeleteSliceFromNodes(self.auth, slicename, deleted_nodes)

        return 1

    def updateSlice(self, slice_hrn, rspec, attributes = []):
        return self.create_slice(slice_hrn, rspec, attributes)
         
    def deleteSlice(self, slice_hrn):
        """
        Remove this slice from all components it was previouly associated with and 
        free up the resources it was using.
        """
        if self.slices.has_key(slice_hrn):
            self.slices.pop(slice_hrn)
            self.slices.write()

        slicename = hrn_to_pl_slicename(slice_hrn)
        slices = self.shell.GetSlices(self.auth, [slicename])
        if not slices:
            return 1  
        slice = slices[0]
      
        self.shell.DeleteSliceFromNodes(self.auth, slicename, slice['node_ids'])
        return 1

    def startSlice(self, slice_hrn):
        """
        Stop the slice at plc.
        """
        slicename = hrn_to_pl_slicename(slice_hrn)
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
        slicename = hrn_to_pl_slicename(slice_hrn)
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


    # XX fix rights, should be function name defined in 
    # privilege_table (from util/rights.py)
    def list_nodes(self, cred):
        self.decode_authentication(cred, 'listnodes')
        return self.getNodes()

    def list_slices(self, cred):
        self.decode_authentication(cred, 'listslices')
        return self.getSlices()

    def get_resources(self, cred, hrn = None):
        self.decode_authentication(cred, 'listnodes')
        if not hrn: 
            return self.getNodes()
        else: 
            return self.getResources(hrn)

    def get_ticket(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'getticket')
        return self.getTicket(hrn, rspec)
 
    def get_policy(self, cred):
        self.decode_authentication(cred, 'getpolicy')
        return self.getPolicy()

    def create_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'createslice')
        return self.createSlice(hrn, rspec)

    def update_slice(self, cred, hrn, rspec):
        self.decode_authentication(cred, 'updateslice')
        return self.updateSlice(hrn)    

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
        self.server.register_function(self.update_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.reset_slice)
              
