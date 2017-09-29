#-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
import datetime
from lxml import etree

class Mistar():

	def __init__(self):
		#连接mongodb
		client=MongoClient()
		db=client['Ugirls']
		UA='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
		referer='http://www.mistar8.com'
		self.headers = {'User-Agent': UA, "referer": referer}
		self.mistart_collection=db['ugirls']
		self.title=''
		self.url_list=[]
		self.img_urls=[]
		self.max_num=''

	def all_url(self,url):
		for i in range(42,1243):
			self.url_start=url+'/d/'+str(i)
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
		title =html_img.xpath('/html/head/title/text()')
		self.title= title[0].strip()
		self.title=self.title[:-10]
		path = str(self.title).replace('?', '_').replace(' ','_')
		self.mkdir(path)
		os.chdir("F:\girls\\" + path)
		if len(self.img_urls)==0:
			print("no photo!!!")
		else:
			self.max_num=self.img_urls[-1][-7:-4]
			print(self.max_num)
			print('开始保存:',self.title,'--数量:',self.max_num,'--路径:', 'F:\girls\\', path)
			for j in self.img_urls:
				self.save_mongo(j,http_url)

	def save_mongo(self,img_url,web):
		name = img_url[-7:-4]
		name = str(name).replace('/', '_')
		if name == self.max_num:
			#print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'max', name)
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
		isExists = os.path.exists(os.path.join("F:\girls", path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹！')
			os.makedirs(os.path.join("F:\girls", path))
			os.chdir(os.path.join("F:\girls", path))  ##切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			os.chdir(os.path.join("F:\girls", path))  ##切换到目录
			return False

MISTAR=Mistar().all_url('http://www.ugirls8.com')