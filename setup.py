#!/usr/bin/python

"""
Installation script for the geniwrapper module
"""

import os, sys
import shutil
from distutils.core import setup, Extension

scripts = [ 'geni/gimport.py', 
            'geni/plc.py', 
            'config/sfa-config-tty',
            'cmdline/sfi.py', 
            'cmdline/getNodes.py',
            'cmdline/getRecord.py',
            'cmdline/setRecord.py',
            'cmdline/genidump.py',
            ]
package_dirs = ['geni', 'geni/util', 'geni/methods']
data_files = [ ('/etc/geni/', ['config/aggregates.xml', 'config/registries.xml', 
                               'config/sfa_config', 'config/sfi_config']),
               ('/etc/init.d/', ['geni/init.d/sfa']),
               ('/var/www/html/wsdl', [ 'wsdl/sfa.wsdl' ] ),
               ]
symlinks = ['/usr/share/geniwrapper']
initscripts = ['/etc/init.d/geni']
        
if sys.argv[1] in ['uninstall', 'remove', 'delete', 'clean']:
    python_path = sys.path
    site_packages_path = [ path + os.sep + 'geni' for path in python_path if path.endswith('site-packages')]
    remove_dirs = ['/etc/geni/'] + site_packages_path
    remove_files = ['/usr/bin/gimport.py', '/usr/bin/plc.py', '/usr/bin/sfi.py', '/usr/bin/sfa-config-tty'] + \
                    symlinks + initscripts
    
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
    setup(name='geni',
          packages = package_dirs, 
          data_files = data_files,
          ext_modules = [],
          py_modules = [],
          scripts = scripts,   
          )

    # create symlink to geniwrapper source in /usr/share
    python_path = sys.path
    site_packages_path = [ path + os.sep + 'geni' for path in python_path if path.endswith('site-packages')]
    # python path usualy has /usr/local/lib/ path , filter this out
    site_packages_path = [x for x in site_packages_path if 'local' not in x]

    # we can not do this here as installation root might change paths
    # - baris
    #
    # for src in site_packages_path:
    #     for dst in symlinks:
    #         try: 
    #             os.symlink(src, dst)
    #         except: pass
    # for initscript in initscripts:
    #     os.chmod(initscript, 00744)
