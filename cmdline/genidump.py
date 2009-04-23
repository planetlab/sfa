#! /usr/bin/env python
from __future__ import with_statement

import sys
import os, os.path
import tempfile
import xmlrpclib
from optparse import OptionParser
from geni.util.cert import Keypair, Certificate
from geni.util.credential import Credential
from geni.util.geniclient import GeniClient, ServerException
from geni.util.gid import create_uuid
from geni.util.record import GeniRecord
from geni.util.rspec import Rspec
from types import StringTypes, ListType

def determine_geni_filekind(fn):
    from geni.util.cert import Certificate

    cert = Certificate(filename = fn)

    data = cert.get_data()
    if data:
        dict = xmlrpclib.loads(data)[0][0]
    else:
        dict = {}

    if "gidCaller" in dict:
        return "credential"

    if "uuid" in dict:
        return "gid"

    return "unknown"

def create_parser():
   # Generate command line parser
   parser = OptionParser(usage="genidump [options] filename")

   return parser

def main():
   parser = create_parser()
   (options, args) = parser.parse_args()

   if len(args) <= 0:
        print "No filename given. Use -h for help."
        return -1

   filename = args[0]
   kind = determine_geni_filekind(filename)

   if kind=="credential":
       cred = Credential(filename = filename)
       cred.dump(dump_parents = True)
   elif kind=="gid":
       gid = Gid(filename = filename)
       gid.dump(dump_parents = True)
   else:
       print "unknown filekind", kind

if __name__=="__main__":
   main()
