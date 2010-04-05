##
# Implements SFA Credentials
#
# Credentials are layered on top of certificates, and are essentially a
# certificate that stores a tuple of parameters.
##

### $Id$
### $URL$

import xmlrpclib
import random
import os
import datetime

import xml.dom.minidom
from xml.dom.minidom import Document
from sfa.trust.credential_legacy import CredentialLegacy
from sfa.trust.certificate import Certificate
from sfa.trust.rights import *
from sfa.trust.gid import *
from sfa.util.faults import *
from sfa.util.sfalogging import logger


# TODO:
# . Need to verify credential parents (delegation)
# . implement verify_chain
# . Need to manage ref #s
# . Need to add privileges (make PG and PL privs work together and add delegation per privilege instead of global)
# . Need to test

signature_template = \
'''
<Signature xml:id="Sig_%s" xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo>
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
      <Reference URI="#%s">
      <Transforms>
        <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
      </Transforms>
      <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
      <DigestValue></DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue />
      <KeyInfo>
        <X509Data>
          <X509SubjectName/>
          <X509IssuerSerial/>
          <X509Certificate/>
        </X509Data>
      <KeyValue />
      </KeyInfo>
    </Signature>
'''



##
# Credential is a tuple:
#    (GIDCaller, GIDObject, Expiration (in UTC time), Privileges, DelegateBit)
#
# These fields are encoded in one of two ways.  The legacy style places
# it in the subjectAltName of an X509 certificate.  The new credentials
# are placed in signed XML.


class Credential(object):
    gidCaller = None
    gidObject = None
    expiration = None
    privileges = None
    delegate = False
    issuer_privkey = None
    issuer_gid = None
    issuer_pubkey = None
    parent = None
    xml = None
    max_refid = 0
    ##
    # Create a Credential object
    #
    # @param create If true, create a blank x509 certificate
    # @param subject If subject!=None, create an x509 cert with the subject name
    # @param string If string!=None, load the credential from the string
    # @param filename If filename!=None, load the credential from the file

    def __init__(self, create=False, subject=None, string=None, filename=None):

        # Check if this is a legacy credential, translate it if so
        if string or filename:
            if string:                
                str = string
            elif filename:
                str = file(filename).read()
                
            if str.strip().startswith("-----"):
                self.translate_legacy(str)
            else:
                self.xml = str
                self.decode()
                
    ##
    # Translate a legacy credential into a new one
    #
    # @param String of the legacy credential

    def translate_legacy(self, str):
        legacy = CredentialLegacy(False,string=str)
        self.gidCaller = legacy.get_gid_caller()
        self.gidObject = legacy.get_gid_object()
        lifetime = legacy.get_lifetime()
        if not lifetime:
            self.set_lifetime(3600)
        else:
            self.set_lifetime(int(lifetime))
        self.lifeTime = legacy.get_lifetime()
        self.privileges = legacy.get_privileges()
        self.delegate = legacy.get_delegate()

    ##
    # Need the issuer's private key and name
    # @param key Keypair object containing the private key of the issuer
    # @param gid GID of the issuing authority

    def set_issuer_keys(self, privkey, gid):
        self.issuer_privkey = privkey
        self.issuer_gid = gid

    def set_issuer(self, issuer):
        issuer = issuer

    def set_subject(self, subject):
        subject = subject
        
    def set_pubkey(self, pubkey):
        self.issuer_pubkey = pubkey

    def set_parent(self, cred):
        self.parent = cred

    ##
    # set the GID of the caller
    #
    # @param gid GID object of the caller

    def set_gid_caller(self, gid):
        self.gidCaller = gid
        # gid origin caller is the caller's gid by default
        self.gidOriginCaller = gid

    ##
    # get the GID of the object

    def get_gid_caller(self):
        if not self.gidCaller:
            self.decode()
        return self.gidCaller

    ##
    # set the GID of the object
    #
    # @param gid GID object of the object

    def set_gid_object(self, gid):
        self.gidObject = gid

    ##
    # get the GID of the object

    def get_gid_object(self):
        if not self.gidObject:
            self.decode()
        return self.gidObject

    ##
    # set the lifetime of this credential
    #
    # @param lifetime lifetime of credential
    # . if lifeTime is a datetime object, it is used for the expiration time
    # . if lifeTime is an integer value, it is considered the number of minutes
    #   remaining before expiration

    def set_lifetime(self, lifeTime):
        if isinstance(lifeTime, int):
            self.expiration = datetime.timedelta(seconds=lifeTime*60) + datetime.datetime.utcnow()
        else:
            self.expiration = lifeTime

    ##
    # get the lifetime of the credential (in minutes)

    def get_lifetime(self):
        if not self.lifeTime:
            self.decode()
        return self.expiration

    ##
    # set the delegate bit
    #
    # @param delegate boolean (True or False)

    def set_delegate(self, delegate):
        self.delegate = delegate

    ##
    # get the delegate bit

    def get_delegate(self):
        if not self.delegate:
            self.decode()
        return self.delegate

    ##
    # set the privileges
    #
    # @param privs either a comma-separated list of privileges of a RightList object

    def set_privileges(self, privs):
        if isinstance(privs, str):
            self.privileges = RightList(string = privs)
        else:
            self.privileges = privs

    ##
    # return the privileges as a RightList object

    def get_privileges(self):
        if not self.privileges:
            self.decode()
        return self.privileges

    ##
    # determine whether the credential allows a particular operation to be
    # performed
    #
    # @param op_name string specifying name of operation ("lookup", "update", etc)

    def can_perform(self, op_name):
        rights = self.get_privileges()
        
        if not rights:
            return False

        return rights.can_perform(op_name)

    def append_sub(self, doc, parent, element, text):
        ele = doc.createElement(element)
        ele.appendChild(doc.createTextNode(text))
        parent.appendChild(ele)

    ##
    # Encode the attributes of the credential into an XML string    
    # This should be done immediately before signing the credential.    

    def encode(self):
        p_sigs = None

        # Get information from the parent credential
        if self.parent:
            if not self.parent.xml:
                self.parent.encode()            
            p_doc = xml.dom.minidom.parseString(self.parent.xml)
            p_signed_cred = p_doc.getElementsByTagName("signed-credential")[0]
            p_cred = p_signed_cred.getElementsByTagName("credential")[0]               
            p_signatures = p_signed_cred.getElementsByTagName("signatures")[0]
            p_sigs = p_signatures.getElementsByTagName("Signature")

        # Create the XML document
        doc = Document()
        signed_cred = doc.createElement("signed-credential")
        doc.appendChild(signed_cred)  
        

        # Fill in the <credential> bit
        refid = "ref%d" % (self.max_refid + 1)
        self.max_refid += 1
        
        cred = doc.createElement("credential")
        cred.setAttribute("xml:id", refid)
        signed_cred.appendChild(cred)
        self.append_sub(doc, cred, "type", "privilege")
        self.append_sub(doc, cred, "serial", "8")
        self.append_sub(doc, cred, "owner_gid", self.gidCaller.save_to_string())
        self.append_sub(doc, cred, "owner_urn", self.gidCaller.get_urn())
        self.append_sub(doc, cred, "target_gid", self.gidObject.save_to_string())
        self.append_sub(doc, cred, "target_urn", self.gidObject.get_urn())
        self.append_sub(doc, cred, "uuid", "")
        if  not self.expiration:
            self.set_lifetime(3600)
        self.expiration = self.expiration.replace(microsecond=0)
        self.append_sub(doc, cred, "expires", self.expiration.isoformat())
        privileges = doc.createElement("privileges")
        cred.appendChild(privileges)

        if self.privileges:
            rights = self.privileges.save_to_string().split(",")
            for right in rights:
                priv = doc.createElement("privilege")
                self.append_sub(doc, priv, "name", right.strip())
                self.append_sub(doc, priv, "can_delegate", str(self.delegate))
                privileges.appendChild(priv)

        # Add the parent credential if it exists
        if self.parent:
            parent = doc.createElement("parent")
            parent.appendChild(p_cred)
            cred.appendChild(parent)
        

        signed_cred.appendChild(cred)


        # Fill in the <signature> bit
        signatures = doc.createElement("signatures")

        sz_sig = signature_template % (refid,refid)

        sdoc = xml.dom.minidom.parseString(sz_sig)
        sig_ele = doc.importNode(sdoc.getElementsByTagName("Signature")[0], True)
        signatures.appendChild(sig_ele)
        
        # Add any existing signatures from the parent credential
        if p_sigs:
            for sig in p_sigs:
                signatures.appendChild(sig)


        # Add any parent signatures
        if self.parent:
            for sig in p_sigs:
                signatures.appendChild(sig)

        signed_cred.appendChild(signatures)
        # Get the finished product
        self.xml = doc.toxml()
        #print doc.toprettyxml()


    def save_to_random_tmp_file(self):
        filename = "/tmp/cred_%d" % random.randint(0,999999999)
        self.save_to_file(filename)
        return filename
    
    def save_to_file(self, filename, save_parents=True):
        if not self.xml:
            self.encode()
        f = open(filename, "w")
        f.write(self.xml)
        f.close()

    def save_to_string(self, save_parents=True):
        if not self.xml:
            self.encode()
        return self.xml

    def sign(self):
        if not self.xml:
            self.encode()
        
        # Call out to xmlsec1 to sign it
        ref = 'Sig_ref%d' % self.max_refid
        filename = self.save_to_random_tmp_file()
        signed = os.popen('/usr/bin/xmlsec1 --sign --node-id "%s" --privkey-pem %s,%s %s' \
                 % (ref, self.issuer_privkey, self.issuer_gid, filename)).read()
        os.remove(filename)

        self.xml = signed

    def getTextNode(self, element, subele):
        sub = element.getElementsByTagName(subele)[0]
        return sub.childNodes[0].nodeValue

    ##
    # Retrieve the attributes of the credential from the XML.
    # This is automatically caleld by the various get_* methods of
    # this class and should not need to be called explicitly.

    def decode(self):
        doc = xml.dom.minidom.parseString(self.xml)
        signed_cred = doc.getElementsByTagName("signed-credential")[0]
        cred = signed_cred.getElementsByTagName("credential")[0]
        signatures = signed_cred.getElementsByTagName("signatures")[0]
        sigs = signatures.getElementsByTagName("Signature")


        self.max_refid = int(cred.getAttribute("xml:id")[3:])
        sz_expires = self.getTextNode(cred, "expires")
        if sz_expires != '':
            self.expiration = datetime.datetime.strptime(sz_expires, '%Y-%m-%dT%H:%M:%S')            
        self.lifeTime = self.getTextNode(cred, "expires")
        self.gidCaller = GID(string=self.getTextNode(cred, "owner_gid"))
        self.gidObject = GID(string=self.getTextNode(cred, "target_gid"))
        privs = cred.getElementsByTagName("privileges")[0]
        sz_privs = ''
        delegates = []
        for priv in privs.getElementsByTagName("privilege"):
            sz_privs += self.getTextNode(priv, "name")
            sz_privs += ","
            delegates.append(self.getTextNode(priv, "can_delegate"))

        # Can we delegate?
        delegate = False
        if "false" not in delegates:
            self.delegate = True

        # Make the rights list
        sz_privs.rstrip(", ")
        self.privileges = RightList(string=sz_privs)
        self.delegate

        
    ##
    # For a simple credential (no delegation) verify..
    # . That the signature is valid for the credential's xml:id
    # . That the signer's pub key matches the pub key of the target (object)
    # . That the target/owner urns match those in the gids
    #
    # @param trusted_certs: The certificates of trusted CA certificates
    
    def verify(self, trusted_certs):
        if not self.xml:
            self.decode()        

        # Verify the sigatures
        filename = self.save_to_random_tmp_file()
        cert_args = " ".join(['--trusted-pem %s' % x for x in trusted_certs])

        ref = "Sig_ref%d" % self.max_refid
        verified = os.popen('/usr/bin/xmlsec1 --verify --node-id "%s" %s %s 2>&1' \
                            % (ref, cert_args, filename)).read()

        if not verified.strip().startswith("OK"):
            raise CredentialNotVerifiable("xmlsec1 error: " + verified)

        os.remove(filename)

    ##
    # Verify that a chain of credentials is valid (see cert.py:verify). In
    # addition to the checks for ordinary certificates, verification also
    # ensures that the delegate bit was set by each parent in the chain. If
    # a delegate bit was not set, then an exception is thrown.
    #
    # Each credential must be a subset of the rights of the parent.

    def verify_chain(self, trusted_certs):
        return

 ##    def verify_chain(self, trusted_certs = None):
##         # do the normal certificate verification stuff
##         Certificate.verify_chain(self, trusted_certs)

##         if self.parent:
##             # make sure the parent delegated rights to the child
##             if not self.parent.get_delegate():
##                 raise MissingDelegateBit(self.parent.get_subject())

##             # make sure the rights given to the child are a subset of the
##             # parents rights
##             if not self.parent.get_privileges().is_superset(self.get_privileges()):
##                 raise ChildRightsNotSubsetOfParent(self.get_subject() 
##                                                    + " " + self.parent.get_privileges().save_to_string()
##                                                    + " " + self.get_privileges().save_to_string())

##         return

    ##
    # Dump the contents of a credential to stdout in human-readable format
    #
    # @param dump_parents If true, also dump the parent certificates

    def dump(self, dump_parents=False):
        print "CREDENTIAL", self.get_subject()

        print "      privs:", self.get_privileges().save_to_string()

        print "  gidCaller:"
        gidCaller = self.get_gid_caller()
        if gidCaller:
            gidCaller.dump(8, dump_parents)

        print "  gidObject:"
        gidObject = self.get_gid_object()
        if gidObject:
            gidObject.dump(8, dump_parents)

        print "   delegate:", self.get_delegate()

        if self.parent and dump_parents:
           print "PARENT",
           self.parent.dump(dump_parents)

