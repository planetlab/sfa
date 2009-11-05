#!/usr/bin/python
#
### $Id: sfa-compnent-server.py 
### $URL:
 
# This wrapper implements the SFA Component Interfaces on PLC.
#
# There are several items that need to be done before starting the wrapper
# server.
#
#   (requirements coming soon)
##

# TCP ports for the three servers
component_port=12348

import os, os.path
from optparse import OptionParser

from sfacomponent.server.component import Component
from sfa.trust.trustedroot import TrustedRootList
from sfa.trust.certificate import Keypair, Certificate
from sfa.trust.hierarchy import Hierarchy
from sfa.util.config import Config

# after http://www.erlenstar.demon.co.uk/unix/faq_2.html
def daemon():
    """Daemonize the current process."""
    if os.fork() != 0: os._exit(0)
    os.setsid()
    if os.fork() != 0: os._exit(0)
    os.umask(0)
    devnull = os.open(os.devnull, os.O_RDWR)
    os.dup2(devnull, 0)
    # xxx fixme - this is just to make sure that nothing gets stupidly lost - should use devnull
    crashlog = os.open('/var/log/sfa.daemon', os.O_RDWR | os.O_APPEND | os.O_CREAT, 0644)
    os.dup2(crashlog, 1)
    os.dup2(crashlog, 2)

def main():
    # xxx get rid of globals - name consistently CamelCase or under_score
    global AuthHierarchy
    global TrustedRoots
    global component_port

    # Generate command line parser
    parser = OptionParser(usage="sfa-component-server [options]")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", 
         help="verbose mode", default=False)
    parser.add_option("-d", "--daemon", dest="daemon", action="store_true",
         help="Run as daemon.", default=False)
    (options, args) = parser.parse_args()

    hierarchy = Hierarchy()
    path = hierarchy.basedir
    key_file = os.path.join(path, "server.key")
    cert_file = os.path.join(path, "server.cert")
   
    # XX TODO: Subject should be the node's hrn    
    subject = "component" 
    if (options.daemon):  daemon()

    if (os.path.exists(key_file)) and (not os.path.exists(cert_file)):
        # If private key exists and cert doesnt, recreate cert
        key = Keypair(filename=key_file)
        cert = Certificate(subject=subject)
        cert.set_issuer(key=key, subject=subject)
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    elif (not os.path.exists(key_file)) or (not os.path.exists(cert_file)):
        # if no key is specified, then make one up
        key = Keypair(create=True)
        key.save_to_file(key_file)
        cert = Certificate(subject=subject)
        cert.set_issuer(key=key, subject=subject)
        cert.set_pubkey(key)
        cert.sign()
        cert.save_to_file(cert_file)

    AuthHierarchy = Hierarchy()

    TrustedRoots = TrustedRootList(Config().get_trustedroots_dir())
    component = Component("", component_port, key_file, cert_file)
    component.start()

if __name__ == "__main__":
    main()
