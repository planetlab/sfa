#
# SFA XML-RPC and SOAP interfaces
#
### $Id: api.py 17793 2010-04-26 21:40:57Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/plc/api.py $
#

import sys
import os
import traceback
import string
import xmlrpclib

from sfa.util.sfalogging import sfa_logger
from sfa.trust.auth import Auth
from sfa.util.config import *
from sfa.util.faults import *
from sfa.trust.rights import *
from sfa.trust.credential import *
from sfa.trust.certificate import *
from sfa.util.namespace import *
from sfa.util.api import *
from sfa.util.nodemanager import NodeManager
from collections import defaultdict


class RecordInfo():
    
    shell = None
    auth = None
    
    # pl records
    sites = {}
    slices = {}
    persons = {}
    nodes = {}
    keys = {}

    # sfa records
    sfa_authorities = {}
    sfa_slices = {}
    sfa_users = {}
    sfa_nodes = {}
     
    records = []

    def __init__(self, api, records):
        self.api = api
        self.shell = api.plshell
        self.auth = api.plauth
        
        site_ids = []
        slice_ids = []
        person_ids = []
        node_ids = []

        # put records into groups based on types
        for record in records:
            pointer = record['pointer']
            if record['type'] == 'authority':
                self.sfa_authorities[pointer] = record
                self.records.append(record)
                site_ids.append(record['pointer'])
            elif record['type'] == 'slice':
                self.sfa_slices[pointer] = record
                self.records.append(record)
                slice_ids.append(record['pointer'])
            elif record['type'] == 'user':
                self.sfa_users[pointer] = record
                self.records.append(record)
                person_ids.append(record['pointer'])
            elif record['type'] == 'node':
                self.sfa_nodes[pointer] = record
                self.records.append(record)
                node_ids.append(record['pointer']) 

        # get pl info for these records
        self.update_pl_sites(site_ids)
        self.update_pl_slices(slice_ids)
        self.update_pl_persons(person_ids)
        self.update_pl_nodes(node_ids)
       
        site_ids = []
        slice_ids = []
        person_ids = []
        node_ids = []
        # now get pl records for all ids associated with 
        # these records
        for record in records:
            if 'site_id' in record:
                site_ids.append(record['site_id'])
            if 'site_ids' in records:
                site_ids.extend(record['site_ids'])
            if 'person_ids' in record:
                person_ids.extend(record['person_ids'])
            if 'slice_ids' in record:
                slice_ids.extend(record['slice_ids'])
            if 'node_ids' in record:
                node_ids.extend(record['node_ids'])

        # get pl info for these records
        self.update_pl_sites(site_ids)
        self.update_pl_slices(slice_ids)
        self.update_pl_persons(person_ids)
        self.update_pl_nodes(node_ids)

        # convert pl ids to hrns  
        self.update_hrns()

        # update sfa info
        self.update_sfa_info(person_ids)

    def update_pl_sites(self, site_ids):
        """
        Update site records with PL info 
        """
        if not site_ids:
            return
        sites = self.shell.GetSites(self.auth, site_ids)
        for site in sites:
            site_id = site['site_id']
            self.sites[site_id] = site
            if site_id in self.sfa_authorities:
                self.sfa_authorities[site_id].update(site)

    def update_pl_slices(self, slice_ids):
        """
        Update slice records with PL info
        """
        if not slice_ids:
            return
        slices = self.shell.GetSlices(self.auth, slice_ids)
        for slice in slices:
            slice_id = slice['slice_id']
            self.slices[slice_id] = slice
            if slice_id in self.sfa_slices:
                self.sfa_slices[slice_id].update(slice)

    def update_pl_persons(self, person_ids):
        """
        Update person records with PL info
        """
        key_ids = []
        if not person_ids:
            return
        persons = self.shell.GetPersons(self.auth, person_ids)
        for person in persons:
            person_id = person['person_id']
            self.persons[person_id] = person 
            key_ids.extend(person['key_ids'])
            if person_id in self.sfa_users:
                self.sfa_users[person_id].update(person)
        self.update_pl_keys(key_ids)

    def update_pl_keys(self, key_ids):
        """
        Update user records with PL public key info
        """
        if not key_ids:
            return
        keys = self.shell.GetKeys(self.auth, key_ids)
        for key in keys:
            person_id = key['person_id']
            self.keys[key['key_id']] = key
            if person_id in self.sfa_users:
                person = self.sfa_users[person_id]    
                if not 'keys' in person:
                    person['keys'] = [key['key']]
                else: 
                    person['keys'].append(key['key'])

    def update_pl_nodes(self, node_ids):
        """
        Update node records with PL info
        """
        if not node_ids:
            return 
        nodes = self.shell.GetNodes(self.auth, node_ids)
        for node in nodes:
            node_id = node['node_id']
            self.nodes[node['node_id']] = node
            if node_id in self.sfa_nodes:
                self.sfa_nodes[node_id].update(node)
    

    def update_hrns(self):
        """
        Convert pl ids to hrns
        """
        for record in self.records:
            # get all necessary data
            type = record['type']
            pointer = record['pointer']
            auth_hrn = self.api.hrn
            login_base = ''
            if pointer == -1:
                continue       

            if 'site_id' in record:
                site = self.sites[record['site_id']]
                login_base = site['login_base']
                record['site'] = ".".join([auth_hrn, login_base])
            if 'person_ids' in record:
                emails = [self.persons[person_id]['email'] for person_id in record['person_ids'] \
                          if person_id in self.persons]
                usernames = [email.split('@')[0] for email in emails]
                person_hrns = [".".join([auth_hrn, login_base, username]) for username in usernames]
                record['persons'] = person_hrns
            if 'slice_ids' in record:
                slicenames = [self.slices[slice_id]['name'] for slice_id in record['slice_ids'] \
                              if slice_id in self.slices]
                slice_hrns = [slicename_to_hrn(auth_hrn, slicename) for slicename in slicenames]
                record['slices'] = slice_hrns
            if 'node_ids' in record:
                hostnames = [self.nodes[node_id]['hostname'] for node_id in record['node_ids'] \
                             if node_id in self.nodes]
                node_hrns = [hostname_to_hrn(auth_hrn, login_base, hostname) for hostname in hostnames]
                record['nodes'] = node_hrns
            if 'site_ids' in record:
                login_bases = [self.sites[site_id]['login_base'] for site_id in record['site_ids'] \
                               if site_id in self.sites]
                site_hrns = [".".join([auth_hrn, lbase]) for lbase in login_bases]
                record['sites'] = site_hrns 

    def update_sfa_info(self, person_ids):
        from sfa.util.table import SfaTable
        table = SfaTable()
        persons = table.find({'type': 'user', 'pointer': person_ids})
        # create a hrns keyed on the sfa record's pointer.
        # Its possible for  multiple records to have the same pointer so 
        # the dict's value will be a list of hrns.
        person_dict = defaultdict(list)
        for person in persons:
            person_dict[person['pointer']].append(person['hrn'])                       

        def startswith(prefix, values):
            return [value for value in values if value.startswith(prefix)]

        for record in self.records:
            authority = record['authority']
            if record['pointer'] == -1:
                continue
            
            if record['type'] == 'slice':
                # all slice users are researchers
                record['PI'] = []
                record['researchers'] = []    
                for person_id in record['person_ids']:
                    record['researchers'].extend(person_dict[person_id])
                # also add the pis at the slice's site
                site = self.sites[record['site_id']]    
                for person_id in site['person_ids']:
                    person = self.persons[person_id]
                    if 'pi' in person['roles']:
                        # PLCAPI doesn't support per site roles 
                        # (a pi has the pi role at every site he belongs to).
                        # We shouldnt allow this in SFA         
                        record['PI'].extend(startswith(authority, person_dict[person_id]))    

            elif record['type'] == 'authority':
                record['PI'] = []
                record['operator'] = []
                record['owner'] = []
                for person_id in record['person_ids']:
                    person = self.persons[person_id]
                    if 'pi' in person['roles']:
                        # only get PI's at this site
                        record['PI'].extend(startswith(record['hrn'], person_dict[person_id]))
                    if 'tech' in person['roles']:
                        # only get PI's at this site
                        record['operator'].extend(startswith(record['hrn'], person_dict[person_id]))
                    if 'admin' in person['roles']:
                        record['owner'].extend(startswith(record['hrn'], person_dict[person_id]))
                            
            elif record['type'] == 'node':
                record['dns'] = record['hostname']

            elif record['type'] == 'user':
                record['email'] = record['email']                   
                                   
                  
                 
                
                    
    def get_records(self):
        return self.records
 

class SfaAPI(BaseAPI):

    # flat list of method names
    import sfa.methods
    methods = sfa.methods.all
    
    def __init__(self, config = "/etc/sfa/sfa_config.py", encoding = "utf-8", 
                 methods='sfa.methods', peer_cert = None, interface = None, 
                key_file = None, cert_file = None, cache = None):
        BaseAPI.__init__(self, config=config, encoding=encoding, methods=methods, \
                         peer_cert=peer_cert, interface=interface, key_file=key_file, \
                         cert_file=cert_file, cache=cache)
 
        self.encoding = encoding

        from sfa.util.table import SfaTable
        self.SfaTable = SfaTable
        # Better just be documenting the API
        if config is None:
            return

        # Load configuration
        self.config = Config(config)
        self.auth = Auth(peer_cert)
        self.interface = interface
        self.key_file = key_file
        self.key = Keypair(filename=self.key_file)
        self.cert_file = cert_file
        self.cert = Certificate(filename=self.cert_file)
        self.credential = None
        # Initialize the PLC shell only if SFA wraps a myPLC
        rspec_type = self.config.get_aggregate_type()
        if (rspec_type == 'pl' or rspec_type == 'vini'):
            self.plshell = self.getPLCShell()
            self.plshell_version = "4.3"

        self.hrn = self.config.SFA_INTERFACE_HRN
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.logger=sfa_logger

    def getPLCShell(self):
        self.plauth = {'Username': self.config.SFA_PLC_USER,
                       'AuthMethod': 'password',
                       'AuthString': self.config.SFA_PLC_PASSWORD}

        self.plshell_type = 'xmlrpc' 
        # connect via xmlrpc
        url = self.config.SFA_PLC_URL
        shell = xmlrpclib.Server(url, verbose = 0, allow_none = True)
        return shell

    def getCredential(self):
        if self.interface in ['registry']:
            return self.getCredentialFromLocalRegistry()
        else:
            return self.getCredentialFromRegistry()
    
    def getCredentialFromRegistry(self):
        """ 
        Get our credential from a remote registry 
        """
        type = 'authority'
        path = self.config.SFA_DATA_DIR
        filename = ".".join([self.interface, self.hrn, type, "cred"])
        cred_filename = path + os.sep + filename
        try:
            credential = Credential(filename = cred_filename)
            return credential.save_to_string(save_parents=True)
        except IOError:
            from sfa.server.registry import Registries
            registries = Registries(self)
            registry = registries[self.hrn]
            cert_string=self.cert.save_to_string(save_parents=True)
            # get self credential
            self_cred = registry.GetSelfCredential(cert_string, self.hrn, type)
            # get credential
            cred = registry.GetCredential(self_cred, type, self.hrn)
            
            # save cred to file
            Credential(string=cred).save_to_file(cred_filename, save_parents=True)
            return cred

    def getCredentialFromLocalRegistry(self):
        """
        Get our current credential directly from the local registry.
        """

        hrn = self.hrn
        auth_hrn = self.auth.get_authority(hrn)
    
        # is this a root or sub authority
        if not auth_hrn or hrn == self.config.SFA_INTERFACE_HRN:
            auth_hrn = hrn
        auth_info = self.auth.get_auth_info(auth_hrn)
        table = self.SfaTable()
        records = table.findObjects(hrn)
        if not records:
            raise RecordNotFound
        record = records[0]
        type = record['type']
        object_gid = record.get_gid_object()
        new_cred = Credential(subject = object_gid.get_subject())
        new_cred.set_gid_caller(object_gid)
        new_cred.set_gid_object(object_gid)
        new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
        new_cred.set_pubkey(object_gid.get_pubkey())
        r1 = determine_rights(type, hrn)
        new_cred.set_privileges(r1)

        auth_kind = "authority,ma,sa"

        new_cred.set_parent(self.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))

        new_cred.encode()
        new_cred.sign()

        return new_cred.save_to_string(save_parents=True)
   

    def loadCredential (self):
        """
        Attempt to load credential from file if it exists. If it doesnt get
        credential from registry.
        """

        # see if this file exists
        # XX This is really the aggregate's credential. Using this is easier than getting
        # the registry's credential from iteslf (ssl errors).   
        ma_cred_filename = self.config.SFA_DATA_DIR + os.sep + self.interface + self.hrn + ".ma.cred"
        try:
            self.credential = Credential(filename = ma_cred_filename)
        except IOError:
            self.credential = self.getCredentialFromRegistry()

    ##
    # Convert SFA fields to PLC fields for use when registering up updating
    # registry record in the PLC database
    #
    # @param type type of record (user, slice, ...)
    # @param hrn human readable name
    # @param sfa_fields dictionary of SFA fields
    # @param pl_fields dictionary of PLC fields (output)

    def sfa_fields_to_pl_fields(self, type, hrn, record):

        def convert_ints(tmpdict, int_fields):
            for field in int_fields:
                if field in tmpdict:
                    tmpdict[field] = int(tmpdict[field])

        pl_record = {}
        #for field in record:
        #    pl_record[field] = record[field]
 
        if type == "slice":
            if not "instantiation" in pl_record:
                pl_record["instantiation"] = "plc-instantiated"
            pl_record["name"] = hrn_to_pl_slicename(hrn)
	    if "url" in record:
               pl_record["url"] = record["url"]
	    if "description" in record:
	        pl_record["description"] = record["description"]
	    if "expires" in record:
	        pl_record["expires"] = int(record["expires"])

        elif type == "node":
            if not "hostname" in pl_record:
                if not "hostname" in record:
                    raise MissingSfaInfo("hostname")
                pl_record["hostname"] = record["hostname"]
            if not "model" in pl_record:
                pl_record["model"] = "geni"

        elif type == "authority":
            pl_record["login_base"] = hrn_to_pl_login_base(hrn)

            if not "name" in pl_record:
                pl_record["name"] = hrn

            if not "abbreviated_name" in pl_record:
                pl_record["abbreviated_name"] = hrn

            if not "enabled" in pl_record:
                pl_record["enabled"] = True

            if not "is_public" in pl_record:
                pl_record["is_public"] = True

        return pl_record


    def fill_record_info(self, records):
        """
        Given a SFA record, fill in the PLC specific and SFA specific
        fields in the record. 
        """
        if not isinstance(records, list):
            records = [records]

        record_info = RecordInfo(self, records)
        return record_info.get_records()

    def update_membership_list(self, oldRecord, record, listName, addFunc, delFunc):
        # get a list of the HRNs tht are members of the old and new records
        if oldRecord:
            oldList = oldRecord.get(listName, [])
        else:
            oldList = []     
        newList = record.get(listName, [])

        # if the lists are the same, then we don't have to update anything
        if (oldList == newList):
            return

        # build a list of the new person ids, by looking up each person to get
        # their pointer
        newIdList = []
        table = self.SfaTable()
        records = table.find({'type': 'user', 'hrn': newList})
        for rec in records:
            newIdList.append(rec['pointer'])

        # build a list of the old person ids from the person_ids field 
        if oldRecord:
            oldIdList = oldRecord.get("person_ids", [])
            containerId = oldRecord.get_pointer()
        else:
            # if oldRecord==None, then we are doing a Register, instead of an
            # update.
            oldIdList = []
            containerId = record.get_pointer()

    # add people who are in the new list, but not the oldList
        for personId in newIdList:
            if not (personId in oldIdList):
                addFunc(self.plauth, personId, containerId)

        # remove people who are in the old list, but not the new list
        for personId in oldIdList:
            if not (personId in newIdList):
                delFunc(self.plauth, personId, containerId)

    def update_membership(self, oldRecord, record):
        if record.type == "slice":
            self.update_membership_list(oldRecord, record, 'researcher',
                                        self.plshell.AddPersonToSlice,
                                        self.plshell.DeletePersonFromSlice)
        elif record.type == "authority":
            # xxx TODO
            pass



class ComponentAPI(BaseAPI):

    def __init__(self, config = "/etc/sfa/sfa_config.py", encoding = "utf-8", methods='sfa.methods',
                 peer_cert = None, interface = None, key_file = None, cert_file = None):

        BaseAPI.__init__(self, config=config, encoding=encoding, methods=methods, peer_cert=peer_cert,
                         interface=interface, key_file=key_file, cert_file=cert_file)
        self.encoding = encoding

        # Better just be documenting the API
        if config is None:
            return

        self.nodemanager = NodeManager(self.config)

    def sliver_exists(self):
        sliver_dict = self.nodemanager.GetXIDs()
        if slicename in sliver_dict.keys():
            return True
        else:
            return False
