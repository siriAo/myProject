# _*_ coding : utf-8 _*_
# @Time : 2022-10-11 19:19
# @Author : Ao_Jiao
# @File : item
# @Project : myProject
from weiboSpider.asyn.user import User


class Item:
    def __init__(self, text: str, created_at: str, status_city: str, status_province: str, status_country: str,
                 user: User):
        self.text = text
        self.created_at = created_at
        self.status_city = status_city
        self.status_province = status_province
        self.status_country = status_country
        self.user = user
