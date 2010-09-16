import unittest
import os
from sfa.util.faults import *
from sfa.trust.hierarchy import *
from sfa.util.config import *

BASEDIR = "test_hierarchy"
PURGE_BASEDIR = "rm -rf test_hierarchy"

class TestHierarchy(unittest.TestCase):
    def setUp(self):
        os.system(PURGE_BASEDIR)
        pass

    def testInit(self):
        h = Hierarchy(BASEDIR)

    def testGetAuthInfo(self):
        h = Hierarchy(BASEDIR)

        name = "planetlab.us.arizona.stork"

        self.assertEqual(h.auth_exists(name), False)

        self.assertRaises(MissingAuthority, h.get_auth_info, name)

        h.create_auth(name, create_parents=True)
        auth_info = h.get_auth_info(name)
        self.assert_(auth_info)

        gid = auth_info.get_gid_object()
        self.assert_(gid)
        self.assertEqual(gid.get_subject(), name)

        pubkey = auth_info.get_pkey_object()
        self.assert_(gid)

        # try to get it again, make sure it's still there
        auth_info2 = h.get_auth_info(name)
        self.assert_(auth_info2)

        gid = auth_info2.get_gid_object()
        self.assert_(gid)
        self.assertEqual(gid.get_subject(), name)

        pubkey = auth_info2.get_pkey_object()
        self.assert_(gid)


if __name__ == "__main__":
    unittest.main()
