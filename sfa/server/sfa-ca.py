#!/usr/bin/python

#
# SFA Certificate Signing and management 
#   

import os
import sys
from optparse import OptionParser
from sfa.trust.certificate import Keypair, Certificate
from sfa.trust.gid import GID, create_uuid
from sfa.trust.hierarchy import Hierarchy
from sfa.util.config import Config

def main():
    args = sys.argv
    script_name = args[0]
    parser = OptionParser(usage="%(script_name)s [options]" % locals())
    parser.add_option("-d", "--display", dest="display", default=None,
                      help="print contents of specified gid")           
    parser.add_option("-s", "--sign", dest="sign", default=None, 
                      help="gid to sign" )
    parser.add_option("-k", "--key", dest="key", default=None, 
                      help="keyfile to use for signing")
    parser.add_option("-i", "--import", dest="importgid", default=None,
                      help="gid file to import into the registry")
    parser.add_option("-e", "--export", dest="export", 
                      help="name of gid to export from registry")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="where to write the exprted gid") 
    parser.add_option("-v", "--verbose", dest="verobse", 
                      help="be verbose")           
                
    (options, args) = parser.parse_args()


    if options.display:
        display(options)
    elif options.sign:
        sign(options)
    elif options.importgid:
        import_gid(options) 
    elif options.export:
        export_gid(options)  
    else:
        parser.print_help()
        sys.exit(1)        


def display(options):
    gidfile = os.path.abspath(options.display)
    print gidfile
    if not gidfile or not os.path.isfile(gidfile):
        print "No such gid: %s" % gidfile
        sys.exit(1) 
    gid = GID(filename=gidfile)
    gid.dump(dump_parents=True)

def sign(options):
    from sfa.util.table import SfaTable
    hierarchy = Hierarchy()
    config = Config()
    parent_hrn = config.SFA_INTERFACE_HRN
    auth_info = hierarchy.get_auth_info(parent_hrn)

    # load the gid
    gidfile = os.path.abspath(options.sign)
    if not os.path.isfile(gidfile):
        print "no such gid: %s" % gidfile
        sys.exit(1)
    gid = GID(filename=gidfile)

    # load the parent private key
    pkeyfile = options.key
    # if no pkey was specified, then use the this authority's key
    if not pkeyfile:
        pkeyfile = auth_info.privkey_filename
    if not os.path.isfile(pkeyfile):
        print "no such pkey: %s.\nPlease specify a valid private key" % pkeyfile
        sys.exit(1)
    parent_key = Keypair(filename=pkeyfile)

    # load the parent gid
    parent_gid = auth_info.gid_object

    # get the outfile
    outfile = options.outfile
    if not outfile:
        outfile = os.path.abspath('./signed-%s.gid' % gid.get_hrn())
   
    # check if gid already has a parent
 
    # sign the gid
    gid.set_issuer(parent_key, parent_hrn)
    gid.set_parent(parent_gid)
    gid.sign()
    gid.save_to_file(outfile, save_parents=True)            
    

def export(options):
    from sfa.util.table import SfaTable
    pass

def import_gid(options):
    from sfa.util.table import SfaTable
    pass

if __name__ == '__main__':
    main()
