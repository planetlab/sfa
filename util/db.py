import os
from pg import DB
from excep import *
from tree import *
from util import *

#planetlab authentication structure
pl_auth = {'Username': 'ssevinc@princeton.edu',        # User account
'AuthMethod': 'password',        # Type of auth this is. Can be password, session ...
'AuthString':  'Ss3928Ee' # the password for this account
} 

def get_plDB_conn():
    dbname = 'plDB'
    address = 'localhost'
    port = 5433
    user = 'postgres'
    password = '111'
    cnx = DB(dbname, address, port=port, user=user, passwd=password)
    return cnx
    
#copy the pl db info to requester
def get_plDB_info(dst):
    dst.db_name = 'plDB'
    dst.address = 'localhost'
    dst.port = 5433
    dst.user = 'postgres'
    dst.password = '111'


#determines the database info of a given hrn
#if the hrn does not exist in the tree hierarchy None is returned
def determine_dbinfo(hrn, tree):
    info = tree.tree_lookup(hrn)
    if info == None:
        return None
    else:
        db_info = info.node_data['db_info']
        cnx = DB(db_info.db_name, db_info.address, port = db_info.port, user = db_info.user, passwd = db_info.password)
        tablename = db_info.table_name
        return [cnx, tablename]

#convert the parameter list to query string suitable for supplying to database queries
#input: query type, table name and field-value pairs
def generate_querystr(type, table, dict):
    querystr = ""
    if type == 'INSERT':
        keys = dict.keys()
        str1 = keys[0]
        for i in range(1, len(keys)):
            str1 = str1 + ','+ keys[i]
        str2 = ""
        for i in range(len(keys)-1):
            if isinstance(dict[keys[i]],str):
                str2 = str2 + "'" + dict[keys[i]] + "', " 
            else:
                str2 = str2 + str(dict[keys[i]]) + ", "
        if isinstance(dict[keys[len(keys)-1]],str):
            str2 = str2 + "'" + dict[keys[len(keys)-1]] + "'" 
        else:
            str2 = str2 + str(dict[keys[len(keys)-1]]) 
        querystr = "INSERT INTO "+table+ "(" + str1 + ") VALUES(" + str2 + ")"
    elif type == 'UPDATE':
        str1 = ""
        keys = dict.keys()
        for i in range(len(keys)-1):
            if keys[i] != 'hrn':
                if isinstance(dict[keys[i]],str):
                    str1 = str1 + keys[i] + " = '" + dict[keys[i]] + "', " 
                else:
                    str1 = str1 + keys[i] + " = " + dict[keys[i]] + ", " 
        if keys[len(keys)-1] != 'hrn':
            if isinstance(dict[keys[len(keys)-1]],str):
                str1 = str1 + keys[len(keys)-1] + " = '" + dict[keys[len(keys)-1]] + "'" 
            else:
                str1 = str1 + keys[len(keys)-1] + " = '" + dict[keys[len(keys)-1]]
        querystr = "UPDATE "+table+ " SET " + str1 + " WHERE hrn = '"+get_leaf(dict["hrn"])+"'"
    elif type == 'DELETE':
        querystr = "DELETE FROM "+table+" WHERE hrn = '"+get_leaf(dict["hrn"])+"'"
    return querystr
            
