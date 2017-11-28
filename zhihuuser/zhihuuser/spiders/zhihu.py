# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider, Request
from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
	name = "zhihu"
	allowed_domains = ["www.zhihu.com"]
	# start_urls = ['http://www.zhihu.com/']
	# 入口用户昵称
	start_user = 'excited-vczh'
	# 入口网址
	user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
	# 入口网址参数
	user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
	# 关注的用户网址
	follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&amp;offset={offset}&amp;limit={limit}'
	# 关注的用户网址参数
	follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
	# 分析用户网址
	followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
	# 粉丝用户网址参数
	followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

	def start_requests(self):
		# 拼接入口用户网址，传给用户信息解析
		yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)

	#解析入口用户信息
	def parse_user(self, response):
		# print(response.text)
		result = json.loads(response.text)
		item = UserItem()
		for field in item.fields:
			if field in result.keys():
				item[field] = result.get(field)
		# 返回入口用户信息
		yield item
		# 调用关注的用户函数
		yield Request(self.follows_url.format(user=self.start_user, include=self.follow_query, limit=20, offset=0),
					  self.parse_follows)
		# 调用粉丝用户的函数
		yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
					  self.parse_followers)


	#解析关注的用户信息
	def parse_follows(self, response):
		# print(response.text)
		result = json.loads(response.text)
		if 'data' in result.keys():
			for result in result.get('data'):
				yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
							  self.parse_user)
		if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
			next_page = result.get('paging').get('next')
			yield Request(next_page, self.parse_follows)

	#解析粉丝用户的信息
	def parse_followers(self, response):
		results = json.loads(response.text)

		if 'data' in results.keys():
			for result in results.get('data'):
				yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query),
							  self.parse_user)

		if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
			next_page = results.get('paging').get('next')
			yield Request(next_page,
						  self.parse_followers)
