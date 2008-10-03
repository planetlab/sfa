##
# Create an authority via the hierarchy module.
#
# This tool was most likely used during development and is deprecated by the
# import tool.
##

import getopt
import sys

from hierarchy import *

hrn = None

def process_options():
   global hrn

   (options, args) = getopt.getopt(sys.argv[1:], '', [])
   for opt in options:
       name = opt[0]
       val = opt[1]

   if not args:
       print "no hrn specified"
       sys.exit(-1)

   hrn = args[0]


def main():
    process_options()

    h = Hierarchy()
    h.create_auth(hrn)

if __name__ == "__main__":
    main()
