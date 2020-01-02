import requests
import json
import re

from selenium import webdriver

driver = webdriver.Chrome('/Users/lfl/Downloads/chromedriver')

driver.get('http://exercise.kingname.info/exercise_advanced_ajax.html')

import time

time.sleep(8)

print(driver.page_source)

#
# url_exercise1_get = 'http://exercise.kingname.info/ajax_1_backend'
#
# print(requests.get(url_exercise1_get).content.decode())
#
# url_exercise1_post = 'http://exercise.kingname.info/ajax_1_postbackend'
#
# print(requests.post(url_exercise1_post, json={'name': "kingname", 'age': 24}).content.decode())
#
# url_exercise2 = 'http://exercise.kingname.info/exercise_ajax_2.html'
#
# html2 = requests.get(url_exercise2).content.decode()
# code_json = re.search("secret = '(.*?)'", html2, re.S).group(1)
# print(json.loads(code_json))


