import os, sys
import uuid
sys.path.append('./sec')
from util import *
from excep import *
from sec import *
from db import *
from pl_to_geni import *

ROOT_AUTH = 'planetlab' #need to know the higher most node

class TreeNodeInfo:
    def __init__(self):
        self.name = '' # hrn
        self.login_base = None
        self.node_data = None
    def serial(self):
        dic = {'name':self.name, 'login_base':self.login_base, 'node_data':None}
        if self.node_data:
            dic['node_data'] = {}
            if self.node_data.has_key('key_info'):
                dic['node_data']['key_info'] = self.node_data['key_info'].serial()
            if self.node_data.has_key('db_info'):
                dic['node_data']['db_info'] = self.node_data['db_info'].serial()
        return dic
        
class KeyInfo:
    def __init__(self):
        self.folder = ''
        self.id_file = ''
        self.id_key_file = ''
        self.acc_file = ''
        self.cred_file = ''
        self.last_update = ''
    def serial(self):
        return {'folder': self.folder, 'id_file': self.id_file, 'id_key_file': self.id_key_file, 'acc_file': self.acc_file, 'cred_file': self.cred_file, 'last_update': self.last_update}
    
class DbInfo:
    def __init__(self):
        self.table_name = ''  #ex: planetlab.br_sr
        self.db_name = '' #ex: plDB 
        self.address = ''
        self.port = 0
        self.user = ''
        self.password = ''
    def serial(self):
        return {'table_name':self.table_name, 'db_name':self.db_name, 'address':self.address, 'port':self.port, 'user':self.user, 'password':self.password}

class TreeNode:
    def __init__(self):
        self.info = None
        self.children = []
    def serial(self):
        children = []
        if len(self.children)>0:
            for c in self.children:
                children.append(c.serial())
        if self.info:
            return {'children':children, 'info':self.info.serial()}
        else:
            return {'children':children, 'info':None}
        
class InterfaceTree:
    def __init__(self, type, filename, auth_addr):
        #the tree for keeping the site names managed by this interface instance
        self.my_tree = None
        self.type = type
        self.filename = filename
        self.auth_addr = auth_addr
        self.tree_init()
        
    #check a hrn if exists in the tree, return the info of it, if not found return None
    #hrn:string
    def tree_lookup(self, hrn) :
        tree= self.my_tree
        if not tree: #tree empty
            return None
        found = True
        hrn_arr = geni_to_arr(hrn)
        tmp_tree = tree
        if tmp_tree.info.name != hrn_arr[0] :
            found = False
        else : 
            cur_name = hrn_arr[0] + ''
            for i in range(1, len(hrn_arr)):
                cur_name = cur_name + '.' + hrn_arr[i]
                child_found = False
                child = {}
                for j in range(len(tmp_tree.children)) : 
                    if tmp_tree.children[j].info.name == cur_name :
                        child_found = True
                        child = tmp_tree.children[j]
                        break
                if child_found == False:
                    found = False
                    break
                else:
                    tmp_tree = child
        if found == True:
            return tmp_tree.info
        else:
            return  None

    def is_leaf(self, hrn):
        tree= self.my_tree
        if not tree: #tree empty
            return None
        found = True
        hrn_arr = geni_to_arr(hrn)
        tmp_tree = tree
        if tmp_tree.info.name != hrn_arr[0] :
            found = False
        else : 
            cur_name = hrn_arr[0] + ''
            for i in range(1, len(hrn_arr)):
                cur_name = cur_name + '.' + hrn_arr[i]
                child_found = False
                child = {}
                for j in range(len(tmp_tree.children)) : 
                    if tmp_tree.children[j].info.name == cur_name :
                        child_found = True
                        child = tmp_tree.children[j]
                        break
                if child_found == False:
                    found = False
                    break
                else:
                    tmp_tree = child
        if found == True:
            return tmp_tree.children == []
        else:
            return  None
    
    #add a new branch into the tree, branch is indicated by info
    #info: TreeNodeInfo
    def tree_add(self, info):
        tree= self.my_tree
        inserted = False
        hrn_arr = geni_to_arr(info.name)
        tmp_tree = tree
        
        if hrn_arr == []:
            raise TreeException("Wrong input hrn: "+info.name)
        else:
            if tree == None:
                if len(hrn_arr) == 1:
                    #insert the node
                    tree = TreeNode()
                    tree.info = info
                    inserted = True
            else:
                cur_name = hrn_arr[0] + ''
                if tmp_tree.info.name == cur_name:
                    for i in range(1, len(hrn_arr)):
                        cur_name = cur_name + '.' + hrn_arr[i]
                        child_found = False
                        child = {}
                        for j in range(len(tmp_tree.children)) : 
                            if tmp_tree.children[j].info.name == cur_name :
                                child_found = True
                                child = tmp_tree.children[j]
                                break
                        if child_found == False:
                            if len(hrn_arr) - i == 1:
                                #insert the remaining of hrn
                                new_child = TreeNode()
                                new_child.info = info
                                tmp_tree.children.append(new_child)
                                inserted = True
                            break
                        else:
                            tmp_tree = child
                    if inserted == False:
                        print "The hrn '"+info.name+"' should be at leaf position to be inserted.\n"
            return inserted
                
    #remove the branch indicated by hrn from the tree
    #hrn: string
    def tree_remove(self, hrn):
        tree= self.my_tree
        removed = False
        hrn_arr = geni_to_arr(hrn)
        tmp_tree = tree
        if tmp_tree.info.name == hrn_arr[0] :
            cur_name = hrn_arr[0] + ''
            for i in range(1, len(hrn_arr)):
                cur_name = cur_name + '.' + hrn_arr[i]
                child_found = False
                child = {}
                for j in range(len(tmp_tree.children)) : 
                    if tmp_tree.children[j].info.name == cur_name :
                        child_found = True
                        child = tmp_tree.children[j]
                        break
                if child_found == False:
                    break
                else:
                    if i == len(hrn_arr)-1:
                        tmp_tree.children.remove(child)
                        removed = True
                    else:
                        tmp_tree = child
        return removed
                
    #initialize the tree with the file data
    def tree_init(self):
        filename = self.filename
        type = self.type
        try:
            #check if dict file exists 
            if not os.path.exists(filename+'_dict'):
                if not os.path.exists(filename):
                    print 'Error: File not found.\n'
                    raise NonExistingFile(filename)
                else:
                    self.__file_to_treedict(filename)
                    self.my_tree = self.__deserialize_tree(eval(open(filename+'_dict').read()))
            else:
                self.my_tree = self.__deserialize_tree(eval(open(filename+'_dict').read()))
            #create the tables and key folders if they do not exist already
            self.__sync_with_db_rec(type, self.my_tree)
        except:
            print 'Error in initialzing the tree.\n'
            os._exit(1)
            
    def save_tree(self):
        open(self.filename+'_dict', 'w').write(str(self.my_tree.serial()))

    def __sync_with_db_rec(self, type, treenode):
        self.__sync_with_db(type, treenode)
        for child in treenode.children:
            self.__sync_with_db_rec(type, child)
        
    #if do not exist, creates the (key folder, private key and self signed cert) and the db table for the node, fills the table with the children info
    #type: 'slice' or 'component' indicating the registry type
    #hierarchy:hrn so far
    #treenode: node to be synched
    def __sync_with_db(self, type, treenode):
        curdir = os.getcwd()
        key_req = False
        table_req = False
        if not treenode.info.node_data:
            treenode.info.node_data = {}
            #create key folder, private key and self signed cert
            hrn = treenode.info.name
            dirname = type+'/'+(hrn).replace('.','/')
            hrn_suffix = get_leaf(hrn)
            if os.path.exists(dirname):
                os.system('rm -rf '+dirname)
            os.makedirs(dirname)
            os.chdir(dirname)
            create_self_cert(hrn_suffix)
            k = KeyInfo()
            k.folder = dirname
            k.id_file = hrn_suffix+'.cert'
            k.id_key_file = hrn_suffix +'.pkey'
            #for the top authority create the acc and cred files
            if obtain_authority(hrn) == '':
                id_cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(k.id_file).read())
                id_pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(k.id_key_file).read())
                uu_id = str(uuid.uuid4().int)
                regtype = ''
                if type == 'slice':
                    regtype = 'slc'
                else:
                    regtype = 'comp'
                rights = '(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)'
                rights = rights + '#0:reg:'+regtype+':'+hrn
                k.acc_file = 'acc_file'
                k.cred_file = 'cred_file'
                acc = create_acc(id_cert, id_pkey, id_cert.get_pubkey(), hrn, uu_id)
                cred = create_cred(id_cert, id_pkey, id_cert.get_pubkey(), 'Registry credentials', rights)
                open(k.acc_file, 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, acc))
                open(k.cred_file, 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cred))
            treenode.info.node_data['key_info'] = k
            os.chdir(curdir)
            #create the table and set in the treenode data structure
            suffix = ''
            if type == 'slice':
                suffix = SR_SUFFIX
            else:
                suffix = CR_SUFFIX
            tablename = hrn.replace('.','$') + suffix
            cnx = get_plDB_conn()
            querystr = "CREATE TABLE "+tablename+" ( \
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

            cnx.query('DROP TABLE IF EXISTS '+tablename) #drop the table if it exists
            cnx.query(querystr)
            d = DbInfo()
            d.table_name = tablename
            get_plDB_info(d)
            treenode.info.node_data['db_info'] = d
            #if the authority resides in PL as site, then fill it with the PL data
            if treenode.children == []:
                populate_pl_data(hrn_suffix, tablename, type)
                treenode.info.login_base = hrn_suffix
            #insert the record into parent's table
            if obtain_authority(hrn) != '':
                rectype = ''
                regtype = ''
                if type == 'slice':
                    rectype = 'SA'
                    regtype = 'slc'
                else:
                    rectype = 'MA'
                    regtype = 'comp'
                uu_id = ''
                if treenode.children != []:
                    uu_id = str(uuid.uuid4().int)
                rights = '(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)'
                rights = rights + '#0:reg:'+regtype+':'+obtain_authority(hrn)+'#1:reg:'+regtype+':'+hrn
                id_file = treenode.info.node_data['key_info'].folder+'/'+ treenode.info.node_data['key_info'].id_file
                pubkey = X509.load_cert(id_file).get_pubkey().as_pem(cipher=None)
                wrapper = 'local'
                pointer = -1
                if treenode.children == []: #get pointer if authority resides in PL as site
                    pointer = cnx.query("SELECT site_id FROM sites WHERE login_base='"+hrn_suffix+"'").dictresult()[0]['site_id']
                disabled = 'f'
                record = {'hrn':get_leaf(hrn), 'type':rectype, 'uuid':uu_id, 'rights':rights, 'pubkey':pubkey, 'wrapperURL':wrapper, 'pointer':pointer, 'disabled':disabled}
                querystr = generate_querystr('INSERT', obtain_authority(hrn).replace('.','$')+suffix, record)
                cnx.query(querystr)
    
    #gets a tree in the form of a dictionary, 
    #                ex:  {'info':{'name':'planetlab', 'node_data':{'key_info':{...}, 'db_info':{...}}}, 'children':[x1, x2, ..]}
    #returns the tree in the TreeNode class format
    def __deserialize_tree(self, treenode_dict):
        node = TreeNode()        
        node.info = TreeNodeInfo()
        node.info.name = treenode_dict['info']['name']
        node.info.login_base = treenode_dict['info']['login_base']
        if treenode_dict['info']['node_data']:
            node.info.node_data = {}
            if treenode_dict['info']['node_data'].has_key('key_info'):
                node.info.node_data['key_info'] = KeyInfo()
                keyinf = treenode_dict['info']['node_data']['key_info']
                node.info.node_data['key_info'].folder = keyinf['folder']
                node.info.node_data['key_info'].id_file = keyinf['id_file']
                node.info.node_data['key_info'].id_key_file = keyinf['id_key_file']
                node.info.node_data['key_info'].acc_file = keyinf['acc_file']
                node.info.node_data['key_info'].cred_file = keyinf['cred_file']
                node.info.node_data['key_info'].last_update = keyinf['last_update']
            if treenode_dict['info']['node_data'].has_key('db_info'):
                node.info.node_data['db_info'] = DbInfo()
                dbinf = treenode_dict['info']['node_data']['db_info']
                node.info.node_data['db_info'].table_name = dbinf['table_name']
                node.info.node_data['db_info'].db_name = dbinf['db_name']
                node.info.node_data['db_info'].address = dbinf['address']
                node.info.node_data['db_info'].port = dbinf['port']
                node.info.node_data['db_info'].user = dbinf['user']
                node.info.node_data['db_info'].password = dbinf['password']
        for child in treenode_dict['children']:
            node.children.append(self.__deserialize_tree(child))
        return node 

    #gets a file name for tree and constructs an output file which contains the tree in dictionary format
    #write to file:  ex:  {'info':{'name':'planetlab', 'node_data':{'key_info':{...}, 'db_info':{...}}}, 'children':[x1, x2, ..]}
    def __file_to_treedict(self, filename):
        lines = open(filename).readlines()
        hierarchy = ''
        (node, line) = self.__file_to_treedict_rec(lines, 0, hierarchy, 0)
        open(filename+'_dict', 'w').write(str(node))
        
    #helper function
    #return: (node, line)
    def __file_to_treedict_rec(self, lines, indent, hierarchy, line):
        node = {'info':{'name':'', 'login_base':'', 'node_data':None}, 'children':[]}
        #count #tabs
        j = 0
        while lines[line][j] == '\t':
            j = j+1
        if indent != j:
            print 'Error in file to dictionary conversion.\n'
            return None
        name = lines[line].split(' ')[0]
        name = name[j:len(name)]
        if hierarchy == '':
            node['info']['name'] = name
        else:
            node['info']['name'] = hierarchy + '.' + name
        node['info']['login_base'] = name
        #next indent count
        j = 0
        if line+1 != len(lines):        
            while lines[line+1][j] == '\t':
                j = j+1
        if j > indent+1:
            print 'Error in file to dictionary conversion.\n'
            return None
        indent2 = j
        line = line+1
        while indent2 > indent: 
            (child, line) = self.__file_to_treedict_rec(lines, indent2, node['info']['name'], line)
            node['children'].append(child)
            j = 0
            if line != len(lines):    
                while lines[line][j] == '\t':
                    j = j+1
            indent2 = j
        return (node, line)


    #determines the key info of a given hrn within the tree, performs calls back to 'server' to obtain updated certs
    #if the hrn does not exist in the tree hierarchy None is returned
    #server: the server instance is passed for calls to getCredential/getAccounting if necessary
    #type is credential or accounting; one of them at a time is determined by the function
    #returns an array containing the self-signed certificate, private key, and acc or cred chain in string
    def determine_keyinfo(self, hrn, server, type):
        tree = self
        reg_type = self.type
        info = tree.tree_lookup(hrn)
        if info == None:
            return None
        else:
            keyinfo = info.node_data['key_info']
            folder = keyinfo.folder
            id_file = folder+'/'+keyinfo.id_file
            id_key_file = folder+'/'+keyinfo.id_key_file
            #check the id file
            if not os.path.exists(folder) or not os.path.exists(id_file):
                print 'Id file for '+hrn+' does not exist.\n'
                return None
            else:
                #check acc or cred
                acc_str = None
                cred_str = None
                renew_res = renew_cert(type, folder, reg_type, hrn, server, tree, tree.auth_addr, server.sec)
                if renew_res == None:
                    return None
                if type == 'accounting':
                    keyinfo.acc_file = 'acc_file'
                    acc_str = open(keyinfo.folder+'/'+keyinfo.acc_file).read()
                else:
                    keyinfo.cred_file = 'cred_file'
                    cred_str = open(keyinfo.folder+'/'+keyinfo.cred_file).read()
                id = crypto.load_certificate(crypto.FILETYPE_PEM, open(id_file).read())
                id_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(id_key_file).read())
                return [id, id_key, acc_str, cred_str]
