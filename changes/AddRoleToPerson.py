from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Persons import Person, Persons
from PLC.Auth import Auth
from PLC.Roles import Role, Roles
import sys   	##################################soners
sys.path.append('../../../../util')
from pl_to_geni import *
from util import *
from db import *

class AddRoleToPerson(Method):
    """
    Grants the specified role to the person.
    
    PIs can only grant the tech and user roles to users and techs at
    their sites. Admins can grant any role to any user.

    Returns 1 if successful, faults otherwise.
    """

    roles = ['admin', 'pi']

    accepts = [
        Auth(),
        Mixed(Role.fields['role_id'],
              Role.fields['name']),
        Mixed(Person.fields['person_id'],
              Person.fields['email']),
        ]

    returns = Parameter(int, '1 if successful')

    def call(self, auth, role_id_or_name, person_id_or_email):
        # Get role
        roles = Roles(self.api, [role_id_or_name])
        if not roles:
            raise PLCInvalidArgument, "Invalid role '%s'" % unicode(role_id_or_name)
        role = roles[0]

        # Get account information
        persons = Persons(self.api, [person_id_or_email])
        if not persons:
            raise PLCInvalidArgument, "No such account"
        person = persons[0]

        if person['peer_id'] is not None:
            raise PLCInvalidArgument, "Not a local account"

        # Authenticated function
        assert self.caller is not None

        # Check if we can update this account
        if not self.caller.can_update(person):
            raise PLCPermissionDenied, "Not allowed to update specified account"

        # Can only grant lesser (higher) roles to others
        if 'admin' not in self.caller['roles'] and \
           role['role_id'] <= min(self.caller['role_ids']):
            raise PLCInvalidArgument, "Not allowed to grant that role"

        if role['role_id'] not in person['role_ids']:
            person.add_role(role)

	self.event_objects = {'Person': [person['person_id']],
			      'Role': [role['role_id']]}
	self.message = "Role %d granted to person %d" % \
                       (role['role_id'], person['person_id'])

	#erase the GENI rights so that PL will not be imcompatible with GENI ############################soners
	(global_sr_tree, global_cr_tree) = get_tree_globals()
	cnx = get_plDB_conn()
	site_ids = cnx.query("SELECT site_id FROM person_slice WHERE person_id = "+person['person_id'])
	for sid in site_ids:
		(site_id, site_hrn) = site_to_auth(sid)
		dbinfo = determine_dbinfo(site_hrn, global_sr_tree)
		if dbinfo == None:
			raise PLCInvalidArgument, "No GENI authority corresponding to the site"
		cnx = dbinfo[0]
		tablename = dbinfo[1]
		
		querystr = "UPDATE "+tablename+" SET rights = '' WHERE pointer = "+person['person_id']
		cnx.query(querystr)

        return 1
