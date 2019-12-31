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
    # headers = {
    #     'Accept: */*',
    #     'Accept-Encoding: gzip, deflate, br',
    #     'Accept-Language: zh-CN,zh;q=0.9',
    #     'Connection: keep-alive',
    #     'Host: ds.suning.com',
    #     'Referer: https://list.suning.com/0-336522-0.html?safp=d488778a.46601.searchMain.16&safc=cate.0.0',
    #     'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    # }
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
    print(url)
    driver.get(url)
    # 滚动操作
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

    # 输入页码跳转页数
    # 正则匹配出总共多少页
    selector = lxml.html.fromstring(html_code)
    page_have = selector.xpath('//*[@id="bottom_pager"]/div/span[3]')
    page_have2 = selector.xpath('//*[@id="bottomPage"]')
    if len(page_have) == 0:
        # 获取当前页信息
        pass
    elif len(page_have2) == 0:
        # 看有几页，一定是5页以下
        pass
    else:
        page = selector.xpath('//*[@id="bottom_pager"]/div/span[3]/text()')
        print(type(page), page)
        print(len(page))
        if len(page) == 0:
            print('该品类无商品或只有一页')
        else:
            page_num = int(re.findall(r"\d+\.?\d*", str(page))[0])
            driver.get(url)
            for page_n in range(2, page_num):
                # 滚动操作
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
                time.sleep(5)
                html_code = get_suning_html(url)
                print(html_code)
                # 找到页码输入框，输入页码，从2开始
                input_f = driver.find_element_by_id('bottomPage')
                time.sleep(5)
                # 找到确定按钮，点击确定
                submit = driver.find_element_by_xpath('//*[@id="bottom_pager"]/div/a[7]')
                input_f.clear()
                input_f.send_keys(page_n)
                print('点击')
                submit.click()
                time.sleep(10)
            driver.close()
    # return html_code_list


def get_suning_detail(url):
    """
    开始获取数据，商品标题，参数，等
    :return:
    """
    html_code = get_suning_detail_code(url)
    selector = lxml.html.fromstring(html_code)
    goods_id = selector.xpath('//*[@id="product-list"]/ul/li/@id')
    for id in goods_id:
        # 商品id
        goods_id = id
        # 商品标题
        goods_title = selector.xpath('//*[@id="{}"]/div/div/div[2]/div[2]/a/text()'.format(id))[0]
        # 商品卖点
        goods_selling_point = selector.xpath('//*[@id="{}"]/div/div/div[2]/div[2]/a/em/text()'.format(id))[0]
        # 商品特征2
        feature = selector.xpath('//*[@id="{}"]/div/div/div[2]/div[3]/em/text()'.format(id))
        goods_feature = "+".join(feature)
        # 评价条数
        evaluation_num = selector.xpath('//*[@id="{}"]/div/div/div[2]/div[4]/div/a/i/text()'.format(id))[0]

    return goods_id, goods_title, goods_selling_point, goods_feature, evaluation_num


if __name__ == '__main__':
    url_list = get_suning_url(start_url)
    pool = Pool(1)
    pool.map(get_suning_detail_code, url_list)
