import hashlib
import re

import jieba.posseg
from loguru import logger
from opencc import opencc

from utility.filter import filter_content


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
            md5.update(content.encode())
        except Exception as e:
            logger.exception(f" error:{e} ")
    return md5.hexdigest()


if __name__ == "__main__":
    test_title = "(.*?)（.*?）{.dfk*?}[.*?]【.*?】"
    test_title = re.sub(r"\((.*?)\)|(（.*?）)|(\{.*?\})|(\[.*?\])|(【.*?】)", "", test_title)  # 清除括号及里面的内容
    print(test_title)
