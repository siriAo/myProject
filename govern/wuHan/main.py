# _*_ coding : utf-8 _*_
# @Time : 2022-11-08 15:09
# @Author : Ao_Jiao
# @File : main
# @Project : myProject
import json
import time
import random
import requests
from govern.wuHan.item import Item
from govern.wuHan.mongoDB import Mongo

# POST
URL = 'http://api1.liuyan.cjn.cn/messageboard/internetUserInterface/selectThreadsByGroup'
DETAIL_URL = 'http://api1.liuyan.cjn.cn/messageboard/internetUserInterface/selectThreadsOne'
# handleState: 1全部 2办理中 3已回复
# fid: 6 江岸区已回复 50644 条
# pageSize=100&pageNum=1& fid=6 & handleState=  &threadState=&
# pageSize=100&pageNum=2& fid=6 & handleState=3 &threadState=&

# pageSize=100&pageNum=1& fid=7 & handleState=3 &threadState=&
# pageSize=100&pageNum=2& fid=7 & handleState=3 &threadState=&

# pageSize=100&pageNum=1& fid=8 & handleState=3 &threadState=&
# pageSize=100&pageNum=2& fid=8 & handleState=3 &threadState=&
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '56',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'api1.liuyan.cjn.cn',
    'Origin': 'http://liuyan.cjn.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://liuyan.cjn.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}
session = requests.Session()
RAND = random.Random()


def scrape_list(page: int, fid: int):
    data = {'pageSize': 50,
            'pageNum': page,
            'fid': fid,
            'handleState': 3,
            }
    try:
        return scrape_api(URL, data)
    except Exception as e:
        print(e.message)
        return None


def scrape_detail(tid: int):
    data = {'tid': tid
            }
    try:
        return scrape_api(DETAIL_URL, data)
    except Exception as e:
        print(e.message)
        return None


def scrape_api(url, data):
    time.sleep(RAND.randint(2, 4))
    response = session.post(url, data=data, headers=HEADERS)
    if response.status_code == 200:
        print('{} ok. Data={}'.format(url, data))
        return response
    else:
        if response.status_code == 502:
            scrape_api(url, data)
        else:
            print('{} error. Data={}'.format(url, data))
            return None


def parse_list(response):
    items = []
    root = json.loads(response.text)['rows']
    for i in range(len(root)):
        target = root[i]
        title = target['subject']  # 标题
        content = target['content']  # 正文
        dateline_txt = target['dateline_txt']  # 留言时间
        domainId = target['domainId']  # 分类码
        domainId_txt = target['domainId_txt']  # 问题分类（社会服务,公园、绿化广场管理问题等）
        queryCode = target['queryCode']  # tid查询码
        typeId = target['typeId']  # 留言类别码
        typeId_txt = target['typeId_txt']  # 留言类别（问题反映,咨询等）

        item = Item(title, content, dateline_txt, domainId, domainId_txt, queryCode, typeId, typeId_txt)
        items.append(item)
    return items


def parse_detail(tid: int):
    response = scrape_detail(tid)
    target = json.loads(response.text)['threadsObj']['answersList'][0]
    asContent = target['asContent']  # 回复内容
    organization = target['organization']  # 回复组织
    replydateline_txt = target['dateline_txt']  # 回复时间
    feedbackContent = target['feedbackContent']  # 题主追问
    feedbackCreateTime = target['feedbackCreateTime']  # 追问时间
    return asContent, organization, replydateline_txt, feedbackContent, feedbackCreateTime


if __name__ == '__main__':

    endPage = 1013
    for i in range(211, endPage + 1):
        response = scrape_list(page=i, fid=6)
        items = parse_list(response)
        for item in items:
            args = parse_detail(item.queryCode)
            item.update(*args)
            item.clean()
            # print(item)
        # 写入MongoDB
        collection = Mongo(db='govern', collection='wuHan')
        collection.insert_many(items)
