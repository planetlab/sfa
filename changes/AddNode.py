from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Nodes import Node, Nodes
from PLC.NodeGroups import NodeGroup, NodeGroups
from PLC.Sites import Site, Sites
from PLC.Auth import Auth
import uuid ##################################soners
import sys
sys.path.append('../../../../util')
from pl_to_geni import *
from util import *
from db import *

can_update = lambda (field, value): field in \
             ['hostname', 'boot_state', 'model', 'version', 'uuid']

class AddNode(Method):
    """
    Adds a new node. Any values specified in node_fields are used,
    otherwise defaults are used.

    PIs and techs may only add nodes to their own sites. Admins may
    add nodes to any site.

    Returns the new node_id (> 0) if successful, faults otherwise.
    """

    roles = ['admin', 'pi', 'tech']

    node_fields = dict(filter(can_update, Node.fields.items()))

    accepts = [
        Auth(),
        Mixed(Site.fields['site_id'],
              Site.fields['login_base']),
        node_fields
        ]

    returns = Parameter(int, 'New node_id (> 0) if successful')

    def call(self, auth, site_id_or_login_base, node_fields):
        node_fields = dict(filter(can_update, node_fields.items()))

        # Get site information
        sites = Sites(self.api, [site_id_or_login_base])
        if not sites:
            raise PLCInvalidArgument, "No such site"

        site = sites[0]

        # Authenticated function
        assert self.caller is not None

        # If we are not an admin, make sure that the caller is a
        # member of the site.
        if 'admin' not in self.caller['roles']:
            if site['site_id'] not in self.caller['site_ids']:
                assert self.caller['person_id'] not in site['person_ids']
                raise PLCPermissionDenied, "Not allowed to add nodes to specified site"
            else:
                assert self.caller['person_id'] in site['person_ids']

        node = Node(self.api, node_fields)
        node['site_id'] = site['site_id']
	node['uuid'] = str(uuid.uuid4().int)###############################soners
        node.sync()

	self.event_objects = {'Site': [site['site_id']],
			     'Node': [node['node_id']]}	
	self.message = "Node %s created" % node['node_id']

	#insert the record into GENI tables  ###############################soner
	(global_sr_tree, global_cr_tree) = get_tree_globals()
	(site_id, site_hrn) = site_to_auth(site['site_id'])
	dbinfo = determine_dbinfo(site_hrn, global_cr_tree)
	if dbinfo == None:
		raise PLCInvalidArgument, "No GENI authority corresponding to the site "+site['name']
	cnx = dbinfo[0]
	tablename = dbinfo[1]
	
	new_hrn = plnode_to_node(node['hostname'], 0)
	existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ")
	if existing != None:
		new_hrn = plnode_to_node(node['hostname'], 1)
		existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ")
		if existing != None:
			new_hrn = plnode_to_node(node['hostname'], 2)
		
	geni_record = {'hrn':''}
	geni_record["hrn"] = new_hrn
	geni_record["type"] = 'node'
	geni_record['pointer'] = node['node_id']
	
        querystr = generate_querystr('INSERT', tablename, geni_record)
        cnx.query(querystr)
	
        return node['node_id']
