##
# A simple tool for adding an initscript via the PLCAPI. I couldn't find the
# obvious way to do this through the PL interface, so I wrote this utility to
# do it.
#
# It takes two command line parameters: an initscript name and the contents of
# the initscript.
#
# For example,
#     addinitscript.py foo "echo test"
##

import getopt
import sys
import tempfile

from config import *

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

def main():
    connect_shell()

    if len(sys.argv)<3:
       print "syntax: addinitscript.py name value"
       sys.exit(-1)

    name = sys.argv[1]
    value = sys.argv[2]

    fields={}
    fields['enabled'] = True
    fields['name'] = name
    fields['script'] = value
    shell.AddInitScript(pl_auth, fields)

if __name__ == "__main__":
    main()
