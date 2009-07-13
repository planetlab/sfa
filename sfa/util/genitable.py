# genitable.py
#
# implements support for geni records stored in db tables
#
# TODO: Use existing PLC database methods? or keep this separate?

### $Id$
### $URL$

import report

from pg import DB, ProgrammingError

from sfa.trust.gid import *
from sfa.util.record import *
from sfa.util.debug import *

class GeniTable:

    GENI_TABLE_PREFIX = "sfa$"

    def __init__(self, create=False, hrn="unspecified.default.registry", cninfo=None):

        self.hrn = hrn

        # pgsql doesn't like table names with "." in them, to replace it with "$"
        self.tablename = GeniTable.GENI_TABLE_PREFIX + self.hrn.replace(".", "$")

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
                hrn text, \
                gid text, \
                type text, \
                pointer integer, \
                date_created timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                last_updated timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP);"
        template = "CREATE INDEX %s_%s_idx ON %s (%s);"
        indexes = [template % ( self.tablename, field, self.tablename, field) \
                   for field in ['key', 'hrn', 'type','pointer']]
        # IF EXISTS doenst exist in postgres < 8.2
        try:
            self.cnx.query('DROP TABLE IF EXISTS ' + self.tablename)
        except ProgrammingError:
            try:
                self.cnx.query('DROP TABLE ' + self.tablename)
            except ProgrammingError:
                pass
        
        self.cnx.query(querystr)
        for index in indexes:
            self.cnx.query(index)

    def remove(self, record):
        query_str = "DELETE FROM " + self.tablename + " WHERE key = '" + record.get_key() + "'"
        self.cnx.query(query_str)

    def insert(self, record):
        dont_insert = ['date_created', 'last_updated']
        fields = [field for field in  record.fields.keys() if field not in dont_insert]  
        fieldnames = ["key"] + fields
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
        for result in result_dict_list:
            if result['type'] in ['authority']:
                result_rec_list.append(AuthorityRecord(dict=result))
            elif result['type'] in ['node']:
                result_rec_list.append(NodeRecord(dict=result))
            elif result['type'] in ['slice']:
                result_rec_list.append(SliceRecord(dict=result))
            elif result['type'] in ['user']:
                result_rec_list.append(UserRecord(dict=result))
            else:
                result_rec_list.append(GeniRecord(dict=result))
        return result_rec_list

    def resolve_dict(self, type, hrn):
        return self.find_dict(type, hrn, "hrn")

    def resolve(self, type, hrn):
        return self.find(type, hrn, "hrn")

    def list_dict(self):
        query_str = "SELECT * FROM " + self.tablename
        result_dict_list = self.cnx.query(query_str).dictresult()
        return result_dict_list

    def list(self):
        result_dict_list = self.list_dict()
        result_rec_list = []
        for dict in result_dict_list:
            result_rec_list.append(GeniRecord(dict=dict).as_dict())
        return result_rec_list

    @staticmethod
    def geni_records_purge(cninfo):

        cnx = DB(cninfo['dbname'], cninfo['address'], 
                 port=cninfo['port'], user=cninfo['user'], passwd=cninfo['password'])
        tableList = cnx.get_tables()
        for table in tableList:
            if table.startswith(GeniTable.GENI_TABLE_PREFIX) or \
                    table.startswith('public.' + GeniTable.GENI_TABLE_PREFIX) or \
                    table.startswith('public."' + GeniTable.GENI_TABLE_PREFIX):
                report.trace("dropping table " + table)
                cnx.query("DROP TABLE " + table)
