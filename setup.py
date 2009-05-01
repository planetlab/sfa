#!/usr/bin/python

"""
Installation script for the geniwrapper module
"""

from distutils.core import setup, Extension
import os, sys

version = '0.2'
scripts = ['geni/gimport.py', 'geni/plc.py', 'cmdline/sfi.py']
package_dirs = ['geni', 'geni/util', 'geni/methods']
data_files = [('/etc/geni/', ['geni/aggregates.xml', 'geni/registries.xml', 'geni/util/geni_config', 'cmdline/configSfi.sh'])]

def list_dir(directory):
    # list the files in this directory
    try:
        files = os.listdir(directory)
        add_directory_path = lambda path: directory + os.sep + path
        # add absolute path to files
        files = map(add_directory_path, files)
        # separate files from directories
        files_only = lambda path: os.path.isfile(path)
        directories_only = lambda path: os.path.isdir(path)
        directories = filter(directories_only, files)
        files = filter(files_only, files)
        for d in directories:
            try:
                (fs, ds) = list_dir(d)
                files.extend(fs)
            except: 
                print "Error listing", d
        return (files, directories)
    except:
        return ([], [])
        
        
if sys.argv[1] in ['uninstall', 'remove', 'delete']:
    python_path = sys.path
    site_packages_only = lambda path: path.endswith('site-packages') 
    site_packages_path = filter(site_packages_only, python_path)
    add_geni_path = lambda path: path + os.sep + 'geni'
    site_packages_path = map(add_geni_path, site_packages_path) 
    remove_dirs = ['/etc/geni/'] + site_packages_path
    remove_files = ['/usr/bin/gimport.py', '/usr/bin/plc.py', '/usr/bin/sfi.py']
    # update list of files/directories to remove
    for directory in remove_dirs:
        files, dirs = list_dir(directory)
        remove_files.extend(list(set(files)))
        remove_dirs.extend(dirs)
        remove_dirs.reverse()

    # remove files   
    for filepath in remove_files:
        print "removing", filepath, " ... ",
        try: 
            os.remove(filepath)
            print "success"
        except: print "failed"
    # remove directories 
    for directory in remove_dirs: 
        print "removing", directory, " ... ",
        try: 
            os.rmdir(directory)
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
      description = "Geni api",      
      long_description = """\
Geniwrapper implements the Geni interface which serves 
as a layer between the existing PlanetLab interfaces 
and the Geni API.
                    """,
      license = 'GPL')
