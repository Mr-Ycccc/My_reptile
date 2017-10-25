#-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
import datetime
from lxml import etree
import logging

class Xiuren():



	def __init__(self):
		#连接mongodb
		client=MongoClient()
		db=client['Xiuren']
		UA='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
		referer='http://www.xiuren8.com/'
		self.headers = {'User-Agent': UA, "referer": referer}
		self.mistart_collection=db['xiuren']
		self.title=''
		self.url_list=[]
		self.img_urls=[]
		self.max_num=''

	def all_url(self,url):
		'''
		logging.basicConfig(filename='/root/spider_logs/xiuren.log', level=print)
		isExists = os.path.exists(os.path.join("/root/spider_logs/xiuren.log"))
		if not isExists:
			print(u'建了日志文件xiuren.log！')
			return True
		else:
			print(u'日志文件已经存在了！')
		'''
		for i in range(1,1000):
			self.url_start=url+'thread-'+str(i)
			self.url_list.append(self.url_start)

		for j in self.url_list:
			if self.mistart_collection.find_one({'主题页面': j}):
				print(j,'页面已经爬取')
			else:
				self.img_url(j)

	def img_url(self,http_url):
		html=requests.get(http_url)
		html_img=etree.HTML(html.text)
		self.img_urls=html_img.xpath('//img/@src')
		title =html_img.xpath('//h3/text()')
		if len(self.img_urls)==0 or len(title)==0:
			print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "no photo!!!")
		else:
			self.title = title[0].strip()
			path = str(self.title).replace('?', '_').replace(' ', '_')
			self.mkdir(path)
			os.chdir("/root/Xiuren/" + path)
			for i in self.img_urls:
				if 'view/img/logo.png' in self.img_urls:
					self.img_urls.remove('view/img/logo.png')
				if 'view/img/avatar.png' in self.img_urls:
					self.img_urls.remove('view/img/avatar.png')
			self.max_num = self.img_urls[-1][-7:-4]
			print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '开始保存:', self.title, '--', http_url, '--数量:', self.max_num, '--路径:', '/root/Xiuren/', path)
			for j in self.img_urls[2:]:
				self.save_mongo(j,http_url)

	def save_mongo(self,img_url,web):
		name = img_url[-7:-4]
		name = str(name).replace('/', '_')
		if name == self.max_num:
			print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'max', name)
			self.save(img_url,name)
			post = {
				'标题': self.title,
				'主题页面': web,
				'图片地址': self.img_urls,
				'获取时间': datetime.datetime.now()
			}
			# 把信息存入mongodb
			self.mistart_collection.save(post)
			# print(post)
			print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), post['标题'], '已存入monggodb')
		else:
			#print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'save', name)
			self.save(img_url,name)


	def save(self, img_url,name):
		img = requests.get(img_url)
		f = open(name + '.jpg', 'ab')
		f.write(img.content)
		f.close()


	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(os.path.join("/root/Xiuren/", path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹！')
			os.makedirs(os.path.join("/root/Xiuren/", path))
			os.chdir(os.path.join("/root/Xiuren/", path))  ##切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			os.chdir(os.path.join("/root/Xiuren/", path))  ##切换到目录
			return False

Xiuren=Xiuren().all_url('http://www.xiuren8.com/')
