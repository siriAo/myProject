# _*_ coding : utf-8 _*_
# @Time : 2022-11-08 19:02
# @Author : Ao_Jiao
# @File : item
# @Project : myProject
import re


class Item:
    def __init__(self, title: str, content: str, dateline_txt: str, domainId: str, domainId_txt: str, queryCode: str,
                 typeId: str, typeId_txt: str):
        self.title = title  # 标题
        self.content = content  # 正文
        self.dateline_txt = dateline_txt  # 留言时间
        self.domainId = domainId  # 分类码
        self.domainId_txt = domainId_txt  # 问题分类（社会服务,公园、绿化广场管理问题等）
        self.queryCode = queryCode  # tid查询码
        self.typeId = typeId  # 留言类别码
        self.typeId_txt = typeId_txt  # 留言类别（问题反映,咨询等）
        self.asContent = None  # 回复内容
        self.organization = None  # 回复组织
        self.replydateline_txt = None  # 回复时间
        self.feedbackContent = None  # 题主追问
        self.feedbackCreateTime = None  # 追问时间

    def __str__(self):
        return 'title={}\ncontent={}\ndateline_txt={}\ndomainId_txt={}\nqueryCode={}\nasContent={}\norganization={}'.format(
            self.title, self.content, self.dateline_txt, self.domainId_txt, self.queryCode, self.asContent,
            self.organization)

    def update(self, asContent: str, organization: str, replydateline_txt: str, feedbackContent: str,
               feedbackCreateTime: str):
        self.asContent = asContent  # 回复内容
        self.organization = organization  # 回复组织
        self.replydateline_txt = replydateline_txt  # 回复时间
        self.feedbackContent = feedbackContent  # 题主追问
        self.feedbackCreateTime = feedbackCreateTime  # 追问时间

    def clean(self):
        if self.domainId == 'null':
            domainId = None
        if self.domainId_txt == 'null':
            domainId_txt = None
        if self.typeId == 'null':
            typeId = None
        if self.typeId_txt == 'null':
            typeId_txt = None
        if self.asContent == 'null':
            asContent = None
        if self.organization == 'null':
            organization = None
        if self.replydateline_txt == 'null':
            replydateline_txt = None
        if self.feedbackContent == 'null':
            feedbackContent = None
        if self.feedbackCreateTime == 'null':
            feedbackCreateTime = None

    def toMongo(self):
        return dict(title=self.title,
                    content=self.content,
                    dateline_txt=self.dateline_txt,
                    domainId=self.domainId,
                    domainId_txt=self.domainId_txt,
                    queryCode=self.queryCode,
                    typeId=self.typeId,
                    typeId_txt=self.typeId_txt,
                    asContent=self.asContent,
                    organization=self.organization,
                    replydateline_txt=self.replydateline_txt,
                    feedbackContent=self.feedbackContent,
                    feedbackCreateTime=self.feedbackCreateTime)
