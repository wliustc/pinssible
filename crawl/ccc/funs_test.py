from funs import *
import MySQLdb
import sys
try:
	conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306)
	conn.select_db('ecommerce')	
	cursor = conn.cursor()
	
	sql = "select asin from camel_top_drop";
	cnt = cursor.execute(sql)
	print cnt
	results = cursor.fetchall()
	excluded = []
	for asin in results:
		excluded.append(asin[0])
	
	process_camel(conn, excluded)

	#conn.commit()
	cursor.close()
	conn.close()
	
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	
