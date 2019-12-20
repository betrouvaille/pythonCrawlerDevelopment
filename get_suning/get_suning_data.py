import re
import time
import pymysql
import requests
import lxml.html
from selenium import webdriver
from multiprocessing import Pool

# 开始url为全部商品分类链接
start_url = 'https://list.suning.com/?safp=d488778a.homepage1.99345513004.1#20089'


def db_conn():
    """
    连接数据库，查询操作
    :return:
    """
    db = pymysql.connect(host='127.0.0.1', user='root', password='0816', port=3306)
    cursor = db.cursor()


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
    url = 'http:' + url
    driver.get(url)
    html_code = get_suning_html(url)

    # 输入页码跳转页数
    # 正则匹配出总共多少页
    selector = lxml.html.fromstring(html_code)
    page = str(selector.xpath('//*[@id="bottom_pager"]/div/span[3]/text()'))
    page_num = int(re.findall(r"\d+\.?\d*", page)[0])
    html_code_list = []
    for page_n in range(1, page_num + 1):
        if page_n == 1:
            # 翻到浏览器底部等待加载完成
            driver.execute_script(""" 
                        (function () { 
                            var y = document.body.scrollTop; 
                            var step = 100; 
                            window.scroll(0, y); 
                            function f() { 
                                if (y < document.body.scrollHeight) { 
                                    y += step; 
                                    window.scroll(0, y); 
                                    setTimeout(f, 50); 
                                }
                                else { 
                                    window.scroll(0, y); 
                                    document.title += "scroll-done"; 
                                } 
                            } 
                            setTimeout(f, 1000); 
                        })(); 
                        """)
            time.sleep(1)
            html_code = get_suning_html(url)
            html_code_list.append(html_code)
        else:
            # 找到页码输入框，输入页码，从2开始
            input_f = driver.find_element_by_id('bottomPage')
            input_f.send_keys(page_n)
            # 找到确定按钮，点击确定
            submit = driver.find_element_by_class_name('page-more ensure')
            submit.click()
            html_code = get_suning_html(url)
            html_code_list.append(html_code)
    driver.close()
    return html_code_list


def get_suning_detail(url):
    """
    开始获取数据，商品标题，参数，等
    :return:
    """
    html_code = get_suning_detail_code(url)
    selector = lxml.html.fromstring(html_code)
    goods_id = selector.xpath('//*[@id="product-list"]/ul/li/@id')
    print(goods_id)
    time.sleep(1)


if __name__ == '__main__':
    url_list = get_suning_url(start_url)
    pool = Pool(4)
    pool.map(get_suning_detail_code, url_list)
