# _*_ coding : utf-8 _*_
# @Time : 2022-10-26 18:42
# @Author : Ao_Jiao
# @File : item
# @Project : myProject
import re


class Item:
    def __init__(self, href: str, submit_title: str, reply_unit: str, public_date: str):
        """

        :param href:
        :param submit_title:标题
        :param reply_unit:回复单位
        :param public_date:发布日期
        """
        # feedbackshow?id=428681328F5A40789C013
        self.id = re.match('feedbackshow\?id=(.*)', href).group(1)
        self.submit_title = submit_title  # 来信标题
        self.submit_date = None  # 来信日期
        self.submit_content = None  # 来信内容
        self.reply_unit = reply_unit  # 回复单位
        self.public_date = public_date  # 发布日期
        self.reply_content = None  # 回复内容

    def __str__(self):
        return 'submit_title={}\nsubmit_date={}\nsubmit_content={}\nreply_unit={}\npublic_date={}\nreply_content={}'.format(
            self.submit_title, self.submit_date, self.submit_content,
            self.reply_unit, self.public_date, self.reply_content)

    def update(self, submit_date, submit_content, reply_content):
        self.submit_date = submit_date
        self.submit_content = submit_content
        self.reply_content = reply_content

    def clean(self):
        if self.submit_title:
            self.submit_title = self.submit_title.replace('\r', '')  # 来信标题
        if self.submit_date:
            self.submit_date = self.submit_date.replace('\r', '')  # 来信日期
        if self.submit_content:
            self.submit_content = self.submit_content.replace('\r', '')  # 来信内容
        if self.reply_unit:
            self.reply_unit = self.reply_unit.replace('\r', '')  # 回复单位
        if self.public_date:
            self.public_date = self.public_date.replace('\r', '')  # 发布日期
        if self.reply_content:
            self.reply_content = self.reply_content.replace('\r', '')  # 回复内容

    def toMongo(self):
        return {'submit_title': self.submit_title,
                'submit_date': self.submit_date,
                'submit_content': self.submit_content,
                'reply_unit': self.reply_unit,
                'public_date': self.public_date,
                'reply_content': self.reply_content}
