import importlib
import sys

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request

from dingdian.items import DingdianItem

importlib.reload(sys)


class Myspider(scrapy.Spider):
	name = 'dingdian'
	allowed_domains = ['23us.so']
	bash_url = 'http://www.23us.so/list/'
	bashurl = '.html'

	def start_requests(self):
		for i in range(1, 10):
			url = self.bash_url + str(i) + '_1' + self.bashurl
			yield Request(url, self.parse)

	def parse(self, response):
		# print(response.text)
		max_num = BeautifulSoup(response.text, 'lxml').find('div', class_="pagelink").find_all('a')[-1].get_text()
		bashurl = str(response.url)[:-7]
		for num in range(1, int(max_num) + 1):
			url = bashurl + '_' + str(num) + self.bashurl
			yield Request(url, callback=self.get_name)

	def get_name(self, respense):
		tds = BeautifulSoup(respense.text, 'lxml').find_all('tr', bgcolor="#FFFFFF")
		for td in tds:
			novelname = td.find('a').get_text()
			novelurl = td.find('a')['href']
			yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl})

	def get_chapterurl(self, response):
		item = DingdianItem()
		item['name'] = str(response.meta['name']).replace('\xa0', '')
		item['novelurl'] = response.meta['url']
		# category=BeautifulSoup(response.text,'lxml').find('table').find('a').get_text()
		td_list = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')
		item['category'] = str(td_list[0].get_text()).replace('\xa0', '')
		item['author'] = str(td_list[1].get_text()).replace('\xa0', '')
		item['serialstatus'] = str(td_list[2].get_text()).replace('\xa0', '')
		item['serialnumber'] = str(td_list[4].get_text()).replace('\xa0', '')
		item['name_id'] = str(response.url)[-10:-5].replace('/', '')
		return item
