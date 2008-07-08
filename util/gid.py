from cert import *
import uuid
import xmlrpclib

# GID is a tuplie:
#    (uuid, hrn, public_key)

def create_uuid():
    return str(uuid.uuid4().int)

class GID(Certificate):
    uuid = None
    hrn = None

    def __init__(self, create=False, subject=None, string=None, filename=None, uuid=None, hrn=None):
        Certificate.__init__(self, create, subject, string, filename)
        if uuid:
            self.uuid = uuid
        if hrn:
            self.hrn = hrn

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        if not self.uuid:
            self.decode()
        return self.uuid

    def set_hrn(self, hrn):
        self.hrn = hrn

    def get_hrn(self):
        if not self.hrn:
            self.decode()
        return self.hrn

    def encode(self):
        dict = {"uuid": self.uuid,
                "hrn": self.hrn}
        str = xmlrpclib.dumps((dict,))
        self.set_data(str)

    def decode(self):
        data = self.get_data()
        if data:
            dict = xmlrpclib.loads(self.get_data())[0][0]
        else:
            dict = {}
            
        self.uuid = dict.get("uuid", None)
        self.hrn = dict.get("hrn", None)



