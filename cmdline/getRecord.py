#!/usr/bin/python

"""
Filters/Prints record objects


faiyaza at cs dot princeton dot edu
Copyright (c) 2009 Board of Trustees, Princeton University

$Id$
$HeadURL$
"""

import sys
import os
from optparse import OptionParser
from pprint import pprint

from geni.util.rspec import RecordSpec


def create_parser():
    command = sys.argv[0]
    argv = sys.argv[1:]
    usage = "%(command)s [options]" % locals()
    description = """getRecord will open a record file and print all key/values, or filter results based on a given key or set of keys."""
    parser = OptionParser(usage=usage,description=description)
    parser.add_option("-i", "--infile", dest="infile", metavar="FILE", 
        default=None,  help = "record file path")
    parser.add_option("-d", "--debug", dest="DEBUG", action="store_true",
        default=False,  help = "record file path")
   
    return parser    

def printRecord(r, depth = 0):
    line = ""
    # Set the dept
    for tab in range(0,depth): line += "    "
    # check if it's nested
    for i in r.keys(): 
        if type(r[i]) == dict:
            # print the parent, carry return
            print line + "%s :\n" % i
            #recurse here, increment depth
            printRecord(r[i], depth + 1)
        else:
            #assume we've hit the bottom
            if (type(r[i]) == tuple) or (type(r[i]) == list):
                print line + " %s:" % i
                for j in r[i]:
                    if type(j) == dict:
                        printRecord(j, depth + 2)
                    else: print line + line + " %s" % j
            else:
                print line + " %s:    %s" % (i, r[i])

def main():
    parser = create_parser(); 
    (options, args) = parser.parse_args()

    # Check the the file was specified  
    if not options.infile:
        print "You must specify a record file"
        return -1
    else:
        try: 
            record = RecordSpec()
            print "Openning %s.\n" % options.infile
            record.parseFile(options.infile)
        except: raise 
        record.dict = record.toDict()

        if args:
            print "Filtering on key: %s" % args

        if options.DEBUG: 
            pprint(record.dict)
            print "#####################################################"

        else:
            printRecord(record.dict)

if __name__ == '__main__':
    main()
    #try: main()
    #except Exception, e:
    #    print e
