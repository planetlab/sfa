# record.py
#
# implements support for geni records
#
# TODO: Use existing PLC database methods? or keep this separate?

import report

# Record is a tuple (Name, GID, Type, Info)
#    info is comprised of the following sub-fields
#        pointer = a pointer to the record in the PL database
#        pl_info = planetlab-specific info (when talking to client)
#        geni_info = geni-specific info (when talking to client)

class GeniRecord():
    def __init__(self, name=None, gid=None, type=None, pointer=None, dict=None):
        self.dirty = True
        self.pl_info = None
        self.geni_info = None
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
            if "pl_info" in dict:
               self.set_pl_info(dict["pl_info"])
            if "geni_info" in dict:
               self.set_geni_info(dict["geni_info"])

    def set_name(self, name):
        self.name = name
        self.dirty = True

    def set_gid(self, gid):
        if isinstance(gid, str):
            self.gid = gid
        else:
            self.gid = gid.save_to_string(save_parents=True)
        self.dirty = True

    def set_type(self, type):
        self.type = type
        self.dirty = True

    def set_pointer(self, pointer):
        self.pointer = pointer
        self.dirty = True

    def set_pl_info(self, pl_info):
        self.pl_info = pl_info
        self.dirty = True

    def set_geni_info(self, geni_info):
        self.geni_info = geni_info
        self.dirty = True

    def get_pl_info(self):
        if self.pl_info:
            return self.pl_info
        else:
            return {}

    def get_geni_info(self):
        if self.geni_info:
            return self.geni_info
        else:
            return {}

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_pointer(self):
        return self.pointer

    # TODO: not the best name for the function, because we have things called gidObjects in the Cred
    def get_gid_object(self):
        return GID(string=self.gid)

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
            dict[name] = getattr(self, name)

        if self.pl_info:
            dict['pl_info'] = self.pl_info

        if self.geni_info:
            dict['geni_info'] = self.geni_info

        return dict

    def dump(self, dump_parents=False):
        print "RECORD", self.name
        print "        hrn:", self.name
        print "       type:", self.type
        print "        gid:"
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


