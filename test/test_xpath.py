from lxml import etree
import requests


url='http://cuiqingcai.com/2621.html'

html=requests.get(url)
response=etree.HTML(html.text)
result=response.xpath("/html/body/section/div[3]/div/article/p[25]/text()")
result_1=response.xpath("/html/body/table/tr[627]/td[2]")
result2=response.xpath("/html/body/section/div[3]/div/article/p[13]/text()")

print(result)
print(result_1)
