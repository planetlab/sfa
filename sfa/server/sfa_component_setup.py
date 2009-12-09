#!/usr/bin/python
import sys
import os
import tempfile
from optparse import OptionParser
from sfa.util.config import Config
import sfa.util.xmlrpcprotocol as xmlrpcprotocol
import sfa.util.misc as misc
from sfa.trust.certificate import Keypair, Certificate
from sfa.trust.credential import Credential
from sfa.trust.gid import GID

def get_server(url=None, port=None, keyfile=None, certfile=None,verbose=False):
    """
    returns an xmlrpc connection to the service a the specified 
    address
    """
    if url:
        url_parts = url.split(":")
        if len(url_parts) >1:
            pass
        else:
            url = "http://%(url)s:%(port)s" % locals()
    else:
        # connect to registry by default
        config = Config()
        addr, port = config.SFA_REGISTRY_HOST, config.SFA_REGISTRY_PORT
        url = "http://%(addr)s:%(port)s" % locals()

    if verbose:
        print "Contacting registry at: %(url)s" % locals()

    server = xmlrpcprotocol.get_server(url, keyfile, certfile)
    return server    
    

def create_default_dirs():
    config = Config()
    hierarchy = Hierarchy()
    config_dir = config.config_path
    trusted_certs_dir = config.get_trustedroots_dir()
    authorities_dir = hierarchy.basedir
    all_dirs = [config_dir, trusted_certs_dir, authorities_dir]
    for dir in all_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
             
def get_node_key(registry=None, verbose=False):
    # this call requires no authentication, 
    # so we can generate a random keypair here
    subject="component"
    keyfile = tempfile.mktemp()
    certfile = tempfile.mktemp()
    key = Keypair(create=True)
    key.save_to_file(keyfile)
    cert = Certificate(subject=subject)
    cert.set_issuer(key=key, subject=subject)
    cert.set_pubkey(key)
    cert.sign()
    cert.save_to_file(certfile)
    
    registry = get_server(service_url = options.registry, keyfile=keyfile, certfile=certfile)    
    registry.get_key()

def create_server_keypair(keyfile=None, certfile=None, hrn="component", verbose=False):
    """
    create the server key/cert pair in the right place
    """
    key = Keypair(filename=keyfile)
    key.save_to_file(keyfile)
    cert = Certificate(subject=hrn)
    cert.set_issuer(key=key, subject=hrn)
    cert.set_pubkey(key)
    cert.sign()
    cert.save_to_file(certfile, save_parents=True)       
        
def get_credential(registry=registry, verbose=False):
    config = Config()
    hierarchy = Hierarchy()
    key_dir= hierarchy.basedir
    data_dir = config.data_path
    config_dir = config.config_path
    credfile = data_dir + os.sep + 'node.cred'
    # check for existing credential
    if os.path.exists(credfile):
        if verbose:
            print "Loading Credential from %(credfile)s " % locals()  
        cred = Credential(filename=credfile).save_to_string(save_parents=True)
    else:
        if verbose:
            print "Getting credential from registry" 
        # make sure node private key exists
        node_pkey_file = config_dir + os.sep + "node.key"
        node_gid_file = config_dir + os.sep + "node.gid"
        if not os.path.exists(node_pkey_file) or \
           not os.path.exists(node_gid_file):
            get_node_key(registry=registry, verbose=verbose)
        
        gid = GID(filename=node_gid_file)
        hrn = gid.get_hrn()
        # create server key and certificate
        keyfile =data_dir + os.sep + "server.key"
        certfile = data_dir + os.sep + "server.cert"
        key = Keypair(filename=node_pkey_file)
        key.save_to_file(keyfile)
        create_server_keypair(keyfile, certfile, hrn, verbose)

        # get credential from registry 
        registry = get_server(url=registry, keyfile=keyfile, certfile=certfile)
        cert_str = cert.save_to_string(save_parents=True)
        cred = registry.get_self_credential(cert_str, 'node', hrn)    
        Credential(string=cred).save_to_file(credfile)
    
    return cred

def get_trusted_certs(registry=None, verbose=False):
    """
    refresh our list of trusted certs.
    """
    # define useful variables
    config = Config()
    data_dir = config.data_path
    trusted_certs_dir = config.get_trustedroots_dir()
    keyfile = data_dir + os.sep + "server.key"
    certfile = data_dir + os.sep + "server.cert"
    node_gid_file = config_dir + os.sep + "node.gid"
    node_gid = GID(filename=node_gid_file)
    hrn = node_gid.get_hrn()
    # get credential
    cred = get_credential(registry=registry, verbose=verbose)
    # make sure server key cert pair exists
    create_server_keypair(keyfile=keyfile, certfile=certfile, hrn=hrn, verbose=verbose)
    registry = get_server(url=registry, keyfile=keyfile, certfile=certfile)
    # get the trusted certs and save them in the right place
    if verbose:
        print "Getting trusted certs from registry"
    trusted_certs = registry.get_trusted_certs(cred)
    trusted_gid_names = [] 
    for gid_str in trusted_certs:
        gid = GID(string=gid_str)
        gid.decode()
        trusted_gid_names.append(gid.get_hrn())
        gid_filename = trusted_certs_dir + os.sep + gid.get_hrn() + ".gid"
        if verbose:
            print "Writing GID for %s as %s" % (gid.get_hrn(), gid_filename) 
        gid.save_to_file(gid_filename, save_parents=True)

    # remove old certs
    all_gids_names = os.listdir(trusted_certs_dir)
    for gid_name in all_gids_names:
        if gid_name not in trusted_gid_names:
            os.unlink(trusted_certs_dir + os.sep + gid_name)                     

def get_gids(registry=None, verbose=False):
    """
    Get the gid for all instantiated slices on this node and store it
    in /etc/sfa/slice.gid in the slice's filesystem
    """
    # define useful variables
    config = Config()
    data_dir = config.data_path
    trusted_certs_dir = config.get_trustedroots_dir()
    keyfile = data_dir + os.sep + "server.key"
    certfile = data_dir + os.sep + "server.cert"
    node_gid_file = config_dir + os.sep + "node.gid"
    node_gid = GID(filename=node_gid_file)
    hrn = node_gid.get_hrn()
    interface_hrn = config.SFA_INTERFACE_HRN
    # get credential
    cred = get_credential(registry=registry, verbose=verbose)
    # make sure server key cert pair exists
    create_server_keypair(keyfile=keyfile, certfile=certfile, hrn=hrn, verbose=verbose)
    registry = get_server(url=registry, keyfile=keyfile, certfile=certfile)
            
    if verbose:
        print "Getting current slices on this node"
    # get a list of slices on this node
    from sfa.plc.api import ComponentAPI
    api = ComponentAPI()
    slicenames = api.nodemanger.GetXIDs().keys()   
    slicename_to_hrn = lambda name: ".".join([interface_hrn, name.replace('_', '.')])
    hrns = map(slicename_to_hrn, slicenames)

    if verbose:
        print "Getting gids for slices on this node from registry"  
    # get the gids
    # and save them in the right palce
    records = registry.get_gids(cred, hrns)
    for record in records:
        # if this isnt a slice record skip it
        if not record['type'] == 'slice':
            continue
        slicename = misc.hrn_to_pl_slicename(record['hrn'])
        # if this slice isnt really instatiated skip it
        if not os.path.exists("/vservers/%(slicename)s" % locals()):
            continue
       
        # save the slice gid in /etc/sfa/ in the vservers filesystem
        vserver_path = "/vserver/%(slicename)s" % locals()
        gid = record['gid']
        slice_gid_filename = os.sep.join([vserver_path, config_dir, "slice.gid"])
        if verbose:
            print "Saving GID for %(slicename)s as %(slice_gid_filename)s" % locals()
        GID(string=gid).save_to_file(slice_gid_filename, save_parents=True)
        # save the node gid in /etc/sfa
        node_gid_filename = os.sep.join([vserver_path, config_dir, "node.gid"])
        if verbose:
            print "Saving node GID for %(slicename)s as %(slice_gid_filename)s" % locals()
        node_gid.save_to_file(node_gid_filename, save_parents=True) 
                

def dispatch(options, args):

    create_default_dirs()
    if options.key:
        if verbose:
            print "Getting the component's pkey"
        get_node_key(options.registry, options.verbose)
    if options.certs:
        if options.verbose:
            print "Getting the component's trusted certs"
        get_certs(options.verbose)
    if options.gids:        
        if options.verbose:
            print "Geting the component's GIDs"
        get_gids(options.verbose)

def main():
    args = sys.argv
    prog_name = args[0]
    parser = OptionParser(usage="%(prog_name)s [options]" % locals())
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      default=False, help="Be verbose") 
    parser.add_option("-r", "--registry", dest="registry", default=None,
                      help="Url of registry to contact")  
    parser.add_option("-k", "--key", dest="key", action="store_true", 
                     default=False,  
                     help="Get the node's pkey from the registry")
    parser.add_option("-c", "--certs", dest="certs", action="store_true",
                      default=False,
                      help="Get the trusted certs from the registry")
    parser.add_option("-g", "--gids", dest="gids", action="store_true",       
                      default=False,
                      help="Get gids for all the slices on the component")

    (options, args) = parser.parse_args()

    dispatch(options, args)

if __name__ == '__main__':
    main()    
