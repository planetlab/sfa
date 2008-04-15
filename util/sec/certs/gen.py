import sys
from OpenSSL import crypto
sys.path.append('../')
sys.path.append('../..')
from sec import *

#id certificates

create_self_cert('planetlab')
create_self_cert('jp')
create_self_cert('osaka')
create_self_cert('usersoner')

planetlab_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('planetlab.cert').read())
jp_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('jp.cert').read())
osaka_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('osaka.cert').read())
usersoner_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('usersoner.cert').read())

planetlab_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open('planetlab.pkey').read())
jp_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open('jp.pkey').read())
osaka_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open('osaka.pkey').read())
usersoner_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open('usersoner.pkey').read())

#accounting certificates

planetlab_acc = create_acc(planetlab_cert, planetlab_pkey, planetlab_cert.get_pubkey(), 'planetlab', '77059b82-e826-11dc-9dc2-001ec2091968')
jp_acc = create_acc(planetlab_cert, planetlab_pkey, jp_cert.get_pubkey(), 'planetlab.jp', '3fd66a4c-d574-4aa0-9ddd-3904af595bd2')
osaka_acc = create_acc(jp_cert, jp_pkey, osaka_cert.get_pubkey(), 'planetlab.jp.osaka', '05b3c29b-0dae-4a95-b92b-0e01548f61e0')
usersoner_acc = create_acc(osaka_cert, osaka_pkey, usersoner_cert.get_pubkey(), 'planetlab.jp.osaka.usersoner', '220828220198687580431599291716859620971')

#credential certificates

planetlab_cred = create_cred(planetlab_cert, planetlab_pkey, planetlab_cert.get_pubkey(), 'Registry credentials', '(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)#0:reg:planetlab')
jp_cred = create_cred(planetlab_cert, planetlab_pkey, jp_cert.get_pubkey(), 'Registry credentials', '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)#0:reg:planetlab#1:reg:planetlab.jp')
osaka_cred = create_cred(jp_cert, jp_pkey, osaka_cert.get_pubkey(), 'Registry credentials', '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)#0:reg:planetlab.jp#1:reg:planetlab.jp.osaka')
usersoner_cred = create_cred(osaka_cert, osaka_pkey, usersoner_cert.get_pubkey(), 'Registry credentials', '(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)#0:reg:planetlab.jp.osaka')

#acc and cred files

ac1 = crypto.dump_certificate(crypto.FILETYPE_PEM, planetlab_acc)
ac2 = crypto.dump_certificate(crypto.FILETYPE_PEM, jp_acc)
ac3 = crypto.dump_certificate(crypto.FILETYPE_PEM, osaka_acc)
ac4 = crypto.dump_certificate(crypto.FILETYPE_PEM, usersoner_acc)
#open('planetlab_acc_file', 'w').write(ac1)
#open('jp_acc_file', 'w').write(ac2+ac1)
open('osaka_acc_file', 'w').write(ac3+ac2+ac1)
open('usersoner_acc_file', 'w').write(ac4+ac3+ac2+ac1)

cred1 = crypto.dump_certificate(crypto.FILETYPE_PEM, planetlab_cred)
cred2 = crypto.dump_certificate(crypto.FILETYPE_PEM, jp_cred)
cred3 = crypto.dump_certificate(crypto.FILETYPE_PEM, osaka_cred)
cred4 = crypto.dump_certificate(crypto.FILETYPE_PEM, usersoner_cred)
#open('planetlab_cred_file', 'w').write(cred1)
#open('jp_cred_file', 'w').write(cred2+cred1)
open('osaka_cred_file', 'w').write(cred3+cred2+cred1)
open('usersoner_cred_file', 'w').write(cred4+cred3+cred2+cred1)

