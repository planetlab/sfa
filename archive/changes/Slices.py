from types import StringTypes
import time
import re

from PLC.Faults import *
from PLC.Parameter import Parameter, Mixed
from PLC.Filter import Filter
from PLC.Debug import profile
from PLC.Table import Row, Table
from PLC.SliceInstantiations import SliceInstantiation, SliceInstantiations
from PLC.Nodes import Node
from PLC.Persons import Person, Persons
from PLC.SliceAttributes import SliceAttribute

class Slice(Row):
    """
    Representation of a row in the slices table. To use, optionally
    instantiate with a dict of values. Update as you would a
    dict. Commit to the database with sync().To use, instantiate
    with a dict of values.
    """

    table_name = 'slices'
    primary_key = 'slice_id'
    join_tables = ['slice_node', 'slice_person', 'slice_attribute', 'peer_slice', 'node_slice_whitelist']
    fields = {
        'slice_id': Parameter(int, "Slice identifier"),
        'site_id': Parameter(int, "Identifier of the site to which this slice belongs"),
        'name': Parameter(str, "Slice name", max = 32),
        'instantiation': Parameter(str, "Slice instantiation state"),
        'url': Parameter(str, "URL further describing this slice", max = 254, nullok = True),
        'description': Parameter(str, "Slice description", max = 2048, nullok = True),
        'max_nodes': Parameter(int, "Maximum number of nodes that can be assigned to this slice"),
        'creator_person_id': Parameter(int, "Identifier of the account that created this slice"),
        'created': Parameter(int, "Date and time when slice was created, in seconds since UNIX epoch", ro = True),
        'expires': Parameter(int, "Date and time when slice expires, in seconds since UNIX epoch"),
	'uuid': Parameter(str, "Universal Unique Identifier"),
        'node_ids': Parameter([int], "List of nodes in this slice", ro = True),
        'person_ids': Parameter([int], "List of accounts that can use this slice", ro = True),
        'slice_attribute_ids': Parameter([int], "List of slice attributes", ro = True),
        'peer_id': Parameter(int, "Peer to which this slice belongs", nullok = True),
        'peer_slice_id': Parameter(int, "Foreign slice identifier at peer", nullok = True),
        }
    related_fields = {
	'persons': [Mixed(Parameter(int, "Person identifier"),
			  Parameter(str, "Email address"))],
	'nodes': [Mixed(Parameter(int, "Node identifier"),
		        Parameter(str, "Fully qualified hostname"))]
   	}
    # for Cache
    class_key = 'name'
    foreign_fields = ['instantiation', 'url', 'description', 'max_nodes', 'expires', 'uuid']
    foreign_xrefs = [
        {'field': 'node_ids' ,         'class': 'Node',   'table': 'slice_node' },
	{'field': 'person_ids',        'class': 'Person', 'table': 'slice_person'},
	{'field': 'creator_person_id', 'class': 'Person', 'table': 'unused-on-direct-refs'},
        {'field': 'site_id',           'class': 'Site',   'table': 'unused-on-direct-refs'},
    ]
    # forget about this one, it is read-only anyway
    # handling it causes Cache to re-sync all over again 
    # 'created'

    def validate_name(self, name):
        # N.B.: Responsibility of the caller to ensure that login_base
        # portion of the slice name corresponds to a valid site, if
        # desired.

        # 1. Lowercase.
        # 2. Begins with login_base (letters or numbers).
        # 3. Then single underscore after login_base.
        # 4. Then letters, numbers, or underscores.
        good_name = r'^[a-z0-9]+_[a-zA-Z0-9_]+$'
        if not name or \
           not re.match(good_name, name):
            raise PLCInvalidArgument, "Invalid slice name"

        conflicts = Slices(self.api, [name])
        for slice in conflicts:
            if 'slice_id' not in self or self['slice_id'] != slice['slice_id']:
                raise PLCInvalidArgument, "Slice name already in use, %s"%name

        return name

    def validate_instantiation(self, instantiation):
        instantiations = [row['instantiation'] for row in SliceInstantiations(self.api)]
        if instantiation not in instantiations:
            raise PLCInvalidArgument, "No such instantiation state"

        return instantiation

    validate_created = Row.validate_timestamp

    def validate_expires(self, expires):
        # N.B.: Responsibility of the caller to ensure that expires is
        # not too far into the future.
        check_future = not ('is_deleted' in self and self['is_deleted'])
        return Row.validate_timestamp(self, expires, check_future = check_future)

    add_person = Row.add_object(Person, 'slice_person')
    remove_person = Row.remove_object(Person, 'slice_person')

    add_node = Row.add_object(Node, 'slice_node')
    remove_node = Row.remove_object(Node, 'slice_node')

    add_to_node_whitelist = Row.add_object(Node, 'node_slice_whitelist')
    delete_from_node_whitelist = Row.remove_object(Node, 'node_slice_whitelist')

    def associate_persons(self, auth, field, value):
        """
        Adds persons found in value list to this slice (using AddPersonToSlice).
	Deletes persons not found in value list from this slice (using DeletePersonFromSlice).
        """
	
	assert 'person_ids' in self
	assert 'slice_id' in self
        assert isinstance(value, list)

	(person_ids, emails) = self.separate_types(value)[0:2]

	# Translate emails into person_ids	
	if emails:
	    persons = Persons(self.api, emails, ['person_id']).dict('person_id')
	    person_ids += persons.keys()
	
	# Add new ids, remove stale ids
        if self['person_ids'] != person_ids:
            from PLC.Methods.AddPersonToSlice import AddPersonToSlice
            from PLC.Methods.DeletePersonFromSlice import DeletePersonFromSlice
            new_persons = set(person_ids).difference(self['person_ids'])
            stale_persons = set(self['person_ids']).difference(person_ids)

            for new_person in new_persons:
                AddPersonToSlice.__call__(AddPersonToSlice(self.api), auth, new_person, self['slice_id'])
            for stale_person in stale_persons:
                DeletePersonFromSlice.__call__(DeletePersonFromSlice(self.api), auth, stale_person, self['slice_id'])

    def associate_nodes(self, auth, field, value):
	"""
	Adds nodes found in value list to this slice (using AddSliceToNodes).
	Deletes nodes not found in value list from this slice (using DeleteSliceFromNodes).
	"""

        from PLC.Nodes import Nodes

	assert 'node_ids' in self
	assert 'slice_id' in self
	assert isinstance(value, list)
	
	(node_ids, hostnames) = self.separate_types(value)[0:2]
	
	# Translate hostnames into node_ids
	if hostnames:
	    nodes = Nodes(self.api, hostnames, ['node_id']).dict('node_id')
	    node_ids += nodes.keys()
	
	# Add new ids, remove stale ids
	if self['node_ids'] != node_ids:
	    from PLC.Methods.AddSliceToNodes import AddSliceToNodes
	    from PLC.Methods.DeleteSliceFromNodes import DeleteSliceFromNodes
	    new_nodes = set(node_ids).difference(self['node_ids'])
	    stale_nodes = set(self['node_ids']).difference(node_ids)
	    
	    if new_nodes:
		AddSliceToNodes.__call__(AddSliceToNodes(self.api), auth, self['slice_id'], list(new_nodes))
	    if stale_nodes:
		DeleteSliceFromNodes.__call__(DeleteSliceFromNodes(self.api), auth, self['slice_id'], list(stale_nodes))			
    def associate_slice_attributes(self, auth, fields, value):
	"""
	Deletes slice_attribute_ids not found in value list (using DeleteSliceAttribute). 
	Adds slice_attributes if slice_fields w/o slice_id is found (using AddSliceAttribute).
	Updates slice_attribute if slice_fields w/ slice_id is found (using UpdateSlceiAttribute).  
	"""
	
	assert 'slice_attribute_ids' in self
	assert isinstance(value, list)

	(attribute_ids, blank, attributes) = self.separate_types(value)
	
	# There is no way to add attributes by id. They are
	# associated with a slice when they are created.
	# So we are only looking to delete here 
	if self['slice_attribute_ids'] != attribute_ids:
	    from PLC.Methods.DeleteSliceAttribute import DeleteSliceAttribute
	    stale_attributes = set(self['slice_attribute_ids']).difference(attribute_ids)
	
	    for stale_attribute in stale_attributes:
		DeleteSliceAttribute.__call__(DeleteSliceAttribute(self.api), auth, stale_attribute['slice_attribute_id'])	 	
	
	# If dictionary exists, we are either adding new
        # attributes or updating existing ones.
        if attributes:
            from PLC.Methods.AddSliceAttribute import AddSliceAttribute
            from PLC.Methods.UpdateSliceAttribute import UpdateSliceAttribute
	
	    added_attributes = filter(lambda x: 'slice_attribute_id' not in x, attributes)
	    updated_attributes = filter(lambda x: 'slice_attribute_id' in x, attributes)

	    for added_attribute in added_attributes:
		if 'attribute_type' in added_attribute:
		    type = added_attribute['attribute_type']
		elif 'attribute_type_id' in added_attribute:
		    type = added_attribute['attribute_type_id']
		else:
		    raise PLCInvalidArgument, "Must specify attribute_type or attribute_type_id"

		if 'value' in added_attribute:
		    value = added_attribute['value']
		else:
		    raise PLCInvalidArgument, "Must specify a value"
		
		if 'node_id' in added_attribute:
		    node_id = added_attribute['node_id']
		else:
		    node_id = None

		if 'nodegroup_id' in added_attribute:
		    nodegroup_id = added_attribute['nodegroup_id']
		else:
		    nodegroup_id = None 
 
		AddSliceAttribute.__call__(AddSliceAttribute(self.api), auth, self['slice_id'], type, value, node_id, nodegroup_id)
	    for updated_attribute in updated_attributes:
		attribute_id = updated_attribute.pop('slice_attribute_id')
		if attribute_id not in self['slice_attribute_ids']:
		    raise PLCInvalidArgument, "Attribute doesnt belong to this slice" 
		else:
		    UpdateSliceAttribute.__call__(UpdateSliceAttribute(self.api), auth, attribute_id, updated_attribute)	 	 
	
    def sync(self, commit = True):
        """
        Add or update a slice.
        """

        # Before a new slice is added, delete expired slices
        if 'slice_id' not in self:
            expired = Slices(self.api, expires = -int(time.time()))
            for slice in expired:
                slice.delete(commit)

        Row.sync(self, commit)

    def delete(self, commit = True):
        """
        Delete existing slice.
        """

        assert 'slice_id' in self

        # Clean up miscellaneous join tables
        for table in self.join_tables:
            self.api.db.do("DELETE FROM %s WHERE slice_id = %d" % \
                           (table, self['slice_id']))

        # Mark as deleted
        self['is_deleted'] = True
        self.sync(commit)


class Slices(Table):
    """
    Representation of row(s) from the slices table in the
    database.
    """

    def __init__(self, api, slice_filter = None, columns = None, expires = int(time.time())):
        Table.__init__(self, api, Slice, columns)

        sql = "SELECT %s FROM view_slices WHERE is_deleted IS False" % \
              ", ".join(self.columns)

        if expires is not None:
            if expires >= 0:
                sql += " AND expires > %d" % expires
            else:
                expires = -expires
                sql += " AND expires < %d" % expires

        if slice_filter is not None:
            if isinstance(slice_filter, (list, tuple, set)):
                # Separate the list into integers and strings
                ints = filter(lambda x: isinstance(x, (int, long)), slice_filter)
                strs = filter(lambda x: isinstance(x, StringTypes), slice_filter)
                slice_filter = Filter(Slice.fields, {'slice_id': ints, 'name': strs})
                sql += " AND (%s) %s" % slice_filter.sql(api, "OR")
            elif isinstance(slice_filter, dict):
                slice_filter = Filter(Slice.fields, slice_filter)
                sql += " AND (%s) %s" % slice_filter.sql(api, "AND")
            elif isinstance (slice_filter, StringTypes):
                slice_filter = Filter(Slice.fields, {'name':[slice_filter]})
                sql += " AND (%s) %s" % slice_filter.sql(api, "AND")
            elif isinstance (slice_filter, int):
                slice_filter = Filter(Slice.fields, {'slice_id':[slice_filter]})
                sql += " AND (%s) %s" % slice_filter.sql(api, "AND")
            else:
                raise PLCInvalidArgument, "Wrong slice filter %r"%slice_filter

        self.selectall(sql)
