def f(sl):
    sl.sort(key=lambda s:(s[1],-s[0]))
    tl  = sorted(list(set([s[0] for s in sl] + [s[1] for s in sl])))
    cd  = {tl[i]:i for i in range(len(tl))}
    csl = [[] for i in range(len(tl))]
    for s0,s1 in sl:
        csl[cd[s1]].append(cd[s0])
    # start dp!
    n   = len(tl)
    dp  = [[len(csl[0])]] #dp[0][0]=1 or 0
    for r in range(1,len(tl)):
        dp.append([i for i in dp[-1]]+[0])
        for l in csl[r]:  #use this to update all before!
            dp[r][l] += 1
            for x in range(l-1,-1,-1):    #use this
                dp[r][x] = max(dp[r][x],dp[r][l]+dp[l-1][x])    #x<l
    return dp[-1][0]

T = int(input())
for i in range(T):
    n  =  int(input())
    ll = [list(map(int,input().split())) for _ in range(n)]
    print(f(ll))

