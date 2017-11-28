import urllib
import urllib.request as urlrequest
import json
import time
import random
import pandas as pd

df = pd.read_csv("F:\\top250_f1.csv",sep = "#", encoding = 'utf8')
urlsplit = df.url.str.split('/').apply(pd.Series)
id_list = list(urlsplit[4])
num=0
IP_list = ['42.55.170.182:80','110.216.60.162:80','118.114.77.47:8080']  #这里写几个可用的IP地址和端口号，只抓250个页面，有两三个IP就够了。
IP = random.choice(IP_list)

with open('F:\\top250_f2.csv', 'w',encoding='utf8') as outputfile:

    outputfile.write("num#rank#alt_title#title#pubdate#language#writer#director#cast#movie_duration#year#movie_type#tags#image\n")

    proxy = urlrequest.ProxyHandler({'https':  'IP'})
    print(proxy)
    opener = urlrequest.build_opener(proxy)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4)AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
    urlrequest.install_opener(opener)

    for id in id_list:
        url_visit = 'https://api.douban.com/v2/movie/subject/{}'.format(id)
        crawl_content = urlrequest.urlopen(url_visit).read()
        json_content = json.loads(crawl_content.decode('utf-8'))

        rank = json_content['rating']['average']
        alt_title = json_content['alt_title']
        image = json_content['image']
        title = json_content['title']
        pubdate = json_content['attrs']['pubdate']
        language = json_content['attrs']['language']
        try:
            writer = json_content['attrs']['writer']
        except:
            writer = 'None'
        director = json_content['attrs']['director']
        cast = json_content['attrs']['cast']
        movie_duration = json_content['attrs']['movie_duration']
        year = json_content['attrs']['year']
        movie_type = json_content['attrs']['movie_type']
        tags = json_content['tags']
        num = num +1
        outputfile.write("{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}\n".format(num,rank,alt_title,title,pubdate,language,writer,
                                                                              director,cast,movie_duration,year,movie_type,tags,image))
        time.sleep(1)