from urllib import *
import socket
import string
from datetime import datetime
import re
from time import time
          #<h3><a onclick="camel_out(this, 'Camel Product', 'US - Top Drop', '0785198849 - Amazon', 3099); return(false);" title="Price history for Secret Wars" href="http://camelcamelcamel.com/Secret-Wars-Marvel-Comics/product/0785198849?active=price_amazon&amp;context=top_drops">Secret Wars</a>
pattern = "\s*<h3><a onclick=\"camel_out\(this, '(.+)', '(.+)', '(.+) - (.+)', (.+)\); return\(false\);\" title=\"(.+)\" href=\"(.+)\">(.+)</a>";
#                                                 source  region asin  amazon/other num          title  url  name    

"""	
	@param  date string like Mar 10, 2015 05:18 AM, or datetime without time
	return hours since 2011.1.1 00:00:00 UTC	
"""
socket.setdefaulttimeout(5)

def get_day_index():
	t = int(time() / (24 * 3600))
	return t

def get_hour(date_string):

	length = len(date_string)
	short_len = len("Mar 10, 2015")
	long_len = len("Mar 10, 2015 05:18 AM")
	beg_date = datetime(2011, 1, 1, 0, 0, 0)
	d = False
	if (length == short_len):
		d = datetime.strptime(date_string, "%b %d, %Y")
	elif (length == long_len):
		d = datetime.strptime(date_string, "%b %d, %Y %H:%M %p")
	if (d):
		diff = d - beg_date
		#print diff.days, diff.seconds
		return diff.days * 24 + diff.seconds / (24 * 3600)		
	return -1

def process_item(fileOrUrl):
	#res = urlopen(item_url)
	try:
		if (fileOrUrl.startswith("http")):
			res = urlopen(fileOrUrl)
		else:
			res = open(fileOrUrl)
	
		detail_start = False
		item = {}
		patObj = re.compile("\s*<a href=\"/browse/([\w_-]+)/([\w_-]+)\">")
		key = False
		price_start = False
		price_key = False
		price_list_start = False
		price_grabed = False
		price_list_key = False
		price_string = []
		for line in res:
			if re.match("\s*<h3 class=\"notopmargin\">Amazon Price History</h3>", line):
				price_start = True
				#print "Got price start"
				continue
			if (price_start and re.match("\s*</table>", line)):
				price_start = False
				continue
			
			if (not price_grabed):
				if re.match("\s*<h3 class=\"notopmargin\">Last 5 price changes</h3>", line):
					price_list_start = True
					price_grabed = True
					continue
			if (price_list_start and re.match("\s*</table>", line)):
				price_list_start = False
				#print "************** price_list_start set to False"
				continue
				
			if (price_list_start):
				if (re.match(".+[AP]M$", line)):
					price_string.append(get_hour(line.strip()))
					#print get_hour(line.strip())
				else:
					obj = re.match(".*\$([\d\.]+)", line)
					if (obj):
						p = int(string.atof(obj.group(1)) * 100)
						price_string.append(p)

			if (price_start and re.match("\s*<td >Current</td>", line)):
				price_key = "price_cur"
				continue
			if (price_key == "price_cur"):
				val = re.match("\s*<td\s*>\$([\d+\.]+)</td>", line)
				if (val):
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = "price_curtime"
				continue
			if (price_key == "price_curtime"):
				val = re.match("\s*<td\s*>(.+)</td>", line)
				if (val):
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = False
				continue
				
			if (price_start and re.match("\s*<td >Highest ", line)):
				price_key = "price_high"
				continue
			if (price_key == "price_high"):
				val = re.match("\s*<td\s*>\$([\d+\.]+)</td>", line)
				if (val):
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = "price_hightime"
				continue
			if (price_key == "price_hightime"):
				val = re.match("\s*<td\s*>(.+)</td>", line)
				if val:
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = False
				continue
				
			if (price_start and re.match("\s*<td >Lowest", line)):
				price_key = "price_low"
				continue
			if (price_key == "price_low"):
				val = re.match("\s*<td\s*>\$([\d+\.]+)</td>", line)
				if (val):
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = "price_lowtime"
				continue
			if (price_key == "price_lowtime"):
				val = re.match("\s*<td\s*>(.+)</td>", line)
				if (val):
					val = val.group(1)
				else:
					continue
				#print "Current price: ", val
				item[price_key] = val
				price_key = False
				continue
				#print line
			#if (not price_start):
			#	key = False
			if (re.match("\s*<table class=\"product_fields\">", line)):
				detail_start = True
				#print "Detail start"
				continue
			if (detail_start):
				if (re.match("\s*</table>", line)):
					detail_start = False
					#print "Detail End"
			if (not detail_start):
				continue
			obj = patObj.match(line)
			if (obj):
				item[obj.group(1)] =  obj.group(2) 
			else:
				line = line.strip()
				if (line[0]!='<'):
					if (not key):
						key = line.lower()
					else:
						item[key] = line
						key = False
		res.close()
		keys = sorted(item.keys())
		item['prices'] = str(price_string)
	except Exception as e:
		print fileOrUrl
		return False
	return item
	
def format_item(item, name, asin, fullName):
	#del item['asin']
	del item['sku']
	item['product_group'] =  item['product group']
	del item['product group']
	item['tracks'] = item['total people tracking']
	del item['total people tracking']
	
	if (item.has_key('list price')):
		del item['list price']
	if (item.has_key('last tracked')):
		del item['last tracked']
	
	if (item.has_key('sales rank') ) :
		item['sales_rank'] = int(item['sales rank'].replace(",", ""))
		del item['sales rank']
	if (item.has_key('last update scan')):
		del item['last update scan']
	if (item.has_key('price_curtime')):
		item['price_curtime'] = get_hour(item['price_curtime'])
	if ('price_hightime' in item):
		item['price_hightime'] = get_hour(item['price_hightime'])
	if ('price_lowtime' in item):
		item['price_lowtime'] = get_hour(item['price_lowtime'])
	item['name'] = name
	item['asin'] = asin
	item['full_name'] = fullName
	if (item.has_key('prices')):
		item['price_list'] = item['prices']
		del item['prices']
	
	if ("artist" in item):
		del item['artist']
	fields = [ "asin" ,  "name" ,  "full_name",  "product_group" ,  "category" ,  "model" ,  "locale" ,  "sales_rank",  "ean" ,  "price_list" ,  "price_cur" ,  "price_low" ,  "price_high",
		"price_lowtime" ,  "price_hightime",  "price_curtime" ,  "tracks",  "upc",  "manufacturer"]
	keys = item.keys()
	for key in keys:
		if (not (key in fields)):
			del item[key]
		
def process_camel(conn, excluded=[]):
	url = "http://camelcamelcamel.com/top_drops"
	startReg = re.compile("\s*<select id=\"field\"")
	#pattern = "\s*<option value=\"([\w-]+)\">(.+)</option>"
	patObj = re.compile(pattern)
	rs = urlopen(url)
	catList = []
	start = False
	for line in rs:    			
		obj = patObj.match(line)
		if (obj):
			catList.append(obj.group(7))
			link = obj.group(7)
			asin = obj.group(3)
			if (asin in excluded):
				print "Already processed"
				continue
			
			#fields = [ "asin" ,  "name" ,  "full_name",  "product_group" ,  "category" ,  "model" ,  "locale" ,  "sales_rank",  "ean" ,  "price_list" ,  "price_cur" ,  "price_low" ,  "price_high",
			#"price_lowtime" ,  "price_hightime",  "price_curtime" ,  "tracks",  "upc",  "manufacturer"]
			#print obj.group(3), obj.group(8)
			#print obj.group(1), obj.group(2).replace("&nbsp;", "").replace("&amp;", ">")
			#full_name = obj.group(2).replace("&nbsp;", "").replace("&amp;", ">")
			link = link[:link.index("?")] 
			print "************Processing " , link
			#print obj.group(8), obj.group(3), obj.group(6)
			full_name = obj.group(8)
			full_name = full_name.replace("&#x27;", "'").replace("&quot;", "\"")
			#if (full_name.startswith("Price history for ")):
			#	full_name = full_name[len("Price history for "):]
			name = re.match("http://camelcamelcamel.com/(.+)/product", link).group(1)
			#name = obj.group(8)
			#if len(name) >= 2:
			#	print name, len(name)
			#print 
			#if (True):
			#	continue
			
			item = {
				'asin': asin,
				'name': name,
				'full_name': full_name,
				'fetch_day': get_day_index()
			}
			
			
			#item = process_item(link)
			#if (not item):
			#	continue
			#sys.exit(-1)
			#source  region asin  amazon/other num          title  url  name    
			#format_item(item, name, asin, full_name)
			#print item.keys()
			insert_or_update(conn, "camel_top_drop", item, {'asin':asin} )
			#break

		#process_item(cat)
		
				#pass
#print "Done"


def build_update_string(tab, item, where):
	keys = sorted(where.keys())
	where_str = ""
	for key in keys:
		where_str += " and `" + str(key) + "` = " + "\"" + str(where[key]) + "\""
	#print where_str
	where_str = where_str[5:]
	update_str = ""
	keys = sorted(item.keys())
	
	for key in keys:
		update_str += ", `" + str(key) + "` = \"" + str(item[key]) + "\""
	update_str = update_str[2:]
	sql = "update " + tab + " set " + update_str  + " where " + where_str
	return sql

def build_select_string(tab, where):
	keys = sorted(where.keys())
	where_str = ""
	for key in keys:
		where_str += " and `" + str(key) + "` = " + "\"" + str(where[key]) + "\""
	where_str = where_str[5:]
	sql = "select * from " + tab + " where " + where_str 
	return sql

def build_insert_string(tab, item):
	keys = sorted(item.keys())
	column_str = ""
	value_str = ""
	for key in keys:
		column_str += ", `" + str(key) + "`"
		value_str += ", \"" + str(item[key]) + "\""
	column_str = column_str[2:]
	value_str = value_str[2:]
	sql = "insert into " + tab + "(" + column_str + ") values(" + value_str + ")"
	return sql

def build_insert_param_string(tab, item):
	keys = sorted(item.keys())
	column_str = ""
	value_str = ""
	for key in keys:
		column_str += ", `" + str(key) + "`"
		value_str += ", %s"
	column_str = column_str[2:]
	value_str = value_str[2:]
	sql = "insert into " + tab + "(" + column_str + ") values(" + value_str + ")"
	return sql
def insert_item(conn, tab, item):
	keys = sorted(item.keys())
	column_str = ""
	value_str = ""
	values = []
	for key in keys:
		column_str += ", `" + str(key) + "`"
		value_str += ", %s"
		values.append(item[key])
	column_str = column_str[2:]
	value_str = value_str[2:]
	sql = "insert into " + tab + "(" + column_str + ") values(" + value_str + ")"
	cursor = conn.cursor()
	cursor.execute(sql, values)
	conn.commit()
	
def insert_or_update(conn, tab, item, where):
	cursor = conn.cursor()
	select_sql = build_select_string(tab, where)
	count=cursor.execute(select_sql)
	sql = ""
	if (count > 0):
		return
		#sql = build_update_string(tab, item, where)
	else:
		insert_item(conn, tab, item)
		#sql = build_insert_string(tab, item)
	#print sql
	#cursor.execute(sql)
#print build_select_string("top", {"name":"zkh", "age": 20})




#update_item(None, "top", {"name":"zkh", "age": 20}, {"id": 11})
