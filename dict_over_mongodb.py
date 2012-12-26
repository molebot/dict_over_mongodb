'''
need: pymongo  ( https://github.com/mongodb/mongo-python-driver )
author: molebot@outlook.com
'''

from pymongo import MongoClient as _mc
from pymongo import ASCENDING as asc
from pymongo import DESCENDING as desc

class dictomongo( dict ):
    id = '@_id_#'
    def filter( self, **args ):
        self.arg = args
    def __getitem__( self, key ):
        return list(self.collect.find( {self.id:key}, **self.arg ))
    def __setitem__( self, key, value ):
        one = self.collect.find_one( {self.id:key}, **self.arg ) 
        one.update( value )
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
            self.db.create_collection(self.collection,**capped)
        self.collect = self.db[self.collection]