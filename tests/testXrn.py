#!/usr/bin/python
import sys
import unittest

from sfa.util.faults import *
from sfa.util.xrn import Xrn
from sfa.util.plxrn import PlXrn

verbose=False

class TestXrn(unittest.TestCase):

    def __hrn(self,h,t,exp_urn):
        if verbose: print 'testing (',h,t,') expecting',exp_urn
        if exp_urn:
            xrn=Xrn(hrn=h,type=t)
            if verbose: print xrn.dump_string()
            urn=xrn.get_urn()
            (h1,t1) = Xrn(urn=urn).get_hrn_type()
            if h1!=h or t1!=t or urn!=exp_urn:
                print "hrn->urn->hrn : MISMATCH with in=(%s,%s) -- out=(%s,%s) -- urn=%s"%(h,t,h1,t1,urn)
            self.assertEqual(h1,h)
            self.assertEqual(t1,t)
            self.assertEqual(urn,exp_urn)
        else:
            # could not figure how to use assertFails on object construction..
            # with self.assertRaises(SfaAPIError):
            #    Xrn(hrn=h,type=t).get_urn()
            try:
                Xrn(hrn=h,type=t).get_urn()
                failure="Unexpectedly created Xrn object"
            except SfaAPIError:
                failure=False
            except Exception,e:
                failure="Xrn creation raised unexpected exception %r"%e
            if failure: 
                print "hrn->urn->hrn - %s with HRN=%s TYPE=%s"%(failure,h,t)
                self.assertFalse(True)


    def test_hrn001 (self): 
        self.__hrn("ple.inria.baris",'user',
                   "urn:publicid:IDN+ple:inria+user+baris")
    def test_hnr002 (self): 
        self.__hrn("emulab\.net.myslice.jktest",'slice',
                   "urn:publicid:IDN+emulab.net:myslice+slice+jktest")
    def test_hrn003(self):
        self.__hrn("emulab\\.net.jktest", "slice",
                   "urn:publicid:IDN+emulab.net+slice+jktest")
    def test_hrn004(self):
        self.__hrn("plc.princeton.tmack",'user',
                   "urn:publicid:IDN+plc:princeton+user+tmack")
    def test_hrn005(self):
        self.__hrn("fake-pi1@onelab.eu",'user',
                   "urn:publicid:IDN+fake-pi1@onelab+user+eu")
    def test_hrn006(self):
        self.__hrn("plc.princeton.tmack", 'user',
                   "urn:publicid:IDN+plc:princeton+user+tmack" )
    def test_hrn007(self):
        # not providing a type is currently not supporte
        self.__hrn("fake-pi1@onelab.eu",None,
                   None)
    def test_hrn008(self):
        self.__hrn("plc.princeton.planetlab1", 'node',
                   "urn:publicid:IDN+plc:princeton+node+planetlab1" )
    def test_hrn009(self):
        self.__hrn("plc.princeton", 'authority',
                   "urn:publicid:IDN+plc:princeton+authority+sa" )
    def test_hrn010(self):
        self.__hrn("plc.vini.site", 'authority',
                   "urn:publicid:IDN+plc:vini:site+authority+sa" )
        

    
    def test_host001 (self):
        xrn=PlXrn (auth="ple.inria",hostname="onelab09.pl.sophia.inria.fr")
        self.assertEqual (xrn.get_hrn_type(), ("ple.inria.onelab09",'node'))
    def test_host002 (self):
        xrn=PlXrn (auth="ple\\.inria",hostname="onelab09.pl.sophia.inria.fr")
        self.assertEqual (xrn.get_hrn_type(), ("ple\\.inria.onelab09",'node'))

    def test_slice001  (self):
        xrn=PlXrn (auth="ple",slicename="inria_omftest")
        self.assertEqual (xrn.get_hrn_type(), ("ple.inria.omftest",'slice'))

    def test_person001 (self):
        xrn=PlXrn (auth="ple.inria",email="first.last@some.domain.com")
        self.assertEqual (xrn.get_hrn_type(), ("ple.inria.first_last",'person'))
    def test_person002 (self):
        xrn=PlXrn (auth="ple.inria",email="first+last@some.domain.com")
        self.assertEqual (xrn.get_hrn_type(), ("ple.inria.first_last",'person'))
        


    def test_login_base_001 (self):
        xrn=PlXrn(hrn='ple.inria.omftest',type='slice')
        self.assertEqual(xrn.login_base(),'inria')

    def test_slicename_001 (self):
        xrn=PlXrn(hrn='ple.inria.omftest',type='slice')
        self.assertEqual(xrn.slicename(),'inria_omftest')

    def test_authname_001 (self):
        xrn=PlXrn(hrn='ple.inria.omftest',type='slice')
        self.assertEqual(xrn.authname(),'inria')


