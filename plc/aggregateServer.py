
from geniserver import *
from cert import *
from trustedroot import *
from excep import *
from aggregate import *

class AggregateServer(GeniServer):

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)
        self.aggregate = Aggregate(hrn)

    def nodes(self):
	return self.aggregate.get_components
    
    def slices(self):
	return self.aggregate.get_slices

    def resources(self, cred, hrn):
	self.decode_authentication(cred, 'info')
	self.verify_object_belongs_to_me(hrn)
	
	return self.aggregate.get_resources(hrn)

    def create(self, cred, hrn, rspec):
	self.decode_authentication(cred, 'embed')
	self.verify_object_belongs_to_me(hrn, rspec)
	return self.aggregate.create(hrn)

    def delete(self, cred, hrn):
	self.decode_authentication(cred, 'embed')
	self.verify_object_belongs_to_me(hrn)
	return self.aggregate.delete_slice(hrn)

    def start(self, cred, hrn):
	self.decode_authentication(cred, 'control')
	return self.aggregaet.start(hrn)

    def stop(self, cred, hrn):
	self.decode_authentication(cred, 'control')
	return self.aggregate.stop(hrn)		

    def reset(self, cred, hrn):
	self.decode_authentication(cred, 'control')
	return self.aggregate.reset(hrn)

    def policy(self, cred):
	self.decode_authentication(cred, 'info')
	return self.aggregate.get_policy()

    def register_functions(self):
        GeniServer.register_functions(self)

        # Aggregate interface methods
	self.server.register_function(self.components)
	self.server.register_function(self.slices)   
	self.server.register_function(self.resources)   
	self.server.register_function(self.create)   
	self.server.register_function(self.delete)   
	self.server.register_function(self.start)   
	self.server.register_function(self.stop)
	self.server.register_function(self.reset)   
	self.server.register_function(self.policy)   
 
