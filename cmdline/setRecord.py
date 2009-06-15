#!/usr/bin/python

"""
Updates record objects


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


def editDict(replacewith, recordDict, options):
    # first we find the part of the tree we want to replace
    # and check it exists.
    for (key, val) in replacewith.items():
        if not recordDict.has_key(key):
            print "Cannot find key %s in record %s.  Adding new key."\
                 % (key, options.infile)
        else:
            print "Replacing %s = %s with %s\n" % (key, recordDict[key], val)
        recordDict[key] = val
   

def patchDict(args):
    """
    Takes the arg list, seperates into tag/value, creates a dict.
    """
    patch = {}
    for vect in args:
        if vect.count("="):
            patch[vect.split("=")[0]] = vect.split("=")[1]
        else:
            raise TypeError, "Argument error: Records are updated with key=val\n" \
                            "%s Unknown key/val" % vect
    return patch


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
        record = RecordSpec(xml = f)
        f.close()
    except: raise


    if args:
        patch = patchDict(args)
        if options.DEBUG:  print "Replace w/ %s" %  patch
        editDict(patch, record.dict["record"], options)
    if options.DEBUG:
        print "New Record:\n%s" % record.dict

    record.pprint()

    record.rootNode = record.dict2dom(record.dict)
    s = record.toxml()
    f = open(options.infile,"w")
    f.write(s)

if __name__ == '__main__':
    try: main()
    except Exception, e:
        print e
