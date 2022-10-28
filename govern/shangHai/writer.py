# _*_ coding : utf-8 _*_
# @Time : 2022-10-26 20:52
# @Author : Ao_Jiao
# @File : writer
# @Project : myProject
import csv
from item import Item


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

    def csv_write_in(self, delimiter, items: [Item]):
        csv_writer = csv.writer(self.file, delimiter=delimiter)  # 指定分隔符为逗号
        for item in items:
            csv_writer.writerow([item.submit_title, item.submit_date, item.submit_content,
                                 item.reply_unit, item.public_date, item.reply_content])

