#!/usr/bin/python
from M2Crypto import X509
import sys

id_file = ""
try:
    if len(sys.argv)>1:
        id_file = sys.argv[len(sys.argv)-1]
    else:
        print 'File '+id_file+' does not exist.\n'
        sys.exit(0)
    pubkey = X509.load_cert(id_file).get_pubkey().as_pem(cipher=None)
    print pubkey
    
    print "Character map:\n"
    prev = ''
    cur = ''
    for ch in pubkey:
        prev = cur
        cur = ch
        if cur == '\n':
            1==1
        print ch,
except:
    print "Error in input file.\n"
