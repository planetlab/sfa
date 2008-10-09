##
# Gacks Server
##

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

from gacksexcep import *
from gackscalendar import *

##
# GacksServer is a GeniServer that serves component interface requests.
#

class GacksServer(GeniServer):

    ##
    # Create a new GacksServer object.
    #
    # @param ip the ip address to listen on
    # @param port the port to listen on
    # @param key_file private key filename of registry
    # @param cert_file certificate filename containing public key (could be a GID file)

    def __init__(self, ip, port, key_file, cert_file):
        GeniServer.__init__(self, ip, port, key_file, cert_file)

    ##
    # Register the server RPCs for Gacks

    def register_functions(self):
        GeniServer.register_functions(self)
        self.server.register_function(self.get_handle)

    def get_handle(self, rspec):
        handles = rspec_to_handles(rspec)
        return handles_to_strings(handles)

    def set_allocator(self, callerGID_str, handle_strs, allocatorGID_str, which, where, reqsig)
        callerGID = GID(callerGID_str)
        allocatorGID = GID(allocatorGID_str)

        # TODO: verify callerGID ssl key

        callerGID.verify_chain(self.trusted_cert_list)
        allocatorGID.verify_chain(self.trusted_cert_list)

        handles = strings_to_handles(handle_strs)
        for handle in handles:
            # find the existing records that overlap the handle
            existing_recs = self.calendar.query_handles([handle])

            if not existing_recs:
                raise GacksResourceNotFound(hand.as_string())

            # TODO: Merge existing_recs

            for item in existing_recs:
                if not item.contains_allocator(callerGID->get_name()):
                    raise CallerNotAllocator(item.as_string())
                if not item.is_superset(handle):
                    raise RequestSpansReservations(handle.as_string() + " on " + item.as_string())

            leftovers = []
            results = []
            for item in existing_recs:
                if item.is_proper_supserset(handle):
                    parts = item.clone().split_subset(handle.unitStart, handle.unitStop, handle.timeStart, handle.timeStop)
                    results.extend(parts[0])
                    leftovers.extend(parts[1:])
                else:
                    results.extend(item)

            for item in existing_recs:
                calendar.remove_record(item)

            for item in leftovers:
                calendar.insert_record(item)

            for item in results:
                item.set_allocator(callerGID->get_name(), allocatorGID->get_name(), which, where)
                calendar.insert_record(item)

    def set_consumer(self, callerGID_str, handle_strs, cred_str, reqsig):
        callerGID = GID(string = callerGID_str)
        cred = Credential(string = cred_str)

        # TODO: verify callerGID ssl key

        callerGID.verify_chain(self.trusted_cert_list)
        cred.verify_chain(self.trusted_cert_list)

        handles = strings_to_handles(handle_strs)
        for handle in handles:
            existing_recs = self.calendar.query_handles([handle])

            if not existing_recs:
                raise GacksResourceNotFound(hand.as_string())

            for rec in existing_recs:
                rec.set_consumer(cred.objectGID.get_name())
                calendar.update_record(rec)

if __name__ == "__main__":
    global TrustedRoots

    key_file = "gacksserver.key"
    cert_file = "gacksserver.cert"

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

    s = ComponentManager("", 12346, key_file, cert_file)
    s.trusted_cert_list = TrustedRoots.get_list()
    s.run()

