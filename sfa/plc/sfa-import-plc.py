#!/usr/bin/python
#
### $Id$
### $URL$
#
##
# Import PLC records into the Geni database. It is indended that this tool be
# run once to create Geni records that reflect the current state of the
# planetlab database.
#
# The import tool assumes that the existing PLC hierarchy should all be part
# of "planetlab.us" (see the root_auth and level1_auth variables below).
#
# Public keys are extracted from the users' SSH keys automatically and used to
# create GIDs. This is relatively experimental as a custom tool had to be
# written to perform conversion from SSH to OpenSSL format. It only supports
# RSA keys at this time, not DSA keys.
##

import getopt
import sys
import tempfile

from sfa.util.record import *
from sfa.util.genitable import GeniTable
from sfa.util.misc import *
from sfa.util.config import Config
from sfa.util.report import trace, error

from sfa.trust.certificate import convert_public_key, Keypair
from sfa.trust.trustedroot import *
from sfa.trust.hierarchy import *
from sfa.trust.gid import create_uuid
from sfa.plc.sfaImport import *



def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

def main():
    process_options()
    config = Config()
    root_auth = config.SFA_REGISTRY_ROOT_AUTH
    level1_auth = config.SFA_REGISTRY_LEVEL1_AUTH
    sfaImporter = sfaImport()
    shell = sfaImporter.shell
    plc_auth = sfaImporter.plc_auth 
    AuthHierarchy = sfaImporter.AuthHierarchy
    TrustedRoots = sfaImporter.TrustedRoots
    
    if not level1_auth or level1_auth in ['']:
        level1_auth = None
    
    print "Import: creating top level authorities"
    if not level1_auth:
        sfaImporter.create_top_level_auth_records(root_auth)
        import_auth = root_auth
    else:
        if not AuthHierarchy.auth_exists(level1_auth):
            AuthHierarchy.create_auth(level1_auth)
        sfaImporter.create_top_level_auth_records(level1_auth)
        import_auth = level1_auth

    print "Import: adding", import_auth, "to trusted list"
    authority = AuthHierarchy.get_auth_info(import_auth)
    TrustedRoots.add_gid(authority.get_gid_object())

    sites = shell.GetSites(plc_auth, {'peer_id': None})
    # create a fake internet2 site first
    i2site = {'name': 'Internet2', 'abbreviated_name': 'I2',
                    'login_base': 'internet2', 'site_id': -1}
    sfaImporter.import_site(import_auth, i2site)
    
    for site in sites:
        sfaImporter.import_site(import_auth, site)

if __name__ == "__main__":
    main()
