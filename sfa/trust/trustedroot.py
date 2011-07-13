import os.path
import glob

from sfa.trust.gid import GID

class TrustedRootList:
    def __init__(self, dir):
        self.basedir = dir
        # create the directory to hold the files, if not existing
        if not os.path.isdir (self.basedir):
            os.makedirs(self.basedir)

    def add_gid(self, gid):
        fn = os.path.join(self.basedir, gid.get_hrn() + ".gid")
        gid.save_to_file(fn)

    def get_list(self):
        gid_list = []
        pattern=os.path.join(self.basedir,"*.gid")
        gid_files = glob.glob(pattern)
        for gid_file in gid_files:
            # ignore non-files
            if os.path.isfile(gid_file):
                gid = GID(filename = gid_file)
                gid_list.append(gid)
        return gid_list

    def get_file_list(self):
        gid_file_list = []
        pattern=os.path.join(self.basedir,"*.gid")
        gid_files = glob.glob(pattern)
        for gid_file in gid_files:
            # ignore non-files
            if os.path.isfile(gid_file):
                gid_file_list.append(gid_file)        
        return gid_file_list
