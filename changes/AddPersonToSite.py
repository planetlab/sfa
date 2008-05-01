from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Persons import Person, Persons
from PLC.Sites import Site, Sites
from PLC.Auth import Auth
import sys		###########################soner
sys.path.append('../../../../util')
from pl_to_geni import *
from util import *
from db import *

class AddPersonToSite(Method):
    """
    Adds the specified person to the specified site. If the person is
    already a member of the site, no errors are returned. Does not
    change the person's primary site.

    Returns 1 if successful, faults otherwise.
    """

    roles = ['admin']

    accepts = [
        Auth(),
        Mixed(Person.fields['person_id'],
              Person.fields['email']),
        Mixed(Site.fields['site_id'],
              Site.fields['login_base'])
        ]

    returns = Parameter(int, '1 if successful')

    def call(self, auth, person_id_or_email, site_id_or_login_base):
        # Get account information
        persons = Persons(self.api, [person_id_or_email])
        if not persons:
            raise PLCInvalidArgument, "No such account"
        person = persons[0]

        if person['peer_id'] is not None:
            raise PLCInvalidArgument, "Not a local account"

        # Get site information
        sites = Sites(self.api, [site_id_or_login_base])
        if not sites:
            raise PLCInvalidArgument, "No such site"
        site = sites[0]

        if site['peer_id'] is not None:
            raise PLCInvalidArgument, "Not a local site"

        if site['site_id'] not in person['site_ids']:
            site.add_person(person)

	# Logging variables
	self.event_objects = {'Site': [site['site_id']],
			      'Person': [person['person_id']]}
	self.message = 'Person %d added to site %d' % \
		(person['person_id'], site['site_id'])
		
	#insert the record into GENI tables        ###################soner
	(global_sr_tree, global_cr_tree) = get_tree_globals()
	(site_id, site_hrn) = site_to_auth(site_id_or_login_base)
	dbinfo = determine_dbinfo(site_hrn, global_sr_tree)
	if dbinfo == None:
		raise PLCInvalidArgument, "No GENI authority corresponding to the site "+site['name']
	cnx = dbinfo[0]
	tablename = dbinfo[1]
	
	new_hrn = person_to_user(person['email'])
	existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ")
	if existing != None:
		new_hrn = person_to_user(person['email'], 1)
		existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ")
		if existing != None:
			new_hrn = person_to_user(person['email'], 2)
	
	geni_record = {'hrn':''}
	geni_record["hrn"] = new_hrn
	geni_record["type"] = 'user'
	geni_record['pointer'] = person['person_id']
	
        querystr = generate_querystr('INSERT', tablename, geni_record)
        cnx.query(querystr)
	
	return 1
