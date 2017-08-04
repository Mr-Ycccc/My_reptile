# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
import  datetime
import multiprocessing

class mzitu():

	def __init__(self):
		#连接mongodb
		client=MongoClient()
		db=client['meinvxiezhenji']
		self.meizitu_collection=db['meizitu']
		self.title=''
		self.url=''
		self.img_urls=[]

	def all_url(self, url):
		##调用request函数把套图地址传进去会返回给我们一个response
		html = request.get(url,3)
		all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
		for a in all_a:
			title= a.get_text()
			self.title=title
			# 有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
			path = str(title).replace('?', '_')
			# 调用mkdir函数创建文件夹！这儿path代表的是标题title
			self.mkdir(path)
			os.chdir("D:\mzitu\\"+path)
			print('开始保存:', title,'路径:','D:\mzitu\\',path)
			href = a['href']
			#把页面地址保存到self.url
			self.url=href
			##调用html函数把href参数传递过去！href是套图的地址
			print('href:', href)
			if self.meizitu_collection.find_one({'主题页面': href}):
				print(href,'页面已经爬取')
			else:
				self.html(href)


	##这个函数是处理套图地址获得图片的页面地址
	def html(self, href):
		html = request.get(href,3)
		#计数器，判断是否下载完毕
		page_num=0
		max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
		for page in range(1, int(max_span) + 1):
			page_num=page_num+1
			page_url = href + '/' + str(page)
			#调用img函数
			print('page_url:', page_url)
			self.img(page_url,max_span,page_num)


	##这个函数处理图片页面地址获得图片的实际地址
	def img(self, page_url,max_span,page_num):
		img_html = request.get(page_url,3)
		img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
		#每次循环都把图片地址存到list
		self.img_urls.append(img_url)
		#当max_span和Page_num相等时，就是最后一张图片了，最后一次下载图片并保存到数据库中。
		print('imge_url:', img_url)
		if int(max_span)==page_num:
			self.save(img_url)
			#构造字典，存入mongodb
			post={
				'标题':self.title,
				'主题页面':self.url,
				'图片地址':self.img_urls,
				'获取时间':datetime.datetime.now()
			}
			#把信息存入mongodb
			self.meizitu_collection.save(post)
			print(post,'已存入monggodb')
		else:
			self.save(img_url)



	##这个函数保存图片
	def save(self, img_url):
		name = img_url[-9:-4]
		img = request.get(img_url,3)
		f = open(name + '.jpg', 'ab')
		f.write(img.content)
		f.close()


	##这个函数创建文件夹
	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(os.path.join("D:\mzitu", path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹！')
			os.makedirs(os.path.join("D:\mzitu", path))
			os.chdir(os.path.join("D:\mzitu", path))  ##切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			os.chdir(os.path.join("D:\mzitu", path))  ##切换到目录
			return False

Mzitu = mzitu()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
