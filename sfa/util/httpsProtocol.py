import httplib
import socket

# wrapper around standartd https modules. Properly supports timeouts.  

class HTTPSConnection(httplib.HTTPSConnection):
    def __init__(self, host, port=None, key_file=None, cert_file=None,
                 strict=None, timeout = None):
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file, strict)
        self.timeout = float(timeout)

    def connect(self):
        """Connect to a host on a given (SSL) port."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        ssl = socket.ssl(sock, self.key_file, self.cert_file)
        self.sock = httplib.FakeSocket(sock, ssl)

class HTTPS(httplib.HTTPS):
   def __init__(self, host='', port=None, key_file=None, cert_file=None,
                     strict=None, timeout = None):
        # urf. compensate for bad input.
        if port == 0:
            port = None
        self._setup(HTTPSConnection(host, port, key_file, cert_file, strict, timeout))

        # we never actually use these for anything, but we keep them
        # here for compatibility with post-1.5.2 CVS.
        self.key_file = key_file
        self.cert_file = cert_file

