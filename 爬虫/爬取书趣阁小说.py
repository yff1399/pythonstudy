#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# 用于爬书趣阁下载小说

import requests
import parsel
import os

# 下载一章
def get_one_chapter(url, book_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    html = response.text
    sel = parsel.Selector(html)
    title = sel.css('.content h1::text').extract_first()
    contents = sel.css('#content::text').extract()
    contents1 = [content.strip() for content in contents]
    text = '\n'.join(contents1)

    print(book_name + '/' + title + '.txt')

    with open(book_name + '/' + title + '.txt', mode='w', encoding='utf-8') as f:
        f.write(title + '\r\n')
        f.write(text)


def get_all_chapter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36 '
    }

    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    sel = parsel.Selector(response.text)
    # 书名
    book_name = sel.css('body > div.book > div.info > h2::text').extract_first()
    if not os.path.exists(book_name):
        os.mkdir(book_name)

    for a in sel.css('body > div.listmain > dl > dd > a::attr(href)').extract():
        book_url = url + a
        get_one_chapter(book_url, book_name)


# 下载整本《元尊》
# url = 'http://www.shuquge.com/txt/5809/'
# 下载整本《剑来》
url = 'http://www.shuquge.com/txt/8659/'
get_all_chapter(url)
