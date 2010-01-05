from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.rspec import RSpec
from sfa.server.registry import Registries
from sfa.plc.nodes import *
import sys

def get_rspec(api, hrn, origin_hrn):
    xml = """<?xml version="1.0"?>
<RSpec name="eucalyptus">
</RSpec>"""
    return xml

"""
Hook called via 'sfi.py create'
"""
def create_slice(api, hrn, xml):
    return True

def main():
    r = RSpec()
    r.parseFile(sys.argv[1])
    rspec = r.toDict()
    create_slice(None,'plc',rspec)

if __name__ == "__main__":
    main()
