# _*_ coding : utf-8 _*_
# @Time : 2022-10-26 15:30
# @Author : Ao_Jiao
# @File : lingDaoXinXiang
# @Project : myProject
import asyncio
import random
import time

import requests

from govern.shangHai.writer import Writer
from parsel import Selector
from item import Item
from mongoDB import Mongo

# ldxx->swld
# https://xfb.sh.gov.cn/xinfang/swld/feedback/feedbacklist?testpara=0&pageNo=1&pagesize=10
# https://xfb.sh.gov.cn/xinfang/swld/feedback/feedbacklist?testpara=0&pageNo=2&pagesize=10

# https://xfb.sh.gov.cn/xinfang/swld/feedback/feedbackshow?id=428681328F5A40789C01302CB062E351

# hfxd->szzc
# https://xfb.sh.gov.cn/xinfang/szzc/feedback/feedbacklist?testpara=0&pageNo=1&pagesize=10
# https://xfb.sh.gov.cn/xinfang/szzc/feedback/feedbacklist?testpara=0&pageNo=2&pagesize=10

# https://xfb.sh.gov.cn/xinfang/szzc/feedback/feedbackshow?id=6A1C13FD2D4C4F6A81E380928E6EDBA8

LIST_URL = 'https://xfb.sh.gov.cn/xinfang/swld/feedback/feedbacklist'
DETAIL_URL = 'https://xfb.sh.gov.cn/xinfang/swld/feedback/feedbackshow'
# LIST_URL = 'https://xfb.sh.gov.cn/xinfang/szzc/feedback/feedbacklist'
# DETAIL_URL = 'https://xfb.sh.gov.cn/xinfang/szzc/feedback/feedbackshow'
HEADERS = {'Cache-Control': 'no-cache',
           'Host': 'xfb.sh.gov.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
           }
session = requests.session()
RAND = random.Random()
# 隧道域名:端口号
tunnel = "v677.kdltps.com.com:15818"
# 用户名密码方式
username = "t16684119323712"
password = "5t85vy58"
proxies = {
    # "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}


def scrape_list(i: int):
    params = {'testpara': 0,
              'pageNo': i,
              'pagesize': 10
              }
    try:
        return scrape_api(LIST_URL, params)
    except Exception as e:
        print(e.message)
        return None


def scrape_detail(id: str):
    params = {'id': id}
    try:
        return scrape_api(DETAIL_URL, params)
    except Exception as e:
        print(e.message)
        return None


def scrape_api(url, params):
    time.sleep(RAND.randint(2, 4))
    response = session.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        print('{} ok'.format(url))
        return response
    else:
        if response.status_code == 502:
            scrape_api(url, params)
        else:
            print('{} error'.format(url))
            return None


def parse_list(html: str):
    arr = []
    selector = Selector(text=html)
    items = selector.xpath("//table[@id='Datatable-1']/tbody/tr")
    # print(type(items), len(items), items)
    for item in items:
        # <class 'parsel.selector.SelectorList'>
        href = item.xpath("td[1]/a/@href")
        submit_title = item.xpath("td[1]/a/text()")
        reply_unit = item.xpath("td[2]/text()")
        public_date = item.xpath("td[3]/text()")
        # print(type(href), href.get(), submit_title.get(), reply_unit.get(), public_date.get())
        arr.append(Item(href.get(), submit_title.get(), reply_unit.get(), public_date.get()))
    return arr


def parse_detail(html: str):
    selector = Selector(text=html)
    item = selector.xpath("//table[@class='cd_table2']/tbody")
    # print(type(item), len(item), item)
    submit_date = item.xpath("tr[2]/td[2]//span/text()")  # 来信日期
    submit_content = item.xpath("tr[3]/td[2]//span/text()")  # 来信内容
    reply_content = item.xpath("tr[6]/td[2]//span/text()")  # 回复内容
    # print(submit_date.get(), submit_content.get(), reply_content.get())
    return submit_date.get(), submit_content.get(), reply_content.get()


if __name__ == '__main__':
    # response = scrape_list(1)
    # items = parse_list(response.text)
    #
    # response = scrape_detail(items[0].id)
    # args = parse_detail(response.text)
    # items[0].update(*args)
    # items[0].clean()
    # response = scrape_detail(items[1].id)
    # args = parse_detail(response.text)
    # items[1].update(*args)
    # items[1].clean()
    # items = [items[0], items[1]]
    max_page = 705
    for i in range(446, max_page + 1):
        response = scrape_list(i)
        if response:
            items = parse_list(response.text)
        else:
            continue
        for item in items:
            response = scrape_detail(item.id)
            if response:
                args = parse_detail(response.text)
                item.update(*args)
                item.clean()
        # 写入本地
        with Writer(name='ldxx.csv', mode='a', encoding='utf-8') as writer:
            writer.csv_write_in(delimiter=',', items=items)
        collection = Mongo(db='govern', collection='ldxx')
        collection.insert_many(items)

    '''
    max_page = 893
    for i in range(1, max_page + 1):
        response = scrape_list(i)
        if response:
            items = parse_list(response.text)
        else:
            continue
        for item in items:
            response = scrape_detail(item.id)
            if response:
                args = parse_detail(response.text)
                item.update(*args)
                item.clean()
        # 写入本地
        with Writer(name='hfxd.csv', mode='a', encoding='utf-8') as writer:
            writer.csv_write_in(delimiter=',', items=items)
        collection = Mongo(db='govern', collection='hfxd')
        collection.insert_many(items)
        '''




