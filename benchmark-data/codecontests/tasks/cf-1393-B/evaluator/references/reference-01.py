import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int,input().split()))
u = [0]*int(1e5+1)
for i in a:
    u[i] += 1
can1 = 0
can2 = 0
for i in u:
    can1 += i//4
    can2 += i%4//2
q = int(input())
for i in range(q):
    p, x = map(str,input().split())
    x = int(x)
    if p == "+":
        u[x] += 1
        if u[x] % 4 == 0:
            can1 += 1
            can2 -= 1
        elif u[x] % 4 == 2:
            can2 += 1
    else:
        u[x] -= 1
        if u[x] % 4 == 3:
            can1 -= 1
            can2 += 1
        elif u[x] % 4 == 1:
            can2 -= 1
    # print(can1)
    # print(can2)
    if can1 >= 2 or (can1 == 1 and can2 >= 2):
        print("YES")
    else:
        print("NO")






