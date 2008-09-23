import tempfile
import os

import sys

from cert import *
from gid import *
from geniserver import *
from excep import *
from trustedroot import *
from misc import *
from record import *
from geniticket import *

import accounts
import database
import sm
import database


class ComponentManager(GeniServer):
    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.stop_slice)
        self.server.register_function(self.start_slice)
        self.server.register_function(self.reset_slice)
        self.server.register_function(self.delete_slice)
        self.server.register_function(self.list_slices)
        self.server.register_function(self.redeem_ticket)
        self.server.register_function(self.reboot)

    # Slice Interface

    def stop_slice(self, cred_str):
        self.decode_authentication(cred_str, "stopslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "stopslice:", slicename
        accounts.get(slicename).start()

    def start_slice(self, cred_str):
        self.decode_authentication(cred_str, "startslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "startslice:", slicename
        accounts.get(slicename).start()

    def reset_slice(self, cred_str):
        self.decode_authentication(cred_str, "resetslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "resetslice:", slicename

        # find the existing record for the slice
        try:
            rec = database.db[slicename]
        except KeyError:
            raise SliverDoesNotExist(slicename)

        accounts.get(slicename).stop()
        accounts.get(slicename).ensure_destroyed()
        accounts.get(slicename).ensure_created(rec)

    def delete_slice(self, cred_str):
        self.decode_authentication(cred_str, "deleteslice")
        slicename = hrn_to_pl_slicename(self.object_gid.get_hrn())
        print "deleteslice:", slicename
        accounts.get(slicename).ensure_destroyed()

    # this is similar to geniserver.decode_authentication
    def decode_ticket(self, ticket_string):
        self.client_ticket = Ticket(string = ticket_string)
        self.client_gid = self.client_ticket.get_gid_caller()
        self.object_gid = self.client_ticket.get_gid_object()

        # make sure the client_gid is not blank
        if not self.client_gid:
            raise MissingCallerGID(self.client_ticket.get_subject())

        # make sure the client_gid matches the certificate that the client is using
        peer_cert = self.server.peer_cert
        if not peer_cert.is_pubkey(self.client_gid.get_pubkey()):
            raise ConnectionKeyGIDMismatch(self.client_gid.get_subject())

        if self.trusted_cert_list:
            self.client_ticket.verify_chain(self.trusted_cert_list)
            if self.client_gid:
                self.client_gid.verify_chain(self.trusted_cert_list)
            if self.object_gid:
                self.object_gid.verify_chain(self.trusted_cert_list)

    def geni_ticket_to_plc_rec(self, ticket):
        ticket_attrs = ticket.get_attributes()
        ticket_rspec = ticket.get_rspec()
        rec = {}

        rec["name"] = ticket_attrs.get("name")
        rec["keys"] = '\n'.join(ticket_attrs.get("keys",[]))
        rec["initscript"] = ticket_attrs.get("initscript", "")
        rec["vref"] = ticket_attrs.get("vref", "default")
        rec["timestamp"] = ticket_attrs.get("timestamp")    # should there be a default timestamp?

        rspec = {}
        rec['rspec'] = rspec
        for resname, default_amt in sm.DEFAULT_ALLOCATION.iteritems():
            try:
                t = type(default_amt)
                amt = t.__new__(t, ticket_attrs[resname])
            except (KeyError, ValueError):
                amt = default_amt
            rspec[resname] = amt

        return rec

    def redeem_ticket(self, ticket_str):
        self.decode_ticket(ticket_str)
        ticket = self.client_ticket

        print "ticket received for", self.object_gid.get_hrn()

        rec = self.geni_ticket_to_plc_rec(ticket)

        print "record", rec

        database.db.deliver_record(rec)

    # Slice Information

    def list_slices(self, cred_str):
        self.decode_authentication(cred_str, "listslices")
        slice_names = database.db.keys()
        return slice_names

    # Management Interface

    def reboot(self, cred_str):
        self.decode_authentication(cred_str, "reboot")
        system("/sbin/reboot")


if __name__ == "__main__":
    global TrustedRoots

    key_file = "component.key"
    cert_file = "component.cert"

    # if no key is specified, then make one up
    if (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        key = Keypair(create=True)
        key.save_to_file(key_file)

        cert = Certificate(subject="component")
        cert.set_issuer(key=key, subject="component")
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    TrustedRoots = TrustedRootList()

    # XXX: does this conflict with the nodemanager's database? I don't think
    # so because there are locks, but double check...
    database.start()

    s = ComponentManager("", 12345, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

