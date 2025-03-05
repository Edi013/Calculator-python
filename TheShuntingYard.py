from collections import deque
import re


class Operator:
    def __init__(self, precedence, arguments):
        self.precedence = precedence
        self.arguments = arguments


OPERATORS = {
    '+': Operator(2, 2),
    '-': Operator(1, 2),
    '*': Operator(3, 2),
    '/': Operator(4, 2),
    '^': Operator(5, 2)  # Added power operator
}


def tokenize(expression):
    tokens = re.findall(r'\d+|[-+*/^()]', expression)
    return tokens


def shunting_yard(expression):
    output = []
    operators = deque()
    tokens = tokenize(expression)

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in OPERATORS:
            while (operators and operators[0] in OPERATORS and
                   OPERATORS[operators[0]].precedence >= OPERATORS[token].precedence):
                output.append(operators.popleft())
            operators.appendleft(token)
        elif token == '(':
            operators.appendleft(token)
        elif token == ')':
            while operators and operators[0] != '(':
                output.append(operators.popleft())
            operators.popleft()

    while operators:
        output.append(operators.popleft())

    return output


def evaluate_rpn(rpn_expression):
    stack = deque()

    for token in rpn_expression:
        if token.isdigit():
            stack.append(float(token))
        elif token in OPERATORS:
            b = stack.pop()
            a = stack.pop() if OPERATORS[token].arguments == 2 else 0
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '^':
                result = a ** b  # Power operator
            stack.append(result)

    return stack.pop()


def evaluate_expression(expression):
    rpn = shunting_yard(expression)
    return evaluate_rpn(rpn)
