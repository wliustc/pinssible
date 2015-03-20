# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  asin = scrapy.Field()
  title = scrapy.Field()
  category = scrapy.Field()
  brand = scrapy.Field()
  shipping = scrapy.Field()
  star = scrapy.Field()
  views = scrapy.Field()
  feature = scrapy.Field()
  description = scrapy.Field()
  details = scrapy.Field()
  weight = scrapy.Field()
  length = scrapy.Field()
  width = scrapy.Field()
  height = scrapy.Field()
  sales_rank = scrapy.Field()
  list_price = scrapy.Field()
  sale_price = scrapy.Field()
  comments = scrapy.Field()
  fetch_time = scrapy.Field()
  detailed_comments = scrapy.Field()
  image_small = scrapy.Field()
  image_big = scrapy.Field()
  image_list = scrapy.Field()
  pass
