import unittest
import os
from hierarchy import *
from config import *

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

        auth_info = h.get_auth_info("planetlab.us.arizona.stork", "sa", can_create=True)
        self.assert_(auth_info)

        gid = auth_info.get_gid_object()
        self.assert_(gid)
        self.assertEqual(gid.get_subject(), "planetlab.us.arizona.stork")

        pubkey = auth_info.get_pkey_object()
        self.assert_(gid)

        # try to get it again, make sure it's still there
        auth_info2 = h.get_auth_info("planetlab.us.arizona.stork", "sa", can_create=False)
        self.assert_(auth_info2)

        gid = auth_info2.get_gid_object()
        self.assert_(gid)
        self.assertEqual(gid.get_subject(), "planetlab.us.arizona.stork")

        pubkey = auth_info2.get_pkey_object()
        self.assert_(gid)


if __name__ == "__main__":
    unittest.main()
