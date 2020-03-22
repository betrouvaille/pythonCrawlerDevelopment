from lxml import etree
import requests

BASE_DOMAIN = 'https://www.dytt8.net'

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "https://www.dytt8.net/html/gndy/dyzz/list_23_1.html"
    }


def get_detail_urls(url):
    """

    :param url:
    :return:
    """
    detail_urls_list = []
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('gb2312', 'ignore')
    html = etree.HTML(text)
    detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
    for detail_url in detail_urls:
        detail_url = BASE_DOMAIN + detail_url
        detail_urls_list.append(detail_url)
    return detail_urls_list


def parse_detail_page(url):
    movie = {}
    response = requests.get(url=url,headers=HEADERS)
    text = response.content.decode('gbk', 'ignore')
    html = etree.HTML(text)
    title = html.xpath('//*[@id="header"]/div/div[3]/div[3]/div[1]/div[2]/div[1]/h1/font/text()')[0]
    movie['title'] = title
    try:
        photo = html.xpath('//*[@id="Zoom"]//img/@src')[0]
    except IndexError:
        photo = 'null'
    movie['photo'] = photo
    print(movie)


def spider():

    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for i in range(1, 8):
        url = base_url.format(i)
        movie_detail_urls = get_detail_urls(url)
        for movie_detail_url in movie_detail_urls:
            movie = parse_detail_page(movie_detail_url)


if __name__ == '__main__':
    spider()