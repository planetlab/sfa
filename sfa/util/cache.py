#
# This module implements general purpose caching system
#
from __future__ import with_statement
import time
import threading
from datetime import datetime

# maximum lifetime of cached data (in seconds) 
MAX_CACHE_TTL = 60 * 60

class CacheData:

    data = None
    created = None
    expires = None
    lock = None

    def __init__(self, data, ttl = MAX_CACHE_TTL):
        self.lock = threading.RLock()
        self.data = data
        self.renew(ttl)

    def is_expired(self):
        return time.time() > self.expires

    def get_created_date(self):
        return str(datetime.fromtimestamp(self.created))

    def get_expires_date(self):
        return str(datetime.fromtimestamp(self.expires))

    def renew(self, ttl = MAX_CACHE_TTL):
        self.created = time.time()
        self.expires = self.created + ttl   
       
    def set_data(self, data, renew=True, ttl = MAX_CACHE_TTL):
        with self.lock: 
            self.data = data
            if renew:
                self.renew(ttl)
    
    def get_data(self):
        return self.data

class Cache:

    cache  = {}
    lock = threading.RLock()
   
    def add(self, key, value, ttl = MAX_CACHE_TTL):
        with self.lock:
            if self.cache.has_key(key):
                self.cache[key].set_data(value, ttl=ttl)
            else:
                self.cache[key] = CacheData(value, ttl)
           
    def get(self, key):
        data = self.cache.get(key)
        if not data or data.is_expired():
            return None 
        return data.get_data()
