# -*- coding:utf-8 -*-
import requests
import re
import random
import time
from bs4 import BeautifulSoup


class download():
	def __init__(self):

		self.iplist = []
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
		url = 'http://www.xicidaili.com/nn/'
		html = requests.get(url, headers=headers)
		soup = BeautifulSoup(html.text, 'lxml')
		find_tr = soup.find_all('tr')
		for i in range(1, 100):
			find_td = find_tr[i].find_all('td')
			iplistn = re.findall(r'<td>(.*?)</td>', str(find_td))
			if len(iplistn) != 0:
				ip = '%s:%s' % (iplistn[0], iplistn[1])
				self.iplist.append(ip)
		print(self.iplist)

		self.user_agent_list = [
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]

	def get(self, url, timeout, proxy=None, num_retries=6):  # 给函数一个默认参数proxy为空
		UA = random.choice(self.user_agent_list)  # 从self.user_agent_list中随机取出一个字符串
		headers = {'User-Agent': UA, "referer": "http://www.mzitu.com/all"}  # 构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）

		if proxy == None:  # 当代理为空时，不使用代理获取response
			try:
				# print(requests.get(url, headers=headers, timeout=timeout).status_code)
				return requests.get(url, headers=headers, timeout=timeout)
			except:  # 如过上面的代码执行报错则执行下面的代码

				if num_retries > 0:  # num_retries是限定的重试次数
					time.sleep(10)  # 延迟十秒
					print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
					return self.get(url, timeout, num_retries - 1)  # 调用自身 并将次数减1
				else:
					print(u'开始使用代理')
					time.sleep(10)
					IP = ''.join(str(random.choice(self.iplist)).strip())
					proxy = {'http': IP}
					return self.get(url, timeout, proxy, )  # 代理不为空的时候

		else:  # 当代理不为空
			try:
				IP = ''.join(
					str(random.choice(self.iplist)).strip())  # 将从获取的字符串处理成需要的格式
				proxy = {'http': IP}  # 构造成一个代理
				return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)  # 使用代理获取response
			except:

				if num_retries > 0:
					time.sleep(10)
					IP = ''.join(str(random.choice(self.iplist)).strip())
					proxy = {'http': IP}
					print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
					print(u'当前代理是：', proxy)
					return self.get(url, timeout, proxy, num_retries - 1)
				else:
					print(u'代理失效！取消代理')
					return self.get(url, 3)


request = download()
