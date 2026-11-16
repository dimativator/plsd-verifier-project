eps=10**(-9)
mn=10
mx=100000000
n=int(input())
arr=list(map(int,input().split()))
for i in range(n):
    mn = max(mn,(arr[i]*10)/(i+1))
    mx = min(mx,((arr[i]+1)*10)/(i+1))
ans1=((n+1)*mn)//10
ans2=((n+1)*(mx-eps))//10
if ans2>ans1:
    print('not unique')
else:
    print('unique')
    print(int(ans1))





