# credential.py
#
# implements GENI credentials
#
# Credentials are layered on top of certificates, and are essentially a
# certificate that stores a tuple of parameters.

from cert import *
from rights import *
from gid import *
import xmlrpclib

# Credential is a tuple:
#     (GIDCaller, GIDObject, LifeTime, Privileges, Delegate)
#
# These fields are encoded using xmlrpc into the subjectAltName field of the
# x509 certificate. Note: Call encode() once the fields have been filled in
# to perform this encoding.

class Credential(Certificate):
    gidCaller = None
    gidObject = None
    lifeTime = None
    privileges = None
    delegate = False

    def __init__(self, create=False, subject=None, string=None, filename=None):
        Certificate.__init__(self, create, subject, string, filename)

    def create_similar(self):
        return Credential()

    def set_gid_caller(self, gid):
        self.gidCaller = gid

    def get_gid_caller(self):
        if not self.gidCaller:
            self.decode()
        return self.gidCaller

    def set_gid_object(self, gid):
        self.gidObject = gid

    def get_gid_object(self):
        if not self.gidObject:
            self.decode()
        return self.gidObject

    def set_lifetime(self, lifeTime):
        self.lifeTime = lifeTime

    def get_lifetime(self):
        if not self.lifeTime:
            self.decode()
        return self.lifeTime

    def set_delegate(self, delegate):
        self.delegate = delegate

    def get_delegate(self):
        if not self.delegate:
            self.decode()
        return self.delegate

    def set_privileges(self, privs):
        if isinstance(privs, str):
            self.privileges = RightList(string = privs)
        else:
            self.privileges = privs

    def get_privileges(self):
        if not self.privileges:
            self.decode()
        return self.privileges

    def can_perform(self, op_name):
        rights = self.get_privileges()
        if not rights:
            return False
        return rights.can_perform(op_name)

    def encode(self):
        dict = {"gidCaller": None,
                "gidObject": None,
                "lifeTime": self.lifeTime,
                "privileges": None,
                "delegate": self.delegate}
        if self.gidCaller:
            dict["gidCaller"] = self.gidCaller.save_to_string(save_parents=True)
        if self.gidObject:
            dict["gidObject"] = self.gidObject.save_to_string(save_parents=True)
        if self.privileges:
            dict["privileges"] = self.privileges.save_to_string()
        str = xmlrpclib.dumps((dict,), allow_none=True)
        self.set_data(str)

    def decode(self):
        data = self.get_data()
        if data:
            dict = xmlrpclib.loads(self.get_data())[0][0]
        else:
            dict = {}

        self.lifeTime = dict.get("lifeTime", None)
        self.delegate = dict.get("delegate", None)

        privStr = dict.get("privileges", None)
        if privStr:
            self.privileges = RightList(string = privStr)
        else:
            self.privileges = None

        gidCallerStr = dict.get("gidCaller", None)
        if gidCallerStr:
            self.gidCaller = GID(string=gidCallerStr)
        else:
            self.gidCaller = None

        gidObjectStr = dict.get("gidObject", None)
        if gidObjectStr:
            self.gidObject = GID(string=gidObjectStr)
        else:
            self.gidObject = None

    def verify_chain(self, trusted_certs = None):
        # do the normal certificate verification stuff
        Certificate.verify_chain(self, trusted_certs)

        if self.parent:
            # make sure the parent delegated rights to the child
            if not self.parent.get_delegate():
                raise MissingDelegateBit(self.parent.get_subject())

            # XXX todo: make sure child rights are a subset of parent rights

        return

    def dump(self, dump_parents=False):
        print "CREDENTIAL", self.get_subject()

        print "      privs:", self.get_privileges().save_to_string()

        print "  gidCaller:"
        gidCaller = self.get_gid_caller()
        if gidCaller:
            gidCaller.dump(8, dump_parents)

        print "  gidObject:"
        gidObject = self.get_gid_object()
        if gidObject:
            gidObject.dump(8, dump_parents)

        print "   delegate:", self.get_delegate()

        if self.parent and dump_parents:
           print "PARENT",
           self.parent.dump(dump_parents)





