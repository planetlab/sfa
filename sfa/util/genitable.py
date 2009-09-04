# genitable.py
#
# implements support for geni records stored in db tables
#
# TODO: Use existing PLC database methods? or keep this separate?

### $Id$
### $URL$

import report
import  pgdb
from pg import DB, ProgrammingError
from sfa.trust.gid import *
from sfa.util.record import *
from sfa.util.debug import *
from sfa.util.config import *
from sfa.util.filter import *

class GeniTable(list):

    GENI_TABLE_PREFIX = "sfa"

    def __init__(self, record_filter = None):

        # pgsql doesn't like table names with "." in them, to replace it with "$"
        self.tablename = GeniTable.GENI_TABLE_PREFIX

        # establish a connection to the pgsql server
        cninfo = Config().get_plc_dbinfo()     
        self.cnx = DB(cninfo['dbname'], cninfo['address'], port=cninfo['port'], user=cninfo['user'], passwd=cninfo['password'])

        if record_filter:
            records = self.find(record_filter)
            for record in reocrds:
                self.append(record)             

    def exists(self):
        tableList = self.cnx.get_tables()
        if 'public.' + self.tablename in tableList:
            return True
        if 'public."' + self.tablename + '"' in tableList:
            return True
        return False

    def create(self):
        
        querystr = "CREATE TABLE " + self.tablename + " ( \
                record_id serial PRIMARY KEY , \
                hrn text NOT NULL, \
                authority text NOT NULL, \
                gid text, \
                type text NOT NULL, \
                pointer integer, \
                date_created timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                last_updated timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP);"
        template = "CREATE INDEX %s_%s_idx ON %s (%s);"
        indexes = [template % ( self.tablename, field, self.tablename, field) \
                   for field in ['hrn', 'type', 'authority', 'pointer']]
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
        query_str = "DELETE FROM %s WHERE record_id = %s" % (self.tablename, record['record_id']) 
        self.cnx.query(query_str)

    def insert(self, record):
        dont_insert = ['date_created', 'last_updated']
        fields = [field for field in  record.fields.keys() if field not in dont_insert]  
        fieldnames = ["pointer"] + fields
        fieldvals = record.get_field_value_strings(fieldnames)
        query_str = "INSERT INTO " + self.tablename + \
                       "(" + ",".join(fieldnames) + ") " + \
                       "VALUES(" + ",".join(fieldvals) + ")"
        #print query_str
        self.cnx.query(query_str)

    def update(self, record):
        dont_update = ['date_created', 'last_updated']
        fields = [field for field in  record.fields.keys() if field not in dont_update]  
        fieldvals = record.get_field_value_strings(fields)
        pairs = []
        for field in fields:
            val = record.get_field_value_string(field)
            pairs.append(field + " = " + val)
        update = ", ".join(pairs)

        query_str = "UPDATE %s SET %s WHERE record_id = %s" % \
                    (self.tablename, update, record['record_id'])
        #print query_str
        self.cnx.query(query_str)

    def quote(self, value):
        """
        Returns quoted version of the specified value.
        """

        # The pgdb._quote function is good enough for general SQL
        # quoting, except for array types.
        if isinstance(value, (list, tuple, set)):
            return "ARRAY[%s]" % ", ".join(map, self.quote, value)
        else:
            return pgdb._quote(value)

    def find(self, record_filter = None):
        sql = "SELECT * FROM %s WHERE True " % self.tablename
        
        if isinstance(record_filter, (list, tuple, set)):
            ints = filter(lambda x: isinstance(x, (int, long)), record_filter)
            strs = filter(lambda x: isinstance(x, StringTypes), record_filter)
            record_filter = Filter(GeniRecord.all_fields, {'record_id': ints, 'hrn': strs})
            sql += "AND (%s) %s " % record_filter.sql("OR") 
        elif isinstance(record_filter, dict):
            record_filter = Filter(GeniRecord.all_fields, record_filter)        
            sql += " AND (%s) %s" % record_filter.sql("AND")
        elif isinstance(record_filter, StringTypes):
            record_filter = Filter(GeniRecord.all_fields, {'hrn':[record_filter]})    
            sql += " AND (%s) %s" % record_filter.sql("AND")
        elif isinstance(record_filter, int):
            record_filter = Filter(GeniRecord.all_fields, {'record_id':[record_filter]})    
            sql += " AND (%s) %s" % record_filter.sql("AND")
        results = self.cnx.query(sql).dictresult()
        return results

    def findObjects(self, record_filter = None):
        
        results = self.find(record_filter) 
        result_rec_list = []
        for result in results:
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


    def drop(self):
        try:
            self.cnx.query('DROP TABLE IF EXISTS ' + self.tablename)
        except ProgrammingError:
            try:
                self.cnx.query('DROP TABLE ' + self.tablename)
            except ProgrammingError:
                pass
    
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
