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
            #loggername='console'
            #handler=logging.StreamHandler()
            #handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
            logfile = "/var/log/sfa.log"

        if not loggername:
            loggername=os.path.basename(logfile)
        try:
            handler=logging.handlers.RotatingFileHandler(logfile,maxBytes=1000000, backupCount=5) 
        except IOError:
            # This is usually a permissions error becaue the file is
            # owned by root, but httpd is trying to access it.
            tmplogfile=os.getenv("TMPDIR", "/tmp") + os.path.sep + os.path.basename(logfile)
            # In strange uses, 2 users on same machine might use same code,
            # meaning they would clobber each others files
            # We could (a) rename the tmplogfile, or (b)
            # just log to the console in that case.
            # Here we default to the console.
            if os.path.exists(tmplogfile) and not os.access(tmplogfile,os.W_OK):
                loggername = loggername + "-console"
                handler = logging.StreamHandler()
            else:
                handler=logging.handlers.RotatingFileHandler(tmplogfile,maxBytes=1000000, backupCount=5) 
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger=logging.getLogger(loggername)
        self.logger.setLevel(level)
        # check if logger already has the handler we're about to add
        handler_exists = False
        for l_handler in self.logger.handlers:
            if l_handler.baseFilename == handler.baseFilename and \
               l_handler.level == handler.level:
                handler_exists = True 

        if not handler_exists:
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

    # some code is using logger.warn(), some is using logger.warning()
    def warning(self, msg):
        self.logger.warning(msg)
   
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

    def enable_console(self, stream=sys.stdout):
        formatter = logging.Formatter("%(message)s")
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


info_logger = _SfaLogger(loggername='info', level=logging.INFO)
debug_logger = _SfaLogger(loggername='debug', level=logging.DEBUG)
warn_logger = _SfaLogger(loggername='warning', level=logging.WARNING)
error_logger = _SfaLogger(loggername='error', level=logging.ERROR)
critical_logger = _SfaLogger(loggername='critical', level=logging.CRITICAL)
logger = info_logger
sfi_logger = _SfaLogger(logfile=os.path.expanduser("~/.sfi/")+'sfi.log',loggername='sfilog', level=logging.DEBUG)
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
    logger1=_SfaLogger('logger.log', loggername='std(info)')
    logger2=_SfaLogger('logger.log', loggername='error', level=logging.ERROR)
    logger3=_SfaLogger('logger.log', loggername='debug', level=logging.DEBUG)
    
    for (logger,msg) in [ (logger1,"std(info)"),(logger2,"error"),(logger3,"debug")]:
        
        print "====================",msg, logger.logger.handlers
   
        logger.enable_console()
        logger.critical("logger.critical")
        logger.error("logger.error")
        logger.warn("logger.warning")
        logger.info("logger.info")
        logger.debug("logger.debug")
        logger.setLevel(logging.DEBUG)
        logger.debug("logger.debug again")
    
        @profile(logger)
        def sleep(seconds = 1):
            time.sleep(seconds)

        logger.info('console.info')
        sleep(0.5)
        logger.setLevel(logging.DEBUG)
        sleep(0.25)

