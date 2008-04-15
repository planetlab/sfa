#
# certgen.py
#
# Copyright (C) Martin Sjogren and AB Strakt 2001, All rights reserved
#
# $Id: certgen.py,v 1.2 2004/07/22 12:01:25 martin Exp $
#
"""
Certificate generation and validation module.
"""

from OpenSSL import crypto
import time, calendar, datetime

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA

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

def createCertRequest(pkey, name, digest="md5"):
    """
    Create a certificate request.

    Arguments: pkey   - The key to associate with the request
               digest - Digestion method to use for signing, default is md5
               **name - The name of the subject of the request, possible
                        arguments are:
                          C     - Country name
                          ST    - State or province name
                          L     - Locality name
                          O     - Organization name
                          OU    - Organizational unit name
                          CN    - Common name
                          emailAddress - E-mail address
    Returns:   The certificate request in an X509Req object
    """
    req = crypto.X509Req()
    subj = req.get_subject()
    for (key,value) in name.items():
        setattr(subj, key, value)
    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req

def createCertificate(req, (issuerCert, issuerKey), serial, (notBefore, notAfter), extensions=[], digest="md5"):
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
    Returns:   The signed certificate in an X509 object
    """
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(issuerCert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    if extensions:
        extList = []
        for name, critical, value in extensions:
            ext = crypto.X509Extension (name, critical, value)
            extList.append(ext)
        cert.add_extensions(extList)
    cert.sign(issuerKey, digest)
    return cert


#checks if a certificate is valid in terms of validity periods    
def check_valid(usercert):
    """
    Method that ensures the issuer cert has
    valid, not_before and not_after fields
    """
    valid = True
    before_time = usercert.get_not_before()
    after_time = usercert.get_not_after()
    before_tuple = time.strptime(str(before_time), "%b %d %H:%M:%S %Y %Z")
    after_tuple = time.strptime(str(after_time), "%b %d %H:%M:%S %Y %Z")
    starts =  datetime.timedelta(seconds=calendar.timegm(before_tuple))
    expires = datetime.timedelta(seconds=calendar.timegm(after_tuple))
    now = datetime.timedelta(seconds=time.time())
    time_delta = expires - now
    
    #cert has expired
    if time_delta.days < 0:
        valid = False
    #cert is not yet valid
    time_delta = now - starts
    if time_delta.days < 0:   
        valid = False

    return valid
