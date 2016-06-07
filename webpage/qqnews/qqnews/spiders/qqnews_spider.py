import scrapy
import re

from qqnews.items import qqnewsItem
from scrapy.http import Request
from scrapy.http.request.form import FormRequest
from selenium import webdriver
#from selenium.remote import connect

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

def enc(line):
    for l in line:
        print l.encode('utf-8')

class qqnewsSpider(scrapy.Spider):
    name = 'qqnews'
    allowed_domains = ['news.qq.com',
            'coral.qq.com',
        ]
    start_urls = [
        'http://news.qq.com/a/20160427/003825.htm',
    ]

    #def __init__(self):
        #self.driver = webdriver.Firefox()
    def parse_ajax(self, response):
        print "HERE **************"
        print response.body
        match = re.search(r"\"commentnum\":\"(\w+)\"\}", response.body)
        self.items['comment_num'] = match.group(1)
        print self.items['comment_num']
        yield self.items

    # 'http://news.qq.com/a/20160531/006521.htm'
    def parse(self, response):
        import traceback
        traceback.print_stack()
        #print f1()
        #extra_links = response.xpath("//div[@class='bd']/div[@id='kbContA']/div[@class='list clearfix']/ul/li/a[@target='_blank']/@href").extract()
        #extra_links = ['http://news.qq.com/a/20160602/000303.htm',
        #        'http://news.qq.com/a/20160601/044744.htm'
        #    ]
        #extra_links = ['http://news.qq.com/a/20160602/000303.htm']
        item = qqnewsItem()
        #self.items = item
        #extra_links = ['http://coral.qq.com/article/1383089650/commentnum?callback=_cbSum&source=1&t=0.9233111530535709']
        #for url in extra_links:
        #    yield Request(url, callback = self.parse_ajax )
        
        item['title'] = response.xpath("//div[@class='hd']/h1/text()").extract()
        item['content'] = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        item['msg_src'] = response.xpath("//span[@class='color-a-1']/a[@target='_blank']/text()").extract()
        item['msg_src_link'] = response.xpath("//span[@class='color-a-1']/a[@target='_blank']/@href").extract()
        #item['comment_num'] = response.xpath("//div[@class='tit-bar clearfix']/span[@class='r all-number-comment']/a[@id='cmtNum']/text()").extract()
        
        # html unit driver
        #driver = connect('htmlunit')
        driver = webdriver.Remote('http://127.0.0.1:4446/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
        driver.get(response.url)
        # firefox driver
        #self.driver.get(response.url)
        item['comment_num'] = self.driver.find_elements_by_xpath("//div[@class='tit-bar clearfix']/span[@class='r all-number-comment']/a[@id='cmtNum']")[0].text
        #print enc(item['title'])
        #print enc(item['content'])
        #print enc(item['msg_src'])
        #print enc(item['msg_src_link'])
        yield item
        self.driver.close()
