#!/usr/bin/python
import sys
import os
import sfa.util.xmlrpcprotocol as xmlrpc
import unittest
from unittest import TestCase
from optparse import OptionParser
from sfa.util.xmlrpcprotocol import ServerException
from sfa.util.namespace import *
from sfa.util.config import *
from sfa.trust.certificate import *
from sfa.client import sfi

class Client:
    registry = None
    aggregate = None
    sm = None
    cm = None
    user = None
    key = None
    cert = None
    credential = None
    type = None            
    def __init__(self, options):
        try: self.config = config = Config(options.config_file)
        except:
            print "failed to read config_file %s" % options.config_file
            sys.exit(1)
        key_path = os.path.dirname(options.config_file)
        user_name = self.config.SFI_USER.split('.')[-1:][0]
        key_file = key_path + os.sep + user_name + '.pkey'
        cert_file = key_path + os.sep + user_name + '.cert'
        self.key = Keypair(filename=key_file)
        self.cert = Certificate(subject=self.config.SFI_USER)
        self.cert.set_pubkey(self.key)
        self.cert.set_issuer(self.key, self.config.SFI_USER)
        self.cert.sign()
        self.cert.save_to_file(cert_file)        
        SFI_AGGREGATE = config.SFI_SM.replace('12347', '12346')
        SFI_CM = 'http://' + options.cm_host + ':12346'
        self.registry = xmlrpc.get_server(config.SFI_REGISTRY, key_file, cert_file)
        self.aggregate = xmlrpc.get_server(SFI_AGGREGATE, key_file, cert_file)
        self.sm = xmlrpc.get_server(config.SFI_SM, key_file, cert_file)
        self.cm = xmlrpc.get_server(SFI_CM, key_file, cert_file)
        self.user = config.SFI_USER
        # XX defaulting to user, but this should be configurable so we can
        # test from components persepctive
        self.type = 'user'
        
    def get_credential(self, hrn = None, type = 'user'):
        if not hrn: hrn = self.user 
        if hrn == self.user:
            cert = self.cert.save_to_string(save_parents=True)
            request_hash = self.key.compute_hash([cert, 'user', hrn])
            self.credential = self.registry.get_self_credential(cert, type, hrn, request_hash)
            return self.credential
        else:
            if not self.credential:
                self.get_credential(self.user, 'user')
            return self.registry.get_credential(self.credential, type, hrn)     

       

class BasicTestCase(unittest.TestCase):
    def __init__(self, testname, client):
        unittest.TestCase.__init__(self, testname)
        self.client = client
    
    def setUp(self):
        self.registry = self.client.registry
        self.aggregate = self.client.aggregate
        self.sm = self.client.sm
        self.cm = self.client.cm
        self.credential = self.client.credential
        self.hrn = self.client.user
        self.type = self.client.type  
                
# Registry tests
class RegistryTest(BasicTestCase):

    def setUp(self):
        """
        Make sure test records dont exsit
        """
        BasicTestCase.setUp(self)

    def testGetSelfCredential(self):
        self.client.get_credential()

    def testRegister(self):
        assert True 
    
    def testRegisterPeerObject(self):
        assert True
   
    def testUpdate(self):
        assert True

    def testResolve(self):
        self.registry.resolve(self.credential, self.hrn)
        assert True
   
    def testRemove(self):
        assert True
 
    def testRemovePeerObject(self):
        assert True

    def testList(self):
        authority = get_authority(self.client.user)
        self.registry.list(self.credential, authority)
             
    def testGetRegistries(self):
        self.registry.get_registries(self.credential)
    
    def testGetAggregates(self):
        self.registry.get_aggregates(self.credential)

    def testGetTrustedCerts(self):
        # this should fail unless we are a node
        callable = self.registry.get_trusted_certs
        server_exception = False 
        try:
            callable(self.credential)
        except ServerException:
            server_exception = True
        finally:
            if self.type in ['user'] and not server_exception:
                assert False
            
            


class AggregateTest(BasicTestCase):
    def setup(self):
        BasicTestCase.setUp(self)

    def testGetSlices(self):
        self.aggregate.get_slices(self.credential)

    def testGetResources(self):
        self.aggregate.get_resources(self.credential)

    def testCreateSlice(self):
        assert True

    def testDeleteSlice(self):
        assert True

    def testGetTicket(self):
        assert True

class SlicemgrTest(AggregateTest):
    def setup(self):
        AggregateTest.setUp(self)

class ComponentTest(BasicTestCase):
    def setup(self):
        BasicTestCase.setUp(self)

    def testStartSlice(self):
        assert True

    def testStopSlice(self):
        assert True

    def testDeleteSlice(self):
        assert True

    def testRestartSlice(self):
        assert True

    def testGetSlices(self):
        assert True        

    def testRedeemTicket(self):
        assert True


def test_names(testcase):
    return [name for name in dir(testcase) if name.startswith('test')]
 
if __name__ == '__main__':

    args = sys.argv
    prog_name = args[0]
    default_config_dir = os.path.expanduser('~/.sfi/sfi_config')
    default_cm = "echo.cs.princeton.edu"
    parser = OptionParser(usage="%(prog_name)s [options]" % locals())
    parser.add_option('-f', '--config_file', dest='config_file', default=default_config_dir,
                      help='config file. default is %s' % default_config_dir)
    parser.add_option('-r', '--registry', dest='registry', action='store_true',
                      default=False, help='run registry tests')
    parser.add_option('-a', '--aggregate', dest='aggregate', action='store_true',
                      default=False, help='run aggregate tests')
    parser.add_option('-s', '--slicemgr', dest='slicemgr', action='store_true',
                      default=False, help='run slicemgr tests')
    parser.add_option('-c', '--component', dest='component', action='store_true',
                      default=False, help='run component tests')
    parser.add_option('-d', '--cm_host', dest='cm_host', default=default_cm, 
                      help='dns name of component to test. default is %s' % default_cm)
    parser.add_option('-A', '--all', dest='all', action='store_true',
                      default=False, help='run component tests')
    
    options, args = parser.parse_args()
    suite = unittest.TestSuite()
    client = Client(options)
    # bootstrap the users credential
    client.get_credential()

    if options.registry or options.all:
        for name in test_names(RegistryTest):
            suite.addTest(RegistryTest(name, client))

    if options.aggregate or options.all: 
        for name in test_names(AggregateTest):
            suite.addTest(AggregateTest(name, client))

    if options.slicemgr or options.all: 
        for name in test_names(SlicemgrTest):
            suite.addTest(SlicemgrTest(name, client))

    if options.component or options.all: 
        for name in test_names(ComponentTest):
            suite.addTest(ComponentTest(name, client))

    unittest.TextTestRunner(verbosity=2).run(suite)

