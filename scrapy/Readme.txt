��Ŀ˵��:
   1. ��Ҫ�õ��Ŀ�Դ���
       scrapy, BeautifulSoup
   2. ���߰�װ��ص�
      ��װ scrapy 
	    sudo apt-get install python-lxml  xml-core python-dev
	    sudo pip install w3lib lxml cssselect Twisted-Core html5lib beautifulsoup4 Twisted	 
		
      selenium ��ص�
	    sudo pip install selenium
		sudo apt-get install xfvb
		 
    3. scrapy ץȡ�Ż�
	   1. д /etc/hosts, ����վ��������ip д��
	   
	4. DB ���� mysql, db �ļ�Ϊ scrapy.sql
		���ݿ�����:
		   db_name: ecommerce
		   db_user: root
		   db_pass:  root
		   db_port:  3306
		   
		   ����λ�� 
		     ccc/pipelines.py
			 amazon/pipelines.py
			 amazon/spider/camel.py
	
	5. �ļ��޸�
	   1. ccc/
	            items.py      (�������ݽṹ)
				setting.py    (����pipelines)
				pipelines.py  (ʵ��pipelines)
		  ccc/spider/
				camel.py       (ʵ�������߼�)

       2  amazon/		  
				items.py      (�������ݽṹ)
				setting.py    (����pipelines)
				pipelines.py  (ʵ��pipelines)
		  ccc/spider/
				products.py    (ʵ�������߼�)
				
	  6. ����
	      1. ���� ccc Ŀ¼, 
			  ���� scrapy crawl  camel ��ץȡ 
		      http://camelcamelcamel.com/top_drops ������
		  2.  ���� amazon Ŀ¼,
		      ���� scrapy crawl  products ��ץȡ 
		      http://www.amazon.com ������
	   
	   
	   
	
	      
   
   