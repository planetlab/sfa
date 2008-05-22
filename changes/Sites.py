from types import StringTypes
import string

from PLC.Faults import *
from PLC.Parameter import Parameter, Mixed
from PLC.Filter import Filter
from PLC.Debug import profile
from PLC.Table import Row, Table
from PLC.Slices import Slice, Slices
from PLC.PCUs import PCU, PCUs
from PLC.Nodes import Node, Nodes
from PLC.Addresses import Address, Addresses
from PLC.Persons import Person, Persons

class Site(Row):
    """
    Representation of a row in the sites table. To use, optionally
    instantiate with a dict of values. Update as you would a
    dict. Commit to the database with sync().
    """

    table_name = 'sites'
    primary_key = 'site_id'
    join_tables = ['person_site', 'site_address', 'peer_site']
    fields = {
        'site_id': Parameter(int, "Site identifier"),
        'name': Parameter(str, "Full site name", max = 254),
        'abbreviated_name': Parameter(str, "Abbreviated site name", max = 50),
        'login_base': Parameter(str, "Site slice prefix", max = 20),
        'is_public': Parameter(bool, "Publicly viewable site"),
        'enabled': Parameter(bool, "Has been enabled"),
	'latitude': Parameter(float, "Decimal latitude of the site", min = -90.0, max = 90.0, nullok = True),
        'longitude': Parameter(float, "Decimal longitude of the site", min = -180.0, max = 180.0, nullok = True),
        'url': Parameter(str, "URL of a page that describes the site", max = 254, nullok = True),
        'date_created': Parameter(int, "Date and time when site entry was created, in seconds since UNIX epoch", ro = True),
        'last_updated': Parameter(int, "Date and time when site entry was last updated, in seconds since UNIX epoch", ro = True),
        'max_slices': Parameter(int, "Maximum number of slices that the site is able to create"),
        'max_slivers': Parameter(int, "Maximum number of slivers that the site is able to create"),
	'uuid': Parameter(str, "Universal Unique Identifier"),
        'person_ids': Parameter([int], "List of account identifiers"),
        'slice_ids': Parameter([int], "List of slice identifiers"),
        'address_ids': Parameter([int], "List of address identifiers"),
        'pcu_ids': Parameter([int], "List of PCU identifiers"),
        'node_ids': Parameter([int], "List of site node identifiers"),
        'peer_id': Parameter(int, "Peer to which this site belongs", nullok = True),
        'peer_site_id': Parameter(int, "Foreign site identifier at peer", nullok = True),
	'ext_consortium_id': Parameter(int, "external consortium id", nullok = True)
        }
    related_fields = {
 	'persons': [Mixed(Parameter(int, "Person identifier"),
                          Parameter(str, "Email address"))],
	'addresses': [Mixed(Parameter(int, "Address identifer"),
                            Filter(Address.fields))]
	}
    # for Cache
    class_key = 'login_base'
    foreign_fields = ['abbreviated_name', 'name', 'is_public', 'latitude', 'longitude',
		      'url', 'max_slices', 'max_slivers', 'uuid', 
		      ]
    # forget about these ones, they are read-only anyway
    # handling them causes Cache to re-sync all over again 
    # 'last_updated', 'date_created'
    foreign_xrefs = []

    def validate_name(self, name):
        if not len(name):
            raise PLCInvalidArgument, "Name must be specified"

        return name

    validate_abbreviated_name = validate_name

    def validate_login_base(self, login_base):
        if not len(login_base):
            raise PLCInvalidArgument, "Login base must be specified"

        if not set(login_base).issubset(string.lowercase + string.digits):
            raise PLCInvalidArgument, "Login base must consist only of lowercase ASCII letters or numbers"

        conflicts = Sites(self.api, [login_base])
        for site in conflicts:
            if 'site_id' not in self or self['site_id'] != site['site_id']:
                raise PLCInvalidArgument, "login_base already in use"

        return login_base

    def validate_latitude(self, latitude):
        if not self.has_key('longitude') or \
           self['longitude'] is None:
            raise PLCInvalidArgument, "Longitude must also be specified"

        return latitude

    def validate_longitude(self, longitude):
        if not self.has_key('latitude') or \
           self['latitude'] is None:
            raise PLCInvalidArgument, "Latitude must also be specified"

        return longitude

    validate_date_created = Row.validate_timestamp
    validate_last_updated = Row.validate_timestamp

    add_person = Row.add_object(Person, 'person_site')
    remove_person = Row.remove_object(Person, 'person_site')

    add_address = Row.add_object(Address, 'site_address')
    remove_address = Row.remove_object(Address, 'site_address')

    def update_last_updated(self, commit = True):
        """
        Update last_updated field with current time
        """

        assert 'site_id' in self
        assert self.table_name

        self.api.db.do("UPDATE %s SET last_updated = CURRENT_TIMESTAMP " % (self.table_name) + \
                       " where site_id = %d" % (self['site_id']) )
        self.sync(commit)    


    def associate_persons(self, auth, field, value):
	"""
	Adds persons found in value list to this site (using AddPersonToSite).
	Deletes persons not found in value list from this site (using DeletePersonFromSite).
	"""
	
	assert 'person_ids' in self
	assert 'site_id' in self
	assert isinstance(value, list)

	(person_ids, emails) = self.separate_types(value)[0:2]

	# Translate emails into person_ids
	if emails:
	    persons = Persons(self.api, emails, ['person_id']).dict('person_id')
	    person_ids += persons.keys()

	# Add new ids, remove stale ids
	if self['person_ids'] != person_ids:
	    from PLC.Methods.AddPersonToSite import AddPersonToSite
	    from PLC.Methods.DeletePersonFromSite import DeletePersonFromSite
	    new_persons = set(person_ids).difference(self['person_ids'])
	    stale_persons = set(self['person_ids']).difference(person_ids)
	 
	    for new_person in new_persons:
		AddPersonToSite.__call__(AddPersonToSite(self.api), auth, new_person, self['site_id'])
	    for stale_person in stale_persons:
		DeletePersonFromSite.__call__(DeletePersonFromSite(self.api), auth, stale_person, self['site_id'])		

    def associate_addresses(self, auth, field, value):
	"""
	Deletes addresses_ids not found in value list (using DeleteAddress).  
	Adds address if slice_fields w/o address_id found in value list (using AddSiteAddress).
	Update address if slice_fields w/ address_id found in value list (using UpdateAddress).
	"""
	
	assert 'address_ids' in self
	assert 'site_id' in self
        assert isinstance(value, list)

        (address_ids, blank, addresses) = self.separate_types(value)

	for address in addresses:
	    if 'address_id' in address:
		address_ids.append(address['address_id']) 		

        # Add new ids, remove stale ids
        if self['address_ids'] != address_ids:
            from PLC.Methods.DeleteAddress import DeleteAddress
            stale_addresses = set(self['address_ids']).difference(address_ids)

            for stale_address in stale_addresses:
                DeleteAddress.__call__(DeleteAddress(self.api), auth, stale_address)	
	
	if addresses:
	    from PLC.Methods.AddSiteAddress import AddSiteAddress
	    from PLC.Methods.UpdateAddress import UpdateAddress
		
	    updated_addresses = filter(lambda address: 'address_id' in address, addresses)
	    added_addresses = filter(lambda address: 'address_id' not in address, addresses)
		
	    for address in added_addresses:
		AddSiteAddress.__call__(AddSiteAddress(self.api), auth, self['site_id'], address)	
    	    for address in updated_addresses:
		address_id = address.pop('address_id')
		UpdateAddress.__call__(UpdateAddress(self.api), auth, address_id, address)

    def delete(self, commit = True):
        """
        Delete existing site.
        """

        assert 'site_id' in self

        # Delete accounts of all people at the site who are not
        # members of at least one other non-deleted site.
        persons = Persons(self.api, self['person_ids'])
        for person in persons:
            delete = True

            person_sites = Sites(self.api, person['site_ids'])
            for person_site in person_sites:
                if person_site['site_id'] != self['site_id']:
                    delete = False
                    break

            if delete:
                person.delete(commit = False)

        # Delete all site addresses
        addresses = Addresses(self.api, self['address_ids'])
        for address in addresses:
            address.delete(commit = False)

        # Delete all site slices
        slices = Slices(self.api, self['slice_ids'])
        for slice in slices:
            slice.delete(commit = False)

        # Delete all site PCUs
        pcus = PCUs(self.api, self['pcu_ids'])
        for pcu in pcus:
            pcu.delete(commit = False)

        # Delete all site nodes
        nodes = Nodes(self.api, self['node_ids'])
        for node in nodes:
            node.delete(commit = False)

        # Clean up miscellaneous join tables
        for table in self.join_tables:
            self.api.db.do("DELETE FROM %s WHERE site_id = %d" % \
                           (table, self['site_id']))

        # Mark as deleted
        self['deleted'] = True
        self.sync(commit)

class Sites(Table):
    """
    Representation of row(s) from the sites table in the
    database.
    """

    def __init__(self, api, site_filter = None, columns = None):
        Table.__init__(self, api, Site, columns)

        sql = "SELECT %s FROM view_sites WHERE deleted IS False" % \
              ", ".join(self.columns)

        if site_filter is not None:
            if isinstance(site_filter, (list, tuple, set)):
                # Separate the list into integers and strings
                ints = filter(lambda x: isinstance(x, (int, long)), site_filter)
                strs = filter(lambda x: isinstance(x, StringTypes), site_filter)
                site_filter = Filter(Site.fields, {'site_id': ints, 'login_base': strs})
                sql += " AND (%s) %s" % site_filter.sql(api, "OR")
            elif isinstance(site_filter, dict):
                site_filter = Filter(Site.fields, site_filter)
                sql += " AND (%s) %s" % site_filter.sql(api, "AND")
            elif isinstance (site_filter, StringTypes):
                site_filter = Filter(Site.fields, {'login_base':[site_filter]})
                sql += " AND (%s) %s" % site_filter.sql(api, "AND")
            elif isinstance (site_filter, int):
                site_filter = Filter(Site.fields, {'site_id':[site_filter]})
                sql += " AND (%s) %s" % site_filter.sql(api, "AND")
            else:
                raise PLCInvalidArgument, "Wrong site filter %r"%site_filter

        self.selectall(sql)
