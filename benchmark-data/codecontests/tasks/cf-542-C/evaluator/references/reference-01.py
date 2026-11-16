from random import randint
from copy import deepcopy

n = int(input())
a = list(map(int, input().split()))
for i in range(n):
    a[i] -= 1

def gen(n):
    a = []
    for i in range(n):
        a.append(randint(0, n - 1))
    return a

def stupid(a, v=False):
    n = len(a)
    init = [a[i] for i in range(n)]
        
    k = 1
    good = False
    while not good:
        good = True
        if v:
            print(a)
        for i in range(n):
            if a[a[i]] != a[i]:
                good = False
        if good:
            break
        k += 1
        b = [0 for i in range(n)]
        for i in range(n):
            b[i] = init[a[i]]

        a = [b[i] for i in range(n)]

    return k

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def get_lcm(a, b):
    return a * b // gcd(a, b)

def solve(a, v=False):
    n = len(a)
    d = [0 for i in range(n)]
    on_cycle = [False for i in range(n)]
    cycle_length = [0 for i in range(n)]
    until = [0 for i in range(n)]
    to_len = [0 for i in range(n)]

    for i in range(n):
        if a[i] == i:
            on_cycle[i] = True
            cycle_length[i] = 1
            continue
        cur = i
        cnt = 1
        for j in range(3 * n):
            cur = a[cur]
            cnt += cur == i
        on_cycle[i] = cnt > 1

        if on_cycle[i]:
            cur = i
            steps = 0
            for j in range(3 * n):
                cur = a[cur]
                steps += 1
                if cur == i:
                    break
            cycle_length[i] = steps


    for i in range(n):
        if not on_cycle[i]:
            cur = i
            steps = 0
            for j in range(n + 1):
                cur = a[cur]
                steps += 1
                if on_cycle[cur]:
                    break
            until[i] = steps
            to_len[i] = cycle_length[cur]

    if v:
        print('cycle', cycle_length)
        print('until', until)
    lcm = 1
    low = 0
    for i in range(n):
        if on_cycle[i]:
            lcm = get_lcm(lcm, cycle_length[i])
        else:
            low = max(low, until[i])
            continue
            to = to_len[i]
            p = until[i]
            
            if p % to:
                p = ((p // to) + 1) * to
            low = max(low, p)
            if v:
                print(i, p, to)
    ans = lcm
    while ans < low:
        ans += lcm
    return ans

print(solve(a))
while False:
    a = gen(randint(1, 15))
    print(a)
    print(stupid(deepcopy(a)))
    print(solve(deepcopy(a)))
    assert(stupid(deepcopy(a)) == solve(deepcopy(a)))
