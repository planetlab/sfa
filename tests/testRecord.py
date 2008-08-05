import unittest
import xmlrpclib
from record import *
from cert import *
from gid import *

class TestRecord(unittest.TestCase):
    def setUp(self):
        pass

    def testCreate(self):
        r = GeniRecord()

class TestTable(unittest.TestCase):

    def setUp(self):
        self.reg_hrn = "test.table"
        self.rec_hrn = self.reg_hrn + "." + "record"
        pass

    def testCreate(self):
        t = GeniTable(hrn = self.reg_hrn)
        t.create()

    def testInsert(self):
        t = GeniTable(hrn = self.reg_hrn)

        k = Keypair(create=True)
        gid = GID(subject="scott.foo", uuid=create_uuid(), hrn=self.rec_hrn)
        gid.set_pubkey(k)
        gid.set_issuer(key=k, subject=self.rec_hrn)
        gid.encode()
        gid.sign()

        r = GeniRecord(name=self.rec_hrn, gid=gid.save_to_string(), type="user", pointer=3)
        t.insert(r)

    def testLookup(self):
        t = GeniTable(hrn = self.reg_hrn)

        rec_list = t.lookup(self.rec_hrn)
        self.assertEqual(len(rec_list), 1)
        r = rec_list[0]
        self.assertEqual(r.name, self.rec_hrn)
        self.assertEqual(r.pointer, 3)

    def testUpdate(self):
        t = GeniTable(hrn = self.reg_hrn)

        rec_list = t.lookup(self.rec_hrn)
        r = rec_list[0]

        r.set_pointer(4)
        t.update(r)

        rec_list = t.lookup(self.rec_hrn)
        self.assertEqual(len(rec_list), 1)
        r = rec_list[0]
        self.assertEqual(r.name, self.rec_hrn)
        self.assertEqual(r.pointer, 4)

if __name__ == "__main__":
    unittest.main()
