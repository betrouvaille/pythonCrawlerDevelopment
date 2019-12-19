import time

import requests
import lxml.html
from selenium import webdriver
from multiprocessing import Pool

start_url = 'https://list.suning.com/?safp=d488778a.homepage1.99345513004.1#20089'


def get_suning_html(url):
    """
    获取网页源代码
    :param url: 获取源代码目标url
    :return: 网页源代码
    """
    html = requests.get(url)
    return html.content.decode()


def get_suning_url(url):
    """
    从分类页面中提取各类别的url
    :return:各类别url列表
    """
    html_code = get_suning_html(url)
    selector = lxml.html.fromstring(html_code)
    url_list = []
    for i in range(1, 12):
        phone_url = selector.xpath('//*[@id="20089"]/div[{}]/div[2]/a/@href'.format(i))
        url_list = phone_url + url_list
    return url_list


def get_suning_detail_code(url):
    """
    获取类别详情页面源代码
    :return:详情页面源代码list
    """
    driver = webdriver.Chrome(r'E:\chromedriver_win32\chromedriver.exe')
    url_list = get_suning_url(start_url)
    html_code_list = []
    for url in url_list:
        url = 'http:' + url
        print(url)
        driver.get(url)
        driver.execute_script("window.scrollTo(0,10000)")  # 翻到浏览器底部等待加载完成
        time.sleep(2)
        html_code = get_suning_html(url)
        html_code_list.append(html_code)
    return html_code_list


def get_suning_detail(html_code):
    """
    开始获取数据，商品标题，价格，参数，等
    :return:
    """
    html_code = get_suning_detail_code()
    selector = lxml.html.fromstring(html_code)
    goods_id = selector.xpath('//*[@id="product-list"]/ul/li/@id')
    print(goods_id)
    time.sleep(1)


if __name__ == '__main__':
    html_code_list = get_suning_detail_code()
    pool = Pool(4)
    pool.map(get_suning_detail, html_code_list)
