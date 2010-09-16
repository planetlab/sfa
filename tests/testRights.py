import unittest
from sfa.trust.rights import *

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

   def testIsSuperset(self):
      pright = Right("sa")
      cright = Right("embed")
      self.assert_(pright.is_superset(cright))
      self.assert_(not cright.is_superset(pright))

      pright = Right("embed")
      cright = Right("embed")
      self.assert_(pright.is_superset(cright))
      self.assert_(cright.is_superset(pright))

      pright = Right("control")
      cright = Right("embed")
      self.assert_(not pright.is_superset(cright))
      self.assert_(not cright.is_superset(pright))

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

    def testIsSuperset(self):
        pRightList = RightList(string="sa")
        cRightList = RightList(string="embed")
        self.assert_(pRightList.is_superset(cRightList))
        self.assert_(not cRightList.is_superset(pRightList))

        pRightList = RightList(string="embed")
        cRightList = RightList(string="embed")
        self.assert_(pRightList.is_superset(cRightList))
        self.assert_(cRightList.is_superset(pRightList))

        pRightList = RightList(string="control")
        cRightList = RightList(string="embed")
        self.assert_(not pRightList.is_superset(cRightList))
        self.assert_(not cRightList.is_superset(pRightList))

        pRightList = RightList(string="control,sa")
        cRightList = RightList(string="embed")
        self.assert_(pRightList.is_superset(cRightList))
        self.assert_(not cRightList.is_superset(pRightList))


if __name__ == "__main__":
    unittest.main()
