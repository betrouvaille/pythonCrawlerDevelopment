import time

import requests
# # html = requests.get('https://www.baidu.com').content.decode()
# # print(html)

from multiprocessing.dummy import Pool


def query(url):
    """
    获取网页源代码
    :param url:
    :return:
    """
    requests.get(url)


def ca_time():
    """
    计算获取100次网页代码多线程时间
    :return:
    """
    start = time.time()
    url_list = []
    for i in range(100):
        url_list.append('https://baidu.com')
    pool = Pool(5)
    pool.map(query, url_list)
    end = time.time()
    print('多线程时间', {end - start})


# #
# #
# # def calc_power(num):
# #     return num * num
# #
# #
# # pool = Pool(3)
# # origin_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# # result = pool.map(calc_power, origin_num)
# # print(result)


# # start = time.time()
# # for i in range(100):
# #     query('https://mi.com')
# #
# # end = time.time()
# # print('单线程时间', {end - start})


def yanghuisanjia():
    """
    杨辉三角
    :return:
    """
    l = []
    for n in range(30):
        r = [1]
        l.append(r)
        if n == 0:
            print(r)
            continue
        for m in range(1, n):
            r.append(l[n - 1][m - 1] + l[n - 1][m])
        r.append(1)
        print(r)


if __name__ == '__main':
    pass
