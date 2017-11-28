# -*- coding: utf-8 -*-
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihuuserPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
	collection_name='zhihu_vczh'

	def __init__(self,mongo_url,mongo_db):
		self.mongo_url=mongo_url
		self.mongo_db=mongo_db

	@classmethod
	def from_crawler(cls,crawler):
		return cls(
			mongo_url=crawler.settings.get('MONGO_URL'),
			mongo_db=crawler.settings.get('MONGO_DATABASE')
		)

	def open_spider(self,spider):
		self.client=pymongo.MongoClient(self.mongo_url)
		self.db=self.client[self.mongo_db]

	def close_spider(self,spider):
		self.client.close()

	def process_item(self,item,spider):
		self.db[self.collection_name].update({'url_token':item['url_token']},{'$set':dict(item)},True)
		return item