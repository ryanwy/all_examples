#!/usr/bin/python

import requests
import copy
import os
import sys
from twisted.internet import reactor
from twisted.internet import task

class CheckProxy(object):
    
    def __init__(self, path):
        self.pathname = path
        self.origin_proxies = []
        self.proxies = []
    
    def read_file(self):
        try:
            with open(self.pathname) as f:
                for l in f.readlines():
                    l = l.strip('\n')
                    if l:
                        self.proxies.append(l)
        except Exception as e:
            print e
        else:
            print "read done"

    def write_file(self):
        try:
            with open(self.pathname, 'w') as f:
                f.writelines(self.proxies)
        except Exception as e:
            print e
        else:
            print "write done"

    def make_response(self, proxy):
        origin_proxy = copy.deepcopy(proxy)
        print 'checking ' + proxy
        try:
            self.set_env_proxy(origin_proxy)    
            proxy_dict = {'http': 'http://' + proxy}
            r = requests.get('http://httpbin.org/ip', proxies=proxy_dict,
timeout=5)          
            data = r.json()
        except Exception as e:
            self.origin_proxies.remove(origin_proxy)
            print 'proxy ' + origin_proxy + ' is invalid'
            print e

    def check_proxy(self):
        if self.proxies:
            self.origin_proxies = copy.deepcopy(self.proxies)            
        else:
            print "data empty, exit()"
            reactor.stop()
            sys.exit(0)
        map(self.make_response, self.proxies)

        if self.origin_proxies:
            self.proxies = copy.deepcopy(self.origin_proxies)
            self.write_file()
        else:
            self.proxies = []
            os.system("cat /dev/null >" + self.pathname)
            print "clear file: " + self.pathname
        print "checking all done"

    def set_env_proxy(self, proxy):
        import os
        scheme = 'http'
        if proxy.find(scheme) == -1:
            proxy = scheme + proxy
        os.environ['http_proxy'] = proxy


def main():
    cp = CheckProxy('./pl.txt')
    cp.read_file()
    loop = task.LoopingCall(cp.check_proxy)
    loopDeferred = loop.start(10)

    reactor.run()

if __name__ == '__main__':
    main()
