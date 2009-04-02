##
# Implements support for geni records
#
# TODO: Use existing PLC database methods? or keep this separate?
##

import report
from types import StringTypes
from gid import *
from geni.util.rspec import *
##
# The GeniRecord class implements a Geni Record. A GeniRecord is a tuple
# (Name, GID, Type, Info).
#
# Name specifies the HRN of the object
# GID is the GID of the object
# Type is user | sa | ma | slice | component
#
# Info is comprised of the following sub-fields
#        pointer = a pointer to the record in the PL database
#        pl_info = planetlab-specific info (when talking to client)
#        geni_info = geni-specific info (when talking to client)
#
# The pointer is interpreted depending on the type of the record. For example,
# if the type=="user", then pointer is assumed to be a person_id that indexes
# into the persons table.
#
# A given HRN may have more than one record, provided that the records are
# of different types. For example, planetlab.us.arizona may have both an SA
# and a MA record, but cannot have two SA records.

class GeniRecord:

    ##
    # Create a Geni Record
    #
    # @param name if !=None, assign the name of the record
    # @param gid if !=None, assign the gid of the record
    # @param type one of user | sa | ma | slice | component
    # @param pointer is a pointer to a PLC record
    # @param dict if !=None, then fill in this record from the dictionary

    def __init__(self, name=None, gid=None, type=None, pointer=None, dict=None, string=None):
        self.dirty = True
        self.pl_info = None
        self.geni_info = None
        self.name = None
        self.gid = None
        self.type = None
        self.pointer = None
        if name:
            self.set_name(name)
        if gid:
            self.set_gid(gid)
        if type:
            self.set_type(type)
        if pointer:
            self.set_pointer(pointer)
        if dict:
            self.load_from_dict(dict)
        if string:
            self.load_from_string(string)

    ##
    # Set the name of the record
    #
    # @param name is a string containing the HRN

    def set_name(self, name):
        self.name = name
        self.dirty = True

    ##
    # Set the GID of the record
    #
    # @param gid is a GID object or the string representation of a GID object

    def set_gid(self, gid):
        if isinstance(gid, StringTypes):
            self.gid = gid
        else:
            self.gid = gid.save_to_string(save_parents=True)
        self.dirty = True

    ##
    # Set the type of the record
    #
    # @param type is a string: user | sa | ma | slice | component

    def set_type(self, type):
        self.type = type
        self.dirty = True

    ##
    # Set the pointer of the record
    #
    # @param pointer is an integer containing the ID of a PLC record

    def set_pointer(self, pointer):
        self.pointer = pointer
        self.dirty = True

    ##
    # Set the PLC info of the record
    #
    # @param pl_info is a dictionary containing planetlab info

    def set_pl_info(self, pl_info):
        self.pl_info = pl_info
        self.dirty = True

    ##
    # Set the geni info the record
    #
    # @param geni_info is a dictionary containing geni info

    def set_geni_info(self, geni_info):
        self.geni_info = geni_info
        self.dirty = True

    ##
    # Return the pl_info of the record, or an empty dictionary if none exists

    def get_pl_info(self):
        if self.pl_info:
            return self.pl_info
        else:
            return {}

    ##
    # Return the geni_info of the record, or an empty dictionary if none exists

    def get_geni_info(self):
        if self.geni_info:
            return self.geni_info
        else:
            return {}

    ##
    # Return the name (HRN) of the record

    def get_name(self):
        return self.name

    ##
    # Return the type of the record

    def get_type(self):
        return self.type

    ##
    # Return the pointer of the record. The pointer is an integer that may be
    # used to look up the record in the PLC database. The evaluation of pointer
    # depends on the type of the record

    def get_pointer(self):
        return self.pointer

    ##
    # Return the GID of the record, in the form of a GID object
    # TODO: not the best name for the function, because we have things called
    # gidObjects in the Cred

    def get_gid_object(self):
        return GID(string=self.gid)

    ##
    # Return a key that uniquely identifies this record among all records in
    # Geni. This key is used to uniquely identify the record in the Geni
    # database.

    def get_key(self):
        return self.name + "#" + self.type

    ##
    # Returns a list of field names in this record. pl_info, geni_info are not
    # included because they are not part of the record that is stored in the
    # database, but are rather computed values from other entities

    def get_field_names(self):
        return ["name", "gid", "type", "pointer"]

    ##
    # Given a field name ("name", "gid", ...) return the value of that field.
    #
    # @param name is the name of field to be returned

    def get_field_value_string(self, fieldname):
        if fieldname == "key":
            val = self.get_key()
        else:
            val = getattr(self, fieldname)
        if isinstance(val, str):
            return "'" + str(val) + "'"
        else:
            return str(val)

    ##
    # Given a list of field names, return a list of values for those fields.
    #
    # @param fieldnames is a list of field names

    def get_field_value_strings(self, fieldnames):
        strs = []
        for fieldname in fieldnames:
            strs.append(self.get_field_value_string(fieldname))
        return strs

    ##
    # Return the record in the form of a dictionary

    def as_dict(self):
        dict = {}
        names = self.get_field_names()
        for name in names:
            dict[name] = getattr(self, name)

        if self.pl_info:
            dict['pl_info'] = self.pl_info

        if self.geni_info:
            dict['geni_info'] = self.geni_info

        return dict

    ##
    # Load the record from a dictionary
    #
    # @param dict dictionary to load record fields from

    def load_from_dict(self, dict):
        self.set_name(dict['name'])
        gidstr = dict.get("gid", None)
        if gidstr:
            self.set_gid(dict['gid'])

        self.set_type(dict['type'])
        self.set_pointer(dict['pointer'])
        if "pl_info" in dict:
           self.set_pl_info(dict["pl_info"])
        if "geni_info" in dict:
           self.set_geni_info(dict["geni_info"])

    ##
    # Save the record to a string. The string contains an XML representation of
    # the record.

    def save_to_string(self):

        dict = self.as_dict()
        record = RecordSpec()
        record.parseDict(dict)
        str = record.toxml()
        #str = xmlrpclib.dumps((dict,), allow_none=True)
        return str

    ##
    # Load the record from a string. The string is assumed to contain an XML
    # representation of the record.

    def load_from_string(self, str):
        #dict = xmlrpclib.loads(str)[0][0]
        
        record = RecordSpec()
        record.parseString(str)
        record_dict = record.toDict()
        geni_dict = record_dict['record']
        self.load_from_dict(geni_dict)

    ##
    # Dump the record to stdout
    #
    # @param dump_parents if true, then the parents of the GID will be dumped

    def dump(self, dump_parents=False):
        print "RECORD", self.name
        print "        hrn:", self.name
        print "       type:", self.type
        print "        gid:"
        if (not self.gid):
            print "        None"
        else:
            self.get_gid_object().dump(8, dump_parents)
        print "    pointer:", self.pointer

        print "  geni_info:"
        geni_info = getattr(self, "geni_info", {})
        if geni_info:
            for key in geni_info.keys():
                print "       ", key, ":", geni_info[key]

        print "    pl_info:"
        pl_info = getattr(self, "pl_info", {})
        if pl_info:

            for key in pl_info.keys():
                print "       ", key, ":", pl_info[key]


    def getdict(self):
        info = {'hrn': self.name, 'type': self.type, 'gid': self.gid}
        info.update(getattr(self, "geni_info", {}))
        info.update(getattr(self, "pl_info", {}))
        return info
