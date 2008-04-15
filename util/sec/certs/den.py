import sys
from OpenSSL import crypto
from M2Crypto import X509
sys.path.append('../')
sys.path.append('../..')
from sec import *

 

##osaka2 = X509.load_cert_string(crypto.dump_certificate(crypto.FILETYPE_PEM, osaka_acc))
##usersoner2 = X509.load_cert_string(crypto.dump_certificate(crypto.FILETYPE_PEM, usersoner_acc))
##
##t1 = osaka2.as_text()
##t2 = usersoner2.as_text()
##
##res = usersoner2.verify(osaka2.get_pubkey()) 
##
##print res

#pl_pem = X509.load_cert('usersoner.cert')
#pkey = pl_pem.get_pubkey().as_pem(cipher=None)

#from pg import DB

#dbname = 'plDB'
#address = 'localhost'
#port = 5433
#user = 'postgres'
#password = '111'
#cnx = DB(dbname, address, port=port, user=user, passwd=password)
#cnx.query("UPDATE planetlab$jp$osaka_sr SET pubkey = '"+pkey+"' WHERE hrn = 'usersoner'")

#print pkey


planetlab_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('planetlab.cert').read())
planetlab_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open('planetlab.pkey').read())
planetlab_acc = create_acc(planetlab_cert, planetlab_pkey, planetlab_cert.get_pubkey(), 'planetlab', '28698598650165084658569185050284587399', 3)
ac1 = crypto.dump_certificate(crypto.FILETYPE_PEM, planetlab_acc)
open('planetlab_acc_file', 'w').write(ac1)

##
##res = c1_pem2.verify(c3_pem2.get_pubkey()) 
