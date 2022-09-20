# _*_ coding : utf-8 _*_
# @Time : 2022-09-20 11:04
# @Author : Ao_Jiao
# @File : test
# @Project : myProject
from time import sleep

from govern.item import Item
from govern.writer import Writer

import random
import requests
import json

URL = 'http://cq.gov.cn/cq12345/api/bs-tsm-oworder-slave/page'
HEADERS = {
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '62',
    'Content-Type': 'application/json',
    'Host': 'cq.gov.cn',
    'Origin': 'http://cq.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.cq.gov.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
}

session = requests.Session()
randomizer = random.Random()


def create_request(index: int):
    DATA = {'descend': 'true',
            'pageNo': index,
            'pageSize': 30,
            'sort': '',
            'status': 2
            }
    return requests.Request(method='POST', url=URL, json=DATA)


if __name__ == '__main__':
    for i in range(1, 7):
        request = session.prepare_request(create_request(i))
        response = session.send(request)

        print(response.status_code)
        print(response.text)

        js = json.loads(response.text)
        root = js['data']['result']
        try:
            for x in range(30):
                node = root[x]
                workOrderTitle = node['workOrderTitle']
                workOrderContent = node['workOrderContent']
                replyDate = node['replyDate']
                replyContent = node['replyContent']
                item = Item(workOrderTitle, workOrderContent, replyDate, replyContent)
                with Writer('data.csv', mode='a', encoding='utf-8') as wr:
                    wr.csv_write_in(delimiter=',', item=item)

        except Exception as e:
            pass

        sleep(randomizer.randint(4, 10))
