class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


def ListAnd(b, e):
    _list = []
    for b_str in b:
        for e_str in e:
            _list.append(b_str + "+" + e_str)
    return _list


def ListOr(b, e):
    _list = []
    for b_str in b:
        _list.append(b_str)
    for e_str in e:
        _list.append(e_str)
    return _list


def Operation(b, e, per):
    if per == '+':
        return ListAnd(b, e)
    else:
        return ListOr(b, e)


def Parse(formula):
    formula = formula.replace("（", "(").replace("）", ")").replace("||", "|")
    stack = Stack()
    # items=[]
    i = 0
    for i in range(0, len(formula)):
        c = formula[i]
        if c == '(':
            # items.append("(")
            stack.push("(")
        elif c == ')':
            stack.pop()
            # items.pop()
        elif c == '+':
            if stack.size() == 0:
                i = i - 1
                break
        elif c == '|':
            if stack.size() == 0:
                i = i - 1
                break
    i = i + 1
    if i != 0 and i < len(formula):
        b = formula[0: i].strip()
        if b is not None and b != "" and b[0] == '(' and b[len(b) - 1] == ')':
            b = b[1:len(b) - 1]
        format_before = Parse(b)
        e = formula[i + 1:len(formula)].strip()
        format_last = Parse(e)
        return Operation(format_before, format_last, formula[i])
    else:
        b = formula
        if b is not None and b != "" and b[0] == '(' and b[len(b) - 1] == ')':
            b = b[1: len(b) - 1].strip()
            return Parse(b)
        else:
            _list = [formula]
            return _list


if __name__ == "__main__":
    print(Parse("(济南|青岛|淄博|枣庄|东营|烟台|潍坊|济宁|泰安|威海|日照||滨州|德州|聊城|临沂|菏泽)+(中毒|[集体腹泻]|非法|维权|上访"
                "|[黑作坊]|[保护伞]|[黑势力]|[钓鱼执法]|[群死群伤]|自焚|水灾|洪水|抢劫|强奸|偷拍|[咸猪手]|[黑中介]|臭水|塌方|坍塌"
                "|倒塌|酒驾|醉驾|撞人|撞死|滥用|违规|违法|[垃圾填埋]|杀人|诈骗|跑路|老赖|贪污|腐败|[环保督查组]|[环保督察组]|"
                "环境污染|雾霾|(污水+(偷排|违规|违排|排放))|[脏乱差]|[臭气熏天]|辱骂|打砸|死亡|死人|爆炸|泄漏|强拆|强征|[暴力拆迁]|"
                "[强行征地]|[暴力执法]|质问|[省长的一封信]|[书记的一封信]|[帮帮我们]|[给我们做主]|传染|(透析+感染)|[医疗事故]|毁坏|"
                "虐童|虐待|乱停乱放|垮塌|扰民|[野蛮拆迁]|[交警钓鱼]|[钓鱼执法]|偷排|宰客|闹事|[领导无能]|侵占|[挪用公款]|行骗|恐吓|"
                "抗议|[作风问题]|[不正当关系]|霸凌|体罚|爆雷|[暴力执法]|[执法不严]|传销|扰乱|受骗|坠河|跳河|破坏设施|破坏环境|"
                "[生态环境恶化]|顶风作案|欠薪|[资金周转问题]|拖欠|黑名单|[城管打人]|[警察打人]|[公务员打人]|医闹|[大操大办]|嫖娼|"
                "吸毒|贩毒|枉法|一手遮天|黑幕|潜规则|肮脏|篡改|血汗钱|[不文明执法]|推搡|鬼城|经济下滑|[经济增长缓慢]|[GDP下滑]|"
                "[GDP造假]|浪费资源|[走下神坛]|[跌落神坛]|[跌下神坛]|[应急管理部]|[生态环境部]|[环保督察组]|[环保督查组]|"
                "[以租代售]|[炒房]|死鱼|死虾|[重大车祸]|[特大车祸]|[连环车祸]|涉黑|拆霸|楼霸|涉贪|揭发|渎职|买官|卖官|[贪赃枉法]"
                "|贪官|罢免|撤职|贬职|职务之便|黑手|公款吃喝|结党|营私|[拉帮结派]|猖獗|[开除党籍]|官匪勾结|恶政|政腐|暴政|纵容|"
                "包庇|不作为|霸占|撞死|警匪勾结|羁押|逼供|用刑|打压|扣留|毒打|恶警|袭民|[粗暴执法]|[暴力执法]|庇护|[恶警袭民]|腐败|"
                "[执法黑暗]|[官商勾结]|官官相护|以权谋私|为所欲为|恶行|封堵|纠纷|打砸|索贿|突击提拨|贿选|徇私舞弊|腐化|[土地执法]|"
                "[官民对峙]|民怨|官官相为|领导无能|受贿|包庇|巨贪|私吞|侵吞)"))
