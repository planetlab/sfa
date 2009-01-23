#! /usr/bin/env python
from __future__ import with_statement

# sfi -- slice-based facility interface

import sys
import os, os.path
import getopt
from util.cert import Keypair, Certificate
from util.credential import Credential
from util.geniclient import GeniClient
from util.record import GeniRecord
from util.gid import GID

infile = None
outfile = None
gidfile = None
email = None
ip = None
dns = None
hrn = None
type = None
dump = False
researcher = []

long_opts = ["infile=", "outfile=", "email=", "ip=", "dns=", "gidfile=", "hrn=", "type=", "addresearcher=", "delresearcher=", "dump"]

def showhelp():
   print "syntax: editRecord.py <options>"
   print "    --help                ... show help"
   print "    --infile <name>       ... read record from file"
   print "    --outfile <name>      ... write record to file"
   print "    --dump                ... dump record to stdout"
   print "    --gidfile <fn>        ... load gid from file"
   print "    --hrn <name>          ... set hrn"
   print "    --type <type>         ... set type (user|slice|sa|ma|...)"
   print "    --email <addr>        ... user: set email address"
   print "    --ip <addr>           ... node: set ip address"
   print "    --dns <hostname>      ... node: set hostname"
   print "    --addresearcher <hrn> ... slice: add researcher"
   print "    --delresearcher <hrn> ... slice: delete researcher"

def process_options():
   global infile, outfile
   global email, ip, dns, gidfile, hrn, type
   global researcher
   global dump

   (options, args) = getopt.getopt(sys.argv[1:], '', long_opts)
   for opt in options:
       name = opt[0]
       val = opt[1]

       if name == "--help":
           showhelp()
           sys.exit(0)
       elif name == "--infile":
           infile = val
       elif name == "--outfile":
           outfile = val
       elif name == "--email":
           email = val
       elif name == "--ip":
           ip = val
       elif name == "--dns":
           dns = val
       elif name == "--gidfile":
           gidfile = val
       elif name == "--hrn":
           hrn = val
       elif name == "--type":
           type = val
       elif name == "--dump":
           dump = True
       elif name == "--addresearcher":
           researcher.append(val)
       elif name == "--delresearcher":
           researcher.append("-" + val)

def errorcheck(record):
   geni_info = record.get_geni_info()

   if not record.type:
       print "Warning: no type specified"
   if not record.type in ["user", "sa", "ma", "slice", "node"]:
       print "Warning: unknown record type"
   if not record.name:
       print "Warning: unknown record name"
   if not record.gid:
       print "Warning: unknown record gid"

   if record.type == "user":
       if not geni_info.get("email",None):
           print "Warning: unknown email in user record"

   if record.type == "node":
       if not geni_info.get("ip",None):
           print "Warning: unknown ip in node record"
       if not geni_info.get("dns",None):
           print "Warning: unknown dns in node record"

# updates is a list of items to add or remove. If an item starts with "-", then
# it will be removed. Otherwise it will be added
def update_list(dict, listname, updates):
   list = dict.get(listname, [])
   for hrn in updates:
       if hrn.startswith("-"):
           real_hrn = hrn[1:]
           if real_hrn in list:
               list.delete(real_hrn)
       else:
           if not hrn in list:
               list.append(hrn)

   dict[listname] = list

def main():
   process_options()

   # if the user didn't tell us to do much of anything, then maybe he needs
   # some help
   if (not infile) and (not outfile) and (not dump):
       showhelp()
       return

   if infile:
       str = file(infile, "r").read()
       record = GeniRecord(string = str)
   else:
       record = GeniRecord()

   geni_info = record.get_geni_info()
   geni_info_orig = geni_info.copy()

   if email:
       geni_info["email"] = email

   if ip:
       geni_info["ip"] = ip

   if dns:
       geni_info["dns"] = dns

   if hrn:
       record.name = hrn

   if type:
       record.type = type

   if gidfile:
       gid_str = file(gidfile, "r").read()
       gid = GID(string=gid_str)
       record.set_gid(gid)

   if researcher:
       update_list(geni_info, "researcher", researcher)

   if (geni_info != geni_info_orig):
       record.set_geni_info(geni_info)

   errorcheck(record)

   if dump:
       record.dump(False)

   if outfile:
       str = record.save_to_string()
       file(outfile, "w").write(str)
       print "wrote record to", outfile

if __name__=="__main__":
   main()
