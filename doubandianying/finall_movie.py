import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame

url = 'https://movie.douban.com/top250?start={}&filter='
result_list = []

for i in range(11):
    start = i * 25
    url_list = url.format(start)
    web_parse = requests.get(url_list)
    soup = BeautifulSoup(web_parse.text, 'html5lib')
    web_all_div = soup.find_all(class_="item")
    for i in web_all_div:
        result_dict = {}
        # 排名
        result_dict['ranking'] = i.find('em').get_text()
        # 标题
        result_dict['title'] = i.find('img')['alt']
        # 链接
        result_dict['href'] = i.find('a')['href']
        # 简评
        try:
            result_dict['comment'] = i.find(class_="inq").get_text()
        except:
            result_dict['comment'] = ''
        # 评分
        result_dict['score'] = i.find(class_="rating_num").get_text()
        # 评论数量
        result_dict['comment_num'] = i.find(class_="star").find_all("span")[3].get_text()[:-3]
        result_list.append(result_dict)
#print(result_list)

data_frame = DataFrame(result_list, columns=['title', 'ranking', 'comment', 'score', 'comment_num', 'href'])
#print(data_frame)
data_frame.to_csv('F:\\movie_introduce.csv',encoding='utf-8',index=False)

href_split = data_frame['href'].str.split('/').apply(pd.Series)
#print(href_split)
movie_num = list(href_split[4])
#print(movie_num[100])


douban_api = 'http://api.douban.com/v2/movie/subject/'
details_list = []
api_url_list = []
for i in range(200,250):
    api_url = douban_api + str(movie_num[i])
    api_url_list.append(api_url)
for i in api_url_list:
    details_dict = {}
    print(i)
    api_result = requests.get(i)
    api_result_json = api_result.json()
    # print(api_result.status_code)
    try:
        details_dict['movie_title'] = api_result_json['title']
        details_dict['movie_year'] = api_result_json['year']
        details_dict['movie_director'] = api_result_json['directors'][0]['name']
        details_dict['movie_role'] = api_result_json['casts'][0]['name'] + '/' + api_result_json['casts'][1][
            'name'] + '/' + api_result_json['casts'][2]['name']
        details_dict['movie_area'] = '/'.join(api_result_json['countries'])
        details_dict['movie_genres'] = '/'.join(api_result_json['genres'])
    except Exception as error:
        print(error)
    print(details_dict)
    details_list.append(details_dict)
detail_frame = DataFrame(details_list,
                         columns=['movie_title', 'movie_year', 'movie_director', 'movie_role', 'movie_area',
                                  'movie_genres'])
detail_frame.to_csv('F:\\movie_detail3.csv',encoding='utf-8',index=False)