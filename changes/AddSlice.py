import re

from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Slices import Slice, Slices
from PLC.Auth import Auth
from PLC.Sites import Site, Sites
import uuid ##################################soners
import sys
sys.path.append('../../../../util')
from pl_to_geni import *
from util import *
from db import *

can_update = lambda (field, value): field in \
             ['name', 'instantiation', 'url', 'description', 'max_nodes', 'uuid']

class AddSlice(Method):
    """
    Adds a new slice. Any fields specified in slice_fields are used,
    otherwise defaults are used.

    Valid slice names are lowercase and begin with the login_base
    (slice prefix) of a valid site, followed by a single
    underscore. Thereafter, only letters, numbers, or additional
    underscores may be used.

    PIs may only add slices associated with their own sites (i.e.,
    slice prefixes must always be the login_base of one of their
    sites).

    Returns the new slice_id (> 0) if successful, faults otherwise.
    """

    roles = ['admin', 'pi']

    slice_fields = dict(filter(can_update, Slice.fields.items()))

    accepts = [
        Auth(),
        slice_fields
        ]

    returns = Parameter(int, 'New slice_id (> 0) if successful')

    def call(self, auth, slice_fields):
        slice_fields = dict(filter(can_update, slice_fields.items()))

        # 1. Lowercase.
        # 2. Begins with login_base (letters or numbers).
        # 3. Then single underscore after login_base.
        # 4. Then letters, numbers, or underscores.
        name = slice_fields['name']
        good_name = r'^[a-z0-9]+_[a-zA-Z0-9_]+$'
        if not name or \
           not re.match(good_name, name):
            raise PLCInvalidArgument, "Invalid slice name"

        # Get associated site details
        login_base = name.split("_")[0]
        sites = Sites(self.api, [login_base])
        if not sites:
            raise PLCInvalidArgument, "Invalid slice prefix %s in %s"%(login_base,name)
        site = sites[0]

        if 'admin' not in self.caller['roles']:
            if site['site_id'] not in self.caller['site_ids']:
                raise PLCPermissionDenied, "Slice prefix %s must be the same as the login_base of one of your sites"%login_base

        if len(site['slice_ids']) >= site['max_slices']:
            raise PLCInvalidArgument, "Site %s has reached (%d) its maximum allowable slice count (%d)"%(site['name'],
                                                                                                         len(site['slice_ids']),
                                                                                                         site['max_slices'])

	if not site['enabled']:
	    raise PLCInvalidArgument, "Site %s is disabled can cannot create slices" % (site['name'])
	 
        slice = Slice(self.api, slice_fields)
        slice['creator_person_id'] = self.caller['person_id']
        slice['site_id'] = site['site_id']
	slice['uuid'] = str(uuid.uuid4().int)###############################soner
	
        slice.sync()

	self.event_objects = {'Slice': [slice['slice_id']]}

	#insert the record into GENI tables  ###############################soner
	(global_sr_tree, global_cr_tree) = get_tree_globals()
	(site_id, site_hrn) = site_to_auth(site['site_id'])
	dbinfo = determine_dbinfo(site_hrn, global_sr_tree)
	if dbinfo == None:
		raise PLCInvalidArgument, "No GENI authority corresponding to the site "+site['name']
	cnx = dbinfo[0]
	tablename = dbinfo[1]
	
	new_hrn = plslice_to_slice(slice['name'])	
	geni_record = {'hrn':''}
	geni_record["hrn"] = new_hrn
	geni_record["type"] = 'slice'
	geni_record['pointer'] = slice['slice_id']
	
        querystr = generate_querystr('INSERT', tablename, geni_record)
        cnx.query(querystr)
	
        return slice['slice_id']
