import dateutil.parser

def utcparse(str):
    """ Translate a string into a time using dateutil.parser.parse but make sure it's in UTC time and strip
    the timezone, so that it's compatible with normal datetime.datetime objects"""
    
    t = dateutil.parser.parse(str)
    if not t.utcoffset() is None:
        t = t.utcoffset() + t.replace(tzinfo=None)
    return t
