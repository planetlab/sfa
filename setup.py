#!/usr/bin/python

"""
Installation script for the geniwrapper module
"""

import sys, os, os.path
import shutil
from distutils.core import setup

bins = [ 'config/sfa-config-tty',
            'sfa/plc/sfa-import-plc.py', 
            'sfa/plc/sfa-nuke-plc.py', 
            'sfa/server/sfa-server.py', 
            'sfa/client/sfi.py', 
            'sfa/client/getNodes.py',
            'sfa/client/getRecord.py',
            'sfa/client/setRecord.py',
            'sfa/client/genidump.py',
            ]
remove_bins = [ '/usr/bin/' + os.path.basename(bin) for bin in bins ]

package_dirs = [ 'sfa', 
                 'sfa/client',
                 'sfa/methods',
                 'sfa/plc',
                 'sfa/server',
                 'sfa/trust',
                 'sfa/util', 
                 'sfa/rspecs',
                 'sfa/rspecs/aggregates',
                 'sfa/rspecs/aggregates/vini'
                 ]
data_files = [ ('/etc/sfa/', [ 'config/aggregates.xml', 
                               'config/registries.xml', 
                               'config/sfa_config', 
                               'config/sfi_config',
                               ]),
               ('/etc/init.d/', ['sfa/init.d/sfa']),
               ]
initscripts = [ '/etc/init.d/sfa' ]
        
if sys.argv[1] in ['uninstall', 'remove', 'delete', 'clean']:
    python_path = sys.path
    site_packages_path = [ path + os.sep + 'sfa' for path in python_path if path.endswith('site-packages')]
    remove_dirs = ['/etc/sfa/'] + site_packages_path
    remove_files = remove_bins + initscripts
    
    # remove files   
    for filepath in remove_files:
        print "removing", filepath, "...",
        try: 
            os.remove(filepath)
            print "success"
        except: print "failed"
    # remove directories 
    for directory in remove_dirs: 
        print "removing", directory, "...",
        try: 
            shutil.rmtree(directory)
            print "success"
        except: print "failed"
 
else:
    
    # avoid repeating what's in the specfile already
    setup(name='sfa',
          packages = package_dirs, 
          data_files = data_files,
          ext_modules = [],
          py_modules = [],
          scripts = bins,   
          )

