import urllib2
import random


def getHtml(url, proxies):
	random_proxy = random.choice(proxies)
	proxy_support = urllib2.ProxyHandler({"http": random_proxy})
	opener = urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
	html = urllib2.urlopen(url)
	return html


url = "http://www.csdn.net/"
proxies = ["101.53.101.172:9999", "171.117.93.229:8118", "119.251.60.37:21387", "58.246.194.70:8080"
																				"115.173.218.224:9797",
		   "110.77.0.70:80"]

for i in range(0, 10000):
	try:
		html = getHtml(url, proxies)
		print(html.info())  # 打印网页的头部信息，只是为了展示访问到了网页，可以自己修改成想显示的内容
		print(i)
	except:
		print("出现故障")
