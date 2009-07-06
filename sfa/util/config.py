##
# Geniwrapper Configuration Info
#
# This module holds configuration parameters for geniwrapper. There are two
# main pieces of information that are used: the database connection and
# the PLCAPI connection
##

##
# Geniwrapper uses a MYSQL database to store records. This database may be
# co-located with the PLC database, or it may be a separate database. The
# following parameters define the connection to the database.
#
# Note that Geniwrapper does not access any of the PLC databases directly via
# a mysql connection; All PLC databases are accessed via PLCAPI.

### $Id$
### $URL$

import os.path
import traceback

from sfa.util.debug import log

class Config:
    """
    Parse the bash/Python/PHP version of the configuration file. Very
    fast but no type conversions.
    """

    def __init__(self, config_file = "/etc/sfa/sfa_config"):
        self.config_file = None
        self.config_path = None
        self.load(config_file)

    def load(self, config_file):
        try:
            execfile(config_file, self.__dict__)
            self.config_file = config_file
            self.config_path = os.path.dirname(config_file)
        except IOError, e:
            raise IOError, "Could not find the configuration file: %s" % config_file


def get_default_dbinfo():
    config = Config()
    dbinfo={
        'dbname' : config.SFA_PLC_DB_NAME,
        'address' : config.SFA_PLC_DB_HOST,
        'port' : config.SFA_PLC_DB_PORT,
        'user' : config.SFA_PLC_DB_USER,
        'password' : config.SFA_PLC_DB_PASSWORD
        }
    return dbinfo

##
# Geniwrapper uses a PLCAPI connection to perform operations on the registry,
# such as creating and deleting slices. This connection requires an account
# on the PLC server with full administrator access.
#
# The Url parameter controls whether the connection uses PLCAPI directly (i.e.
# Geniwrapper is located on the same machine as PLC), or uses a XMLRPC connection
# to the PLC machine. If you wish to use the API directly, then remove the Url
# field from the dictionary. 

def get_pl_auth():
    config = Config()
    pl_auth = {
        'Username': config.SFA_PLC_USER,
        'AuthMethod': 'capability',
        'AuthString':  config.SFA_PLC_PASSWORD,
        "Url": config.SFA_PLC_URL
        }
    return pl_auth
