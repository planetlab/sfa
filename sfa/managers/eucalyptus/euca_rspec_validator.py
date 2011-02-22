#!/usr/bin/env python

from __future__ import with_statement 
import sys
import os
from lxml import etree as ET

##
# The location of the RelaxNG schema.
#
EUCALYPTUS_RSPEC_SCHEMA='eucalyptus.rng'

def main():
    with open(sys.argv[1], 'r') as f:
        xml = f.read()
        schemaXML = ET.parse(EUCALYPTUS_RSPEC_SCHEMA)
        rspecValidator = ET.RelaxNG(schemaXML)
        rspecXML = ET.XML(xml)
        if not rspecValidator(rspecXML):
            error = rspecValidator.error_log.last_error
            message = '%s (line %s)' % (error.message, error.line) 
            print message
        else:
            print 'It is valid'

if __name__ == "__main__":
    main()

