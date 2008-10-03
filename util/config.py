##
# Geniwrapper Configuration Info
#
# This module holds configuration parameters for geniwrapper. There are two
# main pieces of information that are used: the database connection and
# the PLCAPI connection
##

##
# Geniwrapper uses a MYSQL database to store records. This database may be
# co-located with the PLC database, or it may be a separate database. The
# following parameters define the connection to the database.
#
# Note that Geniwrapper does not access any of the PLC databases directly via
# a mysql connection; All PLC databases are accessed via PLCAPI.

def get_default_dbinfo():
    dbinfo={}
    dbinfo['dbname'] = 'planetlab4'
    dbinfo['address'] = 'localhost'
    dbinfo['port'] = 5432
    dbinfo['user'] = 'pgsqluser'
    dbinfo['password'] = '4c77b272-c892-4bdf-a833-dddeeee1a2ed'

    return dbinfo

##
# Geniwrapper uses a PLCAPI connection to perform operations on the registry,
# such as creating and deleting slices. This connection requires an account
# on the PLC server with full administrator access.
#
# The Url parameter controls whether the connection uses PLCAPI directly (i.e.
# Geniwrapper is located on the same machine as PLC), or uses a XMLRPC connection
# to the PLC machine. If you wish to use the API directly, then remove the Url
# field from the dictionary. 

def get_pl_auth():
    pl_auth = {'Username': 'root@198.0.0.132',
    'AuthMethod': 'password',
    'AuthString':  'root',
    "Url": "https://localhost:443/PLCAPI/"
    }

    return pl_auth
