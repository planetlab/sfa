import dateutil.parser
import datetime

from sfa.util.sfalogging import logger

def utcparse(string):
    """ Translate a string into a time using dateutil.parser.parse but make sure it's in UTC time and strip
    the timezone, so that it's compatible with normal datetime.datetime objects"""
    
    if isinstance (string, datetime.datetime):
        logger.warn ("argument to utcparse already a datetime - doing nothing")
        return string
    t = dateutil.parser.parse(string)
    if t.utcoffset() is not None:
        t = t.utcoffset() + t.replace(tzinfo=None)
    return t
