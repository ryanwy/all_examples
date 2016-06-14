import scrapy

from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor as le
from scrapy.spiders import Rule,CrawlSpider
from scrapy.http import Request
from socialqqnews.items import FirstPageItem,SocialqqnewsItem

class SocialnewsSpider(CrawlSpider):
    name = 'qqnews'
    allow_domain = ['news.qq.com']
    start_urls = ['http://news.qq.com/society_index.shtml']
    rules = [
        #Rule(le(allow=('http://news.qq.com/society_index.shtml')), callback='parse_0', follow=True),
        Rule(le(allow=("news.qq.com/a/[0-9]{8}/[0-9]{6}.htm$")), callback='parse_1', follow=True)
    ]
   
    
    def parse_0(self, response):
        item = FirstPageItem()
        item['url'] = response.xpath("//div[@class='Q-tpList']/div[@class='Q-tpWrap']/div[@class='text']/em[@class='f14 l24']/a[@class='linkto']/@href").extract() 
        #print item['url']
        yield item
        #yield Request(item['url'])
 
    def parse_1(self, response):
        item = SocialqqnewsItem()
        item['title'] = response.xpath("//div[@class='hd']/h1/text()").extract()
        item['content'] = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        item['msg_src'] = response.xpath("//span[@class='color-a-1']/a[@target='_blank']/text()").extract()
        item['msg_src_link'] = response.xpath("//span[@class='color-a-1']/a[@target='_blank']/@href").extract()
        yield item
