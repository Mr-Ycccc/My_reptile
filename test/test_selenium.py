from selenium import webdriver
import time

browser=webdriver.Chrome()
browser.get("https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F")

user_name=browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys("18694069389")
user_passwd=browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys("Wake@123")
#browser.find_element_by_id("TANGRAM__PSP_3__verifyCode").send_keys(input())
time.sleep(20)
user_submit=browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
time.sleep(10)
browser.get_screenshot_as_file("F:\\error.jpg")
result_cookies=browser.get_cookies()
print(user_name)
print(user_passwd)
print(user_submit)
print(result_cookies)
#browser.quit()