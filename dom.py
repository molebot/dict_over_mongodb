'''
need: pymongo  ( https://github.com/mongodb/mongo-python-driver )
author: molebot@outlook.com

examples:
>>> from dom import dictomongo as dm
>>> s=dm('test')
>>> s['123']=123
>>> s
{u'_id': ObjectId('50dad1e11ffd9e11c8fea454'), u'id': u'123', u'v': 123}
>>> len(s)
1
>>> s['234']=234
>>> s
{u'_id': ObjectId('50dad1e11ffd9e11c8fea454'), u'id': u'123', u'v': 123}
{u'_id': ObjectId('50dad2311ffd9e11c8fea455'), u'id': u'234', u'v': 234}
>>> s.filter(sort=[('v',s.desc)])
>>> s.get()
[{u'_id': ObjectId('50dad2311ffd9e11c8fea455'), u'id': u'234', u'v': 234}, {u'_i
d': ObjectId('50dad1e11ffd9e11c8fea454'), u'id': u'123', u'v': 123}]
>>> s.filter(sort=[('v',s.asc)])
>>> s.get()
[{u'_id': ObjectId('50dad1e11ffd9e11c8fea454'), u'id': u'123', u'v': 123}, {u'_i
d': ObjectId('50dad2311ffd9e11c8fea455'), u'id': u'234', u'v': 234}]
>>> s.filter(limit=1)
>>> s.get()
[{u'_id': ObjectId('50dad1e11ffd9e11c8fea454'), u'id': u'123', u'v': 123}]
>>> len(s)
2
>>> s.clear()
>>> len(s)
0
>>>
>>> s['1']=1
>>> s['2']=2
>>> s['3']=3
>>> s
{u'_id': ObjectId('50dad85e1ffd9e1adc57d469'), u'id': u'1', u'v': 1}
{u'_id': ObjectId('50dad8641ffd9e1adc57d46a'), u'id': u'2', u'v': 2}
{u'_id': ObjectId('50dad8681ffd9e1adc57d46b'), u'id': u'3', u'v': 3}
>>> s.clear_arg()
>>> s.arg
{}
>>> s.sort(v=s.asc).limit(2).get()
[{u'_id': ObjectId('50dad85e1ffd9e1adc57d469'), u'id': u'1', u'v': 1}, {u'_id':
ObjectId('50dad8641ffd9e1adc57d46a'), u'id': u'2', u'v': 2}]
>>> s.arg
{'sort': [('v', 1)], 'limit': 2}
>>> s.clear_arg()
>>> s.arg
{}
'''

from pymongo import MongoClient as _mc
from pymongo import ASCENDING as asc
from pymongo import DESCENDING as desc

class dictomongo( dict ):
    def filter( self, **args ):
        self.arg = args
    def sort( self, **args ):
        self.arg.update({'sort':args.items()})
        return self
    def limit( self, n ):
        self.arg.update({'limit':n})
        return self
    def skip( self, n ):
        self.arg.update({'skip':n})
        return self
    def clear_arg( self ):
        self.arg = {}
    def get( self ):
        if self.arg:
            out = self.collect.find(**self.arg )
        else:
            out = self.collect.find()
        if out:
            return list(out)
        else:
            return []
    def has_key( self, key ):
        if type(key)==type(()):
            spec = dict([key])
        else:
            spec = {self.id:key}
        return self.collect.find_one( spec ) != None
    def pop( self, key ):
        if type(key)==type(()):
            spec = dict([key])
        else:
            spec = {self.id:key}
        out = list(self.collect.find( spec ))
        self.__delitem__( spec )
        return out
    def keys( self ):
        out = self.get()
        if out:
            return map(lambda x:x[self.id],out)
        else:
            return []
    def values( self ):
        out = self.get()
        if out:
            return map(lambda x:x[self.value],out)
        else:
            return []
    def items( self ):
        out = self.get()
        if out:
            return map(lambda x:(x[self.id],x[self.value]),out)
        else:
            return []
    def __getitem__( self, key ):
        if type(key)==type(()):
            spec = dict([key])
        else:
            spec = {self.id:key}
        if self.arg:
            out = self.collect.find( spec, **self.arg )
        else:
            out = self.collect.find( spec )
        if out:
            return list(out)
        else:
            return []
    def __setitem__( self, key, value ):
        if type(key)==type(()):
            spec = dict([key])
        else:
            spec = {self.id:key}
        if self.arg:
            one = self.collect.find_one( spec, **self.arg )
        else:
            one = self.collect.find_one( spec )
        if one is None:
            one = {self.id:key}
        if type(value) == type({}):
            one.update( value )
        else:
            one[self.value] = value
        self.collect.save( one )
    def __repr__( self ):
        return '\n'.join(map(str,list(self.collect.find())))
    def __delitem__( self, key ):
        if type(key)==type(()):
            spec = dict([key])
        else:
            spec = {self.id:key}
        if self.capped is None:
            self.collect.remove( spec )
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
                    capped = None ):    #  example : {'capped':True,'size':10**10,'max':500}
        self.id = 'id'
        self.value = 'v'
        self.arg = {}
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
