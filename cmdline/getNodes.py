#!/usr/bin/python
import sys
import os
import traceback
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
    options = ['alive']
    cmp_options = ['rwfs', 'uptime', 'loads', 'meminfo', 'kernver', 'cpuspeed', 'txrate', 'rxrate', 'numslices', 'liveslices']
     

    parser = OptionParser(usage=usage,description=description)
    for opt in options:
        parser.add_option("--%s" % opt, dest="%s" % opt, action="store_true", 
                          help = "available options [%s]" % ",".join(cmp_options))
   return parser    

def get_comon_data()
    date = datetime.now()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    for num in [year, month, day]:
        if len(num) == 1:
            num = "0" + num
     
    comon_data_file = sfi_dir + os.sep + "comon_data.dat" 
    comon_url = "http://comon.cs.princeton.edu/status/dump_comon_%s%s%s" % (year, month, day)
    
    # wget comon data and save it 
    # wget(comon_url)
    #  

def main():
    parser = create_parser()

    get_comon_data()
    

if __name__ == '__main__':
    main()
