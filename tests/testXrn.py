#!/usr/bin/python
import sys
import unittest

from sfa.util.faults import *
from sfa.util.xrn import Xrn

verbose=False

class TestXrn(unittest.TestCase):

    hrns=[ # hrn, type, expected_urn
        ('ple.inria.baris','user', "urn:publicid:IDN+ple:inria+user+baris"),
        ('emulab\.net.slice.jktest','slice', "urn:publicid:IDN+emulab.net:slice+slice+jktest"),
        ('plc.princeton.tmack','user', "urn:publicid:IDN+plc:princeton+user+tmack"),
        ('fake-pi1@onelab.eu','user', "urn:publicid:IDN+fake-pi1@onelab+user+eu"),
        # not providing a type is currently not supported
        ('fake-pi1@onelab.eu',None, None),
        ]
    
    urns=[ # urn, expected_hrn, expected_type
        ('urn:publicid:IDN+emulab:net+slice+jktest', "emulab.net.jktest", "slice"),
        ('urn:publicid:IDN+emulab.net+slice+jktest', "emulab\\.net.jktest", "slice"),
        ("urn:publicid:IDN+plc:princeton+user+tmack", "plc.princeton.tmack", "user"),
        ]

    def test_hrns(self):
        for (h,t,exp_urn) in TestXrn.hrns:
            print 'testing (',h,t,') expecting',exp_urn
            if exp_urn:
                xrn=Xrn(hrn=h,type=t)
                if verbose: print xrn.dump_string()
                urn=xrn.get_urn()
                (h1,t1) = Xrn(urn=urn).get_hrn()
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
                    

    def test_urns(self):
        for (urn, exp_hrn, exp_type) in TestXrn.urns:
            xrn=Xrn(urn=urn)
            print 'testing urn',urn,'expecting (',exp_hrn,exp_type,')'
            if verbose: print xrn.dump_string()
            (h,t)=xrn.get_hrn()
            urn1 = Xrn(hrn=h,type=t).get_urn()
            if urn1!=urn:
                print "urn->hrn->urn : MISMATCH with in=(%s) -- out=(%s) -- hrn=(%s,%s)"%(urn,urn1,h,t)
            self.assertEqual(urn1,urn)
