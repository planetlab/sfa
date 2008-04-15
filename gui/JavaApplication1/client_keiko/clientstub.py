#!/usr/bin/python

import os, sys
from M2Crypto import SSL
sys.path.append('/home/soners/work/geni/rpc/util')
sys.path.append('/home/soners/work/geni/rpc/util/sec')
from sec import *

SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 8002
AUTH_HOST = '127.0.0.1' 
AUTH_PORT = 8002

renew_res1 = 0
renew_res2 = 0

def verify_callback(preverify_ok, ctx):
    return 1

class GENIClient():
    def __init__(self, hrn, type, id_file, id_key_file, acc_file, cred_file):
        self.hrn = hrn
        self.type = type
        #check if the certificate and the private key exists, terminate if not
        if not os.path.exists(id_file) or not os.path.exists(id_key_file) :
            print 'The certificate or the private key does not exist.\n'
            os.exit(1)
        #check the acc and cred files
        if not os.path.exists(acc_file) or not is_valid_chain(acc_file):
            open(acc_file, 'w').write('ANONYM')
        if not os.path.exists(cred_file) or not is_valid_chain(cred_file):
            open(cred_file, 'w').write('NO_CRED')
        #initialize the security system
        self.sec = Sec('client',  id_file, id_key_file, acc_file, cred_file)
        #ssl parameters
        self.ctx = SSL.Context()
        self.ctx.load_cert(self.sec.id_file,self.sec.id_key_file)
        self.ctx.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, depth=9, callback=verify_callback)    
    
    def connect(self, host, port):    
        #if the acc and cred needs renewal then do call to authority
        if self.type == 'user' or self.type == 'slice' or self.type == 'SA': 
            reg_type = 'slice'
        else:
            reg_type ='component'
        renew_res1 = renew_cert('accounting', '.', reg_type, self.hrn, None, None, (AUTH_HOST, AUTH_PORT), self.sec)
        renew_res2 = renew_cert('credential', '.', reg_type, self.hrn, None, None, (AUTH_HOST, AUTH_PORT), self.sec)
        if renew_res1 == None:
            print "There is no certificate in the directory "+"./\n"
            os.exit(0)
        #connect to server
        server = SSL.Connection(self.ctx)
        server.connect((host,port))
        peer = self.sec.auth_protocol(server)
        if peer:
            return server
        else:
            return None
        
def main():
    try:
        #read the input file
        fp = open('tmp_input.txt', 'r')
        user_data = fp.readline()
        call_data = fp.readline()
        print 'Read file.\n'
        
        #client related info
        HRN = user_data.split(' ')[0]
        TYPE = user_data.split(' ')[1].split('\n')[0]
        name = get_leaf(HRN)
        ID_FILE = name+'.cert'
        ID_KEY_FILE = name+'.pkey'
        ACC_FILE = 'acc_file'
        CRED_FILE = 'cred_file'
        my_client = GENIClient(HRN, TYPE, ID_FILE, ID_KEY_FILE, ACC_FILE, CRED_FILE)
        print 'Constructed client.\n'
        
        #operation call
        message = eval(call_data)
        server = my_client.connect(SERVER_HOST, SERVER_PORT)
        if server:
            server.write(str(message))
            result = server.read() 
            server.close()
            print 'Performed the call.\n'
        else:
            result = "Error in client data structures.\n"
            
        if renew_res2 == 1:
            result = "Cred renewed. "+result
        if renew_res1 == 1:
            result = "Acc renewed. "+result
        #write result to output file
        open('tmp_output.txt','w').write(result)
        print 'Written to file.\n'
    except:
        #write result to output file
        open('tmp_output.txt','w').write("An error occurred in client stub.\n")
        print 'Exception occurred.\n'
        
if __name__=="__main__":
    print 'Client started.\n'
    main()
