# _*_ coding : utf-8 _*_
# @Time : 2022-08-10 17:15
# @Author : AoJiao
# @File : __init__.py
# @Project : pythonProject
import re
from random import Random
from time import sleep
from lxml import etree
from requests import Request, session

# UID = 7643376782  # 崩坏3
# UID = 6415164493  # 米哈游
# UID = 1878206395  # 张继科
UID = 1165631310  # 周杰伦
# UID = 1686532492  # 撒贝宁
# UID = 1776448504  # 蔡徐坤
# START_URL = 'https://weibo.cn'
TARGET_URL = 'https://weibo.cn/u/{}'.format(UID)
TARGET_URL_FROM_SECOND = 'https://weibo.cn/u/{}?page={}'
WEIBO_URL_FROM_SECOND = '{}&page={}'
headers = {
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
}
session = session()
randomizer = Random()


def request_url(method, url, headers):
    request = Request(method, url=url, headers=headers)
    pre = session.prepare_request(request)
    for _ in range(2):
        response = session.send(pre)  # response <class 'requests.models.Response'>
        if response.status_code == 200:
            # print('响应正文:', response.text)  # <class 'str'>
            return response
        else:
            print('访问频次过快，即将重新请求')
            sleep(randomizer.randint(4, 5))
    print(url, '访问失败')
    return None


# 解析用户页面 (可调整是否查看转发微博的原文)
def parse_root_page(response):
    html = etree.HTML(response.content)  # html <class 'lxml.etree._Element'>,response.content <class 'bytes'>
    url_list = html.xpath(
        '//div[@class="c"]/div/a[@class="cc"]/@href')  # 获取本页所有评论链接 <class 'lxml.etree._ElementUnicodeResult'>
    weibo_list, zhuanfa_list = clean_url(url_list)  # url清洗
    # url_list = weibo_list + zhuanfa_list  # 所有url
    total_page = parse_pages(html)

    print('第{}微博'.format(total_page))
    print('微博链接:', weibo_list)
    print('*' * 100)
    return weibo_list, total_page


# url清洗
def clean_url(url_list):
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


# 解析微博正文页面
def parse_articlepage(response):
    html = etree.HTML(response.content)
    content = ''
    content_list = html.xpath('//div[@class="c"]/div/span/text()')
    comment_list, total_comment_page = parse_comment(html)
    for element in content_list:
        content += element
    print('发文时间', content_list[-1])
    print('微博正文:', content)
    print('评论:', comment_list)
    print('第{}评论'.format(total_comment_page))
    return content, comment_list, total_comment_page


# 解析微博正文第二页
def parse_commentpage(response):
    html = etree.HTML(response.content)
    comment_list, total_comment_page = parse_comment(html)
    print('评论:', comment_list)
    print('第{}评论'.format(total_comment_page))
    return comment_list, total_comment_page


# 解析评论
def parse_comment(html):
    comment_list = html.xpath('//div[@class="c"]/span[@class="ctt"]/text()')
    total_comment_page = parse_pages(html)
    return comment_list, total_comment_page


# 解析一共多少页
def parse_pages(html):
    page = ''
    temp = html.xpath('//div[@id="pagelist"]//div/text()')
    for element in temp:
        page += element
    return page  # '2/34页'


def visit_all_weibo_list(weibo_url_list):
    for i in weibo_url_list:
        # 跳转至微博正文页面
        response = request_url('GET', url=i, headers=headers)
        if response is None:
            break

        # 解析微博正文页
        content, comment_list, total_comment_page = parse_articlepage(response)
        print('*' * 100)

        sleep(randomizer.randint(1, 3))

        # 解析微博第二页以后的评论页
        if total_comment_page:
            comment_max_page = int(re.search('\d+/(\d+)页', total_comment_page).group(1))  # '2/34页'

            # 测试设置 只保留2页评论
            if comment_max_page > 2:
                comment_max_page = 2

            for page in range(2, comment_max_page + 1):
                response = request_url('GET', url=WEIBO_URL_FROM_SECOND.format(i, page), headers=headers)
                if response is None:
                    continue
                comment_list, total_comment_page = parse_commentpage(response)
                print('*' * 100)
                sleep(randomizer.randint(1, 3))


if __name__ == '__main__':
    print('正在爬取 UID={} 的微博'.format(UID))
    print('*' * 100)
    # 访问目标uid第一页的微博
    response = request_url('GET', url=TARGET_URL, headers=headers)
    weibo_url_list, main_max_page = parse_root_page(response)
    visit_all_weibo_list(weibo_url_list)

    sleep(randomizer.randint(1, 3))

    # 访问目标uid第二页之后的微博
    if main_max_page:
        main_max_page = int(re.search('\d+/(\d+)页', main_max_page).group(1))
        for j in range(2, main_max_page + 1):
            response = request_url('GET', url=TARGET_URL_FROM_SECOND.format(UID, j), headers=headers)
            if response is None:
                print('第{}页微博访问失败'.format(j))
                break

            weibo_url_list, main_max_page = parse_root_page(response)
            visit_all_weibo_list(weibo_url_list)

            sleep(randomizer.randint(1, 3))
