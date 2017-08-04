# -*- coding: utf-8 -*-
from threading import Thread
from Queue import Queue
import time
from bs4 import BeautifulSoup
from YarnMonitor import yarn_apps_running
import sys
from urllib import urlencode
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf8')


# 解析页面内容
def parse_web(arguments):
	id_name = {}
	for a in range(len(yarn_list_result_in)):
		id = yarn_list_result_in[a][0]
		name = yarn_list_result_in[a][1]
		id_name[id] = name
	substr = arguments[1]
	url = arguments[0]
	resp = urllib2.urlopen(url)
	content = resp.read()
	bs = BeautifulSoup(content, 'html5lib')
	table = bs.find_all('table')

	# 获取active，complet，failed
	h4_active = bs.find_all(id="active")
	h4_completed = bs.find_all(id="completed")
	h4_failed = bs.find_all(id="failed")
	failed_dict = {}
	failed_count = 0
	active_dict = {}
	active_count = 0
	# 获取active总数
	for i in h4_active:
		active_count = re.search('[\d]+', i.string).group()
	print(active_count, 'active_count')
	# 判断active是否有数据
	if active_count == '0':
		print(url, 'active not exist!')
	else:
		active = table[2]
		active_th = active.find_all('th')
		active_td = active.find_all('td')
		print(url, 'active exist!')
		for i in range(len(active_th)):
			for active_string in active_th[i].stripped_strings:
				for active_string2 in active_td[i].stripped_strings:
					active_dict[active_string] = active_string2
		active_dict.pop('(')
		active_dict.pop(')')
		active_dict.pop('?')
	# 判断是否有failed
	if len(h4_failed) == 0:
		pass
		print(url, 'failed not exist!')
	# 如果存在则统计failed数据
	else:
		failed = table[-1]
		failed_th = failed.find_all('th')
		failed_td = failed.find_all('td')
		# 获取failed总数
		for i in h4_failed:
			failed_count = re.search('[\d]+', i.string).group()
		# 获取failed数据
		print(url, 'failed exist!')
		for i in range(len(failed_th)):
			for failed_string in failed_th[i].stripped_strings:
				for failed_string2 in failed_td[i].stripped_strings:
					failed_dict[failed_string] = failed_string2
		failed_dict.pop('(')
		failed_dict.pop(')')
		failed_dict.pop('?')
	return (id_name[substr], active_dict, active_count, failed_dict, failed_count)


# 这个是工作进程，负责不断从队列取数据并处理
def working():
	while True:
		arguments = q.get()
		# parse_web(arguments)
		result = parse_web(arguments)
		# print(arguments,':',result)
		result_list.append(result)
		time.sleep(1)
		q.task_done()


# 发送短信
def sendMessage(phoneNumber, jobMessage):
	# get message
	data = {}
	data['phoneNumber'] = phoneNumber
	data['content'] = "DEV-测试【夸客金融】%s" % str(jobMessage)
	data['deptType'] = "001"
	data['besType'] = "001"
	data['besId'] = "001"

	# get url
	# url = "http://qf-coreuat-01:8128/sms-frontal/MessageController/sendMsg"
	url = "http://172.16.4.55:8080/sms-frontal/MessageController/sendMsg"

	postData = urlencode(data).encode('utf-8')
	req = urllib2.Request(url=url, data=postData)
	response = urllib2.urlopen(req)
	return response.read()


# 处理failed数据
def failed_message(tuple_list, active_run_count):
	failed_list = {}
	active_list = {}
	for i in range(len(tuple_list)):
		# 判断active是否有错误数据
		if len(tuple_list[i][1]) == 0:
			# print('active error not exist!')
			active_name = tuple_list[i][0]
			active_content = tuple_list[i][1]
			active_list[active_name] = active_content
		else:
			# print('active exist!')
			active_name = tuple_list[i][0]
			active_content = tuple_list[i][1]
			# 取active总数，判断是否超过50
			active_runcount = int(tuple_list[i][2])
			if active_runcount >= active_run_count:
				active_content['active_count'] = tuple_list[i][2]
				active_list[active_name] = active_content
			else:
				active_list[active_name] = {}
		# 判断是否有failed数据
		if len(tuple_list[i][3]) == 0:
			# print('failed error not exist!')
			failed_name = tuple_list[i][0]
			failed_content = tuple_list[i][3]
			failed_list[failed_name] = failed_content
		# pass
		else:
			# print('failed exist!')
			failed_name = tuple_list[i][0]
			failed_content = tuple_list[i][3]
			failed_content['failed_count'] = tuple_list[i][4]
			failed_list[failed_name] = failed_content
	return (active_list, failed_list)


# 判断监控的job是否在yarn运行
def yarn_list_parse(yarn_list, monitorlist):
	monitor_yarn_list = []
	not_monitor_yarn_list = []
	monitor_yarn_list_name = []
	# 判断在yarn上正在运行的监控job
	for i in range(len(yarn_list)):
		for j in monitorlist:
			if j == yarn_list[i][1]:
				monitor_yarn_list.append(yarn_list[i])
	# 判断没在yarn上运行的监控job
	for i in range(len(monitor_yarn_list)):
		monitor_yarn_list_name.append(monitor_yarn_list[i][1])
	for k in monitorlist:
		if k not in monitor_yarn_list_name:
			not_monitor_yarn_list.append(k)
	return (monitor_yarn_list, not_monitor_yarn_list)


# 整合错误信息
def error_message_parse(yarn_list_result_not_in, yarn_list_result_in):
	error_message_list = []
	# 返回是否在yarn运行的信息
	if len(yarn_list_result_not_in) == 0:
		print('需要监控的job都在Yarn运行！')
	else:
		error_message = '%s：【ERROR】没有在Yarn运行！\n' % ','.join(map(str, yarn_list_result_not_in))
		error_message_list.append(error_message)
	# 返回active和failed错误信息
	if len(yarn_list_result_in) != 0:
		running_result = failed_message(result_list, active_run_count)
		for k in set(running_result[0].keys() + running_result[1].keys()):
			active_message = None
			error_message = None
			# active message
			if len(running_result[0][k]) == 0:
				active_message = None
			else:
				active_message = "%s：【Active信息】积压过量，数量为%s；" % (k, running_result[0][k]['active_count'])
			# failed message
			if len(running_result[1][k]) == 0:
				error_message = None
			else:
				error_message = "【Failed信息】数据处理失败共计%s个，最近一次批次Job ID为%s,提交时间为%s。\n" % (
					running_result[1][k]['failed_count'], running_result[1][k]['Batch Time'],
					running_result[1][k]['Processing Time'])

			# active and failed message
			if active_message is None and error_message is not None:
				error_message_list.append(k + "：" + error_message)
			if active_message is not None and error_message is not None:
				error_message_list.append(active_message + error_message)
			if active_message is not None and error_message is None:
				error_message_list.append(active_message + "\n")

	return error_message_list


if __name__ == "__main__":
	# q是任务队列,NUM是并发线程总数,JOBS是有多少任务
	q = Queue(maxsize=0)
	NUM = 6
	JOBS = q.qsize()

	# 解析页面后返回的数据
	result_list = []
	# url_list保存拼接后的网址
	url_list = list()
	# 获取服务器上运行的job
	address = "hadoop4"
	port = 8088
	state_list = ["RUNNING"]
	yarn_list = yarn_apps_running(address, port, state_list)
	# job运行数量
	active_run_count = 10
	# 需要监控的job
	monitor_list = ['ssc_kafka_pdl_main_rule_test.py','ssc_kafka_dac_in_call.py', 'ssc_kafka_jyd_in_loan.py', 'ssc_kafka_log.py']
	# 程序开始执行时间：
	start_time = time.time()
	# yarn_list_result_in为在yarn运行的监控job，yarn_list_result_not_in为没在yarn运行的监控job
	yarn_list_result = yarn_list_parse(yarn_list, monitor_list)
	yarn_list_result_in = yarn_list_result[0]
	yarn_list_result_not_in = yarn_list_result[1]
	# 拼接url
	url = 'http://%s:%s/proxy/' % (address, str(port))
	for i in range(len(yarn_list_result_in)):
		url_list.append([url + yarn_list_result_in[i][0] + "/streaming/",yarn_list_result_in[i][0]])

	# 把拼接好的url加入队列
	for s in url_list:
		q.put(s)
	# fork NUM个线程等待队列
	for i in range(NUM):
		t = Thread(target=working)
		t.setDaemon(True)
		t.start()
	# 把JOBS排入队列
	for i in range(JOBS):
		q.put(i)
	# 等待所有JOBS完成
	q.join()
	# 返回整合后的error信息
	error_message_list_result = error_message_parse(yarn_list_result_not_in, yarn_list_result_in)
	error_msg = "".join(error_message_list_result)
	# 发送短信
	phoneNumberList = []
	if len(error_msg) == 0:
		print('监控job运行正常！')
	else:
		print(error_msg)
		'''
		for phoneNumber in phoneNumberList:
			send_result = sendMessage(phoneNumber, error_msg)
		print(send_result)
		'''
	# 程序结束时间
	end_time = time.time()

	print("It wastes %.4f seconds!" % float(end_time - start_time))
