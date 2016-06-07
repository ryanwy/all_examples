#!/usr/local/bin/python

import sys

from twisted.internet import reactor
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from spiders.qqnews_spider import qqnewsSpider

def test(depth = 0):
    frame = sys._getframe(depth)
    code = frame.f_code

    print "frame depth = ", depth
    print "func name = ", code.co_name
    print "func filename = ", code.co_filename
    print "func lineno = ", code.co_firstlineno
    print "func locals = ", frame.f_locals
def f1():
    names = []
    import inspect
    frame = inspect.currentframe()
    ## Keep moving to next outer frame
    while True:
        try:
            frame = frame.f_back
            name = frame.f_code.co_name
            names.append(name)
        except:
            break
    return names

spider = qqnewsSpider()
settings = get_project_settings()
cp = CrawlerProcess(settings)
crawler = Crawler(spider)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.crawl(spider)
cp.start()
reactor.run()


