from __future__ import with_statement 
from sfa.util.faults import *
from sfa.util.namespace import *
from sfa.util.rspec import RSpec
from sfa.server.registry import Registries
from sfa.plc.nodes import *

import boto
from boto.ec2.regioninfo import RegionInfo
from boto.exception import EC2ResponseError
from ConfigParser import ConfigParser
from xmlbuilder import XMLBuilder
from xml.etree import ElementTree as ET

import sys
import os

# The data structure used to represent a cloud.
# It contains the cloud name, its ip address, image information,
# key pairs, and clusters information.
cloud = {}

##
# Initialize the aggregate manager by reading a configuration file.
#
def init_server():
    configParser = ConfigParser()
    configParser.read(['/etc/sfa/eucalyptus_aggregate.conf', 'eucalyptus_aggregate.conf'])
    if len(configParser.sections()) < 1:
        print >>sys.stderr, 'No cloud defined in the config file'
        raise 'Cannot find cloud definition in configuration file.'

    # Only read the first section.
    cloudSec = configParser.sections()[0]
    cloud['name'] = cloudSec
    cloud['access_key'] = configParser.get(cloudSec, 'access_key')
    cloud['secret_key'] = configParser.get(cloudSec, 'secret_key')
    cloud['cloud_url']  = configParser.get(cloudSec, 'cloud_url')
    cloudURL = cloud['cloud_url']
    if cloudURL.find('https://') >= 0:
        cloudURL = cloudURL.replace('https://', '')
    elif cloudURL.find('http://') >= 0:
        cloudURL = cloudURL.replace('http://', '')
    (cloud['ip'], parts) = cloudURL.split(':')

##
# Creates a connection to Eucalytpus. This function is inspired by 
# the make_connection() in Euca2ools.
#
# @return A connection object or None
#
def getEucaConnection():
    global cloud
    accessKey = cloud['access_key']
    secretKey = cloud['secret_key']
    eucaURL   = cloud['cloud_url']
    useSSL    = False
    srvPath   = '/'
    eucaPort  = 8773

    if not accessKey or not secretKey or not eucaURL:
        print >>sys.stderr, 'Please set ALL of the required environment ' \
                            'variables by sourcing the eucarc file.'
        return None
    
    # Split the url into parts
    if eucaURL.find('https://') >= 0:
        useSSL  = True
        eucaURL = eucaURL.replace('https://', '')
    elif eucaURL.find('http://') >= 0:
        useSSL  = False
        eucaURL = eucaURL.replace('http://', '')
    (eucaHost, parts) = eucaURL.split(':')
    if len(parts) > 1:
        parts = parts.split('/')
        eucaPort = int(parts[0])
        parts = parts[1:]
        srvPath = '/'.join(parts)

    return boto.connect_ec2(aws_access_key_id=accessKey,
                            aws_secret_access_key=secretKey,
                            is_secure=useSSL,
                            region=RegionInfo(None, 'eucalyptus', eucaHost), 
                            port=eucaPort,
                            path=srvPath)

##
# A class that builds the RSpec for Eucalyptus.
#
class EucaRSpecBuilder(object):
    ##
    # Initizes a RSpec builder
    #
    # @param cloud A dictionary containing data about a 
    #              cloud (ex. clusters, ip)
    def __init__(self, cloud):
        self.eucaRSpec = XMLBuilder()
        self.cloudInfo = cloud

    ##
    # Creates the ClusterSpec stanza.
    #
    # @param clusters Clusters information.
    #
    def __clustersXML(self, clusters):
        xml = self.eucaRSpec
        for cluster in clusters:
            instances = cluster['instances']
            with xml.ClusterSpec(id=cluster['name'], ip=cluster['ip']):
                for inst in instances:
                    with xml.Node(instanceType=inst[0]):
                        with xml.FreeSlot:
                            xml << str(inst[1])
                        with xml.MaxAllow:
                            xml << str(inst[2])
                        with xml.NumCore:
                            xml << str(inst[3])
                        with xml.Mem:
                            xml << str(inst[4])
                        with xml.DiskSpace(unit='GB'):
                            xml << str(inst[5])

    ##
    # Creates the Images stanza.
    #
    # @param images A list of images in Eucalyptus.
    #
    def __imagesXML(self, images):
        xml = self.eucaRSpec
        with xml.Images:
            for image in images:
                with xml.Image(id=image.id):
                    with xml.Type:
                        xml << image.type
                    with xml.Arch:
                        xml << image.architecture
                    with xml.State:
                        xml << image.state
                    with xml.location:
                        xml << image.location

    ##
    # Creates the KeyPairs stanza.
    #
    # @param keypairs A list of key pairs in Eucalyptus.
    #
    def __keyPairsXML(self, keypairs):
        xml = self.eucaRSpec
        with xml.KeyPairs:
            for key in keypairs:
                with xml.Key:
                    xml << key.name

    ##
    # Generates the RSpec.
    #
    def toXML(self):
        if not self.cloudInfo:
            print >>sys.stderr, 'No cloud information'
            return ''

        xml = self.eucaRSpec
        cloud = self.cloudInfo
        with xml.RSpec(name='eucalyptus'):
            with xml.Capacity:
                with xml.CloudSpec(id=cloud['name'], ip=cloud['ip']):
                    self.__keyPairsXML(cloud['keypairs'])
                    self.__imagesXML(cloud['images'])
                    self.__clustersXML(cloud['clusters'])
            with xml.Request:
                with xml.CloudSpec(id=cloud['name'], ip=cloud['ip']):
                    with xml.Credential(type='X509'):
                        xml << 'cred'
                    with xml.Node(instanceType='m1.small', number='1'):
                        with xml.Kernel:
                            xml << 'eki-F26610C6'
                        with xml.Ramdisk:
                            xml << ''
                        with xml.DiskImage:
                            xml << 'emi-88760F45'
                        with xml.Key:
                            xml << 'cortex'
        return str(xml)

##
# A parser to parse the output of availability-zones.
#
# Note: Only one cluster is supported. If more than one, this will
#       not work.
#
class ZoneResultParser(object):
    def __init__(self, zones):
        self.zones = zones

    def parse(self):
        if len(self.zones) < 3:
            return
        clusterList = []
        cluster = {} 
        instList = []

        cluster['name'] = self.zones[0].name
        cluster['ip']   = self.zones[0].state

        for i in range(2, len(self.zones)):
            currZone = self.zones[i]
            instType = currZone.name.split()[1]

            stateString = currZone.state.split('/')
            rscString   = stateString[1].split()

            instFree      = int(stateString[0])
            instMax       = int(rscString[0])
            instNumCpu    = int(rscString[1])
            instRam       = int(rscString[2])
            instDiskSpace = int(rscString[3])

            instTuple = (instType, instFree, instMax, instNumCpu, instRam, instDiskSpace)
            instList.append(instTuple)
        cluster['instances'] = instList
        clusterList.append(cluster)

        return clusterList

def get_rspec(api, hrn, origin_hrn):
    global cloud
    conn = getEucaConnection()

    if not conn:
        print >>sys.stderr, 'Error: Cannot make a connection to the cloud'
        return ''

    try:
        # Zones
        zones = conn.get_all_zones(['verbose'])
        p = ZoneResultParser(zones)
        clusters = p.parse()
        cloud['clusters'] = clusters
        
        # Images
        images = conn.get_all_images()
        cloud['images'] = images

        # Key Pairs
        keyPairs = conn.get_all_key_pairs()
        cloud['keypairs'] = keyPairs
    except EC2ResponseError:
        errTree = ET.fromstring(EC2ResponseError.body)
        errMsgE = errTree.find('.//Message')
        print >>sys.stderr, errMsgE.text

    rspec = EucaRSpecBuilder(cloud).toXML()

    return rspec

"""
Hook called via 'sfi.py create'
"""
def create_slice(api, hrn, xml):
    return True

def main():
    #r = RSpec()
    #r.parseFile(sys.argv[1])
    #rspec = r.toDict()
    #create_slice(None,'plc',rspec)
    rspec = get_rspec('euca', 'hrn:euca', 'oring_hrn')
    print rspec

if __name__ == "__main__":
    main()

