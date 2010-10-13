#!/usr/bin/python
import sys
import unittest

from sfa.util.namespace import *

class TestNamespace(unittest.TestCase):

    hrns=[
        ('plc.princeton.tmack','user'),
        ('fake-pi1@onelab.eu','user'),
        ('ple.inria.baris','user'),
        ('emulab\.net.slice.jktest','slice'),
        ]
    
    urns=[
        'urn:publicid:IDN+emulab:net+slice+jktest',
        'urn:publicid:IDN+emulab.net+slice+jktest',

        ]

    def test_hrns(self):
        for (h,t) in TestNamespace.hrns:
            print 'testing hrn',h,t
            urn=hrn_to_urn(h,t)
            (h1,t1) = urn_to_hrn(urn)
            self.assertEqual(h1,h)
            self.assertEqual(t1,t)
            if h1!=h or t1!=t:
                print "hrn->urn->hrn : MISMATCH with in=(%s,%s) -- out=(%s,%s) -- urn=%s"%(h,t,h1,t1,urn)

    def test_urns(self):
        for urn in TestNamespace.urns:
            print 'testing urn',urn
            (h,t)=urn_to_hrn(urn)
            urn1 = hrn_to_urn(h,t)
            self.assertEqual(urn1,urn)
            if urn1!=urn:
                print "urn->hrn->urn : MISMATCH with in=(%s) -- out=(%s) -- hrn=(%s,%s)"%(urn,urn1,h,t)
