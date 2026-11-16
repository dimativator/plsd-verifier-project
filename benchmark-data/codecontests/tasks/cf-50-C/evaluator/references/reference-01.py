import math

n = int(input())

l = []
for i in range(n):
    l.append(tuple(list(map(int, input().split(" ")))))
l = list(set(l))
n = len(l)

pmin = 0
for i in range(1, n):
    if(l[i][1] < l[pmin][1] or (l[i][1] == l[pmin][1] and l[i][0] < l[pmin][0])):
        pmin = i

l[pmin], l[0] = l[0], l[pmin]

def orientation(p0, p1, p2):
    x = (p1[1] - p0[1]) * (p2[0] - p1[0]) - (p1[0] - p0[0]) * (p2[1] - p1[1])
    if(x < 0):
        return -1
    if(x > 0):
        return 1
    return 0

l = [(p[0] - l[0][0], p[1] - l[0][1]) for p in l[1:]]
l.sort(key = lambda p: (-p[0]/p[1] if(p[1] != 0) else -10e14, p[0] ** 2 + p[1] ** 2))
l = [(0, 0)] + l

t = [l[0]]
i = 1
n = len(l)
while(1):
    while(i < n - 1 and orientation(l[0], l[i], l[i + 1]) == 0):
        i += 1
    if(i >= n - 1):
        break
    t.append(l[i])
    i += 1
    
t.append(l[-1])

if(len(t) == 1):
    print(4)
elif(len(t) == 2):
    print(max(abs(t[1][1] - t[0][1]), abs(t[1][0] - t[0][0])) * 2 + 4)
else:
    stack = [t[0], t[1], t[2]]
    for i in range(3, len(t)):
        while(orientation(stack[-2], stack[-1], t[i]) == 1):
            stack.pop()
        stack.append(t[i])
    
    n = len(stack)
    s = 4
    for i in range(n - 1):
        s += max(abs(stack[i + 1][1] - stack[i][1]), abs(stack[i + 1][0] - stack[i][0]))
    s += max(abs(stack[0][1] - stack[n - 1][1]), abs(stack[0][0] - stack[n - 1][0]))
    print(s)