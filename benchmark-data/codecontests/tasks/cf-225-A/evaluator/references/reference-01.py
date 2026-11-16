q=int(input())
w=int(input())
k=0
for i in range(q):
    e=list(map(int,input().split()))
    if (w in e) or ((7-w) in e):
        print('NO')
        k=1
        break
if k==0:
    print('YES')