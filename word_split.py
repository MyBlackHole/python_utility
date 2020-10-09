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
    print(Parse("(青岛|市南区|市北区|李沧|崂山|城阳|西海岸新区|黄岛|即墨|平度|莱西|胶州)"
                "+(劳动仲裁|劳动监察|劳动人事争议仲裁|劳动合同|解除合同|欠薪|欠保|讨薪|最低工资|加班费|加班工资|工资|强制加班|高温费|高温补贴|年休假|非法用工|年假|病假|欠费)"))
    '((拖欠|不发)+(工资|薪水|劳动报酬|社保))|辅警|((公司|单位)+押金)|劳动部门|劳动局|工资指导线|工资指导价位|(欠缴+(养老|社保))|山东企业复工|人力资源社会保障|人社)'
