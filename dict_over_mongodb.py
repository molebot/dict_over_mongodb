'''
need: pymongo  ( https://github.com/mongodb/mongo-python-driver )
author: molebot@outlook.com
'''

from pymongo import MongoClient as _mc
from pymongo import ASCENDING as asc
from pymongo import DESCENDING as desc

class dictomongo( dict ):
    def filter( self, **args ):
        self.arg = args
    def __getitem__( self, key ):
        if self.arg:
            return list(self.collect.find( {self.id:key}, **self.arg ))
        else:
            return list(self.collect.find( {self.id:key} ))
    def __setitem__( self, key, value ):
        if self.arg:
            one = self.collect.find_one( {self.id:key}, **self.arg )
        else:
            one = self.collect.find_one( {self.id:key} )
        if one is None:
            one = {self.id:key}
        if type(value) == type({}):
            one.update( value )
        else:
            one['v'] = value
        self.collect.save( one )
    def __delitem__( self, key ):
        if self.capped is None:
            if key:
                self.collect.remove( key )
            else:
                self.clear()
    def __len__( self ):
        return self.collect.count()
    def clear( self ):
        if self.capped is None:
            self.collect.drop()
    def __init__( self, collection, 
                    host = 'localhost', 
                    port = 27017,
                    user = None,
                    pswd = None,
                    database_name = 'dict_over_mongo', 
                    capped = None ):    #  example : {capped:True,size:10**10,max:500}
        self.id = '@_id_#'
        self.arg = None
        self.asc = asc
        self.desc = desc
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.capped = capped
        self.database_name = database_name
        self.collection = collection
        self.conn = _mc(host = self.host,port = self.port)
        self.db = self.conn[self.database_name]
        if self.user and self.pswd:
            self.auth = self.db.authenticate(self.user,self.pswd)
        if self.collection not in self.db.collection_names():
            if capped:
                self.db.create_collection(self.collection,**capped)
            else:
                self.db.create_collection(self.collection)
        self.collect = self.db[self.collection]
    def error(self):
        return self.collect.get_lasterror_options()

def do():
    import time
    print 'test'
    s = dictomongo('test')
    s['12']=123
    s['%.3f'%time.time()] = time.time()
    print s['12']
    print len(s)