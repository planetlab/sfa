import os

from geni.util.storage import *
from geni.util.debug import log

class Policy(SimpleStorage):

    def __init__(self, api):
        self.api = api    
        self.policy_file = os.sep.join([self.api.server_basedir, self.api.interface + '.' + self.api.hrn + '.policy'])
        default_policy = {'slice_whitelist': [],
                          'slice_backlist': [],
                          'node_whitelist': [],
                          'node_blacklist': []} 
        SimpleStorage.__init__(self, self.policy_file, default_policy)
        self.load()          
 
