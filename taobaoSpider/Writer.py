# _*_ coding : utf-8 _*_
# @Time : 2022-08-07 18:20
# @Author : AoJiao
# @File : writer
# @Project : myProject
import csv


class Writer:
    def __init__(self, name, mode, encoding):
        self.name = name
        self.mode = mode
        self.encoding = encoding
        self.file = None

    def __enter__(self):
        self.file = open(self.name, mode=self.mode, encoding=self.encoding)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def csv_write_in(self,  delimiter, item):
        csv_writer = csv.writer(self.file, delimiter=delimiter)  # 指定分隔符为逗号
        csv_writer.writerow([item.info, item.price, item.num, item.name])


'''
def write(item):
    with open('taobao.csv', mode='a', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',')  # 指定分隔符为逗号
        csv_writer.writerow([item.info, item.price, item.num, item.name])
'''
