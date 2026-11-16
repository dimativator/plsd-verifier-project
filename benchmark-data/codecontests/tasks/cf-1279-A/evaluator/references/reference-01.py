n = int(input())
for i in range(n):
    l = [int(k) for k in input().split()]
    l.sort()
    if l[2] <= l[1]+l[0]+1 :
    	print("YES")
    else :
    	print("NO")