from sfa.rspecs.versions.pgv2 import PGv2

class PGv3(PGv2):
    type = 'GENI'
    content_type = 'ad'
    version = '3'
    schema = 'http://www.geni.net/resources/rspec/3/ad.xsd'
    namespace = 'http://www.geni.net/resources/rspec/3'
    extensions = {
        'flack': "http://www.protogeni.net/resources/rspec/ext/flack/1",
        'planetlab': "http://www.planet-lab.org/resources/sfa/ext/planetlab/1",
    }
    namespaces = dict(extensions.items() + [('default', namespace)])
    elements = []


class PGv3Ad(PGv3):
    enabled = True
    content_type = 'ad'
    schema = 'http://www.geni.net/resources/rspec/3/ad.xsd'
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/ad.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="advertisement"/>'

class PGv3Request(PGv3):
    enabled = True
    content_type = 'request'
    schema = 'http://www.geni.net/resources/rspec/3/request.xsd'
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/request.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="request"/>'

class PGv2Manifest(PGv3):
    enabled = True
    content_type = 'manifest'
    schema = 'http://www.geni.net/resources/rspec/3/manifest.xsd'
    template = '<rspec xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.geni.net/resources/rspec/3" xsi:schemaLocation="http://www.geni.net/resources/rspec/3 http://www.geni.net/resources/rspec/3/manifest.xsd" xmlns:flack="http://www.protogeni.net/resources/rspec/ext/flack/1" xmlns:planetlab="http://www.planet-lab.org/resources/sfa/ext/planetlab/1" type="manifest"/>'
     
