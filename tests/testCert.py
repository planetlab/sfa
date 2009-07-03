import unittest
import xmlrpclib
from sfa.trust.certificate import Certificate, Keypair

class TestCert(unittest.TestCase):
   def setUp(self):
      pass

   def testCreate(self):
      cert = Certificate()
      cert.create()

   def testSetAndGetSubject(self):
      cert = Certificate()
      cert.create()
      cert.set_subject("test")
      subj = cert.get_subject()
      self.assertEqual(subj, "test")

   def testSign(self):
      cert = Certificate(subject="test")

      # create an issuer and sign the certificate
      issuerKey = Keypair(create=True)
      issuerSubject = "testissuer"
      cert.set_issuer(issuerKey, issuerSubject)
      cert.sign()

   def testAddExtension(self):
      cert = Certificate(subject="test")
      cert.add_extension("subjectAltName", 0, "URI:http://foovalue")

      self.assertEqual(cert.get_extension("subjectAltName"),
                       "URI:http://foovalue")

   def testSetData(self):
      cert = Certificate(subject="test")
      data = "this is a test"
      cert.set_data(data)
      self.assertEqual(cert.get_data(), data)

      # try something a bit more complicated, like an xmlrpc encoding of
      # some parameters
      cert = Certificate(subject="test")
      data = xmlrpclib.dumps((1, "foo", ["a", "b"], {"c": "d", "e": "f"}, True))
      cert.set_data(data)
      self.assertEqual(cert.get_data(), data)


   def testSaveAndLoadString(self):
      cert = Certificate(subject="test")
      cert.add_extension("subjectAltName", 0, "URI:http://foovalue")

      # create an issuer and sign the certificate
      issuerKey = Keypair(create=True)
      issuerSubject = "testissuer"
      cert.set_issuer(issuerKey, issuerSubject)
      cert.sign()

      certstr = cert.save_to_string()

      #print certstr

      cert2 = Certificate()
      cert2.load_from_string(certstr)

      # read back the subject and make sure it is correct
      subj = cert2.get_subject()
      self.assertEqual(subj, "test")

      # read back the issuer and make sure it is correct
      issuerName = cert2.get_issuer()
      self.assertEqual(issuerName, "testissuer")

      # read back the extension and make sure it is correct
      self.assertEqual(cert2.get_extension("subjectAltName"),
                       "URI:http://foovalue")

   def testLongExtension(self):
      cert = Certificate(subject="test")

      # should produce something around 256 KB
      veryLongString = "URI:http://"
      shortString = ""
      for i in range(1, 80):
          shortString = shortString + "abcdefghijklmnopqrstuvwxyz012345"
      for i in range(1, 100):
          veryLongString = veryLongString + shortString + str(i)

      cert.add_extension("subjectAltName", 0, veryLongString)

      # create an issuer and sign the certificate
      issuerKey = Keypair(create=True)
      issuerSubject = "testissuer"
      cert.set_issuer(issuerKey, issuerSubject)
      cert.sign()

      certstr = cert.save_to_string()

      cert2 = Certificate()
      cert2.load_from_string(certstr)
      val = cert2.get_extension("subjectAltName")
      self.assertEqual(val, veryLongString)

   def testVerify(self):
      cert = Certificate(subject="test")

      # create an issuer and sign the certificate
      issuerKey = Keypair(create=True)
      issuerSubject = "testissuer"
      cert.set_issuer(issuerKey, issuerSubject)
      cert.sign()

      result = cert.verify(issuerKey)
      self.assert_(result)

      # create another key
      issuerKey2 = Keypair(create=True)
      issuerSubject2 = "wrongissuer"

      # and make sure it doesn't verify
      result = cert.verify(issuerKey2)
      self.assert_(not result)

      # load the cert from a string, and verify again
      cert2 = Certificate(string = cert.save_to_string())
      result = cert2.verify(issuerKey)
      self.assert_(result)
      result = cert2.verify(issuerKey2)
      self.assert_(not result)

   def test_is_signed_by(self):
      cert1 = Certificate(subject="one")

      key1 = Keypair()
      key1.create()
      cert1.set_pubkey(key1)

      # create an issuer and sign the certificate
      issuerKey = Keypair(create=True)
      issuerSubject = "testissuer"
      cert1.set_issuer(issuerKey, issuerSubject)
      cert1.sign()

      cert2 = Certificate(subject="two")

      key2 = Keypair(create=True)
      cert2.set_pubkey(key2)

      cert2.set_issuer(key1, cert=cert1)

      # cert2 is signed by cert1
      self.assert_(cert2.is_signed_by_cert(cert1))
      # cert1 is not signed by cert2
      self.assert_(not cert1.is_signed_by_cert(cert2))

   def test_parents(self):
      cert_root = Certificate(subject="root")
      key_root = Keypair(create=True)
      cert_root.set_pubkey(key_root)
      cert_root.set_issuer(key_root, "root")
      cert_root.sign()

      cert1 = Certificate(subject="one")
      key1 = Keypair(create=True)
      cert1.set_pubkey(key1)
      cert1.set_issuer(key_root, "root")
      cert1.sign()

      cert2 = Certificate(subject="two")
      key2 = Keypair(create=True)
      cert2.set_pubkey(key2)
      cert2.set_issuer(key1, cert=cert1)
      cert2.set_parent(cert1)
      cert2.sign()

      cert3 = Certificate(subject="three")
      key3 = Keypair(create=True)
      cert3.set_pubkey(key3)
      cert3.set_issuer(key2, cert=cert2)
      cert3.set_parent(cert2)
      cert3.sign()

      self.assert_(cert1.verify(key_root))
      self.assert_(cert2.is_signed_by_cert(cert1))
      self.assert_(cert3.is_signed_by_cert(cert2))

      cert3.verify_chain([cert_root])

      # now save the chain to a string and load it into a new certificate
      str_chain = cert3.save_to_string(save_parents=True)
      cert4 = Certificate(string = str_chain)

      # verify the newly loaded chain still verifies
      cert4.verify_chain([cert_root])

      # verify the parentage
      self.assertEqual(cert4.get_parent().get_subject(), "two")
      self.assertEqual(cert4.get_parent().get_parent().get_subject(), "one")



if __name__ == "__main__":
    unittest.main()
