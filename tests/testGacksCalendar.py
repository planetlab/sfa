import unittest
import xmlrpclib
from gackscalendar import *

class TestGacksCalendar():
    def setUp(self):
        self.r1 = GacksRecord("cpu", 0, 10, 100, 200, ["foo", "bar"], "slice1")
        self.r2 = GacksRecord("cpu", 0, 10, 200, 300, ["foo", "bar"], "slice2")
        self.r3 = GacksRecord("cpu", 10, 60, 150, 250, ["foo", "bar"], "slice3")
        self.r4 = GacksRecord("disk", 0, 50, 100, INFINITY, ["foo", "bar"], "slice4")

    def testCreate(self):
        c = self.CalClass()

    def testInsert(self):
        c = self.CalClass()
        c.insert_record(self.r1)
        c.insert_record(self.r2)
        c.insert_record(self.r3)
        c.insert_record(self.r4)

    def testQuery(self):
        c = self.CalClass()
        c.insert_record(self.r1)
        c.insert_record(self.r2)
        c.insert_record(self.r3)
        c.insert_record(self.r4)

        records = c.query()

        self.assertEqual(len(records), 4)

    def testRemove(self):
        c = self.CalClass()
        c.insert_record(self.r1)
        c.insert_record(self.r2)
        c.insert_record(self.r3)
        c.insert_record(self.r4)

        c.remove_record(self.r2)
        c.remove_record(self.r4)

        records = c.query()
        self.assertEqual(len(records), 2)

        self.assert_(c.find_record(self.r1))
        self.assertEqual(c.find_record(self.r2), None)
        self.assert_(c.find_record(self.r3))
        self.assertEqual(c.find_record(self.r4), None)


class TestGacksListCalendar(unittest.TestCase, TestGacksCalendar):
    def setUp(self):
        self.CalClass = GacksListCalendar
        TestGacksCalendar.setUp(self)

if __name__ == "__main__":
    unittest.main()
