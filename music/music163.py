# -*- coding:utf-8 -*-

import pandas as pd
import requests
import base64
from Crypto.Cipher import AES
import sys
import importlib
import time

importlib.reload(sys)

url = 'https://music.163.com/#/song?id=31445772'

headers = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	"Connection": "keep-alive",
	"Content-Length": "476",
	"Content-Type": "application/x-www-form-urlencoded",
	"Host": "music.163.com",
	"Referer": "https://music.163.com/",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/57.0"
}

# 设置代理服务器
proxies = {
	'http:': 'http://121.232.146.184',
	'https:': 'https://144.255.48.197'
}

# offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
# first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
second_param = "010001"  # 第二个参数
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"
# 解析整理后的json_list
comment_detail_list = []


# 获取参数
def get_params(page=1):  # page为传入页数
	iv = "0102030405060708"
	first_key = forth_param
	second_key = 16 * 'F'
	if (page == 1):  # 如果为第一页
		first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
		h_encText = AES_encrypt(first_param, first_key, iv)
	else:
		offset = str((page - 1) * 20)
		first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
		h_encText = AES_encrypt(first_param, first_key, iv)
	h_encText = AES_encrypt(h_encText, second_key, iv)
	return h_encText


# 获取 encSecKey
def get_encSecKey():
	encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
	return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
	pad = 16 - len(text) % 16
	text = text + pad * chr(pad)
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	encrypt_text = encryptor.encrypt(text)
	encrypt_text = base64.b64encode(encrypt_text)
	encrypt_text = str(encrypt_text, encoding="utf-8")
	return encrypt_text


# 解析页面
def parse_web(url):
	params = get_params()
	encSecKey = get_encSecKey()
	data = {
		"params": params,
		"encSecKey": encSecKey
	}
	response = requests.post(url, headers=headers, data=data).json()

	comment_total = response['total']
	if comment_total % 20 == 0:
		page_count = comment_total / 20
	else:
		page_count = (comment_total // 20) + 1
	print('评论总数%s,共 %s 页' % (comment_total, page_count))
	print('获取第 1 页评论')
	parse_json_first_page(response)
	for i in range(2, page_count):
		params = get_params(i)
		encSecKey = get_encSecKey()
		data = {
			"params": params,
			"encSecKey": encSecKey
		}
		print('获取第 %s 页评论' % i)
		response = requests.post(url, headers=headers, data=data).json()
		parse_json_else_page(response)


def parse_json_first_page(web_result_json):
	# 热门评论
	hot_comments_list = web_result_json['hotComments']
	# 普通评论
	comments_list = web_result_json['comments']

	# 解析热门评论json
	for i in range(len(hot_comments_list)):
		hot_result_dict = {}
		hot_result_dict['user_name'] = hot_comments_list[i]['user']['nickname']
		hot_result_dict['user_id'] = hot_comments_list[i]['user']['userId']
		hot_result_dict['like_count'] = hot_comments_list[i]['likedCount']
		hot_result_dict['comment_time'] = timestamp_datetime(hot_comments_list[i]['time'])
		hot_result_dict['content'] = hot_comments_list[i]['content']
		comment_detail_list.append(hot_result_dict)
	# 解析普通评论json
	for i in range(len(comments_list)):
		result_dict = {}
		result_dict['user_name'] = comments_list[i]['user']['nickname']
		result_dict['user_id'] = comments_list[i]['user']['userId']
		result_dict['like_count'] = comments_list[i]['likedCount']
		result_dict['comment_time'] = timestamp_datetime(comments_list[i]['time'])
		result_dict['content'] = comments_list[i]['content']
		comment_detail_list.append(result_dict)
	print('获取完毕！')
	parse_pandas(comment_detail_list)
	#return comment_detail_list


def parse_json_else_page(web_result_json):
	# 普通评论
	comments_list = web_result_json['comments']
	# 解析普通评论json
	for i in range(len(comments_list)):
		result_dict = {}
		result_dict['user_name'] = comments_list[i]['user']['nickname']
		result_dict['user_id'] = comments_list[i]['user']['userId']
		result_dict['like_count'] = comments_list[i]['likedCount']
		result_dict['comment_time'] = timestamp_datetime(comments_list[i]['time'])
		result_dict['content'] = comments_list[i]['content'].replace('\n', '')
		comment_detail_list.append(result_dict)
	print('获取完毕！')
	parse_pandas(comment_detail_list)
	#return comment_detail_list


def parse_pandas(comment_list):
	dates = pd.DataFrame(comment_list, columns=['user_name', 'user_id', 'content', 'like_count', 'comment_time'])
	dates.to_csv('F:\\music163_晴天.csv', index=False, mode='a', encoding='utf-8')
	print('存入文件！')


def timestamp_datetime(value):
	format = '%Y-%m-%d %H:%M:%S'
	value = time.localtime(value / 1000)
	## 经过localtime转换后变成time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
	# 最后再经过strftime函数转换为正常日期格式。
	dt = time.strftime(format, value)
	return dt


if __name__ == '__main__':
	start_time = time.time()  # 开始时间
	url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{id}?csrf_token='
	song_id = '186016'
	web_url = url.format(id=song_id)
	result = parse_web(web_url)
	#save_file = parse_pandas(comment_detail_list)
	end_time = time.time()  # 结束时间
	print("程序耗时%s秒." % (end_time - start_time))
