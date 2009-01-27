# genitable.py
#
# implements support for geni records stored in db tables
#
# TODO: Use existing PLC database methods? or keep this separate?

import report

from pg import DB
from gid import *
from record import *

GENI_TABLE_PREFIX = "geni$"

class GeniTable():
    def __init__(self, create=False, hrn="unspecified.default.registry", cninfo=None):
        global GENI_TABLE_PREFIX

        self.hrn = hrn

        # pgsql doesn't like table names with "." in them, to replace it with "$"
        self.tablename = GENI_TABLE_PREFIX + self.hrn.replace(".", "$")

        # establish a connection to the pgsql server
        self.cnx = DB(cninfo['dbname'], cninfo['address'], port=cninfo['port'], user=cninfo['user'], passwd=cninfo['password'])

        # if asked to create the table, then create it
        if create:
            self.create()

    def exists(self):
        tableList = self.cnx.get_tables()
        if 'public.' + self.tablename in tableList:
            return True
        if 'public."' + self.tablename + '"' in tableList:
            return True
        return False

    def create(self):
        querystr = "CREATE TABLE " + self.tablename + " ( \
                key text, \
                name text, \
                gid text, \
                type text, \
                pointer integer);"

        self.cnx.query('DROP TABLE IF EXISTS ' + self.tablename)
        self.cnx.query(querystr)

    def remove(self, record):
        query_str = "DELETE FROM " + self.tablename + " WHERE key = '" + record.get_key() + "'"
        self.cnx.query(query_str)

    def insert(self, record):
        fieldnames = ["key"] + record.get_field_names()
        fieldvals = record.get_field_value_strings(fieldnames)
        query_str = "INSERT INTO " + self.tablename + \
                       "(" + ",".join(fieldnames) + ") " + \
                       "VALUES(" + ",".join(fieldvals) + ")"
        #print query_str
        self.cnx.query(query_str)

    def update(self, record):
        names = record.get_field_names()
        pairs = []
        for name in names:
           val = record.get_field_value_string(name)
           pairs.append(name + " = " + val)
        update = ", ".join(pairs)

        query_str = "UPDATE " + self.tablename+ " SET " + update + " WHERE key = '" + record.get_key() + "'"
        #print query_str
        self.cnx.query(query_str)

    def find_dict(self, type, value, searchfield):
        query_str = "SELECT * FROM " + self.tablename + " WHERE " + searchfield + " = '" + str(value) + "'"
        dict_list = self.cnx.query(query_str).dictresult()
        result_dict_list = []
        for dict in dict_list:
           if (type=="*") or (dict['type'] == type):
               result_dict_list.append(dict)
        return result_dict_list

    def find(self, type, value, searchfield):
        result_dict_list = self.find_dict(type, value, searchfield)
        result_rec_list = []
        for dict in result_dict_list:
            result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

    def resolve_dict(self, type, hrn):
        return self.find_dict(type, hrn, "name")

    def resolve(self, type, hrn):
        return self.find(type, hrn, "name")

    def list_dict(self):
        query_str = "SELECT * FROM " + self.tablename
        result_dict_list = self.cnx.query(query_str).dictresult()
        return result_dict_list

    def list(self):
        result_dict_list = self.list_dict()
        result_rec_list = []
        for dict in result_dict_list:
            result_rec_list.append(GeniRecord(dict=dict))
        return result_rec_list

def set_geni_table_prefix(x):
    global GENI_TABLE_PREFIX

    GENI_TABLE_PREFIX = x

def geni_records_purge(cninfo):
    global GENI_TABLE_PREFIX

    cnx = DB(cninfo['dbname'], cninfo['address'], port=cninfo['port'], user=cninfo['user'], passwd=cninfo['password'])
    tableList = cnx.get_tables()
    for table in tableList:
        if table.startswith(GENI_TABLE_PREFIX) or \
           table.startswith('public.' + GENI_TABLE_PREFIX) or \
           table.startswith('public."' + GENI_TABLE_PREFIX):
               report.trace("dropping table " + table)
               cnx.query("DROP TABLE " + table)
