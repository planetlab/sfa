import unittest
import xmlrpclib
from gackshandle import *

class TestGacksHandle(unittest.TestCase):
   def setUp(self):
       pass

   def testCreate(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       self.assertEqual(h.id, "cpu")
       self.assertEqual(h.unitStart, 10)
       self.assertEqual(h.unitStop, 15)
       self.assertEqual(h.timeStart, 20)
       self.assertEqual(h.timeStop, 25)

   def testAsString(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       s = h.as_string()
       self.assertEqual(s, "cpu#10-15#20-25")

   def testLoadFromString(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       s = h.as_string()
       h2 = GacksHandle(string=s)
       self.assertEqual(h.id, h2.id)
       self.assertEqual(h.unitStart, h2.unitStart)
       self.assertEqual(h.unitStop, h2.unitStop)
       self.assertEqual(h.timeStart, h2.timeStart)
       self.assertEqual(h.timeStop, h2.timeStop)

   def testGetQuantity(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       self.assertEqual(h.get_quantity(), 5)

   def testGetDuration(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       self.assertEqual(h.get_duration(), 5)

   def testClone(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       h2 = h.clone()
       self.assertEqual(h.id, h2.id)
       self.assertEqual(h.unitStart, h2.unitStart)
       self.assertEqual(h.unitStop, h2.unitStop)
       self.assertEqual(h.timeStart, h2.timeStart)
       self.assertEqual(h.timeStop, h2.timeStop)

   def testSplitUnit(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       parts = h.split_unit(12)
       h1 = parts[0]
       h2 = parts[1]

       self.assertEqual(h1.id, "cpu")
       self.assertEqual(h1.unitStart, 10)
       self.assertEqual(h1.unitStop, 12)
       self.assertEqual(h1.timeStart, 20)
       self.assertEqual(h1.timeStop, 25)

       self.assertEqual(h2.id, "cpu")
       self.assertEqual(h2.unitStart, 12)
       self.assertEqual(h2.unitStop, 15)
       self.assertEqual(h2.timeStart, 20)
       self.assertEqual(h2.timeStop, 25)

   def testSplitTime(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)
       parts = h.split_time(23)
       h1 = parts[0]
       h2 = parts[1]

       self.assertEqual(h1.id, "cpu")
       self.assertEqual(h1.unitStart, 10)
       self.assertEqual(h1.unitStop, 15)
       self.assertEqual(h1.timeStart, 20)
       self.assertEqual(h1.timeStop, 23)

       self.assertEqual(h2.id, "cpu")
       self.assertEqual(h2.unitStart, 10)
       self.assertEqual(h2.unitStop, 15)
       self.assertEqual(h2.timeStart, 23)
       self.assertEqual(h2.timeStop, 25)

   def testSplitSubset(self):
       h = GacksHandle("cpu", 10, 15, 20, 25)

       # split out a subset right in the middle
       parts = h.clone().split_subset(12, 13, 22, 23)

       self.assertEqual(len(parts), 5)
       self.assert_(find_handle_in_list(parts, 10, 12, 20, 25)) # h1
       self.assert_(find_handle_in_list(parts, 12, 13, 20, 22)) # h2
       self.assert_(find_handle_in_list(parts, 12, 13, 23, 25)) # h3
       self.assert_(find_handle_in_list(parts, 13, 15, 20, 25)) # h4
       self.assert_(find_handle_in_list(parts, 12, 13, 22, 23)) # s

       # split out a subset in the top left corner
       parts = h.clone().split_subset(10, 13, 20, 23)

       self.assertEqual(len(parts), 3)
       self.assert_(find_handle_in_list(parts, 10, 13, 23, 25)) # h3
       self.assert_(find_handle_in_list(parts, 13, 15, 20, 25)) # h4
       self.assert_(find_handle_in_list(parts, 10, 13, 20, 23)) # s

       # split out a subset in the bottom right corner
       parts = h.clone().split_subset(12, 15, 22, 25)

       self.assertEqual(len(parts), 3)
       self.assert_(find_handle_in_list(parts, 10, 12, 20, 25)) # h1
       self.assert_(find_handle_in_list(parts, 12, 15, 20, 22)) # h2
       self.assert_(find_handle_in_list(parts, 12, 15, 22, 25)) # s

class TestGacksRecord(unittest.TestCase):
   def setUp(self):
       pass

   def testCreate(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       self.assertEqual(r.id, "cpu")
       self.assertEqual(r.unitStart, 10)
       self.assertEqual(r.unitStop, 15)
       self.assertEqual(r.timeStart, 20)
       self.assertEqual(r.timeStop, 25)
       self.assertEqual(r.allocatorHRNs, ["foo", "bar"])
       self.assertEqual(r.consumerHRN, "slice1")

   def testClone(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       r2 = r.clone()

       self.assertEqual(r.id, r2.id)
       self.assertEqual(r.unitStart, r2.unitStart)
       self.assertEqual(r.unitStop, r2.unitStop)
       self.assertEqual(r.timeStart, r2.timeStart)
       self.assertEqual(r.timeStop, r2.timeStop)
       self.assertEqual(r.allocatorHRNs, r2.allocatorHRNs)
       self.assertEqual(r.consumerHRN, r2.consumerHRN)

   def testSetAllocator(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       r.set_allocator("bar", "bob", -1, 1)
       self.assertEqual(r.allocatorHRNs, ["foo", "bar", "bob"])

       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       r.set_allocator("bar", "bob", -1, 0)
       self.assertEqual(r.allocatorHRNs, ["foo", "bob"])

       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar","foo","bar"], "slice1")
       r.set_allocator("bar", "bob", 0, 0)
       self.assertEqual(r.allocatorHRNs, ["foo", "bob"])

       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar","foo","bar"], "slice1")
       r.set_allocator("bar", "bob", 1, 0)
       self.assertEqual(r.allocatorHRNs, ["foo", "bar", "foo", "bob"])

   def testGetAllocator(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       self.assertEqual(r.get_allocators(), ["foo", "bar"])

   def testSetConsumer(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       r.set_consumer("slice2")
       self.assertEqual(r.get_consumer(), "slice2")

   def testGetConsumer(self):
       r = GacksRecord("cpu", 10, 15, 20, 25, ["foo","bar"], "slice1")
       self.assertEqual(r.get_consumer(), "slice1")



if __name__ == "__main__":
    unittest.main()
