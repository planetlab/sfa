#!/usr/bin/python

"""
Installation script for the geniwrapper module
"""

from distutils.core import setup, Extension
import os, sys
import shutil

version = '0.2'
scripts = ['geni/gimport.py', 'geni/plc.py', 'cmdline/sfi.py', 'config/geni-config-tty']
package_dirs = ['geni', 'geni/util', 'geni/methods']
data_files = [('/etc/geni/', ['config/aggregates.xml', 'config/registries.xml', 'config/geni_config', 'config/sfi_config']),
              ('/etc/init.d/', ['geni/geniwrapper'])]
symlinks = ['/usr/share/geniwrapper']
initscripts = ['/etc/init.d/geniwrapper']
        
if sys.argv[1] in ['uninstall', 'remove', 'delete', 'clean']:
    python_path = sys.path
    site_packages_only = lambda path: path.endswith('site-packages') 
    site_packages_path = filter(site_packages_only, python_path)
    add_geni_path = lambda path: path + os.sep + 'geni'
    site_packages_path = map(add_geni_path, site_packages_path) 
    remove_dirs = ['/etc/geni/'] + site_packages_path
    remove_files = ['/usr/bin/gimport.py', '/usr/bin/plc.py', '/usr/bin/sfi.py', '/usr/bin/geni-config-tty'] + \
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
    setup(name='geniwrapper', 
      version = version,
      packages = package_dirs, 
      data_files = data_files,
      ext_modules = [],
      py_modules = [],
      scripts = scripts,   
      url = 'http://svn.planet-lab.org/svn/geniwrapper/',
      description = "Geni API",      
      long_description = """\
Geniwrapper implements the Geni interface which serves 
as a layer between the existing PlanetLab interfaces 
and the Geni API.
                    """,
      license = 'GPL')

    # create symlink to geniwrapper source in /usr/share
    python_path = sys.path
    site_packages_only = lambda path: path.endswith('site-packages')
    site_packages_path = filter(site_packages_only, python_path)
    add_geni_path = lambda path: path + os.sep + 'geni'
    site_packages_path = map(add_geni_path, site_packages_path)
    # python path usualy has /urs/local/lib/ path , filter this out
    site_packages_path = filter(lambda x: 'local' not in x, site_packages_path) 

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
