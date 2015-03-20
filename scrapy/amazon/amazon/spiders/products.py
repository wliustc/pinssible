# -*- coding: utf-8 -*-
import scrapy
#from items import CccItem
from funs import *
from amazon.items import AmazonItem

class CamelSpider(scrapy.Spider):
	name = "products"
	allowed_domains = ["www.camelcamelcamel.com"]
	start_urls = (
		'http://camelcamelcamel.com/top_drops',
	)
	
	def start_requests(self):
		requests = []
		conn = get_mysql_connection("root", "root", "ecommerce")
		day_index = get_day_index()
		sql = "select asin from camel_item where fetch_day = " + str(day_index)
		cursor = conn.cursor()
		cnt = cursor.execute(sql)
		if (cnt <= 0):
			cursor.close()
			conn.close()
			return []
		rows = cursor.fetchall()
		for row in rows:
			asin = row[0]
			url = get_amazon_itemurl(asin)
			requests.append(self.make_requests_from_url(url))
			print "********" , url, len(rows)
			break
		cursor.close()
		conn.close()
		return requests

	def __get_item_text_by_ids(self, response, ids):
		if (type(ids) == str):
			ids = [ids]	
		val = ""	
		for id in ids:
			path = "//*[@id='%s']/text()" % (id)	
			val = response.xpath(path).extract()
			#print "Path: ", path, ", val: ", val
			if (val):
				break
		if (type (val) == list):
			val = val[0]	
			val = val.strip()	
		return val

	def parse(self, response):
		asin = response.url.split("/")[-1]
		#filename = response.url.split("/")[-1] + ".html"
		#with open(filename, 'wb') as f:
		#	f.write(response.body)
		item = get_item_detail(response.body)
		#print item
		db_item = AmazonItem()
		for key in item.keys():
			db_item[key] = item[key]
		db_item['asin'] = asin
		#print db_item
		return db_item
		"""
		deal_price = self.__get_item_text_by_ids(response, [
			"priceblock_dealprice",  "priceblock_ourprice",
			"actualPriceValue",  "priceblock_saleprice"
		])
		#print "Deal price: ", deal_price
		brand  = self.__get_item_text_by_ids(response, ["brand", "amsPopoverTrigger"])
		if (not brand):
			print "Try brand with other way"
			brand = response.xpath("//*[@id='product-title_feature_div']/div/span/a/text()").extract()
		#print "Brand: ", brand
		productTitle = self.__get_item_text_by_ids(response, ["productTitle", "btAsinTitle"])
		#print "Product title: ", productTitle
		
		image_element = response.xpath("//*[@id = 'landingImage']")
		image_small = ""
		image_big = ""
		image_list = ""
		if (image_element):
			image_small = image_element.xpath("@src").extract()
			image_big = image_element.xpath('@data-old-hires').extract()
			image_list = image_element.xpath('@data-a-dynamic-image').extract()
		
		#rank_cat = response.css(".zg_hrsr_ladder").extract()
		rank_cat = response.xpath("//*[@id='SalesRank']/td[2]/ul/li[1]/span[1]/text()").extract()
		if (rank_cat):
			#rank_cat = rank_cat_ele.text
			print "Rank in cat: ", rank_cat
		cat = response.xpath("//*[@id='SalesRank']/td[2]/ul/li[1]/span[2]/text()").extract()	
		print cat
		"""
		#cat = ""
		#cat = get_item_text_by_soup(soup, "wayfinding-breadcrumbs_feature_div")
		#if (not cat):
		#	crumb_ele = soup.find(class_ = "detailBreadcrumb")
		#	if (crumb_ele):
		#		cat = crumb_ele.text
		#cat = re.sub("\s+", " ", cat).strip()
		
		
