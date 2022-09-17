# _*_ coding : utf-8 _*_
# @Time : 2022-08-07 18:13
# @Author : AoJiao
# @File : __init__.py
# @Project : myProject

import urllib.parse
from random import Random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

import Parser
from Writer import Writer

START_URL = 'https://www.taobao.com/'
BASIC_URL = 'https://s.taobao.com/search?q={}&s={}'
PRODUCT_NAME = '飞利浦'
END_PAGE = 2

if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                            {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})
    browser.get(START_URL)
    browser.maximize_window()
    browser.find_element(By.ID, 'q').send_keys(PRODUCT_NAME)
    sleep(Random().randint(1, 3))
    browser.find_element(By.CLASS_NAME, 'btn-search').click()

    # 手动扫码登录
    sleep(30)

    # 解析第一页商品元素
    res = Parser.parse(browser)
    # 写入到本地
    with Writer('taobao.csv', mode='a', encoding='utf-8') as wr:
        for item in res:
            wr.csv_write_in(delimiter=',', item=item)

    # 解析后续页面
    page = 1
    while page != END_PAGE:
        browser.get(
            BASIC_URL.format(urllib.parse.quote(PRODUCT_NAME),
                             page * 44))
        # 解析商品元素
        res = Parser.parse(browser)
        # 写入到本地

        with Writer('taobao.csv', mode='a', encoding='utf-8') as wr:
            for item in res:
                wr.csv_write_in(delimiter=',', item=item)
        sleep(Random().randint(1, 3))
        page += 1
    '''
    # 写入到本地
    for item in res:
        Writer.write(item)
    '''
