import re

from loguru import logger

from utility.LongWeibo import long_weibo
from utility.MiniNetUtility import mininet
from utility.base import str_is_none


def parse_uid(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Host': 'weibo.com'
        }

        html = long_weibo.download_weibo(url, 'BaseConfig', need_cookies=True, headers=headers)
        if str_is_none(html):
            return None
        mtc = re.search(r"BaseConfig\['oid'\]='(\d+)'", html)
        check = re.search(r"BaseConfig\['onick'\]='欢迎新用户'", html)
        if mtc is None:
            return None
        elif check is None:
            return mtc.group(1)
    except Exception as e:
        logger.exception(e)


def getuid(url):
    uid = ''
    if str_is_none(url):
        return uid

    if 'weibo.com/u/' in url:
        mtc = re.search(r"weibo.com/u/(\d+)", url)
        if mtc is not None:
            uid = mtc.group(1)
        else:
            uid = parse_uid(url)
    else:
        url_split = url.split('/')
        if len(url_split) == 5 and url_split[3].isdigit():
            uid = url_split[3]
        else:
            uid = parse_uid(url)
            uid = uid if not str_is_none(uid) else ''
    return uid
