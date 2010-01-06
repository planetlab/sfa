#
# SFA XML-RPC and SOAP interfaces
#
### $Id$
### $URL$
#

import sys
import os
import traceback
import string
import xmlrpclib
from sfa.trust.auth import Auth
from sfa.util.config import *
from sfa.util.faults import *
from sfa.util.debug import *
from sfa.trust.rights import *
from sfa.trust.credential import *
from sfa.trust.certificate import *
from sfa.util.namespace import *
from sfa.util.api import *
from sfa.util.nodemanager import NodeManager
from sfa.util.sfalogging import *
from sfa.util.table import SfaTable

class SfaAPI(BaseAPI):

    # flat list of method names
    import sfa.methods
    methods = sfa.methods.all
    
    def __init__(self, config = "/etc/sfa/sfa_config", encoding = "utf-8", methods='sfa.methods', 
                 peer_cert = None, interface = None, key_file = None, cert_file = None):
        BaseAPI.__init__(self, config=config, encoding=encoding, methods=methods, peer_cert=peer_cert,
                         interface=interface, key_file=key_file, cert_file=cert_file)
 
        self.encoding = encoding

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
        rspec_type = self.config.get_aggregate_rspec_type()
        if (rspec_type == 'pl' or rspec_type == 'vini'):
            self.plshell = self.getPLCShell()
            self.plshell_version = self.getPLCShellVersion()

        self.hrn = self.config.SFA_INTERFACE_HRN
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.logger=get_sfa_logger()

    def getPLCShell(self):
        self.plauth = {'Username': self.config.SFA_PLC_USER,
                       'AuthMethod': 'password',
                       'AuthString': self.config.SFA_PLC_PASSWORD}
        try:
            self.plshell_type = 'direct'
            import PLC.Shell
            shell = PLC.Shell.Shell(globals = globals())
            shell.AuthCheck(self.plauth)
            return shell
        except ImportError:
            self.plshell_type = 'xmlrpc' 
            # connect via xmlrpc
            url = self.config.SFA_PLC_URL
            shell = xmlrpclib.Server(url, verbose = 0, allow_none = True)
            shell.AuthCheck(self.plauth)
            return shell

    def getPLCShellVersion(self):
        # We need to figure out what version of PLCAPI we are talking to.
        # Some calls we need to make later will be different depending on
        # the api version. 
        try:
            # This is probably a bad way to determine api versions
            # but its easy and will work for now. Lets try to make 
            # a call that only exists is PLCAPI.4.3. If it fails, we
            # can assume the api version is 4.2
            self.plshell.GetTagTypes(self.plauth)
            return '4.3'
        except:
            return '4.2'
            

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
            self_cred = registry.get_self_credential(cert_string, type, self.hrn)
            # get credential
            cred = registry.get_credential(self_cred, type, self.hrn)
            
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
        table = SfaTable()
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

    def fill_record_pl_info(self, record):
        """
        Fill in the planetlab specific fields of a SFA record. This
        involves calling the appropriate PLC method to retrieve the 
        database record for the object.
        
        PLC data is filled into the pl_info field of the record.
    
        @param record: record to fill in field (in/out param)     
        """
        type = record['type']
        pointer = record['pointer']
        auth_hrn = self.hrn
        login_base = ''
        # records with pointer==-1 do not have plc info associated with them.
        # for example, the top level authority records which are
        # authorities, but not PL "sites"
        if pointer == -1:
            record.update({})
            return

        if (type in ["authority"]):
            pl_res = self.plshell.GetSites(self.plauth, [pointer])
        elif (type == "slice"):
            pl_res = self.plshell.GetSlices(self.plauth, [pointer])
        elif (type == "user"):
            pl_res = self.plshell.GetPersons(self.plauth, [pointer])
        elif (type == "node"):
            pl_res = self.plshell.GetNodes(self.plauth, [pointer])
        else:
            raise UnknownSfaType(type)
        
        if not pl_res:
            raise PlanetLabRecordDoesNotExist(record['hrn'])

        # convert ids to hrns
        pl_record = pl_res[0]
        if 'site_id' in pl_record:
            sites = self.plshell.GetSites(self.plauth, pl_record['site_id'], ['login_base'])
            site = sites[0]
            login_base = site['login_base']
            pl_record['site'] = ".".join([auth_hrn, login_base])
        if 'person_ids' in pl_record:
            persons =  self.plshell.GetPersons(self.plauth, pl_record['person_ids'], ['email'])
            emails = [person['email'] for person in persons]
            usernames = [email.split('@')[0] for email in emails]
            person_hrns = [".".join([auth_hrn, login_base, username]) for username in usernames]
            pl_record['persons'] = person_hrns 
        if 'slice_ids' in pl_record:
            slices = self.plshell.GetSlices(self.plauth, pl_record['slice_ids'], ['name'])
            slicenames = [slice['name'] for slice in slices]
            slice_hrns = [slicename_to_hrn(auth_hrn, slicename) for slicename in slicenames]
            pl_record['slices'] = slice_hrns
        if 'node_ids' in pl_record:
            nodes = self.plshell.GetNodes(self.plauth, pl_record['node_ids'], ['hostname'])
            hostnames = [node['hostname'] for node in nodes]
            node_hrns = [hostname_to_hrn(auth_hrn, login_base, hostname) for hostname in hostnames]
            pl_record['nodes'] = node_hrns
        if 'site_ids' in pl_record:
            sites = self.plshell.GetSites(self.plauth, pl_record['site_ids'], ['login_base'])
            login_bases = [site['login_base'] for site in sites]
            site_hrns = [".".join([auth_hrn, lbase]) for lbase in login_bases]
            pl_record['sites'] = site_hrns
        if 'key_ids' in pl_record:
            keys = self.plshell.GetKeys(self.plauth, pl_record['key_ids'])
            pubkeys = []
            if keys:
                pubkeys = [key['key'] for key in keys]
            pl_record['keys'] = pubkeys     

        record.update(pl_record)



    def fill_record_sfa_info(self, record):
        sfa_info = {}
        type = record['type']
        table = SfaTable()
        if (type == "slice"):
            person_ids = record.get("person_ids", [])
            persons = table.find({'type': 'user', 'pointer': person_ids})
            researchers = [person['hrn'] for person in persons]
            sfa_info['researcher'] = researchers

        elif (type == "authority"):
            person_ids = record.get("person_ids", [])
            persons = table.find({'type': 'user', 'pointer': person_ids})
            persons_dict = {}
            for person in persons:
                persons_dict[person['pointer']] = person 
            pl_persons = self.plshell.GetPersons(self.plauth, person_ids, ['person_id', 'roles'])
            pis, techs, admins = [], [], []
            for person in pl_persons:
                pointer = person['person_id']
                
                if pointer not in persons_dict:
                    # this means there is not sfa record for this user
                    continue    
                hrn = persons_dict[pointer]['hrn']    
                if 'pi' in person['roles']:
                    pis.append(hrn)
                if 'tech' in person['roles']:
                    techs.append(hrn)
                if 'admin' in person['roles']:
                    admins.append(hrn)
            
            sfa_info['PI'] = pis
            sfa_info['operator'] = techs
            sfa_info['owner'] = admins
            # xxx TODO: OrganizationName

        elif (type == "node"):
            sfa_info['dns'] = record.get("hostname", "")
            # xxx TODO: URI, LatLong, IP, DNS
    
        elif (type == "user"):
            sfa_info['email'] = record.get("email", "")
            # xxx TODO: PostalAddress, Phone

        record.update(sfa_info)

    def fill_record_info(self, record):
        """
        Given a SFA record, fill in the PLC specific and SFA specific
        fields in the record. 
        """
        self.fill_record_pl_info(record)
        self.fill_record_sfa_info(record)

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
        table = SfaTable()
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

    def __init__(self, config = "/etc/sfa/sfa_config", encoding = "utf-8", methods='sfa.methods',
                 peer_cert = None, interface = None, key_file = None, cert_file = None):

        BaseAPI.__init__(self, config=config, encoding=encoding, methods=methods, peer_cert=peer_cert,
                         interface=interface, key_file=key_file, cert_file=cert_file)
        self.encoding = encoding

        # Better just be documenting the API
        if config is None:
            return

        self.nodemanager = NodeManager(config)

    def sliver_exists(self):
        sliver_dict = self.nodemanager.GetXIDs()
        if slicename in sliver_dict.keys():
            return True
        else:
            return False
