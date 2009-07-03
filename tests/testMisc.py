import unittest
from sfa.util.misc import *

class TestMisc(unittest.TestCase):
   def setUp(self):
      pass

   def testGetLeft(self):
      self.assertEqual(get_leaf("foo"), "foo")
      self.assertEqual(get_leaf("foo.bar"), "bar")

   def testGetAuthority(self):
      self.assertEqual(get_authority("foo"), "")
      self.assertEqual(get_authority("foo.bar"), "foo")
      self.assertEqual(get_authority("foo.bar.x"), "foo.bar")

if __name__ == "__main__":
    unittest.main()
