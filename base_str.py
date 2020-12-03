#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_str
   Description:
   Author:             Black Hole
   date:               2020/11/25
-------------------------------------------------
   Change Activity:    2020/11/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re
from urllib.parse import urljoin

from loguru import logger


def key_split(_list: list, base_sep: str = '+', sep_list: list = [',', '+', ' ', '＋']) -> list:
    """
    分割字符串列表
    Args:
        _list: 数据源
        base_sep: 默认切换字符
        sep_list: 需要切分的字符列表
    Input: ['广州人社局+周江波＋贪污']
    Returns: ['广州人社局', '周江波', '贪污']
    Class: <class 'list'>
    """
    _list_all = []
    for i, item in enumerate(_list):
        for sep in sep_list:
            item = item.replace(sep, base_sep)
        _list_all.extend(item.split(base_sep))
    return _list_all


def clear_source(content_source: str, url: str, old_content) -> str:
    """
    对content进行格式化，方便阅读
    :param content_source: 需要处理的文本
    :param url:
    :param old_content:
    :return: str
    """
    try:
        if content_source:
            content_source = re.sub(r'[{}\[\]]', '', content_source)  # 清除{}[]符号
            content_source = re.sub('[.]', '#1', content_source)
            content_source = re.sub('[*]', '#2', content_source)
            content_source = re.sub('[?]', '#3', content_source)
            content_source = re.sub('[(]', '#4', content_source)
            content_source = re.sub('[)]', '#5', content_source)  # 替换有转义意义的字符，分别用不同值代替
            # 清楚script和style标签及里面的内容，前提需要将原文的换行符替换为空，并且将转义字符替换，才不会在替换过程报错
            clear_script = re.sub('<script.*?>.*?</script>|<style>.*?</style>', '', content_source.replace('\n', ''))
            p_contents = re.findall('<[pP].*?>.*?</[pP]>', clear_script)  # 寻找全部p标签
            texts = []
            for p in p_contents:  # 循环遍历，
                p_text = re.search('<[pP].*?>(.*?)</[pP]>', p).group(1).strip()  # 找到每个p标签里的内容，在前面添加四个空格作为新p，跟旧p替换
                new_p = re.sub(p_text, f'    {p_text}', p)
                texts.append([new_p, p])
            for new_p, old_p in texts:
                clear_script = re.sub(old_p, new_p, clear_script)  # 将旧p全部替换为新p
            sub_n = re.sub('<[pP].*?>|<br>', '\\n', clear_script)  # p标签和br标签替换为换行符
            sub_img = re.sub('<img', '%img', sub_n)  # 替换为%是为了防止下面的将全部<.*?>替换为空
            clear_tag = re.sub('<.*?>|&nbsp;', '', sub_img)
            content = re.sub('%img', '<img', clear_tag)  # 换回去
            content = re.sub('#1', '.', content)
            content = re.sub('#2', '*', content)
            content = re.sub('#3', '?', content)
            content = re.sub('#4', '(', content)
            content = re.sub('#5', ')', content)  # 换回原意
            src_list = re.findall('src="(.*?)"', content)
            my_list = [i for i in src_list if i != '']  # 清除列表有空字符串，防止下面替换过程中出现替换太多次的结果
            add_hrefs = []
            # 将相对路径替换为绝对路径
            for old_href in my_list:
                if not old_href.startswith('http'):
                    new_href = urljoin(url, old_href)
                    add_hrefs.append([new_href, old_href])
            for new_href, old_href in add_hrefs:
                content = re.sub(old_href, new_href, content)
            if content == '':  # 如果为空，则用原content
                content = old_content
        else:
            content = old_content
    except Exception as e:
        logger.info(f"error: {e}")
        content = old_content
    return content


if __name__ == '__main__':
    key_list = ['南京健康园门诊部+欺骗', '栖霞市妇幼保健院+作风', '奋发新青年+生物岛', '纪委 举报', '风波', '大宁县+骗贷', '中阳县+骗保', '击落', '万柏林区+知法犯法',
                '集贤+锁喉',
                '特朗普+6G+试验', '潞州区+群殴', '插队+大妈', '广州市人社+何士林＋徇私', '运城 大火', '广州市人力资源和社会保障局+干部＋腐败', '杨斌 腐败', '特朗普+回应+中方',
                '江苏+李云峰',
                '江苏+赵晶夫', '湖南+谭勇', '溺水+泳池+索赔', '山西+征地', '南国书香节+便利贴', '平遥 供热管道', '江苏省高淳监狱医院+忽悠', '南京京科皮肤病医院+索贿',
                '江宁县中医医院+收礼', '伤人',
                '汾阳+不正当关系', '广州人社+领导＋犯罪', '江苏+成玉祥', '江宁五洲医院+违纪', '忻州+代县+炸药', '尘肺+广州', '纪委 收入', '壶关县+官官相护', '荔湾+流氓',
                '香港+起火+餐厅',
                '中国人民解放军第四五四医院三甲医院+诈骗', '高淳县中医院+检举', '南京自然医学会和燕门诊部+检举', '广州市人社+领导＋上访访', '南京外滩门诊部+检举', '拐骗',
                '广州+新粤剧+粤剧的发展之路',
                '身亡+快递+回应', '天河+红军+小学', '援助湖北', '和顺县+贩卖枪支', '湖南+彭楠', '南京大桥四处职工医院+投诉', '南京铁医红山医院+受贿', '新会 新冠', '榆社+跳楼',
                '听证',
                '平遥 施工 坍塌 被埋', '江苏邮政老年康复中心+受贿', '六合区妇幼保健所+乱收费', '番禺区+2020年青蓝国际创新创业大赛', '中学', '老师', '缅甸掸邦小镇',
                '高淳县顾陇医院+检举', '学生 殴打',
                '南京市化学纤维厂职工医院+勾结', '补贴', '广州市人社+郭志勇＋冤案', '新会 睦洲镇', '广州+高级技工学校', '强行', '平鲁区+团伙作案', '尧都+矿事故空难事故',
                '杭州 分区 上城江干合并',
                '新会 草菅人命', '河津市+公款吃喝', '钟钢省', '榆社+环保督查', '江苏现代女子医疗保健院+勾结', '江宁县人民医院+索贿', '南京康爱医院+黑幕', '茂华万通源',
                '南京中南门诊部+揭发',
                '南京东院专科门诊部+诈骗', '扬郭医院+检举', '虐待+女子', '法官+详情+男子', '柳林县+选举黑幕', '双十一+广州', '旅游+投诉+垃圾+九寨沟+重建+瘫痪', '太原+城管+商贩',
                '太原 疑似',
                '致死', '新会 绑架', '致使', '霍州+公车私用', '江宁医院+欺骗', '扬子石油化工公司医院扬子医院+腐败', '白云+上课', '南京仁康增高诊疗研究中心+诈骗', '资源',
                '番禺+广州市芳村工人文化宫',
                '维护', '江苏+陈维健', '美国+特朗普+解雇', '美国+奥巴马+任职', '泥巴路', '承认+苹果+问题', '南京大学医学院第二附属医院+投诉', '待遇', '钟南山+妻子',
                '广州+尘肺病',
                '广州人社+李明华＋信访', '黑恶', '市北+体育测试', '刘明理', '南京市雨花台区口腔病防治所+受贿', '江苏现代女子医疗保健院+违纪', '文物保护', '南京扬子医院+诈骗',
                '隰县+暴力执法',
                '新绛县+倒塌', '妄为', '王维林', '南京华西妇科医院+揭发', '杭州 机场 收费 20', '平遥 施工 坍塌', '巴西进口牛肉', '萧山 收费',
                '旅游+投诉+垃圾+九寨沟+重建+铁路', '残忍',
                '高淳县中医院+勾结', '南京紫金医院+违纪', '阳曲县+坍塌', '共享单车', '丁真+签约+小伙', '江宁五洲医院+曝光', '朱东铁', '租客退租不成反被房东搬空+民警介入房东仍拒绝退租',
                '广州+楼宇评定+政府层面', '捉奸', '芮城县+劫持', '侯马市+杀人', '安全隐患丛生', '投掷+手榴弹+纪录', '杏花岭区+侵占', '南京市戒毒所+诈骗', '汾西+双开',
                '美国+相撞',
                '鸿运花园+电梯', '灵石县+逮捕', '福建+冷链+证明', '宁武县+严重事故', '江苏省中西医结合医院三甲医院+索贿', '郭敬明+朋友+diss', '广州市人力资源和社会保障局+官员＋接访',
                '中卫 扇耳光',
                '南京军区南京总医院+曝光', '六合区妇幼保健所+索贿', '浦口区中医院+揭发', '浦口区中心医院浦口监狱医院+作风', '31个省(自治区|直辖市) 病例', '运城+大火', '广州+刘茂建',
                '绝食', '潮南',
                '溧水县城西医院+投诉', '晋中 施工 被埋', '基金', '老街 摔', '江苏省南京监狱医院+欺骗', '江苏+王建平', '中医', '广州人社+何士林＋玩手机', '危机',
                '太钢原集体+职工信访',
                '太原 职工安置 不担当', '南京斯麦尔口腔门诊部+乱收费', '天津+核酸+阳性', '杨斌 贪腐', '钟南山+疫情+日程表', '不忘初心 主题教育活动', '南京现代长城皮肤病医院+违纪',
                '白市驿 交通事故',
                '涉嫖', '铁道部浦镇车辆厂职工医院+勾结', '一辆大货车和客车相撞', '退伍', '广州 支队长 死亡', '未来三年', '解雇+局长', '中毒', '国泰+学生', '山阴县+骗保',
                '南京市化学纤维厂职工医院+投诉', '临汾+蒲县+侵占', '武乡县+聚众滋事', '江宁县中医医院+忽悠', '夏县+山体崩塌', '江浦县人民医院+收礼', '模型', '放走+警方+人员',
                '平台+反垄断+指南+落实',
                '南京邦德骨科医院+腐败', '荔湾+工人运动', '大同+平城区+用刑', '晋城+裸官', '南京华诺口腔门诊部+曝光', '孟子义+回应+发文', '新壹站 跳楼', '武乡县+火灾',
                '溧水县中医院+违纪',
                '广州人社局+周江波＋贪污']
    key_list = ['广州人社局+周江波＋贪污']
    print(key_split(key_list))
