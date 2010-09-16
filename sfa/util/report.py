def trace(x, logger=None):
    if logger:
        logger.info(x)
    else:
        print x

def error(x, logger=None):
    if logger:
        logger.error(x)
    else:    
        print x
