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

import os
import sys

# If we have been checked out into a directory at the same
# level as myplc, where plc_config.py lives. If we are in a
# MyPLC environment, plc_config.py has already been installed
# in site-packages.
myplc = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + \
        os.sep + "myplc"

class Config:
    """
    Parse the bash/Python/PHP version of the configuration file. Very
    fast but no type conversions.
    """

    def __init__(self, file = "/etc/planetlab/plc_config"):
        # Load plc_config
        try:
            execfile(file, self.__dict__)
        except:
            # Try myplc directory
            try:
                execfile(myplc + os.sep + "plc_config", self.__dict__)
            except:
                raise PLCAPIError("Could not find plc_config in " + \
                                  file + ", " + \
                                  myplc + os.sep + "plc_config")


plcConfig = Config()

def get_default_dbinfo():
    dbinfo = { 'dbname' : plcConfig.PLC_DB_NAME,
        'address' : plcConfig.PLC_DB_HOST,
        'port' : plcConfig.PLC_DB_PORT,
        'user' : plcConfig.PLC_DB_USER,
        'password' : plcConfig.PLC_DB_PASSWORD
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
    pl_auth = {'Username': plcConfig.PLC_API_MAINTENANCE_USER,
        'AuthMethod': 'capability',
        'AuthString':  plcConfig.PLC_MAINTENANCE_PASSWORD,
        "Url": 'https://%s:%s%s' %(plcConfig.PLC_API_HOST, plcConfig.PLC_API_PORT, plcConfig.PLC_API_PATH)
    }

    return pl_auth
