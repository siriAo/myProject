# _*_ coding : utf-8 _*_
# @Time : 2023-01-03 14:03
# @Author : Ao_Jiao
# @File : dataClean
# @Project : myProject

import re
from opencc import OpenCC


def is_chinese(uchar: str):
    if u'\u4e00' <= uchar <= u'\u9fa5':  # 判断一个uchar是否是汉字
        return True
    else:
        return False


def clear_character(sentence):
    pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^，^。^！^a-z^A-Z^0-9]")  # 只保留中英文、数字和符号，去掉其他东西
    # 若只保留中英文和数字，则替换为[^\u4e00-\u9fa5^a-z^A-Z^0-9]
    line = re.sub(pattern, '', sentence)  # 把文本中匹配到的字符替换成空字符
    new_sentence = ''.join(line.split())  # 去除空白
    return new_sentence


def simplified(sentence):
    new_sentence = OpenCC('t2s').convert(sentence)  # 繁体转为简体
    return new_sentence


def process(data):
    # 去除空格
    content1 = data.replace(' ', '')  # 去掉文本中的空格
    content2 = content1.replace('...', '，')  # 去掉文本中的省略号
    content3 = clear_character(content2)
    content4 = simplified(content3)
    return content4


if __name__ == "__main__":
    str_arr = ['   大家好， 欢迎一起来学习文本的空格   去除   ！',
               '   大家好， 这里还有  很多的知识...一起拉学习吧 ！',
               '1,2,3...我们开始吧， 加油！',
               '现在听着音乐,duo rui mi,很开心*_*',
               '你现在读的这里是简体，這裡是繁體，能看懂嗎？',
               '你好\n结婚']
    is_chinese('大')
    for contents in str_arr:
        print('处理前文本：' + contents)
        content = process(contents)
        print('处理后文本：' + content)
