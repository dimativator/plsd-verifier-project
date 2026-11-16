Str=input()
ss=[int(s) for s in Str.split() if s.isdigit()]
p=ss[0]
n=ss[1]
ll=[]
for i in range(n):
    x=int(input())
    r=x%p
    if r not in ll:
        ll.append(r)
    else:
        print(i+1)
        break
else:
    print(-1)
