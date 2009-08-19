### $Id$
### $URL$

import datetime
import time
import traceback
import sys

from types import StringTypes
from sfa.util.misc import *
from sfa.util.rspec import *
from sfa.util.specdict import *
from sfa.util.faults import *
from sfa.util.storage import *
from sfa.util.policy import Policy
from sfa.util.debug import log
from sfa.server.aggregate import Aggregates
from sfa.server.registry import Registries

class Slices(SimpleStorage):

    def __init__(self, api, ttl = .5, caller_cred=None):
        self.api = api
        self.ttl = ttl
        self.threshold = None
        path = self.api.config.SFA_BASE_DIR
        filename = ".".join([self.api.interface, self.api.hrn, "slices"])
        filepath = path + os.sep + filename
        self.slices_file = filepath
        SimpleStorage.__init__(self, self.slices_file)
        self.policy = Policy(self.api)    
        self.load()
	self.caller_cred=caller_cred


    def get_peer(self, hrn):
        # Becaues of myplc federation,  we first need to determine if this
        # slice belongs to out local plc or a myplc peer. We will assume it 
        # is a local site, unless we find out otherwise  
        peer = None

        # get this slice's authority (site)
        slice_authority = get_authority(hrn)

        # get this site's authority (sfa root authority or sub authority)
        site_authority = get_authority(slice_authority).lower()

        # check if we are already peered with this site_authority, if so
        peers = self.api.plshell.GetPeers(self.api.plauth, {}, ['peer_id', 'peername', 'shortname', 'hrn_root'])
        for peer_record in peers:
            names = [name.lower() for name in peer_record.values() if isinstance(name, StringTypes)]
            if site_authority in names:
                peer = peer_record['shortname']

        return peer

    def refresh(self):
        """
        Update the cached list of slices
        """
        # Reload components list
        now = datetime.datetime.now()
        if not self.has_key('threshold') or not self.has_key('timestamp') or \
           now > datetime.datetime.fromtimestamp(time.mktime(time.strptime(self['threshold'], self.api.time_format))):
            if self.api.interface in ['aggregate']:
                self.refresh_slices_aggregate()
            elif self.api.interface in ['slicemgr']:
                self.refresh_slices_smgr()

    def refresh_slices_aggregate(self):
        slices = self.api.plshell.GetSlices(self.api.plauth, {'peer_id': None}, ['name'])
        slice_hrns = [slicename_to_hrn(self.api.hrn, slice['name']) for slice in slices]

         # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.api.time_format)
        delta = datetime.timedelta(hours=self.ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.api.time_format)
        
        slice_details = {'hrn': slice_hrns,
                         'timestamp': hr_timestamp,
                         'threshold': hr_threshold
                        }
        self.update(slice_details)
        self.write()     
        

    def refresh_slices_smgr(self):
        slice_hrns = []
        aggregates = Aggregates(self.api)
        credential = self.api.getCredential()
        for aggregate in aggregates:
            try:
                slices = aggregates[aggregate].get_slices(credential)
                slice_hrns.extend(slices)
            except:
                print >> log, "Error calling slices at aggregate %(aggregate)s" % locals()
         # update timestamp and threshold
        timestamp = datetime.datetime.now()
        hr_timestamp = timestamp.strftime(self.api.time_format)
        delta = datetime.timedelta(hours=self.ttl)
        threshold = timestamp + delta
        hr_threshold = threshold.strftime(self.api.time_format)

        slice_details = {'hrn': slice_hrns,
                         'timestamp': hr_timestamp,
                         'threshold': hr_threshold
                        }
        self.update(slice_details)
        self.write()


    def delete_slice(self, hrn):
        if self.api.interface in ['aggregate']:
            self.delete_slice_aggregate(hrn)
        elif self.api.interface in ['slicemgr']:
            self.delete_slice_smgr(hrn)
        
    def delete_slice_aggregate(self, hrn):

        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, {'name': slicename})
        if not slices:
            return 1        
        slice = slices[0]

        # determine if this is a peer slice
        peer = self.get_peer(hrn)
        if peer:
            self.api.plshell.UnBindObjectFromPeer(self.api.plauth, 'slice', slice['slice_id'], peer)
        self.api.plshell.DeleteSliceFromNodes(self.api.plauth, slicename, slice['node_ids'])
        if peer:
            self.api.plshell.BindObjectToPeer(self.api.plauth, 'slice', slice['slice_id'], peer, slice['peer_slice_id'])
        return 1

    def delete_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            try:
                aggregates[aggregate].delete_slice(credential, hrn, caller_cred=self.caller_cred)
            except:
                print >> log, "Error calling list nodes at aggregate %s" % aggregate
                traceback.print_exc(log)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print exc_type, exc_value, exc_traceback

    def create_slice(self, hrn, rspec):
        
	# check our slice policy before we procede
        whitelist = self.policy['slice_whitelist']     
        blacklist = self.policy['slice_blacklist']
       
        if whitelist and hrn not in whitelist or \
           blacklist and hrn in blacklist:
            policy_file = self.policy.policy_file
            print >> log, "Slice %(hrn)s not allowed by policy %(policy_file)s" % locals()
            return 1

        if self.api.interface in ['aggregate']:     
            self.create_slice_aggregate(hrn, rspec)
        elif self.api.interface in ['slicemgr']:
            self.create_slice_smgr(hrn, rspec)

    def create_slice_aggregate(self, hrn, rspec):

        # Determine if this is a peer slice
        peer = self.get_peer(hrn)

        spec = Rspec(rspec)
        # Get the slice record from geni
        slice = {}
        slice_record = None
        registries = Registries(self.api)
        registry = registries[self.api.hrn]
        credential = self.api.getCredential()
        records = registry.resolve(credential, hrn)
        for record in records:
            if record.get_type() in ['slice']:
                slice_record = record.as_dict()
        if not slice_record:
            raise RecordNotFound(hrn)   

        # Make sure slice exists at plc, if it doesnt add it
        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, [slicename], ['slice_id', 'node_ids', 'site_id'] )
        if not slices:
            parts = slicename.split("_")
            login_base = parts[0]
            # if site doesnt exist add it
            sites = self.api.plshell.GetSites(self.api.plauth, [login_base])
            if not sites:
                authority = get_authority(hrn)
                site_records = registry.resolve(credential, authority)
                site_record = {}
                if not site_records:
                    raise RecordNotFound(authority)
                site_record = site_records[0]
                site = site_record.as_dict()
                
                 # add the site
                remote_site_id = site.pop('site_id')
                site_id = self.api.plshell.AddSite(self.api.plauth, site)
                # this belongs to a peer 
                if peer:
                    self.api.plshell.BindObjectToPeer(self.api.plauth, 'site', site_id, peer, remote_site_id)
            else:
                site = sites[0]
                site_id = site['site_id']
                remote_site_id = site['peer_site_id']
            
            # create slice object
            slice_fields = {}
            slice_keys = ['name', 'url', 'description']
            for key in slice_keys:
                if key in slice_record and slice_record[key]:
                    slice_fields[key] = slice_record[key]

            # add the slice  
            slice_id = self.api.plshell.AddSlice(self.api.plauth, slice_fields)
            slice = slice_fields
            
            #this belongs to a peer
            if peer:
                self.api.plshell.BindObjectToPeer(self.api.plauth, 'slice', slice_id, peer, slice_record['pointer'])
            slice['node_ids'] = []
        else:
            slice = slices[0]
            slice_id = slice['slice_id']
            site_id = slice['site_id']    
        # get the list of valid slice users from the registry and make 
        # they are added to the slice 
        researchers = record.get('researcher', [])
        for researcher in researchers:
            person_record = {}
            person_records = registry.resolve(credential, researcher)
            for record in person_records:
                if record.get_type() in ['user']:
                    person_record = record
            if not person_record:
                pass
            person_dict = person_record.as_dict()
            persons = self.api.plshell.GetPersons(self.api.plauth, [person_dict['email']], ['person_id', 'key_ids'])

            # Create the person record 
            if not persons:
                person_id=self.api.plshell.AddPerson(self.api.plauth, person_dict)

                # The line below enables the user account on the remote 
                # aggregate soon after it is created. without this the 
                # user key is not transfered to the slice (as GetSlivers 
                # returns key of only enabled users), which prevents the 
                # user from login to the slice. We may do additional checks 
                # before enabling the user.

                self.api.plshell.UpdatePerson(self.api.plauth, person_id, {'enabled' : True})
                if peer:
                    self.api.plshell.BindObjectToPeer(self.api.plauth, 'person', person_id, peer, person_record['pointer'])
                key_ids = []
            else:
                person_id = persons[0]['person_id'] 
                key_ids = persons[0]['key_ids']

            # if this is a peer person, we must unbind them from the peer or PLCAPI will throw
            # an error
            if peer:
                self.api.plshell.UnBindObjectFromPeer(self.api.plauth, 'person', person_id, peer)
                self.api.plshell.UnBindObjectFromPeer(self.api.plauth, 'site', site_id,  peer)

            self.api.plshell.AddPersonToSlice(self.api.plauth, person_dict['email'], slicename)
            self.api.plshell.AddPersonToSite(self.api.plauth, person_dict['email'], site_id)   
            if peer:
                self.api.plshell.BindObjectToPeer(self.api.plauth, 'person', person_id, peer, person_record['pointer'])
                self.api.plshell.BindObjectToPeer(self.api.plauth, 'site', site_id, peer, remote_site_id) 

            # Get this users local keys
            keylist = self.api.plshell.GetKeys(self.api.plauth, key_ids, ['key'])
            keys = [key['key'] for key in keylist]

            # add keys that arent already there 
	    key_ids=person_record['key_ids']
            for personkey in person_dict['keys']:
                if personkey not in keys:
                    key = {'key_type': 'ssh', 'key': personkey}
                    if peer:
                        self.api.plshell.UnBindObjectFromPeer(self.api.plauth, 'person', person_id, peer)
                    key_id=self.api.plshell.AddPersonKey(self.api.plauth, person_dict['email'], key)
                    if peer:
			 self.api.plshell.BindObjectToPeer(self.api.plauth, 'person', person_id, peer, person_record['pointer'])
			 self.api.plshell.BindObjectToPeer(self.api.plauth, 'key', key_id, peer, key_ids.pop(0))

        # find out where this slice is currently running
        nodelist = self.api.plshell.GetNodes(self.api.plauth, slice['node_ids'], ['hostname'])
        hostnames = [node['hostname'] for node in nodelist]

        # get netspec details
        nodespecs = spec.getDictsByTagName('NodeSpec')
        nodes = []
        for nodespec in nodespecs:
            if isinstance(nodespec['name'], list):
                nodes.extend(nodespec['name'])
            elif isinstance(nodespec['name'], StringTypes):
                nodes.append(nodespec['name'])

        # remove nodes not in rspec
        deleted_nodes = list(set(hostnames).difference(nodes))
        # add nodes from rspec
        added_nodes = list(set(nodes).difference(hostnames))

        if peer:
            self.api.plshell.UnBindObjectFromPeer(self.api.plauth, 'slice', slice_id, peer)
        self.api.plshell.AddSliceToNodes(self.api.plauth, slicename, added_nodes) 
        self.api.plshell.DeleteSliceFromNodes(self.api.plauth, slicename, deleted_nodes)
        if peer:
            self.api.plshell.BindObjectToPeer(self.api.plauth, 'slice', slice_id, peer, slice_record['pointer'])

        return 1

    def create_slice_smgr(self, hrn, rspec):
        spec = Rspec()
        tempspec = Rspec()
        spec.parseString(rspec)
        slicename = hrn_to_pl_slicename(hrn)
        specDict = spec.toDict()
        if specDict.has_key('Rspec'): specDict = specDict['Rspec']
        if specDict.has_key('start_time'): start_time = specDict['start_time']
        else: start_time = 0
        if specDict.has_key('end_time'): end_time = specDict['end_time']
        else: end_time = 0

        rspecs = {}
        aggregates = Aggregates(self.api)
        credential = self.api.getCredential()
        # only attempt to extract information about the aggregates we know about
        for aggregate in aggregates:
            netspec = spec.getDictByTagNameValue('NetSpec', aggregate)
            if netspec:
                # creat a plc dict 
                resources = {'start_time': start_time, 'end_time': end_time, 'networks': netspec}
                resourceDict = {'Rspec': resources}
                tempspec.parseDict(resourceDict)
                rspecs[aggregate] = tempspec.toxml()

        # notify the aggregates
        for aggregate in rspecs.keys():
            try:
                # send the whloe rspec to the local aggregate
                if aggregate in [self.api.hrn]:
                    aggregates[aggregate].create_slice(credential, hrn, rspec, caller_cred=self.caller_cred)
                else:
                    aggregates[aggregate].create_slice(credential, hrn, rspecs[aggregate], caller_cred=self.caller_cred)
            except:
                print >> log, "Error creating slice %(hrn)s at aggregate %(aggregate)s" % locals()
                traceback.print_exc()
        return 1


    def start_slice(self, hrn):
        if self.api.interface in ['aggregate']:
            self.start_slice_aggregate(hrn)
        elif self.api.interface in ['slicemgr']:
            self.start_slice_smgr(hrn)

    def start_slice_aggregate(self, hrn):
        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, {'name': slicename}, ['slice_id'])
        if not slices:
            raise RecordNotFound(hrn)
        slice_id = slices[0]
        attributes = self.api.plshell.GetSliceAttributes(self.api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attreibutes[0]['slice_attribute_id']
        self.api.plshell.UpdateSliceAttribute(self.api.plauth, attribute_id, "1" )
        return 1

    def start_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            aggregates[aggregate].start_slice(credential, hrn)
        return 1


    def stop_slice(self, hrn):
        if self.api.interface in ['aggregate']:
            self.stop_slice_aggregate(hrn)
        elif self.api.interface in ['slicemgr']:
            self.stop_slice_smgr(hrn)

    def stop_slice_aggregate(self, hrn):
        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, {'name': slicename}, ['slice_id'])
        if not slices:
            raise RecordNotFound(hrn)
        slice_id = slices[0]['slice_id']
        attributes = self.api.plshell.GetSliceAttributes(self.api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attributes[0]['slice_attribute_id']
        self.api.plshell.UpdateSliceAttribute(self.api.plauth, attribute_id, "0")
        return 1

    def stop_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            aggregates[aggregate].stop_slice(credential, hrn)  

