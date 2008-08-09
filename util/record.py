# record.py
#
# implements support for geni records
#
# TODO: Use existing PLC database methods? or keep this separate?

from pg import DB

GENI_TABLE_PREFIX = "geni$"

# Record is a tuple (Name, GID, Type, Info)
#    info is implemented as a pointer to a PLC record

class GeniRecord():
    def __init__(self, name=None, gid=None, type=None, pointer=None, dict=None):
        self.dirty=True
        if name:
            self.set_name(name)
        if gid:
            self.set_gid(gid)
        if type:
            self.set_type(type)
        if pointer:
            self.set_pointer(pointer)
        if dict:
            self.set_name(dict['name'])
            self.set_gid(dict['gid'])
            self.set_type(dict['type'])
            self.set_pointer(dict['pointer'])

    def set_name(self, name):
        self.name = name
        self.dirty = True

    def set_gid(self, gid):
        self.gid = gid
        self.dirty = True

    def set_type(self, type):
        self.type = type
        self.dirty = True

    def set_pointer(self, pointer):
        self.pointer = pointer
        self.dirty = True

    def get_key(self):
        return self.name + "#" + self.type

    def get_field_names(self):
        return ["name", "gid", "type", "pointer"]

    def get_field_value_string(self, fieldname):
        if fieldname == "key":
            val = self.get_key()
        else:
            val = getattr(self, fieldname)
        if isinstance(val, str):
            return "'" + str(val) + "'"
        else:
            return str(val)

    def get_field_value_strings(self, fieldnames):
        strs = []
        for fieldname in fieldnames:
            strs.append(self.get_field_value_string(fieldname))
        return strs

    def as_dict(self):
        dict = {}
        names = self.get_field_names()
        for name in names:
            dict[name] = self.getattr(name)
        return dict

# GeniTable
#
# Represents a single table on a registry for a single authority.

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

    def create(self):
        querystr = "CREATE TABLE " + self.tablename + " ( \
                key text, \
                name text, \
                gid text, \
                type text, \
                pointer integer);"

        self.cnx.query('DROP TABLE IF EXISTS ' + self.tablename)
        self.cnx.query(querystr)

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

    def resolve_raw(self, type, hrn):
        query_str = "SELECT * FROM " + self.tablename + " WHERE name = '" + hrn + "'"
        dict_list = self.cnx.query(query_str).dictresult()
        result_dict_list = []
        for dict in dict_list:
           if (type=="*") or (dict['type'] == type):
               result_dict_list.append(dict)
        return result_dict_list

    def resolve(self, type, hrn):
        result_dict_list = self.resolve_raw(type, hrn)
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
        if table.startswith(GENI_TABLE_PREFIX):
            cnx.query("DROP TABLE " + table)
