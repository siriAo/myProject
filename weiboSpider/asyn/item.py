# _*_ coding : utf-8 _*_
# @Time : 2022-10-11 19:19
# @Author : Ao_Jiao
# @File : item
# @Project : myProject
from weiboSpider.asyn.user import User
from weiboSpider.asyn.comment import Comment


class Item:
    def __init__(self, text: str, created_at: str,
                 status_city: str, status_province: str, status_country: str,
                 user: User, *, topic_list: [str] or None, bid: str, comments: [Comment]):
        self.text = text
        self.created_at = created_at
        self.status_city = status_city
        self.status_province = status_province
        self.status_country = status_country
        self.user = user
        self.topic_list = topic_list
        self.bid = bid
        self.comments = comments
        if comments:
            self.comments_count = len(self.comments)
        else:
            self.comments_count = 0

    def toMongo(self) -> dict:
        return {'bid': self.bid,
                'topic': self.topic_list,
                'text': self.text,
                'created_at': self.created_at,
                'status_city': self.status_city,
                'status_province': self.status_province,
                'status_country': self.status_country,
                'user': self.user.toMongo(),
                'comments_count': self.comments_count,
                'comments': self.commentstoMongo()
                }

    def commentstoMongo(self) -> [dict]:
        if self.comments:
            return [comment.toMongo() for comment in self.comments]
        else:
            return None
