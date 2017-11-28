import urllib.request as urlrequest
from bs4 import BeautifulSoup
from Download import request

top250_url = "https://movie.douban.com/top250?start={}&filter="

with open('F:\\top250_f1.csv', 'w', encoding='utf8') as outputfile:
	outputfile.write("num#title#director#role#init_year#area#genre#rating_num#comment_num#comment#url\n")
	for i in range(0,10):
		start = i * 25
		print(start)
		url_visit = top250_url.format(start)
		print(url_visit)
		crawl_content = urlrequest.urlopen(url_visit).read()
		http_content = crawl_content.decode('utf8')
		soup = BeautifulSoup(http_content, 'html.parser')
		all_item_divs = soup.find_all(class_='item')

		for each_item_div in all_item_divs:
			pic_div = each_item_div.find(class_='pic')
			num = pic_div.find('em').get_text()  # 排名
			href = pic_div.find('a')['href']  # 电影链接
			title = pic_div.find('img')['alt']  # 电影名称
			bd_div = each_item_div.find(class_='bd')
			infos = bd_div.find('p').get_text().strip().split('\n')
			infos_1 = infos[0].split('\xa0\xa0\xa0')
			director = infos_1[0][4:].rstrip('...').rstrip('/').split('/')[0]  # 导演
			role = str(infos_1[1:])[6:].split('/')[0]  # 主演
			infos_2 = infos[1].lstrip().split('\xa0/\xa0')
			year = infos_2[0]  # 上映时间
			area = infos_2[1]  # 国家/地区
			genre = infos_2[2:]  # 电影类型
			star_div = each_item_div.find(class_='star')
			rating_num = star_div.find(class_='rating_num').get_text()  # 评分
			comment_num = star_div.find_all('span')[3].get_text()[:-3]  # 评价数量
			quote = each_item_div.find(class_='quote')
			#inq = ''
		# inq = quote.find(class_='inq').get_text()  #一句话评价
		# print(type(inq))

		outputfile.write('{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#\n'.format(num, title, director, role, year, area,
																	 genre, rating_num, comment_num, href))
		print(num, title, director, role, year, area,genre, rating_num, comment_num, href)
