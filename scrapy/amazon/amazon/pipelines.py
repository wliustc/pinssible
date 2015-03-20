# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import datetime
#import json

def should_update(old_grab_day):
	diff = datetime.datetime.today() - old_grab_day
	if (diff.days > 1):
		return True
	if (diff.days == 0 and diff.seconds > 300):
		return True
	return False

class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		asin = item['asin']
		conn = MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
		conn.select_db('ecommerce')
		cursor = conn.cursor()
		conn.set_character_set('utf8')
		cursor.execute('SET NAMES utf8;') 
		sql = "select fetch_time from amazon_item where asin = '%s'" % (asin)
		cnt = cursor.execute(sql)
		if (cnt):
			fetch_time = cursor.fetchone()
			fetch_time = fetch_time[0]
			#if (fetch_time.get)
			if (should_update(fetch_time) ):
				print "\n" + "*" * 50
				print "Delete item: ", asin, "\n"
				cursor.execute("delete from amazon_item where asin = %s" , (asin))
			else:
				cursor.close()
				conn.close()
				raise DropItem("Duplicate item found: %s" % item['asin'])
		cursor.close()
		conn.close()
		return item
		"""
		if item["id"] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids_seen.add(item["id"])
		return item
		"""

class AmazonPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			db = 'ecommerce',
			user = 'root',
			passwd = 'root',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = False
		)

	def process_item(self, item, spider):
		#print "AmazonPipeline should not be processed"
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		return item

	def handle_error(self, *args, **arg_map):
		print "Error occured: ", args
		pass 

	def _conditional_insert(self, tx, p):
		tx.execute("insert into amazon_item" +
		"(asin,     brand,      category,    comments,   description, detailed_comments, details, feature, "
		+ "image_big, image_list, image_small, list_price, sale_price,  sales_rank,        title) values"
		+ "(%s, %s, %s, %s, %s, %s, %s, %s,"
		+ " %s, %s, %s, %s, %s, %s, %s)" ,			
			
		(p['asin'], p['brand'], p['category'], p['comments'], p['description'],p['detailed_comments'], p['details'], p['feature'],
		p['image_big'], p['image_list'], p['image_small'], p['list_price'], p['sale_price'], p['sales_rank'], p['title'] )
		)
