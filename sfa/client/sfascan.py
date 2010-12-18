#!/usr/bin/python

import socket
import re

from sfa.client.sfi import Sfi
from sfa.util.sfalogging import sfa_logger,sfa_logger_goes_to_console
import sfa.util.xmlrpcprotocol as xmlrpcprotocol

m_url_with_proto=re.compile("\w+://(?P<hostname>[\w\-\.]+):(?P<port>[0-9]+)/.*")
m_url_without_proto=re.compile("(?P<hostname>[\w\-\.]+):(?P<port>[0-9]+).*")
def url_to_hostname_port (url):
    print 'url',url
    match=m_url_with_proto.match(url)
    if match:
        return (match.group('hostname'),match.group('port'))
    match=m_url_without_proto.match(url)
    if match:
        return (match.group('hostname'),match.group('port'))
    return ('undefined','???')

###
class Interface:
    def __init__ (self,url,name=None):
        self.names=[]
        self.set_name(name)
        try:
            (self.hostname,self.port)=url_to_hostname_port(url)
            self.ip=socket.gethostbyname(self.hostname)
            self.probed=False
        except:
            import traceback
            traceback.print_exc()
            self.hostname="undefined"
            self.port="???"
            self.probed=True
            self._version={}

    def equal (self,against):
        return (self.ip == against.ip) and (self.port == against.port)

    def set_name (self,name):
        if name and name not in self.names: 
            self.names.append(name)

    def url(self):
        return "http://%s:%s"%(self.hostname,self.port)

    # connect to server and trigger GetVersion
    def get_version(self):
        if self.probed:
            return self._version
        # dummy to meet Sfi's expectations for its 'options' field
        class DummyOptions:
            pass
        options=DummyOptions()
        options.verbose=False
        try:
            client=Sfi(options)
            client.read_config()
            key_file = client.get_key_file()
            cert_file = client.get_cert_file(key_file)
            url="http://%s:%s/"%(self.hostname,self.port)
            sfa_logger().info('issuing get version at %s'%url)
            server=xmlrpcprotocol.get_server(url, key_file, cert_file, options)
            self._version=server.GetVersion()
#            pdb.set_trace()
        except:
            self._version={}
        self.probed=True
        return self._version

class SfaScan:

    # provide the entry points (a list of interfaces)
    def __init__ (self):
        pass

    # scan from the given interfaces as entry points
    def scan(self,interfaces):
        import pdb
#        pdb.set_trace()
        if not isinstance(interfaces,list):
            interfaces=[interfaces]
        # should add nodes, but with what name ?
        to_scan=interfaces
        scanned=[]
        def was_scanned (interface):
            for i in scanned:
                if interface.equal(i): return i
            return False
        # keep on looping until we reach a fixed point
        while to_scan:
            for interface in to_scan:
                version=interface.get_version()
                if 'peers' in version: 
                    for (next_name,next_url) in version['peers'].items():
                        # should add edge
                        next_interface=Interface(next_url)
                        seen_interface=was_scanned(next_interface)
                        if seen_interface:
                            # record name
                            seen_interface.set_name(next_name)
                        else:
                            sfa_logger().info('adding %s'%next_interface.url())
                            to_scan.append(next_interface)
                            
                scanned.append(interface)
                to_scan.remove(interface)
    

def main():
    sfa_logger_goes_to_console()
    scanner=SfaScan()
    entry=Interface("http://www.planet-lab.eu:12345/")
    scanner.scan(entry)

if __name__ == '__main__':
    main()
