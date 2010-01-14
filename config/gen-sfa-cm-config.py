#!/usr/bin/python
import os
from sfa.util.config import Config

sfa_config = Config()
all_vars = ['SFA_CONFIG_DIR', 'SFA_DATA_DIR', 'SFA_INTERFACE_HRN',
            'SFA_REGISTRY_HOST', 'SFA_REGISTRY_PORT', 
            'SFA_AGGREGATE_HOST', 'SFA_AGGREGATE_PORT', 
            'SFA_SM_HOST', 'SFA_SM_PORT',
            'SFA_CM_ENABLED', 'SFA_CM_HOST', 'SFA_CM_PORT']
defaults = {
    'SFA_CM_ENABLED': '1',
    'SFA_CM_HOST': 'localhost',
    'SFA_CM_PORT': '12346'
    }
     
const_dict = {}
for key in all_vars:
    value = ""        
    if key in defaults:
        value = defaults[key]
    elif hasattr(sfa_config, key):
        value = getattr(sfa_config, key)
    const_dict[key] = value

filename = sfa_config.config_path + os.sep + 'sfa_component_config'
conffile = open(filename, 'w')
format='%s="%s"\n'

for var in all_vars:
    conffile.write(format % (var, const_dict[var]))

conffile.close() 
    

