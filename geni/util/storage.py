import os

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
        if os.path.exists(self.db_filename) and os.path.isfile(self.db_filename):
            db_file = open(self.db_filename, 'r')
            dict.__init__(self, eval(db_file.read()))
        elif os.path.exists(self.db_filename) and not os.path.isfile(self.db_filename):
            raise IOError, '%s exists but is not a file. please remove it and try again' \
                           % self.db_filename
        else:
            db_file = open(self.db_filename, 'w')
            db_file.write('{}')
            db_file.close()
 
    def write(self):
        db_file = open(self.db_filename, 'w')  
        db_file.write(str(self))
        db_file.close()
    
    def sync(self):
        self.write()
