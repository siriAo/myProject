# _*_ coding : utf-8 _*_
# @Time : 2022-09-07 11:36
# @Author : AoJiao
# @File : search_by_title
# @Project : myProject

# 问题:代理频率,账号异地检测
import re
import json
import asyncio
import logging
import aiohttp
from random import Random

# START_URL = 'https://m.weibo.cn'
TITLE = '永远会被女生之间的友情感动'
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
        # 'cookie': '_T_WM=7caaa4548fc1763ff481143848ab99e8; SCF=AhHd-Hi2qQD2QXv6h0FQf5JcuN0YEfSeOBQyHIvblpOqtpAxstF_TTHfDlH9UBuYWXV8AS1nW-9IByfbhGbEkmc.; SUB=_2A25OHAqkDeRhGeFJ41QZ8C_OzzyIHXVt_pbsrDV6PUNbktANLUfjkW1NfuRN_DAI5IjIVxXSQF5JfHjJqKsCHzYM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFW2JJ2xLsHBVrHqiBFC-Ud5JpX5KMhUgL.FoMN1hqReh2ESh52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMp1KeReh.4SoqX; ALF=1665140724; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=8ad9f9; mweibo_short_token=b7b8a4f6fa; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2597%25A5%25E6%259C%25AC%25E5%258F%2591%25E5%25B8%2583%25E6%259C%2580%25E9%25AB%2598%25E7%25BA%25A7%25E5%2588%25AB%25E9%25A2%2584%25E8%25AD%25A6%26fid%3D100103type%253D1%2526q%253D%25E6%2597%25A5%25E6%259C%25AC%25E5%258F%2591%25E5%25B8%2583%25E6%259C%2580%25E9%25AB%2598%25E7%25BA%25A7%25E5%2588%25AB%25E9%25A2%2584%25E8%25AD%25A6%26uicode%3D10000011',
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
        # 'x-xsrf-token': '8ad9f9'
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
        # 'cookie': '_T_WM=19540876774; XSRF-TOKEN=5c084b; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26uicode%3D10000011%26fid%3D100103type%253D1%2526t%253D10%2526q%253D%2523%25E8%258B%25B1%25E9%259B%2584%25E5%259B%259E%25E5%25AE%25B6%2523',
        # 'mweibo-pwa': 1,
        'pragma': 'no-cache',
        'referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3Dip',
        # 'sec-ch-ua': 'Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103',
        # 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'x-xsrf-token': '5c084b'
    },
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
            return await response.text(), response.url


async def parse(response):
    """
    解析json格式的响应数据
    :param response:
    :return:
    """
    js = json.loads(response[0])
    if js['ok'] == 1:
        # 校验先后顺序ok,card_type
        # 9=>['data']['cards'][] ['mblog']['text']
        # 11=>['data']['cards'][] [card_group][]card_type=9
        for i in range(len(js['data']['cards'])):
            text = ''
            temp = ''
            root = js['data']['cards'][i]

            if root['card_type'] == 9:
                temp = root['mblog']['text']

            if root['card_type'] == 11:
                for j in range(len(root['card_group'])):
                    target = root['card_group'][j]
                    if target['card_type'] == 9:
                        temp = target['mblog']['text']

            # 清洗数据
            result = re.search('<a href=".*?(\d+)">全文</a>', temp)
            if result:
                href = result.group(1)
                url = 'https://m.weibo.cn/statuses/extend?id=' + href
                logger.info('{} registered into the loop'.format(url))
                r = await scrape_index(url)
                text = parse_detail(r[0])
            else:
                text = re.sub('<.*?>', '', temp)
            print('i={} {}'.format(i, text))
            print('-' * 100)
        return True

    else:
        logger.warning('{} data does not exist.'.format(response[1]))
        print('{} 数据不存在或无数据返回'.format(response[1]))
        return False


def parse_detail(response):
    text = ''
    js = json.loads(response)
    # 清洗数据
    temp = js['data']['longTextContent']
    text = re.sub('<.*?>', '', temp)
    return text


# /status/4815116816878481
# https://m.weibo.cn/detail/4815116816878481
# 正文API:https://m.weibo.cn/statuses/extend?id=4815116816878481
# 评论API:https://m.weibo.cn/comments/hotflow?id=4815116816878481&mid=4815116816878481&max_id_type=0
# https://m.weibo.cn/detail/4815108959636382
# 正文API:https://m.weibo.cn/statuses/extend?id=4815111493519560
# 评论API:https://m.weibo.cn/comments/hotflow?id=4815111493519560&mid=4815111493519560&max_id_type=0

async def main():
    """
    异步主函数
    :return:
    """
    global aio_session
    aio_session = aiohttp.ClientSession()
    # aio_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    flag = True  # 没有考虑ip被封的情况下，防止设定访问频数严重超出可响应范围
    END_INDEX = 1  # 下拉刷新19次
    for x in range(END_INDEX):  # 目的是减缓访问频率
        if flag:
            if x == 0:
                result = await asyncio.gather(
                    *[asyncio.create_task(scrape_index(SEARCH_URL, i)) for i in range(1, 10)])  # 1-9
            else:
                result = await asyncio.gather(
                    *[asyncio.create_task(scrape_index(SEARCH_URL, i + 10 * x)) for i in range(0, 10)])  # 10-x9
            for response in result:
                flag = await parse(response)

    await aio_session.close()
    await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
