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

class TestTable(unittest.TestCase):

    def setUp(self):
        set_geni_table_prefix("testRecord$")
        self.reg_hrn = "test.table"
        self.rec_hrn = self.reg_hrn + "." + "record"

    def test000_Purge(self):
        geni_records_purge(get_default_dbinfo())

    def test001_Create(self):
        t = GeniTable(hrn = self.reg_hrn, cninfo=get_default_dbinfo())
        t.create()

    def test002_Insert(self):
        t = GeniTable(hrn = self.reg_hrn, cninfo=get_default_dbinfo())

        k = Keypair(create=True)
        gid = GID(subject="scott.foo", uuid=create_uuid(), hrn=self.rec_hrn)
        gid.set_pubkey(k)
        gid.set_issuer(key=k, subject=self.rec_hrn)
        gid.encode()
        gid.sign()

        r = GeniRecord(name=self.rec_hrn, gid=gid.save_to_string(), type="user", pointer=3)
        t.insert(r)

    def test003_Lookup(self):
        t = GeniTable(hrn = self.reg_hrn, cninfo=get_default_dbinfo())

        rec_list = t.resolve("*", self.rec_hrn)
        self.assertEqual(len(rec_list), 1)
        r = rec_list[0]
        self.assertEqual(r.name, self.rec_hrn)
        self.assertEqual(r.pointer, 3)

    def test004_Update(self):
        t = GeniTable(hrn = self.reg_hrn, cninfo=get_default_dbinfo())

        rec_list = t.resolve("*", self.rec_hrn)
        r = rec_list[0]

        r.set_pointer(4)
        t.update(r)

        rec_list = t.resolve("*", self.rec_hrn)
        self.assertEqual(len(rec_list), 1)
        r = rec_list[0]
        self.assertEqual(r.name, self.rec_hrn)
        self.assertEqual(r.pointer, 4)

if __name__ == "__main__":
    unittest.main()
