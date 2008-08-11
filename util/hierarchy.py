# hierarchy.py
#
# hierarchy of GENI authorities
#
# This correspond's almost identically to the functionality of Soner's
# "tree" module. Each component of an HRN is stored in a different subdirectory.
# Inside this subdirectory are:
#      *.GID - GID file
#      *.PKEY - private key file
#      *.DBINFO - database info

import os
from cert import *
from gid import *
from misc import *
from config import *

class AuthInfo():
    hrn = None
    gid_filename = None
    privkey_filename = None
    dbinfo_filename = None

    def __init__(self, hrn, gid_filename, privkey_filename, dbinfo_filename):
        self.hrn = hrn
        self.gid_filename = gid_filename
        self.privkey_filename = privkey_filename
        self.dbinfo_filename = dbinfo_filename

    def get_gid_object(self):
        return GID(filename = self.gid_filename)

    def get_pkey_object(self):
        return Keypair(filename = self.privkey_filename)

    def get_dbinfo(self):
        f = file(self.dbinfo_filename)
        dict = eval(f.read())
        f.close()
        return dict

class Hierarchy():
    def __init__(self, basedir="."):
        self.basedir = basedir

    def get_auth_filenames(self, hrn):
        leaf = get_leaf(hrn)
        parent_hrn = get_authority(hrn)
        directory = os.path.join(self.basedir, hrn.replace(".", "/"))

        gid_filename = os.path.join(directory, leaf+".gid")
        privkey_filename = os.path.join(directory, leaf+".pkey")
        dbinfo_filename = os.path.join(directory, leaf+".dbinfo")

        return (directory, gid_filename, privkey_filename, dbinfo_filename)

    def auth_exists(self, hrn):
        (directory, gid_filename, privkey_filename, dbinfo_filename) = \
            self.get_auth_filenames(hrn)

        return os.path.exists(gid_filename) and \
               os.path.exists(privkey_filename) and \
               os.path.exists(dbinfo_filename)

    def create_auth(self, hrn):
        (directory, gid_filename, privkey_filename, dbinfo_filename) = \
            self.get_auth_filenames(hrn)

        # create the directory to hold the files
        try:
            os.makedirs(directory)
        # if the path already exists then pass
        except OSError, (errno, strerr):
            if errno == 17:
                pass

        pkey = Keypair(create = True)
        pkey.save_to_file(privkey_filename)

        gid = self.create_gid(hrn, create_uuid(), pkey)
        gid.save_to_file(gid_filename)

        # XXX TODO: think up a better way for the dbinfo to work

        dbinfo = get_default_dbinfo()
        dbinfo_file = file(dbinfo_filename, "w")
        dbinfo_file.write(str(dbinfo))
        dbinfo_file.close()

    def get_auth_info(self, hrn, can_create=True):
        if not self.auth_exists(hrn):
            if not can_create:
                return MissingAuthority(hrn)

            self.create_auth(hrn)

        (directory, gid_filename, privkey_filename, dbinfo_filename) = \
            self.get_auth_filenames(hrn)

        auth_info = AuthInfo(hrn, gid_filename, privkey_filename, dbinfo_filename)

        return auth_info

    def create_gid(self, hrn, uuid, pkey):
        parent_hrn = get_authority(hrn)

        gid = GID(subject=hrn, uuid=uuid)

        if not parent_hrn:
            # if there is no parent hrn, then it must be self-signed. this
            # is where we terminate the recursion
            gid.set_issuer(pkey, hrn)
        else:
            # we need the parent's private key in order to sign this GID
            parent_auth_info = self.get_auth_info(parent_hrn)
            gid.set_issuer(parent_auth_info.get_pkey_object(), parent_auth_info.hrn)
            gid.set_parent(parent_auth_info.get_gid_object())

        gid.set_pubkey(pkey)
        gid.sign()

        return gid

    def refresh_gid(self, gid, hrn=None, uuid=None, pubkey=None):
        # TODO: compute expiration time of GID, refresh it if necessary
        gid_is_expired = False

        # update the gid if we need to
        if gid_is_expired or hrn or uuid or pubkey:
            if not hrn:
                hrn = gid.get_hrn()
            if not uuid:
                uuid = gid.get_uuid()
            if not pubkey:
                pubkey = gid.get_pubkey()

            gid = self.create_gid(hrn, uuid, pubkey)

        return gid

