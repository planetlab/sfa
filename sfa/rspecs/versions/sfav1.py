from sfa.rspecs.rspec_elements import RSpecElement, RSpecElements

class SFAv1:
    format = 'SFA'
    type = '*'
    version = '1'
    schema = None
    namespaces = {}
    elements = [
        RSpecElement(RSpecElements.NETWORK, 'network', '//network'),
        RSpecElement(RSpecElements.NODE, 'node', '//node'),
        RSpecElement(RSpecElements.SLIVER, 'sliver', '//node/sliver'),
    ] 


if __name__ == '__main__':
    from sfa.rspecs.rspec import RSpec
    from sfa.rspecs.rspec_elements import *
    r = RSpec('/tmp/resources.rspec')
    r.load_rspec_elements(SFAv1.elements)
    print r.get(RSpecElements.NODE)
