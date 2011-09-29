from sfa.rspecs.rspec_version import BaseVersion
from sfa.rspecs.rspec_elements import RSpecElement, RSpecElements

class PGv2Ad(PGv2):
    enabled = True
    type = 'ProtoGENI'
    content_type = 'ad'
    version = '2'
    schema = 'http://www.protogeni.net/resources/rspec/2/ad.xsd'
    namespace = 'http://www.protogeni.net/resources/rspec/2' 
    extensions = { 
        'flack': "http://www.protogeni.net/resources/rspec/ext/flack/1",
        'planetlab': "http://www.planet-lab.org/resources/sfa/ext/planetlab/1", 
    }
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.protogeni.net/resources/rspec/2" xsi:schemaLocation="http://www.protogeni.net/resources/rspec/2 http://www.protogeni.net/resources/rspec/2/ad.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" />'      

class PGv2Request(PGv2):
    enabled = True
    type = 'ProtoGENI'
    content_type = 'request'
    version = '2'
    schema = 'http://www.protogeni.net/resources/rspec/2/request.xsd'
    namespace = 'http://www.protogeni.net/resources/rspec/2'
    extensions = {
        'flack': "http://www.protogeni.net/resources/rspec/ext/flack/1",
        'planetlab': "http://www.planet-lab.org/resources/sfa/ext/planetlab/1",
    }
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.protogeni.net/resources/rspec/2" xsi:schemaLocation="http://www.protogeni.net/resources/rspec/2 http://www.protogeni.net/resources/rspec/2/request.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" />'

class PGv2Manifest(PGv2):
    enabled = True
    type = 'ProtoGENI'
    content_type = 'manifest'
    version = '2'
    schema = 'http://www.protogeni.net/resources/rspec/2/manifest.xsd'
    namespace = 'http://www.protogeni.net/resources/rspec/2'
    extensions = {
        'flack': "http://www.protogeni.net/resources/rspec/ext/flack/1",
        'planetlab': "http://www.planet-lab.org/resources/sfa/ext/planetlab/1",
    }
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.protogeni.net/resources/rspec/2" xsi:schemaLocation="http://www.protogeni.net/resources/rspec/2 http://www.protogeni.net/resources/rspec/2/manifest.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" />'

class PGv2(BaseVersion):
    elements = [
        RSpecElement(RSpecElements.NETWORK, 'network', '//default:node[@component_manager_id][1]'),
        RSpecElement(RSpecElements.NODE, 'node', '//default:node | //node'),
        RSpecElement(RSpecElements.SLIVER, 'sliver', '//default:node/default:sliver_type | //node/sliver_type'),
    ]
 


if __name__ == '__main__':
    from sfa.rspecs.rspec import RSpec
    from sfa.rspecs.rspec_elements import *
    r = RSpec('/tmp/pg.rspec')
    r.load_rspec_elements(PGv2.elements)
    r.namespaces = PGv2.namespaces
    print r.get(RSpecElements.NODE)
