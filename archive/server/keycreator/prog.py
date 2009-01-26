import sys
from OpenSSL import crypto
from M2Crypto import X509
sys.path.append('../../util/sec')
sys.path.append('../../util')
from sec import *
from util import *
from db import *

SUFFIX1 = '_srr'
SUFFIX2 = '_crr'

#get input from user
hrn = raw_input('Enter the hrn of the object: ')

#generate certificate and the private key
name = get_leaf(hrn)
create_self_cert(name)

#extract the public key from the certificate and input to the database
cert = X509.load_cert(name+'.cert')
pubkey_pem = cert.get_pubkey().as_pem(cipher=None)

cnx = get_plDB_conn()
tablename = obtain_authority(hrn).replace('.','$')
t1 = tablename+SUFFIX1
t2 = tablename+SUFFIX2

querystr = "SELECT * FROM "+t1+" WHERE hrn='"+name+"';"
res = cnx.query(querystr)
if res:
        querystr = "UPDATE "+t1+" SET pubkey = '"+pubkey_pem+"' WHERE hrn = '"+name+"';"
        cnx.query(querystr)
else:
    querystr = "SELECT * FROM "+t2+" WHERE hrn='"+name+"';"
    res = cnx.query(querystr)
    if res:
        querystr = "UPDATE "+t2+" SET pubkey = '"+pubkey_pem+"' WHERE hrn = '"+name+"';"
        cnx.query(querystr)
    else:
        print 'The record with name:'+hrn+"' does not exist in the system.\n"
        os.exit(1)

print "Public key is successfully added to '"+hrn+"' record.\nThe certificate and key are generated.\n"




