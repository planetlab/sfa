import logging

#SFA access log initialization

SFA_ACCESS_LOGFILE='/var/log/sfa_access.log'
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logfile=logging.FileHandler(SFA_ACCESS_LOGFILE)
logfile=logging.FileHandler(SFA_HTTPD_ACCESS_LOGFILE)
formatter = logging.Formatter("%(asctime)s - %(message)s")
logfile.setFormatter(formatter)
logger.addHandler(logfile)

def get_sfa_logger():
    return logger
