from fractions import Fraction

# 运算符元组
OPERATORS = ('+', '-', '*', '/', '(', ')')
# 优先级字典
PRIORITY = dict([
    ('+', 1),
    ('-', 1),
    ('*', 2),
    ('/', 2)
])


def pop_left_bracket(postfix, operators):
    """依次弹栈并追加到后缀表达式，直到遇到左括号为止。"""
    while operators:
        operator = operators.pop()
        if operator == '(':
            break
        else:
            postfix.append(operator)


def compare_and_pop(i, postfix, operators):
    """比较优先级并进行相应操作。"""
    if len(operators) == 0:
        operators.append(i)
        return
    while operators:
        operator = operators.pop()
        if operator == '(':
            operators += ['(', i]
            return
        elif PRIORITY[i] > PRIORITY[operator]:
            operators += [operator, i]
            return
        else:
            postfix.append(operator)
    operators.append(i)


def pop_rest(postfix, operators):
    """弹出所有剩余的运算符，追加到后缀表达式。"""
    while operators:
        postfix.append(operators.pop())


def valid_infix(infix):
    pass


def is_number(text):
    """判断字符串是否为整数或者浮点数。"""
    try:
        return int(text)
    except:
        try:
            return float(text)
        except:
            return None


def infix_to_postfix(infix):
    """将中缀表达式转换为后缀表达式。"""
    infix = infix.split()
    postfix = []
    operators = []

    # TODO jpch89: 检查中缀表达式合法性
    # if not valid_infix(infix):
    #     return None

    for i in infix:
        if is_number(i):
            postfix.append(i)
        elif i in OPERATORS:
            if i == '(':
                operators.append(i)
            elif i == ')':
                pop_left_bracket(postfix, operators)
            else:
                compare_and_pop(i, postfix, operators)

    pop_rest(postfix, operators)

    return postfix

def fraction_cal(i, left, right):
    if (i == '+'):
        return str(Fraction(left) + Fraction(right))
    if (i == '-'):
        return str(Fraction(left) - Fraction(right))
    if (i == '*'):
        return str(Fraction(left) * Fraction(right))
    if (i == '/'):
        return str(Fraction(left) / Fraction(right))



def calc_postfix(postfix):
    """计算后缀表达式的值。"""
    operands = []

    for i in postfix:
        if is_number(i):
            operands.append(i)
        else:
            right = operands.pop()
            left = operands.pop()
            operands.append(fraction_cal(i, left, right))
            # operands.append(str(eval(left + i + right)))

    try:
        return eval(operands[0])
    except ValueError:
        return eval(operands[0])

def getAnswer(infix):
    postfix = infix_to_postfix(infix)
    result = calc_postfix(postfix)
    return result

# def main():
#     infix = input('输入算式(请用空格分隔数字/运算符/括号)：')

#     postfix = infix_to_postfix(infix)
#     if postfix is not None:
#         print('后缀表达式为：%s' % ' '.join(postfix))
#     else:
#         print('不合法的算式！')
#         exit()

#     result = calc_postfix(postfix)
#     print('计算结果为：%s' % result)


# if __name__ == '__main__':
#     main()

