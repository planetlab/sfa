#!/usr/bin/python
from sfa.rspecs.sfa_rspec import SfaRSpec
from sfa.rspecs.pg_rspec import PGRSpec
from sfa.rspecs.rspec import RSpec
from lxml import etree 

def parse_rspec(in_rspec):
    rspec = RSpec(rspec=in_rspec)
    # really simple check
    # TODO: check against schema instead
    out_rspec = None 
    if rspec.xml.xpath('//network'):
        #out_rspec = SfaRSpec(in_rspec)
        out_rspec = SfaRSpec()
        out_rspec.xml = rspec.xml
    else:
        #out_rspec = PGRSpec(in_rspec)
        out_rspec = PGRSpec()
        out_rspec.xml = rspec.xml
    return out_rspec


if __name__ == '__main__':
    
    print "Parsing SFA RSpec:", 
    rspec = parse_rspec('nodes.rspec')
    print rspec.type
    rspec = parse_rspec('protogeni.rspec')
    print "Parsing ProtoGENI RSpec:", 
    print rspec.type
    
    

