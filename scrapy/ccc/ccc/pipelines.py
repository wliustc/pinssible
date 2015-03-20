#from scrapy import log
#from scrapy.core.exceptions import DropItem

#from scrapy.http import Request
from scrapy.exceptions import DropItem
#from scrapy.contrib.pipeline.images import ImagesPipeline
#import time

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import json

class JsonWriterPipeline(object):
	def __init__(self):
		self.file = open("items.jl",  "wb")
	
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		self.file.write(line)
		return item
		
class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()
	def process_item(self, item, spider):
		if item["id"] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids_seen.add(item["id"])
		return item


class CccPipeline(object):

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
        
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        
        query.addErrback(self.handle_error)
        return item
    def handle_error(self, *args, **arg_map):
	print "Error occured: ", args
	pass 
    def _conditional_insert(self, tx, item):
        tx.execute("insert into camel_item(asin, is_best, list_price, sale_price,fetch_day) values(%s, %s, %s, %s, %s)" +
		" on duplicate key update is_best = %s, list_price = %s, sale_price = %s, fetch_day = %s",
		(item['asin'], item['is_best'], item['list_price'], item['sale_price'], item['fetch_day'],
		item['is_best'], item['list_price'], item['sale_price'], item['fetch_day'] )
	)
	#print item
	"""
	idx = 1
        for item in items:
            print idx, item
            idx = idx + 1
		
        """
	"""
		if item.get('name'):
            tx.execute(\
                "insert into book (name, publisher, publish_date, price ) \
                 values (%s, %s, %s, %s)",
                (item['name'],  item['publisher'], item['publish_date'], 
                item['price'])
            )
        """
