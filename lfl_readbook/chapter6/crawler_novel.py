import redis
import requests
import lxml.html
from pymongo import MongoClient



# 链接MongoDB 装爬好的文章
client = MongoClient()

db_name = 'Chapter6'
col_name = 'baiyexing'
database = client[db_name]
handler = database[col_name]


# 目标网站
url_target = 'http://dongyeguiwu.zuopinj.com/5525/'
html = requests.get(url_target).content.decode()

selector = lxml.html.fromstring(html)

# 目标网站里的目标链接们
all_chapters_url = selector.xpath('//div[@class="book_list"]/ul/li/a/@href')
client = redis.StrictRedis()

# 把目标链接们放进redis
for url in all_chapters_url:
    client.lpush('url_queue2', url)


# 开始一条条url爬
content_list = []
while client.llen('url_queue2') > 0:

    # 从redis 拿出一条url
    url = client.lpop('url_queue2').decode()
    print(url)
    source = requests.get(url).content

    selector = lxml.html.fromstring(source)
    chapter_name = selector.xpath('//div[@class="h1title"]/h1/text()')[0]
    content = selector.xpath('//div[@id="htmlContent"]/p/text()')

    # 存到一个装结果的list里面
    content_list.append({'title':chapter_name, 'content': '\n'.join(content)})


handler.insert_many(content_list)
