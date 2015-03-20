# -*- coding: utf-8 -*-
import scrapy
#from items import CccItem
from funs import *
from ccc.items import CccItem

class CamelSpider(scrapy.Spider):
	name = "camel"
	allowed_domains = ["www.camelcamelcamel.com"]
	start_urls = (
		'http://camelcamelcamel.com/top_drops',
	)
	
	def start_requests(self):
		requests = []
		asins= ['B00009NDCX', 'B0090JVF1A', 'B00FAQW2RS']
		for asin in asins:
			url = get_amazon_itemurl(asin)
			requests.append(self.make_requests_from_url(url))
		return requests

	def parse(self, response):
		filename = response.url.split("/")[-1] + ".html"
		with open(filename, 'wb') as f:
			f.write(response.body)
	