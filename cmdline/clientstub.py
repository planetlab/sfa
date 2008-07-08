#!/usr/bin/python

import os, sys
from M2Crypto import SSL
from sec import *
from cliexcep import *
import report

# XXX SMBAKER: changed MAX_RESULT from 3000B to 32KB
MAX_RESULT = 32768

def verify_callback(preverify_ok, ctx):
    return 1

class GENIClient():
    def __init__(self, hrn, type, id_file, id_key_file, acc_file, cred_file):
        self.hrn = hrn
        self.type = type

        #check if the certificate and the private key exists, terminate if not
        if not os.path.exists(id_file):
            report.error("Certificate file " + id_file + " does not exist")
            raise NonexistingFile(id_file)

        if not os.path.exists(id_key_file):
            report.error("Key file: " + id_key_file + " does not exist")
            raise NonexistingFile(key_file)

        report.trace("cert: " + id_file + ", key_file: " + id_key_file)

        #check the acc and cred files
        if not os.path.exists(acc_file) or not is_valid_chain(acc_file):
            report.trace("replacing acc_file: " + acc_file + " with anonymous acc")
            open(acc_file, 'w').write('ANONYM')

        if not os.path.exists(cred_file) or not is_valid_chain(cred_file):
            report.trace("replacing cred_file: " + cred_file + " with no_cred")
            open(cred_file, 'w').write('NO_CRED')

        #initialize the security system
        self.sec = Sec('client',  id_file, id_key_file, acc_file, cred_file)
        #ssl parameters
        self.ctx = SSL.Context()
        self.ctx.load_cert(self.sec.id_file, self.sec.id_key_file)
        self.ctx.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, depth=9, callback=verify_callback)

    def connect(self, host, port):
        #if the acc and cred needs renewal then do call to authority
        if self.type == 'user' or self.type == 'slice' or self.type == 'SA':
            reg_type = 'slice'
        else:
            reg_type ='component'

        auth_host = host
        auth_port = port

        report.trace("renewing accounting")
        renew_res1 = renew_cert('accounting', '.', reg_type, self.hrn, None, None, (auth_host, auth_port), self.sec)
        if renew_res1 == None:
            report.error("There is no certificate in the directory .")
            raise NoCertInDirectory(".")

        report.trace("renewing credential")
        renew_res2 = renew_cert('credential', '.', reg_type, self.hrn, None, None, (auth_host, auth_port), self.sec)
        # XXX check result of renew_res2 ?

        #connect to server
        server = SSL.Connection(self.ctx)

        report.trace("connecting")
        server.connect((host,port))

        report.trace("authenticating")
        peer = self.sec.auth_protocol(server)
        if peer:
            report.trace("Authentication successful")
            return server
        else:
            report.error("Authentication failed")
            raise AuthenticationFailed()

def toFileFormat(res_str):
    out_str = ""
    try:
        res_dict = eval(res_str)
        if res_dict['geni'].has_key('pubkey'): # in public key, replace '\n' with ' '
            pubkey = res_dict['geni']['pubkey']
            pubkey = pubkey.split('-----BEGIN RSA PRIVATE KEY-----')[1].split('-----END RSA PRIVATE KEY-----')[0].replace('\n',' ')
            pubkey = '-----BEGIN RSA PRIVATE KEY-----'+pubkey+'-----END RSA PRIVATE KEY-----'
            res_dict['geni']['pubkey'] = pubkey

        if res_dict.has_key('message'):
            out_str = res_dict['message']+'\n'
        else:
            out_str = "{'geni':{\n"
            for key in res_dict['geni']:
                val = ''
                if res_dict['geni'][key] == None:
                    val = ''
                elif isinstance(res_dict['geni'][key], str):
                    val = res_dict['geni'][key]
                else:
                    val = str(res_dict['geni'][key])
                out_str = out_str+"'"+key+"':"+val+"\n"
            out_str = out_str + "}\n"
            out_str = out_str + "'pl':{\n"
            for key in res_dict['pl']:
                val = ''
                if res_dict['pl'][key] == None:
                    val = ''
                if isinstance(res_dict['pl'][key], str):
                    val = res_dict['pl'][key]
                else:
                    val = str(res_dict['pl'][key])
                out_str = out_str+"'"+key+"':"+val+"\n"
            out_str = out_str + "}}"
    except:
        out_str = res_str
    return out_str

def evaluate(call_data):
    call_data = eval(call_data)
    #adjust the key format to obey server's storage format
    if call_data['g_params'].has_key('pubkey'): #replace the ' ' with '\n'
        pubkey = call_data['g_params']['pubkey']
        pubkey = pubkey.split('-----BEGIN RSA PRIVATE KEY-----')[1].split('-----END RSA PRIVATE KEY-----')[0].replace(' ','\n')
        pubkey = '-----BEGIN RSA PRIVATE KEY-----'+pubkey+'-----END RSA PRIVATE KEY-----'
        call_data['g_params']['pubkey'] = pubkey
    return call_data

def oldmain():
    try:
        #read the input file
        fp = open('tmp_input.txt', 'r')
        user_data = fp.readline()
        call_data = fp.read()
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
        message = evaluate(call_data)
        server = my_client.connect(SERVER_HOST, SERVER_PORT)
        if server:
            server.write(str(message))
            result = toFileFormat(server.read(MAX_RESULT))
            server.close()
            print 'Performed the call.\n'
        else:
            result = "Error in client data structures.\n"

        #write result to output file
        open('tmp_output.txt','w').write(result)
        print 'Written to file.\n'
    except "XXX": # XXX smbaker
        #write result to output file
        open('tmp_output.txt','w').write("An error occurred in client stub.\n")
        print 'Exception occurred.\n'

#if __name__=="__main__":
#    print 'Client started.\n'
#    os.system("echo foo > foo.txt")
#    os.system("mv tmp_input.3 tmp_input.4")
#    os.system("mv tmp_input.2 tmp_input.3")
#    os.system("mv tmp_input.1 tmp_input.2")
#    os.system("cp tmp_input.txt tmp_input.1")
#    main()
