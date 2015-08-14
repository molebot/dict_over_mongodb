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


vsn = '2015.08.08.3'



def filelog(symbol,i,j,o):
    p = dict2str(o)
    file_log[i].error('#%s#%d#%d#%d#%s#'%(symbol,i,j,len(p),p))

def getprice(one):
    return (one['h']+one['l'])/2.0
cache['hh'] = {}

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
        uu = zz(1,0,7, 1,q=-2)*myth-1*zz(1,0,7,-1,q=-2)
        nn = zz(1,0,7,-1,q=-2)*myth-1*zz(1,0,7, 1,q=-2)
        uu,uuu = uu2,uu
        nn,nnn = nn2,nn
        uuu=min(uuu, 100*(1+myth))#*2.0
        nnn=max(nnn,-100*(1+myth))#*2.0
        if uuu<100*myth:
            uuu = 100*myth+(100*myth-uuu)
        if nnn>-100*myth:
            nnn = -100*myth-(nnn+100*myth)
#        uu,uuu = uuu,uu
#        nn,nnn = nnn,nn
        _blue = (_fox+_just)/2.0
        _blue = max(-280,_blue)
        _blue = min( 280,_blue)
        saved['old'] = []
        ks = max(abs(_max),abs(_min))/max(0.001,_max-_min)
        for i in self.todo:
            c[i][0]['vsn'] = vsn
            c[i][0]['point'] = saved.get('point',c[1][0]['c'])
            c[i][0]['mole'] = _blue
            c[i][0]['just'] = _just# = saved['old'][2][1]
            c[i][0]['k1'] = kmm(1)
            c[i][0]['uuu'] = uuu
            c[i][0]['nnn'] = nnn
            c[i][0]['uu'] = uu
            c[i][0]['nn'] = nn
            c[i][0]['fox'] = _blue
            self.cache[i][0] = c[i][0]
            self.save(i,c[i][0])

        short = saved.get('short',0)
        llong = saved.get('long',1)
        dead = saved.get('dead',0)
        LS = saved.get('ls',1)
        Point = saved.get('point',c[1][0]['c'])
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
            saved['base_ma'] = ma(saved['base_p'],saved.get('base_ma',0),5)
            saved['fill'] = fill = 0
            if _day_.hour==9 and _day_.minute<30:
                saved['dead'] = dead = 0
                saved['base_p']=0
            elif _day_.hour==15:
                saved['dead'] = dead = 0
                saved['base_p']=0
            else:
                saved['dead'] = dead = 1
                _p = saved.get('base_p',0)
                if _p==0:
                    saved['base_p'] = 0.0001
                else:
                    saved['base_p'] = _p+_profit

        if fill<1:
            if LS2*(c[1][0]['c']-Point)>=10:
                saved['fill'] = fill = 1
        #=======================================
        if _day_.hour==15 and _day_.minute>10:
            saved['dead'] = dead = 0
            saved['base_p']=0
            closeit = 0
        else:
            closeit = 1
        out['result'] = LS2*dead*closeit
        out['long'] = llong
        out['short'] = short
#        out['fill'] = fill
#        out['uuu'] = uuu
#        out['nnn'] = nnn
#        out['just'] = _blue
        out['point'] = saved.get('base_p',0)#-max(saved.get('base_ma',0),saved.get('daybase',0))
#        out['profit'] = saved.get('base_p',0)
        #self.state['his']
        if self.state.get('ss',0)!=LS2:
            time_str = _day_.strftime('%m.%d.%H:%M:%S')
            self.state['ss']=LS2
            _his = self.state.get('his',['none'])
            _his.append('%s#%.1f=%d@%.1f'%(time_str,self.realprice,LS2,saved.get('base_p',0)))
            self.state['his'] = _his[-26:]
        self.result = out
        self.all_result()
    def day_level(self):
        saved = self.state
        _p = saved.get('base_p',0)*0#-max(saved.get('base_ma',0),saved.get('daybase',0))
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
            _p = saved.get('base_p',0)#-saved.get('daybase',0)
            thread.start_new_thread(alertmail,('%s_%.1f_%.1f'%(acc.account,self.money,_p),))
            return (new,now)
        return (now,last)

    def check_base(self,pos,_todo,_last):
        if _last and 'old' not in _todo:
            if 'old' in _last:_last.pop('old')
            _todo['old'] = _last
        _flow = [
        ('m','s','hr',getprice),
        ('zm','zs','hz',zmm),
        ('xm','xs','hx',dmm),
        ]
        if _last:
            for mm,ss,hh,func in _flow:
                if hh not in _todo:
                    _todo[hh] = [func(_last)]+_last[hh][:fibo[-1]]
                _prcs = func(_todo)
                _list = [_prcs] + _todo[hh]
                _todo[mm]={}
                _todo[ss]={}
                for i in fibo:
                    _str_ = str(i)
                    vle = ma(_prcs,_last[mm][_str_],i)
                    _todo[ss][_str_] = st(vle,[one for one in _list[:i]],i)
                    _todo[mm][_str_] = vle
        else:
            for m,s,h,func in _flow:
                if hh not in _todo:
                    _todo[hh] = []
                _prcs = func(_todo)
                _list = [_prcs] + _todo[hh]
                _todo[mm]={}
                _todo[ss]={}
                for i in fibo:
                    _str_ = str(i)
                    vle = _prcs
                    _todo[ss][_str_] = 0.0
                    _todo[mm][_str_] = vle
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
class Base:pass
############################################################################################################
'''
#        end
'''
############################################################################################################
