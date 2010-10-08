#!/usr/bin/python
##
# Delete all the database records for SFA. This tool is used to clean out SFA
# records during testing.
#
# Authority info (maintained by the hierarchy module in a subdirectory tree)
# is not purged by this tool and may be deleted by a command like 'rm'.
##

import sys
import os
from optparse import OptionParser

from sfa.trust.hierarchy import *
from sfa.util.record import *
from sfa.util.table import SfaTable
from sfa.util.sfalogging import sfa_logger_goes_to_import,sfa_logger

def main():
   usage="%prog: trash the registry DB (the 'sfa' table in the 'planetlab5' database)"
   parser = OptionParser(usage=usage)
   parser.add_option('-f','--file-system',dest='clean_fs',action='store_true',default=False,
                     help='Clean up the /var/lib/sfa/authorities area as well')
   (options,args)=parser.parse_args()
   if args:
      parser.print_help()
      sys.exit(1)
   sfa_logger_goes_to_import()
   sfa_logger().info("Purging SFA records from database")
   table = SfaTable()
   table.sfa_records_purge()
   if options.clean_fs:
      # just remove all files that do not match 'server.key' or 'server.cert'
      preserved_files = [ 'server.key', 'server.cert']
      for (dir,_,files) in os.walk('/var/lib/sfa/authorities'):
         for file in files:
            if file in preserved_files: continue
            path=dir+os.sep+file
            os.unlink(path)
            if not os.path.exists(path):
               sfa_logger().info("Unlinked file %s"%path)
            else:
               sfa_logger().error("Could not unlink file %s"%path)
if __name__ == "__main__":
   main()
