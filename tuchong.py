# -*- conding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import os
import logging
import importlib
import sys
import io
#importlib.reload(sys)
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

'''
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelno)s %(levelname)s %(pathname)s %(filename)s %(funcName)s %(lineno)d %(thread)d %(threadName)s %(process)d %(message)s',
                datefmt='%a,%Y %b %d %H:%M:%S',
                filename='F:\\tuchong\\log.log',
                filemode='w')
'''


class tuchong():
	# url = 'https://stock.tuchong.com/search?source=tc_pc_home_search&term={term}'
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
	url = 'https://tuchong.com/rest/2/sites/{user_id}/posts?count=20&page={page}&before_timestamp=0'
	#url='https://seanarcher.tuchong.com/rest/2/sites/{user_id}/posts?count=20&page={page}&before_timestamp=1511168487'

	def get_web(self, user_id, page):
		self.page = page
		self.user_id = user_id
		web_url = self.url.format(user_id=self.user_id, page=self.page)
		web_result = requests.get(web_url, headers=self.headers).json()
		if web_result['more'] == True:
			print('存在下一页')
			self.page = int(self.page) + 1
			self.parse_web(web_result)
			self.get_web(self.user_id, self.page)
		else:
			print('不存在下一页')

	def parse_web(self,web_result):
		post_list = web_result['post_list']
		parse_all_img_list = []
		for i in range(0, len(post_list)):
			parse_all_img_dict = {}
			parse_all_img_dict['user'] = post_list[i]['author_id']
			parse_all_img_dict['user_name'] = post_list[i]['excerpt']#'私房人像'
			parse_all_img_dict['title'] = post_list[i]['title']
			parse_all_img_dict['img_count'] = post_list[i]['image_count']
			img_list = post_list[i]['images']
			parse_img_list = []
			for j in range(len(img_list)):
				parse_img_dict = {}
				parse_img_dict['img_id'] = img_list[j]['img_id']
				parse_img_dict['img_href'] = img_list[j]['source']['l']
				parse_img_list.append(parse_img_dict)
			parse_all_img_dict['img_list'] = parse_img_list
			parse_all_img_list.append(parse_all_img_dict)

		self.img_save(parse_all_img_list)

	def img_save(self, parse_all_img_list):
		if len(parse_all_img_list[0]['user_name']) == 0:
			author='Null'
		else:
			author = parse_all_img_list[0]['user_name']
		self.mkdir(author)
		for i in range(len(parse_all_img_list)):
			self.mkdir(author + '\\' + parse_all_img_list[i]['title'])
			# print(parse_all_img_list[i])
			for j in range(len(parse_all_img_list[i]['img_list'])):
				img_name = (parse_all_img_list[i]['title'] + str(parse_all_img_list[i]['img_list'][j]['img_id'])).replace('?','')
				img = requests.get(parse_all_img_list[i]['img_list'][j]['img_href'])
				with open(img_name + '.jpg', 'ab') as f:
					f.write(img.content)


	def mkdir(self, path):
		path = path.strip().replace('。', '').replace('?', '').replace("\n", "").replace("\r", "").replace("业务400", "").replace(' ', '')
		isExists = os.path.exists(os.path.join("F:\\tuchong", path))
		if not isExists:
			print('新建摄影师文件夹：', path)
			os.makedirs(os.path.join("F:\\tuchong\\", path))
			os.chdir(os.path.join("F:\\tuchong\\", path))
			print('切换文件夹:', path)
			return True
		else:
			print('摄影师文件夹', path, '已存在')
			os.chdir(os.path.join("F:\\tuchong\\", path))
			print('切换文件夹:', path)
			return False


result = tuchong().get_web(1066859, 1)
# print(result)
