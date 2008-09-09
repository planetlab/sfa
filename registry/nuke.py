import getopt
import sys

from hierarchy import *
from record import *
from genitable import *
from config import *

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
