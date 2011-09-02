import os

class VersionManager:
    
    def __init__(self):
        self.versions = []
        self.load_versions()

    def load_versions(self):
        path = os.path.dirname(os.path.abspath( __file__ ))
        versions_path = path + os.sep + 'versions'
        versions_module_path = 'sfa.rspecs.versions'
        valid_module = lambda x: os.path.isfile(os.sep.join([versions_path, x])) \
                        and not x.endswith('.pyc') and x not in ['__init__.py']
        files = [f for f in os.listdir(versions_path) if valid_module(f)]
        for filename in files:
            basename = filename.split('.')[0]
            module_path = versions_module_path +'.'+basename
            module = __import__(module_path, fromlist=module_path)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, 'version'):
                    self.versions.append(attr)

    def get_version(self, format, version_num=None, type=None):
        retval = None
        for version in self.versions:
            if format is None or format.lower() == version.format.lower():
                if version_num is None or version_num == version.version:
                    if type is None or type.lower() == version.type.lower():
                        retval = version
        if not retval:
            raise Exception, "No such version format: %s version: %s type:%s "% (format, version_num, type)
        return retval    
        

if __name__ == '__main__':
    v = VersionManager()
    print v.versions
    print v.get_version('sfa') 
    

