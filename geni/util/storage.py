
class SimpleStorage(dict):

    db_filename = None
    types = ['dict', 'tabbed', 'text', 'shell']

    def __init__(self, db_filename, db = {}, type = 'dict'):

        if type not in self.types:
            raise Exception, "Invalid type %s, must be in %s" % (type, self.types)
        self.type = type
        dict.__init__(self, db)
        self.db_filename = db_filename
    
    def load(self):
        db_file = open(self.db_filename, 'r')
        dict.__init__(self, eval(db_file.read()))    
 
    def write(self):
        db_file = open(self.db_filename, 'w')  
        db_file.write(str(self))
        db_file.close()
    
    def sync(self):
        self.write()
