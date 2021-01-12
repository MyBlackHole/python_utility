#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          文本处理
   Description:
   Author:             Black Hole
   date:               2020/10/9
-------------------------------------------------
   Change Activity:    2020/10/9:
-------------------------------------------------
"""


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
    print(Parse("毒品|暴动|暴乱|爆炸|绑架|逼供|惨案|藏独|持械|冲突|刺杀|篡改|错案|打砸|弹药|恶势力|犯法|犯罪|攻击|拐卖|黑社会|黑势力|击毙|极端组织|极端分子|挟持|戒严|聚众|枪支|开枪|枪击|砍人|砍死|抗法|抗议|恐怖|恐慌|扣押|狂殴|滥用|勒索|轮奸|裸死|灭口|命案|谋杀|闹访|闹事|虐童|潜逃|欠薪|讨薪|强暴|强拆|强盗|强奸|强征|抢劫|侵吞|囚禁|群架|群殴|人命|杀人|烧毁|烧杀|涉黑|涉黄|身亡|施暴|示威|死伤|死亡|讨薪|讨债|跳河|跳楼|维权|外逃|枉法|围攻|围殴|武力|袭击|泄密|刑讯|血案|医闹|用刑|游行|冤|致残|抓获|追诉|坠楼|自焚|自杀|纵火|走私|截访|民愤|上访|((集体|群体|非法)+(游行|讨薪|集会|散步|上访|中毒|绝食|抗议|停工|停运|打砸|堵路|示威))|PX项目|罢工|罢市|罢课|摆花圈"))
