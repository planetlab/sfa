import datetime
import time
from geni.util.misc import *
from geni.util.rspec import *
from geni.util.specdict import *
from geni.util.excep import *
from geni.util.storage import *
from geni.util.policy import Policy
from geni.util.debug import log
from geni.aggregate import Aggregates
from geni.registry import Registries

class Slices(SimpleStorage):

    def __init__(self, api, ttl = .5):
        self.api = api
        self.ttl = ttl
        self.threshold = None
        path = self.api.config.basepath
        filename = ".".join([self.api.interface, self.api.hrn, "slices"])
        filepath = path + os.sep + filename
        self.slices_file = filepath
        SimpleStorage.__init__(self, self.slices_file)
        self.policy = Policy(self.api)    
        self.load()


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
        slices = self.api.plshell.GetSlices(self.api.plauth, {}, ['name'])
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
        slices = self.api.plshell.GetSlices(self.api.plauth, [slicename])
        if not slices:
            return 1        
        slice = slices[0]

        self.api.plshell.DeleteSliceFromNodes(self.api.plauth, slicename, slice['node_ids'])
        return 1

    def delete_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates(self.api)
        for aggregate in aggregates:
            aggregates[aggregate].delete_slice(credential, hrn)

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
        spec = Rspec(rspec)
        # Get the slice record from geni
        slice = {}
        registries = Registries(self.api)
        registry = registries[self.api.hrn]
        credential = self.api.getCredential()
        records = registry.resolve(credential, hrn)
        for record in records:
            if record.get_type() in ['slice']:
                slice = record.as_dict()
        if not slice:
            raise RecordNotFound(slice_hrn)   

        # Make sure slice exists at plc, if it doesnt add it
        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, [slicename], ['node_ids'])
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
                site.pop('site_id')
                site_id = self.api.plshell.AddSite(self.api.plauth, site)
            else:
                site = sites[0]

            self.api.plshell.AddSlice(self.api.plauth, slice)

        # get the list of valid slice users from the registry and make 
        # they are added to the slice 
        researchers = slice.get('researcher', [])
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
                self.api.plshell.AddPerson(self.api.plauth, person_dict)
                key_ids = []
            else:
                key_ids = persons[0]['key_ids']

            self.api.plshell.AddPersonToSlice(self.api.plauth, person_dict['email'], slicename)        

            # Get this users local keys
            keylist = self.api.plshell.GetKeys(self.api.plauth, key_ids, ['key'])
            keys = [key['key'] for key in keylist]

            # add keys that arent already there 
            for personkey in person_dict['keys']:
                if personkey not in keys:
                    key = {'key_type': 'ssh', 'key': personkey}
                    self.api.plshell.AddPersonKey(self.api.plauth, person_dict['email'], key)

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

        self.api.plshell.AddSliceToNodes(self.api.plauth, slicename, added_nodes) 
        self.api.plshell.DeleteSliceFromNodes(self.api.plauth, slicename, deleted_nodes)

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
                aggregates[aggregate].create_slice(credential, hrn, rspecs[aggregate])
            except:
                print >> log, "Error creating slice %(hrn)% at aggregate %(aggregate)%" % locals()
    
        return 1


    def start_slice(self, hrn):
        if self.api.interface in ['aggregate']:
            self.start_slice_aggregate()
        elif self.api.interface in ['slicemgr']:
            self.start_slice_smgr()

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
        aggregates = Aggregates()
        for aggregate in aggregates:
            aggreegates[aggregate].start_slice(credential, hrn)
        return 1


    def stop_slice(self, hrn):
        if self.api.interface in ['aggregate']:
            self.stop_slice_aggregate()
        elif self.api.interface in ['slicemgr']:
            self.stop_slice_smgr()

    def stop_slice_aggregate(self, hrn):
        slicename = hrn_to_pl_slicename(hrn)
        slices = self.api.plshell.GetSlices(self.api.plauth, {'name': slicename}, ['slice_id'])
        if not slices:
            raise RecordNotFound(hrn)
        slice_id = slices[0]
        attributes = self.api.plshell.GetSliceAttributes(self.api.plauth, {'slice_id': slice_id, 'name': 'enabled'}, ['slice_attribute_id'])
        attribute_id = attributes[0]['slice_attribute_id']
        self.api.plshell.UpdateSliceAttribute(self.api.plauth, attribute_id, "0")
        return 1

    def stop_slice_smgr(self, hrn):
        credential = self.api.getCredential()
        aggregates = Aggregates()
        for aggregate in aggregates:
            aggregate[aggregate].stop_slice(credential, hrn)  

