import time,datetime
from hashlib import md5
from core import *
from svgcandle import *
from math import ceil
from urllib2 import urlopen
from qqmail import alertmail
import thread
import requests
import acc

vsn = '20150801.4'


def filelog(symbol,i,j,o):
    p = dict2str(o)
    file_log[i].error('#%s#%d#%d#%d#%s#'%(symbol,i,j,len(p),p))

def getprice(one):
    return (one['h']+one['l'])/2.0
cache['hh'] = {}
def get_skip():
    _day_ = datetime.datetime.now()
    _hour_ = _day_.strftime('%m%d%H')
    if cache.get('skip_cache','')==_hour_:
        return cache['cache_skip']
    else:
        _day_ = datetime.datetime.now()
        hour_str = _hour_
        if (_day_.isoweekday()==6):
            out=0
            if cache['skip'] != hour_str:
                cache['skip'] = hour_str
                logger.error('skip weekend end')
        elif (_day_.month==12 and _day_.day>=30) or (_day_.month==1 and _day_.day<=3):
            out=0.001
            if cache['skip'] != hour_str:
                cache['skip'] = hour_str
                logger.error('skip new year')
        elif _day_.isoweekday()==1 and _day_.hour<9:
            out=0.001
            if cache['skip'] != hour_str:
                cache['skip'] = hour_str
                logger.error('skip weekend begin')
        else:
            out=1
        cache['skip_cache'] = _hour_
        cache['cache_skip'] = out
        logger.error('cache_skip')
        return out
fill_state={}
all_state={}
cache['weeks'] = {}
class Iron:
    def get_result(self):
        out = {}
        c = self.cache
        saved = self.state

        if len(c[3])<2:
            self.result={'result':0}
            return self.all_result()

        fc = {}
        def fox(pos0,pos1):
            _store = fc
            if (pos0,pos1) not in _store:
                _store[(pos0,pos1)] = pmm(c[pos0][pos1])
            return _store[(pos0,pos1)]
        qc = {}
        def qq(pos0,pos1,level,k,q=-1):
            _store = qc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = zwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        rc = {}
        def rr(pos0,pos1,level,k,q=-1):
            _store = rc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = wb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        mc = {}
        def mm(pos0,pos1,level,k,q=-1):
            _store = mc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = pwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        zc = {}
        def zz(pos0,pos1,level,k,q=-1):
            _store = zc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = xwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        def mole(i):
            return fox(i,0)
        _sc = {}
        def signal(pos):
            _store = _sc
            if pos not in _store:
                _store[pos] = dmm(c[pos][0])
            return _store[pos]
        _bc = {}
        def signalb(pos):
            _store = _bc
            if pos not in _store:
                _store[pos] = bmm(c[pos][0])
            return _store[pos]
        def kw(pos,pp=-1):
            return zz(pos,0,7,1,q=pp)-zz(pos,0,7,-1,q=pp)
        def kwb(pos,pp=-1):
            return rr(pos,0,7,1,q=pp)-rr(pos,0,7,-1,q=pp)
        def kmm(pos):
            return zz(pos,0,7,0)+runout(pos)*(signal(pos)-zz(pos,0,7,0))
        def kmmb(pos):
            return rr(pos,0,7,0)+runoutb(pos)*(signalb(pos)-rr(pos,0,7,0))
        def runout(pos):
            uu = [zz(pos,0,ii, 1,q=-1) for ii in [3,4,5,6,7]]
            nn = [zz(pos,0,ii,-1,q=-1) for ii in [3,4,5,6,7]]
            uc = max(0,max(uu)-nn[0])
            nc = max(0,uu[0]-min(nn))
            cc = min(uc,nc)
            return max(0.001,uu[0]-nn[0])/max(0.001,cc)
        def runoutb(pos):
            uu = [rr(pos,0,ii, 1,q=-1) for ii in [3,4,5,6,7]]
            nn = [rr(pos,0,ii,-1,q=-1) for ii in [3,4,5,6,7]]
            uc = max(0,max(uu)-nn[0])
            nc = max(0,uu[0]-min(nn))
            cc = min(uc,nc)
            return max(0.001,uu[0]-nn[0])/max(0.001,cc)
        ppp = abs(kmm(1))
        pk = (ppp/(100*myth))**(1+myth)
        pss = pk*(kmm(1)-zz(1,0,7,0))+zz(1,0,7,0)
        _fox = zz(3,0,7,0)+pss*kw(3,pp=-2)/(myth*200)
        _just = zz(3,0,7,0)+kmm(1)*kw(3,pp=-2)/(myth*200)
#        _back = rr(3,0,7,0)+kmmb(1)*kwb(3,pp=-2)/(myth*200)

        _max = zz(3,0,7, 1,q=-2)
        _min = zz(3,0,7,-1,q=-2)

        uuu = -1*zz(3,0,7,-1,q=-1)
        nnn = -1*zz(3,0,7, 1,q=-1)

        uk = min(1.0,abs(max(0,uuu))/abs(nnn))
        nk = min(1.0,abs(min(0,nnn))/abs(uuu))

        uu = -1*uk*zz(1,0,7,-1,q=-2)
        nn = -1*nk*zz(1,0,7, 1,q=-2)
        uu2 = uu-myth*nn
        nn2 = nn-myth*uu
        pu = max(0,nnn)
        pn = min(0,uuu)
        uu,uuu = uuu,uu2
        nn,nnn = nnn,nn2
        uuu=min(uuu, 100*(1+myth))#*2.0
        nnn=max(nnn,-100*(1+myth))#*2.0
        uuu=max( 100*myth,uuu)
        nnn=min(-100*myth,nnn)
        _blue = (_fox+_just)/2.0
        _blue = max(-280,_blue)
        _blue = min( 280,_blue)
        _blue2 = max(pu-162,_blue)
        _blue2 = min(pn+162,_blue2)
        old = saved.get('old',[])
        if old and old[0][0]==c[1][0]['_id']:
            old = old[1:]
        old.insert(0,(c[1][0]['_id'],_blue2))
        saved['old'] = old[:5]
#        _just = 0#saved['old'][2][1]
        ks = max(abs(_max),abs(_min))/max(0.001,_max-_min)
        for i in self.todo:
            c[i][0]['vsn'] = vsn
            c[i][0]['point'] = saved.get('point',c[1][0]['c'])
            c[i][0]['mole'] = _blue
#            c[i][0]['blue'] = _back
            c[i][0]['just'] = _just# = saved['old'][2][1]
            c[i][0]['k1'] = kmm(1)
            c[i][0]['uuu'] = uuu
            c[i][0]['nnn'] = nnn
            c[i][0]['uu'] = uu#zz(1,0,7, 1,q=-2)
            c[i][0]['nn'] = nn#zz(1,0,7,-1,q=-2)
            c[i][0]['fox'] = _blue
            self.cache[i][0] = c[i][0]
            self.save(i,c[i][0])

        short = saved.get('short',0)
        llong = saved.get('long',1)
        dead = saved.get('dead',0)
        LS = saved.get('ls',1)
        Point = saved.get('point',0)
        real = saved.get('real',self.realprice)
        fill = saved.get('fill',0)
        daybase = saved.get('daybase',0.0)




        _pos_ = 1
        _pass = (_blue-(uuu+nnn)/2.0)
        blast = _blue
        _just = 0

        if short==0 and c[_pos_][0].get('doit',0)==0:
            if llong*_pass>0:# DON'T CHANGE HERE
                if (blast>uuu) and blast>_just and zz(1,0,3, 1,q=-1)>zz(1,1,3, 1,q=-1):
                    saved['short'] = short = 1
                if (blast<nnn) and blast<_just and zz(1,0,3,-1,q=-1)<zz(1,1,3,-1,q=-1):
                    saved['short'] = short = -1
            else:
                if _pass*llong<0:
                    if blast>uuu:
                        saved['short'] = short = 1
                    if blast<nnn:
                        saved['short'] = short = -1
        elif c[_pos_][0].get('doit',0)==0:
            if short>0 and (blast<=uuu or blast<_just) and zz(1,0,3,-1,q=-1)<zz(1,1,3,-1,q=-1):
                saved['short'] = short = 0
            if short<0 and (blast>=nnn or blast>_just) and zz(1,0,3, 1,q=-1)>zz(1,1,3, 1,q=-1):
                saved['short'] = short = 0

        if short!=0 and short!=llong:
            saved['long'] = llong = short
        if short==0:
            LS2 = -1*llong
        else:
            LS2 = short

        changed = False

        _day_ = datetime.datetime.now()
        if LS2!=LS:
            saved['ls'] = LS2
            _profit = LS*(self.realprice-real)
            saved['real'] = self.realprice
            saved['point'] = Point = c[1][0]['c']
            c[i][0]['point'] = c[1][0]['c']
            
            c[_pos_][0]['doit']=1
            self.cache[_pos_][0] = c[_pos_][0]
            self.save(_pos_,c[_pos_][0])

            LS = LS2
            saved['base_p']=saved.get('base_p',0)+_profit
            saved['fill'] = fill = 0
            if _day_.hour==9 and _day_.minute<30:
                saved['dead'] = dead = 0
                saved.get('daybaseday',0)==0
            elif _day_.hour==15:
                saved['dead'] = dead = 0
                saved.get('daybaseday',0)==0
            elif zz(3,0,7,1,q=-1)*zz(3,0,7,-1,q=-1)>0 and LS2*zz(3,0,7,0)<0:
                saved['dead'] = dead = 0
            else:
                saved['dead'] = dead = 1

            if dead>0 and saved.get('daybaseday',0)==0:
                saved['daybase'] = saved.get('base_p',0.0)
                saved['daybaseday'] = 1

        if fill<1:
            if LS2*(c[1][0]['c']-Point)>=10:
                saved['fill'] = fill = 1
        #=======================================
        if _day_.hour==15 and _day_.minute>10:
            saved['dead'] = dead = 0
            saved.get('daybaseday',0)==0
            closeit = 0
        else:
            closeit = 1
        out['result'] = LS2*dead*closeit
        out['long'] = llong
        out['short'] = short
        out['fill'] = fill
        out['uuu'] = uuu
        out['nnn'] = nnn
        out['just'] = _blue
        out['point'] = Point
        out['profit'] = saved.get('base_p',0)
        #self.state['his']
        if self.state.get('ss',0)!=LS2:
            time_str = _day_.strftime('%m%d%H%M%S')
            self.state['ss']=LS2
            _his = self.state.get('his',['none'])
            _his.append('%s#%.1f=%d@%.1f'%(time_str,self.realprice,LS2,saved.get('base_p',0)-saved.get('daybase',0)))
            self.state['his'] = _his[-21:]
        self.result = out
        self.all_result()
    def day_level(self):
        saved = self.state
        _p = saved.get('base_p',0)-saved.get('daybase',0)
        if _p<-20:
            return 1
        elif _p<-10:
            return 2
        else:
            return -1
    def thisweek(self,_base,_aceq):
        self.thisweek = _base
        self.thisaceq = _aceq
        self.thisbase = _base
#=====================================================================
#=====================================================================
#=====================================================================
#=====================================================================
#=====================================================================
    def __init__(self,symbol,plus="20150723"):
        self.db = {}
        self.data={}
        self.symbol = symbol#+plus
        self.todo = [1,3]
        for i in self.todo:self.db[i] = conn[symbol][str(i)]
        self.out = {}
        _a = allstate[self.symbol]
        if _a:
            self.state = _a[0]
        else:
            self.state = {}
        self.cache = {}
        self.offset = 1
        self.hour = datetime.datetime.now().hour
    def all_result(self):
        allstate[self.symbol] = self.state
        return {'state':self.state,'result':self.result}
    def price(self,price):
        for i in self.todo:
            self.new_price(price,i)
    def new_price(self,price,pos):
        _result = list(self.db[pos].find({'do':1},sort=[('_id',desc)],limit=2))
        length = fibo[pos+self.offset]
        if len(_result)>0:
            now = _result[0]
            if len(_result)>1:
                last = _result[1]
            else:
                last = None
            now['c'] = price
            now['h'] = max(now['c'],now['h'])
            now['l'] = min(now['c'],now['l'])
            now['time'] = time.time()
            now['do'] = 0
            now,last = self.check_k_len(now,length,last,pos)
            now,last = self.check_k_hour(now,last,pos)
            now = self.check_base(pos,now,last)
        else:
            last = None
            now = {'_id':0,'do':0,'o':price,'h':price,'l':price,'c':price,'hour':self.hour}
            now = self.check_base(pos,now,last)
    def real(self,p):self.realprice = p
    def money(self,p):self.money = p
    def check_k_len(self,now,length,last,pos):
        if now['h']-now['o']>length:
            high = now['h']
            now['h'] = now['o']+length
            now['c'] = now['o']+length
            new = {'o':now['c'],'h':high,'l':now['c'],'c':now['c'],'do':0,'hour':self.hour}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            now = self.check_base(pos,now,last)
            return self.check_k_len(new,length,now,pos)
        elif now['o']-now['l']>length:
            low = now['l']
            now['l'] = now['o']-length
            now['c'] = now['o']-length
            new = {'o':now['c'],'h':now['c'],'l':low,'c':now['c'],'do':0,'hour':self.hour}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            now = self.check_base(pos,now,last)
            return self.check_k_len(new,length,now,pos)
        else:
            return (now,last)
    def check_k_hour(self,now,last,pos):
        if now.get('hour',-1)!=self.hour:
            p = now['c']
            new = {'o':p,'h':p,'l':p,'c':p,'do':0,'hour':self.hour}
            new['_id'] = int(time.time()/3600)*1000000
            new['cnt'] = 0
            self.check_len(pos)
            now = self.check_base(pos,now,last)
            saved = self.state
            _p = saved.get('base_p',0)-saved.get('daybase',0)
            thread.start_new_thread(alertmail,('%s_%.1f_%.1f'%(acc.account,self.money,_p),))
            return (new,now)
        return (now,last)

    def check_base(self,pos,_todo,_last):
        if _last and 'old' not in _todo:
            if 'old' in _last:_last.pop('old')
            _todo['old'] = _last
#=====================================================================  raw
        if 'hr' not in _todo:
            if _last:
                _todo['hr'] = [getprice(_last)]+_last['hr'][:fibo[-1]]
            else:
                _todo['hr'] = []
        _prcs = getprice(_todo)
        _list = [_prcs] + _todo['hr']
        _todo['m']={}
        _todo['s']={}
        for i in fibo:
            _str_ = str(i)
            if _last:
                vle = ma(_prcs,_last['m'][_str_],i)
                _todo['s'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = _prcs
                _todo['s'][_str_] = 0.0
            _todo['m'][_str_] = vle
#=====================================================================  k
        #=====clear====
        if 'hz' not in _todo:
            if _last:
                _todo['hz'] = [zmm(_last)]+_last['hz'][:fibo[-1]]
            else:
                _todo['hz'] = []
        _prcs = zmm(_todo)
        _list = [_prcs] + _todo['hz']
        _todo['zm']={}
        _todo['zs']={}
        for i in fibo:
            _str_ = str(i)
            if _last and len(_last.get('zm',{}))==len(fibo):
                vle = ma(_prcs,_last['zm'][_str_],i)
                _todo['zs'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = _prcs
                _todo['zs'][_str_] = 0.0#
            _todo['zm'][_str_] = vle
#=====================================================================  k
        #=====clear====
        if 'hx' not in _todo:
            if _last:
                _todo['hx'] = [dmm(_last)]+_last.get('hx',[])[:fibo[-1]]
            else:
                _todo['hx'] = []
        _prcs = dmm(_todo)
        _list = [_prcs] + _todo['hx']
        _todo['xm']={}
        _todo['xs']={}
        for i in fibo:
            _str_ = str(i)
            if _last and len(_last.get('xm',{}))==len(fibo):
                vle = ma(_prcs,_last['xm'][_str_],i)
                _todo['xs'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = _prcs
                _todo['xs'][_str_] = 0.0#
            _todo['xm'][_str_] = vle
#=====================================================================
        _todo['do']=1
        _todo['time'] = time.time()
        if _last:
            self.cache[pos] = [_todo,_last]
            self.save(pos,_last)
        else:
            self.cache[pos] = [_todo]
        self.save(pos,_todo)
        return _todo
    def data_out(self,pos):
        _result = self.db[pos].find({'do':1},sort=[('_id',desc)],limit=2)
        return jsondump(list(_result))
    def data_in(self):
        for ii in self.todo:
            f = open('/root/local/%d.txt'%ii)
            c = f.readlines()[0]
            _list = jsonload(c)
            f.close()
            for one in _list:# int(time.time()/3600)*1000000
                _mod = one['_id']%1000000
                one['_id'] += 100 #int(time.time()/3600)*1000000+_mod
                self.save(ii,one)
                print "save ok",ii
        return 'ok'
#=====================================================================
    def save(self,Pos,Dict):
        self.db[Pos].save(Dict)
    def check_len(self,pos):
        _time = time.time()-pos*2*24*3600
        self.db[pos].remove({'time':{'$lt':_time}})
#=====================================================================
    def get_image(self,pos,lens,group,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(lens),skip=int(offset)*int(lens)))
        _l = self.state.get('his',['none'])[::-1]
        out = SVG(group,result[::-1],_l,data).to_html()
        return out
    def only_image(self,pos,lens,group,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(lens),skip=int(offset)*int(lens)))
        out = SVG(group,result[::-1],[self.symbol+" "+str(datetime.datetime.now())[:19]],data).to_html()
        return out
############################################################################################################
'''
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
#        mid
'''
############################################################################################################
class Base:
    period = [(12,12,3600,0),(2,3,3600,1),(3,4,3600,2),(4,5,3600,3)]
    save = { }
    kk = 34
    def cname(self,ss):return '%s_%s'%(self.symbol,ss)
    def get_money(self,get_string):
        return self.get_result(get_string)
    def get_result(self,get_string):
        out = []
        c = self.cache
        d = self.db
        if not cache['symbol'].get(self.symbol,None):
            cache['symbol'][self.symbol] = 'init'
        def cname(ss):return '%s_%s'%(self.symbol,ss)

        fc = {}
        def fox(pos0,pos1):
            _store = fc
            if (pos0,pos1) not in _store:
                _store[(pos0,pos1)] = pmm(c[pos0][pos1])
            return _store[(pos0,pos1)]
        qc = {}
        def qq(pos0,pos1,level,k,q=-1):
            _store = qc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = zwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        mc = {}
        def mm(pos0,pos1,level,k,q=-1):
            _store = mc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = pwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        zc = {}
        def zz(pos0,pos1,level,k,q=-1):
            _store = zc
            if (level,pos0,pos1,k,q) not in _store:
                _store[(level,pos0,pos1,k,q)] = xwb(level,c[pos0][pos1],k,3,q)
            return _store[(level,pos0,pos1,k,q)]
        def mole(i):
            return fox(i,0)
        _sc = {}
        def signal(pos):
            _store = _sc
            if pos not in _store:
                _store[pos] = dmm(c[pos][0])
            return _store[pos]

        def just(i,ss=-1):
            s = sum(map(lambda x:fibo[13-x],[3,4,5,6]))*1.0
            u = sum(map(lambda x:fibo[13-x],filter(lambda y:zz(i,0,y, 1,q=ss)>zz(i,0,y+1, 1,q=ss),[3,4,5,6])))
            n = sum(map(lambda x:fibo[13-x],filter(lambda y:zz(i,0,y,-1,q=ss)<zz(i,0,y+1,-1,q=ss),[3,4,5,6])))
            return 1.0+((u+n)/s)*(myth**i)
        def blue(i):
            return fox(i,0)
        def cell(ps=-1):
            a1 = (1.0+just(1,ss=ps))*blue(1)
            a2 = (1.0+just(2,ss=ps))*blue(2)
            a3 = (1.0+just(3,ss=ps))*blue(3)
            return a1+a2+a3
        def runout(pos):
            uu = [zz(pos,0,ii, 1,q=-1) for ii in [3,4,5,6,7]]
            nn = [zz(pos,0,ii,-1,q=-1) for ii in [3,4,5,6,7]]
            uc = max(0,max(uu)-nn[0])
            nc = max(0,uu[0]-min(nn))
            cc = min(uc,nc)
            return max(0.001,uu[0]-nn[0])/max(0.001,cc)
        def kw(pos,pp=-1):
            return zz(pos,0,7,1,q=pp)-zz(pos,0,7,-1,q=pp)
        def jk(pos):
            return just(pos)
        def wk(pos):
            kk = 1.0
            for one in range(pos,4):
                kk*=runout(one)
            return kk
        def au(pos):
            xx = pos
            yy = 3
            return qq(xx,0,yy,1-1,q=1)+(qq(xx,0,yy,1,q=1)-qq(xx,0,7, 0,q=1))*runout(xx)            #return zz(pos,0,7,0)+runout(pos)*(zz(pos,0,7,1,q=-1)-zz(pos,0,7,0))
        def an(pos):
            xx = pos
            yy = 3
            return qq(xx,0,yy,1-1,q=1)-(qq(xx,0,yy,1,q=1)-qq(xx,0,7, 0,q=1))*runout(xx)            #return zz(pos,0,7,0)+runout(pos)*(zz(pos,0,7,1,q=-1)-zz(pos,0,7,0))
        def rmm(pos):
            return (zz(pos,0,7,0)+runout(pos)*(signal(pos)-zz(pos,0,7,0)))*jk(pos)
            return zz(pos,0,7,0)+wk(pos)*(signal(pos)-zz(pos,0,7,0))
        def kmm(pos):
            return zz(pos,0,7,0)+runout(pos)*(signal(pos)-zz(pos,0,7,0))
            return wk(pos)*signal(pos)
        def get_mrm():
            ww = [rmm(ii)*kw(ii)*ii for ii in [1,2,3]]
            wk = [kw(ii)*ii for ii in [1,2,3]]
            return sum(ww)/sum(wk)
        def get_mrw():
            ww = [zz(ii,0,7,0)*kw(ii) for ii in [1,2,3]]
            wk = [kw(ii) for ii in [1,2,3]]
            return sum(ww)/sum(wk)
        def get_mwm(pos,shift,k):
            if k>0:
                return qq(pos,0,7,shift,q=-1)+shift*kmm(pos)
            else:
                return qq(pos,0,7,-1*shift,q=-1)+shift*kmm(pos)
        def get_mwma(pos,shift,k):
            if k>0:
                return zz(pos,0,7,shift,q=-1)+shift*kmm(pos)
            else:
                return zz(pos,0,7,-1*shift,q=-1)+shift*kmm(pos)
        def get_mwmb(pos,shift,k):
            _fox1 = kmm(pos)#fox(1,0)*just(1)+fox(2,0)*just(2)+fox(3,0)*just(3)
            if k>0:
                return sum([mm(ii,0,7,shift,q=-1) for ii in [1]])+shift*_fox1
            else:
                return sum([mm(ii,0,7,-1*shift,q=-1) for ii in [1]])+shift*_fox1
        def get_mru():
            big = get_mwm(3,1,kmm(3))
            sml = get_mwm(1,-1,kmm(3))
            return (big+sml)/2.0
        def get_mrn():
            big = get_mwm(3,-1,kmm(3))
            sml = get_mwm(1,1,kmm(3))
            return (big+sml)/2.0
        def get_single(pos):
            if zz(pos,0,3, 1,q=0)>zz(pos,0,7, 1,q=0):# for ii in [3,4,5,6]]==[ii>0 for ii in [3,4,5,6]]:
                return 1
            if zz(pos,0,3,-1,q=0)<zz(pos,0,7,-1,q=0):#[zz(pos,0,ii,-1,q=1)<zz(pos,0,ii+1,-1,q=1) for ii in [3,4,5,6]]==[ii>0 for ii in [3,4,5,6]]:
                return -1
            return 0
            if [zz(pos,0,ii,1,q=1)>zz(pos,0,ii+1,1,q=1) for ii in [3,4,5,6]]==[ii>0 for ii in [3,4,5,6]]:
                return 1
            if [zz(pos,0,ii,-1,q=1)<zz(pos,0,ii+1,-1,q=1) for ii in [3,4,5,6]]==[ii>0 for ii in [3,4,5,6]]:
                return -1
            return 0

        ppp = abs(kmm(1))
        pk = (ppp/(100*myth))**(1+myth)
        pss = pk*(kmm(1)-zz(1,0,7,0))+zz(1,0,7,0)
        _fox = zz(3,0,7,0)+pss*kw(3,pp=-2)/(myth*200)
        _just = zz(3,0,7,0)+kmm(1)*kw(3,pp=-2)/(myth*200)

        uu1 = zz(3,0,7,0)+zz(1,0,7, 1,q=-2)*kw(3)/(myth*200)
        nn1 = zz(3,0,7,0)+zz(1,0,7,-1,q=-2)*kw(3)/(myth*200)
        _max = min([zz(ii,0,7, 1,q=-2) for ii in [1,2,3]])
        _min = max([zz(ii,0,7,-1,q=-2) for ii in [1,2,3]])
        kk = 0.5#min(1.0,kk-myth+0.5)
        uuu = -1*zz(3,0,7,-1,q=-1)
        nnn = -1*zz(3,0,7, 1,q=-1)
        uu = -1*(zz(3,0,7,-1,q=-1)+zz(1,0,7,-1,q=-1))/2.0
        nn = -1*(zz(3,0,7, 1,q=-1)+zz(1,0,7, 1,q=-1))/2.0
        _plus = _fox-zz(1,0,7,0)
        _blue = (_fox+_just)/2.0
        _blue = max(-280,_blue)
        _blue = min( 280,_blue)
        ks = max(abs(_max),abs(_min))/max(0.001,_max-_min)
        for i in [1,2,3]:
            for xx in [1,2,3]:
                for yy in [3,4,5,6,7]:
                    c[i][0]['zu%d%d'%(xx,yy)] = zz(xx,0,yy, 1,q=-2)
                    c[i][0]['zn%d%d'%(xx,yy)] = zz(xx,0,yy,-1,q=-2)
                    c[i][0]['mu%d%d'%(xx,yy)] = zz(xx,0,yy, 1,q=-1)
                    c[i][0]['mn%d%d'%(xx,yy)] = zz(xx,0,yy,-1,q=-1)
            c[i][0]['km%d'%1] = kmm(1)
            c[i][0]['km%d'%2] = kmm(2)
            c[i][0]['km%d'%3] = kmm(3)
            c[i][0]['uu'] = uu
            c[i][0]['nn'] = nn
            c[i][0]['vsn'] = vsn
            c[i][0]['point'] = saved[cname('point')]
            c[i][0]['mole'] = _fox
            c[i][0]['show'] = _just
            c[i][0]['uuu'] = uuu
            c[i][0]['nnn'] = nnn
            c[i][0]['max'] = _max
            c[i][0]['min'] = _min
            c[i][0]['fox'] = _blue
            self.cache[i][0] = c[i][0]
            d[i].save(c[i][0])
            if self.save and 1<0:
                for j in [0,1]:
                    o = c[i][j]
                    thread.start_new_thread(filelog,(self.symbol,i,j,o))
        if not get_string:
            return c[1][0]

        short = saved[cname('short')]
        long = saved[cname('long')]
        LS = saved[cname('ls')]
        Point = saved[cname('point')]
        fill = saved[cname('fill')]
        Pos = saved[cname('pos')]
        blast = saved[cname('blast')]

        if Point<1:
            saved[cname('point')] = Point = c[1][0]['c']
        if long==0:
            saved[cname('long')] = long = 1


        _pos_ = 1
        bigger = 0
        _pass = (_blue-(uuu+nnn)/2.0)
        blast = _blue

        if short==0 and c[_pos_][0].get('doit',0)==0:
            if long*_pass>0:# DON'T CHANGE HERE
                if ks<0:
                    if (blast>uuu) and c[1][0]['fox']>c[1][1]['fox']:
                        oldstate[cname('short')] = short = 1
                    if (blast<nnn) and c[1][0]['fox']<c[1][1]['fox']:
                        oldstate[cname('short')] = short = -1
                else:
                    if (blast>uuu) and zz(1,0,3, 1,q=-1)>zz(1,1,3, 1,q=-1):# and zz(1,0,7, 1,q=-1)>zz(1,1,7, 1,q=-1):
                        oldstate[cname('short')] = short = 1
                    if (blast<nnn) and zz(1,0,3,-1,q=-1)<zz(1,1,3,-1,q=-1):# and zz(1,0,7,-1,q=-1)<zz(1,1,7,-1,q=-1):
                        oldstate[cname('short')] = short = -1
            else:
                if _pass*long<0:
                    if blast>uuu:
                        oldstate[cname('short')] = short = 1
                    if blast<nnn:
                        oldstate[cname('short')] = short = -1
        elif c[_pos_][0].get('doit',0)==0:
            if ks>0:
                if short>0 and (blast<=uuu) and zz(1,0,3,-1,q=-1)<zz(1,1,3,-1,q=-1):
                    oldstate[cname('short')] = short = 0
                if short<0 and (blast>=nnn) and zz(1,0,3, 1,q=-1)>zz(1,1,3, 1,q=-1):
                    oldstate[cname('short')] = short = 0
            else:
                if short>0 and blast<=uuu and c[1][0]['fox']<c[1][1]['fox']:
                    oldstate[cname('short')] = short = 0
                if short<0 and blast>=nnn and c[1][0]['fox']>c[1][1]['fox']:
                    oldstate[cname('short')] = short = 0
        if short!=0 and short!=long:
            oldstate[cname('long')] = long = short
        if short==0:
            LS2 = -1*long
        else:
            LS2 = short
        changed = False
        Dead = oldstate[cname('dead')]
        _day_ = datetime.datetime.now()
        if LS2!=LS:
            oldstate[cname('ls')] = LS2
            _profit = LS*(c[1][0]['c']-Point)
            oldstate[cname('point')] = Point = c[1][0]['c']
            c[i][0]['point'] = c[1][0]['c']
            
            c[_pos_][0]['doit']=1
            self.cache[_pos_][0] = c[_pos_][0]
            d[_pos_].save(c[_pos_][0])

            LS = LS2
            changed = True
            timenum = str(int(time.time()))
            mavar = 5
            oldstate[cname('base_p')]=oldstate[cname('base_p')]+_profit
            target = 0
            if len(self.his)>1:
                last = self.his[-2]
                target = ma(oldstate[cname('base_p')],last[1],mavar)
                if timenum == self.his[-1][0]:
                    self.his = self.his[:-1]
            self.his.append((timenum,max(target,oldstate[cname('base_p')]-50),oldstate[cname('base_p')]))
            history[self.symbol] = self.his[-2:]
#            if self.his[-1][-1]>self.his[-1][-2] and oldstate['skip_%s'%self.symbol]==0 and time.time()>saved[cname('skip')]:
            if oldstate['skip_%s'%self.symbol]==0 and time.time()>saved[cname('skip')]:
                oldstate[cname('dead')] = Dead = 1
            else:
                oldstate[cname('dead')] = Dead = 0
            oldstate[cname('fill')] = fill = 0
        cache['weeks'].update({self.account:'%16s # %10.5f = %10.5f'%(self.account,self.thisweek,self.thisaceq)})
        if fill<1:
            if short!=10 and LS2*(c[1][0]['c']-Point)>=10:
                oldstate[cname('fill')] = fill = 1
            if short==10 and abs(kmm(1))<62 and LS2*(c[1][0]['c']-Point)>10:
                oldstate[cname('fill')] = fill = 1
        #=======================================
        hour_str = _day_.strftime('%d%H')
        out.append(str(int(float(c[1][0]['from'])))[-4:])            #       0
        _t = c[1][0]['c']-c[1][0]['o']#
        out.append('%.1f'%_t)   #       1
        out.append(long)   #       2
        out.append(short)  #       3
        if len(state)>0:
            state.clear_arg()
            c_l = [one['time'] for one in state.get()]
            if c_l:
                _q_ = int(max(c_l)-min(c_l))
                if _q_>300:
                    thread.start_new_thread(alertmail,('time out',str(state.get())))
                    state.clear()
                out.append('%d.%d'%(_q_,len(state)))
            else:
                out.append(0)
        else:
            out.append(0)
        out.append(hour_str)    #       5
        if (_day_.hour>=19 and _day_.day == oldstate['feinong']):
            out.append(0)
        elif oldstate['skip_%s'%self.symbol]==1:
            out.append(0)
        elif Dead==0 or 'demo' not in self.account:  #   account
            out.append('000')
        else:
            out.append('%.3f'%min(get_skip(),1.0))
        out.append(5)
        out.append(fill)         #      08
        out.append(oldstate['feinong'])# 11
        out.append('%.2f'%uuu)
        out.append('%.2f'%_blue)         #      08
        out.append('%.2f'%nnn)
        out.append(Dead)
        out.append(0)
        if self.his:
            out.append('%.2f'%self.his[-1][-1])
        out.append('%.1f'%Point)   #      mm(1,0,7, 1,q=-1)-mm(1,0,7,-1,q=-1)
        out.append(oldstate['skip_%s'%self.symbol])
        out.append('%.2f'%ks)         #      08
        time_str = _day_.strftime('%m%d%H%M%S')
        if cache.get('ss%s'%self.symbol,0)!=LS2:
            cache['ss%s'%self.symbol]=LS2
            _his = cache.get('his_%s'%self.symbol,['none'])
            _his.append('%s#%.1f=%d@%.1f'%(time_str,Point,LS2,self.his[-1][-1]))
            cache['his_%s'%self.symbol] = _his[-21:]
        _str = '%s%s%.0f|@xyz110'%(time_str,self.account,time.time())
        out.append('%s_%s'%(time_str,'1'))#md5(_str).hexdigest()))
        _all_ = '|'.join([str(i) for i in out])
        cache['symbol'][self.symbol] = _all_
        if cache.get('short%s'%self.symbol,0)!=short:
            changed = False
            cache['short%s'%self.symbol] = short
        else:
            changed = True
        self.check_len()
#        logger.error(_all_)
        return (_all_,changed)
    def real(self,p):self.realprice = p
    def load_data(self,data,pos):
        d = str2dict(data)
        print(d)
        self.db[pos].save(d)
        return 'ok'
    def thisweek(self,_base,_aceq):
        _day_ = datetime.datetime.now()
        _wd_ = _day_.isoweekday()
        _sec_ = 24*3600.0
        if 'btc' in self.account:
            self.thisweek = _base
        else:
            self.thisweek = (100+((_wd_-1)*_sec_+int(time.time()+3600*8)%_sec_)/_sec_)*_base/100.0
        self.thisaceq = _aceq
        self.thisbase = _base
    def data_out(self,pos):
        out = []
        _result = self.db[pos].find({'do':1},sort=[('_id',desc)],limit=2)
        for i in list(_result):
            i.pop('1')
            i.pop('2')
            i.pop('3')
            out.append(i)
        return jsondump(out)
    def data_in(self):
        for ii in [1,2,3]:
            f = open('%d.txt'%ii)
            c = f.readlines()[0]
            _list = jsonload(c)
            f.close()
            for one in _list:
                one['_id'] += 100
                self.db[ii].save(one)
                print "save ok",ii
        return 'ok'
    def __init__(self,symbol,account,db='molebot201411'):
        self.symbol = symbol
        self.account = account
        self.save=False
        self.datalimit=5
        self.balance = 0.0
        self.data = conn[db]
        self.hour = datetime.datetime.now().hour
        if self.symbol not in fill_state.keys():
            fill_state[self.symbol] = {}
        his = history[self.symbol]
        if his:
            self.his = his
        else:
            self.his = []
        _aceq = aceqhis[self.account]
        if _aceq:
            self.aceq = _aceq
        else:
            self.aceq = []
        self.db = {}
        self.cache = {}
        for x,y,z,k in self.period:
            self.db[k] = self.data['%s%d'%(self.symbol,k)]
            self.db[k].ensure_index('from',cache_for=3600*24*6)
        if self.symbol not in all_state.keys():
            all_state[self.symbol] = {}
    def check_len(self):
        for i in range(len(self.period)):
            _time = time.time()-i*2*24*3600
            self.db[i].remove({'time':{'$lt':_time}})
    def price(self,price,clock):
        self.new_price(price,clock,1)
    def check_k_len(self,now,length,last,pos,oldt):
        t = '%.3f'%time.time()
        if now['h']-now['o']>length:
            high = now['h']
            now['h'] = now['o']+length
            now['c'] = now['o']+length
            new = {'from':t,'to':t,'o':now['c'],'h':high,'l':now['c'],'c':now['c'],'do':0,'hour':self.hour}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            if pos == 1:
                self.new_price(now['c'],time.time(),2)
                self.new_price(now['c'],time.time(),3)
            now = self.check_base(pos,now,last)
            self.save = True
            return self.check_k_len(new,length,now,pos,oldt)
        elif now['o']-now['l']>length:
            low = now['l']
            now['l'] = now['o']-length
            now['c'] = now['o']-length
            new = {'from':t,'to':t,'o':now['c'],'h':now['c'],'l':low,'c':now['c'],'do':0,'hour':self.hour}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            if pos == 1:
                self.new_price(now['c'],time.time(),2)
                self.new_price(now['c'],time.time(),3)
            now = self.check_base(pos,now,last)
            self.save = True
            return self.check_k_len(new,length,now,pos,oldt)
        else:
            return (now,last)
    def check_k_hour(self,now,t,last,pos):
        if now.get('hour',-1)!=self.hour:
            p = now['c']
            self.save = True
            new = {'from':t,'to':t,'o':p,'h':p,'l':p,'c':p,'do':0,'hour':self.hour}
            new['_id'] = int(time.time()/3600)*1000000
            new['cnt'] = 0

            if pos == 1:
#                thread.start_new_thread(alertmail,('hour',str(state.get())))
                self.new_price(now['c'],time.time(),2)
                self.new_price(now['c'],time.time(),3)
            now = self.check_base(pos,now,last)
            return (new,now)
        return (now,last)
    def new_price(self,price,clock,pos):
        t = '%.3f'%clock
        data = self.db[pos]
        x,y,z,_s = self.period[pos]
        _result = data.find({'do':1},sort=[('_id',desc)],limit=2)
        if _result.count()>0:
            now = _result[0]
            if _result.count()>1:
                last = _result[1]
            else:
                last = None
            now['to'] = t
            now['c'] = price
            now['h'] = max(now['c'],now['h'])
            now['l'] = min(now['c'],now['l'])
            now['time'] = time.time()
            now['do'] = 0
            length = fibo[x]
            now,last = self.check_k_len(now,length,last,pos,now['from'])
            now,last = self.check_k_hour(now,t,last,pos)
            if pos == 1:
                self.new_price(price,time.time(),2)
                self.new_price(price,time.time(),3)
            now = self.check_base(pos,now,last)
        else:
            last = None
            now = {'_id':0,'do':0,'from':t,'to':t,'o':price,'h':price,'l':price,'c':price,'hour':self.hour}
            if pos == 1:
                self.new_price(price,time.time(),2)
                self.new_price(price,time.time(),3)
            now = self.check_base(pos,now,last)
    def check_base(self,pos,_todo,_last):
        if _last and 'old' not in _todo:
            if 'old' in _last:_last.pop('old')
            _todo['old'] = _last
#=====================================================================  raw
        if 'hr' not in _todo:
            if _last:
                _todo['hr'] = [getprice(_last)]+_last['hr'][:fibo[-1]]
            else:
                _todo['hr'] = []
        _prcs = getprice(_todo)
        _list = [_prcs] + _todo['hr']
        _todo['m']={}
        _todo['s']={}
        for i in fibo:
            _str_ = str(i)
            if _last:
                vle = ma(_prcs,_last['m'][_str_],i)
                _todo['s'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = _prcs
                _todo['s'][_str_] = 0.0
            _todo['m'][_str_] = vle
#=====================================================================  k
        '''
        if 'hp' not in _todo:
            if _last:
                _todo['hp'] = [pmm(_last)]+_last['hp'][:fibo[-1]]
            else:
                _todo['hp'] = []
        _prcs = pmm(_todo)
        _list = [_prcs] + _todo['hp']
        _todo['pm']={}
        _todo['ps']={}
        for i in fibo:
            _str_ = str(i)
            if _last and len(_last.get('pm',{}))==len(fibo):
                vle = ma(_prcs,_last['pm'][_str_],i)
                _todo['ps'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = 0.0
                _todo['ps'][_str_] = 0.0
            _todo['pm'][_str_] = vle
        '''
#=====================================================================  k
        #=====clear====
        if 'hz' not in _todo:
            if _last:
                _todo['hz'] = [zmm(_last)]+_last['hz'][:fibo[-1]]
            else:
                _todo['hz'] = []
        _prcs = zmm(_todo)
        _list = [_prcs] + _todo['hz']
        _todo['zm']={}
        _todo['zs']={}
        for i in fibo:
            _str_ = str(i)
            if _last and len(_last.get('zm',{}))==len(fibo):
                vle = ma(_prcs,_last['zm'][_str_],i)
                _todo['zs'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
                vle = _prcs
                _todo['zs'][_str_] = 0.0#
            _todo['zm'][_str_] = vle
#=====================================================================  k
        #=====clear====
        if 'hx' not in _todo:
            if _last:
                _todo['hx'] = [dmm(_last)]+_last.get('hx',[])[:fibo[-1]]
            else:
                _todo['hx'] = []
        _prcs = dmm(_todo)
        _list = [_prcs] + _todo['hx']
        _todo['xm']={}
        _todo['xs']={}
        for i in fibo:
            _str_ = str(i)
            if _last and len(_last.get('xm',{}))==len(fibo):
#                logger.error('in %s %d'%(self.symbol,i))
                vle = ma(_prcs,_last['xm'][_str_],i)
                _todo['xs'][_str_] = st(vle,[one for one in _list[:i]],i)
            else:
#                logger.error('out %s %d'%(self.symbol,i))
                vle = _prcs
                _todo['xs'][_str_] = 0.0#
            _todo['xm'][_str_] = vle
#=====================================================================
        _todo['do']=1
        _todo['time'] = time.time()
        if _last:
            self.cache[pos] = [_todo,_last]
        else:
            self.cache[pos] = [_todo]
        if pos == 1:
            self.get_result(False)
#=====================================================================  x
            if 1<0:
                if 'hy' not in _todo:
                    if _last:
                        _todo['hy'] = [self.cache[1][1]['mole']]+_last.get('hy',[])[:fibo[-1]]
                    else:
                        _todo['hy'] = []
                _prcs = self.cache[1][0]['mole']
                _list = [_prcs] + _todo['hy']
                _todo['ym']={}
                _todo['ys']={}
                for i in fibo:
                    _str_ = str(i)
                    if _last and len(_last.get('ym',{}))==len(fibo):
                        vle = ma(_prcs,_last['ym'][_str_],i)
                        _todo['ys'][_str_] = st(vle,[one for one in _list[:i]],i)
                    else:
                        vle = 0.0
                        _todo['ys'][_str_] = 0.0#
                    _todo['ym'][_str_] = vle
#=====================================================================
        all_state[self.symbol][pos] = _todo['from']
        _todo['do']=1
        _todo['time'] = time.time()
        if _last:
            self.cache[pos] = [_todo,_last]
        else:
            self.cache[pos] = [_todo]
        for m in [1,2,3]:
            a = all_state[self.symbol].get(m,None)
            if a:
                _todo[str(m)] = a
        self.db[pos].save(_todo)
        return _todo
    def get_data(self,pos,len,groutp,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(len),skip=int(offset)*int(len)))
        out = []
        for i in result:
            i['_pos_'] = int(pos)
            i['_symbol_'] = self.symbol
            if 'time' in i:
                out.append('''%(_id)s <a target="_blank" href="/delete_k/%(_symbol_)s/%(_pos_)d/%(_id)s/molebot">---del---</a>  %(time).3f'''%i)
            else:
                out.append('''%(_id)s <a target="_blank" href="/delete_k/%(_symbol_)s/%(_pos_)d/%(_id)s/molebot">---del---</a> none'''%i)
        return '<br/>'.join(out)
    def get_image(self,pos,lens,group,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(lens),skip=int(offset)*int(lens)))
        _s = cache['symbol'][self.symbol]
        if len(_s)>50:
            _l = [_s[:50],_s[50:],self.symbol]
        else:
            _l = [_s,self.symbol]
        _l += cache.get('weeks',{}).values()
        _l += ['='*10]
        _l += cache.get('his_%s'%self.symbol,['none'])[::-1]
        out = SVG(group,result[::-1],_l,data).to_html()
        return out
    def only_image(self,pos,lens,group,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(lens),skip=int(offset)*int(lens)))
        out = SVG(group,result[::-1],[self.symbol+" "+str(datetime.datetime.now())[:19]],data).to_html()
        return out
############################################################################################################
'''
#        end
'''
############################################################################################################
