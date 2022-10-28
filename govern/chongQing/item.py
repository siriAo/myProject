# _*_ coding : utf-8 _*_
# @Time : 2022-09-20 13:04
# @Author : Ao_Jiao
# @File : Item
# @Project : myProject
class Item:
    def __init__(self, workOrderTitle, workOrderContent, replyDate, replyContent):
        self.workOrderTitle = workOrderTitle
        self.workOrderContent = workOrderContent
        self.replyDate = replyDate
        self.replyContent = replyContent
