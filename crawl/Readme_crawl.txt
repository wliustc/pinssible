��Ŀ˵��:
   1. ��Ҫ�õ��Ŀ�Դ���
       selenium, BeautifulSoup
   2. ���߰�װ��ص�
      ��װ scrapy 
	    sudo apt-get install python-lxml  xml-core python-dev
	    sudo pip install w3lib lxml cssselect Twisted-Core html5lib beautifulsoup4 Twisted	 
		
      selenium ��ص�
	    sudo pip install selenium
		sudo apt-get install xfvb	 
    
	   
	3. DB ���� mysql, db �ļ�Ϊ crawl.sql
		���ݿ�����:
		   db_name: ecommerce
		   db_user: root
		   db_pass:  root
		   db_port:  3306
		   
		   �����ʵ�ʵĲ�����, ��Ҫ�޸�
		    ccc/funs_test.py			
			amazon/grab_amazon_items_v2.py
			amazon/grab_amazon_items.py
			amazon/item_v2.py	
	
	4. �ļ�˵��
	       ccc/funs.py  ���������ļ�
		   ccc/funs_test.py  main �ļ�
		   amazon/funs.py ���������ļ�
		   amazon/grab_amazon_items_v2 ����ץȡ�ļ�
		   
				
	 5. ����
	      1. ���� ccc Ŀ¼, 
			  ���� python funs_test ��ץȡ 
		      http://camelcamelcamel.com/top_drops ������
		  2.  ���� amazon Ŀ¼,
		      ���� python grab_amazon_items_v2 ��ץȡ 
		      http://www.amazon.com ������
	   
	   
	   
	
	      
   
   