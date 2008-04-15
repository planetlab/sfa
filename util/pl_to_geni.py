import sys
from pg import DB
from db import *
from util import *

PL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        
#given a login_base or site_id (which are ids of a site in Planetlab), determines the hierarchical name of it in GENI
def site_to_auth(id_or_loginbase):
    cnx = get_plDB_conn()
    site_id = None
    hrn = None
    loginbase = None
    if isinstance(id_or_loginbase, int):
        site_id = id_or_loginbase
        querystr = "SELECT login_base FROM sites WHERE site_id = "+str(id_or_loginbase)
        res = cnx.query(querystr).dictresult()
        if res:
            loginbase = res[0]['login_base']
        else:
            return None
    else:
        loginbase = id_or_loginbase
        #get site_id
        querystr = "SELECT site_id FROM sites WHERE login_base = '"+loginbase+"'"
        res = cnx.query(querystr).dictresult()
        if res:
            site_id = res[0]['site_id']
        else:
            return None
    #search login_base in trees
    (sr_tree, cr_tree) = get_tree_globals()
    hrn = site_to_auth_rec(loginbase, sr_tree.my_tree)
    if not hrn:
        hrn = site_to_auth_rec(loginbase, cr_tree.my_tree)
    if not hrn:
        return None
    else:
        return (site_id, hrn)
    
def site_to_auth_rec(loginbase, treenode):
    if treenode.info.login_base and treenode.info.login_base == loginbase:
        return treenode.info.name
    else:
        for child in treenode.children:
            name = site_to_auth_rec(loginbase, child)
            if name:
                return name
    return None
    
def hrn_to_loginbase(hrn, algorithm=0):
    hrn_arr = hrn.split('.')
    j = len(hrn_arr)-2
    alg_count = algorithm-1 
    login_base = hrn_arr[len(hrn_arr)-1]
    while j>=0 and alg_count>=0:
        if alg_count == 0:
            login_base = login_base+hrn_arr[j]
        j = j-1
        alg_count = alg_count-1
    if len(login_base) > 20:
        return login_base[0:20]
    else:
        return login_base
        
    
#given an email or person_id (which are ids of a person in Planetlab), determined the last portion of hierarchical name of it in GENI
def person_to_user(email, algorithm = 0):
    hrn_suffix = ''
    if algorithm == 0:
        hrn_suffix = email.split('@')[0].replace('.','-')
    elif algorithm == 1:
        hrn_suffix = email.split('@')[0].replace('.','-')+'-'+email.split('@')[1].split('.')[0]
    elif algorithm == 2:
        hrn_suffix = email.replace('@','-')
        hrn_suffix = hrn_suffix.replace('.','-')
    return hrn_suffix
    
def plslice_to_slice(slice_name):
    i = 0
    while slice_name[i]!='_':
        i = i+1
    return slice_name[i+1:len(slice_name)]
    
def plnode_to_node(hostname, algorithm = 0):
    hrn_suffix = ''
    if algorithm == 0:
        hrn_suffix = hostname.split('.')[0]
    elif algorithm == 1:
        hrn_suffix = hostname.split('.')[0]+'-'+hostname.split('.')[1]
    elif algorithm == 2:
        hrn_suffix = hrn_suffix.replace('.','-')
    return hrn_suffix
    
def check_exists_pl(cnx, pointer, type):
    exists = True
    if type == 'SA' or type == 'MA':
        res = cnx.query("SELECT deleted FROM sites WHERE site_id = "+str(pointer)).dictresult()
        if len(res)==0 or res[0]['deleted'] == 't':
            exists = False
    elif type == 'slice':
        res = cnx.query("SELECT is_deleted FROM slices WHERE slice_id = "+str(pointer)).dictresult()
        if len(res)==0 or res[0]['is_deleted'] == 't':
            exists = False
    elif type == 'user':
        res = cnx.query("SELECT deleted FROM persons WHERE person_id = "+str(pointer)).dictresult()
        if len(res)==0 or res[0]['deleted'] == 't':
            exists = False
    elif type == 'node':
        res = cnx.query("SELECT deleted FROM nodes WHERE node_id = "+str(pointer)).dictresult()
        if len(res)==0 or res[0]['deleted'] == 't':
            exists = False
    return exists
    
def check_exists_geni(record, dbinfo):
    cnx = dbinfo[0]
    table = dbinfo[1] 
    try:
        #lookup in GENI tables
        geni_res = cnx.query("SELECT * FROM "+table+" WHERE hrn = '"+get_leaf(record['g_params']["hrn"])+"' ").dictresult()
        if geni_res:
            return geni_res[0]
        else:
            return None
    except:
        return None
        
#fill the geni table with the records in PL database
#login_base: indicates the site in PL
#tablename: the GENI table name
#type: 'slice' or 'component' indicating the registry type of the GENI table
def populate_pl_data(login_base, tablename, type):
    cnx = get_plDB_conn()
    site_id = cnx.query("SELECT site_id FROM sites WHERE login_base='"+login_base+"';").dictresult()[0]['site_id']
    
    if type == 'slice': #slice registry
        #populate user records
        querystr = "SELECT p.person_id, p.email FROM persons as p, person_site as ps WHERE p.person_id = ps.person_id AND  ps.site_id = "+str(site_id)
        users = cnx.query(querystr).dictresult()
        for user in users:
            new_hrn = person_to_user(user['email'])
            existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ").dictresult()
            if len(existing) > 0:
                new_hrn = person_to_user(user['email'], 1)
                existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ").dictresult()
                if len(existing) > 0:
                    new_hrn = person_to_user(user['email'], 2)
            cnx.query("INSERT INTO "+tablename+"(hrn,type,wrapperurl,pointer) VALUES('"+new_hrn+"','user','local',"+str(user['person_id'])+")")
        #populate slice records
        querystr = "SELECT slice_id, name FROM slices WHERE site_id = "+str(site_id)
        slices = cnx.query(querystr).dictresult()
        for slice in slices:
            slcname = slice['name'].split('_')
            if slcname[len(slcname)-1] != 'deleted':
                new_hrn = plslice_to_slice(slice['name'])
                existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ").dictresult()
                if len(existing) > 0:
                    new_hrn = new_hrn+'-'+str(slice['slice_id'])
                cnx.query("INSERT INTO "+tablename+"(hrn,type,wrapperurl,pointer) VALUES('"+new_hrn+"','slice','local',"+str(slice['slice_id'])+")")
                
    if type == 'component': #component registry
        #populate node records
        querystr = "SELECT node_id, hostname FROM nodes WHERE site_id = "+str(site_id)
        nodes = cnx.query(querystr).dictresult()
        for node in nodes:
            new_hrn = plnode_to_node(node['hostname'], 0)
            existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ").dictresult()
            if len(existing) > 0:
                new_hrn = plnode_to_node(node['hostname'], 1)
                existing = cnx.query("SELECT * FROM "+tablename+" WHERE hrn = '"+new_hrn+"'; ").dictresult()
                if len(existing) > 0:
                    new_hrn = plnode_to_node(node['hostname'], 2)
            cnx.query("INSERT INTO "+tablename+"(hrn,type,wrapperurl,pointer) VALUES('"+new_hrn+"','node','local',"+str(node['node_id'])+")")
        
