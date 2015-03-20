# -*- coding: UTF-8 -*- 

from time import time
import sys

from funs import *
		
begin_time = time()

reload(sys)
sys.setdefaultencoding('utf-8')

#try:
if (True):

	asin = "B0002913F0"
	asin = "B00DB9JV5W"	
	asin = sys.argv[1]
	conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
	conn.select_db('ecommerce')
	
	cursor = conn.cursor()
	conn.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;') 
	
	
	url = get_amazon_itemurl(asin)
	contents = get_contents_by_urllib(url)	
	item = get_item_detail(contents)	
	print item
	#insert_item(conn, "amazon_item_detail", item)
	cursor.close()
	conn.close()


passed = time() - begin_time
print "Program running time: ", passed, " seconds"






	
	
