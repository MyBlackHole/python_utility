#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          KeywordService
   Description:
   Author:             Black Hole
   date:               2020/9/18
-------------------------------------------------
   Change Activity:    2020/9/18:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re

import jieba
import jieba.analyse
from loguru import logger


# 12月2日
# def parse_md5(blog: Blog, task):
#     try:
#         md5_entity = MD5Entity()
#         if not str_is_none(blog.quoteID):
#             qid_md5 = get_md5(blog.quoteID)
#             md5_entity.qblogidMd5 = qid_md5
#             mc = re.findall('#[^#]+#', blog.quote)
#             for mtc in mc:
#                 top_md5 = get_md5(mtc)
#                 md5_entity.topicNameMD5.append((top_md5))
#             mc = re.findall('http://t.cn/[a-zA-Z0-9_]+', blog.quote)
#             for mtc in mc:
#                 qshorturl = ShortUrlEntity()
#                 shor_url_md5 = mtc
#                 if task.site == 1:
#                     try:
#                         if shor_url_md5 not in task.weibo_short:
#                             task.weibo_short.append(shor_url_md5)
#                         qshorturl.shortUrl = shor_url_md5
#                         blog.qshortUrlInfo.append((qshorturl))
#                     except Exception as e:
#                         logger.exception(e)
#         else:
#             md5_entity.qblogidMd5 = ''
#         m_coll = re.findall('#[^#]+#', blog.content)
#         for mtc in m_coll:
#             mtc_b = json.dumps(mtc)
#             mtc = json.loads(mtc_b)
#             top_md5 = get_md5(mtc)
#             md5_entity.topicNameMD5.append(top_md5)
#         m_coll = re.findall('http://t.cn/[a-zA-Z0-9_]+', blog.content)
#         for mtc in m_coll:
#             short_url = ShortUrlEntity()
#             shor_url_md5 = mtc
#             if task.site == 1:
#                 try:
#                     if shor_url_md5 not in task.weibo_short:
#                         task.weibo_short.append(shor_url_md5)
#                     short_url.shortUrl = shor_url_md5
#                     blog.shortUrlInfo.append((short_url))
#                 except Exception as e:
#                     logger.debug(f"error: {e}")
#             md5_entity.shortUrlMD5.append(shor_url_md5)
#         blog.md5s = md5_entity
#
#     except Exception as e:
#         logger.debug(f"error: {e}")


def get_nick_name_by_index(text):
    names = ''
    try:
        mc = re.findall(r'@([\u4e00-\u9fa5\w\-]+)', text)
        for at_name in mc:
            names += at_name + ' '
        names = names.strip(' ')

    except Exception as e:
        logger.debug(f"error: {e}")

    return names


def jb_parse_keywords(count: int, text: str):
    return ' '.join(jieba.analyse.textrank(text, topK=count))


if __name__ == '__main__':
    text = """
    
5天前，河北大午农牧集团有限公司（下称“大午集团”）孙大午等人涉嫌寻衅滋事、破坏生产经营等违法犯罪，被公安机关凌晨突击带走，并查封公司所有账户。尽管未出具任何行政决议，两级政府工作组也在当天派工作组入驻，拿到人力和财务资料，目前全面进驻集团包括学校、医院在内的各子公司。

　　有律师认为，如果抓捕过程属实，表明公安机关力度很大、决心很大。知情人士指出，这与被大午称为“6.21事件”和“8.4事件”的土地纠纷有关，大午集团人员与国营保定农场人员因土地确认问题发生冲突，并迎来当地警方的强力介入，导致大午多名员工“被抓”。

　　据媒体报道，11月11日凌晨1点，6辆大巴车载着特警，带着冲锋枪、警犬和梯子，闯进大午集团的自建小区，带走了一批集团高管和子公司的领导，公司创始人及监事长孙大午也在其中。

　　上述警方通报显示，消息来源是高碑店市公安局。值得注意的是，大午集团的注册地是保定徐水区，这意味着此次行动是异地出警。此外，大午集团办公室人员向《华夏时报》记者证实，公司远在海南的总经理刘平，也在同一时间被带走。

　　上述公司员工告诉记者，11日中午保定市、徐水区两级政府领导和公司中层以上领导进行了一场会议，再次读了一遍上述警方通报，此外未对孙大午及其他高层被带走作出进一步说明，也没有其他行政决议；同时让公司维持正常经营，称政府工作组已经入驻，后续将由市级政府主导工作。

　　该人员还告诉记者，11日当天公司的所有银行账号被查封，工作组入驻后拿走了集团的人力和财务资料，且已经全面进驻包括学校、医院在内的各子公司。

　　中国政法大学疑难证据中心主任、北京市友邦律师事务所兼职律师吴丹红称，因为大午集团的财产几乎都被冻结，公司相关人士到律所咨询时，明确表示“可能拿不出多少费用打官司”。

　　北京市友邦律师事务所主任赵光认为，如果媒体报道的抓捕过程属实，说明这不是一般的抓捕行动，而是类似于抓捕严重暴力犯罪嫌疑人的力度、强度，表明公安机关力度很大、决心很大。

　　一位资深律师在接受《华夏时报》记者采访时称，警方查封企业银行账号应该是在企业存在等违法犯罪行为的情况下进行追赃使用的权力，目前孙大午等人涉及的两个罪名寻衅滋事和破坏生产经营，均不涉及财产问题，不应该查封公司账户。

　　他进一步表示，政府可以在企业出现了危机，无法维持经营的情况下提供帮助。一旦需要政府进行强制接管，也需要以行政决定为前提，当事企业依然享有申辩等法律救济的权利。当地政府工作组对大午集团的接管，至今没有公开由哪级政府人员构成，依据什么法律规定，涉嫌违反相关行政法律法规。

　　天眼查显示，大午集团创立于1996年，是河北省农业产业化经营重点龙头企业。创始人孙大午持有公司43.75%的股份，第二大股东是其子孙萌，同时也是公司的法人代表。大午集团对外投资企业28家，业务范围涵盖畜牧、种业、饲料、食品、酒店、金融、康养等多个领域。

　　大午集团位于在徐水城区西北部郊区，距离城区7公里，紧邻荣乌高速出口。园区内有多个厂区分散布局，每个厂区周围农田环绕，双向四车道的公路连接各个厂区，公路沿途有食品产业园、预料场、家禽研究院、畜牧公司、宠物食品场等多家子公司。

　　上述知情人士告诉记者，警方通报所指的“破坏生产经营”，应该与徐水国营农场土地纠纷有关。农场与大午集团相隔不远。保定市政府官网的一份资料显示，2015年时，国营保定农场共计拥有小麦、玉米播种面积1.2万亩。

　　大午集团官方微信公众号“大午采风”曾发文称，多年前，郎五庄村曾将740亩土地交由徐水国营农场耕种。但实际上，徐水国营农场占用郎五庄村土地至少2000亩。后来，郎五庄村将土地租给了大午种业公司。

　　今年6月21日，大午集团人员与国营保定农场人员曾因土地确认问题发生冲突。今年8月4日凌晨，双方再次发生冲突，徐水国营农场人员开着挖掘机、吊车，偷拆大午集团农业公司的办公室，双方发生冲突并迎来当地警方的强力介入，大午集团20多名员工因此受伤，39名员工“被抓”。之后，大午集团召开“把屈辱说给家人听——84磨难记”，以此指控“非法拘禁”。这两次事件被大午称为“6.21事件”和“8.4事件”。

　　该次冲突以何种方式结束，目前尚未公开消息。据知情人士透露，孙大午秉性执着，少与政府之间沟通，倾向于按照法律和经济规律来兴办企业，在当地并不受待见。“经常会请来知名法学家、经济学家为大午集团开讲座，多次批评糟糕的营商环境。”

　　据公开资料显示，民营企业大午集团从养1000只鸡、50头猪起步，发展到员工9000余人，学校师生上万人。2013年年底，孙大午还曾入选“2013时代人物第四届中国绅士榜”。

　　大午集团在发展过程中一波三折并伴随争议。值得注意的是，孙大午已经不是第一次被警方带走。消息称，自2000年1月至2003年5月间，孙大午以高于银行同期存款利率、承诺不交利息税等方式，向社会吸收共计1308万元存款。2003年，他以涉嫌非法集资被徐水县门拘捕，一度引起各方面关注。最终被当地法院以非法吸收公众存款罪判处有期徒刑3年，缓刑4年，处罚金10万元。大午集团也被判处罚金30万元。

　　但孙大午案在当时引起了极大的争议。不少企业家认为，孙大午案件的根源在于僵化的融资体制。对于像孙大午案涉及的“草根金融”，真正可行的选择是疏导和管理，而不是简单地堵。不能因为金融有风险就把民间金融一棍子打死，就堵塞中小企业民间融资的渠道。

    """
    print(jb_parse_keywords(10, text), 1)
