#!/usr/bin/python
from sfa.util.sfalogging import _SfaLogger

class RSpecVersion(dict):

    fields = {'type': None,
              'version': None,
              'schema': None,
              'namespace': None,
              'extenstions': []
        }
    def __init__(self, version={}):
        
        self.logger = _SfaLogger('/var/log/sfa.log')
        dict.__init__(self, self.fields)

        if not version:
            from sfa.rspecs.sfa_rspec import sfa_rspec_version
            self.update(sfa_rspec_version)          
        elif isinstance(version, dict):
            self.update(version)
        elif isinstance(version, basestring):
            version_parts = version.split(' ')
            num_parts = len(version_parts)
            self['type'] = version_parts[0]
            if num_parts > 1:
                self['version'] = version_parts[1]
        else:
            logger.info("Unable to parse rspec version, using default")

    def get_version_name(self):
        return "%s %s" % (str(self['type']), str(self['version']))

if __name__ == '__main__':

    from sfa.rspecs.pl_rspec_version import ad_rspec_versions
    for version in [RSpecVersion(), 
                    RSpecVersion("SFA"), 
                    RSpecVersion("SFA 1"),
                    RSpecVersion(ad_rspec_versions[0])]: 
        print version.get_version_name() + ": " + str(version)

