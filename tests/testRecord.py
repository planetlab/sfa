import unittest
import xmlrpclib
from sfa.trust.gid import *
from sfa.trust.config import *
from sfa.util.record import *

class TestRecord(unittest.TestCase):
    def setUp(self):
        pass

    def testCreate(self):
        r = GeniRecord()

if __name__ == "__main__":
    unittest.main()
