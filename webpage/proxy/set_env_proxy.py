#!/usr/bin/env python
import copy
import os
import re
import time
import base64
import requests
from threading import Timer
from multiprocessing.dummy import Pool as ThreadPool
from twisted.internet import reactor
from twisted.internet import task


class ConstValue(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstException
        else:
            self.__dict__[name] = value

class ConstException(Exception):
    pass          

class NoProxyException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

const = ConstValue()
const.PATH_NAME = './proxy_list.txt'
const.SLEEP_TIME = 20


class Proxy(object):
    def __init__(self, max_page=1):
        self.max_page = max_page
        self.del_proxies = []
        self.origin_proxies =[]
        self.proxies = []
        self.checked_proxies = []
        self.s = requests.Session()
        self.headers = {
            'Host': 'proxy.peuland.com',
            'Origin': 'https://proxy.peuland.com',
            'Referer': 'https://proxy.peuland.com/proxy_list_by_category.htm',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2692.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'peuland_id=35fefe23fedc52da9283ac5ed131cbab;PHPSESSID=pkm7b65es5ojb8oerc7a9i0q31; peuland_md5=ca1f57155f5638ade3c28a900fbdbd55;w_h=800; w_w=1280; w_cd=24; w_a_h=773; w_a_w=1280; php_id=1792520643'
        }
        self.s.headers.update(self.headers)
        self.url = 'https://proxy.peuland.com/proxy/search_proxy.php'

    def _parse_proxy(self):
        i = 1
        while (i <= self.max_page):
            payload = {
                'type': '',
                'country_code': 'CN',
                'is_clusters': '',
                'is_https': '',
                'level_type': 'anonymous',
                'search_type': 'all',
                'page': str(i),
            }
            r = self.s.post(self.url, data=payload)
            data = r.json()['data']
            print data
            for line in data:
                rate = int(base64.b64decode(line['time_downloadspeed']))
                if rate <= 7:
                    continue
                proxy_type = base64.b64decode(line['type'])
                ip = base64.b64decode(line['ip'])
                port = base64.b64decode(line['port'])
                self.proxies.append({proxy_type: ip + ':' + port})
            i = i + 1

    def _check_proxy(self, proxy, anonymous=False):

        try:
            r = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
            data = r.json()
            if anonymous:
                if data['origin'] == proxy.values()[0].split(':')[0]:
                    self.checked_proxies.append(proxy)
            self.checked_proxies.append(proxy)
        except Exception as e:
            print e

    def get_proxy(self):
        self._parse_proxy()
        pool = ThreadPool(8)
        self.origin_proxies = copy.deepcopy(self.proxies)
        pool.map(self._check_proxy, self.proxies)
        pool.close()
        pool.join()
        self.proxies = copy.deepcopy(self.origin_proxies)
        self.save_proxy()
        return self.checked_proxies

    def save_proxy(self, path=const.PATH_NAME):
        try:
            if not self.proxies:
                print "no proxy data"
                os.system('cat /dev/null > ' + path)     
                raise NoProxyException("no proxy data")
                      
            with open(path, 'w') as f:
                f.write(str(self.origin_proxies))
        except Exception as e:
            print e
        finally:
            print "save over"

    def load_proxy(self):
        if not self.proxies:
            try:
                with open(const.PATH_NAME) as f:
                    input = f.read()
                    if len(input) == 0:
                        return None
                    input = input.replace('[', '')
                    input = input.replace(']', '')
                    input = input.replace('{', '')
                    input = input.replace('}', '')
                    input = input.replace('\'', '')
                    input_list = input.split(',') 
                    for l in input_list:
                        mark = l.find(':')
                        type = l[:mark]
                        ipport = l[mark+1:]
                        if type.lower() == 'https':
                            continue
                        self.proxies.append({type: ipport})
            except Exception as e:
                print e
        return self.proxies   
             
    def parse_proxy(self):
        if not self.checked_proxies:
            raise NoProxyException("no proxy data")
                
    def get_sys_proxy(self):
        """ 
        only useful in LAN connect
        """
        http_proxy = os.environ["http_proxy"]
        https_proxy = os.environ["https_proxy"]
        if http_proxy:
            self.proxies.append({'http': http_proxy})
        if https_proxy:
            self.proxies.append({'https': https_proxy})

    def check_timeout_proxy(self):
        """
        check if proxy is valid every time period 
        """
        if not self.origin_proxies:
            self.origin_proxies = copy.deepcopy(self.proxies)
        map(self.make_response, self.proxies)
        self.proxies = copy.deepcopy(self.origin_proxies)
        if self.del_proxies:
            for i in self.del_proxies:    
                self.proxies.remove(i)        
        
        self.save_proxy()
        loop.stop()
         
    def make_response(self, proxy):
        """
        check if the proxy is valid
        """
        ori_proxy = copy.deepcopy(proxy)
        try:
            self.set_env_proxy(ori_proxy) 
            r = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
            data = r.json()
            print "checking proxy " + str(ori_proxy)
        except Exception as e:
            self.del_proxies.append(ori_proxy)    
            print "proxy" + str(ori_proxy) + " is invalid "
            print e
        else:
            import time
            time.sleep(const.SLEEP_TIME)

    def set_env_proxy(self, proxy):
        """
        set system env, but this can only be set in sub process. if we use this
        proxy to get web page, we must first exec command 'source .bashrc'
        """
        p = str(proxy)
        p = p.replace('[', '')
        p = p.replace(']', '')
        p = p.replace('{', '')
        p = p.replace('}', '')
        p = p.replace('\'', '')
        p = p.replace(' ', '')
        mark = p.find(':')
        type = p[:mark]
        ipport = p[mark+1:]
        if type.lower() == 'http':
            hp = 'http://' + ipport
            print 'http://' + ipport
            #os.environ['http_proxy'] =  'http://' + ipport  
            try:
                #os.system('export http_proxy=' + hp)
                os.environ['http_proxy'] = hp
                #os.system('bash -c \'echo "export http_proxy=' + hp + '" >> ~/.bashrc\'')
                #os.system('bash -c \'source ~/.bashrc\'')        
                #import time
                #time.sleep(const.SLEEP_TIME)
            except Exception as e:
                print e

def cbLoopDone(result):
    print("loop done")
    reactor.stop()

def ebLoopFailed(failure):
    print(failure.getBriefTraceback())
    reactor.stop()

if __name__ == '__main__':
    ins = Proxy()
    proxy_list = ins.load_proxy()
    if not proxy_list:
        ins.get_proxy()                
#    time_interval = 2
#    t = Timer(time_interval, ins.check_timeout_proxy)
#    t.start()
#    while True:
#        time.sleep(1)
#        print "main?"

    loop = task.LoopingCall(ins.check_timeout_proxy)
    loopDeferred = loop.start(10)
    loopDeferred.addCallback(cbLoopDone)
    loopDeferred.addErrback(ebLoopFailed)
   
    reactor.run() 
