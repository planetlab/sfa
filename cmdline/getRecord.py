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

def findRoot(r, filter):
    root = None
    if type(r) == dict:
        if not r.has_key(filter):
            for k in r.keys():
                root = findRoot(r[k], filter)
                if root != None: return root
        else:
            return r[filter]
    elif type(r) in (tuple, list):
        for j in r: 
            root = findRoot(j, filter)
            if root != None: return root
    else:
        return root

def main():
    parser = create_parser(); 
    (options, args) = parser.parse_args()

    # Check the the file was specified  
    if not options.infile:
        print "You must specify a record file"
        return -1
    try: 
        print "Openning %s.\n" % options.infile
        f = open(options.infile)
    except: raise

    record = RecordSpec(xml = f)

    if options.DEBUG: 
        pprint(record.dict)
        print "#####################################################"


    if args:
        if options.DEBUG: 
            print "Filtering on key: %s" % args[0]
            pprint(findRoot(record.dict, args[0]))
        record.pprint({args[0]: findRoot(record.dict, args[0])})
    else:
        record.pprint(record.dict)

if __name__ == '__main__':
    try: main()
    except Exception, e:
        print e
