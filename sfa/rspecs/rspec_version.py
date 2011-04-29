#!/usr/bin/python
from sfa.util.sfalogging import sfa_logger

class RSpecVersion:

    format = None
    version = None
    schema = None
    namespace = None
    extensions = []

    def __init__(self, version_raw):
        self.logger = sfa_logger() 
        self.parse_version(version_raw)

    def parse_version(self, version_raw):
        # version_raw is currently a string but will 
        # eventually be a struct.
        try:
            format_split = version_raw.split(' ')
            format, version = format_split[0].lower(), format_split[1]
        except:
            self.logger.info("RSpecVersion: invalid rspec version: %s , using default" \
                        % version_raw)
            # invalid format. Just continue
            format, version = 'sfa', '1'

        self.format = format
        self.version = version 
    

                      
