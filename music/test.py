import requests
from bs4 import BeautifulSoup
from lxml import etree

url='http://music.163.com/#/song?id=478731270'

result=requests.get(url)
response=etree.HTML(result.text)
response2=response.xpath("//*[@id='auto-id-vPpTEdCDbtazgMpT']/div[1]/span/span")
print(result.text)

'''
url='http://www.cnblogs.com/giserliu/p/4399778.html'

html=requests.get(url)
response=etree.HTML(html.text)
result=response.xpath("//*[@id='cnblogs_post_body']/div[4]/p[8]/span/text()")
result=response.xpath("//*[@id='cnblogs_post_body']/div[4]/p[8]/span/text()")
result2=response.xpath('/html/head/link[5]/@type')

print(result)
print(result2)
'''
