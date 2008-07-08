from OpenSSL import crypto
import M2Crypto
from M2Crypto import X509
from M2Crypto import EVP

class Keypair:
   key = None       # public/private keypair
   m2key = None     # public key (m2crypto format)

   def __init__(self, create=False):
      if create:
         self.create()
      pass

   def create(self):
      self.key = crypto.PKey()
      self.key.generate_key(crypto.TYPE_RSA, 1024)

   def save_to_file(self, filename):
      open(filename, 'w').write(self.as_pem())

   def load_from_file(self, filename):
      buffer = open(filename, 'r').read()
      self.load_from_string(buffer)

   def load_from_string(self, string):
      self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, string)
      self.m2key = M2Crypto.EVP.load_key_string(string)

   def as_pem(self):
      return crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key)

   def get_m2_pkey(self):
      if not self.m2key:
         self.m2key = M2Crypto.EVP.load_key_string(self.as_pem())
      return self.m2key

   def get_openssl_pkey(self):
      return self.key

class Certificate:
   digest = "md5"

   data = None
   cert = None
   issuerKey = None
   issuerSubject = None
   parent = None

   def __init__(self, create=False, subject=None, string=None, filename=None):
       if create or subject:
           self.create()
       if subject:
           self.set_subject(subject)
       if string:
           self.load_from_string(string)
       if filename:
           self.load_from_file(filename)

   def create(self):
       self.cert = crypto.X509()
       self.cert.set_serial_number(1)
       self.cert.gmtime_adj_notBefore(0)
       self.cert.gmtime_adj_notAfter(60*60*24*365*5) # five years

   def load_from_string(self, string):
       # if it is a chain of multiple certs, then split off the first one and
       # load it
       parts = string.split("-----parent-----", 1)
       self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, parts[0])
       
       # if there are more certs, then create a parent and let the parent load
       # itself from the remainder of the string
       if len(parts) > 1:
           self.parent = Certificate()
           self.parent.load_from_string(parts[1])


   def load_from_file(self, filename):
       file = open(filename)
       string = file.read()
       self.load_from_string(string)

   def save_to_string(self, save_parents=False):
       string = crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert)
       if save_parents and self.parent:
          string = string + "-----parent-----" + self.parent.save_to_string(save_parents)
       return string

   def save_to_file(self, filename, save_parents=False):
       string = self.save_to_string(save_parents=save_parents)
       open(filename, 'w').write(string)

   def set_issuer(self, key, subject=None, cert=None):
       self.issuerKey = key
       if subject:
          # it's a mistake to use subject and cert params at the same time
          assert(not cert)
          if isinstance(subject, dict) or isinstance(subject, str):
             req = crypto.X509Req()
             reqSubject = req.get_subject()
             if (isinstance(subject, dict)):
                for key in reqSubject.keys():
                    setattr(reqSubject, key, name[key])
             else:
                setattr(reqSubject, "CN", subject)
             subject = reqSubject
             # subject is not valid once req is out of scope, so save req
             self.issuerReq = req
       if cert:
          # if a cert was supplied, then get the subject from the cert
          subject = cert.cert.get_issuer()
       assert(subject)
       self.issuerSubject = subject

   def get_issuer(self, which="CN"):
       x = self.cert.get_issuer()
       return getattr(x, which)

   def set_subject(self, name):
       req = crypto.X509Req()
       subj = req.get_subject()
       if (isinstance(name, dict)):
           for key in name.keys():
               setattr(subj, key, name[key])
       else:
           setattr(subj, "CN", name)
       self.cert.set_subject(subj)

   def get_subject(self, which="CN"):
       x = self.cert.get_subject()
       return getattr(x, which)

   def set_pubkey(self, key):
       assert(isinstance(key, Keypair))
       self.cert.set_pubkey(key.get_openssl_pkey())

   def get_pubkey(self):
       m2x509 = X509.load_cert_string(self.save_to_string())
       pkey = Keypair()
       pkey.key = self.cert.get_pubkey()
       pkey.m2key = m2x509.get_pubkey()
       return pkey

   def add_extension(self, name, critical, value):
       ext = crypto.X509Extension (name, critical, value)
       self.cert.add_extensions([ext])

   def get_extension(self, name):
       # pyOpenSSL does not have a way to get certificates
       m2x509 = X509.load_cert_string(self.save_to_string())
       value = m2x509.get_ext(name).get_value()
       return value

   def set_data(self, str):
       # pyOpenSSL only allows us to add extensions, so if we try to set the
       # same extension more than once, it will not work
       if self.data != None:
          raise "cannot set subjectAltName more than once"
       self.data = str
       self.add_extension("subjectAltName", 0, "URI:http://" + str)

   def get_data(self):
       if self.data:
           return self.data

       try:
           uri = self.get_extension("subjectAltName")
       except LookupError:
           self.data = None
           return self.data

       if not uri.startswith("URI:http://"):
           raise "bad encoding in subjectAltName"
       self.data = uri[11:]
       return self.data

   def sign(self):
       assert self.cert != None
       assert self.issuerSubject != None
       assert self.issuerKey != None
       self.cert.set_issuer(self.issuerSubject)
       self.cert.sign(self.issuerKey.get_openssl_pkey(), self.digest)

   def verify(self, pkey):
       # pyOpenSSL does not have a way to verify signatures
       m2x509 = X509.load_cert_string(self.save_to_string())
       m2pkey = pkey.get_m2_pkey()
       # verify it
       return m2x509.verify(m2pkey)

       # XXX alternatively, if openssl has been patched, do the much simpler:
       # try:
       #   self.cert.verify(pkey.get_openssl_key())
       #   return 1
       # except:
       #   return 0

   def is_signed_by_cert(self, cert):
       k = cert.get_pubkey()
       result = self.verify(k)
       return result

   def set_parent(self, p):
        self.parent = p

   def get_parent(self):
        return self.parent

   def verify_chain(self, trusted_certs = None):
        # if this cert is signed by a trusted_cert, then we are set
        for trusted_cert in trusted_certs:
            if self.is_signed_by_cert(trusted_cert):
                #print self.get_subject(), "is signed by a root"
                return True

        # if there is no parent, then no way to verify the chain
        if not self.parent:
            #print self.get_subject(), "has no parent"
            return False

        # if it wasn't signed by the parent...
        if not self.is_signed_by_cert(self.parent):
            #print self.get_subject(), "is not signed by parent"
            return False

        # if the parent isn't verified...
        if not self.parent.verify_chain(trusted_certs):
            #print self.get_subject(), "parent does not verify"
            return False

        return True
