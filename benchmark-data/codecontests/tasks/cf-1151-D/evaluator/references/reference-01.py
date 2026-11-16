# Why do we fall ? So we can learn to pick ourselves up.
t = int(input())
ss = []
for _ in range(0,t):
    a,b = map(int,input().split())
    ss.append([b-a,a,b])
ss = sorted(ss)
s = 0
for i in range(1,t+1):
    s += ss[i-1][1]*(i-1)+ss[i-1][2]*(t-i)
print(s)