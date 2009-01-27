##
# Delete all the database records for Geni. This tool is used to clean out Geni
# records during testing.
#
# Authority info (maintained by the hierarchy module in a subdirectory tree)
# is not purged by this tool and may be deleted by a command like 'rm'.
##

import getopt
import sys

from geni.util.hierarchy import *
from geni.util.record import *
from geni.util.genitable import *
from geni.util.config import *

def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

def main():
    process_options()

    print "purging geni records from database"
    geni_records_purge(get_default_dbinfo())

if __name__ == "__main__":
    main()
