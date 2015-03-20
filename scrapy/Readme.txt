项目说明:
   1. 主要用到的开源框架
       scrapy, BeautifulSoup
   2. 工具安装相关的
      安装 scrapy 
	    sudo apt-get install python-lxml  xml-core python-dev
	    sudo pip install w3lib lxml cssselect Twisted-Core html5lib beautifulsoup4 Twisted	 
		
      selenium 相关的
	    sudo pip install selenium
		sudo apt-get install xfvb
		 
    3. scrapy 抓取优化
	   1. 写 /etc/hosts, 将网站服务器的ip 写入
	   
	4. DB 用了 mysql, db 文件为 scrapy.sql
		数据库设置:
		   db_name: ecommerce
		   db_user: root
		   db_pass:  root
		   db_port:  3306
		   
		   配置位置 
		     ccc/pipelines.py
			 amazon/pipelines.py
			 amazon/spider/camel.py
	
	5. 文件修改
	   1. ccc/
	            items.py      (定义数据结构)
				setting.py    (设置pipelines)
				pipelines.py  (实现pipelines)
		  ccc/spider/
				camel.py       (实现爬虫逻辑)

       2  amazon/		  
				items.py      (定义数据结构)
				setting.py    (设置pipelines)
				pipelines.py  (实现pipelines)
		  ccc/spider/
				products.py    (实现爬虫逻辑)
				
	  6. 运行
	      1. 进入 ccc 目录, 
			  运行 scrapy crawl  camel 来抓取 
		      http://camelcamelcamel.com/top_drops 的数据
		  2.  进入 amazon 目录,
		      运行 scrapy crawl  products 来抓取 
		      http://www.amazon.com 的数据
	   
	   
	   
	
	      
   
   