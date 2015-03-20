项目说明:
   1. 主要用到的开源框架
       selenium, BeautifulSoup
   2. 工具安装相关的
      安装 scrapy 
	    sudo apt-get install python-lxml  xml-core python-dev
	    sudo pip install w3lib lxml cssselect Twisted-Core html5lib beautifulsoup4 Twisted	 
		
      selenium 相关的
	    sudo pip install selenium
		sudo apt-get install xfvb	 
    
	   
	3. DB 用了 mysql, db 文件为 crawl.sql
		数据库设置:
		   db_name: ecommerce
		   db_user: root
		   db_pass:  root
		   db_port:  3306
		   
		   如果和实际的不符合, 需要修改
		    ccc/funs_test.py			
			amazon/grab_amazon_items_v2.py
			amazon/grab_amazon_items.py
			amazon/item_v2.py	
	
	4. 文件说明
	       ccc/funs.py  函数定义文件
		   ccc/funs_test.py  main 文件
		   amazon/funs.py 函数定义文件
		   amazon/grab_amazon_items_v2 数据抓取文件
		   
				
	 5. 运行
	      1. 进入 ccc 目录, 
			  运行 python funs_test 来抓取 
		      http://camelcamelcamel.com/top_drops 的数据
		  2.  进入 amazon 目录,
		      运行 python grab_amazon_items_v2 来抓取 
		      http://www.amazon.com 的数据
	   
	   
	   
	
	      
   
   