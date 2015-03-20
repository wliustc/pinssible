# -*- coding: utf-8 -*-

# Scrapy settings for ccc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ccc'

SPIDER_MODULES = ['ccc.spiders']
NEWSPIDER_MODULE = 'ccc.spiders'
#ITEM_PIPELINES = ['ccc.pipelines.CccPipeline']

ITEM_PIPELINES = {
	'ccc.pipelines.CccPipeline': 300,
#	'ccc.pipelines.JsonWriterPipeline': 300,
#	'ccc.pipelines.JsonWriterPipeline': 800,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ccc (+http://www.yourdomain.com)'
