# _*_ coding : utf-8 _*_
# @Time : 2022-08-07 18:20
# @Author : AoJiao
# @File : parser
# @Project : myProject
from selenium.webdriver.common.by import By

import Item


def parse(browser):
    res = []
    divs = browser.find_elements(By.XPATH, '//div[@class="items"]/div[contains(@class,"item J_MouserOnverReq")]')
    print(divs)
    for div in divs:
        info = div.find_element(By.XPATH, './/div[@class="row row-2 title"]/a').text
        price = div.find_element(By.XPATH, './/strong').text + '元'
        nums = div.find_element(By.XPATH, './/div[@class="deal-cnt"]').text
        names = div.find_element(By.XPATH, './/div[@class="shop"]/a').text
        res.append(Item.Item(info, price, nums, names))
        print(info, price, nums, names)
    return res
