import time
import requests
from multiprocessing.dummy import Pool
import lxml.html


# # html = requests.get('https://www.baidu.com').content.decode()
# # print(html)


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
# start = time.time()
# for i in range(100):
#     query('https://mi.com')
#
# end = time.time()
# print('单线程时间', {end - start})


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


def get_suning():
    """
    苏宁价格json
    :return:
    """
    url = 'https://ds.suning.com/ds/generalForTile/' \
          '000000011346304317____R1901001_000060021-010-2-0000000000-1--ds0000000003792.jsonp?callback=ds0000000003792'
    url2 = 'https://ds.suning.com/ds/generalForTile/' \
           '000000010989586988____R1901001_000060864,' \
           '000000010606649859____R1901001_000060021,' \
           '000000010973073407____R1901001_000060864,' \
           '000000011356354998____R1901001_000066138,' \
           '000000010657713259____R1901001_000060864,' \
           '000000011344612553____R1901001_000060DER,' \
           '000000011382632596____R1901001_000060021,' \
           '000000010657749544____R1901001_000060864,' \
           '000000011239124433____R1901001_00006J675,' \
           '000000010627906708____R1901001_000060864-010-2-0000000000-1--ds0000000006859.jsonp?callback=ds0000000006859'
    url_json = requests.get(url).content.decode()
    print(type(url_json))


from selenium import webdriver


def get_suning_code():
    """
    用selenium模拟浏览器获取内容
    :return:
    """
    driver = webdriver.Chrome(r'E:\chromedriver_win32\chromedriver.exe')
    driver.get('https://list.suning.com/0-20006-0.html?safp=d488778a.46601.searchMain.2&safc=cate.0.0')
    # js = "var q=document.documentElement.scrollTop=100000"
    # driver.execute_script("window.scrollTo(0,600000000)")
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

    time.sleep(1000)


def xpath_test():
    url = 'https://list.suning.com/0-506574-0.html?safp=d488778a.46601.searchMain.92&safc=cate.0.0'
    html = requests.get(url).content.decode()
    selector = lxml.html.fromstring(html)
    test = selector.xpath('//*[@id="0070941117-11507557649"]/div/div/div[9]')
    print(test)


if __name__ == '__main__':
    xpath_test()
