cases = int(input())
for t in range(cases):
    n,m = list(map(int,input().split()))
    a = [list(map(int,input().split())) for i in range(n)]
    b = [[] for i in range(n+m-1)]
    for i in range(n):
        for j in range(m):
            d = i+j
            b[d].append(a[i][j])
    centre = (n+m-1)//2
    output = 0
    for i in range(centre):
        ones = sum(b[i]) + sum(b[n+m-2-i])
        total = min(i+1,n,m)*2
        output += min(ones,total-ones)
    print(output)