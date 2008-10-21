import unittest
import xmlrpclib
from gacksreceipt import *

class TestGacksReceipt(unittest.TestCase):
   def setUp(self):
       pass

   def testCreate(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       r = GacksReceipt(subject="foo1", handle = h, action="foo")
       self.assertEqual(r.handle, h)
       self.assertEqual(r.action, "foo")

   def testSetHandle(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       r = GacksReceipt(subject="foo1", handle = h)
       self.assertEqual(r.handle, h)

       h2 = GacksHandle("cpu", 10, 15, 20, 25)
       r.SetHandle(h2);
       self.assertEqual(r.handle, h2)

   def testSetAction(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       r = GacksReceipt(subject="foo1", handle = h, action="foo")
       self.assertEqual(r.action, "foo")

       r.SetAction("bar");
       self.assertEqual(r.action, "bar")

   def testEncodeDecode(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       rec1 = GacksRecord("cpu", 10, 13, 20, 25, ["aaa","bbb"], "slice1")
       rec2 = GacksRecord("cpu", 13, 15, 20, 25, ["aaa","bbb"], "slice1")
       r = GacksReceipt(subject="foo1", handle = h, action="foo", reclist=[rec1,rec2])

       r.encode()

       str = r.save_to_string()

       r2 = GacksReceipt(string = str)
       #r2.decode()
       #r2.dump()

       h2 = r2.GetHandle()
       self.assertEqual(h2.id, "cpu")
       self.assertEqual(h2.unitStart, 10)
       self.assertEqual(h2.unitStop, 15)
       self.assertEqual(h2.timeStart, 20)
       self.assertEqual(h2.timeStop, 25)

       self.assertEqual(r2.GetAction(), "foo")

       reclist = r2.GetRecords()
       r1=reclist[0]
       r2=reclist[1]
       self.assertEqual(r1.id, "cpu")
       self.assertEqual(r1.unitStart, 10)
       self.assertEqual(r1.unitStop, 13)
       self.assertEqual(r1.timeStart, 20)
       self.assertEqual(r1.timeStop, 25)
       self.assertEqual(r2.id, "cpu")
       self.assertEqual(r2.unitStart, 13)
       self.assertEqual(r2.unitStop, 15)
       self.assertEqual(r2.timeStart, 20)
       self.assertEqual(r2.timeStop, 25)

if __name__ == "__main__":
    unittest.main()
