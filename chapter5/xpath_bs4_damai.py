import requests
from bs4 import BeautifulSoup
import lxml.html

"""

2019年12月4日 周三

气死我了，原网址失效了，我又在大麦网上找了个网址，但是没想到啊。

没想到啊 舟哥说 python request只能获取静态页面，获取不了动态页面。

他让我去找崔哥，崔哥说建议我用我用chrome啥啥啥。。。

行8！！！！我今天就只处理静态的，动态的等我再学学再弄！！！！！！

"""


target = 'https://search.damai.cn/search.htm'

damai_html = requests.get(target).content.decode()
print(damai_html)


# Beautiful Soup 4 版的解法
print("这是用Beautiful Soup 4的解法")
soup = BeautifulSoup(damai_html, 'lxml')

info_1 = soup.find(class_='location-header')
data = info_1.find_all('span')
for each in data:
    print(each.string)


# 用xpath试试
print("这是用xpath的解法")
selector = lxml.html.fromstring(damai_html)
item_list = selector.xpath('//div[@class="location-header"]')[0]
info = item_list.xpath('string(.)')
print(info)
