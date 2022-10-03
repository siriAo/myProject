# _*_ coding : utf-8 _*_
# @Time : 2022-10-03 15:15
# @Author : Ao_Jiao
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
        self.file = open(self.name, mode=self.mode, encoding=self.encoding,newline='')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def csv_write_in(self, delimiter, text_arr):
        csv_writer = csv.writer(self.file, delimiter=delimiter)  # 指定分隔符为逗号
        for text in text_arr:
            csv_writer.writerow([text])
