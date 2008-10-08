import unittest
import xmlrpclib
from record import *
from cert import *
from gid import *
from config import *

class TestRecord(unittest.TestCase):
    def setUp(self):
        pass

    def testCreate(self):
        r = GeniRecord()

if __name__ == "__main__":
    unittest.main()
