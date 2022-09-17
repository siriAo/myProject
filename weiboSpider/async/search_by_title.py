# _*_ coding : utf-8 _*_
# @Time : 2022-09-07 11:36
# @Author : AoJiao
# @File : search_by_title
# @Project : myProject

# 问题:代理频率,账号异地检测
import json
import asyncio
import logging
import aiohttp
from random import Random

# START_URL = 'https://m.weibo.cn'
TITLE = 'iphon14'
# SEARCH_URL = 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{}&page_type=searchall'.format(TITLE)
SEARCH_URL = 'http://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{}&page_type=searchall'.format(
    TITLE)
# PROXIES_POOL = ['http://183.220.145.3:80', 'http://183.220.145.3:80', 'http://183.220.145.3:80']
MY_HEADERS = [{
    'authority': 'm.weibo.cn',
    'method': 'GET',
    # 'path': '/api/container/getIndex?containerid=100103type%3D1%26q%3Dip&page_type=searchall',
    'scheme': 'https',
    # 'accept': 'application/json, text/plain, */*',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cache-control': 'no-cache',
    'cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWmc0VRWNhdlYiMav2ZDIQL5NHD95QNeKncSK-ESo.XWs4Dqcjci--RiKysi-27i--RiK.7iKL2i--fiKnpi-zNi--fiK.7iKn0i--Ri-zpiKnci--RiKnfiK.7; SCF=AmEg-bFzNVudh8QI7VXSPR5YjKW8T1zp-bPlDEHhbJDXi-WWEQDpeJXaEcRjBdrqGL4oDR_lq-b0uOwlAgWSL9c.; _T_WM=25694f0029db657d9f4581c179e15ab3; SUB=_2A25OC1qTDeRhGeFP41QU9SzKwjiIHXVt9GbbrDV6PUJbkdANLU-kkW1NQRepQQWMT26xhgV8-w_vb-0SFEL6bq0O; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174; XSRF-TOKEN=8414b0',
    # 'mweibo-pwa': 1,
    'pragma': 'no-cache',
    'referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3Dip',
    # 'sec-ch-ua': 'Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103',
    # 'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
    'x-requested-with': 'XMLHttpRequest',
    # 'x-xsrf-token': '19e4e4'
},
    {
        'authority': 'm.weibo.cn',
        'method': 'GET',
        # 'path': '/api/container/getIndex?containerid=100103type%3D1%26q%3Dip&page_type=searchall',
        'scheme': 'https',
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'cache-control': 'no-cache',
        # 'cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWmc0VRWNhdlYiMav2ZDIQL5NHD95QNeKncSK-ESo.XWs4Dqcjci--RiKysi-27i--RiK.7iKL2i--fiKnpi-zNi--fiK.7iKn0i--Ri-zpiKnci--RiKnfiK.7; SCF=AmEg-bFzNVudh8QI7VXSPR5YjKW8T1zp-bPlDEHhbJDXi-WWEQDpeJXaEcRjBdrqGL4oDR_lq-b0uOwlAgWSL9c.; _T_WM=25694f0029db657d9f4581c179e15ab3; SUB=_2A25OC1qTDeRhGeFP41QU9SzKwjiIHXVt9GbbrDV6PUJbkdANLU-kkW1NQRepQQWMT26xhgV8-w_vb-0SFEL6bq0O; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174; XSRF-TOKEN=8414b0',
        # 'mweibo-pwa': 1,
        'pragma': 'no-cache',
        'referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3Dip',
        # 'sec-ch-ua': 'Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103',
        # 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
        'x-requested-with': 'XMLHttpRequest',
        # 'x-xsrf-token': '19e4e4'
    }
]

CONCURRENCY = 3
semaphore = asyncio.Semaphore(CONCURRENCY)
randomizer = Random()
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s   %(filename)s [line:%(lineno)d]  %(message)s  %(asctime)s',
    filename='by_title.log',
    filemode='w',
    encoding='utf-8'
)
logger = logging.getLogger()


async def scrape_index(url: str, index=None):
    """
    :param url: url prepared to request
    :param index: (int)
    :return: scrape_api()
    """
    if index is None or index == 1 or index == 0:
        return await scrape_api(url, None)
    else:
        return await scrape_api(url + '&page={}'.format(index), None)


async def scrape_api(url, params):
    """
    异步的响应数据
    返回页面源码
    :param params:
    :param url: url prepared to request
    :return: response(str)
    """
    async with semaphore:  # 限制最大并发
        async with aio_session.get(url, headers=randomizer.choice(MY_HEADERS),
                                   params=params, ) as response:  # proxy=randomizer.choice(PROXIES_POOL)
            if response.status == 200:
                logger.info('{} done successfully'.format(response.url))
            else:
                logger.warning('{} failed'.format(response.url))
            return await response.text()


def parse(response):
    """
    解析json格式的响应数据
    :param response:
    :return:
    """
    js = json.loads(response)
    # 校验card_type
    # 9=>['data']['cards'][] ['mblog']['text']
    # 11=>['data']['cards'][] [card_group][]card_type=9
    for i in range(len(js['data']['cards'])):
        root = js['data']['cards'][i]

        if root['card_type'] == 9:
            print('i={} {}'.format(i, root['mblog']['text']))

        if root['card_type'] == 11:
            for j in range(len(root['card_group'])):
                target = root['card_group'][j]
                if target['card_type'] == 9:
                    print('i={} {}'.format(i, target['mblog']['text']))
        print('*' * 100)


async def main():
    """
    异步主函数
    :return:
    """
    global aio_session
    aio_session = aiohttp.ClientSession()
    # aio_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    END_INDEX = 2  # 访问1~29
    for x in range(END_INDEX):  # 目的是减缓访问频率
        if x == 0:
            result = await asyncio.gather(
                *[asyncio.create_task(scrape_index(SEARCH_URL, i)) for i in range(1, 10)])  # 1-9
        else:
            result = await asyncio.gather(
                *[asyncio.create_task(scrape_index(SEARCH_URL, i + 10 * x)) for i in range(0, 10)])  # 10-x9
        for response in result:
            parse(response)

    await aio_session.close()
    await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
