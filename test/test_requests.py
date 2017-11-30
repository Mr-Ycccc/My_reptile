import requests
r = requests.get('https://github.com/timeline.json')
print(r.text)
#print(r.encoding)
print(r.content)
print(r.status_code)
print(r.raise_for_status())


import requests
headers = {

    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
response =requests.get("https://www.zhihu.com",headers=headers)

print(response.status_code)
#print(response.headers)
#print(response.cookies)
#print(response.text)
print(requests.codes)