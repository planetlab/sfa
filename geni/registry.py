##
# Registry is a GeniServer that implements the Registry interface

import tempfile
import os
import time
import sys

from geni.util.credential import Credential
from geni.util.hierarchy import Hierarchy
from geni.util.trustedroot import TrustedRootList
from geni.util.cert import Keypair, Certificate
from geni.util.gid import GID, create_uuid
from geni.util.geniserver import GeniServer
from geni.util.geniclient import GeniClient
from geni.util.record import GeniRecord
from geni.util.rights import RightList
from geni.util.genitable import GeniTable
from geni.util.geniticket import Ticket
from geni.util.excep import *
from geni.util.misc import *
from geni.util.config import *
from geni.util.storage import *

##
# Registry is a GeniServer that serves registry and slice operations at PLC.

class Registry(GeniServer):
    ##
    # Create a new registry object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file, config = '/usr/share/geniwrapper/geni/util/geni_config'):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

        # get PL account settings from config module
        self.pl_auth = get_pl_auth()

        # connect to planetlab
        if "Url" in self.pl_auth:
            self.connect_remote_shell()
        else:
            self.connect_local_shell()

        self.key_file = key_file
        self.cert_file = cert_file
        self.config = Config(config)
        self.basedir = self.config.GENI_BASE_DIR + os.sep
        self.server_basedir = self.basedir + os.sep + "geni" + os.sep
        self.hrn = self.config.GENI_INTERFACE_HRN

        # get peer registry information
        registries_file = self.server_basedir + os.sep + 'registries.xml'
        connection_dict = {'hrn': '', 'addr': '', 'port': ''} 
        self.registry_info = XmlStorage(registries_file, {'registries': {'registry': [connection_dict]}})
        self.registry_info.load()
        self.connectRegistry()
        self.connectRegistries()
        
 
    ##
    # Connect to a remote shell via XMLRPC

    def connect_remote_shell(self):
        from geni.util import remoteshell
        self.shell = remoteshell.RemoteShell()

    ##
    # Connect to a local shell via local API functions

    def connect_local_shell(self):
        import PLC.Shell
        self.shell = PLC.Shell.Shell(globals = globals())

    ##
    # Register the server RPCs for the registry

    def loadCredential(self):
        """
        Attempt to load credential from file if it exists. If it doesnt get
        credential from registry.
        """

        # see if this file exists
        # XX This is really the aggregate's credential. Using this is easier than getting
        # the registry's credential from iteslf (ssl errors).   
        ma_cred_filename = self.server_basedir + os.sep + "agg." + self.hrn + ".ma.cred"
        try:
            self.credential = Credential(filename = ma_cred_filename)
        except IOError:
            self.credential = self.getCredentialFromRegistry()

    def getCredentialFromRegistry(self):
        """
        Get our current credential from the registry.
        """
        # get self credential
        self_cred_filename = self.server_basedir + os.sep + "smgr." + self.hrn + ".cred"
        self_cred = self.registry.get_credential(None, 'ma', self.hrn)
        self_cred.save_to_file(self_cred_filename, save_parents=True)

        # get ma credential
        ma_cred_filename = self.server_basedir + os.sep + "smgr." + self.hrn + ".sa.cred"
        ma_cred = self.registry.get_credential(self_cred, 'sa', self.hrn)
        ma_cred.save_to_file(ma_cred_filename, save_parents=True)
        return ma_cred

    def connectRegistry(self):
        """
        Connect to the registry
        """
        # connect to registry using GeniClient
        address = self.config.GENI_REGISTRY_HOSTNAME
        port = self.config.GENI_REGISTRY_PORT
        url = 'http://%(address)s:%(port)s' % locals()
        self.registry = GeniClient(url, self.key_file, self.cert_file)

    def connectRegistries(self):
        """
        Get connection details for the trusted peer registries from file and 
        create an GeniClient connection to each. 
        """
        self.registries= {}
        required_fields = ['hrn', 'addr', 'port']
        registries = self.registry_info['registries']['registry']
        if isinstance(registries, dict):
            registries = [registries]
        if isinstance(registries, list):
            for registry in registries:
                # create xmlrpc connection using GeniClient
                if not set(required_fields).issubset(registry.keys()):
                    continue  
                hrn, address, port = registry['hrn'], registry['addr'], registry['port']
                if not hrn or not address or not port:
                    continue
                url = 'http://%(address)s:%(port)s' % locals()
                self.registries[hrn] = GeniClient(url, self.key_file, self.cert_file)

