vsn = 'in.2015.08.25.re1'
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
    def get_result(self,passit=-1):
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
        a = 1
        b = 3
        ppp = abs(kmm(a))
        pk = (ppp/(100*myth))**(1+myth)
        pss = pk*(kmm(a)-zz(a,0,7,0))+zz(a,0,7,0)
        _fox = zz(b,0,7,0)+pss*kw(b,pp=-2)/(myth*200)
        _just = zz(b,0,7,0)+kmm(a)*kw(b,pp=-2)/(myth*200)

        ppp0 = abs(kmm(a-1))
        pk0 = (ppp0/(100*myth))**(1+myth)
        pss0 = pk0*(kmm(a-1)-zz(a-1,0,7,0))+zz(a-1,0,7,0)
        _fox0 = zz(b-1,0,7,0)+pss0*kw(b-1,pp=-2)/(myth*200)
        _just0 = zz(b-1,0,7,0)+kmm(a-1)*kw(b-1,pp=-2)/(myth*200)

        uuu = -1*zz(b,0,7,-1,q=-1)
        nnn = -1*zz(b,0,7, 1,q=-1)
        uk = min(1.0,abs(max(0,uuu))/abs(nnn))
        nk = min(1.0,abs(min(0,nnn))/abs(uuu))
        uu = -1*uk*zz(a,0,7,-1,q=-2)
        nn = -1*nk*zz(a,0,7, 1,q=-2)
        uu2 = uu-myth*nn
        nn2 = nn-myth*uu
        uuu = uu2
        nnn = nn2

        _blue = (_fox+_just)/2.0
        _blue0 = (_fox0+_just0)/2.0
#        _blue = (_blue+_blue0)/2.0
        _blue = max(-280,_blue)
        _blue = min( 280,_blue)
        _blue,_blue0=_blue0,_blue

        uu = -1*zz(0,0,7,-1,q=-2)
        nn = -1*zz(0,0,7, 1,q=-2)
#        if _blue0>100*(1+myth):
#            _blue0 -= (_blue0-(1+myth)*100)*2.0
#        elif _blue0<-100*(1+myth):
#            _blue0 += (-100*(1+myth)-_blue0)*2.0
        uuu = _blue0+uu
        nnn = _blue0+nn

        uu = uu2
        nn = nn2
        uuu=min(uuu, 100*(1+myth))#*2.0
        nnn=max(nnn,-100*(1+myth))#*2.0
#        if uuu<100*myth:
#            uuu = 100*myth+(100*myth-uuu)
#        if nnn>-100*myth:
#            nnn = -100*myth-(nnn+100*myth)
        _blue -= (uu+nn)/2.0
        if passit>=0:
            todo = [passit]
        else:
            todo = self.todo
        for i in todo:
            c[i][0]['point'] = saved.get('point',c[1][0]['c'])
            c[i][0]['mole'] = _blue
            c[i][0]['just'] = _blue0# = saved['old'][2][1]
            c[i][0]['uuu'] = uuu
            c[i][0]['nnn'] = nnn
            c[i][0]['uu'] = uu
            c[i][0]['nn'] = nn
            c[i][0]['fox'] = _blue
            self.cache[i][0] = c[i][0]
            self.save(i,c[i][0])
        if passit>0:return c[passit][0]
        short = saved.get('short',0)
        llong = saved.get('long',1)
        dead = saved.get('dead',0)
        LS = saved.get('ls',1)
        Point = saved.get('point',c[1][0]['c'])
        real = saved.get('real',self.realprice)
        fill = saved.get('fill',0)
        daybase = saved.get('daybase',0.0)




        _pos_ = a = 0
        _pass = (_blue-(uuu+nnn)/2.0)
        blast = _blue
        _just = 0

        if short==0 and c[_pos_][0].get('doit',0)==0:
            if llong*_pass>0:# DON'T CHANGE HERE
                if (blast>nnn) and zz(a,0,3,-1,q=-1)>zz(a,1,3,-1,q=-1):
                    saved['short'] = short = 1
                    logger.error('++')
                if (blast<uuu) and zz(a,0,3, 1,q=-1)<zz(a,1,3, 1,q=-1):
                    saved['short'] = short = -1
                    logger.error('--')
            else:
                if _pass*llong<0:
#                    if blast>max(uu,uuu):
                    if uuu+nnn>uu+nn:
                        saved['short'] = short = 1
                        logger.error('+!')
#                    if blast<min(nn,nnn):
                    if uuu+nnn<uu+nn:
                        saved['short'] = short = -1
                        logger.error('-!')
        elif c[_pos_][0].get('doit',0)==0:
            if short>0 and (blast<nnn) and zz(a,0,3,-1,q=-1)<zz(a,1,3,-1,q=-1):
                saved['short'] = short = 0
                logger.error('+=')
            if short<0 and (blast>uuu) and zz(a,0,3, 1,q=-1)>zz(a,1,3, 1,q=-1):
                saved['short'] = short = 0
                logger.error('-=')

        if short!=0 and short!=llong:
            saved['long'] = llong = short
        if short==0:
            LS2 = -1*llong
        else:
            LS2 = short

        changed = False

        _day_ = self.day
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
                    saved['base_p'] = _p+_profit-1

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
        self.todo = [4,3,2,0,1]
        for i in self.todo:self.db[i] = conn[self.symbol][str(i)]
        self.out = {}
        self.last = {}
        _a = allstate[self.symbol]
        if _a:
            self.state = _a[0]
        else:
            self.state = {}
        self.cache = {}
        self.offset = 1
        self.day = datetime.datetime.now()
        self.hour = self.day.hour
    def all_result(self):
        allstate[self.symbol] = self.state
        return {'state':self.state,'result':self.result}
    def price(self,price):
        for i in self.todo:
            self.new_price(price,i)
    def new_price(self,price,pos):
        _result = list(self.db[pos].find({'do':1},sort=[('_id',desc)],limit=3))
        self.last[pos] = _result
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
    def getmoney(self,p):self.money = p
    def check_k_len(self,now,length,last,pos):
        if now['h']-now['o']>length:
            high = now['h']
            now['h'] = now['o']+length
            now['c'] = now['o']+length
            new = {'o':now['c'],'h':high,'l':now['c'],'c':now['c'],'do':0,'hour':self.hour,'point':now.get('point',0)}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            now = self.check_base(pos,now,last)

            return self.check_k_len(new,length,now,pos)
        elif now['o']-now['l']>length:
            low = now['l']
            now['l'] = now['o']-length
            now['c'] = now['o']-length
            new = {'o':now['c'],'h':now['c'],'l':low,'c':now['c'],'do':0,'hour':self.hour,'point':now.get('point',0)}

            new['cnt'] = now.get('cnt',0)+1
            new['_id'] = now['_id']+1

            now = self.check_base(pos,now,last)

            return self.check_k_len(new,length,now,pos)
        else:
            return (now,last)
    def check_k_hour(self,now,last,pos):
        if now.get('hour',-1)!=self.hour:
            p = now['c']
            new = {'o':p,'h':p,'l':p,'c':p,'do':0,'hour':self.hour,'point':now.get('point',0)}
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
#        ('pm','ps','hp',pmm),
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
            for mm,ss,hh,func in _flow:
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
        if pos==1:
            _todo = self.get_result(passit=pos)
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
        _time = time.time()-(1+pos)*2*24*3600
        self.db[pos].remove({'time':{'$lt':_time}})
#=====================================================================
    def get_image(self,pos,lens,group,offset=0):
        data = self.db[int(pos)]
        result = list(data.find(sort=[('_id',desc)],limit=int(lens),skip=int(offset)*int(lens)))
        if self.day.strftime('%m.%d') in self.state.get('his',['none'])[-1]:
            _l = self.state.get('his',['none'])[::-1]
        else:
            _l = ['none']
            self.state['his'] = _l
            allstate[self.symbol] = self.state
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
