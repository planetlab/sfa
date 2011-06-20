#!/usr/bin/python

import os, sys
import traceback
import logging, logging.handlers

CRITICAL=logging.CRITICAL
ERROR=logging.ERROR
WARNING=logging.WARNING
INFO=logging.INFO
DEBUG=logging.DEBUG

# a logger that can handle tracebacks 
class _SfaLogger:
    def __init__ (self,logfile=None,loggername=None,level=logging.INFO):
        # default is to locate loggername from the logfile if avail.
        if not logfile:
            loggername='console'
            handler=logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        else:
            if not loggername:
                loggername=os.path.basename(logfile)
            try:
                handler=logging.handlers.RotatingFileHandler(logfile,maxBytes=1000000, backupCount=5) 
            except IOError:
                # This is usually a permissions error becaue the file is
                # owned by root, but httpd is trying to access it.
                tmplogfile=os.getenv("TMPDIR", "/tmp") + os.path.sep + os.path.basename(logfile)
                handler=logging.handlers.RotatingFileHandler(tmplogfile,maxBytes=1000000, backupCount=5) 
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger=logging.getLogger(loggername)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.loggername=loggername

    def setLevel(self,level):
        self.logger.setLevel(level)

    # shorthand to avoid having to import logging all over the place
    def setLevelDebug(self):
        self.logger.setLevel(logging.DEBUG)

    # define a verbose option with s/t like
    # parser.add_option("-v", "--verbose", action="count", dest="verbose", default=0)
    # and pass the coresponding options.verbose to this method to adjust level
    def setLevelFromOptVerbose(self,verbose):
        if verbose==0:
            self.logger.setLevel(logging.WARNING)
        elif verbose==1:
            self.logger.setLevel(logging.INFO)
        elif verbose==2:
            self.logger.setLevel(logging.DEBUG)

    ####################
    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)
        
    def warn(self, msg):
        self.logger.warn(msg)
   
    def error(self, msg):
        self.logger.error(msg)    
 
    def critical(self, msg):
        self.logger.critical(msg)

    # logs an exception - use in an except statement
    def log_exc(self,message):
        self.error("%s BEG TRACEBACK"%message+"\n"+traceback.format_exc().strip("\n"))
        self.error("%s END TRACEBACK"%message)
    
    def log_exc_critical(self,message):
        self.critical("%s BEG TRACEBACK"%message+"\n"+traceback.format_exc().strip("\n"))
        self.critical("%s END TRACEBACK"%message)
    
    # for investigation purposes, can be placed anywhere
    def log_stack(self,message):
        to_log="".join(traceback.format_stack())
        self.debug("%s BEG STACK"%message+"\n"+to_log)
        self.debug("%s END STACK"%message)

####################
# import-related operations go in this file
_import_logger=_SfaLogger(logfile='/var/log/sfa_import.log')
# servers log into /var/log/sfa.log
_server_logger=_SfaLogger(logfile='/var/log/sfa.log')
## clients use the console
#_console_logger=_SfaLogger()

# default is to use the server-side logger
#_the_logger=_server_logger

# clients would change the default by issuing one of these call
#def sfa_logger_goes_to_console():
#    current_module=sys.modules[globals()['__name__']]
#    current_module._the_logger=_console_logger
#
# clients would change the default by issuing one of these call
#def sfa_logger_goes_to_import():
#    current_module=sys.modules[globals()['__name__']]
#    current_module._the_logger=_import_logger

# this is how to retrieve the 'right' logger
def sfa_logger():
    return _server_logger

########################################
import time

def profile(logger):
    """
    Prints the runtime of the specified callable. Use as a decorator, e.g.,
    
    @profile(logger)
    def foo(...):
        ...
    """
    def logger_profile(callable):
        def wrapper(*args, **kwds):
            start = time.time()
            result = callable(*args, **kwds)
            end = time.time()
            args = map(str, args)
            args += ["%s = %s" % (name, str(value)) for (name, value) in kwds.iteritems()]
            # should probably use debug, but then debug is not always enabled
            logger.info("PROFILED %s (%s): %.02f s" % (callable.__name__, ", ".join(args), end - start))
            return result
        return wrapper
    return logger_profile


if __name__ == '__main__': 
    print 'testing sfalogging into logger.log'
    logger=_SfaLogger('logger.log')
    logger.critical("logger.critical")
    logger.error("logger.error")
    logger.warning("logger.warning")
    logger.info("logger.info")
    logger.debug("logger.debug")
    logger.setLevel(logging.DEBUG)
    logger.debug("logger.debug again")
    
    #sfa_logger_goes_to_console()
    my_logger=sfa_logger()
    my_logger.info("redirected to console")

    @profile(my_logger)
    def sleep(seconds = 1):
        time.sleep(seconds)

    my_logger.info('console.info')
    sleep(0.5)
    my_logger.setLevel(logging.DEBUG)
    sleep(0.25)

