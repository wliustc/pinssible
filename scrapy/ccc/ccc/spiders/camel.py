# -*- coding: utf-8 -*-
import scrapy
#from items import CccItem
from funs import *
from ccc.items import CccItem

def html_trim(str):
	str = re.sub("\s+", ' ', str)
	return str.strip()

class CamelSpider(scrapy.Spider):
	name = "camel"
	allowed_domains = ["www.camelcamelcamel.com"]
	start_urls = (
		'http://camelcamelcamel.com/top_drops',
	)

	def parse(self, response):
		print "*" * 50 , "Calling parse", "*" * 20
		idx = 0
		#print response.xpath("//td.deal_top_outer]")
		items = []
		for sel in response.xpath("//td/div"):
			url = sel.xpath('h3/a/@href').extract()
			if (url):
				url = url[0]
				url = url.split("?")[0]
				asin = url[url.rfind("/") +1 :]
				is_best = sel.xpath('h3/div/a/text()').extract()
				if (is_best):
					is_best = html_trim(is_best[0])
				else:
					is_best = ""
				if (is_best.startswith("Best")):
					is_best = 1
				else:
					is_best = 0
				item = CccItem()
				item['asin'] = asin
				item['is_best'] = is_best
				items.append(item)
				#print idx, asin, is_best
			else:
				current_price = sel.xpath("div[1]/text()").extract()
				list_price = sel.xpath("div[2]/span/text()").extract()
				current_price = get_price(current_price[0])
				list_price = get_price(list_price[0])
				#print current_price, list_price
				items[idx]['list_price'] = list_price
				items[idx]['sale_price'] = current_price
				idx = idx + 1
		fetch_day = get_day_index()
		for item in items:
			item['fetch_day'] = fetch_day
			#print item
		return items
			#print idx, sel.xpath('h3/a/@href').extract()
			#print idx, sel.xpath('h3/div/a/text()').extract()
			
			#print sel.xpath("text") .extract()
			#link = sel.xpath("a")
			#best_tag = sel.xpath("div/a")
			#print link.xpath("@href/text()").extract()
		#for sel in response.xpath("//a[@href='/support/gdb']/text()"):
		#	print sel.extract().strip()
			
