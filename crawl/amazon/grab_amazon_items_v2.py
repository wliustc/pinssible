# -*- coding: UTF-8 -*- 

import time
import sys

from funs import *
		
begin_time = time.time()

reload(sys)
sys.setdefaultencoding('utf-8')

#print "Will sleep 10 seconds"
#time.sleep(10)
#exit()
#try:
if (True):

	#asin = "B009CMNE6E"
	
	conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
	conn.select_db('ecommerce')
	
	cursor = conn.cursor()
	conn.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;') 
	
	sql = "select asin from camel_top_drop"
	cnt = cursor.execute(sql)
	if (cnt <= 0):
		print "No top drop found "
		exit()
	
	asins = cursor.fetchall()
	failed_asin_array = []
	for asin_row in asins:
		asin = asin_row[0]
		sql = "select fetch_time from amazon_item_detail where asin = '%s'" % (asin)
		cnt = cursor.execute(sql)
		if (cnt):
			fetch_time = cursor.fetchone()
			print fetch_time
			continue
		url = get_amazon_itemurl(asin)
		tries = 0
		contents = False
		while (tries < 5):
			contents = get_contents_by_urllib(url)
			if (contents):
				break
			print "Not grabed, sleep 2 seconds"
			time.sleep(2)
			tries += 1
		if (not contents):
			failed_asin_array.append(asin)
			continue
		item = get_item_detail(contents)
		if (not item['list_price']):
			print contents
			continue
		item['asin'] = asin
		print item
		insert_item(conn, "amazon_item_detail", item)
	print "\n" + "=" * 50
	print "Tried failed asin"
	for asin in failed_asin_array:
		url = get_amazon_itemurl(asin)
		contents = get_contents_by_urllib(url)
		if (not contents):
			print "Grab failed in last resort: " + asin
			continue

		item = get_item_detail(contents)	
		item['asin'] = asin
		print item
		insert_item(conn, "amazon_item_detail", item)

	cursor.close()	
	conn.close()


passed = time.time() - begin_time
print "Program running time: ", passed, " seconds"






	
	
