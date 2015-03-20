# -*- coding: UTF-8 -*- 

from time import time
import sys

from funs import *



		
begin_time = time()


display = Display(visible=0, size=(800, 600))
display.start()


reload(sys)
sys.setdefaultencoding('utf-8')





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
	for asin in asins:
		sql = "select fetch_time from amazon_item_detail where asin = '%s'" % (asin)
		cnt = cursor.execute(sql)
		if (cnt):
			fetch_time = cursor.fetchone()
			print fetch_time
			continue
			
		item = get_item_by_selenium(asin[0])	
		print item
		insert_item(conn, "amazon_item_detail", item)
	cursor.close()
	conn.close()
	
#except Exception as e:
#	print e
#	exit()	


display.stop()

"""
for key in item:
	try:
		print key, item[key]
	except:
		print "Value error for: ", key
"""


passed = time() - begin_time
print "Program running time: ", passed, " seconds"






	
	
