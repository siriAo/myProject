# _*_ coding : utf-8 _*_
# @Time : 2022-10-16 22:19
# @Author : Ao_Jiao
# @File : comment
# @Project : myProject
class Comment:
    def __init__(self, bid: str, text: str, like_count: int, created_at: str, source: str):
        self.bid = bid
        self.text = text
        self.like_count = like_count
        self.created_at = created_at
        self.source = source

    def toMongo(self) -> dict:
        return {'bid': self.bid,
                'text': self.text,
                'like_count': self.like_count,
                'created_at': self.created_at,
                'source': self.source
                }
