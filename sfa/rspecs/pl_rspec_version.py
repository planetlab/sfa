
ad_rspec_versions = [
     { 'type':  'ProtoGENI',
       'version': '2',
       'schema': 'http://www.protogeni.net/resources/rspec/2/request.xsd',
       'namespace': 'http://www.protogeni.net/resources/rspec/2',
       'extenstions':  [
         'http://www.protogeni.net/resources/rspec/ext/gre-tunnel/1',
         'http://www.protogeni.net/resources/rspec/ext/other-ext/3']
    },
    { 'type': 'SFA',
      'version': '1',
      'schema': [],
      'namespace': [],
      'extensions': []
    }
]

request_rspec_versions = ad_rspec_versions

default_rspec_version = { 'type': 'SFA', 'version': '1' }

supported_rspecs = {'ad_rspec_versions': ad_rspec_versions,
                    'request_rspec_versions': request_rspec_versions,
                    'default_ad_rspec': default_rspec_version}

