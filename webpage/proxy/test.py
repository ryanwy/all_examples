#!/usr/bin/python

import requests

try:
    proxy = {'http': '101.128.101.14:8080'}
    r = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=10)
    print r.json()
except Exception as e:
    print e

