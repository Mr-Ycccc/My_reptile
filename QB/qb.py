# -*- coding:utf-8 -*-

import requests
from lxml import etree
#import urllib
#import urllib2
from bs4 import BeautifulSoup

page=1
url='https://www.qiushibaike.com/hot/page/1/'
user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
referer='https://www.qiushibaike.com/'
headers={"User-Agent":user_agent,"referer":referer}

'''
request = urllib2.Request(url,headers=headers)
response=urllib2.urlopen(request)
print response.read().decode("utf-8")
'''

request=requests.get(url,headers=headers)
response=etree.HTML(request.text)
result=BeautifulSoup(request.text,'lxml').find('div',id='content-left').find_all('span')

for i in result:
	print(i.get_text())
print('------------------------------------------------------------------------------')
result2=BeautifulSoup(request.text,'lxml').find_all('div',class_='content')
for j in result2:
	print(j.get_text())

#for i in range(len(result)):
#	result2=result[i].find('span')
#	print(result2.get_text())
	#.find('span').get_text()
#result=BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
	#response.xpath('//div[@class="content"]')
