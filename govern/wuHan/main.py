# _*_ coding : utf-8 _*_
# @Time : 2022-11-08 15:09
# @Author : Ao_Jiao
# @File : main
# @Project : myProject

import random
import time

import requests

# POST
URL = 'http://api1.liuyan.cjn.cn/messageboard/internetUserInterface/selectThreadsByGroup'
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


def scrape_list(i: int, fid: int):
    data = {'pageSize': 100,
            'pageNum': i,
            'fid': fid,
            'handleState': 3,
            'threadState': ''
            }
    try:
        return scrape_api(URL, data)
    except Exception as e:
        print(e.message)
        return None


def scrape_api(url, data):
    time.sleep(RAND.randint(2, 4))
    response = session.post(url, data=data, headers=HEADERS)
    if response.status_code == 200:
        print('{} ok'.format(url))
        return response
    else:
        if response.status_code == 502:
            scrape_api(url, data)
        else:
            print('{} error'.format(url))
            return None


def parse_list():
    pass


def parse_detail():
    pass


if __name__ == '__main__':
    pass
