import unittest
from sfa.trust.credential import *
from sfa.trust.rights import *
from sfa.trust.gid import *

class TestCred(unittest.TestCase):
   def setUp(self):
      pass

   def testCreate(self):
      cred = Credential(create=True)

   def testDefaults(self):
      cred = Credential(subject="testCredential")

      self.assertEqual(cred.get_gid_caller(), None)
      self.assertEqual(cred.get_gid_object(), None)

   def testLoadSave(self):
      cred = Credential(subject="testCredential")

      gidCaller = GID(subject="caller", uuid=create_uuid(), hrn="foo.caller")
      gidObject = GID(subject="object", uuid=create_uuid(), hrn="foo.object")
      lifeTime = 12345
      delegate = True
      rights = "embed:1,bind:1"

      cred.set_gid_caller(gidCaller)
      self.assertEqual(cred.get_gid_caller().get_subject(), gidCaller.get_subject())

      cred.set_gid_object(gidObject)
      self.assertEqual(cred.get_gid_object().get_subject(), gidObject.get_subject())

      cred.set_lifetime(lifeTime)
      self.assertEqual(cred.get_lifetime(), lifeTime)

      cred.set_privileges(rights)
      self.assertEqual(cred.get_privileges().save_to_string(), rights)

      cred.encode()

      cred_str = cred.save_to_string()

      # re-load the credential from a string and make sure it's fields are
      # intact
      cred2 = Credential(string = cred_str)
      self.assertEqual(cred2.get_gid_caller().get_subject(), gidCaller.get_subject())
      self.assertEqual(cred2.get_gid_object().get_subject(), gidObject.get_subject())
      self.assertEqual(cred2.get_lifetime(), lifeTime)
      self.assertEqual(cred2.get_delegate(), delegate)
      self.assertEqual(cred2.get_privileges().save_to_string(), rights)

if __name__ == "__main__":
    unittest.main()
