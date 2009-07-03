import unittest
import xmlrpclib
from geni.trust.certificate import *
from geni.trust.gid import *
from geni.trust.config import *
from geni.util.record import *

class TestRecord(unittest.TestCase):
    def setUp(self):
        pass

    def testCreate(self):
        r = GeniRecord()

if __name__ == "__main__":
    unittest.main()
