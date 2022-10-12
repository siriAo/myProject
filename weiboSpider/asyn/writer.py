# _*_ coding : utf-8 _*_
# @Time : 2022-10-03 15:15
# @Author : Ao_Jiao
# @File : writer
# @Project : myProject
import csv

from weiboSpider.asyn.item import Item


class Writer:
    def __init__(self, name, mode, encoding):
        self.name = name
        self.mode = mode
        self.encoding = encoding
        self.file = None

    def __enter__(self):
        self.file = open(self.name, mode=self.mode, encoding=self.encoding, newline='')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def csv_write_in(self, delimiter, items: Item):
        csv_writer = csv.writer(self.file, delimiter=delimiter)  # 指定分隔符为逗号
        for item in items:
            csv_writer.writerow(
                [item.text, item.created_at, item.user.id, item.user.screen_name, item.user.followers_count,
                 item.status_city, item.status_province, item.status_country])
