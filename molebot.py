#coding:utf-8
from bottle import route,run,debug,request,redirect,response,error,static_file
import bottle,os,acc
from cmath import log as mathclog
from math import e as mathe
from hashlib import sha1
import time,sys,datetime,random
from xml2dict_encoder import XML2Dict as x2d
from carbon import Iron,vsn
from svgcandle import *
from core import *
from handlers import MongoHandler
#from urllib2 import urlopen
from settings import mongo_server
from qqmail import *
import thread
import requests

ver = '.out.2015.08.24'

def mathlog(a):return mathclog(a).real
#20150817aaa
def cffdata(a,b):
    _day = datetime.datetime.now()
    _time = _day.hour*60+_day.minute
    if acc.account=='me' and ( 555<=_time<=690 or 780<=_time<=915 ):
        dd = {}
        dd['data'] = cache.get('rs','none')
        r = requests.post('http://molebot.com/cff531',data=dd)
        return r.text

cache['pass'] = time.time()+7*24*3600
cache['long']='100'
cache['_'] = {}

def now():return datetime.datetime.now()
def logten():
    if cache['pass']<time.time():
        alertmail('%s reboot'%acc.account)
        os.system("reboot")
    ip = request['REMOTE_ADDR']
    day= datetime.datetime.now().strftime("_%Y_%m_%d_%H")
    url = request.environ['PATH_INFO']+day
    if 'url' not in cache:
        cache['url'] = {}
    if ip+url not in cache['url']:
        cache['url'][ip+url]=0
        if len(cache['url'])>200:
            cache['url']={}
            logger.error('clear cache url')
        if 'Mozilla/4.0' in request.environ.get('HTTP_USER_AGENT','no agent'):
            pass
        else:
            logger.error('''url @ %s [ <a href="http://www.baidu.com/s?wd=%s&_=%.0f" target="_blank">%s</a> ] %.1f
                <span style="color:gray">%s</span>'''%(url,ip,time.time()/10,ip,cache['pass']-time.time(),request.environ.get('HTTP_USER_AGENT','no agent')))
    return True#request.cookies.get('cookie', '0') in cache['cookie']

@route('/all/:o')
def index_show_svg(o):
    logten()
    n = 'see2'
    l = '100'
    m = '3'
    if 1>0:
        return '''<!DOCTYPE html>
    <html><head><title></title></head><body>
    %s <br/> %s
    </body></html>
    '''%(Iron('cff2if').get_image(m,l,n,offset=int(o)),''.join(['''
        <a href="/all/%d" target="_blank">-%d-</a>
        '''%(i,i) for i in range(15)]))

@route('/all1/:o')
def index_show_svg(o):
    logten()
    n = 'see2'
    l = '100'
    m = '1'
    if 1>0:
        return '''<!DOCTYPE html>
    <html><head><title></title></head><body>
    %s <br/> %s
    </body></html>
    '''%(Iron('cff2if').get_image(m,l,n,offset=int(o)),''.join(['''
        <a href="/all1/%d" target="_blank">-%d-</a>
        '''%(i,i) for i in range(15)]))

@route('/only/:o')
def index_show_svg(o):
    logten()
    n = 'only'
    l = '100'
    m = '1'
    if 1>0:
        return '''<!DOCTYPE html>
    <html><head><title></title></head><body>
    %s <br/> %s
    </body></html>
    '''%(Iron('cff2if').get_image(m,l,n,offset=int(o)),''.join(['''
        <a href="/only/%d" target="_blank">-%d-</a>
        '''%(i,i) for i in range(15)]))

@error(500)
def error500(error):
    try:
        logger.error(error.traceback)
    finally:
        return ''
@error(404)
def error404(error):
    logten()
    return ''

@route('/read_xml/:a/:b/')
def read_xml(a,b):
    thread.start_new_thread(alertmail,('start %s'%acc.account,))
    return 'ok'

@route('/show/logs')
def show_logs():
    logten()
    _list = MongoHandler().show()
    _dt = datetime.timedelta(hours=8)
    if _list:
        out = ''.join([ '<pre>%s >>> %s</pre>'%((_dt+one['timestamp'].as_datetime()).strftime("%Y-%m-%d %H:%M:%S"),one['message']) for one in _list])
        return '''<html><head><title>%s</title><META HTTP-EQUIV="REFRESH" CONTENT="10"></head><body>
                %s</body></html>'''%((_dt+_list[0]['timestamp'].as_datetime()).strftime("%H:%M:%S"),out)
    else:
        return '''<html><head><META HTTP-EQUIV="REFRESH" CONTENT="100"></head><body>
                <br/></body></html>'''

@route('/:s/pass')
def passok(s):
    global cache
    cache['pass'] = int(s)*24*3600*21+time.time()
    thread.start_new_thread(cffdata,(1,2))
    return 'ok'

@route('/:s/plus/')
def passokpp(s):
    thread.start_new_thread(alertmail,('%s_onoff_%s'%(acc.account,s),))
    cache['doit'] = min(2,int(s))
    redirect('/w/')

@route('/kaiguan')
def kaiguan():
    if cache.get('doit',0)==0:
        cache['doit'] = 1
    else:
        cache['doit'] = 0
    thread.start_new_thread(alertmail,('%s_onoff_%d'%(acc.account,cache['doit']),))
    redirect('/')

@route('/')
def index21():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)*cache.get('closeit',1)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="10"><title>%s</title></head><body><h2>开关：<a href="/kaiguan">-= %d =-</a> 0:停止交易 1:启动交易</h2>
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        rs = htm%(str(datetime.datetime.now()),doit,pp.get_image('3','80','see'),pss,'<h1>%s</h1>'%vol,timestr,vsn+ver)
        cache['rs'] = rs
        return rs

@route('/w/')
def index21e():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)*cache.get('closeit',1)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="10"><title>%s</title></head><body><h2>开关：%s 0:停止交易 1~n:启动交易手数</h2>
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        onoff = ['''<a href="/%d/plus/"># %d #</a>'''%(xx,xx) for xx in range(3)]
        onoffnow = '''-= %d =-'''%doit
        oostr = onoffnow+" [ "+','.join(onoff)+" ] "
        rs = htm%(str(datetime.datetime.now()),oostr,pp.get_image('3','80','see'),pss,'<h1>%s</h1>'%vol,timestr,str(vsn))
        cache['rs'] = rs
        return rs

@route('/1s/')
def index21s():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)*cache.get('closeit',1)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="1"><title>%s</title></head><body>%s
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/><h2>开关：<a href="/kaiguan">-= %d =-</a> <br/>0:停止交易 1:启动交易</h2></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        return htm%(str(datetime.datetime.now()),str(cache.get('result',{})),pp.get_image('3','80','see'),pss,'<h1>%s</h1>'%vol,doit,timestr,str(vsn))

@route('/back/')
def index221():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="10"><title>%s</title></head><body>
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/><h2>开关：<a href="/kaiguan">-= %d =-</a> <br/>0:停止交易 1:启动交易</h2></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        return htm%(str(datetime.datetime.now()),pp.get_image('3','80','see2'),pss,'<h1>%s</h1>'%vol,doit,timestr,str(vsn))

@route('/1/')
def index21():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="10"><title>%s</title></head><body>
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/><h2>开关：<a href="/kaiguan">-= %d =-</a> <br/>0:停止交易 1:启动交易</h2></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        return htm%(str(datetime.datetime.now()),pp.get_image('1','80','see'),pss,'<h1>%s</h1>'%vol,doit,timestr,str(vsn))

@route('/back/1/')
def index21():
    logten()
    if 1>0:
        ps = cache.get('result',{}).get('result',0)
        p = cache.get('point','00000.0')
        vol = cache.get('vol','0.0')
        if ps>0:
            pss = '<font color="red">%.2f</font>'%float(p)
        elif ps<0:
            pss = '<font color="green">%.2f</font>'%float(p)
        else:
            pss = '<font color="gray">%.2f</font>'%float(p)
        doit = cache.get('doit',0)
        now = datetime.datetime.now()+datetime.timedelta(days=15)
        timestr = now.strftime('%y%m')
        htm = u'''<!DOCTYPE html>
    <html><head><META HTTP-EQUIV="REFRESH" CONTENT="10"><title>%s</title></head><body>
<table><tr>
   <td>%s</td>
   <td><h1>%s<br/>%s</h1><br/><br/><br/><h2>开关：<a href="/kaiguan">-= %d =-</a> <br/>0:停止交易 1:启动交易</h2></td>
</tr></table>
IF%s<br/>
ver:%s
    </body></html>
    '''
        pp = Iron('cff2if')
        return htm%(str(datetime.datetime.now()),pp.get_image('1','80','see2'),pss,'<h1>%s</h1>'%vol,doit,timestr,str(vsn))

@route('/log/:a')
def logit(a):
    _day_ = datetime.datetime.now()
    hour_str = _day_.strftime('%Y%m%d')
    if cache.get('log_hour','')!=hour_str:
        cache['log_hour'] = hour_str
        logger.error('logten month %d day %d hour %d weekday %d'%(_day_.month,_day_.day,_day_.hour,_day_.isoweekday()))
    logger.error('log # %s'%a)
    return ''
#============================================================================================================================

@route('/molebot')
def show_index():
    logten()
    return '''
        <html><head>
        <style>
a
{
display:block;
margin:15px;
background-color:#dddddd;
}
</style>
        </head><body><h1>
        <a href="/show/logs" target="_blank">log</a>
        <br/>
        <a href="/" target="_blank">time</a>
        <br/>
        <a href="/load/cff2if/data" target="_blank">load_data</a>
        <a href="/load/molebot/file" target="_blank">load_out</a>
        <a href="/load/carbon/file" target="_blank">load_in</a>
        <br/>
        </h1>
        </body></html>
        '''

@route('/data/:symbol/:pos/molebot')
def dataout2(symbol,pos):
    return Iron(symbol).data_out(int(pos))

@route('/load/:symbol/data')
def dataout(symbol):
    raw = 'https://raw.githubusercontent.com/molebot/dict_over_mongodb/master/%d.txt'
    from requests import get as rget
    a=0
    for ii in [0,1,2,3]:
        cc = rget(raw%ii,timeout=60)
        if cc.status_code==200:
            a+=cc.status_code
            f = open('/root/local/%d.txt'%ii,'w')
            f.writelines(cc.content)
            f.close()
    p = Iron(symbol)
    return p.data_in()+":%d"%a

@route('/load/:filename/file')
def filein(filename):
    raw = 'https://raw.githubusercontent.com/molebot/dict_over_mongodb/master/%s.py'%filename
    from requests import get as rget
    cc = rget(raw,timeout=60)
    if cc.status_code==200:
        f = open('/root/local/%s.py'%filename,'w')
        f.writelines(cc.content)
        f.close()
        return '%s,%d'%(filename,len(cc.content))
    return 'error'

upstate={}
@route('/real/:types/:symbol/:price/:vol/')
def doreal(types,symbol,price,vol):
    _day = datetime.datetime.now()
    _time = _day.hour*60+_day.minute
    if '192.168.' in request['REMOTE_ADDR'] and ( 555<=_time<=690 or 780<=_time<=915 ) and float(price)>0:
        global allstate
        global cache
        tt = time.time()
        if 'symbol' not in cache:cache['symbol'] = {}
        cache['symbol'][types] = symbol
        tick = Iron(types)
        tick.real(float(price))
        tick.getmoney(float(vol))
        tick.price(mathlog(float(price))*3400.0)
        tick.get_result()
        result = tick.result
        cache['result'] = result
        cache['point'] = price
        cache['vol'] = vol
        _level = tick.day_level()
        if cache.get('closeit',1)<1 and result['short'] != 0:
            cache['closeit'] = 1
            cache['result']['close'] = 'none'
        if _level>0:
            if result['short'] == 0:
                uuu = result['uuu']
                nnn = result['nnn']
                _just = result['just']
                if result['result']>0 and uuu-_just<(uuu-nnn)*(myth**(_level+2)):
                    cache['closeit'] = 0
                    cache['result']['close'] = price
                if result['result']<0 and _just-nnn<(uuu-nnn)*(myth**(_level+2)):
                    cache['closeit'] = 0
                    cache['result']['close'] = price
        rs = '{"symbol":"%s","result":"%d"}'%(symbol,result['result']*cache.get('doit',0)*cache.get('closeit',1))
        logger.error('%.4f'%(time.time()-tt))
        cache['cache'] = rs
        return rs
    else:
        return cache.get('cache','{"symbol":"%s","result":"0"}'%symbol)
cff={}
@route('/cffif/:p/data')
def apicff(p):#	s symbol b deadline_base o base a account t aceq p price
    _day = datetime.datetime.now()
    _time = _day.hour*60+_day.minute
    if '192.168.' in request['REMOTE_ADDR'] and ( 555<=_time<=690 or 780<=_time<=915 ):
        global cache
        tt = time.time()
        pp = Iron('cff2if')
        pp.real(float(p))
        pp.getmoney(float(0.0))
        pp.price(mathlog(float(p))*3400.0)  #   delay 15 min
        pp.get_result()
        result = pp.result
        cache['point'] = p
        cache['result'] = result
        _level = pp.day_level()
        if cache.get('closeit',1)<1 and result['short'] != 0:
            cache['closeit'] = 1
        if _level>0:
            if result['short'] == 0:
                uuu = result['uuu']
                nnn = result['nnn']
                _just = result['just']
                if result['result']>0 and uuu-_just<(uuu-nnn)*(myth**(_level+2)):
                    cache['closeit'] = 0
                if result['result']<0 and _just-nnn<(uuu-nnn)*(myth**(_level+2)):
                    cache['closeit'] = 0
        logger.error('%.4f'%(time.time()-tt))
        return 'd'
    else:
        logger.error("ERROR DATA REQUEST")
        logger.error('url @ %s [ %s ]'%(request.environ['PATH_INFO'],request['REMOTE_ADDR']))
        return 'd'
