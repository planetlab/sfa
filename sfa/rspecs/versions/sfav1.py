from sfa.rspecs.rspec_version import RSpecVersion
from sfa.rspecs.rspec_elements import RSpecElement, RSpecElements

class SFAv1(RSpecVersion):
    type = 'SFA'
    content_type = '*'
    version = '1'
    schema = None
    namespace = None
    extensions = {}
    elements = [
        RSpecElement(RSpecElements.NETWORK, 'network', '//network'),
        RSpecElement(RSpecElements.NODE, 'node', '//node'),
        RSpecElement(RSpecElements.SLIVER, 'sliver', '//node/sliver'),
    ] 
    template = '<RSpec type="%s"></RSpec>' % type

if __name__ == '__main__':
    from sfa.rspecs.rspec import RSpec
    from sfa.rspecs.rspec_elements import *
    r = RSpec('/tmp/resources.rspec')
    r.load_rspec_elements(SFAv1.elements)
    print r.get(RSpecElements.NODE)
