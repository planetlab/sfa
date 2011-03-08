#!/usr/bin/python

import sys
import socket
import re

import pygraphviz

from optparse import OptionParser

from sfa.client.sfi import Sfi
from sfa.util.sfalogging import sfa_logger,sfa_logger_goes_to_console
import sfa.util.xmlrpcprotocol as xmlrpcprotocol

m_url_with_proto=re.compile("\w+://(?P<hostname>[\w\-\.]+):(?P<port>[0-9]+).*")
m_url_without_proto=re.compile("(?P<hostname>[\w\-\.]+):(?P<port>[0-9]+).*")
def url_to_hostname_port (url):
    match=m_url_with_proto.match(url)
    if match:
        return (match.group('hostname'),match.group('port'))
    match=m_url_without_proto.match(url)
    if match:
        return (match.group('hostname'),match.group('port'))
    return ('undefined','???')

###
class Interface:

    def __init__ (self,url):
        try:
            (self.hostname,self.port)=url_to_hostname_port(url)
            self.ip=socket.gethostbyname(self.hostname)
            self.probed=False
        except:
            import traceback
            traceback.print_exc()
            self.hostname="unknown"
            self.ip='0.0.0.0'
            self.port="???"
            self.probed=True
            self._version={}

    def url(self):
        return "http://%s:%s/"%(self.hostname,self.port)

    # this is used as a key for creating graph nodes and to avoid duplicates
    def uid (self):
        return "%s:%s"%(self.ip,self.port)

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
        except:
            self._version={}
        self.probed=True
        return self._version

    # default is for when we can't determine the type of the service
    # typically the server is down, or we can't authenticate, or it's too old code
    shapes = {"registry": "diamond", "slicemgr":"ellipse", "aggregate":"box", 'default':'plaintext'}

    def get_label(self):
        version=self.get_version()
        if 'hrn' not in version: return self.url()
        hrn=version['hrn']
        result=hrn
        if 'code_tag' in version: 
            result += " %s"%version['code_tag']
        if 'testbed' in version:
            # could not get so-called HTML-like labels to work
            #"<TABLE><TR><TD>%s</TD></TR><TR><TD>%s</TD></TR></TABLE>"%(result,version['testbed'])
            result += " (%s)"%version['testbed']
        return result

    def get_shape(self):
        default=Interface.shapes['default']
        try:
            version=self.get_version()
            return Interface.shapes.get(version['interface'],default)
        except:
            return default

class SfaScan:

    # provide the entry points (a list of interfaces)
    def __init__ (self):
        pass

    def graph (self,entry_points):
        graph=pygraphviz.AGraph(directed=True)
        self.scan(entry_points,graph)
        return graph
    
    # scan from the given interfaces as entry points
    def scan(self,interfaces,graph):
        if not isinstance(interfaces,list):
            interfaces=[interfaces]

        # remember node to interface mapping
        node2interface={}
        # add entry points right away using the interface uid's as a key
        to_scan=interfaces
        for i in interfaces: 
            graph.add_node(i.uid())
            node2interface[graph.get_node(i.uid())]=i
        scanned=[]
        # keep on looping until we reach a fixed point
        # don't worry about abels and shapes that will get fixed later on
        while to_scan:
            for interface in to_scan:
                # performing xmlrpc call
                version=interface.get_version()
                # 'sfa' is expected if the call succeeded at all
                # 'peers' is needed as well as AMs typically don't have peers
                if 'sfa' in version and 'peers' in version: 
                    # proceed with neighbours
                    for (next_name,next_url) in version['peers'].items():
                        next_interface=Interface(next_url)
                        # locate or create node in graph
                        try:
                            # if found, we're good with this one
                            next_node=graph.get_node(next_interface.uid())
                        except:
                            # otherwise, let's move on with it
                            graph.add_node(next_interface.uid())
                            next_node=graph.get_node(next_interface.uid())
                            node2interface[next_node]=next_interface
                            to_scan.append(next_interface)
                        graph.add_edge(interface.uid(),next_interface.uid())
                scanned.append(interface)
                to_scan.remove(interface)
            # we've scanned the whole graph, let's get the labels and shapes right
            for node in graph.nodes():
                interface=node2interface.get(node,None)
                if interface:
                    node.attr['label']=interface.get_label()
                    node.attr['shape']=interface.get_shape()
                    node.attr['href']=interface.url()
                else:
                    sfa_logger().info("MISSED interface with node %s"%node)
    

default_entry_points=["http://www.planet-lab.eu:12345/"]
default_outfiles=['sfa.png']

def main():
    sfa_logger_goes_to_console()
    parser=OptionParser()
    parser.add_option("-e","--entry",action='append',dest='entry_points',default=[],
                      help="Specify entry points - defaults are %r"%default_entry_points)
    parser.add_option("-o","--output",action='append',dest='outfiles',default=[],
                      help="Output filenames - defaults are %r"%default_outfiles)
    (options,args)=parser.parse_args()
    if args:
        parser.print_help()
        sys.exit(1)
    if not options.entry_points:
        options.entry_points=default_entry_points
    if not options.outfiles:
        options.outfiles=default_outfiles
    scanner=SfaScan()
    entries = [ Interface(entry) for entry in options.entry_points ]
    g=scanner.graph(entries)
    sfa_logger().info("creating layout")
    g.layout(prog='dot')
    for outfile in options.outfiles:
        sfa_logger().info("drawing in %s"%outfile)
        g.draw(outfile)
    sfa_logger().info("done")

if __name__ == '__main__':
    main()
