#!/usr/bin/python
import sys
import os
from optparse import OptionParser
from sfa.util.config import Config
from sfa.util.xmlrpcprotocol import *
from sfa.trust.certificate import Keypair, Certificate
from sfa.trust.credential import Credential

def create_default_dirs():
    config_dir = '/etc/sfa'
    trusted_certs_dir = '/etc/sfa/trusted_certs'
    data_dir = '/var/lib/sfa'
    all_dirs = [config_dir, trusted_certs_dir, data_dir]
    for dir in all_dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)
             
def get_node_key(options):
    if options.verbose:
        print "Getting the component's pkey"
    # this call requires no authentication, 
    # so we can generate a random keypair here
    subject="component"
    keyfile = tempfile.mktemp()
    certfile = tempfile.mktemp()
    key = Keypair(create=True)
    key.save_to_file(keyfile)
    cert = Certificate(subject=component)
    cert.set_issuer(key=key, subject=subject)
    cert.set_pubkey(key)
    cert.sign()
    cert.save_to_file(certfile)
    
    # get the registry url
    url = ""   
    if options.registry:
        url_parts = options.registry.split(":")
        if len(url_parts) >1:
            url = options.registry
        else:
            url = "http://%s:12346" % options.registry
    else:
        config = Config()
        addr, port = config.SFA_REGISTRY_HOST, config.SFA_REGISTRY_PORT_
        url = "http://%(addr)s:%(port)s" % locals()  
        
    if options.verbose:
        print "Contacting registry at: %(url)s" % locals() 
     
    registry = xmlrpcprotocol.get_server(url, keyfile, certfile)
                
def get_credential(options):
    if options.verbose:
        print "Getting the component's credential"
    pass

def get_trusted_certs(options):
    if options.verbose:
        print "Getting the component's trusted certs"
    pass

def get_gids(options):
    if options.verbose:
        print "Geting the component's GIDs"
    
    pass

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

    create_default_dirs()
    if options.key:
        get_key(options)
    if options.certs:
        get_certs(options)
    if options.gids:
        get_gids(options)

if __name__ == '__main__':
    main()    
