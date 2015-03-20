# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CccItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    is_best = scrapy.Field()
    sale_price = scrapy.Field()
    list_price = scrapy.Field()
    fetch_day = scrapy.Field()
    pass
class ProductItem(scrapy.Item):
    asin = scrapy.Field()
    pass
