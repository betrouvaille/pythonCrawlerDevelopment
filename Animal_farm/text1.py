import time

import requests
# html = requests.get('https://www.baidu.com').content.decode()
# print(html)

from multiprocessing.dummy import Pool


#
#
# def calc_power(num):
#     return num * num
#
#
# pool = Pool(3)
# origin_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# result = pool.map(calc_power, origin_num)
# print(result)


def query(url):
    requests.get(url)


# start = time.time()
# for i in range(100):
#     query('https://mi.com')
#
# end = time.time()
# print('单线程时间', {end - start})
start = time.time()
url_list = []
for i in range(100):
    url_list.append('https://baidu.com')

pool = Pool(5)
pool.map(query, url_list)
end = time.time()
print('多线程时间', {end - start})
