#!/usr/bin/python
from sfa.util.sfalogging import sfa_logger


DEFAULT_FORMAT='sfa'
DEFAULT_VERSION_NUMBER=1
class RSpecVersion:

    format = None
    version = None
    schema = None
    namespace = None
    extensions = []

    def __init__(self, version_string):
        self.logger = sfa_logger() 
        self.parse_version_string(version_string)

    def parse_version_string(self, version_string):
        # version_raw is currently a string but will 
        # eventually be a struct.
        try:
            format_split = version_string.split(' ')
            format, version = format_split[0].lower(), format_split[1]
        except:
            self.logger.info("RSpecVersion: invalid rspec version string: %s , using default" \
                        % version_string)
            # invalid format. Just continue
            format, version = DEFAULT_FORMAT, DEFAULT_VERSION_NUMBER

        self.format = format
        self.version = version 
    

    def parse_version_struct(self, version_struct):
        try:
            pass
        except:
            format, version = DEFAULT_FORMAT, DEFAULT_VERSION_NUMBER
