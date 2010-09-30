#!/usr/bin/python

import os
import traceback
import logging, logging.handlers

class SfaLogging:
    def __init__ (self,logfile,name=None,level=logging.INFO):
        # default is to locate logger name from the logfile
        if not name:
            name=os.path.basename(logfile)
        self.logger=logging.getLogger(name)
        self.logger.setLevel(level)
        try:
            handler=logging.handlers.RotatingFileHandler(logfile,maxBytes=1000000, backupCount=5) 
        except IOError:
            # This is usually a permissions error becaue the file is
            # owned by root, but httpd is trying to access it.
            tmplogfile=os.getenv("TMPDIR", "/tmp") + os.path.sep + os.path.basename(logfile)
            handler=logging.handlers.RotatingFileHandler(tmplogfile,maxBytes=1000000, backupCount=5) 
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def wrap(fun):
        def wrapped(self,msg,*args,**kwds):
            native=getattr(self.logger,fun.__name__)
            return native(msg,*args,**kwds)
        #wrapped.__doc__=native.__doc__
        return wrapped

    def setLevel(self,level):
        self.logger.setLevel(level)

    @wrap
    def critical(): pass
    @wrap
    def error(): pass
    @wrap
    def warning(): pass
    @wrap
    def info(): pass
    @wrap
    def debug(): pass
    
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

sfa_logger=SfaLogging(logfile='/var/log/sfa.log')
sfa_import_logger=SfaLogging(logfile='/var/log/sfa_import.log')


########################################
import time

def profile(callable):
    """
    Prints the runtime of the specified callable. Use as a decorator, e.g.,

        @profile
        def foo(...):
            ...

    Or, equivalently,

        def foo(...):
            ...
        foo = profile(foo)

    Or inline:

        result = profile(foo)(...)
    """

    def wrapper(*args, **kwds):
        start = time.time()
        result = callable(*args, **kwds)
        end = time.time()
        args = map(str, args)
        args += ["%s = %s" % (name, str(value)) for (name, value) in kwds.items()]
        sfa_logger.debug("%s (%s): %.02f s" % (callable.__name__, ", ".join(args), end - start))
        return result

    return wrapper

if __name__ == '__main__': 
    print 'testing sfalogging into logger.log'
    global sfa_logger
    sfa_logger=SfaLogging('logger.log')
    sfa_logger.critical("logger.critical")
    sfa_logger.error("logger.error")
    sfa_logger.warning("logger.warning")
    sfa_logger.info("logger.info")
    sfa_logger.debug("logger.debug")
    sfa_logger.setLevel(logging.DEBUG)
    sfa_logger.debug("logger.debug again")

    @profile
    def sleep(seconds = 1):
        time.sleep(seconds)

    sleep(1)
