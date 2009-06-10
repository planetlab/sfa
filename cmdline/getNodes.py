#!/usr/bin/python
import sys
import os
import traceback
import urllib
from datetime import datetime
from optparse import OptionParser
from geni.util.rspec import Rspec

sfi_dir = os.path.expanduser("~/.sfi/")

def create_parser():
    command = sys.argv[0]
    argv = sys.argv[1:]
    usage = "%(command)s [options]" % locals()
    description = """getNodes will query comon and generate a list of nodes 
(plain or rspec) that meet the specified crieteria. If no criteria is 
specified, the default action is to return node comon considers 'alive' 
(resptime > 0)"""
    cmp_options = ['rwfs', 'uptime', 'loads', 'meminfo', 'kernver', 'cpuspeed', 'txrate', 'rxrate', 'numslices', 'liveslices']
    option = ['numslices', 'liveslices', 'gbfree'] 

    parser = OptionParser(usage=usage,description=description)
    for opt in options:
        parser.add_option("--%s" % opt, dest="%s" % opt, action="store_true", 
                          help = "available options [%s]" % ",".join(cmp_options))
   
    return parser    


def download_file(url, localFile):
    webFile = urllib.urlopen(url)
    localFile = open(localFile, 'w')
    localFile.write(webFile.read())
    localFile.close()    
    

def generate_comon_url(options):
    url = "select = 'resptime > 0"
    query_dict = {}
    query_dict['numslices'] = 'numslices %s= %s'
    query_dict['liveslices'] = 'liveslices %s= %s'
    query_dict['gbfree'] = 'gbfree %s= %s'
    
    if options.numslices:
        full_value = options.numslices
         
    url += "'"

def get_comon_data():
    date = datetime.now()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
     
    comon_data_filename = sfi_dir + os.sep + "comon_data.dat" 
    comon_url = "http://comon.cs.princeton.edu/status/dump_comon_%s%s%s" % (year, month, day)
    
    print "storing comon data from %s in %s" % (comon_url, comon_data_filename)     
    download_file(comon_url, comon_data_filename)

    return comon_data_filename
        
def main():
    parser = create_parser()
    (options, args) = parser.parse_args()
    comon_file = get_comon_data()
    

if __name__ == '__main__':
    main()
