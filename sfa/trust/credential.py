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

#import xml.dom.minidom
from xml.dom.minidom import Document, parseString
from sfa.trust.credential_legacy import CredentialLegacy
from sfa.trust.certificate import Certificate
from sfa.trust.rights import *
from sfa.trust.gid import *
from sfa.util.faults import *
from sfa.util.sfalogging import logger


# TODO:
# . SFA is using set_parent to do chaining, but that's no longer necessary
#   with the new credentials. fix.
#    . This probably requires setting up some sort of CA hierarchy.
# . Make sure that the creds pass xml verification (probably need some reordering)
# . Need to implement full verification (parent signatures etc).
# . remove verify_chain
# . make delegation per privilege instead of global
# . make privs match between PG and PL
# . what about tickets?  do they need to be redone to be like credentials?
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




#class Signature(object):

#class Signed_Credential(object):
    

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
    parent_xml = None
    signatures = []
    xml = None
    refid = None
    
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
        self.set_privileges(legacy.get_privileges())
        self.delegate = legacy.get_delegate()

    ##
    # Need the issuer's private key and name
    # @param key Keypair object containing the private key of the issuer
    # @param gid GID of the issuing authority

    def set_issuer_keys(self, privkey, gid):
        self.issuer_privkey = privkey
        self.issuer_gid = gid

    #def set_issuer(self, issuer):
    #    issuer = issuer

    #def set_subject(self, subject):
    #    subject = subject
        
    #def set_pubkey(self, pubkey):
    #    self.issuer_pubkey = pubkey


    ##
    # Store the parent's credential in self.parent_xml
    # Store the parent's signatures in self.signatures
    # Update this credential's refid
    def set_parent(self, cred):
        if not cred.xml:
            cred.encode()

        doc = parseString(cred.xml)
        signed = doc.getElementsByTagName("signed-credential")[0]
        cred = signed.getElementsByTagName("credential")[0]
        signatures = signed.getElementsByTagName("signatures")[0]
        sigs = signatures.getElementsByTagName("Signature")

        self.parent_xml = cred.toxml()
        self.signatures = []
        for sig in sigs:
            self.signatures.append(sig.toxml())

        self.updateRefID()
        

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

        # Create the XML document
        doc = Document()
        signed_cred = doc.createElement("signed-credential")
        doc.appendChild(signed_cred)  
        
        # Fill in the <credential> bit        
        cred = doc.createElement("credential")
        cred.setAttribute("xml:id", self.get_refid())
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
        if self.parent_xml:
            sdoc = parseString(self.parent_xml)
            p_cred = doc.importNode(sdoc.getElementsByTagName("credential")[0], True)
            p = doc.createElement("parent")
            p.appendChild(p_cred)
            cred.appendChild(p)


        # Create the <signatures> tag
        signatures = doc.createElement("signatures")
        signed_cred.appendChild(signatures)

        # Add any parent signatures
        if self.parent_xml:
            for sig in self.signatures:
                sdoc = parseString(sig)
                ele = doc.importNode(sdoc.getElementsByTagName("Signature")[0], True)
                signatures.appendChild(ele)

        # Get the finished product
        self.xml = doc.toxml()
        #print doc.toxml()
        #self.sign()


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

    def get_refid(self):
        if not self.refid:
            self.refid = 'ref0'
        return self.refid

    def set_refid(self, rid):
        self.refid = rid

    ##
    # Figure out what refids exist, and update this credential's id
    # so that it doesn't clobber the others.  Returns the refids of
    # the parents.
    
    def updateRefID(self):
        if not self.parent_xml:
            self.set_refid('ref0')
            return []
        
        refs = []

        next_cred = Credential(string=self.parent_xml)
        while next_cred:
            refs.append(next_cred.get_refid())
            if next_cred.parent_xml:
                next_cred = Credential(string=next_cred.parent_xml)
            else:
                next_cred = None
        
        # Find a unique refid for this credential
        rid = self.get_refid()
        while rid in refs:
            val = int(rid[3:])
            rid = "ref%d" % (val + 1)

        # Set the new refid
        self.set_refid(rid)

        # Return the set of parent credential ref ids
        return refs

    

    def sign(self):
        if not self.issuer_privkey or not self.issuer_gid:
            return
        
        if not self.xml:
            self.encode()

        doc = parseString(self.xml)
        sigs = doc.getElementsByTagName("signatures")[0]
        # Create the signature template
        refid = self.get_refid()
        sz_sig = signature_template % (refid,refid)
        sdoc = parseString(sz_sig)
        sig_ele = doc.importNode(sdoc.getElementsByTagName("Signature")[0], True)
        sigs.appendChild(sig_ele)

        self.xml = doc.toxml()

        
        # Call out to xmlsec1 to sign it
        ref = 'Sig_%s' % self.get_refid()
        filename = self.save_to_random_tmp_file()
        signed = os.popen('/usr/bin/xmlsec1 --sign --node-id "%s" --privkey-pem %s,%s %s' \
                 % (ref, self.issuer_privkey, self.issuer_gid, filename)).read()
        os.remove(filename)


        self.xml = signed

    def getTextNode(self, element, subele):
        sub = element.getElementsByTagName(subele)[0]
        if len(sub.childNodes) > 0:            
            return sub.childNodes[0].nodeValue
        else:
            return None
        
    ##
    # Retrieve the attributes of the credential from the XML.
    # This is automatically caleld by the various get_* methods of
    # this class and should not need to be called explicitly.

    def decode(self):
        doc = parseString(self.xml)
        sigs = None
        signed_cred = doc.getElementsByTagName("signed-credential")

        # Is this a signed-cred or just a cred?
        if len(signed_cred) > 0:
            cred = signed_cred[0].getElementsByTagName("credential")[0]
            signatures = signed_cred[0].getElementsByTagName("signatures")
            if len(signatures) > 0:
                sigs = signatures[0].getElementsByTagName("Signature")
        else:
            cred = doc.getElementsByTagName("credential")[0]
        


        self.set_refid(cred.getAttribute("xml:id"))
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

        # Is there a parent?
        parent = cred.getElementsByTagName("parent")
        if len(parent) > 0:
            self.parent_xml = self.getTextNode(cred, "parent")
            self.updateRefID()

        # Get the signatures
        for sig in sigs:
            self.signatures.append(sig.toxml())
            
    ##
    # Verify that:
    # . All of the signatures are valid and that the issuers trace back
    #   to trusted roots (performed by xmlsec1)
    # . That the issuer of the credential is the authority in the target's urn
    #    . In the case of a delegated credential, this must be true of the root
    #
    # -- For Delegates (credentials with parents)
    # . The privileges must be a subset of the parent credentials
    # . The privileges must have "can_delegate" set for each delegated privilege
    # . The target gid must be the same between child and parents
    # . The expiry time on the child must be no later than the parent
    # . The signer of the child must be the owner of the parent
    #
    # -- Verify does *NOT*
    # . ensure that an xmlrpc client's gid matches a credential gid, that
    #   must be done elsewhere
    #
    # @param trusted_certs: The certificates of trusted CA certificates
    
    def verify(self, trusted_certs):
        logger.info("verifying cert")
        if not self.xml:
            self.decode()        

        # Verify the signatures
        filename = self.save_to_random_tmp_file()
        cert_args = " ".join(['--trusted-pem %s' % x for x in trusted_certs])

        
        refs = []
        refs.append("Sig_%s" % self.get_refid())

        parentRefs = self.updateRefID()
        for ref in parentRefs:
            refs.append("Sig_%s" % ref)

        for ref in refs:
            logger.info('/usr/bin/xmlsec1 --verify --node-id "%s" %s %s 2>&1' \
                            % (ref, cert_args, filename))
            verified = os.popen('/usr/bin/xmlsec1 --verify --node-id "%s" %s %s 2>&1' \
                            % (ref, cert_args, filename)).read()
            if not verified.strip().startswith("OK"):
                raise CredentialNotVerifiable("xmlsec1 error: " + verified)

        os.remove(filename)

        # Verify the parents (delegation)
        #if self.parent_xml:
        #    self.verify_parent(Credential(string=self.parent_xml))

        # Make sure the issuer is the target's authority
        self.verify_issuer()



    ##
    # Make sure the issuer of this credential is the target's authority
    def verify_issuer(self):
        target_authority = get_authority(self.get_gid_object().get_hrn())

        # Find the root credential's refid
        cur_cred = self
        root_refid = None
        while cur_cred:            
            if cur_cred.parent_xml:
                cur_cred = Credential(string=cur_cred.parent_xml)
            else:
                root_refid = "Sig_%s" % cur_cred.get_refid()                
                cur_cred = None

        # Find the signature for the root credential
        root_issuer = None
        for sig in self.signatures:
            doc = parseString(sig)
            esig = doc.getElementsByTagName("Signature")[0]
            ref = esig.getAttribute("xml:id")
            if ref.lower() == root_refid.lower():
                # Found the right signature, look for the issuer
                keyinfo = esig.getElementsByTagName("X509Data")[0]
                root_issuer = self.getTextNode(keyinfo, "X509SubjectName")
                root_issuer = root_issuer.strip('CN=')
                
        # Ensure that the signer of the root credential is the target_authority
        root_issuer = hrn_to_urn(root_issuer, 'authority')
        target_authority = hrn_to_urn(target_authority, 'authority')

        if root_issuer != target_authority:
            raise CredentialNotVerifiable("issuer (%s) != authority of target (%s)" \
                                          % (root_issuer, target_authority))
                                          
        
    def verify_parent(self, parent_cred):
        if parent_cred.parent_xml:
            parent_cred.verify_parent(Credential(string=parent_cred.parent_xml))

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

        if self.parent_xml and dump_parents:
           print "PARENT",
           #self.parent.dump(dump_parents)

