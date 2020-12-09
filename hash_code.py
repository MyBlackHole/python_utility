#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          save_to_data
   Description:
   Author:             Black Hole
   date:               2020/9/29
-------------------------------------------------
   Change Activity:    2020/9/29:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import hashlib
import json
import uuid

import jieba.posseg
from loguru import logger
from opencc import opencc


def get_uuid3(_str: str) -> str:
    """
    获取某关键字为基础的 uuid3
    """
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, _str)).replace("-", "")


def is_chinese(title):
    """
    检查标题是否包含中文
    :param title: 需要检查的字符串
    :return: bool
    """
    for ch in title:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def hash_title(title):
    """
        对标题进行哈希
        :param title:
        :return:
        """
    # title没有包含中文时直接hash
    if not is_chinese(title):
        title = title.strip('\r\n')  # 清除换行符
        cypher_text = hashlib.md5()
        cypher_text.update(title.encode())
        hash2 = cypher_text.hexdigest()
        return hash2

    # 转为简体
    c = opencc.OpenCC('t2s')
    title = c.convert(title)

    title = re.sub(r"\((.*?)\)|(（.*?）)|(\{.*?\})|(\[.*?\])|(【.*?】)", "", title)  # 清除括号及里面的内容
    title = re.sub(
        r"(\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月|\d{1,2}月\d{1,2}日|\d{1,4}年|\d{4}/\d{1,2}/\d{1,2}|\d{4}/\d{1,2}|\d{4}.\d{1,2}.\d{1,2}|\d{4}.\d{1,2}|\d{4}-\d{1,2}-\d{1,2}|\d{4}-\d{1,2}|\d{1,2}日|\d{1,4})(\s\d{1,2}:\d{1,2}|)",
        "", title)  # 清除日期时间
    title = re.sub(r'(https?://|ftp://|file://|www\.)[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '',
                   title)  # 清除url
    title = re.sub(r"[ \[\]^_*×―－()（）$%~!@#…&￥—+=<>《》！?？:：•`·、。，；,.;\"‘’“”-]", '', title)  # 清除标点和空格、tab
    title = title.strip('\r\n')  # 清除换行符

    if len(title) <= 8:
        # 处理后title长度小于等于8时不使用分词
        res = title
    else:
        # 结巴分词
        res = ''
        words = jieba.posseg.cut(title, HMM=False)

        for kw in words:
            # if kw.flag != 'mq' and kw.flag != 'a' and kw.flag != 'd' and kw.flag != 'p':
            # 去掉 d 副词, mq 数量词, a 形容词, p 介词
            if kw.flag not in ['mq', 'a', 'd', 'p']:
                if len(kw.word) > 1:
                    res += kw.word
        # 分词后为空时则使用分词之前的title
        if res == '':
            res = title

    cypher_text = hashlib.md5()
    try:
        cypher_text.update(res.encode())
        hash2 = cypher_text.hexdigest()
        return hash2
    except Exception as e:
        logger.exception(f" error:{e} ")


def weibo_hash_code(content):
    content = filter_content(content)
    if len(content) > 15:
        content = content[:14]
    md5 = hashlib.md5()
    if content:
        try:
            b = json.dumps(content)
            content = json.loads(b)
            md5.update(content.encode())
        except Exception as e:
            logger.exception(f" error:{e} ")
    return md5.hexdigest()


def filter_content(content: str) -> str:
    # 清除url
    content = re.sub(r'(https?://|ftp://|file://|www\.)[-A-Za-z0-9+&@#/%?=~_|!:,.; ]+[-A-Za-z0-9+&@#/%=~_|]', '',
                     content)
    # 去掉话题 ---- ##
    content = re.sub(r'#.*?#', '', content)

    # 移除中括号及其内容(大几率是表情) - --- []
    content = re.sub(r'\[.*?\]', '', content)

    # 去掉括号及其内容 ---- () （） 【】
    content = re.sub(r'【.*?】|\(.*?\)|（.*?）', '', content)

    # 移除特殊字符 ---- ...全文：
    content = re.sub(r"\.\.\.全文：", '', content)

    # 清除博文中@的人：
    # # a. "回复@.*?:"
    content = re.sub(r"回复@.*?:|回复@.*?：", '', content)

    # # b. "//@.*?:"
    content = re.sub(r"//@.*?:|//@.*?：", '', content)

    # # c. "@.*?:"
    content = re.sub(r"@.*?:|@.*?：", '', content)

    # # d. "@.*?\\s"
    content = re.sub(r"@.*?\s", '', content)

    # # d. "@.*?\\s"
    content = re.sub(r"@.*?\s", '', content)

    # 清除标点和空格、tab
    content = re.sub(r"[ \[\]^\-_*×―－()（）$%~!！@#…&￥—+=<>《》?？:：•`·、。，；,.;\"‘’“”-]", '',
                     content)
    return content


if __name__ == "__main__":
    test_title = "(.*?)（.*?）{.dfk*?}[.*?]【.*?】"
    text = f"""\u003cp>\u003cstrong>\u003cimg src=\"https://x0.ifengimg.com/res/2020/B242CB0FC2609B82826B76E125C5AEA350
89F0B5_size252_w799_h555.png\" />\u003c/strong>\u003c/p>\u003cp>截至26日零时，韩国今年秋季接种流感疫苗后死亡的人数已经增
至59人，台湾地区也报道51例接种疫苗后出现的不良反应，案例中就有与韩国接种后出现死亡的疫苗同款。对此，台湾卫生福利主管部门负责人陈时中草草回应，台
湾疫苗不良反应报告并未异常，没有考虑停打，岛内网友痛批“冷血官僚”“请陈时中带头吃美猪与施打赛诺菲疫苗”！\u003c/p>\u003cp>据台湾联合新闻网报道，
台湾台中市51岁男子于10月10日打了流感疫苗10天后，出现急性多发性神经炎（GBS格林巴利症候群）病危，而这名男子与日前传出疑似流感疫苗致心肌炎不良反应个
案都是打了赛诺菲疫苗。截至目前，台湾已经出现51例接种疫苗后出现的不良反应，有12例属严重不良反应。\u003c/p>\u003cp>值得一提的是，韩国免费接种计
划采用的流感疫苗由五家制药企业供应，分别为法国赛诺菲集团、本土的GC制药公司、SK生物科技、一洋药品公司以及英国葛兰素史克公司。新加坡卫生部门25日深夜
发布声明说，新加坡已暂停使用韩国采用的两款流感疫苗，其中就包括赛诺菲生产的VaxigripTetra流感疫苗。\u003c/p>\u003cp>然而，台湾防疫部门发言人庄
人祥宣称，新加坡决定停打相关疫苗，原因尚待与新加坡确认，目前台湾没有考虑停打。陈时中竟回应台湾的流感疫苗不良反应报告比韩国少很多，并未证实韩国死亡
事件的直接原因是接种流感疫苗。“最近传出这一例，则要先看医院处理的状况，已请医院提出报告。”针对疫苗，陈时中仅草草一句带过：“请赛诺菲回应各地相关的
不良反应。”\u003c/p>\u003cp>\u003cimg class=\"empty_bg\" data-lazyload=\"https://x0.ifengimg.com/res/2020/A38C29D09F2FB5D
DD06534AAC446EE14ECD2D7EE_size73_w686_h332.png\" src=\"data:image/gif;base64,R0lGODlhAQABAIAAAP\" style=\"background-co
lor:#f2f2f2;padding-top:48.39650145772595%;\" />\u003c/p>\u003cp>岛内网友评论截图\u003c/p>\u003cp>“只是收集？还不先暂停施打？要
等更多人出现问题吗？”岛内民众怒斥：“冷血官僚！”“请陈时中带头吃美猪与施打赛诺菲疫苗！”“这种阿Q心态，会不会太夸张了！”“叫别人（赛诺菲）回应，你自
己不会去查吗？”“新加坡：与死亡无关，停用；台湾：与死亡无关，继续！你选择哪一个？”\u003c/p>"""
    text = text.encode().decode()
    import re

    # p = re.findall(r'(<img.*?/>)', text, re.DOTALL)
    # text = re.search(r'(<img.*/>)', text, re.DOTALL)
    s = re.compile(r'(<img.*?/>)', re.DOTALL)
    text = re.sub(s, '', text)
    text = re.sub(r'(<.*?>)', '', text)
    # for i in p:
    #     text = re.sub(i, '', text, re.DOTALL)
    # text = re.sub(r'</p><p>(.*?)</p><p>', '', text, re.DOTALL)
    print(text)
    # print(text[:14])
    # print(filter_content(text))
