import os, sys
from OpenSSL import crypto
from M2Crypto import X509
from M2Crypto import SSL
sys.path.append('../')
from certgen import *
from util import *
from db import *
from tree import *

CRED_GRANT_TIME = 3600000 #in seconds
ACC_GRANT_TIME = 10000000
TOP_LEVEL_CERTS_DIR = "trusted_certs"
MAX_CERT_SIZE = 1024
MAX_CERT_CHAIN = 9

creds= ["","","","","","","","","","","","","","","","","","","","","","","","",""]
creds[0] = "register"
creds[1] = "remove"
creds[2] = "remove_self"
creds[3] = "update"
creds[4] = "update_self"
creds[5] = "lookup"
creds[6] = "lookup_self"
creds[7] = "list"
creds[8] = "getCredential"
creds[9] = "getAccounting"
creds[10] = "getTicket"      # = embed privilege in the docs
creds[11] = "splitTicket"
creds[12] = "redeemTicket"
creds[13] = "stop"
creds[14] = "start"
creds[15] = "delete"
creds[16] = "listSlices"
creds[17] = "getStatus"
creds[18] = "getSlice"
creds[19] = "refresh"
creds[20] = "delegate"
creds[21] = "instantiate"
creds[22] = "bind"
creds[23] = "control"

class PeerInfo :
    def __init__(self):
        self.cert = None
        self.acc = Accounting()   #accounting information
        self.cred = Credential()  #credential information

#info_certs looks like: [{'hrn':None, 'uuid':0}]
class Accounting:
    def __init__(self):
        self.info_certs = []
        self.cert_chain = []
    def get_hrn(self):
        return self.info_certs[0]['hrn']
    def get_uuid(self):
        return self.info_certs[0]['uuid']

#info_certs looks like: [{'operation_set':None, 'on_interfaces':None}]
#operation_set looks like: [0:['register','update','update_self',..], 1:['getTicket', 'splitTicket',..],..]
#on_interfaces looks like: [{'lbl':0, 'name':'planetlab.jp.jaist', 'type':'registry'},..{}]
class Credential: 
    def __init__(self):
        self.info_certs = [] #list of operations and list of sites on which operations can be performed
        self.cert_chain = []
    def get_cred(self):
        return self.info_certs[0]
        
#type: 'accounting' or 'credential' 
#folder: directory of that the certificate should reside
#reg_type: 'slice' or 'component'
#hrn: name of the object to get certificates for
#server: the server instance to do operations calls with in the internal tree
#internal_tree: tree for internal cert renewals
#auth_addr: authority to ask for certificates
#sec: security module to perform auth. protocol with the remote peer
#return 0: no renewal done, 1: renewal done, None: error
def renew_cert(type, folder, reg_type, hrn, server, internal_tree, auth_addr, sec):
    #check if necessary to renew
    if type == 'accounting':
        fname = folder+'/acc_file'
    else:
        fname = folder+'/cred_file'
    if os.path.exists(fname) and is_valid_chain(fname):
        return 0
    else:
        parent_hrn = obtain_authority(hrn)
        hrn_suffix = get_leaf(hrn)
        id_file = folder+'/'+hrn_suffix+'.cert'
        #check the id file
        if not os.path.exists(folder) or not os.path.exists(id_file):
            print 'Id file for '+hrn+' does not exist.\n'
            return None
        #decide if remote call
        remote = True
        if internal_tree:
            dbinfo = determine_dbinfo(parent_hrn, internal_tree)
            if dbinfo:
                remote = False
        if not remote:
            if type == 'accounting':
                #obtain the accounting from parent, write to file
                g = {"hrn":""}
                g["hrn"] = parent_hrn
                g['registry'] = reg_type
                g["account_name"] = hrn 
                p = {}
                record = {'g_params':g, 'p_params':p}
                dbinfo = determine_dbinfo(parent_hrn, internal_tree)
                parentkeyinfo = internal_tree.determine_keyinfo(parent_hrn, server, type)
                open(fname, 'w').write(server.getAccounting(record, dbinfo, parentkeyinfo, X509.load_cert(id_file)))
            else:
                #obtain the credential from parent, write to file
                g = {"hrn":""}
                g["hrn"] = parent_hrn
                if reg_type == 'slice':
                    g['cred_name'] = 'registry:slc'
                else:
                    g['cred_name'] = 'registry:comp'
                p = {}
                record = {'g_params':g, 'p_params':p}
                dbinfo = determine_dbinfo(parent_hrn, internal_tree)
                id = crypto.load_certificate(crypto.FILETYPE_PEM, open(id_file).read())
                peerinfo = [hrn, id]
                parentkeyinfo = internal_tree.determine_keyinfo(parent_hrn, server, type)
                open(fname, 'w').write(server.getCredential(record, dbinfo, parentkeyinfo, peerinfo))
        else: #if not local call
            if obtain_authority(hrn) == '':  #we are at the root
                id_key_file = folder+'/'+hrn_suffix+'.pkey'
                id_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(id_file).read())
                id_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(id_key_file).read())
                peer_cred_str = open(fname).read()
                c_pem = X509.load_cert_string("-----BEGIN CERTIFICATE-----"+peer_cred_str.split("-----BEGIN CERTIFICATE-----")[1])
                if type == 'accounting':
                    cert_uuid = c_pem.get_ext("subjectAltName").get_value().split('http://')[1].split('#')[2].split('uuid:')[1]
                    acc = create_acc(id_cert, id_pkey, id_cert.get_pubkey(), hrn, cert_uuid)
                    open(fname, 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, acc))
                else:
                    rights = c_pem.get_ext("subjectAltName").get_value().split('http://')[1].split('credential_set:')[1]
                    cred = create_cred(id_cert, id_pkey, id_cert.get_pubkey(), 'Registry credentials', rights)
                    open(fname, 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cred))
            else:
                operation = ''                    
                g = {"hrn":obtain_authority(hrn)}
                if type == 'accounting':
                    operation = "getAccounting";
                    #geni parameters
                    g['registry'] = reg_type
                    g["account_name"] = hrn
                else:
                    operation = "getCredential"
                    #geni parameters
                    if reg_type == 'slice':
                        g['cred_name'] = 'registry:slc'
                    else:
                        g['cred_name'] = 'registry:comp'
                p = {}
                message = {'opname':operation, 'g_params':g, 'p_params':p}
                #connect to authority
                server = SSL.Connection(sec.ctx)
                server.connect(auth_addr)
                peer = sec.auth_protocol(server)
                #do the query and get the result
                server.write(str(message))
                result = server.read(MAX_CERT_SIZE*MAX_CERT_CHAIN)
                open(fname, 'w').write(result)
        return 1
        
#obtains a data structure for credentials out of a given credential string
#return info_cert: {'operation_set':{'register','remove',..}, 'on_interfaces':{{'lbl':'0', 'type':'registry:slc','name':'planetlab.jp'}, ..}}
def get_cred_info(credstr):
    info_cert = {'operation_set':{}, 'on_interfaces':{}}
    set = credstr.split('#')[1].split('credential_set:')[1]
    set_arr = set.split(')')
    for item in set_arr[0:len(set_arr)-1]:
        item = item.split('(')[1].split('-')
        if info_cert['operation_set'].has_key(item[1]):
            info_cert['operation_set'][item[1]].append(creds[int(item[0])])
        else:
            info_cert['operation_set'][item[1]] = [creds[int(item[0])]]
    interface_list = []
    arr = credstr.split('#')
    intlist = arr[2:len(arr)]
    for interface in intlist:
        iarr = interface.split(':')
        newint = {'lbl':iarr[0]}
        if iarr[1] == 'reg':
            if iarr[2] == 'slc':
                newint['type'] ='registry:slc'
            else:
                newint['type'] ='registry:comp'
            newint['name'] = iarr[3]
        elif iarr[1] == 'comp':
            newint['type'] ='component'
            newint['name'] = iarr[2]
        interface_list.append(newint)
    info_cert['on_interfaces'] = interface_list
    return info_cert

#given two credential statements, check if the first one can delegate the second one
#example: "'register' right on 'planetlab.jp' registry interface" is able to delegate a right called "'register' right on 'planetlab.jp.jaist' registry interface" 
def check_delegation(info_cert1, info_cert2):
    passed = False
    for interface in info_cert1['on_interfaces']:
        is_reg = interface['type'] == 'registry:slc' or interface['type'] == 'registry:comp'
        if is_reg and 'register' in info_cert1['operation_set'][interface['lbl']]:
            found = True
            for child_int in info_cert2['on_interfaces']:
                if child_int['type'] == interface['type'] and not check_authority(child_int['name'],interface['name']):
                    found = False
            if found:
                passed = True
                break
    return passed

    """
Create a credential certificate given the parameters: 
    'authcert': the authority certificate
    'authkey': the authority key
    'pubkey': the public key belonging to the object to which the credential will be granted
    'cname': the name of the credential being generated. It should be 'registry credentials' or a silce name like 'planetlab.jp.slice1'
    'rights':  - the sequence representing the set of operations/rights on specific interfaces
                                            ex: (2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-0)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)#0:reg:planetlab.jp#1:reg:planetlab.jp.jaist
    'time': time in seconds how long the life of credential is
"""
def create_cred(authcert, authkey, pubkey, cname, rights, time=CRED_GRANT_TIME):
    #calculate the credset
    if rights == "slice":
        rights = "(10-1)(11-1)(12-1)(13-1)(14-1)(15-1)(16-1)(17-1)(18-1)(23-1)"
    elif rights == "SA":
        rights = "(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)(16-1)(17-1)(18-1)(19-1)"
    elif rights == "MA":
        rights = "(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)(16-1)(17-1)(18-1)"
    else:
        # check if the rights is in correct format ######################
        rights = rights
        #create the CSR for the credential certificate
        key = createKeyPair(TYPE_RSA, 1024)
        certReq = createCertRequest(key, {"CN" : cname})
        certReq.set_pubkey(pubkey)
        #create the credential certificate, return
        content = "#credential_set:"+rights 
        ext = ("subjectAltName", 1, "URI:http://"+content)
        exts = [ext]
        cert = createCertificate(certReq, (authcert, authkey), 0, (0, int(time)), exts)
        return cert

"""
Create an accountability certificate given the parameters: 
    'authc': the name of the authority certificate file
    'authk': the name of the authority key file
    'pubkey': the name of the GID file belonging to the object to which the accountability will be assigned
    'name': the name of the object, which is the accountability information itself
    'uuid': the uuid of the object
    'time': the date and time when the life of accounting information
"""
def create_acc(authcert, authkey, pubkey, name, uuid, time=ACC_GRANT_TIME): 
    #create the CSR for the credential certificate
    key = createKeyPair(TYPE_RSA, 1024)
    certReq = createCertRequest(key, {"CN" : "GENI Accounting"})
    certReq.set_pubkey(pubkey)
    #create the accountability certificate, write into file
    content = "#hrn:"+name+"#uuid:"+uuid
    ext = ("subjectAltName", 1, "URI:http://"+content)
    exts = [ext]
    cert = createCertificate(certReq, (authcert, authkey), 0, (0, int(time)), exts)
    return cert
    
"""
Create self signed certificate and private key.
"""
def create_self_cert(name):
    key = createKeyPair(TYPE_RSA, 1024)
    certReq = createCertRequest(key, {"CN":name})
    cert = createCertificate(certReq, (certReq, key), 0, (0, 60*60*24*365*5)) # five years
    open(name+'.pkey', 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    open(name+'.cert', 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

def verify_callback(preverify_ok, ctx):
    return 1
    
class Sec: 
    def __init__(self, mode, id_file, id_key_file, acc_file, cred_file):
        self.top_level_certs = []
        self.mode = mode
        file_list = os.listdir(TOP_LEVEL_CERTS_DIR)
        for auth_file in file_list:
            # XXX SMBAKER: fix .svn directory
            if os.path.isfile(os.path.join(TOP_LEVEL_CERTS_DIR, auth_file)):
                self.top_level_certs.append(X509.load_cert(TOP_LEVEL_CERTS_DIR+"/"+auth_file))

        self.id_file = id_file
        self.id_key_file = id_key_file
        self.my_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(id_file).read())
        self.my_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(id_key_file).read())
        self.acc_file = acc_file
        self.cred_file = cred_file
        #ssl parameters
        self.ctx = SSL.Context()
        self.ctx.load_cert(self.id_file,self.id_key_file)
        self.ctx.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, depth=9, callback=verify_callback)

    #   - exchange the accounting chains, store peer's accounting in peer.acc
    #   - check TTLs in certificates
    #   - check validity of the chain, but do not check top level's trustedness
    #return 1: means there is a structural error in the chain
    #return 2: one of the TTLs in the chain not valid
    #return 3: public keys do not form a valid chain
    def exchange_accounting(self, conn, peer):
        peer_acc_str=None
        if self.mode == 'server':
            #receive acc chain
            peer_acc_str = conn.read(MAX_CERT_SIZE*MAX_CERT_CHAIN)
            #send the acc chain
            acc_str = open(self.acc_file).read()  #read the certificate chain from file
            conn.write(acc_str) 
        elif self.mode == 'client':
            #send the acc chain
            acc_str = open(self.acc_file).read()  #read the certificate chain from file
            conn.write(acc_str)
            #receive acc chain
            peer_acc_str = conn.read(MAX_CERT_SIZE*MAX_CERT_CHAIN) 
            
        #construct peer_acc data structure
        peer_acc = peer.acc
        if peer_acc_str[0:27] != "-----BEGIN CERTIFICATE-----":
            peer_acc.info_certs = "anonymous"
        else:
            try: 
                #divide the received chain into certificates
                arr = peer_acc_str.split("-----BEGIN CERTIFICATE-----")
                arr = arr[1:len(arr)]
                for i in range(len(arr)):
                    arr[i] = "-----BEGIN CERTIFICATE-----"+arr[i]
                for c_str in arr:
                    c_pem = X509.load_cert_string(c_str)
                    hrn = c_pem.get_ext("subjectAltName").get_value().split('http://')[1].split('#')[1].split('hrn:')[1]
                    uuid = c_pem.get_ext("subjectAltName").get_value().split('http://')[1].split('#')[2].split('uuid:')[1]
                    peer_acc.info_certs.append({'hrn':hrn, 'uuid':uuid})
                    peer_acc.cert_chain.append(c_pem)
            except: 
                print "No valid chain received.\n"
                return 1
            #if structure is ok, go on with other checks
            ttl_ok = True
            chain_ok = True
            #check ttl for the first certificate in the chain:
            if not (check_valid(peer_acc.cert_chain[0])):
                ttl_ok = False
            prevCert = None
            curCert = None
            for i in range(1, len(peer_acc.cert_chain)):
                prevCert = peer_acc.cert_chain[i-1] 
                curCert = peer_acc.cert_chain[i] 
                #check ttl
                if not check_valid(curCert):
                    ttl_ok = False
                #chain validity checks
                if not prevCert.verify(curCert.get_pubkey()) :
                    chain_ok = False
            if ttl_ok == False:
                return 2
            elif chain_ok == False:
                return 3
        return 0

    #   - check the pubkey of first certificate if it matches the peer public key
    #   - check the name hierarchy
    #   - check the top level authority's trustedness
    # return 0: accounting verified
    # return 1: pubkey does not match peer pubkey
    # return 2: name hierarch does not imply hrn
    # return 3: top level authority is unknown
    # return 4: unidentified error
    def verify_accounting(self, peer):
        pubkey_ok = True
        hierarchy_ok = True
        trusted_auth = True
        
        if peer.acc.info_certs == 'anonymous':
            return 0
        try:
            #check the pubkey of the peer
            if peer.acc.cert_chain[0].get_pubkey().as_pem(cipher=None) != peer.cert.get_pubkey().as_pem(cipher=None):
                    pubkey_ok = False
            else:
                #check the name hierarchy
                for i in range(len(peer.acc.info_certs)-1):
                    if check_authority(peer.acc.info_certs[i]['hrn'], peer.acc.info_certs[i+1]['hrn']) == False:
                        hierarchy_ok = False
                            
                #check if the certificate ends with a sign of a trusted top level authority
                if hierarchy_ok:
                    found = False
                    last_cert_pubkey_pem = peer.acc.cert_chain[len(peer.acc.cert_chain)-1].get_pubkey().as_pem(cipher=None)
                    for cert in self.top_level_certs:
                        auth_pubkey_pem = cert.get_pubkey().as_pem(cipher=None)
                        if last_cert_pubkey_pem == auth_pubkey_pem:
                            found = True 
                            break
                    if not found:
                        trusted_auth = False
                        
            if pubkey_ok == False:
                return 1
            elif hierarchy_ok == False:
                return 2
            elif trusted_auth == False:
                return 3
            return 0
        except Exception, e:
            print "Exception in verify_accounting:", e
            return 4
     
    #   - exchange the credential chains, store peer's credential in peer.cred
    #   - check TTLs in certificates
    #   - check validity of the chain, but do not check top level's trustedness
    #return 1: means there is a structural error in the chain
    #return 2: one of the TTLs in the chain not valid
    #return 3: public keys do not form a valid chain
    def exchange_credential(self, conn, peer):
        peer_cred_str = None
        if self.mode == 'server':
            #receive cred chain
            peer_cred_str = conn.read(MAX_CERT_SIZE*MAX_CERT_CHAIN)
            #send the cred chain
            cred_str = open(self.cred_file).read()  #read the certificate chain from file
            conn.write(cred_str)
        elif self.mode == 'client':
            #send the cred chain
            cred_str = open(self.cred_file).read()  #read the certificate chain from file
            conn.write(cred_str)
            #receive cred chain
            peer_cred_str = conn.read(MAX_CERT_SIZE*MAX_CERT_CHAIN)
            
        #construct peer_cred data structure
        peer_cred = peer.cred
        if peer_cred_str[0:27] != "-----BEGIN CERTIFICATE-----":
            peer_cred.info_certs = "no_credential"
        else:
            try:
                #divide the received chain into certificates
                arr = peer_cred_str.split("-----BEGIN CERTIFICATE-----")
                arr = arr[1:len(arr)]
                for i in range(len(arr)):
                    arr[i] = "-----BEGIN CERTIFICATE-----"+arr[i]
                for c_str in arr:
                    c_pem = X509.load_cert_string(c_str)
                    credstr = c_pem.get_ext("subjectAltName").get_value().split('http://')[1]
                    peer_cred.info_certs.append(get_cred_info(credstr))
                    peer_cred.cert_chain.append(c_pem)
            except Exception, e:
                print "Exception in exchange_credential:", e
                print "No valid chain received.\n"
                return 1
            #if structure is ok, go on with other checks
            ttl_ok = True
            chain_ok = True
            #check ttl for the first certificate in the chain:
            if not (check_valid(peer_cred.cert_chain[0])):
                ttl_ok = False
            prevCert = None
            curCert = None
            for i in range(1, len(peer_cred.cert_chain)):
                prevCert = peer_cred.cert_chain[i-1] 
                curCert = peer_cred.cert_chain[i] 
                #check ttl
                if not check_valid(curCert):
                    ttl_ok = False
                #chain validity check
                if not prevCert.verify(curCert.get_pubkey()) :
                    chain_ok = False
            if ttl_ok == False:
                return 2
            elif chain_ok == False:
                return 3
        return 0
        
    #   - check the pubkey of first certificate if it matches the peer public key
    #   - check the delegation hierarchy: the delegated rights must be granted by an authority of the entity
    #   - check the top level authority's trustedness
    # return 0: credential verified
    # return 1: pubkey does not match peer pubkey
    # return 2: delegation hierarchy is invalid
    # return 3: top level authority is unknown
    # return 4: unidentified error
    def verify_credential(self, peer):
        pubkey_ok = True
        hierarchy_ok = True
        trusted_auth = True
        
        if peer.cred.info_certs == 'no_credential':
            return 0
        try:
            #check the pubkey of the peer
            if peer.cred.cert_chain[0].get_pubkey().as_pem(cipher=None) != peer.cert.get_pubkey().as_pem(cipher=None):
                    pubkey_ok = False
            else:
                #check the delegation hierarchy
                for i in range(len(peer.cred.info_certs)-1):
                    if not check_delegation(peer.cred.info_certs[i+1], peer.cred.info_certs[i]) :
                        hierarchy_ok = False
                            
                #check if the certificate ends with a sign of a trusted top level authority
                if hierarchy_ok:
                    found = False
                    last_cert_pubkey_pem = peer.cred.cert_chain[len(peer.cred.cert_chain)-1].get_pubkey().as_pem(cipher=None)
                    for cert in self.top_level_certs:
                        auth_pubkey_pem = cert.get_pubkey().as_pem(cipher=None)
                        if last_cert_pubkey_pem == auth_pubkey_pem:
                            found = True 
                            break
                    if not found:
                        trusted_auth = False
                        
            if pubkey_ok == False:
                return 1
            elif hierarchy_ok == False:
                return 2
            elif trusted_auth == False:
                return 3
            return 0
        except:
            return 4

    def check_authorization(self, acc, cred, op_request):
        allow = False
        allow_self = False #admission for ops on only the caller  itself
        try:
            opname = op_request['opname']
            #anonymously callable functions are allowed always
            if opname == 'getCredential' or opname == 'getAccounting':
                allow = True
            else:
                g_params = op_request['g_params']
                p_params = op_request['p_params']
                target_hrn = g_params['hrn']
                reg_type = ''
                rec_type = g_params['type']
                #determine which registry the call is on (slice or component)
                if rec_type == 'user' or rec_type == 'slice' or rec_type == 'SA':
                    reg_type = 'slc'
                else:
                    reg_type = 'comp'
                operation_set = cred.get_cred()['operation_set']
                on_interfaces = cred.get_cred()['on_interfaces'] 
                is_self_op = False
                if opname == "update" or opname == "remove" or opname == "lookup":
                    is_self_op = True
                #check callable operations within the credential
                for interface in on_interfaces:
                    if interface['type'] == 'registry:'+reg_type and check_authority(target_hrn, interface['name']) and operation_set.has_key(interface['lbl']):
                        if opname in operation_set[interface['lbl']]:
                            allow = True
                            break
                        elif is_self_op and opname + '_self' in operation_set[interface['lbl']] and acc.get_hrn() == target_hrn:
                            allow_self = True
                #if operation is allowed in name, perform additional checks for parameters
                if allow or allow_self:
                    if opname == 'update':
                        if  'ttl' in g_params or 'uuid' in g_params or 'pointer' in g_params or (not allow and 'rights' in g_params):
                            allow = False
                            allow_self = False
            #return result
            if allow or allow_self:
                return True
            else:
                return False
        except Exception, e:
            print "exception in check_authorization:", e
            return False

    def auth_protocol(self, conn):
        if not conn.verify_ok():
            v = conn.get_verify_result()
            print "peer verification failed\n"
            
        peer = PeerInfo()    #keep the peer data who is currently logged in
        #set the gid field
        peer_pem = conn.get_peer_cert()
        peer.cert = peer_pem
        #set the acc field and check it
        result1 = result2 = -1
        result1 = self.exchange_accounting(conn, peer)
        peer_decision = None
        if self.mode == 'server':
            peer_decision = conn.read()
        if result1 == 1:
            conn.write("ACC CHAIN_STRUCTURE_ERROR")
        elif result1 == 2:
            conn.write("ACC TTL_EXPIRED")
        elif result1 == 3:
            conn.write("ACC CHAIN_VERIFY_ERROR")
        else:   #result = 0
            result2 = self.verify_accounting(peer)
            if result2 == 1:
                conn.write("ACC SSL_PUBKEY_MISMATCH")
            elif result2 == 2:
                conn.write("ACC HRN_HIERARCHY_MISMATCH")
            elif result2 == 3:
                conn.write("ACC UNKNOWN_AUTHORITY")
            elif result2 == 4:
                conn.write("ACC UN-IDENTIFIED_ERROR")
            else:
                conn.write("ACC OK")
        if self.mode == 'client':
            peer_decision = conn.read()
        if (result1 != 0)  or (result2 != 0) or peer_decision != "ACC OK" : 
            #close the connection and exit
            conn.close()
            return None
        
        #set the credential field and check it
        result1 = result2 = -1
        result1 = self.exchange_credential(conn,peer)
        peer_decision = None
        if self.mode == 'server':
            peer_decision = conn.read()
        if result1 == 1:
            conn.write("CRED CHAIN_STRUCTURE_ERROR")
        elif result1 == 2:
            conn.write("CRED TTL_EXPIRED")
        elif result1 == 3:
            conn.write("CRED CHAIN_VERIFY_ERROR")
        else:   #result1 = 0
            result2 = self.verify_credential(peer)
            if result2 == 1:
                conn.write("CRED SSL_PUBKEY_MISMATCH")
            elif result2 == 2:
                conn.write("CRED INVALID_DELEGATION")
            elif result2 == 3:
                conn.write("CRED UNKNOWN_AUTHORITY")
            elif result2 == 4:
                conn.write("CRED UN-IDENTIFIED_ERROR")
            else:
                conn.write("CRED OK")
        if self.mode == 'client':
            peer_decision = conn.read()
        if (result1 != 0)  or (result2 != 0) or peer_decision != "CRED OK" : 
            #close the connection and exit
            conn.close()
            return None
        return peer
        
def is_valid_chain(chain_file):
    chain_str = open(chain_file).read()    
    if chain_str[0:27] != "-----BEGIN CERTIFICATE-----":
        return False
    try:
        #divide the received chain into certificates
        arr = chain_str.split("-----BEGIN CERTIFICATE-----")
        arr = arr[1:len(arr)]
        for i in range(len(arr)):
            arr[i] = "-----BEGIN CERTIFICATE-----"+arr[i]
        arr2 = []
        for c_str in arr:
            c_pem = X509.load_cert_string(c_str)
            if not check_valid(c_pem):
                return False
        return True
    except:
        return False

