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
		db=client['Mistar']
		self.mistart_collection=db['mistar']
		self.title=''
		self.url_start=''
		self.img_urls=[]
		self.max_num=''

	def all_url(self,url):
		for i in range(1,168):
			self.url_start=url+'/d/'+str(i)
			self.img_urls.append(self.url_start)

		for j in self.img_urls:
			self.img_url(j)

	def img_url(self,imgurl):
		html=requests.get(imgurl)
		html_title=BeautifulSoup(html.text, 'lxml')
		#img_url=BeautifulSoup(html.text, 'lxml').find_all('img')
		self.title=html_title.title.get_text()
		path = str(self.title).replace('?', '_')
		# 调用mkdir函数创建文件夹！这儿path代表的是标题title
		self.mkdir(path)
		os.chdir("F:\MISTAR\\" + path)
		print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '开始保存:', self.title, '路径:', 'F:\MISTAR\\', path)
		html_img=etree.HTML(html.text)
		result=html_img.xpath('//img/@src')
		self.max_num=result[-1][-8:-4]
		print(self.max_num)
		for j in result:
			self.save(j)


	def save(self, img_url):
			name = img_url[-8:-4]
			name=str(name).replace('/', '_')
			page=img_url[-8:-4]
			print(page)
			if page==self.max_num:
				print('max')
				img = requests.get(img_url)
				f = open(name + '.jpg', 'ab')
				f.write(img.content)
				f.close()
				post = {
					'标题': self.title,
					'主题页面': self.url_start,
					'图片地址': self.img_urls,
					'获取时间': datetime.datetime.now()
				}
				# 把信息存入mongodb
				self.mistart_collection.save(post)
				# print(post)
				print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), post['标题'], '已存入monggodb')
				print(post)
			else:
				print('save')
				img = requests.get(img_url)
				f = open(name + '.jpg', 'ab')
				f.write(img.content)
				f.close()

	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(os.path.join("F:\MISTAR", path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹！')
			os.makedirs(os.path.join("F:\MISTAR", path))
			os.chdir(os.path.join("F:\MISTAR", path))  ##切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			os.chdir(os.path.join("F:\MISTAR", path))  ##切换到目录
			return False

MISTAR=Mistar().all_url('http://www.mistar8.com')