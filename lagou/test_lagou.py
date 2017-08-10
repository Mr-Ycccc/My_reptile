import requests
import os
import pymysql
pymysql.install_as_MySQLdb()
# http请求头信息
headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Connection': 'keep-alive',
	'Content-Length': '25',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie': 'user_trace_token=20170214020222-9151732d-f216-11e6-acb5-525400f775ce; LGUID=20170214020222-91517b06-f216-11e6-acb5-525400f775ce; JSESSIONID=ABAAABAAAGFABEF53B117A40684BFB6190FCDFF136B2AE8; _putrc=ECA3D429446342E9; login=true; unick=yz; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1494688520,1494690499,1496044502,1496048593; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1496061497; _gid=GA1.2.2090691601.1496061497; _gat=1; _ga=GA1.2.1759377285.1487008943; LGSID=20170529203716-8c254049-446b-11e7-947e-5254005c3644; LGRID=20170529203828-b6fc4c8e-446b-11e7-ba7f-525400f775ce; SEARCH_ID=13c3482b5ddc4bb7bfda721bbe6d71c7; index_location_city=%E6%9D%AD%E5%B7%9E',
	'Host': 'www.lagou.com',
	'Origin': 'https://www.lagou.com',
	'Referer': 'https://www.lagou.com/jobs/list_Python?',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'X-Anit-Forge-Code': '0',
	'X-Anit-Forge-Token': 'None',
	'X-Requested-With': 'XMLHttpRequest'
}


def get_json(url, page, lang_name,city):

	data = {'first': 'true', 'pn': page, 'kd': lang_name, 'city':city}
	# post请求
	json = requests.post(url, data, headers=headers).json()
	list_con = json['content']['positionResult']['result']
	info_list = []
	for i in list_con:
		# info = []
		post = ({
			'company': i['companyFullName'],
			'address':str(i['businessZones']),
			'salary': i['salary'],
			'city': i['city'],
			'post': i['positionName'],
			'education': i['education'],
			'work_year': i['workYear'],
			'company_situation': "".join(str(i['industryField']) + '/' + str(i['financeStage'])),
			'remarks': str(i['positionAdvantage']),
			'post_label':str(i['positionLables']),
			'create_time': i['createTime']
		}
		)
		# info.append(i['salary'])
		# info.append(i['city'])
		# info.append(i['education'])
		info_list.append(post)
	return info_list


def main(positionName,city):
	page = 1
	url = 'http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
	info_result = []
	while page < 2:
		info = get_json(url, page, positionName,city)
		info_result = info_result + info
		page += 1
	# 打开数据库连接
	db = pymysql.connect(host='rm-uf6n9e38nsb631qh8o.mysql.rds.aliyuncs.com', user='root', passwd='1q2w#E$R', db='LagouData',port=3306,charset='utf8')
	# 使用cursor()方法获取操作游标
	cursor = db.cursor()
	i=0
	for row in info_result:
		sql = '''
			INSERT INTO LagouData.source_data(post,salary,city,education,work_year,post_label,company,address,company_situation,remarks,create_time)
		         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		    '''

		try:
			#print(row['post'],row['salary'],row['city'],row['education'],row['work_year'],row['post_label'],row['company'],row['address'],row['company_situation'],row['remarks'],row['create_time'])
			# 执行sql语句
			i=i+1
			print(i,row)
			print(i,sql,(row['post'],row['salary'],row['city'],row['education'],row['work_year'],row['post_label'],row['company'],row['address'],row['company_situation'],row['remarks'],row['create_time']))
			cursor.execute(sql,(row['post'],row['salary'],row['city'],row['education'],row['work_year'],row['post_label'],row['company'],row['address'],row['company_situation'],row['remarks'],row['create_time']))
			# 提交到数据库执行
			db.commit()
			print('commit')
		except:
			# 如果发生错误则回滚
			db.rollback()
			print('error')

	db.commit()
	#关闭游标
	cursor.close()
	# 关闭数据库连接
	db.close()

	'''
	# 写入lagou.txt文件中
	os.chdir("F:\\")
	with open('lagou.txt', 'w') as f:
		for row in info_result:
			f.write(str(row) + '\n')
	'''

if __name__ == '__main__':
	# 修改lang_name更换语言类型
	lang_name = 'python'
	# 修改city更换城市
	city='武汉'
	main(lang_name,city)
