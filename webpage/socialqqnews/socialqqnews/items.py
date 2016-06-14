# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SocialqqnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    msg_src = scrapy.Field()
    msg_src_link = scrapy.Field()

class FirstPageItem(scrapy.Item):
    url = scrapy.Field()
