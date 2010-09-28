import logging
import os
import traceback

#SFA access log initialization
TMPDIR = os.getenv("TMPDIR", "/tmp")
SFA_HTTPD_ACCESS_LOGFILE = TMPDIR + "/" + 'sfa_httpd_access.log'
SFA_ACCESS_LOGFILE='/var/log/sfa_access.log'
logger=logging.getLogger()
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

try:
    logfile=logging.FileHandler(SFA_ACCESS_LOGFILE)
except IOError:
    # This is usually a permissions error becaue the file is
    # owned by root, but httpd is trying to access it.
    logfile=logging.FileHandler(SFA_HTTPD_ACCESS_LOGFILE)
    
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logfile.setFormatter(formatter)
logger.addHandler(logfile)
def get_sfa_logger():
    return logger

# logs an exception - use in an except statement
def log_exc(message):
    logger.error("%s BEG TRACEBACK"%message+"\n"+traceback.format_exc().strip("\n"))
    logger.error("%s END TRACEBACK"%message)
    

# for investigation purposes, can be placed anywhere
def log_stack(message):
    to_log="".join(traceback.format_stack())
    logger.debug("%s BEG STACK"%message+"\n"+to_log)
    logger.debug("%s END STACK"%message)
    

