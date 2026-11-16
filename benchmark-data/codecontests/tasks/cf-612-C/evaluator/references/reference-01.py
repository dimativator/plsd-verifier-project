s = input()

stack = []
res = 0
for c in s:
    if c in '(<[{':
        stack.append(c)
    else:
        if not stack:
            print('Impossible')
            break
        last = stack.pop()
        if last + c not in ('[]', '()', '<>', '{}'):
            res += 1
else:
    if stack:
        print('Impossible')
    else:
        print(res)
