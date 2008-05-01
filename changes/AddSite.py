from PLC.Faults import *
from PLC.Method import Method
from PLC.Parameter import Parameter, Mixed
from PLC.Sites import Site, Sites
from PLC.Auth import Auth
import uuid ##################################soners

can_update = lambda (field, value): field in \
             ['name', 'abbreviated_name', 'login_base',
              'is_public', 'latitude', 'longitude', 'url',
              'max_slices', 'max_slivers', 'enabled', 'uuid']

class AddSite(Method):
    """
    Adds a new site, and creates a node group for that site. Any
    fields specified in site_fields are used, otherwise defaults are
    used.

    Returns the new site_id (> 0) if successful, faults otherwise.
    """

    roles = ['admin']

    site_fields = dict(filter(can_update, Site.fields.items()))

    accepts = [
        Auth(),
        site_fields
        ]

    returns = Parameter(int, 'New site_id (> 0) if successful')

    def call(self, auth, site_fields):
        site_fields = dict(filter(can_update, site_fields.items()))
        site = Site(self.api, site_fields)
	site['uuid'] = str(uuid.uuid4().int)###############################soners
        site.sync()
	
	# Logging variables 
	self.event_objects = {'Site': [site['site_id']]}
        self.message = 'Site %d created' % site['site_id']
 	
	return site['site_id']
