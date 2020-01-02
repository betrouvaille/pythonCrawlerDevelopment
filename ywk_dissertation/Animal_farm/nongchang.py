import os
import re
import requests
from multiprocessing.dummy import Pool

start_url = 'http://www.kanunu8.com/book3/6879/'


def get_source(url):
    """
    获取网页源代码
    :param url:网址
    :return:网页源代码
    """
    html = requests.get(url)
    return html.content.decode('gbk')


def get_toc(html):
    """
    获取每一章链接存储到列表中并返回
    :param html: 目录页源代码
    :return: 每章链接
    """
    toc_url_list = []
    toc_block = re.findall('正文(.*?)</tbody>', html, re.S)[0]
    toc_url = re.findall('href="(.*?)"', toc_block, re.S)
    for url in toc_url:
        toc_url_list.append(start_url + url)
    return toc_url_list


def get_article(html):
    """
    获取正文返回章节名和正文内容
    :param html:正文源代码
    :return:章节名和正文内容
    """
    chapter_name = re.search('size="4">(.*?)<', html, re.S).group(1)
    text_block = re.search('<p>(.*?)</p>', html, re.S).group(1)
    text_block = text_block.replace('<br />', '')
    return chapter_name, text_block


def query_article(url):
    """
    获取正文源代码
    :param url: 正文的网址
    :return:
    """
    article_html = get_source(url)
    chapter_name, article_text = get_article(article_html)
    save(chapter_name, article_text)


def save(chapter, article):
    """
    将每一章保存到本地
    :param chapter:章节名
    :param article: 正文
    :return:
    """
    os.makedirs('动物农场', exist_ok=True)
    with open(os.path.join('动物农场', chapter + '.txt'), 'w', encoding='utf-8') as f:
        f.write(article)


if __name__ == '__main__':
    toc_html = get_source(start_url)
    toc_list = get_toc(toc_html)
    pool = Pool(4)
    pool.map(query_article, toc_list)
