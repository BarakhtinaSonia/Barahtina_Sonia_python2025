def is_correct_brackets(s):
    stack = []
    for i in s:
        if i == '(':
            stack.append(i)
        elif i == ')':
            if len(stack) == 0:
                return False
            else: stack.pop()

s = input()
print(is_correct_brackets(s))