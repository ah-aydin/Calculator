class Stack():
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0

def getPriority(item):
    if item in ['+', '-']:
        return 1
    return 2

def infixToPostfix(arr):
    operatorStack = Stack()
    postfix_arr = []

    for elem in arr:
        if elem in ['+', '-', '*', '/']:
            priority_elem = getPriority(elem)
            priority_top = 100
            while priority_top > priority_elem and not operatorStack.empty():
                priority_top = getPriority(operatorStack.top())
                if priority_elem < priority_top:
                    postfix_arr.append(operatorStack.pop())
                if priority_elem == priority_top:
                    postfix_arr.append(operatorStack.pop())
            operatorStack.push(elem)
            continue
        postfix_arr.append(float(elem))

    while not operatorStack.empty():
        postfix_arr.append(operatorStack.pop())

    return postfix_arr

def solvePostfix(postfix_arr):
    stack = Stack()
    for elem in postfix_arr:
        if elem in ['+', '-', '*', '/']:
            second = stack.pop()
            first = stack.pop()
            if elem == '+':
                stack.push(first + second)
            if elem == '-':
                stack.push(first - second)
            if elem == '*':
                stack.push(first * second)
            if elem == '/':
                stack.push(first / second)
            continue
        stack.push(elem)
    return stack.pop()

def solve(arr):
    return solvePostfix(infixToPostfix(arr))
