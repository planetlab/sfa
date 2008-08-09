# config.py
#
# geniwrapper configuration info
#
# this module holds configuration parameters for geniwrapper. The wrapper
# needs an account to connect to PLC with and a database to store geni
# tables

def get_default_dbinfo():
    dbinfo={}
    dbinfo['dbname'] = 'planetlab4'
    dbinfo['address'] = 'localhost'
    dbinfo['port'] = 5432
    dbinfo['user'] = 'pgsqluser'
    dbinfo['password'] = '4c77b272-c892-4bdf-a833-dddeeee1a2ed'

    return dbinfo


