#!/usr/bin/python

"""
Installation script for the geniwrapper module
"""

from distutils.core import setup, Extension
import os, sys

version = '0.2'
scripts = ['geni/gimport.py', 'geni/plc.py', 'cmdline/sfi.py']
package_dirs = ['geni', 'geni/util', 'geni/methods']
data_files = [('/etc/geni/', ['geni/aggregates.xml', 'geni/registries.xml', 'geni/util/geni_config'])]


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
