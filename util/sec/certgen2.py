#!/usr/bin/env python

"""
Certificate generation module.
"""

from OpenSSL     import crypto
from os          import chmod, remove
from os.path     import join

from myap.tools  import execute_cmd
from myap.config import config

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA

YEAR = 60*60*24*365

X509Attr    = ( 'C', 'ST', 'L', 'O', 'OU', 'CN', 'emailAddress' )
X509WinAttr = { 'C'            : 'C',
                'ST'           : 'S',
                'L'            : 'L',
                'O'            : 'O',
                'OU'           : 'OU',
                'CN'           : 'CN',
                'emailAddress' : 'E' }

def createKeyPair(type, bits):
    """
    Create a public/private key pair.

    Arguments: type - Key type, must be one of TYPE_RSA and TYPE_DSA
               bits - Number of bits to use in the key

    Returns:   The public/private key pair in a PKey object
    """

    pkey = crypto.PKey()
    pkey.generate_key(type, bits)

    return pkey

def createCertRequest(pkey, subject, digest='md5'):
    """
    Create a certificate request.

    Arguments: pkey    - The key to associate with the request
               subject - A dictionary with the subject of the request, possible
                         key,value pairs are:
                           C            - Country name
                           ST           - State or province name
                           L            - Locality name
                           O            - Organization name
                           OU           - Organizational unit name
                           CN           - Common name
                           emailAddress - E-mail address
               digest  - Digestion method to use for signing, default is md5

    Returns:   The certificate request in an X509Req object
    """

    req  = crypto.X509Req()
    subj = req.get_subject()

    # Storing attributes in the correct order
    for attr in X509Attr:
        if subject.has_key(attr):
            setattr(subj, attr, subject[attr])

    req.set_pubkey(pkey)
    req.sign(pkey, digest)

    return req

def createCertificate(req, (issuerKey, issuerCert), serial, (notBefore, notAfter), extensions=[], digest='md5'):
    """
    Generate a certificate given a certificate request.

    Arguments: req        - Certificate reqeust to use
               issuerCert - The certificate of the issuer
               issuerKey  - The private key of the issuer
               serial     - Serial number for the certificate
               notBefore  - Timestamp (relative to now) when the certificate
                            starts being valid
               notAfter   - Timestamp (relative to now) when the certificate
                            stops being valid
               digest     - Digest method to use for signing, default is md5
               isca       - The certificate is a CA

    Returns:   The signed certificate in an X509 object
    """

    cert = crypto.X509()
    cert.set_version(2)

    if extensions:
        X509Extensions = []
        for name, critical, value in extensions:
            X509Extensions.append(crypto.X509Extension(name, critical, value))

        cert.add_extensions(X509Extensions)

    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(issuerCert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(issuerKey, digest)

    return cert

def createSignedCertificate(subject, serial, extensions=[], type=TYPE_RSA, bits=2048, cipher='DES-EDE3-CBC', passphrase='', years=5, capkey='', cacert='', capassphrase=''):
    """
    Generate a Signed Certificate.

    Arguments: subject      - The subject of the request, see createCertRequest()
               type         - (optional) Key type, see createKeyPair()
               bits         - (optional) Number of bits to use in the key
               cipher       - (optional) if encrypted PEM format, the cipher to use, see dump_privatekey()
               passphrase   - (optional) if encrypted PEM format, the passphrase to use, see dump_privatekey()
               years        - (optional) Number of years to use for validity, see X509()
               capkey       - (optional) CA's private key (PEM formated string)
               cacert       - (optional) CA's certificate (PEM formated string)
               capassphrase - (optional) if CA private key is in encrypted PEM format,
                              the passphrase to use, see load_privatekey()
               
    Returns:   Two PEM formated strings containing private key and signed certificate
    """

    pkey = createKeyPair(type, bits)
    req  = createCertRequest(pkey, subject)

    if capkey and cacert:
        # Certificate will be signed by an Autority
        capkey = crypto.load_privatekey(crypto.FILETYPE_PEM,  capkey, capassphrase)
        cacert = crypto.load_certificate(crypto.FILETYPE_PEM, cacert)
    else:
        # Self signed certificate
        capkey = pkey
        cacert = req

    cert = createCertificate(req, (capkey, cacert), serial, (0, years*YEAR), extensions=extensions)

    if passphrase:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey, cipher, passphrase)
    else:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)

    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

    return (pkey, cert)

def getSubject(cert, for_win=False):

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    subj = cert.get_subject()

    subject = ''
    for attr in X509Attr:
        value = getattr(subj, attr)
        if value:
            if for_win:
                # Converting Attr to Windows Attr
                attr = X509WinAttr[attr]
            subject += '%s=%s, ' % (attr, value)

    subject = subject[:-2]

    return subject

def convertPemToDer(pkey, cert, cipher='DES-EDE3-CBC', passphrase=''):
    """
    Convert two PEM formated strings (pkey, cert) onto two DER formated strings.

    Arguments: pkey       - private key (PEM formated string)
               cert       - certificate (PEM formated string)
               cipher     - (optional) if encrypted PEM format, the cipher to use, see dump_privatekey()
               passphrase - (optional) if encrypted PEM format, the passphrase to use, see dump_privatekey()

    Returns:   Two DER formated strings containing private key and signed certificate
    """

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM,  pkey, passphrase)
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    
    if passphrase:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pkey, cipher, passphrase)
    else:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pkey)

    cert = crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)

    return (pkey, cert)

def convertDerToPem(pkey, cert, cipher='DES-EDE3-CBC', passphrase=''):
    """
    Convert two DER formated strings (pkey, cert) onto two PEM formated strings.

    Arguments: pkey       - private key (DER formated string)
               cert       - certificate (DER formated string)
               cipher     - (optional) if encrypted DER format, the cipher to use, see dump_privatekey()
               passphrase - (optional) if encrypted DER format, the passphrase to use, see dump_privatekey()

    Returns:   Two PEM formated strings containing private key and signed certificate
    """

    pkey = crypto.load_privatekey(crypto.FILETYPE_ASN1,  pkey, passphrase)
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
    
    if passphrase:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey, cipher, passphrase)
    else:
        pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)

    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

    return (pkey, cert)

def dump_pkcs12(pkey, cert, cacert='', passphrase=''):
    """

    """

    # Storing all the params to a temp file
    temp_file = '/tmp/pkcs12'

    pkcs12 = pkey + cert + cacert

    f = open(temp_file, 'w')
    f.write(pkcs12)
    f.close()
    chmod(temp_file, 0600)

    # Create pkcs12 file with openssl
    cmd = 'openssl pkcs12 -export -in %s -passout pass:"%s"' % (temp_file, passphrase)

    exitcode, pkcs12 = execute_cmd(cmd)
    remove(temp_file)
    
    if exitcode:
        return pkcs12

    return None

def newCertificate(db, ip):

    serial = db.get_last_serial_cert()
    ca     = db.get_certificate(serial=0)

    # Creating the certificate for the ip
    serial       += 1
    subject       = config['SSL_DEFAULT']
    subject['CN'] = ip
    extensions    = (('nsCertType',       False, 'client'),
                     ('keyUsage',         False, 'dataEncipherment'),
                     ('extendedKeyUsage', False, 'clientAuth,1.3.6.1.4.1.311.10.3.4.1'))
    pkey, cert = createSignedCertificate(subject, serial, extensions=extensions, bits=1024, capkey=ca['private_key'], cacert=ca['certificate'], capassphrase=config['SSL_CA_PASS'])

    # Adding it to the database
    db_cert = {}
    db_cert['serial']      = serial
    db_cert['private_key'] = pkey
    db_cert['certificate'] = cert

    return db.set_certificate(db_cert)

def getPKCS12(db, reservation_id):

    ca          = db.get_certificate(serial=0)
    reservation = db.get_reservation(reservation_id=reservation_id)
    certificate = db.get_certificate(certificate_id=reservation['certificate_id'])

    pkcs12 = dump_pkcs12(certificate['private_key'], certificate['certificate'], ca['certificate'])

    return pkcs12
    
def revokeCertificate(db, certificate_id):

    return True

def init(db):

    db.delete_certificates()

    # Creating the CA
    serial     = 0
    subject    = config['SSL_DEFAULT']
    extensions = (('basicConstraints', True,  'CA:true'),
                  ('nsCertType',       False, 'objCA,sslCA,objsign,client,server'),
                  ('keyUsage',         False, 'keyCertSign,cRLSign,nonRepudiation,keyEncipherment,dataEncipherment'),
                  ('extendedKeyUsage', False, 'clientAuth,serverAuth,1.3.6.1.4.1.311.10.3.4.1')) # 1.3.6.1.4.1.311.10.3.4.1 is for VPN

    capkey, cacert = createSignedCertificate(subject, serial, extensions=extensions, passphrase=config['SSL_CA_PASS'])

    # Adding it to the database
    db_cert = {}
    db_cert['serial']      = serial
    db_cert['private_key'] = capkey
    db_cert['certificate'] = cacert
    if not db.set_certificate(db_cert):
        return False

    # Creating the certificate for the WebServer
    serial       += 1
    subject['CN'] = config['SERVER_NAME']
    extensions    = (('nsCertType',       False, 'server'),
                     ('keyUsage',         False, 'keyEncipherment'),
                     ('extendedKeyUsage', False, 'serverAuth'))

    pkey, cert = createSignedCertificate(subject, serial, extensions=extensions, bits=1024, capkey=capkey, cacert=cacert, capassphrase=config['SSL_CA_PASS'])

    # Adding it to the database
    db_cert = {}
    db_cert['serial']      = serial
    db_cert['private_key'] = pkey
    db_cert['certificate'] = cert
    if not db.set_certificate(db_cert):
        return False

    try:
        f = open(config['MYAP_HTTPD_PKEY'], 'w')
        f.write(pkey)
        f.close()
        chmod(config['MYAP_HTTPD_PKEY'], 0600)
    
        f = open(config['MYAP_HTTPD_CERT'], 'w')
        f.write(cert)
        f.close()

    except:
        return False

    # Creating the certificate for Racoon
    serial       += 1
    subject['CN'] = 'Racoon Server'
    extensions    = (('nsCertType',       False, 'client,server'),
                     ('keyUsage',         False, 'keyEncipherment'),
                     ('extendedKeyUsage', False, 'clientAuth,serverAuth,1.3.6.1.4.1.311.10.3.4.1'))

    pkey, cert = createSignedCertificate(subject, serial, extensions=extensions, bits=1024, capkey=capkey, cacert=cacert, capassphrase=config['SSL_CA_PASS'])

    # Adding it to the database
    db_cert = {}
    db_cert['serial']      = serial
    db_cert['private_key'] = pkey
    db_cert['certificate'] = cert
    if not db.set_certificate(db_cert):
        return False

    try:
        pkey_file = join(config['SSL_TOP_DIR'], config['RACOON_PKEY'])
        cert_file = join(config['SSL_TOP_DIR'], config['RACOON_CERT'])

        f = open(pkey_file, 'w')
        f.write(pkey)
        f.close()
        chmod(pkey_file, 0600)
    
        f = open(cert_file, 'w')
        f.write(cert)
        f.close()

    except:
        return False

    return True
 
