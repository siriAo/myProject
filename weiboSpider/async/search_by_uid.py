import logging
import asyncio
import aiohttp
import re
from opencc import OpenCC
from parsel import Selector
from random import Random

UID = 6593199887  # 原神
# UID = 7643376782  # 崩坏3
# UID = 6415164493  # 米哈游
# UID = 1878206395  # 张继科
# UID = 1686532492  # 撒贝宁
# UID = 1776448504  # 蔡徐坤
# UID = 1699432410  # 新华社

# START_URL = 'https://weibo.cn'
TARGET_URL = 'https://weibo.cn/u/{}'.format(UID)
# PROXIES_POOL=['http://183.220.145.3:80','http://183.220.145.3:80','http://183.220.145.3:80']
MY_HEADERS = [{
    'authority': 'weibo.cn',
    'method': 'GET',
    # 'path': '/u/6415164493',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWmc0VRWNhdlYiMav2ZDIQL5NHD95QNeKncSK-ESo.XWs4Dqcjci--RiKysi-27i--RiK.7iKL2i--fiKnpi-zNi--fiK.7iKn0i--Ri-zpiKnci--RiKnfiK.7; SCF=AmEg-bFzNVudh8QI7VXSPR5YjKW8T1zp-bPlDEHhbJDXi-WWEQDpeJXaEcRjBdrqGL4oDR_lq-b0uOwlAgWSL9c.; _WEIBO_UID=7186552694; _T_WM=25694f0029db657d9f4581c179e15ab3; SUB=_2A25OC1qTDeRhGeFP41QU9SzKwjiIHXVt9GbbrDV6PUJbkdANLU-kkW1NQRepQQWMT26xhgV8-w_vb-0SFEL6bq0O; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4811021724681431%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E5%25B0%258F%25E9%25BB%2591%25E5%25AD%2590',
    'pragma': 'no-cache',
    # 'referer': 'https://weibo.cn/7186552694/follow',
    # 'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    # 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'
},
    {
        'authority': 'weibo.cn',
        'method': 'GET',
        # 'path': '/u/6415164493',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'cookie': '_T_WM=7caaa4548fc1763ff481143848ab99e8; MLOGIN=1; SCF=AhHd-Hi2qQD2QXv6h0FQf5JcuN0YEfSeOBQyHIvblpOqT4lRpBdWUaZhq7gp7RdeJ9dLFqfinPCVSwODeVznD6M.; SUB=_2A25OHACiDeRhGeFJ41QZ8C_OzzyIHXVt_qDqrDV6PUJbktANLWjSkW1NfuRN_HMavqILA8Ot35pa1ZDrVRpnD9gs; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFW2JJ2xLsHBVrHqiBFC-Ud5JpX5K-hUgL.FoMN1hqReh2ESh52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMp1KeReh.4SoqX; SSOLoginState=1662546162; ALF=1665138162',
        'pragma': 'no-cache',
        # 'referer': 'https://weibo.cn/7186552694/follow',
        # 'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        # 'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
]

# aio_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
CONCURRENCY = 5
semaphore = asyncio.Semaphore(CONCURRENCY)
randomizer = Random()
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s   %(filename)s [line:%(lineno)d]  %(message)s  %(asctime)s',
    filename='by_uid.log',
    filemode='w',
    encoding='utf-8'
)
logger = logging.getLogger()


async def get_url(index=None):
    """
    :param index: page
    :return: weibo_list, page
    """
    response = await scrape_index(TARGET_URL, index)
    # 解析url
    selector = Selector(text=response)
    url_list = selector.xpath('//div[@class="c"]/div/a[@class="cc"]/@href').getall()  # 获取评论链接
    # url清洗
    weibo_list, zhuanfa_list = clean_url(url_list)
    # 获取页数
    page = ''
    temp = selector.xpath('//div[@id="pagelist"]//div/text()').getall()
    if len(temp) == 0:
        page = None
    else:
        for element in temp:
            page += element
        page = int(re.search('\d+/(\d+)页', page).group(1))
    return weibo_list, page


def clean_url(url_list):
    """
    清洗url_list
    :param url_list: (list) a dirty url_list
    :return: a cleaned list
    """
    weibo_list = []  # 本人发布的微博
    zhuanfa_list = []  # 转发的微博
    for url in url_list:
        if url:
            content = str(url)
            match_result = re.match('(^https://weibo\.cn/comment/.*\?uid=\d+)&rl', content)
            if match_result is not None:
                weibo_list.append(match_result.group(1))
            else:
                match_result = re.match('(^https://weibo\.cn/comment/.*)\?', content)
                zhuanfa_list.append(match_result.group(1))
    return weibo_list, zhuanfa_list


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


async def scrape_index(url, index=None):
    """
    :param url: url prepared to request
    :param index: (int)
    :return: scrape_api()
    """
    if index is None or index == 1 or index == 0:
        return await scrape_api(url, None)
    else:
        return await scrape_api(url, {'page': index})


def parse_index(html):
    """
    解析服务器响应数据
    :param html: http doc response
    :return:
    """
    print(html)
    selector = Selector(text=html)
    # 解析正文
    content = ''
    items = selector.xpath('//div[@class="c"]/div/span/text()').getall()
    if len(items) == 0:
        # public_time 发文日期 content 微博正文
        content = None
        public_time = None
    else:
        public_time = items[-1]
        for item in items:
            content += item

    # 解析页数
    page = ''
    temp = selector.xpath('//div[@id="pagelist"]//div/text()').getall()
    if len(temp) == 0:
        page = None
    else:
        for element in temp:
            page += element
        page = int(re.search('\d+/(\d+)页', page).group(1))

    # 解析评论
    comment_list = selector.xpath('//div[@class="c"]/span[@class="ctt"]/text()').getall()
    if len(comment_list) == 0:
        comment_list = None
    else:
        # 评论清洗
        comment_list = clean_comment(comment_list)
    print(public_time, content)
    print(comment_list)
    print(page)
    print('*' * 100)
    return public_time, content, comment_list, page

    # 存储数据部分


def clean_comment(arr: list):
    """
    清洗评论数据
    :param arr:
    :return:
    """
    p = [x.strip() for x in arr if x.strip() != '' and x != '回复']
    q = [x.lstrip(':') for x in p if len(x) > 1]
    res = []
    for x in q:
        # 清洗表情
        m = re.sub(r'\[.*]', '', x)
        # 清洗英文
        o = re.sub(r'[\dA-Za-z]', '', m)
        # 繁转简
        n = OpenCC('t2s').convert(o)
        # 剔除非中文部分
        line = ''
        for c in n:
            if 19968 < ord(c) < 40869:  # 中文utf-8编码范围为0X4E00-0x9FA5 即19968-40869
                line += c
        if len(line) != 0:
            res.append(line)
    if len(res) == 0:
        return None
    else:
        return res


async def main():
    """
    异步主函数
    :return:
    """
    global aio_session
    aio_session = aiohttp.ClientSession()
    url_list, page = await get_url()
    print(url_list)

    if page:
        t = 1  # 微博主页定位
        page = 2  # 测试限制主页微博为2页
        for _ in range(1, page + 1):
            results = await asyncio.gather(
                *[asyncio.create_task(scrape_index(url)) for url in url_list])  # 因为task一定会被完成，所以不能通过回调函数判断抓取结果
            n = 0
            for result in results:  # 解析
                time, content, comment_list, page_ = parse_index(result)  # 解析结果
                if page_:
                    if page_ > 3:
                        page_ = 3  # 测试限制评论为3页
                        res = await asyncio.gather(
                            *[asyncio.create_task(scrape_index(url_list[n], j)) for j in range(2, page_ + 1)])
                        for r in res:
                            parse_index(r)
                else:
                    continue
                n += 1
            t += 1
            url_list, page = await get_url(t)
            print(url_list)

    await aio_session.close()
    await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
