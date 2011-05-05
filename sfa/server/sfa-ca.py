#!/usr/bin/python

#
# SFA Certificate Signing and management. Root authorities can use this script 
# to sign  the certificate of another authority and become its parent. Sub 
# authorities (authorities that have had their cert signed by another authority) 
# can use this script to update their registry hierarchy with the new cert    
# 
# Example usage: 
#
## sign a peer cert
# sfa-ca.py --sign PEER_CERT_FILENAME -o OUTPUT_FILENAME 
#
## import a cert and update the registry hierarchy
# sfa-ca.py --import CERT_FILENAME   
#
## display a cert
# sfa-ca.py --display CERT_FILENAME


import os
import sys
from optparse import OptionParser
from sfa.trust.certificate import Keypair, Certificate
from sfa.trust.gid import GID, create_uuid
from sfa.trust.hierarchy import Hierarchy
from sfa.util.config import Config
from collections import defaultdict

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
    parser.add_option("-a", "--authority", dest="authority", default=None, 
                      help="sign the gid using the specified authority ")
    parser.add_option("-i", "--import", dest="importgid", default=None,
                      help="gid file to import into the registry")
    parser.add_option("-e", "--export", dest="export", 
                      help="name of gid to export from registry")
    parser.add_option("-t", "--type", dest="type",
                      help="record type", default=None)
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="where to write the exprted gid") 
    parser.add_option("-v", "--verbose", dest="verbose", default=False, 
                      action="store_true", help="be verbose")           
                
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
    """
    Display the sepcified GID
    """
    gidfile = os.path.abspath(options.display)
    if not gidfile or not os.path.isfile(gidfile):
        print "No such gid: %s" % gidfile
        sys.exit(1)
    gid = GID(filename=gidfile)
    gid.dump(dump_parents=True)

def sign_gid(gid, parent_key, parent_gid):
    gid.set_issuer(parent_key, parent_gid.get_hrn())
    gid.set_parent(parent_gid)
    gid.set_intermediate_ca(True)
    gid.set_pubkey(gid.get_pubkey())
    gid.sign()
    return gid 

def sign(options):
    """
    Sign the specified gid
    """
    hierarchy = Hierarchy()
    config = Config()
    default_authority = config.SFA_INTERFACE_HRN
    auth_info = hierarchy.get_auth_info(default_authority)

    # load the gid
    gidfile = os.path.abspath(options.sign)
    if not os.path.isfile(gidfile):
        print "no such gid: %s" % gidfile
        sys.exit(1)
    gid = GID(filename=gidfile)

    # remove previous parent
    gid = GID(string=gid.save_to_string(save_parents=False))

    # load the parent private info
    authority = options.authority    
    # if no pkey was specified, then use the this authority's key
    if not authority:
        authority = default_authority 
    
    if not hierarchy.auth_exists(authority):
        print "no such authority: %s" % authority    

    # load the parent gid and key 
    auth_info = hierarchy.get_auth_info(authority)
    pkeyfile = auth_info.privkey_filename
    parent_key = Keypair(filename=pkeyfile)
    parent_gid = auth_info.gid_object

    # get the outfile
    outfile = options.outfile
    if not outfile:
        outfile = os.path.abspath('./signed-%s.gid' % gid.get_hrn())
   
    # check if gid already has a parent
 
    # sign the gid
    if options.verbose:
        print "Signing %s gid with parent %s" % \
              (gid.get_hrn(), parent_gid.get_hrn())
    gid = sign_gid(gid, parent_key, parent_gid)
    # save the signed gid
    if options.verbose:
        print "Writing signed gid %s" % outfile  
    gid.save_to_file(outfile, save_parents=True)
    

def export_gid(options):
    from sfa.util.table import SfaTable
    # lookup the record for the specified hrn 
    hrn = options.export
    type = options.type
    # check sfa table first
    filter = {'hrn': hrn}
    if type:
        filter['type'] = type                    
    table = SfaTable()
    records = table.find(filter)
    if not records:
        # check the authorities hierarchy 
        hierarchy = Hierarchy()
        try:
            auth_info = hierarchy.get_auth_info()
            gid = auth_info.gid_object 
        except:
            print "Record: %s not found" % hrn
            sys.exit(1)
    else:
        record = records[0]
        gid = GID(string=record['gid'])
        
    # get the outfile
    outfile = options.outfile
    if not outfile:
        outfile = os.path.abspath('./%s.gid' % gid.get_hrn())

    # save it
    if options.verbose:
        print "Writing %s gid to %s" % (gid.get_hrn(), outfile)
    gid.save_to_file(outfile, save_parents=True)

def import_gid(options):
    """
    Import the specified gid into the registry (db and authorities 
    hierarchy) overwriting any previous gid.
    """
    from sfa.util.table import SfaTable
    from sfa.util.record import SfaRecord
    # load the gid
    gidfile = os.path.abspath(options.importgid)
    if not gidfile or not os.path.isfile(gidfile):
        print "No such gid: %s" % gidfile
        sys.exit(1)
    gid = GID(filename=gidfile)
    
    # check if it exists within the hierarchy
    hierarchy = Hierarchy()
    if not hierarchy.auth_exists(gid.get_hrn()):
        print "%s not found in hierarchy" % gid.get_hrn()
        sys.exit(1)

    # check if record exists in db
    table = SfaTable()
    records = table.find({'hrn': gid.get_hrn(), 'type': 'authority'})
    if not records:
        print "%s not found in record database" % get.get_hrn()  
        sys.exit(1)

    # update the database record
    record = records[0]
    record['gid'] = gid.save_to_string(save_parents=True)
    table.update(record)
    if options.verbose:
        print "Imported %s gid into db" % record['hrn']

    # update the hierarchy
    auth_info = hierarchy.get_auth_info(gid.get_hrn())  
    filename = auth_info.gid_filename
    gid.save_to_file(filename, save_parents=True)
    if options.verbose:
        print "Writing %s gid to %s" % (gid.get_hrn(), filename)

    # re-sign all existing gids signed by this authority  
    # create a dictionary of records keyed on the record's authority
    record_dict = defaultdict(list)
    # only get regords that belong to this authority 
    # or any of its sub authorities   
    child_records = table.find({'hrn': '%s*' % gid.get_hrn()})
    if not child_records:
        return
  
    for record in child_records:
        record_dict[record['authority']].append(record) 

    # start with the authority we just imported       
    authorities = [gid.get_hrn()]
    while authorities:
        next_authorities = []
        for authority in authorities:
            # create a new signed gid for each record at this authority 
            # and update the registry
            auth_info = hierarchy.get_auth_info(authority)
            records = record_dict[authority]
            for record in records:
                record_gid = GID(string=record['gid'])
                parent_pkey = Keypair(filename=auth_info.privkey_filename)
                parent_gid = GID(filename=auth_info.gid_filename)
                if options.verbose:
                    print "re-signing %s gid with parent %s" % \
                           (record['hrn'], parent_gid.get_hrn())  
                signed_gid = sign_gid(record_gid, parent_pkey, parent_gid)
                record['gid'] = signed_gid.save_to_string(save_parents=True)
                table.update(record)
                
                # if this is an authority then update the hierarchy
                if record['type'] == 'authority':
                    record_info = hierarchy.get_auth_info(record['hrn'])
                    if options.verbose:
                        print "Writing %s gid to %s" % (record['hrn'], record_info.gid_filename) 
                    signed_gid.save_to_file(filename=record_info.gid_filename, save_parents=True)

             # update list of next authorities
            tmp_authorities = set([record['hrn'] for record in records \
                                   if record['type'] == 'authority'])
            next_authorities.extend(tmp_authorities)

        # move on to next set of authorities
        authorities = next_authorities     

if __name__ == '__main__':
    main()
