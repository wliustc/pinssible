from urllib import *
import socket
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains


from pyvirtualdisplay import Display
from bs4 import BeautifulSoup

import MySQLdb
import time
import re
          #<h3><a onclick="camel_out(this, 'Camel Product', 'US - Top Drop', '0785198849 - Amazon', 3099); return(false);" title="Price history for Secret Wars" href="http://camelcamelcamel.com/Secret-Wars-Marvel-Comics/product/0785198849?active=price_amazon&amp;context=top_drops">Secret Wars</a>
pattern = "\s*<h3><a onclick=\"camel_out\(this, '(.+)', '(.+)', '(.+) - (.+)', (.+)\); return\(false\);\" title=\"(.+)\" href=\"(.+)\">(.+)</a>";
#                                                 source  region asin  amazon/other num          title  url  name    

"""	
	@param  date string like Mar 10, 2015 05:18 AM, or datetime without time
	return hours since 2011.1.1 00:00:00 UTC	
"""
socket.setdefaulttimeout(5)



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

def get_day_index():
        t = int(time.time() / (24 * 3600))
        return t

def get_item_text_by_soup(soup, item_id):
	item = soup.find(id = item_id)
	if (item):
		return item.text.strip()
	return ""

def to_float(str):
	try :
		str = str.replace(",", "")
		return float(str);
	except:
		print "To float failed: ", str
		return 0
		
def get_price(price_str):
	if (price_str.startswith("$")):
		price_str = price_str[1:]
	return to_float(price_str)

def get_item_detail(contents):
	soup = BeautifulSoup(contents)

	deal_price = get_item_text_by_soup(soup, "priceblock_dealprice")
	if (not deal_price):
		deal_price = get_item_text_by_soup(soup, "priceblock_ourprice")
		if (not deal_price):
			deal_price = get_item_text_by_soup(soup, "actualPriceValue")
		if (not deal_price):
			deal_price = get_item_text_by_soup(soup, "priceblock_saleprice")
	deal_price = get_price(deal_price)
	brand  = get_item_text_by_soup(soup, "brand")
	if (not brand):
		brand = get_item_text_by_soup(soup, "amsPopoverTrigger")
	if (not brand):
		brand_ele = soup.select("#product-title_feature_div > div > span > a")
		if (len(brand_ele) > 0) :
			brand =  brand_ele[0] . get_text()
		#print "Brand element: ", brand_ele
	productTitle = get_item_text_by_soup(soup, "productTitle")
	if (not productTitle):
		productTitle = get_item_text_by_soup(soup, "btAsinTitle")


	#views = get_item_text_by_soup(soup, "acrCustomerReviewText")
	features = get_item_text_by_soup(soup, "feature-bullets")
	more_details = get_item_text_by_soup(soup, "detailBullets_feature_div")
	if (not more_details):
		#more_details = get_item_text_by_soup(soup, "detail-bullets")
		eles = soup.select("#detail-bullets ul li")
		details_array = []
		for ele in eles:
			ele_str = str(ele)
			if (ele_str.find("<script") > 0):
				start_pos = ele_str.find("<script")
				end_pos = ele_str.find("</script>")
				#print start_pos, end_pos
				ele_str = ele_str[:start_pos] + ele_str[end_pos + len('</script>') : ] 
				obj = BeautifulSoup(ele_str)
				ele_str = obj.get_text() # re.replace("\s+", " ", obj.get_text())
			else:
				ele_str = ele.get_text()
			ele_str = re.sub("\s+", " ", ele_str)
			details_array.append(ele_str.strip())
		more_details = "\n" . join(details_array)		
	

	comment_div = soup.find(id = 'revMHRL')
				      #revMHRL
	detailed_comments = []
	if (comment_div) : 
		for selection in comment_div.find_all(class_ = "a-section"):
	#for selection in comment_div.find_all(has_class_but_no_id):
			if (selection.has_attr('id')):
				continue
			detailed_comments.append(selection.get_text().strip())

	product_description_ele = soup.find(class_ = "productDescriptionWrapper")
	if (product_description_ele):
		product_description = product_description_ele.text.strip()
	else:
		product_description = get_item_text_by_soup(soup, "productDescription")

	list_price = 0
	price_span = soup.find(class_ = "a-text-strike")
	if (price_span):
			list_price = price_span.text.strip()	
			#list_price = to_float(list_price[1:])
	else:
		list_price = get_item_text_by_soup(soup, "listPriceValue")
		#if (list_price.startswith("$")):
		#	list_price = to_float(list_price[1:])
	list_price = get_price(list_price)
	rank = "0"
	rank_span = soup.find(class_ = "zg_hrsr_rank")  #zg_hrsr_rank
	if (rank_span):
		rank = rank_span.text.strip()
	if (rank.startswith("#")):
		rank = rank[1:]
	rank = int(rank)

	image_element = soup.find(id = 'landingImage')
	image_small = ""
	image_big = ""
	image_list = ""
	if (image_element):
		image_small = image_element['src']          
		#print image_element.get_attr("data-old-hires") 
		image_big = image_element.attrs['data-old-hires'] 
		image_list = image_element.attrs['data-a-dynamic-image']
		

	comments_array = []
	comments = soup.find(class_ = "quotes-column")
	if (comments):
		max_comments = 3
		for comment in comments:
			comments_array.append(comment.text)
	cat = ""
	rank_cat_ele = soup.find(class_ = "zg_hrsr_ladder")
	if (rank_cat_ele):
		rank_cat = rank_cat_ele.text
	cat = get_item_text_by_soup(soup, "wayfinding-breadcrumbs_feature_div")
	if (not cat):
		crumb_ele = soup.find(class_ = "detailBreadcrumb")
		if (crumb_ele):
			cat = crumb_ele.text
	cat = re.sub("\s+", " ", cat).strip()
	#print cat
	#exit()
	item = {
			#'asin': asin,
			'title': productTitle,
			'category'   : cat,
			'brand'      : brand,
			'feature'    : features,
			'description': product_description,
			'details'    : more_details,		
			'sale_price' : deal_price,
			'list_price' : list_price,
			'sales_rank' : rank,
			'comments'	 : str(comments_array),

			'detailed_comments' : str(comments_array),
			'image_small' : image_small,
			'image_big'   : image_big,
			'image_list'  : image_list
	}
	return item

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
			
			item = process_item(link)
			if (not item):
				continue
			#sys.exit(-1)
			#source  region asin  amazon/other num          title  url  name    
			format_item(item, name, asin, full_name)
			#print item.keys()
			insert_or_update(conn, "camel_top_drop", item, {'asin':asin} )
			#break

		#process_item(cat)
		
				#pass
#print "Done"

def getItemText(element, id):
	try:
		item = element.find_element_by_id(id)
		return item.text
	except:
		return ""
def get_items_by_class(driver, cls):
        try:
                return driver.find_elements_by_class_name(cls)
        except:
                return False

def get_item_by_class(driver, cls):
	try:
		return driver.find_element_by_class_name(cls)
	except:
		return False

def get_contents_by_urllib(url):
	try:
		lines = []
		res = urlopen(url)
		for line in res:
			lines.append(line)
		res.close()
		return "\n".join(lines)
	except:
		print "ERROR Occured get_contents_by_urllib: ", url
		return ""

def get_contents_by_selenium():
	try:
		driver = webdriver.Firefox()
		driver.get(url)
		contents = driver.page_source
		driver.close()
		return contents
	except:
		print "ERROR Occured get_contents_by_selenium: ", url
		return ""

def get_amazon_itemurl(asin):
	return "http://www.amazon.com/dp/%s/?psc=1" % (asin)

def get_item_by_selenium(asin):
	url = get_amazon_itemurl(asin)  
	driver = webdriver.Firefox()
	driver.get(url)
	deal_price = getItemText(driver, "priceblock_dealprice")
	if (not deal_price):
		deal_price = getItemText(driver, "priceblock_ourprice")
		if (not deal_price):
			deal_price = getItemText(driver, "actualPriceValue")
		if (not deal_price):
			deal_price = getItemText(driver, "priceblock_saleprice")
	deal_price = to_float(deal_price[1:])

	brand  = getItemText(driver, "brand")
	if (not brand):
		brand = getItemText(driver, "amsPopoverTrigger")
	brand_sec = soup.select("#product-title_feature_div > div > span")
	print brand_sec
	#brand = brand_element.text
	productTitle = getItemText(driver, "productTitle")
	if (not productTitle):
		productTitle = getItemText(driver, "btAsinTitle")
	#star_ele = driver.find_element_by_id("acrPopover")
	views = getItemText(driver, "acrCustomerReviewText")
	features = getItemText(driver, "feature-bullets")
	more_details = getItemText(driver, "detailBullets_feature_div")
	product_description = getItemText(driver, "productDescription")
	if (not product_description):
		product_description_ele = get_item_by_class(driver, "productDescriptionWrapper")
		if (product_description_ele):
			product_description = product_description_ele.text
	list_price = 0
	price_span = get_item_by_class(driver, "a-text-strike")
	if (price_span):
		list_price = price_span.text	
		list_price = to_float(list_price[1:])
	else:
		list_price = getItemText(driver, "listPriceValue")
		if (list_price.startswith("$")):
			list_price = to_float(list_price[1:])
	rank = "0"
	rank_span = get_item_by_class(driver, "zg_hrsr_rank")  #zg_hrsr_rank
	if (rank_span):
		rank = rank_span.text
	if (rank.startswith("#")):
		rank = rank[1:]
	rank = int(rank)
	
	comments_array = []
	comments = get_items_by_class(driver, "quotes-column")
	if (comments):
		max_comments = 3
		for comment in comments:
			comments_array.append(comment.text)
	cat = ""
	rank_cat_ele = get_item_by_class(driver, "zg_hrsr_ladder")
	if (rank_cat_ele):
		rank_cat = rank_cat_ele.text
	cat = getItemText(driver, "wayfinding-breadcrumbs_feature_div")
	
	"""
	comments = driver.find_elements_by_class_name("a-section")
	max_comments = 2
	for comment in comments:
		try:
			print comment.text
		except:
			continue
		max_comments = max_comments-1
		if (max_comments <= 0):
			break
	"""
	cat = cat.replace("\n", "").replace("\t", "")
	driver.close()
	return {
		'asin': asin,
		'title': productTitle,
		'category'   : cat,
		'brand'      : brand,
		'feature'    : features,
		'description': product_description,
		'details'    : more_details,		
		'sale_price' : deal_price,
		'list_price' : list_price,
		'sales_rank' : rank,
		'comments'	 : str(comments_array)		
	}
	"""
		'title' 	 : "",
		'shipping'   : "",
		'star'       : "",
		'views'      : "",		
		'weight'	 :,
		'length'     :,
		'width'		 :,
		'height'	 :,
	"""
	
	"""
	print "Deal price: ", deal_price	
	print "Brand: ", brand.text
	brand_url = brand.get_attribute("href")
	print "Brand URL: ", brand_url	
	print "Title: ", productTitle	
	print "Star: ", star_ele.get_attribute("title")
	print "Views: ", views
	print "Features: ", features
	print "More details:  ", more_details
	print "Product description: ", product_description	
	print "List price: ", price_span.text
	"""
	#pass

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
		values.append(conn.escape_string(str(item[key])))
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
