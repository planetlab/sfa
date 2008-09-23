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
import report
from cert import *
from credential import *
from gid import *
from misc import *
from config import *
from geniticket import *

class AuthInfo():
    hrn = None
    gid_object = None
    gid_filename = None
    privkey_filename = None
    dbinfo_filename = None

    def __init__(self, hrn, gid_filename, privkey_filename, dbinfo_filename):
        self.hrn = hrn
        self.set_gid_filename(gid_filename)
        self.privkey_filename = privkey_filename
        self.dbinfo_filename = dbinfo_filename

    def set_gid_filename(self, fn):
        self.gid_filename = fn
        self.gid_object = None

    def get_gid_object(self):
        if not self.gid_object:
            self.gid_object = GID(filename = self.gid_filename)
        return self.gid_object

    def get_pkey_object(self):
        return Keypair(filename = self.privkey_filename)

    def get_dbinfo(self):
        f = file(self.dbinfo_filename)
        dict = eval(f.read())
        f.close()
        return dict

    def update_gid_object(self, gid):
        gid.save_to_file(self.gid_filename)
        self.gid_object = gid

class Hierarchy():
    def __init__(self, basedir="."):
        self.basedir = os.path.join(basedir, "authorities")

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

    def create_auth(self, hrn, create_parents=False):
        report.trace("Hierarchy: creating authority: " + hrn)

        # create the parent authority if necessary
        parent_hrn = get_authority(hrn)
        if (parent_hrn) and (not self.auth_exists(parent_hrn)) and (create_parents):
            self.create_auth(parent_hrn, create_parents)

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
        gid.save_to_file(gid_filename, save_parents=True)

        # XXX TODO: think up a better way for the dbinfo to work

        dbinfo = get_default_dbinfo()
        dbinfo_file = file(dbinfo_filename, "w")
        dbinfo_file.write(str(dbinfo))
        dbinfo_file.close()

    def get_auth_info(self, hrn):
        #report.trace("Hierarchy: getting authority: " + hrn)

        if not self.auth_exists(hrn):
            raise MissingAuthority(hrn)

        (directory, gid_filename, privkey_filename, dbinfo_filename) = \
            self.get_auth_filenames(hrn)

        auth_info = AuthInfo(hrn, gid_filename, privkey_filename, dbinfo_filename)

        # check the GID and see if it needs to be refreshed
        gid = auth_info.get_gid_object()
        gid_refreshed = self.refresh_gid(gid)
        if gid != gid_refreshed:
            auth_info.update_gid_object(gid_refreshed)

        return auth_info

    def create_gid(self, hrn, uuid, pkey):
        gid = GID(subject=hrn, uuid=uuid, hrn=hrn)

        parent_hrn = get_authority(hrn)
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
        gid.encode()
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

    def get_auth_cred(self, hrn):
        auth_info = self.get_auth_info(hrn)
        gid = auth_info.get_gid_object()

        cred = Credential(subject=hrn)
        cred.set_gid_caller(gid)
        cred.set_gid_object(gid)
        cred.set_privileges("authority")
        cred.set_delegate(True)
        cred.set_pubkey(auth_info.get_gid_object().get_pubkey())

        parent_hrn = get_authority(hrn)
        if not parent_hrn:
            # if there is no parent hrn, then it must be self-signed. this
            # is where we terminate the recursion
            cred.set_issuer(auth_info.get_pkey_object(), hrn)
        else:
            # we need the parent's private key in order to sign this GID
            parent_auth_info = self.get_auth_info(parent_hrn)
            cred.set_issuer(parent_auth_info.get_pkey_object(), parent_auth_info.hrn)
            cred.set_parent(self.get_auth_cred(parent_hrn))

        cred.encode()
        cred.sign()

        return cred

    # this looks almost the same as get_auth_cred, but works for tickets
    # XXX does similarity imply there should be more code re-use?
    def get_auth_ticket(self, hrn):
        auth_info = self.get_auth_info(hrn)
        gid = auth_info.get_gid_object()

        ticket = Ticket(subject=hrn)
        ticket.set_gid_caller(gid)
        ticket.set_gid_object(gid)
        ticket.set_delegate(True)
        ticket.set_pubkey(auth_info.get_gid_object().get_pubkey())

        parent_hrn = get_authority(hrn)
        if not parent_hrn:
            # if there is no parent hrn, then it must be self-signed. this
            # is where we terminate the recursion
            ticket.set_issuer(auth_info.get_pkey_object(), hrn)
        else:
            # we need the parent's private key in order to sign this GID
            parent_auth_info = self.get_auth_info(parent_hrn)
            ticket.set_issuer(parent_auth_info.get_pkey_object(), parent_auth_info.hrn)
            ticket.set_parent(self.get_auth_cred(parent_hrn))

        ticket.encode()
        ticket.sign()

        return ticket

