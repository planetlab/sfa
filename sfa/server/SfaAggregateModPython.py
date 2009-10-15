#
# Apache mod_python interface
#
# Aaron Klingaman <alk@absarokasoft.com>
# Mark Huang <mlhuang@cs.princeton.edu>
#
# Copyright (C) 2004-2006 The Trustees of Princeton University
#

import sys
import traceback
import xmlrpclib
from mod_python import apache

from sfa.plc.api import GeniAPI

api = GeniAPI(interface='aggregate')

class unbuffered:
    """
    Write to /var/log/httpd/error_log. See

    http://www.modpython.org/FAQ/faqw.py?req=edit&file=faq02.003.htp
    """

    def write(self, data):
        sys.stderr.write(data)
        sys.stderr.flush()

#log = unbuffered()

def handler(req):
    try:
        if req.method != "POST":
            req.content_type = "text/html"
            req.send_http_header()
            req.write("""
<html><head>
<title>SFA Aggregate API XML-RPC/SOAP Interface</title>
</head><body>
<h1>SFA Aggregate API XML-RPC/SOAP Interface</h1>
<p>Please use XML-RPC or SOAP to access the SFA API.</p>
</body></html>
""")
            return apache.OK

        # Read request
        request = req.read(int(req.headers_in['content-length']))

        # mod_python < 3.2: The IP address portion of remote_addr is
        # incorrect (always 0.0.0.0) when IPv6 is enabled.
        # http://issues.apache.org/jira/browse/MODPYTHON-64?page=all
        (remote_ip, remote_port) = req.connection.remote_addr
        remote_addr = (req.connection.remote_ip, remote_port)

        # Handle request
        response = api.handle(remote_addr, request)

        # Write response
        req.content_type = "text/xml; charset=" + api.encoding
        req.send_http_header()
        req.write(response)

        return apache.OK

    except Exception, err:
        # Log error in /var/log/httpd/(ssl_)?error_log
        print >> log, err, traceback.format_exc()
        return apache.HTTP_INTERNAL_SERVER_ERROR