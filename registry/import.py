import getopt
import sys
import tempfile

from cert import *
from trustedroot import *
from hierarchy import *
from record import *
from genitable import *
from misc import *

shell = None

root_auth = "planetlab"
level1_auth = "planetlab.us"

def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

def connect_shell():
    global pl_auth, shell

    # get PL account settings from config module
    pl_auth = get_pl_auth()

    # connect to planetlab
    if "Url" in pl_auth:
        import remoteshell
        shell = remoteshell.RemoteShell()
    else:
        import PLC.Shell
        shell = PLC.Shell.Shell(globals = globals())

def get_auth_table(auth_name):
    auth_info = AuthHierarchy.get_auth_info(auth_name)

    table = GeniTable(hrn=auth_name,
                      cninfo=auth_info.get_dbinfo())

    # if the table doesn't exist, then it means we haven't put any records
    # into this authority yet.

    if not table.exists():
        report.trace("Import: creating table for authority " + auth_name)
        table.create()

    return table

def get_pl_pubkey(key_id):
    keys = shell.GetKeys(pl_auth, [key_id])
    if keys:
        key_str = keys[0]['key']

        # generate temporary files to hold the keys
        (ssh_f, ssh_fn) = tempfile.mkstemp()
        ssl_fn = tempfile.mktemp()

        os.write(ssh_f, key_str)
        os.close(ssh_f)

        cmd = "../keyconvert/keyconvert " + ssh_fn + " " + ssl_fn
        print cmd
        os.system(cmd)

        # this check leaves the temporary file containing the public key so
        # that it can be expected to see why it failed.
        # TODO: for production, cleanup the temporary files
        if not os.path.exists(ssl_fn):
            report.trace("  failed to convert key from " + ssh_fn + " to " + ssl_fn)
            return None

        k = Keypair()
        k.load_pubkey_from_file(ssl_fn)

        #sys.exit(-1)

        # remove the temporary files
        os.remove(ssh_fn)
        os.remove(ssl_fn)

        return k
    else:
        return None

def import_person(parent_hrn, person):
    personname = person['last_name'] + "_" + person['first_name']

    hrn = parent_hrn + "." + personname
    report.trace("Import: importing person " + hrn)

    table = get_auth_table(parent_hrn)

    person_record = table.resolve("slice", hrn)
    if not person_record:
        #pkey = Keypair(create=True)
        key_ids = person["key_ids"]
        if key_ids:
            pkey = get_pl_pubkey(key_ids[0])
        else:
            report.trace("   person " + hrn + " does not have a PL public key")
            pkey = Keypair(create=True)
        person_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
        person_record = GeniRecord(name=hrn, gid=person_gid, type="user", pointer=person['person_id'])
        report.trace("  inserting user record for " + hrn)
        table.insert(person_record)

def import_slice(parent_hrn, slice):
    slicename = slice['name'].split("_",1)[-1]

    if not slicename:
        report.error("Import_Slice: failed to parse slice name " + slice['name'])
        return

    hrn = parent_hrn + "." + slicename
    report.trace("Import: importing slice " + hrn)

    table = get_auth_table(parent_hrn)

    slice_record = table.resolve("slice", hrn)
    if not slice_record:
        pkey = Keypair(create=True)
        slice_gid = AuthHierarchy.create_gid(hrn, create_uuid(), pkey)
        slice_record = GeniRecord(name=hrn, gid=slice_gid, type="slice", pointer=slice['slice_id'])
        report.trace("  inserting slice record for " + hrn)
        table.insert(slice_record)

def import_site(parent_hrn, site):
    hrn = parent_hrn + "." + site['login_base']

    report.trace("Import_Site: importing site " + hrn)

    # create the authority
    if not AuthHierarchy.auth_exists(hrn):
        AuthHierarchy.create_auth(hrn)

    auth_info = AuthHierarchy.get_auth_info(hrn)

    table = get_auth_table(parent_hrn)

    sa_record = table.resolve("sa", hrn)
    if not sa_record:
        sa_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="sa", pointer=site['site_id'])
        report.trace("  inserting sa record for " + hrn)
        table.insert(sa_record)

    ma_record = table.resolve("ma", hrn)
    if not ma_record:
        ma_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="ma", pointer=site['site_id'])
        report.trace("  inserting ma record for " + hrn)
        table.insert(ma_record)

    for person_id in site['person_ids']:
        persons = shell.GetPersons(pl_auth, [person_id])
        if persons:
            import_person(hrn, persons[0])

    for slice_id in site['slice_ids']:
        slices = shell.GetSlices(pl_auth, [slice_id])
        if slices:
            import_slice(hrn, slices[0])

def create_top_level_auth_records(hrn):
    parent_hrn = get_authority(hrn)

    auth_info = AuthHierarchy.get_auth_info(parent_hrn)
    table = get_auth_table(parent_hrn)

    sa_record = table.resolve("sa", hrn)
    if not sa_record:
        sa_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="sa", pointer=-1)
        report.trace("  inserting sa record for " + hrn)
        table.insert(sa_record)

    ma_record = table.resolve("ma", hrn)
    if not ma_record:
        ma_record = GeniRecord(name=hrn, gid=auth_info.get_gid_object(), type="ma", pointer=-1)
        report.trace("  inserting ma record for " + hrn)
        table.insert(ma_record)

def main():
    global AuthHierarchy
    global TrustedRoots

    process_options()

    AuthHierarchy = Hierarchy()
    TrustedRoots = TrustedRootList()

    print "Import: creating top level authorities"

    if not AuthHierarchy.auth_exists(root_auth):
        AuthHierarchy.create_auth(root_auth)
    #create_top_level_auth_records(root_auth)
    if not AuthHierarchy.auth_exists(level1_auth):
        AuthHierarchy.create_auth(level1_auth)
    create_top_level_auth_records(level1_auth)

    print "Import: adding", root_auth, "to trusted list"
    root = AuthHierarchy.get_auth_info(root_auth)
    TrustedRoots.add_gid(root.get_gid_object())

    connect_shell()

    sites = shell.GetSites(pl_auth)
    for site in sites:
        import_site(level1_auth, site)

if __name__ == "__main__":
    main()
