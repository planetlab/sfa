import unittest
from rights import *

class TestRight(unittest.TestCase):
   def setUp(self):
      pass

   def testRightInit(self):
      right = Right("embed")
      self.assertEqual(right.kind, "embed")

   def testRightCanPerform(self):
      right = Right("embed")
      self.assert_(right.can_perform("getticket"))
      self.assert_(not right.can_perform("resolve"))

class TestRightList(unittest.TestCase):
    def setUp(self):
        pass

    def testInit(self):
        # create a blank right list
        rightList = RightList()

        # create a right list with "embed" in it
        rightList = RightList(string="embed")

    def testAsString(self):
        rightList = RightList()
        self.assertEqual(rightList.save_to_string(), "")

        rightList = RightList(string="embed")
        self.assertEqual(rightList.save_to_string(), "embed")

        rightList = RightList(string="embed,resolve")
        self.assertEqual(rightList.save_to_string(), "embed,resolve")

    def testCanPerform(self):
        rightList = RightList(string="embed")
        self.assert_(rightList.can_perform("getticket"))
        self.assert_(not rightList.can_perform("resolve"))

        rightList = RightList(string="embed,resolve")
        self.assert_(rightList.can_perform("getticket"))
        self.assert_(rightList.can_perform("resolve"))


if __name__ == "__main__":
    unittest.main()
