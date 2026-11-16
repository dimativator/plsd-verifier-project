for _ in range(int(input())):
    n = int(input())
    u = list(map(int, input().split()))
    s = list(map(int, input().split()))
    p = max(u)
    l = [[] for i in range(p)]
    for i in range(n):
        l[u[i]-1].append(s[i])
    l.sort(key = len, reverse = True)
    for i in range(p):
        l[i].sort(reverse = True)
        for j in range(1, len(l[i])):
            l[i][j]+=l[i][j-1]
    ans = []
    for i in range(1, n+1):
        res = 0
        for j in range(p):
            x = len(l[j])
            if i<=x:
                res+=l[j][x-x%i-1]
            else:
                break
        ans.append(res)
    print(*ans)
    
                
                
                
                
        
            
    