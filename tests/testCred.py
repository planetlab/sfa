import unittest
from sfa.trust.credential import *
from sfa.trust.rights import *
from sfa.trust.gid import *
from sfa.trust.certificate import *

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

      cred.set_expiration(datetime.datetime.utcnow() + datetime.timedelta(seconds=lifeTime))
      
      cred.set_privileges(rights)
      self.assertEqual(cred.get_privileges().save_to_string(), rights)

      cred.get_privileges().delegate_all_privileges(delegate)

      cred.encode()

      cred_str = cred.save_to_string()

      # re-load the credential from a string and make sure its fields are
      # intact
      cred2 = Credential(string = cred_str)
      self.assertEqual(cred2.get_gid_caller().get_subject(), gidCaller.get_subject())
      self.assertEqual(cred2.get_gid_object().get_subject(), gidObject.get_subject())
      self.assertEqual(cred2.get_privileges().get_all_delegate(), delegate)
      self.assertEqual(cred2.get_privileges().save_to_string(), rights)



   def createSignedGID(self, subject, urn, issuer_pkey = None, issuer_gid = None):
      gid = GID(subject=subject, uuid=1, urn=urn)
      keys = Keypair(create=True)
      gid.set_pubkey(keys)
      if issuer_pkey:
         gid.set_issuer(issuer_pkey, str(issuer_gid.get_issuer()))
      else:
         gid.set_issuer(keys, subject)

      gid.encode()
      gid.sign()
      return gid, keys

   
   

   def testDelegationAndVerification(self):
      gidAuthority, keys = self.createSignedGID("site", "urn:publicid:IDN+plc+authority+site")
      gidCaller, ckeys = self.createSignedGID("site.foo", "urn:publicid:IDN+plc:site+user+foo",
                                          keys, gidAuthority)
      gidObject, _ = self.createSignedGID("site.slice", "urn:publicid:IDN+plc:site+slice+bar_slice",
                                          keys, gidAuthority)
      gidDelegatee, _ = self.createSignedGID("site.delegatee", "urn:publicid:IDN+plc:site+user+delegatee",
                                             keys, gidAuthority)

      cred = Credential()
      cred.set_gid_caller(gidCaller)
      cred.set_gid_object(gidObject)
      cred.set_expiration(datetime.datetime.utcnow() + datetime.timedelta(seconds=3600))
      cred.set_privileges("embed:1, bind:1")
      cred.encode()

      gidAuthority.save_to_file("/tmp/auth_gid")
      keys.save_to_file("/tmp/auth_key")
      cred.set_issuer_keys("/tmp/auth_key", "/tmp/auth_gid")
      cred.sign()


      cred.verify(['/tmp/auth_gid'])

      # Test copying
      cred2 = Credential(string=cred.save_to_string())
      cred2.verify(['/tmp/auth_gid'])


      # Test delegation
      delegated = Credential()
      delegated.set_gid_caller(gidDelegatee)
      delegated.set_gid_object(gidObject)      
      delegated.set_parent(cred)
      delegated.set_expiration(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))
      delegated.set_privileges("embed:1, bind:1")
      gidCaller.save_to_file("/tmp/caller_gid")
      ckeys.save_to_file("/tmp/caller_pkey")      
      
      delegated.set_issuer_keys("/tmp/caller_pkey", "/tmp/caller_gid")

      delegated.encode()

      delegated.sign()
      
      # This should verify
      delegated.verify(['/tmp/auth_gid'])

      backup = Credential(string=delegated.get_xml())

      # Test that verify catches an incorrect lifetime      
      delegated.set_expiration(datetime.datetime.utcnow() + datetime.timedelta(seconds=6000))
      delegated.encode()
      delegated.sign()
      try:
         delegated.verify(['/tmp/auth_gid'])
         assert(1==0)
      except CredentialNotVerifiable:
         pass

      # Test that verify catches an incorrect signer
      delegated = Credential(string=backup.get_xml())
      delegated.set_issuer_keys("/tmp/auth_key", "/tmp/auth_gid")
      delegated.encode()
      delegated.sign()

      try:
         delegated.verify(['/tmp/auth_gid'])
         assert(1==0)
      except CredentialNotVerifiable:
         pass


      # Test that verify catches a changed gid
      delegated = Credential(string=backup.get_xml())
      delegated.set_gid_object(delegated.get_gid_caller())
      delegated.encode()
      delegated.sign()

      try:
         delegated.verify(['/tmp/auth_gid'])
         assert(1==0)
      except CredentialNotVerifiable:
         pass


      # Test that verify catches a credential with the wrong authority for the object
      test = Credential(string=cred.get_xml())
      test.set_issuer_keys("/tmp/caller_pkey", "/tmp/caller_gid")
      test.encode()
      test.sign()

      try:
         test.verify(['/tmp/auth_gid'])
         assert(1==0)
      except CredentialNotVerifiable:
         pass      
      
      # Test that * gets translated properly

if __name__ == "__main__":
    unittest.main()
