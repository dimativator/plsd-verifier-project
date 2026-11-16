#dt = {} for i in x: dt[i] = dt.get(i,0)+1
import sys;input = sys.stdin.readline
inp,ip = lambda :int(input()),lambda :[int(w) for w in input().split()]

for _ in range(inp()):
    a,b,n,m = ip()
    if a+b < n+m:
        print("No")
        continue
    no = min(n,m)
    if a < no or b < no:
        print("No")
        continue
    a,b,n,m = a-no,b-no,n-no,m-no
    if n:
        if a+b >= n:
            print("Yes")
        else:
            print("No")
    elif m:
        if min(a,b) >= m:
            print("Yes")
        else:
            print("No")
    else:
        print("Yes")
