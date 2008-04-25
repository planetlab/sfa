#wrapper for the registry

# Socket address
LISTEN_HOST = '127.0.0.1' 
LISTEN_PORT = 8002
SR_FILE = 'interface_tree_sr'
CR_FILE = 'interface_tree_cr'

AUTH_HOST = '127.0.0.1' 
AUTH_PORT = 8002

import SocketServer

import socket, os, sys
from M2Crypto import SSL
from M2Crypto.SSL import SSLError
from M2Crypto import X509
from pg import DB
sys.path.append('../')
sys.path.append('../util')
sys.path.append('../util/sec')
sys.path.append("../PLCAPI/trunk")
from util import *
from tree import *
from excep import *
from sec import *
from db import *
from pl_to_geni import *
import time, datetime, calendar

# Import the API Shell
from PLC.Shell import Shell
shell = Shell(globals = globals())             # Add all the API methods to the global namespace
##                 ,config = options.config,     # Configuartion file (Optional. Defaluts to /etc/planetlab/plc_config)
##                 url = options.url,           # XML-RPC server uirl (Optional)
##                 xmlrpc = options.xmlrpc,     # Use XML-RPC ? (Optional)
##                 cacert = options.cacert,     # Certificate to use (Optional)
##                 method = options.method,     # API authentication method (Optional)
##                 role = options.role,         # Role to assume (Optional)
##                 user = options.user,         # (Optional)
##                 password = options.password, # (Required if user is specified)
##                 session = options.session)   # Session authentication 

class GENIServer(SSL.SSLServer):

    #record is the record to be registered
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    def register(self, record, dbinfo):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        type = record['g_params']["type"]
        
        try:
            #check if record already exists
            existing_res = check_exists_geni(record, dbinfo)
            if existing_res:
                    raise ExistingRecord("Record "+record['g_params']['hrn']+" already exists.\n" )
            if type == "SA" or type == 'MA':
                #geni parameters
                record['g_params']["wrapperurl"] = 'local'
                reg_type = ''
                if type == "SA":
                    reg_type = 'slc'
                else:
                    reg_type = 'comp'
                rights = '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)'
                rights = rights + '#0:reg:'+reg_type+":"+obtain_authority(record['g_params']["hrn"])+'#1:reg:'+reg_type+":"+record['g_params']["hrn"]
                record['g_params']['rights'] = rights
                long_hrn = record['g_params']["hrn"]
                hrn_suffix = get_leaf(record['g_params']["hrn"])
                pointer = -1
                login_base = ''
                #PL specific parameters
                site_fields = record['p_params']
                
                #check if the authority's site exists already
                other_tree = None
                if reg_type == 'slc':
                    other_tree = self.cr_tree
                else:
                    other_tree = self.sr_tree
                info = other_tree.tree_lookup(long_hrn)
                if info:
                    login_base = info.login_base
                    pointer = cnx.query("SELECT site_id FROM sites WHERE login_base = '"+login_base+"';").dictresult()[0]['site_id']
                else:
                    #check if login_base is specified
                    if site_fields.has_key('login_base'):
                        login_base = site_fields['login_base']
                        querystr = "SELECT * FROM sites WHERE login_base = '"+login_base+"'"
                        res = cnx.query(querystr).dictresult()
                        if res:
                            return "Site login_base '"+login_base+", already exists in the system. Try another name.\n"
                    else:
                        #determine new login_base
                        login_base = hrn_to_loginbase(long_hrn)
                        for i in range(1,10):
                            querystr = "SELECT * FROM sites WHERE login_base = '"+login_base+"'"
                            res = cnx.query(querystr).dictresult()
                            if not res:
                                break
                            else:
                                login_base = hrn_to_loginbase(long_hrn, i)
                        site_fields['login_base'] = login_base                        
                    #add into PL table
                    pointer = shell.AddSite(pl_auth, site_fields)
                    
                #create the folder for the site and keys
                curdir = os.getcwd()
                if reg_type == 'slc':
                    dir_type = 'slice'
                else:
                    dir_type = 'component'
                dirname = dir_type+'/'+(long_hrn).replace('.','/')
                if os.path.exists(dirname):
                    os.system('rm -rf '+dirname)
                os.makedirs(dirname)
                os.chdir(dirname)
                create_self_cert(hrn_suffix)
                os.chdir(curdir)
                
                #insert into GENI parent table	
                record['g_params']["hrn"] = get_leaf(record['g_params']["hrn"])
                record['g_params']['pubkey'] = X509.load_cert(dirname+'/'+hrn_suffix+'.cert').get_pubkey().as_pem(cipher=None)
                record['g_params']['pointer'] = pointer
                querystr = generate_querystr('INSERT', table, record['g_params'])
                cnx.query(querystr)
                
                #create the new table for the site
                new_table_name = hrn_to_tablename(long_hrn, reg_type)
                cnx.query('DROP TABLE IF EXISTS '+new_table_name) #drop the table if it exists
                querystr = "CREATE TABLE "+new_table_name+" ( \
                hrn text, \
                type text, \
                uuid text, \
                userlist text, \
                rights text, \
                description text, \
                pubkey text, \
                wrapperURL text, \
                disabled text, \
                pointer integer);"
                cnx.query(querystr)
                
                #update the interface tree
                tree = None
                if type == 'SA':
                    tree = self.sr_tree
                else:
                    tree = self.cr_tree
                parent_data = tree.tree_lookup(obtain_authority(long_hrn)).node_data
                parent_db_info = parent_data['db_info']
                parent_key_info = parent_data['key_info']
                info = TreeNodeInfo()
                info.name = long_hrn
                info.login_base = login_base
                db_info = DbInfo()
                key_info = KeyInfo()
                info.node_data = {'db_info':db_info, 'key_info':key_info}
                
                db_info.table_name = new_table_name
                db_info.db_name = parent_db_info.db_name
                db_info.address = parent_db_info.address
                db_info.port = parent_db_info.port
                db_info.user = parent_db_info.user
                db_info.password = parent_db_info.password
                
                key_info.acc_file = ''
                key_info.cred_file = ''
                key_info.folder = parent_key_info.folder+'/'+hrn_suffix
                key_info.id_file = hrn_suffix+'.cert'
                key_info.id_key_file = hrn_suffix+'.pkey'

                tree.tree_add(info)
                if type == 'SA':
                    self.save_state('sr')
                else:
                    self.save_state('cr')
                return type+' '+long_hrn + ' is successfully added.\n'
            
            elif type == "slice":
                login_base = get_leaf(obtain_authority(record['g_params']["hrn"]))
                #geni parameters
                #hrn is inside dictionary, passed by the client
                long_hrn = record['g_params']["hrn"]
                hrn_suffix = get_leaf(record['g_params']["hrn"])
                #PL specific parameters
                slice_fields = record['p_params']
                slice_fields['name'] = login_base + "_" + hrn_suffix
                
                #insert the PL tables first
                pointer = shell.AddSlice(pl_auth, slice_fields)
                #insert into the GENI tables
                record['g_params']["pointer"] = pointer
                querystr = "UPDATE "+table+" SET hrn = '"+hrn_suffix+"'"
                if record['g_params'].has_key('userlist'):
                    querystr = querystr+" userlist = '"+record['g_params']['userlist']+"'"
                if record['g_params'].has_key('rights'):
                    querystr = querystr+" rights = '"+record['g_params']['rights']+"'"
                querystr = querystr+" WHERE pointer = "+str(record['g_params']["pointer"])
                cnx.query(querystr)
                return "Slice "+long_hrn+" is successfully added.\n"
            elif type == "user":	
                #geni parameters
                #hrn and pubkey are inside dictinary, passed by the client
                long_hrn = record['g_params']["hrn"]
                record['g_params']["hrn"] = get_leaf(record['g_params']["hrn"])
                rights = '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)'
                rights = rights + '#0:reg:slc:'+obtain_authority(record['g_params']["hrn"])
                record['g_params']["rights"] = rights
                #PL specific parameters
                user_fields = record['p_params']
                
                #insert the PL tables first
                pointer = shell.AddPerson(pl_auth, user_fields)
                #insert into the GENI tables
                record['g_params']["pointer"] = pointer
                querystr = generate_querystr('INSERT', table, record['g_params'])
                cnx.query(querystr)
                return "User "+long_hrn+" is successfully added.\n"
                
            elif type == "node":	
                #geni parameters
                #hrn and pubkey are inside dictinary, passed by the client
                long_hrn = record['g_params']["hrn"]
                login_base = self.cr_tree.tree_lookup(obtain_authority(long_hrn)).login_base
                record['g_params']["hrn"] = get_leaf(record['g_params']["hrn"])
                rights = ''
                record['g_params']["rights"] = rights
                #PL specific parameters
                node_fields = record['p_params']
                
                #insert the PL tables first
                pointer = shell.AddNode(pl_auth, login_base, node_fields)
        
                #insert into the GENI tables
                record['g_params']["pointer"] = pointer
                querystr = "UPDATE "+table+" SET hrn = '"+record['g_params']["hrn"]+"'"
                if record['g_params'].has_key('rights') and record['g_params']['rights'] != '':
                    querystr = querystr+" rights = '"+record['g_params']['rights']+"'"
                querystr = querystr+" WHERE pointer = "+str(record['g_params']["pointer"])
                cnx.query(querystr)
                return "Node "+long_hrn+" is successfully added.\n"
                
        except Exception, e:
            print "Error in 'register():"+str(e)
            return "Error in register:."+str(e)
            
    #record is the record to be updated
    #record contains the new values of the fields to be changed in a dictionary. 
    #precondition: the authorization mechanism should already checked the fields intended to be updated
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    def update(self, record, dbinfo):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        try:
            #determine the type and PL pointer of the record
            existing_res = check_exists_geni(record, dbinfo)
            if not existing_res:
                raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
            type = existing_res['type']
            pointer = existing_res['pointer']
            long_hrn = record['g_params']["hrn"]
            
            #PL update
            if type == "SA" and pointer != -1:
                #check if record exists in PL
                pl_res = shell.GetSites(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                #PL specific parameters
                site_fields = record['p_params']
                #update the PL tables
                shell.UpdateSite(pl_auth, pointer, site_fields)
            elif type == "MA" and pointer != -1:
                #check if record exists in PL
                pl_res = shell.GetSites(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                #PL specific parameters
                site_fields = record['p_params']
                #update the PL tables
                shell.UpdateSite(pl_auth, pointer, site_fields)
            elif type == "slice":
                #check if record exists in PL
                pl_res = shell.GetSlices(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                #PL specific parameters
                slice_fields = record['p_params']
                #update the PL tables
                shell.UpdateSlice(pl_auth, pointer, slice_fields)
                #process the new users added to the slice
                for user in record['g_params']['userlist']:
                    usr_dbinfo = determine_dbinfo(get_authority(user), self.tree)
                    if usr_dbinfo:
                        rec = {'g_params':{'hrn':user}, 'p_params':{}}
                        user_pointer = self.lookup(rec, usr_dbinfo)['geni']['pointer']
                        querystr = "INSERT INTO slice_person VALUES("+pointer+", "+user_pointer+");"
                        cnx.query(querystr)
            elif type == "user":
                #check if record exists in PL
                pl_res = shell.GetPersons(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                #PL specific parameters
                user_fields = record['p_params']
                #update the PL tables
                shell.UpdatePerson(pl_auth, pointer, user_fields)
            elif type == "node":
                #check if record exists in PL
                pl_res = shell.GetNodes(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                #PL specific parameters
                node_fields = record['p_params']
                #update the PL tables
                shell.UpdateNode(pl_auth, pointer, node_fields)
                
            #geni update
            #all fields to be updated resides in the dictionary passed by the client, we just change the hrn field
            record['g_params']["hrn"] = get_leaf(record['g_params']["hrn"])
            #update the GENI table
            querystr = generate_querystr('UPDATE', table, record['g_params'])
            cnx.query(querystr)
            return "The record '"+long_hrn+"' is successfully updated.\n"
        except Exception, e:
            print "Error in 'update():'"+str(e)
            return "Error in update:"+str(e)

    #record shows the hrn to be deleted
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    #we enforce that the deletions of SA/MA are only at leaf
    def remove(self, record, dbinfo):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        try:
            #determine the type and PL pointer of the record
            long_hrn = record['g_params']["hrn"]
            hrn_suffix = get_leaf(record['g_params']["hrn"])
            existing_res = check_exists_geni(record, dbinfo)
            if not existing_res:
                raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
            type = existing_res['type']
            pointer = existing_res['pointer']
            
            #delete from the PL tables
            if type == "SA" or type == "MA":
                #do not allow removal if site is not leaf
                tree = None
                if type == 'SA':
                    tree = self.sr_tree
                else:
                    tree = self.cr_tree
                leaf = tree.is_leaf(long_hrn)
                if leaf == None:
                    return "Error in remove.\n"
                elif leaf == False:
                    return "Site removal should be at the leaves.\n"
            
                #update the interface tree
                tree.tree_remove(long_hrn)
                
                if type == 'SA':
                    self.save_state('sr')
                else:
                    self.save_state('cr')
                
                #if the site still exists in the tree, do not remove from pl, else remove
                if not site_to_auth(pointer):
                    try:
                        shell.DeleteSite(pl_auth, pointer)
                    except:
                        1==1  #the site may not be deleted because ttl of it expired, so should continue
            elif type == 'user':
                shell.DeletePerson(pl_auth, pointer)
            elif type == "slice":
                shell.DeleteSlice(pl_auth, pointer)
            elif type == "node":
                shell.DeleteNode(pl_auth, pointer)
                
            #delete from the GENI table
            querystr = generate_querystr('DELETE', table, record['g_params'])
            cnx.query(querystr)
            return "The record '"+long_hrn+"' is successfully removed.\n"
        except Exception, e:
            print "Error in 'delete()'"+str(e)
            return "Error in delete:"+str(e)
            
    #record shows the hrn to be searched
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    def lookup(self, record, dbinfo):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        try:
            #lookup in GENI tables
            existing_res = check_exists_geni(record, dbinfo)
            if not existing_res:
                raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
            type = existing_res['type']
            pointer = existing_res['pointer']
            #lookup in the PL tables
            pl_res = None
            if type == "SA" and pointer != -1:
                pl_res = shell.GetSites(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                pl_res = pl_res[0]
            elif type == "MA" and pointer != -1:
                pl_res = shell.GetSites(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                pl_res = pl_res[0]
            elif type == "slice":
                pl_res = shell.GetSlices(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                pl_res = pl_res[0]
            elif type == "user":
                pl_res = shell.GetPersons(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                pl_res = pl_res[0]
            elif type == "node":
                pl_res = shell.GetNodes(pl_auth, [pointer])
                if not pl_res:
                    self.remove(record,dbinfo)
                    raise NonexistingRecord("Record "+record['g_params']["hrn"]+" does not exist.\n" )
                pl_res = pl_res[0]
            return str({'pl':pl_res, 'geni':existing_res})
        except:
            return None
            

    def list(self, record, dbinfo):
        x=1
        
    #grants the credentials existing in database to the caller
    #peer parameter shows the caller information
    #record keeps the parameter: credential name
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    #keyinfo is the id, id_key, and accounting data for the authority
    #peerinfo is [peer_hrn, peer_certficate]
    def getCredential(self, record, dbinfo, keyinfo, peerinfo):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        try:
            cred_pem = None
            if record['g_params']['cred_name'].split(':')[0] == 'registry':
                #lookup in GENI tables
                geni_res = cnx.query("SELECT * FROM "+table+" WHERE hrn = '"+get_leaf(peerinfo[0])+"' ").dictresult()
                if geni_res:
                    geni_res = geni_res[0]
                else:
                    raise NonexistingRecord("Record "+peerinfo[0]+" does not exist.\n" )
                type = geni_res['type']
                pointer = geni_res['pointer']
                rights = geni_res['rights']
                #lookup in the PL tables
                pl_res = None
                if type == "SA" and pointer != -1:
                    pl_res = shell.GetSites(pl_auth, [pointer])
                    if not pl_res:
                        self.remove(record,dbinfo)
                        raise NonexistingRecord("Record "+peerinfo[0]+" does not exist.\n" )
                elif type == "MA" and pointer != -1:
                    pl_res = shell.GetSites(pl_auth, [pointer])
                    if not pl_res:
                        self.remove(record,dbinfo)
                        raise NonexistingRecord("Record "+peerinfo[0]+" does not exist.\n" )
                elif type == "user":
                    pl_res = shell.GetPersons(pl_auth, [pointer])
                    if not pl_res:
                        self.remove(record,dbinfo)
                        raise NonexistingRecord("Record "+peerinfo[0]+" does not exist.\n" )
                    pl_res = shell.GetPersons(pl_auth, [pointer])[0]
                    if rights == '' or rights == None:
                        if 'admin' in pl_res['roles']:
                            rights = '(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)'+ \
                                        '(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)'
                            rights = rights + '#0:reg:slc:'+ROOT_AUTH + '#1:reg:comp:'+ROOT_AUTH
                        elif 'pi' in pl_res['roles']:
                            rights = '(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)'+\
                                        '(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)'
                            rights = rights + '#0:reg:slc:'+obtain_authority(peerinfo[0]) + '#1:reg:comp:'+obtain_authority(peerinfo[0])
                        elif 'user' in pl_res['roles']:
                            rights = '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)'
                            rights = rights + '#0:reg:slc:'+obtain_authority(peerinfo[0])
                elif type == "node":
                    pl_res = shell.GetNodes(pl_auth, [pointer])
                    if not pl_res:
                        self.remove(record,dbinfo)
                        raise NonexistingRecord("Record "+peerinfo[0]+" does not exist.\n" )
                #authcert, authkey, pubkey, cname, rights, time
                cname = 'Registry credentials'
                openssl_cert = peerinfo[1]
                cred_pem = create_cred(keyinfo[0], keyinfo[1], openssl_cert.get_pubkey(), cname, rights)
            else:
                cred_name = record['g_params']['cred_name'].split(':')
                if cred_name[0] == 'slice':
                    slc_rec = {'g_params':{'hrn':cred_name[1]}, 'p_params':{}}
                    slc_result = self.lookup(slc_rec, dbinfo)
                    has_slc = False
                    deleted = slc_result['p_params']['is_deleted']
                    expires= time.strptime(slc_result['p_params']['expires'], PL_DATETIME_FORMAT)
                    expires = datetime.timedelta(seconds=calendar.timegm(expires))
                    if slc_result and  deleted == 'f':
##                        if peerinfo[0] in slc_result['geni']['userlist']:
##                            has_slc = True
##                        else:
                        usr_dbinfo = determine_dbinfo(get_authority(peerinfo[0]), self.tree)
                        if usr_dbinfo:
                            rec = {'g_params':{'hrn':peerinfo[0]}, 'p_params':{}}
                            user_pointer = self.lookup(rec, usr_dbinfo)['geni']['pointer']
                            querystr = "SELECT * FROM person_slice WHERE person_id = "+user_pointer+" AND slice_id = "+slc_result['geni']['pointer']
                            usr_slc_res = cnx.query(querystr).dictresult()
                            if usr_slc_res:
                                has_slc = True
                        if has_slc:
                            rights = ''
                            if slc_result['geni']['rights'] != '' or slc_result['geni']['rights'] != None:
                                rights = slc_result['geni']['rights']
                            else:
                                rights = '(10-0)(11-0)(12-0)(13-0)(14-0)(15-0)(16-0)(17-0)(18-0)(20-0)(21-0)(22-0)(23-0)'
                                rights = rights + '#0:comp:planetlab.*'
                            #authcert, authkey, pubkey, cname, rights, time
                            cname = slc_result['geni']['hrn']
                            timenow = datetime.timedelta(seconds=time.time())
                            if expires - timenow > CRED_GRANT_TIME:
                                openssl_cert = crypto.load_certificate(crypto.FILETYPE_PEM, peerinfo[1])
                                cred_pem = create_cred(keyinfo[0], keyinfo[1], openssl_cert.get_pubkey(), cname, rights)
                else:
                    raise NonexistingCredType("Credential "+cred_name[0]+" does not exist.\n" )
            if cred_pem == None:
                return cred_pem
            else:
                return crypto.dump_certificate(crypto.FILETYPE_PEM, cred_pem)+keyinfo[3]
        except: 
            return None     


    #returns the existing acconting information in database to the caller
    #peer parameter shows the caller certificate, containing the public key
    #record keeps the parameter: account_name to ask for
    #dbinfo is the information showing the relevant tables to act (db and table name), in the subtree this interface manages
    #keyinfo is the id, id_key, and accounting data for the authority
    #peer_cert is the ssl certificate of the peer
    def getAccounting(self, record, dbinfo, keyinfo, peer_cert):
        cnx = dbinfo[0]
        table = dbinfo[1] 
        try:
            acc = None
            #check if the record exists
            rec = {'g_params':{'hrn':record['g_params']['account_name']}, 'p_params':{}}
            res = eval(self.lookup(rec, dbinfo))
            if not res:
                raise NonexistingRecord("Record "+record['g_params']["account_name"]+" does not exist.\n" )
            if res['geni']['pubkey'] == peer_cert.get_pubkey().as_pem(cipher=None):
                openssl_cert = crypto.load_certificate(crypto.FILETYPE_PEM, peer_cert.as_pem())
                uuid = 0
                if not res['pl']:
                    uuid = res['geni']['uuid']
                else:
                    uuid = res['pl']['uuid']
                acc = create_acc(keyinfo[0], keyinfo[1], openssl_cert.get_pubkey(), record['g_params']['account_name'], uuid)
            if acc == None:
                return acc
            else:
                return crypto.dump_certificate(crypto.FILETYPE_PEM, acc)+keyinfo[2]
        except:
            return None
        
    def __init__(self, socket, handler):
        #initialize trees
        self.sr_tree_file = SR_FILE
        self.cr_tree_file = CR_FILE
        self.sr_tree = None
        self.cr_tree = None
        self.construct_hierarchy()
        set_tree_globals(self.sr_tree, self.cr_tree)
        #initialize security module
        self.sec = None
        self.sec_init()
        #set function list
        self.functionList = {"register":self.register, "remove":self.remove, "update":self.update, "lookup":self.lookup, "list":self.list, "getCredential":self.getCredential, "getAccounting":self.getAccounting}
        SSL.SSLServer.__init__(self, socket, handler, self.sec.ctx)
    
    def construct_hierarchy(self):
        self.sr_tree = InterfaceTree('slice', self.sr_tree_file, (AUTH_HOST, AUTH_PORT)) #slice registry interface tree
        self.cr_tree = InterfaceTree('component', self.cr_tree_file, (AUTH_HOST, AUTH_PORT)) #component registry interface tree
    
    def sec_init(self):
        key_info = self.sr_tree.my_tree.info.node_data['key_info']
        id_file = key_info.folder+'/'+key_info.id_file
        id_key_file = key_info.folder+'/'+key_info.id_key_file
        acc_file = key_info.folder+'/'+key_info.acc_file
        cred_file = key_info.folder+'/'+key_info.cred_file
            
        self.sec = Sec('server', id_file, id_key_file, acc_file, cred_file) 
        renew_cert('accounting', key_info.folder, 'slice', self.sr_tree.my_tree.info.name, None, None, (AUTH_HOST, AUTH_PORT), self.sec)
        renew_cert('credential', key_info.folder, 'slice', self.sr_tree.my_tree.info.name, None, None, (AUTH_HOST, AUTH_PORT), self.sec)
        
    #save the state of the interface trees
    def save_state(self, type='both'):
        if type == 'sr' or type == 'both' :
            self.sr_tree.save_tree()
        if type == 'cr' or type == 'both' :
            self.cr_tree.save_tree()

class handle_connection(SocketServer.BaseRequestHandler):
    def handle(self):
##        pid = os.fork()
##        if pid:
##            # parent process closes connnection and returns
##            self.request.socket.close()
##            return
##        else:
        try:
            peer = server.sec.auth_protocol(self.request)
            if not peer:
                return
            
            operation_request = msg_to_params(self.request.read())
            #determine the database information associated with the hrn of the call
            hrn_of_call = operation_request["g_params"]["hrn"]
            opname = operation_request["opname"]
            target_hrn = ''
            if opname == "register" or opname == "remove" or opname == "update" or opname == "lookup":
                target_hrn = obtain_authority(hrn_of_call)
            elif opname == 'list' or opname == 'getCredential' or opname == 'getAccounting':
                target_hrn = hrn_of_call 
            reg_type = ''
            if opname == "register" or opname == "remove" or opname == "update" or opname == "lookup" or opname == 'list':
                type = operation_request["g_params"]["type"]
                if type == 'slice' or type == 'user' or type == 'SA':
                    reg_type = 'slice'
                else:
                    reg_type = 'component'
            elif opname == 'getCredential':
                if operation_request["g_params"]["cred_name"].split(':')[1] == 'slc':
                    reg_type = 'slice'
                else:
                    reg_type = 'component'
            elif opname == 'getAccounting':
                reg_type = operation_request["g_params"]["registry"]
            tree = None
            if reg_type == 'slice':
                tree = server.sr_tree
            else:
                tree = server.cr_tree    
            dbinfo = determine_dbinfo(target_hrn, tree)
            keyinfo = None
            if opname == 'getAccounting':
                keyinfo = tree.determine_keyinfo(target_hrn, server, 'accounting')
            elif opname == 'getCredential':
                keyinfo = tree.determine_keyinfo(target_hrn, server, 'credential')
            if (dbinfo == None):
                self.request.write("WRONG INTERFACE")
                return
            # check to see if a matching function has been registered
            if not server.functionList.has_key(operation_request['opname']): 
                self.request.write("NO FUNC")
                return
            #check the authorization of the peer
            if not server.sec.check_authorization(peer.acc, peer.cred, operation_request):
                self.request.write("AUTHORIZATION FAIL")
                return
        
            #perform the function call
            op = server.functionList[operation_request["opname"]]
            params = {'g_params':operation_request["g_params"], 'p_params':operation_request["p_params"]} 
            result = None
            if op == server.getAccounting:
                result = op(params,dbinfo, keyinfo, peer.cert)
            elif op == server.getCredential:
                peerinfo = [peer.acc.get_hrn(), crypto.load_certificate(crypto.FILETYPE_PEM, peer.cert.as_pem())]
                result = op(params,dbinfo, keyinfo, peerinfo)
            elif op == server.register or op == server.update or op == server.remove:
                result = str({'message':op(params,dbinfo)})
            else:
                result = op(params,dbinfo)
                if not result: 
                    self.request.write(str({'message':'Requested record does not exist.\n'}))
            self.request.write(result)
            return
        except Exception, e:
            print "There is an error handling the request. "+str(e)
            return

#child process never executes this function, because it exits in "handle_connection".
##    def finish(self):
##        server.save_state()
    
server = GENIServer((LISTEN_HOST, LISTEN_PORT), handle_connection)
def main():
    server.save_state()
    server.serve_forever()   


if __name__=="__main__":
    main()

