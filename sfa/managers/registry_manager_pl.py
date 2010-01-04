import types
import time 
from sfa.server.registry import Registries
from sfa.util.prefixTree import prefixTree
from sfa.util.record import GeniRecord
from sfa.util.genitable import GeniTable
from sfa.util.record import GeniRecord
from sfa.util.genitable import GeniTable
from sfa.trust.gid import GID 
from sfa.util.namespace import *
from sfa.trust.credential import *
from sfa.trust.certificate import *
from sfa.util.faults import *

def get_credential(api, hrn, type, is_self=False):    
    # Is this a root or sub authority
    auth_hrn = api.auth.get_authority(hrn)
    if not auth_hrn or hrn == api.config.SFA_INTERFACE_HRN:
        auth_hrn = hrn
    # get record info
    auth_info = api.auth.get_auth_info(auth_hrn)
    table = GeniTable()
    records = table.findObjects({'type': type, 'hrn': hrn})
    if not records:
        raise RecordNotFound(hrn)
    record = records[0]

    # verify_cancreate_credential requires that the member lists
    # (researchers, pis, etc) be filled in
    api.fill_record_info(record)

    # get the callers gid
    # if this is a self cred the record's gid is the caller's gid
    if is_self:
        caller_hrn = hrn
        caller_gid = record.get_gid_object()
    else:
        caller_gid = api.auth.client_cred.get_gid_caller() 
        caller_hrn = caller_gid.get_hrn()
    
    object_hrn = record.get_gid_object().get_hrn()
    rights = api.auth.determine_user_rights(caller_hrn, record)
    # make sure caller has rights to this object
    if rights.is_empty():
        raise PermissionError(caller_hrn + " has no rights to " + record['name'])

    object_gid = GID(string=record['gid'])
    new_cred = Credential(subject = object_gid.get_subject())
    new_cred.set_gid_caller(caller_gid)
    new_cred.set_gid_object(object_gid)
    new_cred.set_issuer(key=auth_info.get_pkey_object(), subject=auth_hrn)
    new_cred.set_pubkey(object_gid.get_pubkey())
    new_cred.set_privileges(rights)
    new_cred.set_delegate(True)
    auth_kind = "authority,ma,sa"
    new_cred.set_parent(api.auth.hierarchy.get_auth_cred(auth_hrn, kind=auth_kind))
    new_cred.encode()
    new_cred.sign()

    return new_cred.save_to_string(save_parents=True)

def resolve(api, hrns, type=None, origin_hrn=None):

    # load all know registry names into a prefix tree and attempt to find
    # the longest matching prefix
    if not isinstance(hrns, types.ListType):
        hrns = [hrns]
    
    # create a dict whre key is an registry hrn and its value is a
    # hrns at that registry (determined by the known prefix tree).  
    hrn_dict = {}
    registries = Registries(api)
    tree = prefixTree()
    registry_hrns = registries.keys()
    tree.load(registry_hrns)
    for hrn in hrns:
        registry_hrn = tree.best_match(hrn)
        if registry_hrn not in hrn_dict:
            hrn_dict[registry_hrn] = []
        hrn_dict[registry_hrn].append(hrn)
        
    records = [] 
    for registry_hrn in hrn_dict:
        # skip the hrn without a registry hrn
        # XX should we let the user know the authority is unknown?       
        if not registry_hrn:
            continue

        # if the best match (longest matching hrn) is not the local registry,
        # forward the request
        hrns = hrn_dict[registry_hrn]
        if registry_hrn != api.hrn:
            credential = api.getCredential()
            peer_records = registries[registry_hrn].resolve(credential, hrn, origin_hrn)
            records.extend([GeniRecord(dict=record).as_dict() for record in peer_records])

    # try resolving the remaining unfound records at the local registry
    remaining_hrns = set(hrns).difference([record['hrn'] for record in records])
    remaining_hrns = [hrn for hrn in remaining_hrns] 
    table = GeniTable()
    local_records = table.findObjects({'hrn': remaining_hrns})
    for record in local_records:
        try:
            api.fill_record_info(record)
            records.append(dict(record))
        except PlanetLabRecordDoesNotExist:
            # silently drop the ones that are missing in PL
            print >> log, "ignoring geni record ", record['hrn'], \
                              " because pl record does not exist"    
            table.remove(record)

    if not records:
        raise RecordNotFound(str(hrns))

    if type:
        records = filter(lambda rec: rec['type'] in [type], records)

    return records

def list(api, hrn):
    # load all know registry names into a prefix tree and attempt to find
    # the longest matching prefix
    records = []
    registries = Registries(api)
    hrns = registries.keys()
    tree = prefixTree()
    tree.load(hrns)
    registry_hrn = tree.best_match(hrn)
    
    #if there was no match then this record belongs to an unknow registry
    if not registry_hrn:
        raise MissingAuthority(hrn)
    
    # if the best match (longest matching hrn) is not the local registry,
    # forward the request
    records = []    
    if registry_hrn != api.hrn:
        credential = api.getCredential()
        record_list = registries[registry_hrn].list(credential, hrn, origin_hrn)
        records = [GeniRecord(dict=record).as_dict() for record in record_list]
    
    # if we still havnt found the record yet, try the local registry
    if not records:
        if not api.auth.hierarchy.auth_exists(hrn):
            raise MissingAuthority(hrn)

        table = GeniTable()
        records = table.find({'authority': hrn})

    return records


def register(api, record):

    hrn, type = record['hrn'], record['type']

    # validate the type
    if type not in ['authority', 'slice', 'node', 'user']:
        raise UnknownGeniType(type) 
    
    # check if record already exists
    table = GeniTable()
    existing_records = table.find({'type': type, 'hrn': hrn})
    if existing_records:
        raise ExistingRecord(hrn)
       
    record = GeniRecord(dict = record)
    record['authority'] = get_authority(record['hrn'])
    type = record['type']
    hrn = record['hrn']
    api.auth.verify_object_permission(hrn)
    auth_info = api.auth.get_auth_info(record['authority'])
    pub_key = None
    # make sure record has a gid
    if 'gid' not in record:
        uuid = create_uuid()
        pkey = Keypair(create=True)
        if 'key' in record and record['key']:
            if isinstance(record['key'], list):
                pub_key = record['key'][0]
            else:
                pub_key = record['key']
            pkey = convert_public_key(pub_key)

        gid_object = api.auth.hierarchy.create_gid(hrn, uuid, pkey)
        gid = gid_object.save_to_string(save_parents=True)
        record['gid'] = gid
        record.set_gid(gid)

    if type in ["authority"]:
        # update the tree
        if not api.auth.hierarchy.auth_exists(hrn):
            api.auth.hierarchy.create_auth(hrn)

        # get the GID from the newly created authority
        gid = auth_info.get_gid_object()
        record.set_gid(gid.save_to_string(save_parents=True))
        pl_record = api.geni_fields_to_pl_fields(type, hrn, record)
        sites = api.plshell.GetSites(api.plauth, [pl_record['login_base']])
        if not sites:
            pointer = api.plshell.AddSite(api.plauth, pl_record)
        else:
            pointer = sites[0]['site_id']

        record.set_pointer(pointer)
        record['pointer'] = pointer

    elif (type == "slice"):
        acceptable_fields=['url', 'instantiation', 'name', 'description']
        pl_record = api.geni_fields_to_pl_fields(type, hrn, record)
        for key in pl_record.keys():
            if key not in acceptable_fields:
                pl_record.pop(key)
            slices = api.plshell.GetSlices(api.plauth, [pl_record['name']])
            if not slices:
                pointer = api.plshell.AddSlice(api.plauth, pl_record)
            else:
                pointer = slices[0]['slice_id']
            record.set_pointer(pointer)
            record['pointer'] = pointer

    elif  (type == "user"):
        persons = api.plshell.GetPersons(api.plauth, [record['email']])
        if not persons:
            pointer = api.plshell.AddPerson(api.plauth, dict(record))
        else:
            pointer = persons[0]['person_id']

        if 'enabled' in record and record['enabled']:
            api.plshell.UpdatePerson(api.plauth, pointer, {'enabled': record['enabled']})
        # add this persons to the site only if he is being added for the first
        # time by sfa and doesont already exist in plc
        if not persons or not persons[0]['site_ids']:
            login_base = get_leaf(record['authority'])
            api.plshell.AddPersonToSite(api.plauth, pointer, login_base)

        # What roles should this user have?
        api.plshell.AddRoleToPerson(api.plauth, 'user', pointer)
        # Add the user's key
        if pub_key:
            api.plshell.AddPersonKey(api.plauth, pointer, {'key_type' : 'ssh', 'key' : pub_key})

    elif (type == "node"):
        pl_record = api.geni_fields_to_pl_fields(type, hrn, record)
        login_base = hrn_to_pl_login_base(record['authority'])
        nodes = api.plshell.GetNodes(api.plauth, [pl_record['hostname']])
        if not nodes:
            pointer = api.plshell.AddNode(api.plauth, login_base, pl_record)
        else:
            pointer = nodes[0]['node_id']

    record['pointer'] = pointer
    record.set_pointer(pointer)
    record_id = table.insert(record)
    record['record_id'] = record_id

    # update membership for researchers, pis, owners, operators
    api.update_membership(None, record)

    return record.get_gid_object().save_to_string(save_parents=True)

def update(api, record_dict):
    new_record = GeniRecord(dict = record_dict)
    type = new_record['type']
    hrn = new_record['hrn']
    api.auth.verify_object_permission(hrn)
    table = GeniTable()
    # make sure the record exists
    records = table.findObjects({'type': type, 'hrn': hrn})
    if not records:
        raise RecordNotFound(hrn)
    record = records[0]
    record['last_updated'] = time.gmtime()

    # Update_membership needs the membership lists in the existing record
    # filled in, so it can see if members were added or removed
    api.fill_record_info(record)

    # Use the pointer from the existing record, not the one that the user
    # gave us. This prevents the user from inserting a forged pointer
    pointer = record['pointer']
    # update the PLC information that was specified with the record

    if (type == "authority"):
        api.plshell.UpdateSite(api.plauth, pointer, new_record)

    elif type == "slice":
        pl_record=api.geni_fields_to_pl_fields(type, hrn, new_record)
        if 'name' in pl_record:
            pl_record.pop('name')
            api.plshell.UpdateSlice(api.plauth, pointer, pl_record)

    elif type == "user":
        # SMBAKER: UpdatePerson only allows a limited set of fields to be
        #    updated. Ideally we should have a more generic way of doing
        #    this. I copied the field names from UpdatePerson.py...
        update_fields = {}
        all_fields = new_record
        for key in all_fields.keys():
            if key in ['first_name', 'last_name', 'title', 'email',
                       'password', 'phone', 'url', 'bio', 'accepted_aup',
                       'enabled']:
                update_fields[key] = all_fields[key]
        api.plshell.UpdatePerson(api.plauth, pointer, update_fields)

        if 'key' in new_record and new_record['key']:
            # must check this key against the previous one if it exists
            persons = api.plshell.GetPersons(api.plauth, [pointer], ['key_ids'])
            person = persons[0]
            keys = person['key_ids']
            keys = api.plshell.GetKeys(api.plauth, person['key_ids'])
            key_exists = False
            if isinstance(new_record['key'], list):
                new_key = new_record['key'][0]
            else:
                new_key = new_record['key']
            
            # Delete all stale keys
            for key in keys:
                if new_record['key'] != key['key']:
                    api.plshell.DeleteKey(api.plauth, key['key_id'])
                else:
                    key_exists = True
            if not key_exists:
                api.plshell.AddPersonKey(api.plauth, pointer, {'key_type': 'ssh', 'key': new_key})

            # update the openssl key and gid
            pkey = convert_public_key(new_key)
            uuid = create_uuid()
            gid_object = api.auth.hierarchy.create_gid(hrn, uuid, pkey)
            gid = gid_object.save_to_string(save_parents=True)
            record['gid'] = gid
            record = GeniRecord(dict=record)
            table.update(record)

    elif type == "node":
        api.plshell.UpdateNode(api.plauth, pointer, new_record)

    else:
        raise UnknownGeniType(type)

    # update membership for researchers, pis, owners, operators
    api.update_membership(record, new_record)
    
    return 1 

def remove(api, hrn, type, origin_hrn=None):
    table = GeniTable()
    filter = {'hrn': hrn}
    if type not in ['all', '*']:
        filter['type'] = type
    records = table.find(filter)
    if not records:
        raise RecordNotFound(hrn)
    record = records[0]
    type = record['type']

    credential = api.getCredential()
    registries = Registries(api)

    # Try to remove the object from the PLCDB of federated agg.
    # This is attempted before removing the object from the local agg's PLCDB and sfa table
    if hrn.startswith(api.hrn) and type in ['user', 'slice', 'authority']:
        for registry in registries:
            if registry not in [api.hrn]:
                try:
                    result=registries[registry].remove_peer_object(credential, record, origin_hrn)
                except:
                    pass
    if type == "user":
        persons = api.plshell.GetPersons(api.plauth, record['pointer'])
        # only delete this person if he has site ids. if he doesnt, it probably means
        # he was just removed from a site, not actually deleted
        if persons and persons[0]['site_ids']:
            api.plshell.DeletePerson(api.plauth, record['pointer'])
    elif type == "slice":
        if api.plshell.GetSlices(api.plauth, record['pointer']):
            api.plshell.DeleteSlice(api.plauth, record['pointer'])
    elif type == "node":
        if api.plshell.GetNodes(api.plauth, record['pointer']):
            api.plshell.DeleteNode(api.plauth, record['pointer'])
    elif type == "authority":
        if api.plshell.GetSites(api.plauth, record['pointer']):
            api.plshell.DeleteSite(api.plauth, record['pointer'])
    else:
        raise UnknownGeniType(type)

    table.remove(record)

    return 1

def remove_peer_object(api, record, origin_hrn=None):
    pass

def register_peer_object(api, record, origin_hrn=None):
    pass