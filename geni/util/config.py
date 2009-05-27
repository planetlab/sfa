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

from os.path import join,dirname,basename,abspath
from geni.util.debug import log
import traceback

geni =  join(dirname(dirname(dirname(abspath(__file__)))), "geni")

class Config:
    """
    Parse the bash/Python/PHP version of the configuration file. Very
    fast but no type conversions.
    """

    def __init__(self, filepath = "/etc/geni/geni_config"):
        # Load plc_config

        loaded = False
        path = dirname(abspath(__file__))
        self.path = path
        self.basepath = dirname(self.path)
        filename = basename(filepath)
        alt_file = join(self.path, 'util', filename)
        geni_file = join(geni, 'util', filename)
        files = [filepath, alt_file, geni_file]

        for config_file in files:
            try:
                execfile(config_file, self.__dict__)
                loaded = True
                self.config_file = config_file
                break
            except:
                pass

        if not loaded:
            raise Exception, "Could not find config in " + ", ".join(files)

        # set up some useful variables

    def load(self, filepath):
        try:
            execfile(filepath, self.__dict__)
        except:
            raise Exception, "Could not find config in " + filepath

plcConfig = Config("/etc/planetlab/plc_config")

def get_default_dbinfo():
    dbinfo={ 'dbname' : plcConfig.PLC_DB_NAME,
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
    'AuthString':  plcConfig.PLC_API_MAINTENANCE_PASSWORD,
    "Url": 'https://%s:%s%s' %(plcConfig.PLC_API_HOST, plcConfig.PLC_API_PORT, plcConfig.PLC_API_PATH)
    }

    return pl_auth
